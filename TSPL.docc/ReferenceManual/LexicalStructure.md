# Estrutura léxica

Use os componentes de mais baixo nível da sintaxe.

A *estrutura léxica* do Swift descreve quais sequências de caracteres
formam tokens válidos da linguagem.
Esses tokens válidos são os blocos de construção de mais baixo nível da linguagem
e são usados para descrever o restante da linguagem nos capítulos seguintes.
Um token é formado por um identificador, uma palavra-chave, pontuação, um literal ou um operador.

Na maioria dos casos, os tokens são gerados a partir dos caracteres de um arquivo-fonte do Swift
considerando a maior subcadeia possível do texto de entrada,
dentro das restrições da gramática especificada abaixo.
Esse comportamento é chamado de *longest match*
ou *maximal munch*.

## Espaço em branco e comentários

O espaço em branco tem duas funções: separar tokens no arquivo-fonte
e distinguir operadores prefixos, pós-fixos e infixos
(veja <doc:LexicalStructure#Operators>),
mas, fora isso, é ignorado.
São considerados espaço em branco os seguintes caracteres:
espaço (U+0020),
quebra de linha (U+000A),
retorno de carro (U+000D),
tabulação horizontal (U+0009),
tabulação vertical (U+000B),
avanço de página (U+000C)
e nulo (U+0000).

<!--
  Whitespace characters are listed roughly from
  most salient/common to least,
  not in order of Unicode scalar value.
-->

Comentários são tratados como espaço em branco pelo compilador.
Comentários de uma linha começam com `//`
e continuam até uma quebra de linha (U+000A) ou um retorno de carro (U+000D).
Comentários de várias linhas começam com `/*` e terminam com `*/`.
Comentários de várias linhas podem ser aninhados,
mas os marcadores de comentário precisam estar balanceados.

Comentários podem conter formatação e marcação adicionais,
como descrito na [Referência de formatação de marcação](https://developer.apple.com/library/content/documentation/Xcode/Reference/xcode_markup_formatting_ref/index.html).

> Gramática de espaço em branco:
>
> *whitespace* → *whitespace-item* *whitespace*_?_ \
> *whitespace-item* → *line-break* \
> *whitespace-item* → *inline-space* \
> *whitespace-item* → *comment* \
> *whitespace-item* → *multiline-comment* \
> *whitespace-item* → U+0000, U+000B, or U+000C
>
> *line-break* → U+000A \
> *line-break* → U+000D \
> *line-break* → U+000D followed by U+000A
>
> *inline-spaces* → *inline-space* *inline-spaces*_?_ \
> *inline-space* → U+0009 or U+0020
>
> *comment* → **`//`** *comment-text* *line-break* \
> *multiline-comment* → **`/*`** *multiline-comment-text* **`*/`**
>
> *comment-text* → *comment-text-item* *comment-text*_?_ \
> *comment-text-item* → Any Unicode scalar value except U+000A or U+000D
>
> *multiline-comment-text* → *multiline-comment-text-item* *multiline-comment-text*_?_ \
> *multiline-comment-text-item* → *multiline-comment* \
> *multiline-comment-text-item* → *comment-text-item* \
> *multiline-comment-text-item* → Any Unicode scalar value except  **`/*`** or  **`*/`**

## Identificadores

*Identificadores* começam com
uma letra maiúscula ou minúscula de A a Z,
um sublinhado (`_`),
um caractere alfanumérico Unicode não combinante no Plano Multilíngue Básico,
ou um caractere fora do Plano Multilíngue Básico
que não esteja em uma Área de Uso Privado.
Depois do primeiro caractere,
dígitos e caracteres Unicode combinantes também são permitidos.

Trate como internos os identificadores que começam com sublinhado,
os subscripts cujo primeiro rótulo de argumento começa com sublinhado
e os inicializadores cujo primeiro rótulo de argumento começa com sublinhado,
mesmo que a declaração tenha o modificador de nível de acesso `public`.
Essa convenção permite que autores de frameworks marquem parte de uma API
com a qual os clientes não devem interagir nem da qual devem depender,
mesmo quando alguma limitação exige que a declaração seja pública.
Além disso, identificadores que começam com dois sublinhados
são reservados para o compilador do Swift e para a biblioteca padrão.

Para usar uma palavra reservada como identificador
ou para incluir caracteres especiais como espaço em branco,
coloque um acento grave (\`) antes e depois dela.
Por exemplo, `class`, `100` e `model & test` não são identificadores válidos,
mas `` `class` ``, `` `100` `` e `` `model & test` `` são válidos.
Os acentos graves não são considerados parte do identificador;
`` `x` `` e `x` têm o mesmo significado.

<!--
The paragraph above produces a link-resolution warning
because of a known issue with ` in code voice.

https://github.com/swiftlang/swift-book/issues/71
https://github.com/swiftlang/swift-markdown/issues/93
-->

Um identificador bruto pode conter qualquer escalar Unicode, exceto os seguintes:

- Acento grave (`` ` ``)
- Barra invertida (`\`)
- Nulo (U+0000)
- Tabulação horizontal (U+0009)
- Quebra de linha (U+000A)
- Tabulação vertical (U+000B)
- Retorno de carro (U+000D)
- Próxima linha (U+0085)
- Espaço não separável (U+00A0)
- Marca de espaço Ogham (U+1680)
- Quad de en (U+2000)
- Quad de em (U+2001)
- Espaço de en (U+2002)
- Espaço de em (U+2003)
- Espaço de três por em (U+2004)
- Espaço de quatro por em (U+2005)
- Espaço de seis por em (U+2006)
- Espaço de figura (U+2007)
- Espaço de pontuação (U+2008)
- Espaço fino (U+2009)
- Espaço de cabelo (U+200A)
- Separador de linha (U+2028)
- Separador de parágrafo (U+2029)
- Espaço não separável estreito (U+202F)
- Espaço matemático médio (U+205F)
- Espaço ideográfico (U+3000)

<!--
The list above states the rules from SE-0451 without nested negation.
The acceptance revision (https://forums.swift.org/t/76387)
lists the rules as follows:

>>>
The only whitespace that should be permitted in a raw identifier is
`Pattern_White_Space` (which is stable), minus line/paragraph separators, and
minus any already forbidden ASCII characters (like U+0009). That leaves
{U+0020, U+200E, U+200F}.

All other `White_Space` not in the set above, as defined in the Unicode 16.0.0
standard, should be forbidden.
>>>

The list above also avoids discussing whitespace characters
using a different definition of whitespace
from what's in the Whitespace and Comments section above.

0009..000D    ; Pattern_White_Space # Cc   [5] <control-0009>..<control-000D>
0020          ; Pattern_White_Space # Zs       SPACE
0085          ; Pattern_White_Space # Cc       <control-0085>
200E..200F    ; Pattern_White_Space # Cf   [2] LEFT-TO-RIGHT MARK..RIGHT-TO-LEFT MARK
2028          ; Pattern_White_Space # Zl       LINE SEPARATOR
2029          ; Pattern_White_Space # Zp       PARAGRAPH SEPARATOR

0009..000D    ; White_Space # Cc   [5] <control-0009>..<control-000D>
0020          ; White_Space # Zs       SPACE
0085          ; White_Space # Cc       <control-0085>
00A0          ; White_Space # Zs       NO-BREAK SPACE
1680          ; White_Space # Zs       OGHAM SPACE MARK
2000..200A    ; White_Space # Zs  [11] EN QUAD..HAIR SPACE
2028          ; White_Space # Zl       LINE SEPARATOR
2029          ; White_Space # Zp       PARAGRAPH SEPARATOR
202F          ; White_Space # Zs       NARROW NO-BREAK SPACE
205F          ; White_Space # Zs       MEDIUM MATHEMATICAL SPACE
3000          ; White_Space # Zs       IDEOGRAPHIC SPACE

From https://www.unicode.org/Public/UCD/latest/ucd/PropList.txt
-->

Identificadores brutos podem conter espaço em branco,
mas não podem consistir apenas de espaço em branco.
Em um identificador bruto,
uma marca de esquerda para direita (U+200E) ou uma marca de direita para esquerda (U+200F)
é permitida e considerada espaço em branco.
Identificadores brutos podem conter caracteres de operador,
como descrito em <doc:LexicalStructure#Operators>,
mas não podem consistir apenas de caracteres de operador.

> Nota:
> Antes do Swift 6.2,
> escrever acentos graves antes e depois de um identificador
> era conhecido como *identificador escapado*,
> e era limitado a usar uma palavra-chave como identificador.

Dentro de uma closure sem nomes explícitos de parâmetros,
os parâmetros são nomeados implicitamente como `$0`, `$1`, `$2`, e assim por diante.
Esses nomes são identificadores válidos dentro do escopo da closure.

O compilador sintetiza identificadores que começam com cifrão (`$`)
para propriedades que têm uma projeção de property wrapper.
Seu código pode interagir com esses identificadores,
mas você não pode declarar identificadores com esse prefixo.
Para mais informações, veja a seção <doc:Attributes#propertyWrapper>
do capítulo <doc:Attributes>.

<!--
  The cross reference above includes both the section and chapter because,
  even though "propertyWrapper" is the title of the section,
  the section name isn't title case so it doesn't necessarily look like a title.
-->

<!--
The formal grammar below for 'identifier'
produces a link-resolution warning
because of a known issue with ` in code voice.

https://github.com/swiftlang/swift-book/issues/71
https://github.com/swiftlang/swift-markdown/issues/93
-->

> Gramática de um identificador:
>
> *identifier* → *identifier-head* *identifier-characters*_?_ \
> *identifier* → *raw-identifier* \
> *identifier* → *implicit-parameter-name* \
> *identifier* → *property-wrapper-projection* \
> *identifier-list* → *identifier* | *identifier* **`,`** *identifier-list*
>
> *identifier-head* → Upper- or lowercase letter A through Z \
> *identifier-head* → **`_`** \
> *identifier-head* → U+00A8, U+00AA, U+00AD, U+00AF, U+00B2–U+00B5, or U+00B7–U+00BA \
> *identifier-head* → U+00BC–U+00BE, U+00C0–U+00D6, U+00D8–U+00F6, or U+00F8–U+00FF \
> *identifier-head* → U+0100–U+02FF, U+0370–U+167F, U+1681–U+180D, or U+180F–U+1DBF \
> *identifier-head* → U+1E00–U+1FFF \
> *identifier-head* → U+200B–U+200D, U+202A–U+202E, U+203F–U+2040, U+2054, or U+2060–U+206F \
> *identifier-head* → U+2070–U+20CF, U+2100–U+218F, U+2460–U+24FF, or U+2776–U+2793 \
> *identifier-head* → U+2C00–U+2DFF or U+2E80–U+2FFF \
> *identifier-head* → U+3004–U+3007, U+3021–U+302F, U+3031–U+303F, or U+3040–U+D7FF \
> *identifier-head* → U+F900–U+FD3D, U+FD40–U+FDCF, U+FDF0–U+FE1F, or U+FE30–U+FE44 \
> *identifier-head* → U+FE47–U+FFFD \
> *identifier-head* → U+10000–U+1FFFD, U+20000–U+2FFFD, U+30000–U+3FFFD, or U+40000–U+4FFFD \
> *identifier-head* → U+50000–U+5FFFD, U+60000–U+6FFFD, U+70000–U+7FFFD, or U+80000–U+8FFFD \
> *identifier-head* → U+90000–U+9FFFD, U+A0000–U+AFFFD, U+B0000–U+BFFFD, or U+C0000–U+CFFFD \
> *identifier-head* → U+D0000–U+DFFFD or U+E0000–U+EFFFD
>
> *identifier-character* → *decimal-digit* \
> *identifier-character* → U+0300–U+036F, U+1DC0–U+1DFF, U+20D0–U+20FF, or U+FE20–U+FE2F \
> *identifier-character* → *identifier-head* \
> *identifier-characters* → *identifier-character* *identifier-characters*_?_
>
> *implicit-parameter-name* → **`$`** *decimal-digits* \
> *property-wrapper-projection* → **`$`** *identifier-characters*
>
> *raw-identifier* → **`` ` ``** *raw-identifier-characters* **`` ` ``** \
> *raw-identifier-character* → Any Unicode scalar value except  **`` ` ``**,  **`\`**, U+0000, U+000A, or U+000D
> *raw-identifier-characters* → *raw-identifier-character* *raw-identifier-characters*_?_

## Palavras-chave e pontuação

As palavras-chave a seguir são reservadas e não podem ser usadas como identificadores,
a menos que sejam escapadas com acentos graves,
como descrito acima em <doc:LexicalStructure#Identifiers>.
Palavras-chave diferentes de `inout`, `var` e `let`
podem ser usadas como nomes de parâmetros
em uma declaração ou chamada de função
sem serem escapadas com acentos graves.
Quando um membro tem o mesmo nome de uma palavra-chave,
as referências a esse membro não precisam ser escapadas com acentos graves,
exceto quando há ambiguidade entre se referir ao membro
e usar a palavra-chave:
por exemplo, `self`, `Type` e `Protocol` têm significado especial
em uma expressão de membro explícita,
então precisam ser escapados com acentos graves nesse contexto.

<!--
  - test: `keywords-without-backticks`

  ```swifttest
  -> func f(x: Int, in y: Int) {
        print(x+y)
     }
  ```
-->

<!--
  - test: `var-requires-backticks`

  ```swifttest
  -> func g(`var` x: Int) {}
  -> func f(var x: Int) {}
  !$ warning: 'var' in this position is interpreted as an argument label
  !! func f(var x: Int) {}
  !!        ^~~
  !!        `var`
  ```
-->

<!--
  - test: `let-requires-backticks`

  ```swifttest
  -> func g(`let` x: Int) {}
  -> func f(let x: Int) {}
  !$ warning: 'let' in this position is interpreted as an argument label
  !! func f(let x: Int) {}
  !!        ^~~
  !!        `let`
  ```
-->

<!--
  - test: `inout-requires-backticks`

  ```swifttest
  -> func g(`inout` x: Int) {}
  -> func f(inout x: Int) {}
  !$ error: 'inout' before a parameter name is not allowed, place it before the parameter type instead
  !! func f(inout x: Int) {}
  !!        ^~~~~
  !!                 inout
  ```
-->

<!--
  NOTE: This list of language keywords and punctuation
  is derived from the file "swift/include/swift/Parse/Tokens.def"
  and from "utils/gyb_syntax_support/Token.py",
  which generates the TokenKinds.def file.

  Last updated at Swift commit 2f1987567f5, for Swift 5.4.
-->

- Palavras-chave usadas em declarações:
  `associatedtype`,
  `borrowing`,
  `class`,
  `consuming`,
  `deinit`,
  `enum`,
  `extension`,
  `fileprivate`,
  `func`,
  `import`,
  `init`,
  `inout`,
  `internal`,
  `let`,
  `nonisolated`,
  `open`,
  `operator`,
  `precedencegroup`,
  `private`,
  `protocol`,
  `public`,
  `rethrows`,
  `static`,
  `struct`,
  `subscript`,
  `typealias`,
  e `var`.

<!--
  Token.py doesn't include 'open' but DeclNodes.py does.
-->

- Palavras-chave usadas em instruções:
  `break`,
  `case`,
  `catch`,
  `continue`,
  `default`,
  `defer`,
  `do`,
  `else`,
  `fallthrough`,
  `for`,
  `guard`,
  `if`,
  `in`,
  `repeat`,
  `return`,
  `switch`,
  `throw`,
  `where`,
  e `while`.
- Palavras-chave usadas em expressões e tipos:
  `Any`,
  `as`,
  `await`,
  `catch`,
  `false`,
  `is`,
  `nil`,
  `rethrows`,
  `self`,
  `Self`,
  `super`,
  `throw`,
  `throws`,
  `true`,
  e `try`.
- Palavras-chave usadas em padrões:
  `_`.
- Palavras-chave que começam com sinal de número (`#`):
  `#available`,
  `#colorLiteral`,
  `#else`,
  `#elseif`,
  `#endif`,
  `#fileLiteral`,
  `#if`,
  `#imageLiteral`,
  `#keyPath`,
  `#selector`,
  `#sourceLocation`,
  `#unavailable`.

> Nota:
> Antes do Swift 5.9,
> as seguintes palavras-chave eram reservadas:
> `#column`,
> `#dsohandle`,
> `#error`,
> `#fileID`,
> `#filePath`,
> `#file`,
> `#function`,
> `#line`,
> e `#warning`.
> Agora elas são implementadas como macros na biblioteca padrão do Swift:
> [`column`](https://developer.apple.com/documentation/swift/column()),
> [`dsohandle`](https://developer.apple.com/documentation/swift/dsohandle()),
> [`error(_:)`](https://developer.apple.com/documentation/swift/error(_:)),
> [`fileID`](https://developer.apple.com/documentation/swift/fileID()),
> [`filePath`](https://developer.apple.com/documentation/swift/filePath()),
> [`file`](https://developer.apple.com/documentation/swift/file()),
> [`function`](https://developer.apple.com/documentation/swift/function()),
> [`line`](https://developer.apple.com/documentation/swift/line()),
> e [`warning(_:)`](https://developer.apple.com/documentation/swift/warning(_:)).

<!--
  Token.py includes #assert,
  which looks like it's part of an experimental feature
  based on the pound_assert_disabled diagnostic's error message:
  #assert is an experimental feature that is currently disabled
-->

<!--
  Token.py includes #fileID,
  which looks like it's part of a future feature related to
  -enable-experimental-concise-pound-file (see also Swift commit 0e569f5d9e66)
-->

<!--
  Token.py includes 'yield' as a keyword,
  which looks like it's related to a future feature around memory ownership.
-->

- Palavras-chave reservadas em contextos específicos:
  `associativity`,
  `async`,
  `convenience`,
  `didSet`,
  `dynamic`,
  `final`,
  `get`,
  `indirect`,
  `infix`,
  `lazy`,
  `left`,
  `mutating`,
  `none`,
  `nonmutating`,
  `optional`,
  `override`,
  `package`,
  `postfix`,
  `precedence`,
  `prefix`,
  `Protocol`,
  `required`,
  `right`,
  `set`,
  `some`,
  `Type`,
  `unowned`,
  `weak`,
  e `willSet`.
  Fora do contexto em que aparecem na gramática,
  elas podem ser usadas como identificadores.

<!--
  NOTE: The list of context-sensitive keywords above
  is derived from the file "swift/include/swift/AST/Attr.def"
  where they're marked CONTEXTUAL_SIMPLE_DECL_ATTR.
  However, not all context-sensitive keywords appear there;
-->

Os tokens a seguir são reservados como pontuação
e não podem ser usados como operadores personalizados:
`(`, `)`, `{`, `}`, `[`, `]`,
`.`, `,`, `:`, `;`, `=`, `@`, `#`,
`&` (como operador prefixo), `->`, `` ` ``,
`?` e `!` (como operador pós-fixo).

## Literais

Um *literal* é a representação, no código-fonte,
de um valor de um tipo, como um número ou uma string.

São exemplos de literais:

```swift
42               // Integer literal
3.14159          // Floating-point literal
"Hello, world!"  // String literal
/Hello, .*/      // Regular expression literal
true             // Boolean literal
```

<!--
  - test: `basic-literals`

  ```swifttest
  >> let r0 =
  -> 42               // Integer literal
  >> let r1 =
  -> 3.14159          // Floating-point literal
  >> let r2 =
  -> "Hello, world!"  // String literal
  >> let r4 =
  -> /Hello, .*/      // Regular expression literal
  >> let r3 =
  -> true             // Boolean literal
  >> for x in [r0, r1, r2, r3] as [Any] { print(type(of: x)) }
  << Int
  << Double
  << String
  << Bool
  ```
-->

<!--
  Refactor the above if possible to avoid using bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

Um literal não tem tipo por conta própria.
Em vez disso, ele é analisado como tendo precisão infinita,
e a inferência de tipos do Swift tenta inferir um tipo para o literal.
Por exemplo,
na declaração `let x: Int8 = 42`,
o Swift usa a anotação de tipo explícita (`: Int8`) para inferir
que o tipo do literal inteiro `42` é `Int8`.
Se não houver informação de tipo adequada disponível,
o Swift infere que o tipo do literal é um dos tipos literais padrão
definidos na biblioteca padrão do Swift
e listados na tabela abaixo.
Ao especificar a anotação de tipo para um valor literal,
o tipo da anotação deve ser um tipo que possa ser instanciado a partir desse valor literal.
Ou seja, o tipo precisa estar em conformidade
com os protocolos da biblioteca padrão do Swift listados na tabela abaixo.

| Literal | Tipo padrão | Protocolo |
| ------- | ------------ | -------- |
| Inteiro | `Int` | `ExpressibleByIntegerLiteral` |
| Ponto flutuante | `Double` | `ExpressibleByFloatLiteral` |
| String | `String` | `ExpressibleByStringLiteral`, `ExpressibleByUnicodeScalarLiteral` para literais de string que contêm apenas um único escalar Unicode, `ExpressibleByExtendedGraphemeClusterLiteral` para literais de string que contêm apenas um único grapheme cluster estendido |
| Expressão regular | `Regex` | Nenhum |
| Booleano | `Bool` | `ExpressibleByBooleanLiteral` |

Por exemplo, na declaração `let str = "Hello, world"`,
o tipo inferido padrão da string literal `"Hello, world"` é `String`.
Além disso, `Int8` está em conformidade com o protocolo `ExpressibleByIntegerLiteral`,
e por isso pode ser usado na anotação de tipo do literal inteiro `42`
na declaração `let x: Int8 = 42`.

<!--
  The list of ExpressibleBy... protocols above also appears in Declarations_EnumerationsWithRawCaseValues.
  ExpressibleByNilLiteral is left out of the list because conformance to it isn't recommended.
  There is no protocol for regex literal in the list because the stdlib intentionally omits that.
-->

> Gramática de um literal:
>
> *literal* → *numeric-literal* | *string-literal* | *regular-expression-literal* | *boolean-literal* | *nil-literal*
>
> *numeric-literal* → *signed-integer-literal* | *signed-floating-point-literal* \
> *boolean-literal* → **`true`** | **`false`** \
> *nil-literal* → **`nil`**

### Literais inteiros

*Literais inteiros* representam valores inteiros de precisão não especificada.
Por padrão, literais inteiros são expressos em decimal;
você pode especificar outra base usando um prefixo.
Literais binários começam com `0b`,
literais octais começam com `0o`,
e literais hexadecimais começam com `0x`.

Literais decimais contêm os dígitos `0` a `9`.
Literais binários contêm `0` e `1`,
literais octais contêm `0` a `7`,
e literais hexadecimais contêm `0` a `9`
bem como `A` a `F`, em maiúsculas ou minúsculas.

Literais inteiros negativos são expressos colocando um sinal de menos (`-`)
antes de um literal inteiro, como em `-42`.

Sublinhados (`_`) são permitidos entre dígitos para facilitar a leitura,
mas são ignorados e, portanto, não afetam o valor do literal.
Literais inteiros podem começar com zeros à esquerda (`0`),
mas eles também são ignorados e não afetam a base nem o valor do literal.

A menos que seja especificado de outra forma,
o tipo inferido padrão de um literal inteiro é o tipo `Int` da biblioteca padrão do Swift.
A biblioteca padrão do Swift também define tipos para diversos tamanhos
de inteiros com e sem sinal,
como descrito em <doc:TheBasics#Integers>.

<!--
  TR: The prose assumes underscores only belong between digits.
  Is there a reason to allow them at the end of a literal?
  Java and Ruby both require underscores to be between digits.
  Also, are adjacent underscores meant to be allowed, like 5__000?
  (REPL supports them as of swift-1.21 but it seems odd.)
-->

<!--
  NOTE: Updated the syntax-grammar to reflect [Contributor 7746]'s comment in
  <rdar://problem/15181997> Teach the compiler about a concept of negative integer literals.
  This feels very strange from a grammatical point of view.
  Update: This is a parser hack, not a lexer hack. Therefore,
  it's not part of the grammar for integer literal, contrary to [Contributor 2562]'s claim.
  (Doug confirmed this, 4/2/2014.)
-->

> Gramática de um literal inteiro:
>
> *signed-integer-literal* → **`-`**_?_ *integer-literal*
> *integer-literal* → *binary-literal* \
> *integer-literal* → *octal-literal* \
> *integer-literal* → *decimal-literal* \
> *integer-literal* → *hexadecimal-literal*
>
> *binary-literal* → **`0b`** *binary-digit* *binary-literal-characters*_?_ \
> *binary-digit* → Digit 0 or 1 \
> *binary-literal-character* → *binary-digit* | **`_`** \
> *binary-literal-characters* → *binary-literal-character* *binary-literal-characters*_?_
>
> *octal-literal* → **`0o`** *octal-digit* *octal-literal-characters*_?_ \
> *octal-digit* → Digit 0 through 7 \
> *octal-literal-character* → *octal-digit* | **`_`** \
> *octal-literal-characters* → *octal-literal-character* *octal-literal-characters*_?_
>
> *decimal-literal* → *decimal-digit* *decimal-literal-characters*_?_ \
> *decimal-digit* → Digit 0 through 9 \
> *decimal-digits* → *decimal-digit* *decimal-digits*_?_ \
> *decimal-literal-character* → *decimal-digit* | **`_`** \
> *decimal-literal-characters* → *decimal-literal-character* *decimal-literal-characters*_?_
>
> *hexadecimal-literal* → **`0x`** *hexadecimal-digit* *hexadecimal-literal-characters*_?_ \
> *hexadecimal-digit* → Digit 0 through 9, a through f, or A through F \
> *hexadecimal-literal-character* → *hexadecimal-digit* | **`_`** \
> *hexadecimal-literal-characters* → *hexadecimal-literal-character* *hexadecimal-literal-characters*_?_

### Literais de ponto flutuante

*Literais de ponto flutuante* representam valores de ponto flutuante de precisão não especificada.

Por padrão, literais de ponto flutuante são expressos em decimal (sem prefixo),
mas também podem ser expressos em hexadecimal (com prefixo `0x`).

Literais decimais de ponto flutuante consistem em uma sequência de dígitos decimais
seguida por uma fração decimal, um expoente decimal, ou ambos.
A fração decimal consiste em um ponto decimal (`.`)
seguido por uma sequência de dígitos decimais.
O expoente consiste em um prefixo `e`, em maiúscula ou minúscula,
seguido por uma sequência de dígitos decimais que indica
por qual potência de 10 o valor antes do `e` é multiplicado.
Por exemplo, `1.25e2` representa 1.25 x 10², o que resulta em `125.0`.
Da mesma forma, `1.25e-2` representa 1.25 x 10⁻²,
o que resulta em `0.0125`.

Literais hexadecimais de ponto flutuante consistem em um prefixo `0x`,
seguido por uma fração hexadecimal opcional,
seguida por um expoente hexadecimal.
A fração hexadecimal consiste em um ponto decimal
seguido por uma sequência de dígitos hexadecimais.
O expoente consiste em um prefixo `p`, em maiúscula ou minúscula,
seguido por uma sequência de dígitos decimais que indica
por qual potência de 2 o valor antes do `p` é multiplicado.
Por exemplo, `0xFp2` representa 15 x 2², o que resulta em `60`.
Da mesma forma, `0xFp-2` representa 15 x 2⁻², o que resulta em `3.75`.

Literais de ponto flutuante negativos são expressos colocando um sinal de menos (`-`)
antes de um literal de ponto flutuante, como em `-42.5`.

Sublinhados (`_`) são permitidos entre dígitos para facilitar a leitura,
mas são ignorados e, portanto, não afetam o valor do literal.
Literais de ponto flutuante podem começar com zeros à esquerda (`0`),
mas eles também são ignorados e não afetam a base nem o valor do literal.

A menos que seja especificado de outra forma,
o tipo inferido padrão de um literal de ponto flutuante é o tipo `Double`
da biblioteca padrão do Swift, que representa um número de ponto flutuante de 64 bits.
A biblioteca padrão do Swift também define o tipo `Float`,
que representa um número de ponto flutuante de 32 bits.

> Gramática de um literal de ponto flutuante:
>
> *signed-floating-point-literal* → > **`-`**_?_ *floating-point-literal*
> *floating-point-literal* → *decimal-literal* *decimal-fraction*_?_ *decimal-exponent*_?_ \
> *floating-point-literal* → *hexadecimal-literal* *hexadecimal-fraction*_?_ *hexadecimal-exponent*
>
> *decimal-fraction* → **`.`** *decimal-literal* \
> *decimal-exponent* → *floating-point-e* *sign*_?_ *decimal-literal*
>
> *hexadecimal-fraction* → **`.`** *hexadecimal-digit* *hexadecimal-literal-characters*_?_ \
> *hexadecimal-exponent* → *floating-point-p* *sign*_?_ *decimal-literal*
>
> *floating-point-e* → **`e`** | **`E`** \
> *floating-point-p* → **`p`** | **`P`** \
> *sign* → **`+`** | **`-`**

### Literais de string

Um literal de string é uma sequência de caracteres delimitada por aspas.
Um literal de string de uma linha é delimitado por aspas duplas
e tem a seguinte forma:

```swift
"<#characters#>"
```

Literais de string não podem conter
aspas duplas sem escape (`"`),
barra invertida sem escape (`\`),
retorno de carro ou quebra de linha.

Um literal de string de múltiplas linhas é delimitado por três aspas duplas
e tem a seguinte forma:

```swift
"""
<#characters#>
"""
```

Diferente de um literal de string de uma linha,
um literal de string de múltiplas linhas pode conter
aspas duplas sem escape (`"`), retornos de carro e quebras de linha.
Ele não pode conter três aspas duplas sem escape seguidas umas das outras.

A quebra de linha após o `"""` que inicia o literal de string de múltiplas linhas
não faz parte da string.
A quebra de linha antes do `"""` que termina o literal também não faz parte da string.
Para criar um literal de string de múltiplas linhas
que comece ou termine com uma quebra de linha,
escreva uma linha em branco como primeira ou última linha.

Um literal de string de múltiplas linhas pode ser indentado
usando qualquer combinação de espaços e tabulações;
essa indentação não é incluída na string.
O `"""` que termina o literal determina a indentação:
cada linha não vazia do literal deve começar
exatamente com a mesma indentação que aparece antes do `"""` de fechamento;
não há conversão entre tabulações e espaços.
Você pode incluir espaços e tabulações adicionais depois dessa indentação;
esses espaços e tabulações aparecem na string.

As quebras de linha em um literal de string de múltiplas linhas são normalizadas
para usar o caractere de quebra de linha.
Mesmo que seu arquivo-fonte tenha uma mistura de retornos de carro e quebras de linha,
todas as quebras de linha na string serão iguais.

Em um literal de string de múltiplas linhas,
escrever uma barra invertida (`\`) no fim de uma linha
omite essa quebra de linha da string.
Qualquer espaço em branco entre a barra invertida e a quebra de linha
também é omitido.
Você pode usar essa sintaxe para quebrar um literal de string de múltiplas linhas
em várias linhas no código-fonte,
sem alterar o valor da string resultante.

Caracteres especiais podem ser incluídos em literais de string
de uma linha e de múltiplas linhas
usando as seguintes sequências de escape:

- Caractere nulo (`\0`)
- Barra invertida (`\\`)
- Tabulação horizontal (`\t`)
- Quebra de linha (`\n`)
- Retorno de carro (`\r`)
- Aspas duplas (`\"`)
- Aspas simples (`\'`)
- Escalar Unicode (`\u{`*n*`}`),
  em que *n* é um número hexadecimal
  com um a oito dígitos

<!--
  The behavior of \n and \r isn't the same as C.
  We specify exactly what those escapes mean.
  The behavior on C is platform dependent --
  in text mode, \n maps to the platform's line separator
  which could be CR or LF or CRLF.
-->

O valor de uma expressão pode ser inserido em um literal de string
colocando a expressão entre parênteses depois de uma barra invertida (`\`).
A expressão interpolada pode conter um literal de string,
mas não pode conter uma barra invertida sem escape,
um retorno de carro ou uma quebra de linha.

Por exemplo, todos os literais de string a seguir têm o mesmo valor:

```swift
"1 2 3"
"1 2 \("3")"
"1 2 \(3)"
"1 2 \(1 + 2)"
let x = 3; "1 2 \(x)"
```

<!--
  - test: `string-literals`

  ```swifttest
  >> let r0 =
  -> "1 2 3"
  >> let r1 =
  -> "1 2 \("3")"
  >> assert(r0 == r1)
  >> let r2 =
  -> "1 2 \(3)"
  >> assert(r0 == r2)
  >> let r3 =
  -> "1 2 \(1 + 2)"
  >> assert(r0 == r3)
  -> let x = 3; "1 2 \(x)"
  >> assert(r0 == "1 2 \(x)")
  !$ warning: string literal is unused
  !! let x = 3; "1 2 \(x)"
  !!            ^~~~~~~~~~
  ```
-->

<!--
  Refactor the above if possible to avoid using bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

Uma string delimitada por delimitadores estendidos é uma sequência de caracteres
delimitada por aspas e por um conjunto balanceado de um ou mais sinais de número (`#`).
Uma string delimitada por delimitadores estendidos tem as seguintes formas:

```swift
#"<#characters#>"#

#"""
<#characters#>
"""#
```

Caracteres especiais em uma string delimitada por delimitadores estendidos
aparecem na string resultante como caracteres normais,
e não como caracteres especiais.
Você pode usar delimitadores estendidos para criar strings com caracteres
que normalmente teriam um efeito especial,
como gerar uma interpolação de string,
iniciar uma sequência de escape
ou encerrar a string.

O exemplo a seguir mostra um literal de string
e uma string delimitada por delimitadores estendidos
que criam valores de string equivalentes:

```swift
let string = #"\(x) \ " \u{2603}"#
let escaped = "\\(x) \\ \" \\u{2603}"
print(string)
// Prints "\(x) \ " \u{2603}".
print(string == escaped)
// Prints "true".
```

<!--
  - test: `extended-string-delimiters`

  ```swifttest
  -> let string = #"\(x) \ " \u{2603}"#
  -> let escaped = "\\(x) \\ \" \\u{2603}"
  -> print(string)
  <- \(x) \ " \u{2603}
  -> print(string == escaped)
  <- true
  ```
-->

Se você usar mais de um sinal de número para formar
uma string delimitada por delimitadores estendidos,
não coloque espaço em branco entre os sinais de número:

<!--
  - test: `extended-string-delimiters`

  ```swifttest
  -> print(###"Line 1\###nLine 2"###) // OK
  << Line 1
  << Line 2
  ```
-->

```swift
print(###"Line 1\###nLine 2"###) // OK
print(# # #"Line 1\# # #nLine 2"# # #) // Error
```

<!--
  - test: `extended-string-delimiters-err`

  ```swifttest
  -> print(###"Line 1\###nLine 2"###) // OK
  -> print(# # #"Line 1\# # #nLine 2"# # #) // Error
  !$ error: expected expression in list of expressions
  !! print(# # #"Line 1\# # #nLine 2"# # #) // Error
  !! ^
  !$ error: invalid escape sequence in literal
  !! print(# # #"Line 1\# # #nLine 2"# # #) // Error
  !! ^
  ```
-->

Literais de string de múltiplas linhas criados com delimitadores estendidos
têm os mesmos requisitos de indentação que os literais de string de múltiplas linhas comuns.

O tipo inferido padrão de um literal de string é `String`.
Para mais informações sobre o tipo `String`,
veja <doc:StringsAndCharacters>
e [`String`](https://developer.apple.com/documentation/swift/string).

Literais de string concatenados com o operador `+`
são concatenados em tempo de compilação.
Por exemplo, os valores de `textA` e `textB` no exemplo abaixo são idênticos:
nenhuma concatenação em tempo de execução é realizada.

```swift
let textA = "Hello " + "world"
let textB = "Hello world"
```

<!--
  - test: `concatenated-strings`

  ```swifttest
  -> let textA = "Hello " + "world"
  -> let textB = "Hello world"
  ```
-->

> Gramática de um literal de string:
>
> *string-literal* → *static-string-literal* | *interpolated-string-literal*
>
> *string-literal-opening-delimiter* → *extended-string-literal-delimiter*_?_ **`"`** \
> *string-literal-closing-delimiter* → **`"`** *extended-string-literal-delimiter*_?_
>
> *static-string-literal* → *string-literal-opening-delimiter* *quoted-text*_?_ *string-literal-closing-delimiter* \
> *static-string-literal* → *multiline-string-literal-opening-delimiter* *multiline-quoted-text*_?_ *multiline-string-literal-closing-delimiter*
>
> *multiline-string-literal-opening-delimiter* → *extended-string-literal-delimiter*_?_ **`"""`** \
> *multiline-string-literal-closing-delimiter* → **`"""`** *extended-string-literal-delimiter*_?_ \
> *extended-string-literal-delimiter* → **`#`** *extended-string-literal-delimiter*_?_
>
> *quoted-text* → *quoted-text-item* *quoted-text*_?_ \
> *quoted-text-item* → *escaped-character* \
> *quoted-text-item* → Any Unicode scalar value except  **`"`**,  **`\`**, U+000A, or U+000D
>
> *multiline-quoted-text* → *multiline-quoted-text-item* *multiline-quoted-text*_?_ \
> *multiline-quoted-text-item* → *escaped-character* \
> *multiline-quoted-text-item* → Any Unicode scalar value except  **`\`** \
> *multiline-quoted-text-item* → *escaped-newline*
>
> *interpolated-string-literal* → *string-literal-opening-delimiter* *interpolated-text*_?_ *string-literal-closing-delimiter* \
> *interpolated-string-literal* → *multiline-string-literal-opening-delimiter* *multiline-interpolated-text*_?_ *multiline-string-literal-closing-delimiter*
>
> *interpolated-text* → *interpolated-text-item* *interpolated-text*_?_ \
> *interpolated-text-item* → **`\(`** *expression* **`)`** | *quoted-text-item*
>
> *multiline-interpolated-text* → *multiline-interpolated-text-item* *multiline-interpolated-text*_?_ \
> *multiline-interpolated-text-item* → **`\(`** *expression* **`)`** | *multiline-quoted-text-item*
>
> *escape-sequence* → **`\`** *extended-string-literal-delimiter* \
> *escaped-character* → *escape-sequence* **`0`** | *escape-sequence* **`\`** | *escape-sequence* **`t`** | *escape-sequence* **`n`** | *escape-sequence* **`r`** | *escape-sequence* **`"`** | *escape-sequence* **`'`** \
> *escaped-character* → *escape-sequence* **`u`** **`{`** *unicode-scalar-digits* **`}`** \
> *unicode-scalar-digits* → Between one and eight hexadecimal digits
>
> *escaped-newline* → *escape-sequence* *inline-spaces*_?_ *line-break*

<!--
  Quoted text resolves to a sequence of escaped characters by way of
  the quoted-text rule which allows repetition; no need to allow
  repetition in the quoted-text/escaped-character rule too.
-->

<!--
  Now that single quotes are gone, we don't have a character literal.
  Because we may one bring them back, here's the old grammar for them:

  textual-literal -> character-literal | string-literal

  character-literal -> ``'`` quoted-character ``'``
  quoted-character -> escaped-character
  quoted-character -> Any Unicode scalar value except ``'``, ``\``, U+000A, or U+000D
-->

### Literais de expressão regular

Um literal de expressão regular é uma sequência de caracteres
delimitada por barras (`/`), com a seguinte forma:

```swift
/<#regular expression#>/
```

Literais de expressão regular não podem começar com uma tabulação
ou espaço sem escape,
e não podem conter
uma barra (`/`) sem escape, um retorno de carro ou uma quebra de linha.

Dentro de um literal de expressão regular,
a barra invertida é entendida como parte da expressão regular,
e não apenas como caractere de escape como nos literais de string.
Ela indica que o caractere especial seguinte deve ser interpretado literalmente,
ou que o caractere não especial seguinte deve ser interpretado de forma especial.
Por exemplo, `/\(/` corresponde a um único parêntese de abertura
e `/\d/` corresponde a um único dígito.

<!--
  OUTLINE

  Doc comments on Regex struct don't have more syntax details,
  or a cross reference to where you can learn more.
  We probably need at least some baseline coverage
  of the supported syntax here.
  (Unified dialect/superset of POSIX + PCRE 2 + Oniguruma + .NET)

  https://github.com/swiftlang/swift-experimental-string-processing/blob/main/Sources/_StringProcessing/Regex/Core.swift

  Regex literals and the DSL take different approaches to captures.
  The literals give you more type safety.
  The DSL lets you access stuff by name.

  From SE-0354:
  A regex literal may be used with a prefix operator,
  e.g `let r = ^^/x/` is parsed as `let r = ^^(/x/)`.
  In this case,
  when encountering operator characters containing `/` in an expression position,
  the characters up to the first `/` are split into a prefix operator,
  and regex literal parsing continues as normal.
-->

Um literal de expressão regular delimitado por delimitadores estendidos
é uma sequência de caracteres delimitada por barras (`/`)
e por um conjunto balanceado de um ou mais sinais de número (`#`).
Um literal de expressão regular delimitado por delimitadores estendidos
tem as seguintes formas:

```swift
#/<#regular expression#>/#

#/
<#regular expression#>
/#
```

Um literal de expressão regular que usa delimitadores estendidos
pode começar com um espaço ou tabulação sem escape,
conter barras (`/`) sem escape
e se estender por várias linhas.
Para um literal de expressão regular de múltiplas linhas,
o delimitador de abertura deve estar no fim de uma linha,
e o delimitador de fechamento deve estar em uma linha própria.
Dentro de um literal de expressão regular de múltiplas linhas,
a sintaxe estendida de expressões regulares fica habilitada por padrão:
especificamente, espaços em branco são ignorados e comentários são permitidos.

<!--
  TODO As details about the multiline syntax shake out during SE review,
  like indentation and whitespace,
  add them above or spin out a separate paragraph.
-->

Se você usar mais de um sinal de número para formar
um literal de expressão regular delimitado por delimitadores estendidos,
não coloque espaço em branco entre os sinais de número:

```swift
let regex1 = ##/abc/##       // OK
let regex2 = # #/abc/# #     // Error
```

<!--
  - test: `extended-regex-delimiters-err`

  ```swifttest
  -> let regex1 = ##/abc/##       // OK
  -> let regex2 = # #/abc/# #     // Error
  ```
-->

Se precisar criar um literal de expressão regular vazio,
você deve usar a sintaxe de delimitadores estendidos.

> Gramática de um literal de expressão regular:
>
> *regular-expression-literal* → *regular-expression-literal-opening-delimiter* *regular-expression* *regular-expression-literal-closing-delimiter* \
> *regular-expression* → Any regular expression
>
> *regular-expression-literal-opening-delimiter* → *extended-regular-expression-literal-delimiter*_?_ **`/`** \
> *regular-expression-literal-closing-delimiter* → **`/`** *extended-regular-expression-literal-delimiter*_?_
>
> *extended-regular-expression-literal-delimiter* → **`#`** *extended-regular-expression-literal-delimiter*_?_

## Operadores

A biblioteca padrão do Swift define diversos operadores para o seu uso,
muitos dos quais são discutidos em <doc:BasicOperators>
e <doc:AdvancedOperators>.
Esta seção descreve quais caracteres podem ser usados para definir operadores personalizados.

Operadores personalizados podem começar com um dos caracteres ASCII
`/`, `=`, `-`, `+`, `!`, `*`, `%`, `<`, `>`,
`&`, `|`, `^`, `?` ou `~`, ou com um dos caracteres Unicode
definidos na gramática abaixo
(que incluem caracteres dos blocos Unicode
*Operadores Matemáticos*, *Símbolos Diversos* e *Dingbats*, entre outros).
Depois do primeiro caractere,
caracteres Unicode combinantes também são permitidos.

Você também pode definir operadores personalizados
que começam com um ponto (`.`).
Esses operadores podem conter pontos adicionais.
Por exemplo, `.+.` é tratado como um único operador.
Se um operador não começar com ponto,
ele não pode conter ponto em outra posição.
Por exemplo, `+.+` é tratado como
o operador `+` seguido do operador `.+`.

<!--
  - test: `dot-operator-must-start-with-dot`

  ```swifttest
  >> infix operator +.+ ;
  !$ error: consecutive statements on a line must be separated by ';'
  !! infix operator +.+ ;
  !!                 ^
  !!                 ;
  !$ error: operator with postfix spacing cannot start a subexpression
  !! infix operator +.+ ;
  !!                 ^
  !$ error: expected expression
  !! infix operator +.+ ;
  !!                    ^
  >> infix operator .+
  >> infix operator .+.
  ```
-->

Embora você possa definir operadores personalizados que contenham
um ponto de interrogação (`?`),
eles não podem consistir apenas nesse único caractere.
Além disso, embora operadores possam conter um ponto de exclamação (`!`),
operadores pós-fixos não podem começar com ponto de interrogação
nem com ponto de exclamação.

<!--
  - test: `postfix-operators-dont-need-unique-prefix`

  ```swifttest
  >> struct Num { var value: Int }
     postfix operator +
     postfix operator +*
     postfix func + (x: Num) -> Int { return x.value + 1 }
     postfix func +* (x: Num) -> Int { return x.value * 100 }
  >> let n = Num(value: 5)
  >> print(n+)
  << 6
  >> print(n+*)
  << 500
  ```
-->

<!--
  - test: `postfix-operator-cant-start-with-question-mark`

  ```swifttest
  >> postfix operator ?+
  >> postfix func ?+ (x: Int) -> Int {
         if x > 10 {
             return x
         }
         return x + 1
     }
  >> print(1?+)
  !$ error: postfix operator names starting with '?' or '!' are disallowed to avoid collisions with built-in unwrapping operators
  !! postfix operator ?+
  !!                  ^
  !$ error: '+' is not a postfix unary operator
  !! print(1?+)
  !!         ^
  ```
-->

> Nota:
> Os tokens `=`, `->`, `//`, `/*`, `*/`, `.`,
> os operadores prefixos `<`, `&` e `?`,
> o operador infixo `?`,
> e os operadores pós-fixos `>`, `!` e `?` são reservados.
> Esses tokens não podem ser sobrecarregados,
> nem usados como operadores personalizados.

O espaço em branco ao redor de um operador é usado para determinar
se ele é usado como operador prefixo, pós-fixo ou infixo.
Esse comportamento segue as seguintes regras:

- Se um operador tem espaço em branco dos dois lados ou não tem espaço em branco de nenhum lado,
  ele é tratado como operador infixo.
  Por exemplo, o operador `+++` em `a+++b` e em `a +++ b` é tratado como operador infixo.
- Se um operador tem espaço em branco apenas do lado esquerdo,
  ele é tratado como operador unário prefixo.
  Por exemplo, o operador `+++` em `a +++b` é tratado como operador unário prefixo.
- Se um operador tem espaço em branco apenas do lado direito,
  ele é tratado como operador unário pós-fixo.
  Por exemplo, o operador `+++` em `a+++ b` é tratado como operador unário pós-fixo.
- Se um operador não tem espaço em branco à esquerda, mas é seguido imediatamente por um ponto (`.`),
  ele é tratado como operador unário pós-fixo.
  Por exemplo, o operador `+++` em `a+++.b` é tratado como operador unário pós-fixo
  (`a+++ .b`, e não `a +++ .b`).

Para os fins dessas regras,
os caracteres `(`, `[` e `{` antes de um operador,
os caracteres `)`, `]` e `}` depois de um operador,
e os caracteres `,`, `;` e `:`
também são considerados espaço em branco.

Se o operador predefinido `!` ou `?` não tiver espaço em branco à esquerda,
ele é tratado como operador pós-fixo,
independentemente de ter ou não espaço em branco à direita.
Para usar o `?` como operador de encadeamento opcional,
ele não pode ter espaço em branco à esquerda.
Para usá-lo no operador condicional ternário (`?` `:`),
ele deve ter espaço em branco dos dois lados.

Se um dos argumentos de um operador infixo for um literal de expressão regular,
então o operador deve ter espaço em branco dos dois lados.

Em certas construções, operadores que começam com `<` ou `>`
podem ser divididos em dois ou mais tokens.
O restante é tratado da mesma forma e pode ser dividido novamente.
Por isso, você não precisa adicionar espaço em branco
para desambiguar os caracteres `>` de fechamento em construções
como `Dictionary<String, Array<Int>>`.
Nesse exemplo, os caracteres `>` de fechamento não são tratados
como um único token que poderia ser interpretado
erroneamente como o operador de deslocamento de bits `>>`.

<!--
  NOTE: Once the parser sees a < it goes into a pre-scanning lookahead mode.  It
  matches < and > and looks at what token comes after the > -- if it's a . or
  a ( it treats the <...> as a generic parameter list, otherwise it treats
  them as less than and greater than.

  This fails to parse things like x<<2>>(1+2) but it's the same as C#.  So
  don't write that.

  We call out the > > vs >> because
  C++ typically needs whitespace to resolve the ambiguity.
-->

Para aprender a definir novos operadores personalizados,
veja <doc:AdvancedOperators#Custom-Operators>
e <doc:Declarations#Operator-Declaration>.
Para aprender a sobrecarregar operadores existentes,
veja <doc:AdvancedOperators#Operator-Methods>.

<!--
  NOTE: The ? is a reserved punctuation.  Optional-chaining (foo?.bar) is actually a
  monad -- the ? is actually a monadic bind operator.  It is like a burrito.
  The current list of reserved punctuation is in Tokens.def.
-->

> Gramática de operadores:
>
> *operator* → *operator-head* *operator-characters*_?_ \
> *operator* → *dot-operator-head* *dot-operator-characters*
>
> *operator-head* → **`/`** | **`=`** | **`-`** | **`+`** | **`!`** | **`*`** | **`%`** | **`<`** | **`>`** | **`&`** | **`|`** | **`^`** | **`~`** | **`?`** \
> *operator-head* → U+00A1–U+00A7 \
> *operator-head* → U+00A9 or U+00AB \
> *operator-head* → U+00AC or U+00AE \
> *operator-head* → U+00B0–U+00B1 \
> *operator-head* → U+00B6, U+00BB, U+00BF, U+00D7, or U+00F7 \
> *operator-head* → U+2016–U+2017 \
> *operator-head* → U+2020–U+2027 \
> *operator-head* → U+2030–U+203E \
> *operator-head* → U+2041–U+2053 \
> *operator-head* → U+2055–U+205E \
> *operator-head* → U+2190–U+23FF \
> *operator-head* → U+2500–U+2775 \
> *operator-head* → U+2794–U+2BFF \
> *operator-head* → U+2E00–U+2E7F \
> *operator-head* → U+3001–U+3003 \
> *operator-head* → U+3008–U+3020 \
> *operator-head* → U+3030
>
> *operator-character* → *operator-head* \
> *operator-character* → U+0300–U+036F \
> *operator-character* → U+1DC0–U+1DFF \
> *operator-character* → U+20D0–U+20FF \
> *operator-character* → U+FE00–U+FE0F \
> *operator-character* → U+FE20–U+FE2F \
> *operator-character* → U+E0100–U+E01EF \
> *operator-characters* → *operator-character* *operator-characters*_?_
>
> *dot-operator-head* → **`.`** \
> *dot-operator-character* → **`.`** | *operator-character* \
> *dot-operator-characters* → *dot-operator-character* *dot-operator-characters*_?_
>
> *infix-operator* → *operator* \
> *prefix-operator* → *operator* \
> *postfix-operator* → *operator*

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
