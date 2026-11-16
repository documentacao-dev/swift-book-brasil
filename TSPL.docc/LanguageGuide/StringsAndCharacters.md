# Strings e caracteres

Armazene e manipule texto.

Uma *string* é uma sequência de caracteres,
como `"hello, world"` ou `"albatross"`.
Strings em Swift são representadas pelo tipo `String`.
O conteúdo de uma `String` pode ser acessado de várias maneiras,
inclusive como uma coleção de valores `Character`.

Os tipos `String` e `Character` do Swift oferecem
uma forma rápida e compatível com Unicode de trabalhar com texto no seu código.
A sintaxe para criar e manipular strings é leve e legível,
com uma sintaxe de literal de string parecida com a do C.
Concatenar strings é tão simples quanto
combinar duas strings com o operador `+`,
e a mutabilidade de uma string é definida ao escolher entre uma constante ou uma variável,
assim como qualquer outro valor em Swift.
Você também pode usar strings para inserir
constantes, variáveis, literais e expressões em strings maiores,
em um processo conhecido como interpolação de strings.
Isso facilita criar valores de string personalizados para exibição, armazenamento e impressão.

Apesar dessa simplicidade de sintaxe,
o tipo `String` do Swift é uma implementação de string rápida e moderna.
Cada string é composta de caracteres Unicode independentes de codificação,
e oferece suporte para acessar esses caracteres em várias representações Unicode.

