# Operadores básicos

Realize operações como atribuição, aritmética e comparação.

Um *operador* é um símbolo ou uma expressão especial que você usa para
verificar, alterar ou combinar valores.
Por exemplo, o operador de adição (`+`) soma dois números,
como em `let i = 1 + 2`,
e o operador lógico E (`&&`) combina dois valores booleanos,
como em `if enteredDoorCode && passedRetinaScan`.

O Swift oferece os operadores que você talvez já conheça de linguagens como C,
e melhora diversos recursos para eliminar erros comuns de programação.
O operador de atribuição (`=`) não retorna um valor,
para evitar que ele seja usado por engano quando
o operador de igualdade (`==`) é o que se pretendia.
Os operadores aritméticos (`+`, `-`, `*`, `/`, `%` e assim por diante)
detectam e não permitem estouro de valor,
para evitar resultados inesperados ao trabalhar com números que ficam maiores ou menores
que o intervalo de valores permitido pelo tipo que os armazena.
Você pode optar pelo comportamento de estouro de valor
usando os operadores de estouro do Swift,
como descrito em <doc:AdvancedOperators#Overflow-Operators>.

O Swift também oferece operadores de intervalo que não existem em C,
como `a..<b` e `a...b`,
como um atalho para expressar um intervalo de valores.

Este capítulo descreve os operadores comuns do Swift.
<doc:AdvancedOperators> trata dos operadores avançados do Swift,
e descreve como definir seus próprios operadores personalizados
e implementar os operadores padrão para seus próprios tipos personalizados.

## Terminologia

Os operadores são unários, binários ou ternários:

- *Unários* operam sobre um único alvo (como `-a`).
  Operadores unários *prefixos* aparecem imediatamente antes do alvo (como `!b`),
  e operadores unários *postfixos* aparecem imediatamente depois do alvo (como `c!`).
- *Binários* operam sobre dois alvos (como `2 + 3`)
  e são *infixos*, porque aparecem entre os dois alvos.
- *Ternários* operam sobre três alvos.
  Como em C, o Swift tem apenas um operador ternário,
  o operador condicional ternário (`a ? b : c`).

Os valores que os operadores afetam são os *operandos*.
Na expressão `1 + 2`, o símbolo `+` é um operador infixo
e seus dois operandos são os valores `1` e `2`.

## Operador de atribuição

O *operador de atribuição* (`a = b`)
inicializa ou atualiza o valor de `a` com o valor de `b`:

```swift
let b = 10
var a = 5
a = b
// a is now equal to 10
```

<!--
  - test: `assignmentOperator`

  ```swifttest
  -> let b = 10
  -> var a = 5
  -> a = b
  /> a is now equal to \(a)
  </ a is now equal to 10
  ```
-->

Se o lado direito da atribuição for uma tupla com vários valores,
seus elementos podem ser decompostos em várias constantes ou variáveis de uma só vez:

```swift
let (x, y) = (1, 2)
// x is equal to 1, and y is equal to 2
```

<!--
  - test: `assignmentOperator`

  ```swifttest
  -> let (x, y) = (1, 2)
  /> x is equal to \(x), and y is equal to \(y)
  </ x is equal to 1, and y is equal to 2
  ```
-->

<!--
  - test: `tuple-unwrapping-with-var`

  ```swifttest
  >> var (x, y) = (1, 2)
  ```
-->

<!--
  This still allows assignment to variables,
  even though var patterns have been removed,
  because it's parsed as a variable-declaration,
  using the first alternative where (x, y) is a pattern,
  but `var` comes from the variable-declaration-head
  rather than from the pattern.
-->

Diferente do operador de atribuição em C e Objective-C,
o operador de atribuição em Swift não retorna valor algum.
A instrução a seguir não é válida:

```swift
if x = y {
    // This isn't valid, because x = y doesn't return a value.
}
```

<!--
  - test: `assignmentOperatorInvalid`

  ```swifttest
  -> if x = y {
        // This isn't valid, because x = y doesn't return a value.
     }
  !$ error: cannot find 'x' in scope
  !! if x = y {
  !!    ^
  !$ error: cannot find 'y' in scope
  !! if x = y {
  !!        ^
  ```
-->

Esse recurso impede que o operador de atribuição (`=`) seja usado por acidente
quando o operador de igualdade (`==`) é o que se pretendia.
Ao tornar `if x = y` inválido,
o Swift ajuda você a evitar esse tipo de erro no código.

<!--
  TODO: Should we mention that x = y = z is also not valid?
  If so, is there a convincing argument as to why this is a good thing?
