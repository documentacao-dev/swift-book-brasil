#!/usr/bin/env python3
"""Aponta os links <doc:Capitulo#Secao> para a âncora do título traduzido,
numa CÓPIA do TSPL.docc (nunca no repositório).

O Swift-DocC gera a âncora de cada seção a partir do texto do título e não
aceita id próprio. No repositório, todo link fica igual ao do original em
inglês (assim os capítulos ainda em inglês continuam idênticos ao upstream e o
sync não dá conflito). Na hora do build, este script compara os títulos de cada
capítulo traduzido com os do inglês (mesma ordem) e troca as âncoras na cópia.

Uso: python3 tool/traducao/ancorar_links.py <copia/TSPL.docc>
"""
import re
import sys
from pathlib import Path

from comum import DOCC, capitulos, ingles, slug, titulos, traduzido

LINK = re.compile(r'<doc:([A-Za-z]+)#([^>]+)>')


def mapas():
    """{capitulo: {ancora_en: ancora_pt}} dos capítulos traduzidos do repositório."""
    m = {}
    for p in capitulos():
        pt = p.read_text()
        if not traduzido(pt):
            continue
        en = ingles(p)
        if en is None:
            continue
        t_en, t_pt = titulos(en), titulos(pt)
        if len(t_en) != len(t_pt):
            print(f'ERRO {p.name}: {len(t_en)} títulos no inglês, {len(t_pt)} na tradução; pulei')
            continue
        m[p.stem] = {slug(a): slug(b) for a, b in zip(t_en, t_pt) if slug(a) != slug(b)}
    return m


def reescrever(copia):
    copia = Path(copia).resolve()
    if copia == DOCC.resolve():
        sys.exit('recusado: rode numa cópia do TSPL.docc, não no repositório')
    mp, trocas = mapas(), 0
    for p in capitulos(copia):
        texto = p.read_text()

        def trocar(m):
            nonlocal trocas
            novo = mp.get(m.group(1), {}).get(m.group(2))
            if novo is None:
                return m.group(0)
            trocas += 1
            return f'<doc:{m.group(1)}#{novo}>'
        novo_texto = LINK.sub(trocar, texto)
        if novo_texto != texto:
            p.write_text(novo_texto)
    print(f'{len(mp)} capítulo(s) traduzido(s), {trocas} link(s) apontado(s) para âncora em português')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    reescrever(sys.argv[1])
