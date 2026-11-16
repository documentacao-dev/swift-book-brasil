# Compatibilidade de versões

Saiba quais funcionalidades estão disponíveis nos modos de linguagem mais antigos.

Este livro descreve o Swift 6.4,
a versão padrão do Swift incluída no Xcode 27.
Você pode usar o compilador do Swift 6.4 para compilar código
escrito em Swift 6.4, Swift 5, Swift 4.2 ou Swift 4.

Quando você usa o compilador do Swift 6.4
para compilar código que usa o modo de linguagem Swift 5,
pode usar os novos recursos do Swift 6.4:
eles ficam habilitados por padrão ou por uma upcoming feature flag.
No entanto, para habilitar a verificação estrita de concorrência,
é preciso migrar para o modo de linguagem Swift 6.4.

Além disso,
quando você usa o Xcode 15.3 para compilar código Swift 4 e Swift 4.2,
a maioria das funcionalidades do Swift 5 ainda está disponível.
Dito isso,
as alterações a seguir estão disponíveis apenas para código
que usa o modo de linguagem Swift 5 ou posterior:

- Funções que retornam um tipo opaco exigem o runtime do Swift 5.1.
- A expressão `try?` não introduz um nível extra de optional
  em expressões que já retornam optionals.
- Expressões de inicialização com literais inteiros grandes são inferidas
  como do tipo inteiro correto.
  Por exemplo, `UInt64(0xffff_ffff_ffff_ffff)` resulta no valor correto
  em vez de estourar.

Concorrência exige o modo de linguagem Swift 5
e uma versão da biblioteca padrão do Swift
que forneça os tipos de concorrência correspondentes.
Nas plataformas da Apple, defina um deployment target
de pelo menos iOS 13, macOS 10.15, tvOS 13, watchOS 6 ou visionOS 1.

Um target escrito em Swift 6.4 pode depender de
um target escrito em Swift 5, Swift 4.2 ou Swift 4,
e vice-versa.
Isso significa que, se você tiver um projeto grande
dividido em vários frameworks,
pode migrar seu código para uma versão mais nova da linguagem
um framework por vez.

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->

<!-- ia-translate: true -->