> Nota: O tipo `String` do Swift tem ponte com a classe `NSString` do Foundation.
> O Foundation também estende `String` para expor métodos definidos por `NSString`.
> Isso significa que, se você importar o Foundation,
> pode acessar esses métodos de `NSString` em `String` sem precisar fazer cast.
>
> Para mais informações sobre como usar `String` com Foundation e Cocoa,
> veja [Ponte entre String e NSString](https://developer.apple.com/documentation/swift/string#Bridging-Between-String-and-NSString).

## Literais de string

Você pode incluir valores `String` predefinidos no seu código como *literais de string*.
Um literal de string é uma sequência de caracteres
delimitada por aspas duplas (`"`).

Use um literal de string como valor inicial de uma constante ou variável:

```swift
let someString = "Some string literal value"
```

<!--
  - test: `stringLiterals`

  ```swifttest
  -> let someString = "Some string literal value"
  ```
-->

Observe que o Swift infere o tipo `String` para a constante `someString`
porque ela é inicializada com um valor literal de string.

### Literais de string multilinha

Se você precisar de uma string que ocupe várias linhas,
use um literal de string multilinha:
uma sequência de caracteres
delimitada por três aspas duplas:

<!--
  Quote comes from "Alice's Adventures in Wonderland",
  which has been public domain as of 1907.
-->

```swift
let quotation = """
The White Rabbit put on his spectacles.  "Where shall I begin,
please your Majesty?" he asked.

"Begin at the beginning," the King said gravely, "and go on
till you come to the end; then stop."
"""
```

<!--
  - test: `multiline-string-literals`

  ```swifttest
  -> let quotation = """
     The White Rabbit put on his spectacles.  "Where shall I begin,
     please your Majesty?" he asked.

     "Begin at the beginning," the King said gravely, "and go on
     till you come to the end; then stop."
     """
  >> let newlines = quotation.filter { $0 == "\n" }
  >> print(newlines.count)
  << 4
  ```
-->

Um literal de string multilinha inclui todas as linhas entre
suas aspas de abertura e de fechamento.
A string começa na primeira linha depois das aspas de abertura (`"""`)
e termina na linha anterior às aspas de fechamento,
o que significa que nenhuma das strings abaixo
começa ou termina com uma quebra de linha:

```swift
let singleLineString = "These are the same."
let multilineString = """
These are the same.
"""
```

<!--
  - test: `multiline-string-literals`

  ```swifttest
  -> let singleLineString = "These are the same."
  -> let multilineString = """
     These are the same.
     """
  >> print(singleLineString == multilineString)
  << true
  ```
-->

Quando o código-fonte inclui uma quebra de linha
dentro de um literal de string multilinha,
essa quebra de linha também aparece no valor da string.
Se você quiser usar quebras de linha
para deixar o código-fonte mais fácil de ler,
mas não quiser que elas façam parte do valor da string,
escreva uma barra invertida (`\`) no fim dessas linhas:

```swift
let softWrappedQuotation = """
The White Rabbit put on his spectacles.  "Where shall I begin, \
please your Majesty?" he asked.

"Begin at the beginning," the King said gravely, "and go on \
till you come to the end; then stop."
"""
```

<!--
  - test: `multiline-string-literals`

  ```swifttest
  -> let softWrappedQuotation = """
     The White Rabbit put on his spectacles.  "Where shall I begin, \
     please your Majesty?" he asked.

     "Begin at the beginning," the King said gravely, "and go on \
     till you come to the end; then stop."
     """
  >> let softNewlines = softWrappedQuotation.filter { $0 == "\n" }
  >> print(softNewlines.count)
  << 2
  ```
-->

Para criar um literal de string multilinha que começa ou termina com uma quebra de linha,
escreva uma linha em branco como primeira ou última linha.
Por exemplo:

```swift
let lineBreaks = """

This string starts with a line break.
It also ends with a line break.

"""
```

<!--
  - test: `multiline-string-literals`

  ```swifttest
  -> let lineBreaks = """

     This string starts with a line break.
     It also ends with a line break.

     """
  ```
-->

<!--
  These are well-fed lines!
-->

Uma string multilinha pode ser indentada para acompanhar o código ao redor.
O espaço em branco antes das aspas de fechamento (`"""`)
indica ao Swift qual espaço em branco ignorar antes de todas as outras linhas.
No entanto, se você escrever espaço em branco no início de uma linha
além do que vem antes das aspas de fechamento,
esse espaço em branco *é* incluído.

![](multilineStringWhitespace)

<!--
  Using an image here is a little clearer than a code listing,
  since it can call out which spaces "count".
-->

<!--
  - test: `multiline-string-literal-whitespace`

  ```swifttest
  -> let linesWithIndentation = """
         This line doesn't begin with whitespace.
             This line begins with four spaces.
         This line doesn't begin with whitespace.
         """
  ```
-->

No exemplo acima,
mesmo que o literal de string multilinha inteiro esteja indentado,
a primeira e a última linha da string não começam com nenhum espaço em branco.
A linha do meio tem mais indentação que as aspas de fechamento,
então começa com essa indentação extra de quatro espaços.

### Caracteres especiais em literais de string

Literais de string podem incluir os seguintes caracteres especiais:

- Os caracteres especiais escapados `\0` (caractere nulo), `\\` (barra invertida),
  `\t` (tabulação horizontal), `\n` (quebra de linha), `\r` (retorno de carro),
  `\"` (aspas duplas) e `\'` (aspas simples)
- Um valor escalar Unicode arbitrário, escrito como `\u{`*n*`}`,
  em que *n* é um número hexadecimal de 1 a 8 dígitos
  (Unicode é discutido em <doc:StringsAndCharacters#Unicode> abaixo)

<!--
  - test: `stringLiteralUnicodeScalar`

  ```swifttest
  >> _ = "\u{0}"
  >> _ = "\u{00000000}"
  >> _ = "\u{000000000}"
  !$ error: \u{...} escape sequence expects between 1 and 8 hex digits
  !! _ = "\u{000000000}"
  !!      ^
  >> _ = "\u{10FFFF}"
  >> _ = "\u{110000}"
  !$ error: invalid unicode scalar
  !! _ = "\u{110000}"
  !!      ^
  ```
-->

O código abaixo mostra quatro exemplos desses caracteres especiais.
A constante `wiseWords` contém duas aspas duplas escapadas.
As constantes `dollarSign`, `blackHeart` e `sparklingHeart`
demonstram o formato de escalar Unicode:

```swift
let wiseWords = "\"Imagination is more important than knowledge\" - Einstein"
// "Imagination is more important than knowledge" - Einstein
let dollarSign = "\u{24}"        // $,  Unicode scalar U+0024
let blackHeart = "\u{2665}"      // ♥,  Unicode scalar U+2665
let sparklingHeart = "\u{1F496}" // 💖, Unicode scalar U+1F496
```

<!--
  - test: `specialCharacters`

  ```swifttest
  -> let wiseWords = "\"Imagination is more important than knowledge\" - Einstein"
  >> print(wiseWords)
  </ "Imagination is more important than knowledge" - Einstein
  -> let dollarSign = "\u{24}"        // $,  Unicode scalar U+0024
  >> assert(dollarSign == "$")
  -> let blackHeart = "\u{2665}"      // ♥,  Unicode scalar U+2665
  >> assert(blackHeart == "♥")
  -> let sparklingHeart = "\u{1F496}" // 💖, Unicode scalar U+1F496
  >> assert(sparklingHeart == "💖")
  ```
-->

Como literais de string multilinha usam três aspas duplas em vez de apenas uma,
você pode incluir uma aspa dupla (`"`) dentro de um literal de string multilinha
sem escapá-la.
Para incluir o texto `"""` em uma string multilinha,
escape ao menos uma das aspas com barra invertida.
Por exemplo:

```swift
let threeDoubleQuotationMarks = """
Escaping the first quotation mark \"""
Escaping all three quotation marks \"\"\"
"""
```

<!--
  - test: `multiline-string-literals`

  ```swifttest
  -> let threeDoubleQuotationMarks = """
     Escaping the first quotation mark \"""
     Escaping all three quotation marks \"\"\"
     """
  >> print(threeDoubleQuotationMarks)
  << Escaping the first quotation mark """
  << Escaping all three quotation marks """
  ```
-->

### Delimitadores estendidos de string

Você pode colocar um literal de string dentro de *delimitadores estendidos*
para incluir caracteres especiais em uma string
sem que eles sejam interpretados.
Você coloca sua string entre aspas (`"`)
e envolve tudo com sinais de número (`#`).
Por exemplo, imprimir o literal de string `#"Line 1\nLine 2"#`
imprime a sequência de escape de quebra de linha (`\n`)
em vez de imprimir a string em duas linhas.

Se você precisar do efeito especial de um caractere em um literal de string,
use a mesma quantidade de sinais de número na string
depois do caractere de escape (`\`).
Por exemplo, se a sua string é `#"Line 1\nLine 2"#`
e você quer quebrar a linha,
pode usar `#"Line 1\#nLine 2"#` em vez disso.
Da mesma forma, `###"Line1\###nLine2"###` também quebra a linha.

Literais de string criados com delimitadores estendidos também podem ser literais de string multilinha.
Você pode usar delimitadores estendidos para incluir o texto `"""` em uma string multilinha,
substituindo o comportamento padrão que encerra o literal. Por exemplo:

```swift
let threeMoreDoubleQuotationMarks = #"""
Here are three more double quotes: """
"""#
```

<!--
  - test: `extended-string-delimiters`

  ```swifttest
  -> let threeMoreDoubleQuotationMarks = #"""
     Here are three more double quotes: """
     """#
  >> print(threeMoreDoubleQuotationMarks)
  << Here are three more double quotes: """
  ```
-->

## Inicializando uma string vazia

Para criar um valor `String` vazio como ponto de partida
para construir uma string maior,
atribua um literal de string vazio a uma variável
ou inicialize uma nova instância de `String` com a sintaxe de inicializador:

```swift
var emptyString = ""               // empty string literal
var anotherEmptyString = String()  // initializer syntax
// these two strings are both empty, and are equivalent to each other
```

<!--
  - test: `emptyStrings`

  ```swifttest
  -> var emptyString = ""               // empty string literal
  -> var anotherEmptyString = String()  // initializer syntax
  // these two strings are both empty, and are equivalent to each other
  >> assert(emptyString == anotherEmptyString)
  ```
-->

Descubra se um valor `String` está vazio
verificando sua propriedade booleana `isEmpty`:

```swift
if emptyString.isEmpty {
    print("Nothing to see here")
}
// Prints "Nothing to see here".
```

<!--
  - test: `emptyStrings`

  ```swifttest
  -> if emptyString.isEmpty {
        print("Nothing to see here")
     }
  <- Nothing to see here
  ```
-->

<!--
  TODO: init(size, character)
-->

## Mutabilidade de strings

Você indica se uma `String` específica pode ser modificada (ou *mutada*)
atribuindo-a a uma variável (caso em que ela pode ser modificada),
ou a uma constante (caso em que ela não pode ser modificada):

```swift
var variableString = "Horse"
variableString += " and carriage"
// variableString is now "Horse and carriage"

let constantString = "Highlander"
constantString += " and another Highlander"
// this reports a compile-time error - a constant string cannot be modified
```

<!--
  - test: `stringMutability`

  ```swifttest
  -> var variableString = "Horse"
  -> variableString += " and carriage"
  // variableString is now "Horse and carriage"

  -> let constantString = "Highlander"
  -> constantString += " and another Highlander"
  !$ error: left side of mutating operator isn't mutable: 'constantString' is a 'let' constant
  !! constantString += " and another Highlander"
  !! ~~~~~~~~~~~~~~ ^
  !$ note: change 'let' to 'var' to make it mutable
  !! let constantString = "Highlander"
  !! ^~~
  !! var
  // this reports a compile-time error - a constant string cannot be modified
  ```
-->

<!--
  - test: `stringMutability-ok`

  ```swifttest
  -> var variableString = "Horse"
  -> variableString += " and carriage"
  /> variableString is now \"\(variableString)\"
  </ variableString is now "Horse and carriage"
  ```
-->

> Nota: Essa abordagem é diferente da mutação de strings no Objective-C e no Cocoa,
> em que você escolhe entre duas classes (`NSString` e `NSMutableString`)
> para indicar se uma string pode ser mutada.

## Strings são tipos por valor

O tipo `String` do Swift é um *tipo por valor*.
Se você criar um novo valor `String`,
esse valor `String` é *copiado* quando é passado para uma função ou método,
ou quando é atribuído a uma constante ou variável.
Em cada caso, uma nova cópia do valor `String` existente é criada,
e a nova cópia é passada ou atribuída, não a versão original.
Tipos por valor são descritos em <doc:ClassesAndStructures#Structures-and-Enumerations-Are-Value-Types>.

O comportamento padrão do Swift de copiar `String` garante que,
quando uma função ou método passa para você um valor `String`,
fica claro que você é dono desse valor `String` exato,
independentemente de onde ele veio.
Você pode ter certeza de que a string recebida não será modificada
a menos que você mesmo a modifique.

Nos bastidores, o compilador do Swift otimiza o uso de strings
para que a cópia real só aconteça quando for absolutamente necessária.
Isso significa que você sempre tem ótimo desempenho
ao trabalhar com strings como tipos por valor.

## Trabalhando com caracteres

Você pode acessar os valores `Character` individuais de uma `String`
percorrendo a string com um laço `for`-`in`:

```swift
for character in "Dog!🐶" {
    print(character)
}
// D
// o
// g
// !
// 🐶
```

<!--
  - test: `characters`

  ```swifttest
  -> for character in "Dog!🐶" {
        print(character)
     }
  </ D
  </ o
  </ g
  </ !
  </ 🐶
  ```
-->

O laço `for`-`in` é descrito em <doc:ControlFlow#For-In-Loops>.

Como alternativa, você pode criar uma constante ou variável `Character` independente
a partir de um literal de string de um único caractere, fornecendo uma anotação de tipo `Character`:

```swift
let exclamationMark: Character = "!"
```

<!--
  - test: `characters`

  ```swifttest
  -> let exclamationMark: Character = "!"
  ```
-->

Valores `String` podem ser construídos passando um array de valores `Character`
como argumento para o seu inicializador:

```swift
let catCharacters: [Character] = ["C", "a", "t", "!", "🐱"]
let catString = String(catCharacters)
print(catString)
// Prints "Cat!🐱".
```

<!--
  - test: `characters`

  ```swifttest
  -> let catCharacters: [Character] = ["C", "a", "t", "!", "🐱"]
  -> let catString = String(catCharacters)
  -> print(catString)
  <- Cat!🐱
  ```
-->

## Concatenando strings e caracteres

Valores `String` podem ser somados (ou *concatenados*)
com o operador de adição (`+`) para criar um novo valor `String`:

```swift
let string1 = "hello"
let string2 = " there"
var welcome = string1 + string2
// welcome now equals "hello there"
```

<!--
  - test: `concatenation`

  ```swifttest
  -> let string1 = "hello"
  -> let string2 = " there"
  -> var welcome = string1 + string2
  /> welcome now equals \"\(welcome)\"
  </ welcome now equals "hello there"
  ```
-->

Você também pode acrescentar um valor `String` a uma variável `String` existente
com o operador de atribuição por adição (`+=`):

```swift
var instruction = "look over"
instruction += string2
// instruction now equals "look over there"
```

<!--
  - test: `concatenation`

  ```swifttest
  -> var instruction = "look over"
  -> instruction += string2
  /> instruction now equals \"\(instruction)\"
  </ instruction now equals "look over there"
  ```
-->

Você pode acrescentar um valor `Character` a uma variável `String`
com o método `append()` do tipo `String`:

```swift
let exclamationMark: Character = "!"
welcome.append(exclamationMark)
// welcome now equals "hello there!"
```

<!--
  - test: `concatenation`

  ```swifttest
  -> let exclamationMark: Character = "!"
  -> welcome.append(exclamationMark)
  /> welcome now equals \"\(welcome)\"
  </ welcome now equals "hello there!"
  ```
-->

> Nota: Você não pode acrescentar uma `String` ou um `Character` a uma variável `Character` existente,
> porque um valor `Character` deve conter um único caractere apenas.

Se você estiver usando literais de string multilinha
para montar as linhas de uma string maior,
quer que cada linha da string termine com uma quebra de linha,
inclusive a última.
Por exemplo:

```swift
let badStart = """
    one
    two
    """
let end = """
    three
    """
print(badStart + end)
// Prints two lines:
// one
// twothree

let goodStart = """
    one
    two

    """
print(goodStart + end)
// Prints three lines:
// one
// two
// three
```

<!--
  - test: `concatenate-multiline-string-literals`

  ```swifttest
  -> let badStart = """
         one
         two
         """
  -> let end = """
         three
         """
  -> print(badStart + end)
  // Prints two lines:
  </ one
  </ twothree

  -> let goodStart = """
         one
         two

         """
  -> print(goodStart + end)
  // Prints three lines:
  </ one
  </ two
  </ three
  ```
-->

No código acima,
concatenar `badStart` com `end`
produz uma string de duas linhas,
o que não é o resultado desejado.
Como a última linha de `badStart`
não termina com uma quebra de linha,
essa linha é combinada com a primeira linha de `end`.
Já as duas linhas de `goodStart` terminam com quebra de linha,
então, quando combinada com `end`,
o resultado tem três linhas, como esperado.

## Interpolação de strings

*Interpolação de string* é uma forma de construir um novo valor `String`
a partir de uma mistura de constantes, variáveis, literais e expressões,
incluindo os valores deles dentro de um literal de string.
Você pode usar interpolação de strings
tanto em literais de string de uma linha quanto em multilinha.
Cada item que você insere no literal de string fica envolvido por
um par de parênteses, precedido por uma barra invertida (`\`):

```swift
let multiplier = 3
let message = "\(multiplier) times 2.5 is \(Double(multiplier) * 2.5)"
// message is "3 times 2.5 is 7.5"
```

<!--
  - test: `stringInterpolation`

  ```swifttest
  -> let multiplier = 3
  -> let message = "\(multiplier) times 2.5 is \(Double(multiplier) * 2.5)"
  /> message is \"\(message)\"
  </ message is "3 times 2.5 is 7.5"
  ```
-->

No exemplo acima,
o valor de `multiplier` é inserido em um literal de string como `\(multiplier)`.
Esse marcador é substituído pelo valor real de `multiplier`
quando a interpolação de string é avaliada para criar uma string real.

O valor de `multiplier` também faz parte de uma expressão maior mais adiante na string.
Essa expressão calcula o valor de `Double(multiplier) * 2.5`
e insere o resultado (`7.5`) na string.
Nesse caso, a expressão é escrita como `\(Double(multiplier) * 2.5)`
quando incluída dentro do literal de string.

Você pode usar delimitadores estendidos de string para criar strings que contêm
caracteres que, de outra forma, seriam tratados como interpolação de string.
Por exemplo:

```swift
print(#"Write an interpolated string in Swift using \(multiplier)."#)
// Prints "Write an interpolated string in Swift using \(multiplier)."
```

<!--
  - test: `stringInterpolation`

  ```swifttest
  -> print(#"Write an interpolated string in Swift using \(multiplier)."#)
  <- Write an interpolated string in Swift using \(multiplier).
  ```
-->

Para usar interpolação de string
dentro de uma string que usa delimitadores estendidos,
faça a quantidade de sinais de número depois da barra invertida
corresponder à quantidade de sinais de número no início e no fim da string.
Por exemplo:

```swift
print(#"6 times 7 is \#(6 * 7)."#)
// Prints "6 times 7 is 42."
```

<!--
  - test: `stringInterpolation`

  ```swifttest
  -> print(#"6 times 7 is \#(6 * 7)."#)
  <- 6 times 7 is 42.
  ```
-->

> Nota: As expressões que você escreve entre parênteses dentro de uma string interpolada
> não podem conter uma barra invertida (`\`) sem escape, um retorno de carro ou uma quebra de linha.
> No entanto, elas podem conter outros literais de string.

## Unicode

*Unicode* é um padrão internacional para
codificar, representar e processar texto em diferentes sistemas de escrita.
Ele permite representar quase qualquer caractere de qualquer idioma de forma padronizada,
e ler e escrever esses caracteres a partir de uma fonte externa,
como um arquivo de texto ou uma página web.
Os tipos `String` e `Character` do Swift são totalmente compatíveis com Unicode,
como descrito nesta seção.

### Valores escalares Unicode

Nos bastidores,
o tipo `String` nativo do Swift é construído a partir de *valores escalares Unicode*.
Um valor escalar Unicode é um número único de 21 bits para um caractere ou modificador,
como `U+0061` para `LATIN SMALL LETTER A` (`"a"`),
ou `U+1F425` para `FRONT-FACING BABY CHICK` (`"🐥"`).

Note que nem todos os valores escalares Unicode de 21 bits são atribuídos a um caractere:
alguns escalares são reservados para atribuição futura ou para uso na codificação UTF-16.
Valores escalares atribuídos a um caractere normalmente também têm um nome,
como `LATIN SMALL LETTER A` e `FRONT-FACING BABY CHICK` nos exemplos acima.

### Clusters de grafemas estendidos

Cada instância do tipo `Character` do Swift representa
um único *cluster de grafemas estendido*.
Um cluster de grafemas estendido é uma sequência de um ou mais escalares Unicode
que, combinados, produzem um único caractere legível por humanos.

Aqui está um exemplo.
A letra `é` pode ser representada como o único escalar Unicode `é`
(`LATIN SMALL LETTER E WITH ACUTE`, ou `U+00E9`).
No entanto, a mesma letra também pode ser representada como um *par* de escalares:
uma letra `e` comum (`LATIN SMALL LETTER E`, ou `U+0065`),
seguida do escalar `COMBINING ACUTE ACCENT` (`U+0301`).
O escalar `COMBINING ACUTE ACCENT` é aplicado graficamente ao escalar que o precede,
transformando um `e` em um `é` quando é renderizado por
um sistema de renderização de texto que entende Unicode.

Nos dois casos, a letra `é` é representada como um único valor `Character` do Swift
que representa um cluster de grafemas estendido.
No primeiro caso, o cluster contém um único escalar;
no segundo caso, é um cluster de dois escalares:

```swift
let eAcute: Character = "\u{E9}"                         // é
let combinedEAcute: Character = "\u{65}\u{301}"          // e followed by ́
// eAcute is é, combinedEAcute is é
```

<!--
  - test: `graphemeClusters1`

  ```swifttest
  -> let eAcute: Character = "\u{E9}"                         // é
  >> assert(eAcute == "é")
  -> let combinedEAcute: Character = "\u{65}\u{301}"          // e followed by ́
  >> assert(combinedEAcute == "é")
  /> eAcute is \(eAcute), combinedEAcute is \(combinedEAcute)
  </ eAcute is é, combinedEAcute is é
  >> assert(eAcute == combinedEAcute)
  ```
-->

Clusters de grafemas estendidos são uma forma flexível de representar
muitos caracteres de escritas complexas como um único valor `Character`.
Por exemplo, sílabas coreanas do alfabeto hangul
podem ser representadas como uma sequência pré-composta ou decomposta.
As duas representações se qualificam como um único valor `Character` no Swift:

```swift
let precomposed: Character = "\u{D55C}"                  // 한
let decomposed: Character = "\u{1112}\u{1161}\u{11AB}"   // ᄒ, ᅡ, ᆫ
// precomposed is 한, decomposed is 한
```

<!--
  - test: `graphemeClusters2`

  ```swifttest
  -> let precomposed: Character = "\u{D55C}"                  // 한
  >> assert(precomposed == "한")
  -> let decomposed: Character = "\u{1112}\u{1161}\u{11AB}"   // ᄒ, ᅡ, ᆫ
  >> assert(decomposed == "한")
  /> precomposed is \(precomposed), decomposed is \(decomposed)
  </ precomposed is 한, decomposed is 한
  ```
-->

Clusters de grafemas estendidos permitem que escalares de marcas envolventes
(como `COMBINING ENCLOSING CIRCLE`, ou `U+20DD`)
envolvam outros escalares Unicode como parte de um único valor `Character`:

```swift
let enclosedEAcute: Character = "\u{E9}\u{20DD}"
// enclosedEAcute is é⃝
```

<!--
  - test: `graphemeClusters3`

  ```swifttest
  -> let enclosedEAcute: Character = "\u{E9}\u{20DD}"
  >> assert(enclosedEAcute == "é⃝")
  /> enclosedEAcute is \(enclosedEAcute)
  </ enclosedEAcute is é⃝
  ```
-->

Escalares Unicode para símbolos de indicadores regionais
podem ser combinados em pares para formar um único valor `Character`,
como esta combinação de `REGIONAL INDICATOR SYMBOL LETTER U` (`U+1F1FA`)
e `REGIONAL INDICATOR SYMBOL LETTER S` (`U+1F1F8`):

```swift
let regionalIndicatorForUS: Character = "\u{1F1FA}\u{1F1F8}"
// regionalIndicatorForUS is 🇺🇸
```

<!--
  - test: `graphemeClusters4`

  ```swifttest
  -> let regionalIndicatorForUS: Character = "\u{1F1FA}\u{1F1F8}"
  >> assert(regionalIndicatorForUS == "🇺🇸")
  /> regionalIndicatorForUS is \(regionalIndicatorForUS)
  </ regionalIndicatorForUS is 🇺🇸
  ```
-->

## Contando caracteres

Para obter a quantidade de valores `Character` em uma string,
use a propriedade `count` da string:

```swift
let unusualMenagerie = "Koala 🐨, Snail 🐌, Penguin 🐧, Dromedary 🐪"
print("unusualMenagerie has \(unusualMenagerie.count) characters")
// Prints "unusualMenagerie has 40 characters".
```

<!--
  - test: `characterCount`

  ```swifttest
  -> let unusualMenagerie = "Koala 🐨, Snail 🐌, Penguin 🐧, Dromedary 🐪"
  -> print("unusualMenagerie has \(unusualMenagerie.count) characters")
  <- unusualMenagerie has 40 characters
  ```
-->

Observe que o uso de clusters de grafemas estendidos pelo Swift para valores `Character`
significa que concatenação e modificação de strings nem sempre afetam
a contagem de caracteres de uma string.

Por exemplo, se você inicializar uma nova string com a palavra de quatro caracteres `cafe`
e depois acrescentar um `COMBINING ACUTE ACCENT` (`U+0301`) ao fim da string,
a string resultante ainda terá contagem de caracteres `4`,
com um quarto caractere `é`, e não `e`:

```swift
var word = "cafe"
print("the number of characters in \(word) is \(word.count)")
// Prints "the number of characters in cafe is 4".

word += "\u{301}"    // COMBINING ACUTE ACCENT, U+0301

print("the number of characters in \(word) is \(word.count)")
// Prints "the number of characters in café is 4".
```

<!--
  - test: `characterCount`

  ```swifttest
  -> var word = "cafe"
  -> print("the number of characters in \(word) is \(word.count)")
  <- the number of characters in cafe is 4

  -> word += "\u{301}"    // COMBINING ACUTE ACCENT, U+0301

  -> print("the number of characters in \(word) is \(word.count)")
  <- the number of characters in café is 4
  ```
-->

> Nota: Clusters de grafemas estendidos podem ser compostos de vários escalares Unicode.
> Por isso, caracteres diferentes, e representações diferentes do mesmo caractere,
> podem exigir quantidades diferentes de memória para armazenamento.
> Assim, os caracteres em Swift não ocupam a mesma quantidade de memória
> dentro da representação de uma string.
> Como resultado, a quantidade de caracteres de uma string não pode ser calculada
> sem percorrer a string para determinar
> os limites de seus clusters de grafemas estendidos.
> Se você trabalha com valores de string particularmente longos,
> lembre-se de que a propriedade `count`
> precisa percorrer os escalares Unicode de toda a string
> para determinar os caracteres dessa string.
>
> A contagem de caracteres retornada pela propriedade `count`
> nem sempre é igual à propriedade `length` de
> um `NSString` que contém os mesmos caracteres.
> O comprimento de um `NSString` é baseado
> na quantidade de unidades de código de 16 bits da representação UTF-16 da string,
> e não na quantidade de clusters de grafemas estendidos Unicode da string.

## Acessando e modificando uma string

Você acessa e modifica uma string por meio de seus métodos e propriedades,
ou usando a sintaxe de subscript.

### Índices de string

Cada valor `String` tem um *tipo de índice* associado,
`String.Index`,
que corresponde à posição de cada `Character` na string.

Como mencionado acima,
caracteres diferentes podem exigir quantidades diferentes de memória para armazenamento,
então, para determinar qual `Character` está em uma posição específica,
é preciso percorrer cada escalar Unicode desde o início ou o fim da `String`.
Por isso, strings em Swift não podem ser indexadas por valores inteiros.

Use a propriedade `startIndex` para acessar
a posição do primeiro `Character` de uma `String`.
A propriedade `endIndex` é a posição logo após o último caractere de uma `String`.
Por isso,
a propriedade `endIndex` não é um argumento válido para o subscript de uma string.
Se uma `String` estiver vazia, `startIndex` e `endIndex` são iguais.

Você acessa os índices antes e depois de um índice dado
usando os métodos `index(before:)` e `index(after:)` de `String`.
Para acessar um índice mais distante do índice dado,
você pode usar o método `index(_:offsetBy:)`
em vez de chamar um desses métodos várias vezes.

Você pode usar a sintaxe de subscript para acessar
o `Character` em um índice específico de `String`.

```swift
let greeting = "Guten Tag!"
greeting[greeting.startIndex]
// G
greeting[greeting.index(before: greeting.endIndex)]
// !
greeting[greeting.index(after: greeting.startIndex)]
// u
let index = greeting.index(greeting.startIndex, offsetBy: 7)
greeting[index]
// a
```

<!--
  - test: `stringIndex`

  ```swifttest
  -> let greeting = "Guten Tag!"
  >> print(
  -> greeting[greeting.startIndex]
  >> )
  << G
  // G
  >> print(
  -> greeting[greeting.index(before: greeting.endIndex)]
  >> )
  << !
  // !
  >> print(
  -> greeting[greeting.index(after: greeting.startIndex)]
  >> )
  << u
  // u
  -> let index = greeting.index(greeting.startIndex, offsetBy: 7)
  >> print(
  -> greeting[index]
  >> )
  << a
  // a
  ```
-->

Tentar acessar um índice fora do intervalo de uma string,
ou um `Character` em um índice fora do intervalo de uma string,
vai disparar um erro em tempo de execução.

```swift
greeting[greeting.endIndex] // Error
greeting.index(after: greeting.endIndex) // Error
```

<!--
  The code above triggers an assertion failure in the stdlib, causing a stack
  trace, which makes it a poor candidate for being tested.
-->

<!--
  - test: `emptyStringIndices`

  ```swifttest
  -> let emptyString = ""
  -> assert(
  -> emptyString.isEmpty && emptyString.startIndex == emptyString.endIndex
  -> )
  ```
-->

Use a propriedade `indices` para acessar todos os
índices dos caracteres individuais de uma string.

```swift
for index in greeting.indices {
    print("\(greeting[index]) ", terminator: "")
}
// Prints "G u t e n   T a g ! ".
```

<!--
  - test: `stringIndex`

  ```swifttest
  -> for index in greeting.indices {
        print("\(greeting[index]) ", terminator: "")
     }
  >> print("")
  << G u t e n   T a g !
  // Prints "G u t e n   T a g ! ".
  ```
-->

<!--
  Workaround for rdar://26016325
-->

> Nota: Você pode usar as propriedades `startIndex` e `endIndex`
> e os métodos `index(before:)`, `index(after:)` e `index(_:offsetBy:)`
> em qualquer tipo que esteja em conformidade com o protocolo `Collection`.
> Isso inclui `String`, como mostrado aqui,
> bem como tipos de coleção como `Array`, `Dictionary` e `Set`.

### Inserindo e removendo

Para inserir um único caractere em uma string em um índice especificado,
use o método `insert(_:at:)`,
e para inserir o conteúdo de outra string em um índice especificado,
use o método `insert(contentsOf:at:)`.

```swift
var welcome = "hello"
welcome.insert("!", at: welcome.endIndex)
// welcome now equals "hello!"

welcome.insert(contentsOf: " there", at: welcome.index(before: welcome.endIndex))
// welcome now equals "hello there!"
```

<!--
  - test: `stringInsertionAndRemoval`

  ```swifttest
  -> var welcome = "hello"
  -> welcome.insert("!", at: welcome.endIndex)
  /> welcome now equals \"\(welcome)\"
  </ welcome now equals "hello!"

  -> welcome.insert(contentsOf: " there", at: welcome.index(before: welcome.endIndex))
  /> welcome now equals \"\(welcome)\"
  </ welcome now equals "hello there!"
  ```
-->

Para remover um único caractere de uma string em um índice especificado,
use o método `remove(at:)`,
e para remover uma substring em um intervalo especificado,
use o método `removeSubrange(_:)`:

```swift
welcome.remove(at: welcome.index(before: welcome.endIndex))
// welcome now equals "hello there"

let range = welcome.index(welcome.endIndex, offsetBy: -6)..<welcome.endIndex
welcome.removeSubrange(range)
// welcome now equals "hello"
```

<!--
  - test: `stringInsertionAndRemoval`

  ```swifttest
  -> welcome.remove(at: welcome.index(before: welcome.endIndex))
  /> welcome now equals \"\(welcome)\"
  </ welcome now equals "hello there"

  -> let range = welcome.index(welcome.endIndex, offsetBy: -6)..<welcome.endIndex
  -> welcome.removeSubrange(range)
  /> welcome now equals \"\(welcome)\"
  </ welcome now equals "hello"
  ```
-->

<!--
  TODO: Find and Replace section, once the Swift standard library supports finding substrings
-->

> Nota: Você pode usar os métodos `insert(_:at:)`, `insert(contentsOf:at:)`,
> `remove(at:)` e `removeSubrange(_:)`
> em qualquer tipo que esteja em conformidade com o protocolo `RangeReplaceableCollection`.
> Isso inclui `String`, como mostrado aqui,
> bem como tipos de coleção como `Array`, `Dictionary` e `Set`.

## Substrings

Quando você obtém uma substring de uma string,
por exemplo usando um subscript ou um método como `prefix(_:)`,
o resultado é uma instância
de [`Substring`](https://developer.apple.com/documentation/swift/substring),
e não outra string.
Substrings em Swift têm a maioria dos mesmos métodos das strings,
o que significa que você pode trabalhar com substrings
da mesma forma que trabalha com strings.
No entanto, diferentemente das strings,
você usa substrings apenas por um curto período
enquanto executa ações sobre uma string.
Quando estiver pronto para guardar o resultado por mais tempo,
converta a substring para uma instância de `String`.
Por exemplo:

```swift
let greeting = "Hello, world!"
let index = greeting.firstIndex(of: ",") ?? greeting.endIndex
let beginning = greeting[..<index]
// beginning is "Hello"

// Convert the result to a String for long-term storage.
let newString = String(beginning)
```

<!--
  - test: `string-and-substring`

  ```swifttest
  -> let greeting = "Hello, world!"
  -> let index = greeting.firstIndex(of: ",") ?? greeting.endIndex
  -> let beginning = greeting[..<index]
  /> beginning is \"\(beginning)\"
  </ beginning is "Hello"

  // Convert the result to a String for long-term storage.
  -> let newString = String(beginning)
  ```
-->

Assim como as strings, cada substring tem uma região de memória
onde os caracteres que formam a substring são armazenados.
A diferença entre strings e substrings
é que, como otimização de desempenho,
uma substring pode reaproveitar parte da memória
usada para armazenar a string original,
ou parte da memória usada para armazenar outra substring.
(Strings têm uma otimização semelhante,
mas, se duas strings compartilham memória, elas são iguais.)
Essa otimização de desempenho significa
que você não precisa pagar o custo de desempenho de copiar memória
até modificar a string ou a substring.
Como mencionado acima,
substrings não são adequadas para armazenamento de longo prazo:
como elas reaproveitam o armazenamento da string original,
a string original inteira precisa permanecer na memória
enquanto qualquer uma de suas substrings estiver em uso.

No exemplo acima,
`greeting` é uma string,
o que significa que ela tem uma região de memória
onde os caracteres que formam a string são armazenados.
Como
`beginning` é uma substring de `greeting`,
ela reaproveita a memória que `greeting` usa.
Em contraste,
`newString` é uma string:
quando é criada a partir da substring,
ela tem seu próprio armazenamento.
A figura abaixo mostra essas relações:

<!--
  FIXME: The connection between the code and the figure
  would be clearer if the variable names appeared in the figure.
-->

![](stringSubstring)

> Nota: Tanto `String` quanto `Substring` estão em conformidade com o protocolo
> [`StringProtocol`](https://developer.apple.com/documentation/swift/stringprotocol),
> o que significa que, em geral, é conveniente que funções de manipulação de string
> aceitem um valor `StringProtocol`.
> Você pode chamar essas funções com um valor `String` ou `Substring`.

## Comparando strings

O Swift oferece três formas de comparar valores de texto:
igualdade de string e de caractere, igualdade de prefixo e igualdade de sufixo.

### Igualdade de string e de caractere

A igualdade de string e de caractere é verificada com o operador “igual a” (`==`)
e o operador “diferente de” (`!=`),
como descrito em <doc:BasicOperators#Comparison-Operators>:

```swift
let quotation = "We're a lot alike, you and I."
let sameQuotation = "We're a lot alike, you and I."
if quotation == sameQuotation {
    print("These two strings are considered equal")
}
// Prints "These two strings are considered equal".
```

<!--
  - test: `stringEquality`

  ```swifttest
  -> let quotation = "We're a lot alike, you and I."
  -> let sameQuotation = "We're a lot alike, you and I."
  -> if quotation == sameQuotation {
        print("These two strings are considered equal")
     }
  <- These two strings are considered equal
  ```
-->

Dois valores `String` (ou dois valores `Character`) são considerados iguais se
seus clusters de grafemas estendidos forem *canonicamente equivalentes*.
Clusters de grafemas estendidos são canonicamente equivalentes quando têm
o mesmo significado linguístico e a mesma aparência,
mesmo que sejam compostos de escalares Unicode diferentes nos bastidores.

<!--
  - test: `characterComparisonUsesCanonicalEquivalence`

  ```swifttest
  -> let eAcute: Character = "\u{E9}"
  -> let combinedEAcute: Character = "\u{65}\u{301}"
  -> if eAcute != combinedEAcute {
        print("not equivalent, which isn't expected")
     } else {
        print("equivalent, as expected")
     }
  <- equivalent, as expected
  ```
-->

<!--
  - test: `stringComparisonUsesCanonicalEquivalence`

  ```swifttest
  -> let cafe1 = "caf\u{E9}"
  -> let cafe2 = "caf\u{65}\u{301}"
  -> if cafe1 != cafe2 {
        print("not equivalent, which isn't expected")
     } else {
        print("equivalent, as expected")
     }
  <- equivalent, as expected
  ```
-->

Por exemplo, `LATIN SMALL LETTER E WITH ACUTE` (`U+00E9`)
é canonicamente equivalente a `LATIN SMALL LETTER E` (`U+0065`)
seguida de `COMBINING ACUTE ACCENT` (`U+0301`).
As duas formas são maneiras válidas de representar o caractere `é`,
e por isso são consideradas canonicamente equivalentes:

```swift
// "Voulez-vous un café?" using LATIN SMALL LETTER E WITH ACUTE
let eAcuteQuestion = "Voulez-vous un caf\u{E9}?"

// "Voulez-vous un café?" using LATIN SMALL LETTER E and COMBINING ACUTE ACCENT
let combinedEAcuteQuestion = "Voulez-vous un caf\u{65}\u{301}?"

if eAcuteQuestion == combinedEAcuteQuestion {
    print("These two strings are considered equal")
}
// Prints "These two strings are considered equal".
```

<!--
  - test: `stringEquality`

  ```swifttest
  // "Voulez-vous un café?" using LATIN SMALL LETTER E WITH ACUTE
  -> let eAcuteQuestion = "Voulez-vous un caf\u{E9}?"

  // "Voulez-vous un café?" using LATIN SMALL LETTER E and COMBINING ACUTE ACCENT
  -> let combinedEAcuteQuestion = "Voulez-vous un caf\u{65}\u{301}?"

  -> if eAcuteQuestion == combinedEAcuteQuestion {
        print("These two strings are considered equal")
     }
  <- These two strings are considered equal
  ```
-->

Por outro lado, `LATIN CAPITAL LETTER A` (`U+0041`, ou `"A"`),
usado em inglês, *não* é equivalente a
`CYRILLIC CAPITAL LETTER A` (`U+0410`, ou `"А"`),
usado em russo.
Os caracteres são visualmente parecidos,
mas não têm o mesmo significado linguístico:

```swift
let latinCapitalLetterA: Character = "\u{41}"

let cyrillicCapitalLetterA: Character = "\u{0410}"

if latinCapitalLetterA != cyrillicCapitalLetterA {
    print("These two characters aren't equivalent.")
}
// Prints "These two characters aren't equivalent."
```

<!--
  - test: `stringEquality`

  ```swifttest
  -> let latinCapitalLetterA: Character = "\u{41}"
  >> assert(latinCapitalLetterA == "A")

  -> let cyrillicCapitalLetterA: Character = "\u{0410}"
  >> assert(cyrillicCapitalLetterA == "А")

  -> if latinCapitalLetterA != cyrillicCapitalLetterA {
        print("These two characters aren't equivalent.")
     }
  <- These two characters aren't equivalent.
  ```
-->

> Nota: Comparações de string e de caractere em Swift não são sensíveis à localidade.

<!--
  TODO: Add a cross reference to NSString.localizedCompare and
  NSString.localizedCaseInsensitiveCompare.  See also
  https://developer.apple.com/library/ios/documentation/Cocoa/Conceptual/Strings/Articles/SearchingStrings.html#//apple_ref/doc/uid/20000149-SW4
-->

### Igualdade de prefixo e de sufixo

Para verificar se uma string tem determinado prefixo ou sufixo de string,
chame os métodos `hasPrefix(_:)` e `hasSuffix(_:)` da string:
ambos recebem um único argumento do tipo `String` e retornam um valor booleano.

<!--
  - test: `prefixComparisonUsesCharactersNotScalars`

  ```swifttest
  -> let ecole = "\u{E9}cole"
  -> if ecole.hasPrefix("\u{E9}") {
        print("Has U+00E9 prefix, as expected.")
     } else {
        print("Does not have U+00E9 prefix, which is unexpected.")
     }
  <- Has U+00E9 prefix, as expected.
  -> if ecole.hasPrefix("\u{65}\u{301}") {
        print("Has U+0065 U+0301 prefix, as expected.")
     } else {
        print("Does not have U+0065 U+0301 prefix, which is unexpected.")
     }
  <- Has U+0065 U+0301 prefix, as expected.
  ```
-->

<!--
  - test: `suffixComparisonUsesCharactersNotScalars`

  ```swifttest
  -> let cafe = "caf\u{E9}"
  -> if cafe.hasSuffix("\u{E9}") {
        print("Has U+00E9 suffix, as expected.")
     } else {
        print("Does not have U+00E9 suffix, which is unexpected.")
     }
  <- Has U+00E9 suffix, as expected.
  -> if cafe.hasSuffix("\u{65}\u{301}") {
        print("Has U+0065 U+0301 suffix, as expected.")
     } else {
        print("Does not have U+0065 U+0301 suffix, which is unexpected.")
     }
  <- Has U+0065 U+0301 suffix, as expected.
  ```
-->

Os exemplos abaixo consideram um array de strings que representam
os locais das cenas dos dois primeiros atos de *Romeu e Julieta*, de Shakespeare:

```swift
let romeoAndJuliet = [
    "Act 1 Scene 1: Verona, A public place",
    "Act 1 Scene 2: Capulet's mansion",
    "Act 1 Scene 3: A room in Capulet's mansion",
    "Act 1 Scene 4: A street outside Capulet's mansion",
    "Act 1 Scene 5: The Great Hall in Capulet's mansion",
    "Act 2 Scene 1: Outside Capulet's mansion",
    "Act 2 Scene 2: Capulet's orchard",
    "Act 2 Scene 3: Outside Friar Lawrence's cell",
    "Act 2 Scene 4: A street in Verona",
    "Act 2 Scene 5: Capulet's mansion",
    "Act 2 Scene 6: Friar Lawrence's cell"
]
```

<!--
  - test: `prefixesAndSuffixes`

  ```swifttest
  -> let romeoAndJuliet = [
        "Act 1 Scene 1: Verona, A public place",
        "Act 1 Scene 2: Capulet's mansion",
        "Act 1 Scene 3: A room in Capulet's mansion",
        "Act 1 Scene 4: A street outside Capulet's mansion",
        "Act 1 Scene 5: The Great Hall in Capulet's mansion",
        "Act 2 Scene 1: Outside Capulet's mansion",
        "Act 2 Scene 2: Capulet's orchard",
        "Act 2 Scene 3: Outside Friar Lawrence's cell",
        "Act 2 Scene 4: A street in Verona",
        "Act 2 Scene 5: Capulet's mansion",
        "Act 2 Scene 6: Friar Lawrence's cell"
     ]
  ```
-->

Você pode usar o método `hasPrefix(_:)` com o array `romeoAndJuliet`
para contar o número de cenas do Ato 1 da peça:

```swift
var act1SceneCount = 0
for scene in romeoAndJuliet {
    if scene.hasPrefix("Act 1 ") {
        act1SceneCount += 1
    }
}
print("There are \(act1SceneCount) scenes in Act 1")
// Prints "There are 5 scenes in Act 1".
```

<!--
  - test: `prefixesAndSuffixes`

  ```swifttest
  -> var act1SceneCount = 0
  -> for scene in romeoAndJuliet {
        if scene.hasPrefix("Act 1 ") {
           act1SceneCount += 1
        }
     }
  -> print("There are \(act1SceneCount) scenes in Act 1")
  <- There are 5 scenes in Act 1
  ```
-->

Da mesma forma, use o método `hasSuffix(_:)` para contar o número de cenas
que acontecem em ou ao redor da mansão dos Capuleto e da cela de Frei Lourenço:

```swift
var mansionCount = 0
var cellCount = 0
for scene in romeoAndJuliet {
    if scene.hasSuffix("Capulet's mansion") {
        mansionCount += 1
    } else if scene.hasSuffix("Friar Lawrence's cell") {
        cellCount += 1
    }
}
print("\(mansionCount) mansion scenes; \(cellCount) cell scenes")
// Prints "6 mansion scenes; 2 cell scenes".
```

<!--
  - test: `prefixesAndSuffixes`

  ```swifttest
  -> var mansionCount = 0
  -> var cellCount = 0
  -> for scene in romeoAndJuliet {
        if scene.hasSuffix("Capulet's mansion") {
           mansionCount += 1
        } else if scene.hasSuffix("Friar Lawrence's cell") {
           cellCount += 1
        }
     }
  -> print("\(mansionCount) mansion scenes; \(cellCount) cell scenes")
  <- 6 mansion scenes; 2 cell scenes
  ```
-->

> Nota: Os métodos `hasPrefix(_:)` e `hasSuffix(_:)`
> fazem uma comparação de equivalência canônica, caractere por caractere, entre
> os clusters de grafemas estendidos de cada string,
> como descrito em <doc:StringsAndCharacters#String-and-Character-Equality>.

## Representações Unicode de strings

Quando uma string Unicode é gravada em um arquivo de texto ou em outro armazenamento,
os escalares Unicode dessa string são codificados em uma de
várias *formas de codificação* definidas pelo Unicode.
Cada forma codifica a string em pequenos blocos chamados *unidades de código*.
Entre elas estão a forma de codificação UTF-8 (que codifica uma string em unidades de código de 8 bits),
a forma UTF-16 (que codifica uma string em unidades de código de 16 bits),
e a forma UTF-32 (que codifica uma string em unidades de código de 32 bits).

O Swift oferece várias maneiras diferentes de acessar representações Unicode de strings.
Você pode percorrer a string com uma instrução `for`-`in`
para acessar seus valores `Character` individuais como clusters de grafemas estendidos Unicode.
Esse processo é descrito em <doc:StringsAndCharacters#Working-with-Characters>.

Como alternativa, acesse um valor `String`
em uma das três outras representações compatíveis com Unicode:

- Uma coleção de unidades de código UTF-8 (acessada com a propriedade `utf8` da string)
- Uma coleção de unidades de código UTF-16 (acessada com a propriedade `utf16` da string)
- Uma coleção de valores escalares Unicode de 21 bits,
  equivalente à forma de codificação UTF-32 da string
  (acessada com a propriedade `unicodeScalars` da string)

Cada exemplo abaixo mostra uma representação diferente da seguinte string,
composta pelos caracteres `D`, `o`, `g`,
`‼` (`DOUBLE EXCLAMATION MARK`, ou escalar Unicode `U+203C`),
e pelo caractere 🐶 (`DOG FACE`, ou escalar Unicode `U+1F436`):

```swift
let dogString = "Dog‼🐶"
```

<!--
  - test: `unicodeRepresentations`

  ```swifttest
  -> let dogString = "Dog‼🐶"
  ```
-->

### Representação UTF-8

Você pode acessar uma representação UTF-8 de uma `String`
percorrendo sua propriedade `utf8`.
Essa propriedade é do tipo `String.UTF8View`,
que é uma coleção de valores `UInt8` sem sinal de 8 bits,
um para cada byte da representação UTF-8 da string:

![](UTF8)

```swift
for codeUnit in dogString.utf8 {
    print("\(codeUnit) ", terminator: "")
}
print("")
// Prints "68 111 103 226 128 188 240 159 144 182 ".
```

<!--
  - test: `unicodeRepresentations`

  ```swifttest
  -> for codeUnit in dogString.utf8 {
        print("\(codeUnit) ", terminator: "")
     }
  -> print("")
  << 68 111 103 226 128 188 240 159 144 182
  // Prints "68 111 103 226 128 188 240 159 144 182 ".
  ```
-->

<!--
  Workaround for rdar://26016325
-->

No exemplo acima, os três primeiros valores decimais `codeUnit`
(`68`, `111`, `103`)
representam os caracteres `D`, `o` e `g`,
cuja representação UTF-8 é igual à representação ASCII deles.
Os três valores decimais `codeUnit` seguintes
(`226`, `128`, `188`)
são uma representação UTF-8 de três bytes do caractere `DOUBLE EXCLAMATION MARK`.
Os últimos quatro valores `codeUnit` (`240`, `159`, `144`, `182`)
são uma representação UTF-8 de quatro bytes do caractere `DOG FACE`.

<!--
  TODO: contiguousUTF8()
-->

<!--
  TODO: nulTerminatedUTF8()
  (which returns a NativeArray, but handwave this for now)
-->

### Representação UTF-16

Você pode acessar uma representação UTF-16 de uma `String`
percorrendo sua propriedade `utf16`.
Essa propriedade é do tipo `String.UTF16View`,
que é uma coleção de valores `UInt16` sem sinal de 16 bits,
um para cada unidade de código de 16 bits da representação UTF-16 da string:

![](UTF16)

```swift
for codeUnit in dogString.utf16 {
    print("\(codeUnit) ", terminator: "")
}
print("")
// Prints "68 111 103 8252 55357 56374 ".
```

<!--
  - test: `unicodeRepresentations`

  ```swifttest
  -> for codeUnit in dogString.utf16 {
        print("\(codeUnit) ", terminator: "")
     }
  -> print("")
  << 68 111 103 8252 55357 56374
  // Prints "68 111 103 8252 55357 56374 ".
  ```
-->

<!--
  Workaround for rdar://26016325
-->

Novamente, os primeiros três valores `codeUnit`
(`68`, `111`, `103`)
representam os caracteres `D`, `o` e `g`,
cujos valores de unidade de código UTF-16 são os mesmos da representação UTF-8 da string
(porque esses escalares Unicode representam caracteres ASCII).

O quarto valor `codeUnit` (`8252`) é o equivalente decimal do
valor hexadecimal `203C`,
que representa o escalar Unicode `U+203C`
do caractere `DOUBLE EXCLAMATION MARK`.
Esse caractere pode ser representado como uma única unidade de código em UTF-16.

O quinto e o sexto valores `codeUnit` (`55357` e `56374`)
são uma representação em par substituto UTF-16 do caractere `DOG FACE`.
Esses valores são um valor de substituto alto de `U+D83D` (valor decimal `55357`)
e um valor de substituto baixo de `U+DC36` (valor decimal `56374`).

### Representação de escalar Unicode

Você pode acessar uma representação de escalar Unicode de um valor `String`
percorrendo sua propriedade `unicodeScalars`.
Essa propriedade é do tipo `UnicodeScalarView`,
que é uma coleção de valores do tipo `UnicodeScalar`.

Cada `UnicodeScalar` tem uma propriedade `value` que retorna
o valor de 21 bits do escalar, representado dentro de um valor `UInt32`:

![](UnicodeScalar)

```swift
for scalar in dogString.unicodeScalars {
    print("\(scalar.value) ", terminator: "")
}
print("")
// Prints "68 111 103 8252 128054 ".
```

<!--
  - test: `unicodeRepresentations`

  ```swifttest
  -> for scalar in dogString.unicodeScalars {
        print("\(scalar.value) ", terminator: "")
     }
  -> print("")
  << 68 111 103 8252 128054
  // Prints "68 111 103 8252 128054 ".
  ```
-->

<!--
  Workaround for rdar://26016325
-->

As propriedades `value` dos primeiros três valores `UnicodeScalar`
(`68`, `111`, `103`)
representam novamente os caracteres `D`, `o` e `g`.

O quarto `codeUnit` (`8252`) é novamente o equivalente decimal do
valor hexadecimal `203C`,
que representa o escalar Unicode `U+203C`
do caractere `DOUBLE EXCLAMATION MARK`.

A propriedade `value` do quinto e último `UnicodeScalar`, `128054`,
é o equivalente decimal do valor hexadecimal `1F436`,
que representa o escalar Unicode `U+1F436` do caractere `DOG FACE`.

Como alternativa a consultar suas propriedades `value`,
cada valor `UnicodeScalar` também pode ser usado para construir um novo valor `String`,
como com interpolação de string:

```swift
for scalar in dogString.unicodeScalars {
    print("\(scalar) ")
}
// D
// o
// g
// ‼
// 🐶
```

<!--
  - test: `unicodeRepresentations`

  ```swifttest
  -> for scalar in dogString.unicodeScalars {
        print("\(scalar) ")
     }
  </ D
  </ o
  </ g
  </ ‼
  </ 🐶
  ```
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