-->

## Operadores aritméticos

O Swift oferece os quatro *operadores aritméticos* padrão para todos os tipos numéricos:

- Adição (`+`)
- Subtração (`-`)
- Multiplicação (`*`)
- Divisão (`/`)

```swift
1 + 2       // equals 3
5 - 3       // equals 2
2 * 3       // equals 6
10.0 / 2.5  // equals 4.0
```

<!--
  - test: `arithmeticOperators`

  ```swifttest
  >> let r0 =
  -> 1 + 2       // equals 3
  >> assert(r0 == 3)
  >> let r1 =
  -> 5 - 3       // equals 2
  >> assert(r1 == 2)
  >> let r2 =
  -> 2 * 3       // equals 6
  >> assert(r2 == 6)
  >> let r3 =
  -> 10.0 / 2.5  // equals 4.0
  >> assert(r3 == 4.0)
  ```
-->

Diferente dos operadores aritméticos em C e Objective-C,
os operadores aritméticos do Swift não permitem estouro de valor por padrão.
Você pode optar pelo comportamento de estouro de valor usando os operadores de estouro do Swift
(como `a &+ b`). Veja <doc:AdvancedOperators#Overflow-Operators>.

O operador de adição também funciona para concatenar `String`:

```swift
"hello, " + "world"  // equals "hello, world"
```

<!--
  - test: `arithmeticOperators`

  ```swifttest
  >> let r4 =
  -> "hello, " + "world"  // equals "hello, world"
  >> assert(r4 == "hello, world")
  ```
-->

### Operador de resto

O *operador de resto* (`a % b`)
calcula quantos múltiplos de `b` cabem dentro de `a`
e retorna o valor que sobra
(conhecido como *resto*).

> Nota: O operador de resto (`%`) também é conhecido como
> *operador de módulo* em outras linguagens.
> Porém, o comportamento dele no Swift para números negativos significa que,
> estritamente falando, ele é uma operação de resto e não de módulo.

<!--
  - test: `percentOperatorIsRemainderNotModulo`

  ```swifttest
  -> for i in -5...0 {
        print(i % 4)
     }
  << -1
  << 0
  << -3
  << -2
  << -1
  << 0
  ```
-->

Veja como o operador de resto funciona.
Para calcular `9 % 4`, primeiro você descobre quantos `4` cabem em `9`:

![](remainderInteger)

Dá para encaixar dois `4` em `9`, e o resto é `1` (mostrado em laranja).

No Swift, isso seria escrito assim:

```swift
9 % 4    // equals 1
```

<!--
  - test: `arithmeticOperators`

  ```swifttest
  >> let r5 =
  -> 9 % 4    // equals 1
  >> assert(r5 == 1)
  ```
-->

Para determinar a resposta de `a % b`,
o operador `%` calcula a equação a seguir
e retorna `remainder` como saída:

`a` = (`b` x `some multiplier`) + `remainder`

onde `some multiplier` é o maior número de múltiplos de `b`
que cabem em `a`.

Substituindo `9` e `4` nessa equação, temos:

`9` = (`4` x `2`) + `1`

O mesmo método é aplicado ao calcular o resto de um valor negativo de `a`:

```swift
-9 % 4   // equals -1
```

<!--
  - test: `arithmeticOperators`

  ```swifttest
  >> let r6 =
  -> -9 % 4   // equals -1
  >> assert(r6 == -1)
  ```
-->

Substituindo `-9` e `4` na equação, temos:

`-9` = (`4` x `-2`) + `-1`

resultando em um valor de resto `-1`.

O sinal de `b` é ignorado quando `b` é negativo.
Isso significa que `a % b` e `a % -b` sempre dão a mesma resposta.

### Operador de menos unário

O sinal de um valor numérico pode ser invertido com um `-` na frente,
conhecido como *operador de menos unário*:

```swift
let three = 3
let minusThree = -three       // minusThree equals -3
let plusThree = -minusThree   // plusThree equals 3, or "minus minus three"
```

<!--
  - test: `arithmeticOperators`

  ```swifttest
  -> let three = 3
  -> let minusThree = -three       // minusThree equals -3
  -> let plusThree = -minusThree   // plusThree equals 3, or "minus minus three"
  ```
-->

O operador de menos unário (`-`) é colocado diretamente antes do valor sobre o qual opera,
sem nenhum espaço em branco.

### Operador de mais unário

O *operador de mais unário* (`+`) simplesmente retorna
o valor sobre o qual opera, sem nenhuma alteração:

