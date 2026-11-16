#!/usr/bin/env python3
"""Traduz a interface do Swift-DocC (Documentation, Topics, Filter, On This Page...).

O swift-docc-render embute no JavaScript o JSON de cada idioma da interface e
não tem pt-BR. Este script troca, no site já gerado, os textos do en-US pelos
de tool/site/interface-pt-BR.json (mesmas chaves de interface-en-US.json, que é
a referência extraída do render). Chave sem tradução continua em inglês.

Uso: python3 tool/site/interface.py site
"""
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
BLOCO = re.compile(r"JSON\.parse\('((?:[^'\\]|\\.)*)'\)")


def js_para_texto(lit):
    return re.sub(r"\\([\\'])", r'\1', lit)


def texto_para_js(t):
    return t.replace('\\', '\\\\').replace("'", "\\'")


def aplicar(d, pt, prefixo=''):
    trocas = 0
    for k, v in d.items():
        chave = f'{prefixo}.{k}' if prefixo else k
        if isinstance(v, dict):
            trocas += aplicar(v, pt, chave)
        elif chave in pt and isinstance(v, str):
            d[k] = pt[chave]
            trocas += 1
    return trocas


def main(site):
    pt = json.loads((AQUI / 'interface-pt-BR.json').read_text())
    total = 0
    for js in Path(site, 'js').glob('index.*.js'):
        fonte = js.read_text()

        def trocar(m):
            nonlocal total
            try:
                d = json.loads(js_para_texto(m.group(1)))
            except ValueError:
                return m.group(0)
            if not (isinstance(d, dict) and isinstance(d.get('documentation'), dict)
                    and d['documentation'].get('title') == 'Documentation'):
                return m.group(0)
            total += aplicar(d, pt)
            return "JSON.parse('" + texto_para_js(json.dumps(d, ensure_ascii=False, separators=(',', ':'))) + "')"
        js.write_text(BLOCO.sub(trocar, fonte))
    if not total:
        sys.exit('interface.py: JSON en-US do DocC não encontrado (o render mudou?)')
    print(f'interface: {total} texto(s) em português')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'site')
