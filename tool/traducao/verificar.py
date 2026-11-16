#!/usr/bin/env python3
"""Confere os capítulos traduzidos do livro do Swift contra o inglês.

Para cada TSPL.docc/**/*.md que termina com `<!-- ia-translate: true -->`:

- blocos de código idênticos e na mesma ordem;
- links <doc:Capitulo#Ancora> idênticos ao inglês, âncora inclusa (a troca
  para a âncora traduzida só acontece numa cópia, no build: ancorar_links.py);
- URLs de links, diretivas do DocC (@Metadata, @Options...) e comentários HTML idênticos;
- mesmo número de títulos e de notas (`> Nota:`...);
- pouca prosa sobrando em inglês.

Depois, roda o DocC e falha se algum link <doc:...#...> não resolver.
O inglês vem do commit em tool/traducao/ultimo-sync-upstream.txt.
Uso: python3 tool/traducao/verificar.py [--sem-build] [caminhos...]
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from ancorar_links import reescrever
from comum import MARCADOR, CERCA, DOCC, ROOT, capitulos, ingles, titulos, traduzido

DOC = re.compile(r'<doc:([A-Za-z]+)(#[^>]+)?>')
URL = re.compile(r'\]\(([^)\s]+)')
DIRETIVA = re.compile(r'^\s*@[A-Z]\w*.*$', re.M)
ASIDE = re.compile(r'^> [A-Z][\w -]*:', re.M)
EN = set('the and of to is are you your this that with for in it be can when '
         'will from have which an by on as at or'.split())


def sem_codigo(t):
    return CERCA.sub('', t)


def conferir(p):
    erros, avisos = [], []
    pt = p.read_text()
    en = ingles(p)
    if en is None:
        return [f'{p.relative_to(ROOT)}: não existe no upstream']
    if CERCA.findall(en) != CERCA.findall(pt):
        a, b = CERCA.findall(en), CERCA.findall(pt)
        erros.append(f'blocos de código: {len(a)} no inglês, {len(b)} na tradução'
                     + (' (conteúdo diferente)' if len(a) == len(b) else ''))
    se, sp = sem_codigo(en), sem_codigo(pt)
    if DOC.findall(se) != DOC.findall(sp):
        erros.append('links <doc:...> diferentes do inglês (âncora inclusa: fica a do original)')
    if URL.findall(se) != URL.findall(sp):
        erros.append('URLs de links diferentes do inglês')
    coment = re.compile(r'<!--.*?-->', re.S)
    a = coment.findall(se)
    b = [c for c in coment.findall(sp) if c != MARCADOR]
    if a != b:
        erros.append(f'comentários HTML diferentes do inglês ({len(a)} no inglês, {len(b)} na tradução): '
                     'conteúdo escondido no original não pode aparecer, nem o contrário')
    if DIRETIVA.findall(se) != DIRETIVA.findall(sp):
        erros.append('diretivas do DocC (@...) diferentes do inglês')
    if len(titulos(en)) != len(titulos(pt)):
        erros.append(f'títulos: {len(titulos(en))} no inglês, {len(titulos(pt))} na tradução')
    else:
        for a, b in zip(titulos(en), titulos(pt)):
            if a == b and re.search(r'[A-Za-z]{3,}', re.sub(r'`[^`]*`', '', b)):
                avisos.append(f'título igual ao inglês: "{b}"')
    if len(ASIDE.findall(se)) != len(ASIDE.findall(sp)):
        erros.append(f'notas (> X:): {len(ASIDE.findall(se))} no inglês, {len(ASIDE.findall(sp))} na tradução')
    for a in ASIDE.findall(sp):
        if a in ('> Note:', '> Experiment:', '> Important:', '> Tip:', '> Warning:', '> Deprecated:'):
            avisos.append(f'nota com rótulo em inglês: {a}')
    inline = lambda t: {m.group(2).strip() for m in re.finditer(r'(`+)(.+?)\1', t, re.S)}
    sem_coment = lambda t: re.sub(r'<!--.*?-->', '', t, flags=re.S)
    for c in sorted(inline(sem_coment(sp)) - inline(sem_coment(se)))[:5]:
        avisos.append(f'código inline que não existe no inglês (traduzido?): `{c}`')
    prosa = re.sub(r'`[^`]*`|<[^>]+>|\]\([^)]*\)|<!--.*?-->', ' ', sp, flags=re.S).lower()
    palavras = re.findall(r'[a-zà-ú]+', prosa)
    taxa = sum(w in EN for w in palavras) / max(len(palavras), 1)
    if taxa > 0.08:
        erros.append(f'prosa ainda parece inglês ({taxa:.0%} de palavras comuns em inglês)')
    rel = p.relative_to(ROOT)
    for a in avisos:
        print(f'AVISO {rel}: {a}')
    return [f'{rel}: {e}' for e in erros]


def links_quebrados():
    """Roda o DocC e devolve os links <doc:X#Y> que não resolvem."""
    docc = shutil.which('docc') or 'xcrun'
    cmd = [docc] if docc != 'xcrun' else ['xcrun', 'docc']
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / 'TSPL.docc'
        shutil.copytree(DOCC, copia)
        reescrever(copia)
        r = subprocess.run(cmd + ['convert', str(copia), '--output-path', str(Path(tmp) / 'out')],
                           capture_output=True, text=True)
    saida = r.stdout + r.stderr
    nomes = {p.stem for p in capitulos()}
    ruins = set()
    for m in re.finditer(r"warning: '([^']+)' doesn't exist at '/The-Swift-Programming-Language/?(\w*)'", saida):
        alvo = m.group(1)
        if re.fullmatch(r'[A-Za-z0-9%\w.-]+', alvo) and alvo != 'SummaryOfTheGrammar':
            ruins.add(f'{m.group(2)}: <doc:...#{alvo}>' if alvo not in nomes else f'{m.group(2)}: {alvo}')
    return sorted(ruins)


def main():
    args = sys.argv[1:]
    build = '--sem-build' not in args
    args = [a for a in args if a != '--sem-build']
    arquivos = [Path(a).resolve() for a in args] or [p for p in capitulos() if traduzido(p.read_text())]
    erros = [e for p in arquivos for e in conferir(p)]
    if build:
        erros += [f'link quebrado em {l}' for l in links_quebrados()]
    for e in erros:
        print('ERRO', e)
    print(f'{len(arquivos)} arquivo(s) traduzido(s), {len(erros)} erro(s)')
    sys.exit(1 if erros else 0)


if __name__ == '__main__':
    main()