```swift
let minusSix = -6
let alsoMinusSix = +minusSix  // alsoMinusSix equals -6
```

<!--
  - test: `arithmeticOperators`

  ```swifttest
  -> let minusSix = -6
  -> let alsoMinusSix = +minusSix  // alsoMinusSix equals -6
  >> assert(alsoMinusSix == minusSix)
  ```
-->

Embora o operador de mais unário não faça nada de fato,
você pode usá-lo para manter a simetria no código para números positivos,
quando também usa o operador de menos unário para números negativos.

## Operadores de atribuição composta

Assim como em C, o Swift oferece *operadores de atribuição composta*, que combinam a atribuição (`=`) com outra operação.
Um exemplo é o *operador de atribuição por adição* (`+=`):

```swift
var a = 1
a += 2
// a is now equal to 3
```

<!--
  - test: `compoundAssignment`

  ```swifttest
  -> var a = 1
  -> a += 2
  /> a is now equal to \(a)
  </ a is now equal to 3
  ```
-->

A expressão `a += 2` é uma abreviação de `a = a + 2`.
Na prática, a adição e a atribuição são combinadas em um só operador
que executa as duas tarefas ao mesmo tempo.

> Nota: Os operadores de atribuição composta não retornam valor.
> Por exemplo, você não pode escrever `let b = a += 2`.

