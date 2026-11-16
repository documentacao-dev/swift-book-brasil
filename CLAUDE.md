# CLAUDE.md

Tradução PT-BR de **The Swift Programming Language** (o "livro do Swift", TSPL), fork de `swiftlang/swift-book`, parte da org [`documentacao-dev`](https://github.com/documentacao-dev). Publicado em https://swift.documentacao.dev.

- Conteúdo traduzível: `TSPL.docc/**/*.md`, traduzido no lugar. Primeiro as boas-vindas e o Guia da linguagem até Closures; o Manual de referência por último.
- Site: Swift-DocC. `tool/site/build.sh` gera `site/` (resumo da gramática, header/footer próprios sem os scripts do swift.org, `lang="pt-BR"`). Deploy no site Firebase `swift-documentacao` (projeto transliteradu).
- Sync: branch `sync/upstream-AAAA-MM` com merge de `upstream/main`, retradução só do que mudou, `python3 tool/traducao/ancorar_links.py`, atualização de `tool/traducao/ultimo-sync-upstream.txt`.

## Modelo da tradução: sempre Haiku

Toda tradução e retradução de página roda no **Haiku** (`model: haiku`, agente `.claude/agents/traduzir-pt-br.md`), local ou na nuvem. O modelo principal da sessão só orquestra (git, scripts, commits, PR). A revisão é de um subagente Sonnet de contexto limpo, com 100% da prosa lida lado a lado e `COBERTURA` declarada; lotes de no máximo ~1.500 linhas por revisor.

## Convenções do livro (DocC)

- Marcador: **última** linha do arquivo `<!-- ia-translate: true -->` (o DocC exige que o arquivo comece pelo título).
- Blocos de código, código inline, diretivas `@...`, comentários HTML e URLs ficam idênticos.
- Notas: `> Nota:`, `> Experimente:`, `> Importante:` (o DocC aceita rótulo próprio).
- Âncoras: o DocC gera a âncora da seção a partir do texto do título e não aceita id próprio. Depois de traduzir (e depois de cada sync), rode `python3 tool/traducao/ancorar_links.py`: ele troca, em todos os capítulos, `<doc:Capitulo#Ancora-em-ingles>` pela âncora do título traduzido.
- `python3 tool/traducao/verificar.py` confere tudo contra o inglês do commit em `ultimo-sync-upstream.txt` e roda o DocC para achar link `<doc:...#...>` quebrado.

## Aviso de página não traduzida

`tool/site/build.sh` gera `TSPL.docc/header.html` a partir de `tool/site/header.html` com a lista de capítulos sem o marcador; um script na página mostra, no topo, que ela ainda está em inglês, com link para o arquivo no GitHub. Ao traduzir um capítulo, o aviso some no próximo build.
