#!/usr/bin/env python3
"""Copia, byte a byte, os comentários HTML do inglês para a tradução.

Comentários HTML do livro são testes e notas internas que o site não mostra;
eles têm de ficar idênticos ao original (o verificar.py cobra). Quando a
tradução tem o mesmo número de comentários, este script troca cada um pelo do
inglês, na ordem. Se o número for diferente, não mexe (precisa de correção à mão).

Uso: python3 tool/traducao/restaurar_comentarios.py <arquivos...>
"""
import re
import sys
from pathlib import Path

from comum import MARCADOR, ingles

COMENT = re.compile(r'<!--.*?-->', re.S)


def restaurar(p):
    pt = p.read_text()
    en = ingles(p)
    a = COMENT.findall(en)
    b = [c for c in COMENT.findall(pt) if c != MARCADOR]
    if len(a) != len(b):
        return f'{p}: {len(a)} comentários no inglês, {len(b)} na tradução; corrija à mão'
    trocas = iter(a)
    novo = COMENT.sub(lambda m: m.group(0) if m.group(0) == MARCADOR else next(trocas), pt)
    if novo != pt:
        p.write_text(novo)
        return f'{p}: {sum(x != y for x, y in zip(a, b))} comentário(s) restaurado(s)'
    return f'{p}: ok'


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        print(restaurar(Path(arg).resolve()))