Para informações sobre os operadores fornecidos pela biblioteca padrão do Swift,
veja [Declarações de operadores](https://developer.apple.com/documentation/swift/operator_declarations).

## Operadores de comparação

O Swift oferece os seguintes operadores de comparação:

- Igual a (`a == b`)
- Diferente de (`a != b`)
- Maior que (`a > b`)
- Menor que (`a < b`)
- Maior ou igual a (`a >= b`)
- Menor ou igual a (`a <= b`)

> Nota: O Swift também oferece dois *operadores de identidade* (`===` e `!==`),
> que você usa para testar se duas referências a objetos apontam para a mesma instância.
> Para mais informações, veja <doc:ClassesAndStructures#Identity-Operators>.

Cada operador de comparação retorna um valor `Bool` para indicar se a afirmação é verdadeira ou não:

```swift
1 == 1   // true because 1 is equal to 1
2 != 1   // true because 2 isn't equal to 1
2 > 1    // true because 2 is greater than 1
1 < 2    // true because 1 is less than 2
1 >= 1   // true because 1 is greater than or equal to 1
2 <= 1   // false because 2 isn't less than or equal to 1
```

<!--
  - test: `comparisonOperators`

  ```swifttest
  >> assert(
  -> 1 == 1   // true because 1 is equal to 1
  >> )
  >> assert(
  -> 2 != 1   // true because 2 isn't equal to 1
  >> )
  >> assert(
  -> 2 > 1    // true because 2 is greater than 1
  >> )
  >> assert(
  -> 1 < 2    // true because 1 is less than 2
  >> )
  >> assert(
  -> 1 >= 1   // true because 1 is greater than or equal to 1
  >> )
  >> assert( !(
  -> 2 <= 1   // false because 2 isn't less than or equal to 1
  >> ) )
  ```
-->

Operadores de comparação são muito usados em instruções condicionais,
como a instrução `if`:

```swift
let name = "world"
if name == "world" {
    print("hello, world")
} else {
    print("I'm sorry \(name), but I don't recognize you")
}
// Prints "hello, world", because name is indeed equal to "world".
```

<!--
  - test: `comparisonOperators`

  ```swifttest
  -> let name = "world"
  -> if name == "world" {
        print("hello, world")
     } else {
        print("I'm sorry \(name), but I don't recognize you")
     }
  << hello, world
  // Prints "hello, world", because name is indeed equal to "world".
  ```
-->

Para saber mais sobre a instrução `if`, veja <doc:ControlFlow>.

Você pode comparar
duas tuplas se elas tiverem o mesmo tipo e o mesmo número de valores.
As tuplas são comparadas da esquerda para a direita,
um valor por vez,
até que a comparação encontre dois valores
que não são iguais.
Esses dois valores são comparados,
e o resultado dessa comparação
determina o resultado geral da comparação das tuplas.
Se todos os elementos forem iguais,
então as próprias tuplas são iguais.
Por exemplo:

```swift
(1, "zebra") < (2, "apple")   // true because 1 is less than 2; "zebra" and "apple" aren't compared
(3, "apple") < (3, "bird")    // true because 3 is equal to 3, and "apple" is less than "bird"
(4, "dog") == (4, "dog")      // true because 4 is equal to 4, and "dog" is equal to "dog"
```

<!--
  - test: `tuple-comparison-operators`

  ```swifttest
  >> let a =
  -> (1, "zebra") < (2, "apple")   // true because 1 is less than 2; "zebra" and "apple" aren't compared
  >> let b =
  -> (3, "apple") < (3, "bird")    // true because 3 is equal to 3, and "apple" is less than "bird"
  >> let c =
  -> (4, "dog") == (4, "dog")      // true because 4 is equal to 4, and "dog" is equal to "dog"
  >> print(a, b, c)
  << true true true
  ```
-->

No exemplo acima,
você pode ver o comportamento de comparação da esquerda para a direita na primeira linha.
Como `1` é menor que `2`,
`(1, "zebra")` é considerada menor que `(2, "apple")`,
independentemente dos outros valores nas tuplas.
Não importa que `"zebra"` não seja menor que `"apple"`,
porque a comparação já está decidida pelos primeiros elementos das tuplas.
Porém,
quando os primeiros elementos das tuplas são iguais,
os segundos elementos *são* comparados:
é isso que acontece na segunda e na terceira linha.

Tuplas só podem ser comparadas com um operador dado se o operador
puder ser aplicado a cada valor das respectivas tuplas. Por exemplo,
como demonstrado no código abaixo, você pode comparar
duas tuplas do tipo `(String, Int)`, porque
tanto valores `String` quanto `Int` podem ser comparados
com o operador `<`. Já
duas tuplas do tipo `(String, Bool)` não podem ser comparadas
com o operador `<`, porque esse operador não pode ser aplicado a
valores `Bool`.

```swift
("blue", -1) < ("purple", 1)        // OK: Evaluates to true.
("blue", false) < ("purple", true)  // Error: Can't use < to compare Boolean values.
```

<!--
  - test: `tuple-comparison-operators-err`

  ```swifttest
  >> _ =
  -> ("blue", -1) < ("purple", 1)        // OK: Evaluates to true.
  >> _ =
  -> ("blue", false) < ("purple", true)  // Error: Can't use < to compare Boolean values.
  !$ error: type '(String, Bool)' cannot conform to 'Comparable'
  !! ("blue", false) < ("purple", true)  // Error: Can't use < to compare Boolean values.
  !!                 ^
  !$ note: only concrete types such as structs, enums and classes can conform to protocols
  !! ("blue", false) < ("purple", true)  // Error: Can't use < to compare Boolean values.
  !!                 ^
  !$ note: required by referencing operator function '<' on 'Comparable' where 'Self' = '(String, Bool)'
  !! ("blue", false) < ("purple", true)  // Error: Can't use < to compare Boolean values.
  !!                 ^
  ```
-->

<!--
  - test: `tuple-comparison-operators-ok`

  ```swifttest
  >> let x = ("blue", -1) < ("purple", 1)        // OK, evaluates to true
  >> print(x)
  << true
  ```
-->

> Nota: A biblioteca padrão do Swift inclui operadores de comparação de tuplas
> para tuplas com menos de sete elementos.
> Para comparar tuplas com sete ou mais elementos,
> você mesmo precisa implementar os operadores de comparação.

<!--
  TODO: which types do these operate on by default?
  How do they work with strings?
  How about with your own types?
-->

## Operador condicional ternário

O *operador condicional ternário* é um operador especial com três partes,
que tem a forma `question ? answer1 : answer2`.
É um atalho para avaliar uma de duas expressões
conforme `question` seja verdadeira ou falsa.
Se `question` for verdadeira, ele avalia `answer1` e retorna o valor dela;
caso contrário, avalia `answer2` e retorna o valor dela.

O operador condicional ternário é um atalho para o código abaixo:

```swift
if question {
    answer1
} else {
    answer2
}
```

<!--
  - test: `ternaryConditionalOperatorOutline`

  ```swifttest
  >> let question = true
  >> let answer1 = true
  >> let answer2 = true
  -> if question {
        answer1
     } else {
        answer2
     }
  !! /tmp/swifttest.swift:5:4: warning: expression of type 'Bool' is unused
  !! answer1
  !! ^~~~~~~
  !! /tmp/swifttest.swift:7:4: warning: expression of type 'Bool' is unused
  !! answer2
  !! ^~~~~~
  ```
-->

<!--
  FIXME This example has too much hand waving.
  Swift doesn't have 'if' expressions.
-->

Veja um exemplo, que calcula a altura de uma linha de tabela.
A altura da linha deve ser 50 pontos maior que a altura do conteúdo
se a linha tiver um cabeçalho, e 20 pontos maior se a linha não tiver cabeçalho:

```swift
let contentHeight = 40
let hasHeader = true
let rowHeight = contentHeight + (hasHeader ? 50 : 20)
// rowHeight is equal to 90
```

<!--
  - test: `ternaryConditionalOperatorPart1`

  ```swifttest
  -> let contentHeight = 40
  -> let hasHeader = true
  -> let rowHeight = contentHeight + (hasHeader ? 50 : 20)
  /> rowHeight is equal to \(rowHeight)
  </ rowHeight is equal to 90
  ```
-->

O exemplo acima é um atalho para o código abaixo:

```swift
let contentHeight = 40
let hasHeader = true
let rowHeight: Int
if hasHeader {
    rowHeight = contentHeight + 50
} else {
    rowHeight = contentHeight + 20
}
// rowHeight is equal to 90
```

<!--
  - test: `ternaryConditionalOperatorPart2`

  ```swifttest
  -> let contentHeight = 40
  -> let hasHeader = true
  -> let rowHeight: Int
  -> if hasHeader {
        rowHeight = contentHeight + 50
     } else {
        rowHeight = contentHeight + 20
     }
  /> rowHeight is equal to \(rowHeight)
  </ rowHeight is equal to 90
  ```
-->

O uso do operador condicional ternário no primeiro exemplo significa que
`rowHeight` pode receber o valor correto em uma única linha de código,
o que é mais conciso que o código usado no segundo exemplo.

O operador condicional ternário oferece
um atalho eficiente para decidir qual de duas expressões avaliar.
Use o operador condicional ternário com cuidado, porém.
Sua concisão pode gerar código difícil de ler se for usado em excesso.
Evite combinar várias instâncias do operador condicional ternário em uma única instrução composta.

## Operador de coalescência nula

O *operador de coalescência nula* (`a ?? b`)
faz o unwrap de um optional `a` se ele contiver um valor,
ou retorna um valor padrão `b` se `a` for `nil`.
A expressão `a` é sempre de um tipo optional.
A expressão `b` deve ser do mesmo tipo armazenado dentro de `a`.

O operador de coalescência nula é um atalho para o código abaixo:

```swift
a != nil ? a! : b
```

<!--
  - test: `nilCoalescingOperatorOutline`

  ```swifttest
  >> var a: Int?
  >> let b = 42
  >> let c =
  -> a != nil ? a! : b
  >> print(c)
  << 42
  ```
-->

O código acima usa o operador condicional ternário e o force unwrapping (`a!`)
para acessar o valor encapsulado em `a` quando `a` não é `nil`,
e para retornar `b` caso contrário.
O operador de coalescência nula oferece uma maneira mais elegante de encapsular
essa verificação condicional e o unwrap, de modo conciso e legível.

> Nota: Se o valor de `a` não for `nil`,
> o valor de `b` não é avaliado.
> Isso é conhecido como *avaliação de curto-circuito*.

O exemplo a seguir usa o operador de coalescência nula para escolher entre
um nome de cor padrão e um nome de cor definido pelo usuário, que é um optional:

```swift
let defaultColorName = "red"
var userDefinedColorName: String?   // defaults to nil

var colorNameToUse = userDefinedColorName ?? defaultColorName
// userDefinedColorName is nil, so colorNameToUse is set to the default of "red"
```

<!--
  - test: `nilCoalescingOperator`

  ```swifttest
  -> let defaultColorName = "red"
  -> var userDefinedColorName: String?   // defaults to nil

  -> var colorNameToUse = userDefinedColorName ?? defaultColorName
  /> userDefinedColorName is nil, so colorNameToUse is set to the default of \"\(colorNameToUse)\"
  </ userDefinedColorName is nil, so colorNameToUse is set to the default of "red"
  ```
-->

A variável `userDefinedColorName` é definida como um `String` optional,
com valor padrão de `nil`.
Como `userDefinedColorName` é de um tipo optional,
você pode usar o operador de coalescência nula para lidar com o valor dela.
No exemplo acima, o operador é usado para determinar
um valor inicial para a variável `String` chamada `colorNameToUse`.
Como `userDefinedColorName` é `nil`,
a expressão `userDefinedColorName ?? defaultColorName` retorna
o valor de `defaultColorName`, ou seja, `"red"`.

Se você atribuir um valor diferente de `nil` a `userDefinedColorName`
e executar a verificação do operador de coalescência nula novamente,
o valor encapsulado em `userDefinedColorName` é usado no lugar do padrão:

```swift
userDefinedColorName = "green"
colorNameToUse = userDefinedColorName ?? defaultColorName
// userDefinedColorName isn't nil, so colorNameToUse is set to "green"
```

<!--
  - test: `nilCoalescingOperator`

  ```swifttest
  -> userDefinedColorName = "green"
  -> colorNameToUse = userDefinedColorName ?? defaultColorName
  /> userDefinedColorName isn't nil, so colorNameToUse is set to \"\(colorNameToUse)\"
  </ userDefinedColorName isn't nil, so colorNameToUse is set to "green"
  ```
-->

## Operadores de intervalo

O Swift inclui vários *operadores de intervalo*,
que são atalhos para expressar um intervalo de valores.

### Operador de intervalo fechado

O *operador de intervalo fechado* (`a...b`)
define um intervalo que vai de `a` até `b`,
e inclui os valores `a` e `b`.
O valor de `a` não pode ser maior que `b`.

<!--
  - test: `closedRangeStartCanBeLessThanEnd`

  ```swifttest
  -> let range = 1...2
  >> print(type(of: range))
  << ClosedRange<Int>
  ```
-->

<!--
  - test: `closedRangeStartCanBeTheSameAsEnd`

  ```swifttest
  -> let range = 1...1
  ```
-->

<!--
  - test: `closedRangeStartCannotBeGreaterThanEnd`

  ```swifttest
  -> let range = 1...0
  xx assertion
  ```
-->

O operador de intervalo fechado é útil ao iterar sobre um intervalo
em que você quer usar todos os valores,
como em um laço `for`-`in`:

```swift
for index in 1...5 {
    print("\(index) times 5 is \(index * 5)")
}
// 1 times 5 is 5
// 2 times 5 is 10
// 3 times 5 is 15
// 4 times 5 is 20
// 5 times 5 is 25
```

<!--
  - test: `rangeOperators`

  ```swifttest
  -> for index in 1...5 {
        print("\(index) times 5 is \(index * 5)")
     }
  </ 1 times 5 is 5
  </ 2 times 5 is 10
  </ 3 times 5 is 15
  </ 4 times 5 is 20
  </ 5 times 5 is 25
  ```
-->

Para saber mais sobre laços `for`-`in`, veja <doc:ControlFlow>.

### Operador de intervalo semiaberto

O *operador de intervalo semiaberto* (`a..<b`)
define um intervalo que vai de `a` até `b`,
mas não inclui `b`.
Ele é chamado de *semiaberto*
porque contém o primeiro valor, mas não o último.
Assim como no operador de intervalo fechado,
o valor de `a` não pode ser maior que `b`.
Se o valor de `a` for igual a `b`,
o intervalo resultante será vazio.

<!--
  - test: `halfOpenRangeStartCanBeLessThanEnd`

  ```swifttest
  -> let range = 1..<2
  >> print(type(of: range))
  << Range<Int>
  ```
-->

<!--
  - test: `halfOpenRangeStartCanBeTheSameAsEnd`

  ```swifttest
  -> let range = 1..<1
  ```
-->

<!--
  - test: `halfOpenRangeStartCannotBeGreaterThanEnd`

  ```swifttest
  -> let range = 1..<0
  xx assertion
  ```
-->

Intervalos semiabertos são especialmente úteis ao trabalhar com
listas indexadas a partir de zero, como arrays,
em que é útil contar até (mas sem incluir) o tamanho da lista:

```swift
let names = ["Anna", "Alex", "Brian", "Jack"]
let count = names.count
for i in 0..<count {
    print("Person \(i + 1) is called \(names[i])")
}
// Person 1 is called Anna
// Person 2 is called Alex
// Person 3 is called Brian
// Person 4 is called Jack
```

<!--
  - test: `rangeOperators`

  ```swifttest
  -> let names = ["Anna", "Alex", "Brian", "Jack"]
  -> let count = names.count
  >> assert(count == 4)
  -> for i in 0..<count {
        print("Person \(i + 1) is called \(names[i])")
     }
  </ Person 1 is called Anna
  </ Person 2 is called Alex
  </ Person 3 is called Brian
  </ Person 4 is called Jack
  ```
-->

Observe que o array tem quatro itens,
mas `0..<count` conta só até `3`
(o índice do último item do array),
porque é um intervalo semiaberto.
Para saber mais sobre arrays, veja <doc:CollectionTypes#Arrays>.

### Intervalos unilaterais

O operador de intervalo fechado
tem uma forma alternativa para intervalos que se estendem
o máximo possível em uma direção,
por exemplo,
um intervalo que inclui todos os elementos de um array
a partir do índice 2 até o fim do array.
Nesses casos, você pode omitir o valor
de um dos lados do operador de intervalo.
Esse tipo de intervalo é chamado de *intervalo unilateral*,
porque o operador tem um valor de apenas um lado.
Por exemplo:

```swift
for name in names[2...] {
    print(name)
}
// Brian
// Jack

for name in names[...2] {
    print(name)
}
// Anna
// Alex
// Brian
```

<!--
  - test: `rangeOperators`

  ```swifttest
  -> for name in names[2...] {
         print(name)
     }
  </ Brian
  </ Jack

  -> for name in names[...2] {
         print(name)
     }
  </ Anna
  </ Alex
  </ Brian
  ```
-->

O operador de intervalo semiaberto também tem
uma forma unilateral, escrita
apenas com o seu valor final.
Assim como quando você inclui um valor dos dois lados,
o valor final não faz parte do intervalo.
Por exemplo:

```swift
for name in names[..<2] {
    print(name)
}
// Anna
// Alex
```

<!--
  - test: `rangeOperators`

  ```swifttest
  -> for name in names[..<2] {
         print(name)
     }
  </ Anna
  </ Alex
  ```
-->

Intervalos unilaterais podem ser usados em outros contextos,
não apenas em subscripts.
Você não pode iterar sobre um intervalo unilateral
que omite o primeiro valor,
porque não fica claro por onde a iteração deveria começar.
Você *pode* iterar sobre um intervalo unilateral que omite o valor final;
porém, como o intervalo continua indefinidamente,
certifique-se de adicionar uma condição de parada explícita para o laço.
Você também pode verificar se um intervalo unilateral contém um valor específico,
como mostrado no código abaixo.

```swift
let range = ...5
range.contains(7)   // false
range.contains(4)   // true
range.contains(-1)  // true
```

<!--
  - test: `rangeOperators`

  ```swifttest
  -> let range = ...5
  >> print(type(of: range))
  << PartialRangeThrough<Int>
  >> let a =
  -> range.contains(7)   // false
  >> let b =
  -> range.contains(4)   // true
  >> let c =
  -> range.contains(-1)  // true
  >> print(a, b, c)
  << false true true
  ```
-->

## Operadores lógicos

*Operadores lógicos* modificam ou combinam
os valores lógicos booleanos `true` e `false`.
O Swift oferece os três operadores lógicos padrão encontrados em linguagens baseadas em C:

- NÃO lógico (`!a`)
- E lógico (`a && b`)
- OU lógico (`a || b`)

### Operador NÃO lógico

O *operador NÃO lógico* (`!a`) inverte um valor booleano, fazendo `true` virar `false`,
e `false` virar `true`.

O operador NÃO lógico é um operador prefixo,
e aparece imediatamente antes do valor sobre o qual opera,
sem nenhum espaço em branco.
Ele pode ser lido como “não `a`”, como mostrado no exemplo a seguir:

```swift
let allowedEntry = false
if !allowedEntry {
    print("ACCESS DENIED")
}
// Prints "ACCESS DENIED".
```

<!--
  - test: `logicalOperators`

  ```swifttest
  -> let allowedEntry = false
  -> if !allowedEntry {
        print("ACCESS DENIED")
     }
  <- ACCESS DENIED
  ```
-->

A expressão `if !allowedEntry` pode ser lida como “se não é permitida a entrada.”
A linha seguinte só é executada se “não é permitida a entrada” for verdadeiro;
ou seja, se `allowedEntry` for `false`.

Como neste exemplo,
a escolha cuidadosa de nomes para constantes e variáveis booleanas
pode ajudar a manter o código legível e conciso,
evitando duplas negações ou construções lógicas confusas.

### Operador E lógico

O *operador E lógico* (`a && b`) cria expressões lógicas
em que os dois valores precisam ser `true` para que a expressão geral também seja `true`.

Se qualquer um dos valores for `false`,
a expressão geral também será `false`.
Na verdade, se o *primeiro* valor for `false`,
o segundo valor nem chega a ser avaliado,
porque ele não tem como tornar a expressão geral igual a `true`.
Isso é conhecido como *avaliação de curto-circuito*.

Este exemplo usa dois valores `Bool`
e só permite o acesso se os dois valores forem `true`:

```swift
let enteredDoorCode = true
let passedRetinaScan = false
if enteredDoorCode && passedRetinaScan {
    print("Welcome!")
} else {
    print("ACCESS DENIED")
}
// Prints "ACCESS DENIED".
```

<!--
  - test: `logicalOperators`

  ```swifttest
  -> let enteredDoorCode = true
  -> let passedRetinaScan = false
  -> if enteredDoorCode && passedRetinaScan {
        print("Welcome!")
     } else {
        print("ACCESS DENIED")
     }
  <- ACCESS DENIED
  ```
-->

### Operador OU lógico

O *operador OU lógico*
(`a || b`) é um operador infixo formado por dois caracteres de barra vertical seguidos.
Você o usa para criar expressões lógicas em que
apenas *um* dos dois valores precisa ser `true`
para que a expressão geral seja `true`.

Assim como o operador E lógico acima,
o operador OU lógico usa avaliação de curto-circuito para avaliar suas expressões.
Se o lado esquerdo de uma expressão OU lógica for `true`,
o lado direito não é avaliado,
porque ele não pode mudar o resultado da expressão geral.

No exemplo a seguir,
o primeiro valor `Bool` (`hasDoorKey`) é `false`,
mas o segundo valor (`knowsOverridePassword`) é `true`.
Como um dos valores é `true`,
a expressão geral também é avaliada como `true`,
e o acesso é permitido:

```swift
let hasDoorKey = false
let knowsOverridePassword = true
if hasDoorKey || knowsOverridePassword {
    print("Welcome!")
} else {
    print("ACCESS DENIED")
}
// Prints "Welcome!"
```

<!--
  - test: `logicalOperators`

  ```swifttest
  -> let hasDoorKey = false
  -> let knowsOverridePassword = true
  -> if hasDoorKey || knowsOverridePassword {
        print("Welcome!")
     } else {
        print("ACCESS DENIED")
     }
  <- Welcome!
  ```
-->

### Combinando operadores lógicos

Você pode combinar vários operadores lógicos para criar expressões compostas mais longas:

```swift
if enteredDoorCode && passedRetinaScan || hasDoorKey || knowsOverridePassword {
    print("Welcome!")
} else {
    print("ACCESS DENIED")
}
// Prints "Welcome!"
```

<!--
  - test: `logicalOperators`

  ```swifttest
  -> if enteredDoorCode && passedRetinaScan || hasDoorKey || knowsOverridePassword {
        print("Welcome!")
     } else {
        print("ACCESS DENIED")
     }
  <- Welcome!
  ```
-->

Este exemplo usa vários operadores `&&` e `||` para criar uma expressão composta mais longa.
No entanto, os operadores `&&` e `||` continuam operando sobre apenas dois valores,
então isso é, na verdade, três expressões menores encadeadas.
O exemplo pode ser lido assim:

Se digitamos o código correto da porta e passamos pelo scanner de retina,
ou se temos uma chave válida da porta,
ou se conhecemos a senha mestra de emergência,
então permita o acesso.

Com base nos valores de `enteredDoorCode`, `passedRetinaScan` e `hasDoorKey`,
as duas primeiras subexpressões são `false`.
Porém, a senha mestra de emergência é conhecida,
então a expressão composta geral ainda é avaliada como `true`.

> Nota: Os operadores lógicos `&&` e `||` do Swift são associativos à esquerda,
> o que significa que expressões compostas com vários operadores lógicos
> avaliam primeiro a subexpressão mais à esquerda.

### Parênteses explícitos

Às vezes é útil incluir parênteses mesmo quando eles não são estritamente necessários,
para tornar a intenção de uma expressão complexa mais fácil de ler.
No exemplo de acesso à porta acima,
é útil adicionar parênteses em volta da primeira parte da expressão composta
para deixar explícita a sua intenção:

```swift
if (enteredDoorCode && passedRetinaScan) || hasDoorKey || knowsOverridePassword {
    print("Welcome!")
} else {
    print("ACCESS DENIED")
}
// Prints "Welcome!"
```

<!--
  - test: `logicalOperators`

  ```swifttest
  -> if (enteredDoorCode && passedRetinaScan) || hasDoorKey || knowsOverridePassword {
        print("Welcome!")
     } else {
        print("ACCESS DENIED")
     }
  <- Welcome!
  ```
-->

Os parênteses deixam claro que os dois primeiros valores
são considerados parte de um estado possível separado na lógica geral.
O resultado da expressão composta não muda,
mas a intenção geral fica mais clara para quem lê.
Legibilidade sempre vem antes de brevidade;
use parênteses sempre que eles ajudarem a deixar suas intenções claras.

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
