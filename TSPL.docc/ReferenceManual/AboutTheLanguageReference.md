# Sobre a referência da linguagem

Leia a notação que a gramática formal usa.

Esta parte do livro descreve a gramática formal da linguagem de programação Swift.
A gramática descrita aqui serve para ajudar você a entender a linguagem
com mais detalhes, e não para permitir que você implemente diretamente um parser ou um compilador.

A linguagem Swift é relativamente pequena, porque vários tipos, funções e operadores comuns
que aparecem praticamente em todo código Swift
são, na verdade, definidos na biblioteca padrão do Swift. Embora esses tipos, funções
e operadores não façam parte da própria linguagem Swift,
eles são usados extensivamente nas discussões e nos exemplos de código desta parte do livro.

## Como ler a gramática

A notação usada para descrever a gramática formal da linguagem de programação Swift
segue algumas convenções:

- Uma seta (→) marca as produções da gramática e pode ser lida como “pode consistir em”.
- Categorias sintáticas são indicadas por texto em *itálico* e aparecem dos dois lados
  de uma regra de produção da gramática.
- Palavras literais e pontuação são indicadas por texto em **negrito com fonte monoespaçada**
  e aparecem apenas do lado direito de uma regra de produção da gramática.
- Produções alternativas são separadas por barras verticais (|). Quando as produções alternativas são longas demais para ler com facilidade,
  elas são divididas em várias regras de produção, em novas linhas.
- Em alguns casos, texto em fonte regular é usado para descrever o lado direito
  de uma regra de produção da gramática.
- Categorias sintáticas e literais opcionais são marcadas por um ponto de interrogação
  no final, *?*.

Como exemplo, a gramática de um bloco getter-setter é definida assim:

> Gramática de um bloco getter-setter:
>
> *getter-setter-block* → **`{`** *getter-clause* *setter-clause*_?_ **`}`** | **`{`** *setter-clause* *getter-clause* **`}`**

Essa definição indica que um bloco getter-setter pode consistir em uma cláusula getter
seguida por uma cláusula setter opcional, delimitadas por chaves,
*ou* em uma cláusula setter seguida por uma cláusula getter, delimitadas por chaves.
A produção acima equivale a estas duas produções,
em que as alternativas são escritas explicitamente:

> Gramática de um bloco getter-setter:
>
>
> *getter-setter-block* → **`{`** *getter-clause* *setter-clause*_?_ **`}`** \
> *getter-setter-block* → **`{`** *setter-clause* *getter-clause* **`}`**

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
