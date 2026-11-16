#!/usr/bin/env bash
# Build do site swift.documentacao.dev com o Swift-DocC, saída em site/.
#
# - gera o resumo da gramática (bin/generate-grammar), como o publish-book oficial;
# - troca o header/footer do swift.org (scripts externos) pelos nossos:
#   aviso de página ainda em inglês + atribuição e licença;
# - redireciona / para a raiz do livro.
# Uso: tool/site/build.sh   (no macOS usa xcrun docc; no Linux, docc do toolchain)
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

DOCC=(docc)
command -v docc >/dev/null || DOCC=(xcrun docc)

resumo="TSPL.docc/ReferenceManual/SummaryOfTheGrammar.md"
limpar() { rm -f TSPL.docc/header.html TSPL.docc/footer.html.bak "$resumo"; [ -f footer.orig ] && mv footer.orig TSPL.docc/footer.html; true; }
trap limpar EXIT

bin/generate-grammar

em_ingles=$(python3 - <<'PY'
import json, sys
sys.path.insert(0, 'tool/traducao')
from comum import capitulos, traduzido, ROOT
print(json.dumps({p.stem.lower(): str(p.relative_to(ROOT)) for p in capitulos()
                  if not traduzido(p.read_text()) and p.stem != 'SummaryOfTheGrammar'}))
PY
)
python3 -c "import sys; t=open('tool/site/header.html').read().replace('__EM_INGLES__', sys.argv[1]); open('TSPL.docc/header.html','w').write(t)" "$em_ingles"
mv TSPL.docc/footer.html footer.orig
cp tool/site/footer.html TSPL.docc/footer.html

rm -rf site
"${DOCC[@]}" convert \
    --experimental-enable-custom-templates \
    --transform-for-static-hosting \
    --output-path site \
    TSPL.docc
find site -name "*.html" -exec sed -i.bak 's/<html lang="en-US"/<html lang="pt-BR"/' {} + && find site -name "*.bak" -delete
echo "site/ pronto ($(find site -type f | wc -l | tr -d ' ') arquivos)"
