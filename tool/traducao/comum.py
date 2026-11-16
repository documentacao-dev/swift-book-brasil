"""Funções comuns aos scripts de tradução do livro do Swift."""
import re
import subprocess
from pathlib import Path

from slug import slug

ROOT = Path(__file__).resolve().parents[2]
DOCC = ROOT / 'TSPL.docc'
BASE = (ROOT / 'tool' / 'traducao' / 'ultimo-sync-upstream.txt').read_text().strip()
MARCADOR = '<!-- ia-translate: true -->'
CERCA = re.compile(r'^```.*?^```', re.S | re.M)
TITULO = re.compile(r'^(#{2,6})\s+(.*?)\s*$', re.M)


def traduzido(texto):
    return texto.rstrip().endswith(MARCADOR)


def ingles(caminho):
    """Texto do arquivo no commit do upstream registrado (None se não existe)."""
    rel = Path(caminho).resolve().relative_to(ROOT)
    r = subprocess.run(['git', 'show', f'{BASE}:{rel}'], cwd=ROOT, capture_output=True, text=True)
    return None if r.returncode else r.stdout


def titulos(texto):
    return [m.group(2) for m in TITULO.finditer(CERCA.sub('', texto))]


def capitulos(raiz=None):
    return sorted(Path(raiz or DOCC).rglob('*.md'))
