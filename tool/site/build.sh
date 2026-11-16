#!/usr/bin/env bash
# Build do site swift.documentacao.dev com o Swift-DocC, saída em site/.
#
# - gera o resumo da gramática na cópia, como o bin/generate-grammar oficial, mas
#   reconhecendo os blocos "> Gramática de" e com título em português;
# - trabalha numa cópia do TSPL.docc: ali os links <doc:X#Secao> passam a apontar
#   para as âncoras dos títulos traduzidos (ancorar_links.py); o repositório
#   guarda os links iguais aos do original;
# - troca o header/footer do swift.org (scripts externos) pelos nossos:
#   aviso de página ainda em inglês + atribuição e licença;
# - redireciona / para a raiz do livro.
# Uso: tool/site/build.sh   (no macOS usa xcrun docc; no Linux, docc do toolchain)
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

DOCC=(docc)
command -v docc >/dev/null || DOCC=(xcrun docc)

tmp=$(mktemp -d)
limpar() { rm -rf "$tmp"; }
trap limpar EXIT

cp -R TSPL.docc "$tmp/TSPL.docc"
resumo="$tmp/TSPL.docc/ReferenceManual/SummaryOfTheGrammar.md"
{
    echo "# Resumo da gramática"
    echo
    echo "Leia a gramática formal completa."
    echo
    for cap in LexicalStructure Types Expressions Statements Declarations Attributes Patterns GenericParametersAndArguments; do
        sed 's/^> Grammar of /> Gramática de /' "TSPL.docc/ReferenceManual/$cap.md" \
            | awk '/^# / { sub("#", "##"); print; print "" }
                   /^> Gramática de / { g = 1 }
                   g && /^>/ { print }
                   g && /^$/ { g = 0; print "" }'
    done
} > "$resumo"
python3 tool/traducao/ancorar_links.py "$tmp/TSPL.docc"

em_ingles=$(python3 - <<'PY'
import json, sys
sys.path.insert(0, 'tool/traducao')
from comum import capitulos, traduzido, ROOT
print(json.dumps({p.stem.lower(): str(p.relative_to(ROOT)) for p in capitulos()
                  if not traduzido(p.read_text()) and p.stem != 'SummaryOfTheGrammar'}))
PY
)
python3 -c "import sys; t=open('tool/site/header.html').read().replace('__EM_INGLES__', sys.argv[1]); open(sys.argv[2],'w').write(t)" "$em_ingles" "$tmp/TSPL.docc/header.html"
cp tool/site/footer.html "$tmp/TSPL.docc/footer.html"

rm -rf site
"${DOCC[@]}" convert \
    --experimental-enable-custom-templates \
    --transform-for-static-hosting \
    --output-path site \
    "$tmp/TSPL.docc"
python3 tool/site/interface.py site
find site -name "*.html" -exec sed -i.bak 's/<html lang="en-US"/<html lang="pt-BR"/' {} + && find site -name "*.bak" -delete
echo "site/ pronto ($(find site -type f | wc -l | tr -d ' ') arquivos)"
