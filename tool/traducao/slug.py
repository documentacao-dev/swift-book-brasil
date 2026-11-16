"""Âncora que o Swift-DocC gera para um título (urlReadableFragment)."""
import re
import unicodedata


def texto_titulo(md):
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', md)
    t = re.sub(r'<doc:[^>]+>', '', t)
    return t.replace('`', '').replace('*', '')


def slug(md):
    t = texto_titulo(md).strip()
    t = re.sub(r'[\s-]+', '-', t)
    return ''.join(c for c in t if c == '-' or unicodedata.category(c)[0] not in 'PSZC')
