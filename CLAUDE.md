# CLAUDE.md

Tradução PT-BR de **The Swift Programming Language** (o "livro do Swift", TSPL), fork de `swiftlang/swift-book`, parte da org [`documentacao-dev`](https://github.com/documentacao-dev). Publicado em https://swift.documentacao.dev.

- Conteúdo traduzível: `TSPL.docc/**/*.md`, traduzido no lugar. Primeiro as boas-vindas e o Guia da linguagem até Closures; o Manual de referência por último.
- Site: Swift-DocC. `tool/site/build.sh` gera `site/` (resumo da gramática, header/footer próprios sem os scripts do swift.org, `lang="pt-BR"`). Deploy no site Firebase `swift-documentacao` (projeto transliteradu).
- Sync: branch `sync/upstream-AAAA-MM` com merge de `upstream/main`, retradução só do que mudou, atualização de `tool/traducao/ultimo-sync-upstream.txt`.

## Modelo da tradução: sempre Haiku

Toda tradução e retradução de página roda no **Haiku** (`model: haiku`, agente `.claude/agents/traduzir-pt-br.md`), local ou na nuvem. O modelo principal da sessão só orquestra (git, scripts, commits, PR). A revisão é de um subagente Sonnet de contexto limpo, com 100% da prosa lida lado a lado e `COBERTURA` declarada; lotes de no máximo ~1.500 linhas por revisor.

## Convenções do livro (DocC)

- Marcador: **última** linha do arquivo `<!-- ia-translate: true -->` (o DocC exige que o arquivo comece pelo título).
- Blocos de código, código inline, diretivas `@...`, comentários HTML e URLs ficam idênticos.
- Notas: `> Nota:`, `> Experimente:`, `> Importante:` (o DocC aceita rótulo próprio).
- Âncoras: o DocC gera a âncora da seção a partir do texto do título e não aceita id próprio. No repositório, todo `<doc:Capitulo#Ancora>` fica IGUAL ao original em inglês (o verificar.py cobra), inclusive nos capítulos traduzidos; assim os capítulos ainda em inglês ficam idênticos ao upstream e o sync não dá conflito. Só no build (`tool/site/build.sh`) e no verificador, numa cópia temporária do TSPL.docc, o `ancorar_links.py` troca as âncoras pelas dos títulos traduzidos. Nunca rode a troca no repositório.
- `python3 tool/traducao/verificar.py` confere tudo contra o inglês do commit em `ultimo-sync-upstream.txt` e roda o DocC para achar link `<doc:...#...>` quebrado.

## Interface do site

O swift-docc-render não tem pt-BR. `tool/site/interface.py` (chamado no build) troca, no JavaScript gerado, os textos de interface do en-US (Documentation, Topics, Filter, On This Page...) pelos de `tool/site/interface-pt-BR.json`. A referência em inglês é `tool/site/interface-en-US.json`; se o render ganhar chaves novas, extraia de novo e traduza (Haiku).

## Aviso de página não traduzida

`tool/site/build.sh` gera `TSPL.docc/header.html` a partir de `tool/site/header.html` com a lista de capítulos sem o marcador; um script na página mostra, no topo, que ela ainda está em inglês, com link para o arquivo no GitHub. Ao traduzir um capítulo, o aviso some no próximo build.
