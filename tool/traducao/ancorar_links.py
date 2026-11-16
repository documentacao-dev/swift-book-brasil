#!/usr/bin/env python3
"""Reescreve os links <doc:Capitulo#Secao> para a âncora do título traduzido.

O Swift-DocC gera a âncora de cada seção a partir do texto do título e não
aceita id próprio. Quando um capítulo é traduzido, as âncoras mudam e todo
link <doc:Capitulo#Ancora-em-ingles>, em qualquer capítulo, precisa apontar
para a âncora nova. O script compara os títulos de cada capítulo traduzido
com os do inglês (mesma ordem) e troca as âncoras em todos os .md do TSPL.docc.
Rode depois de traduzir e depois de cada sync com o upstream (o upstream
traz links com âncoras em inglês).

Uso: python3 tool/traducao/ancorar_links.py
"""
import re
import sys

from comum import capitulos, ingles, slug, titulos, traduzido

LINK = re.compile(r'<doc:([A-Za-z]+)#([^>]+)>')


def main():
    mapas = {}
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
        mapas[p.stem] = {slug(a): slug(b) for a, b in zip(t_en, t_pt) if slug(a) != slug(b)}
    trocas = 0
    for p in capitulos():
        texto = p.read_text()

        def trocar(m):
            nonlocal trocas
            novo = mapas.get(m.group(1), {}).get(m.group(2))
            if novo is None:
                return m.group(0)
            trocas += 1
            return f'<doc:{m.group(1)}#{novo}>'
        novo_texto = LINK.sub(trocar, texto)
        if novo_texto != texto:
            p.write_text(novo_texto)
    print(f'{len(mapas)} capítulo(s) traduzido(s), {trocas} link(s) reescrito(s)')


if __name__ == '__main__':
    sys.exit(main())
