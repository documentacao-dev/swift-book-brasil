# Padrões

Corresponda e desestruture valores.

Um *padrão* representa a estrutura de um único valor
ou de um valor composto.
Por exemplo, a estrutura da tupla `(1, 2)` é uma lista de dois
elementos separados por vírgula. Como padrões representam a estrutura de um valor
e não um valor específico, você pode compará-los com vários valores.
Por exemplo, o padrão `(x, y)` corresponde à tupla `(1, 2)` e a qualquer
outra tupla de dois elementos. Além de comparar um padrão com um valor,
você pode extrair parte ou todo um valor composto e vincular cada parte
a um nome de constante ou de variável.

No Swift, há dois tipos básicos de padrões:
os que correspondem com sucesso a qualquer tipo de valor,
e os que podem não corresponder a um valor especificado em tempo de execução.

O primeiro tipo de padrão é usado para desestruturar valores em
vinculações simples de variável, de constante e de optional binding.
Eles incluem padrões curinga, padrões de identificador
e qualquer padrão de vinculação de valor ou de tupla que contenha
esses padrões. Você pode especificar uma anotação de tipo para esses padrões
para restringi-los a corresponder apenas a valores de um determinado tipo.

O segundo tipo de padrão é usado para a correspondência completa de padrões,
em que os valores com os quais você está comparando podem não estar presentes em tempo de execução.
Eles incluem padrões de caso de enumeração, padrões optional, padrões de expressão
e padrões de conversão de tipo. Você usa esses padrões em um rótulo case
de uma instrução `switch`, em uma cláusula `catch` de uma instrução `do`,
ou na condição case de uma instrução `if`, `while`,
`guard` ou `for`-`in`.

> Gramática de um padrão:
>
> *pattern* → *wildcard-pattern* *type-annotation*_?_ \
> *pattern* → *identifier-pattern* *type-annotation*_?_ \
> *pattern* → *value-binding-pattern* \
> *pattern* → *tuple-pattern* *type-annotation*_?_ \
> *pattern* → *enum-case-pattern* \
> *pattern* → *optional-pattern* \
> *pattern* → *type-casting-pattern* \
> *pattern* → *expression-pattern*

## Padrão curinga

Um *padrão curinga* corresponde a qualquer valor e o ignora, e é formado
por um sublinhado (`_`). Use um padrão curinga quando não se importa com os valores
que estão sendo comparados. Por exemplo, o código a seguir percorre o intervalo fechado `1...3`,
ignorando o valor atual do intervalo em cada iteração do laço:

```swift
for _ in 1...3 {
    // Do something three times.
}
```

<!--
  - test: `wildcard-pattern`

  ```swifttest
  -> for _ in 1...3 {
        // Do something three times.
     }
  ```
-->

> Gramática de um padrão curinga:
>
> *wildcard-pattern* → **`_`**

## Padrão de identificador

Um *padrão de identificador* corresponde a qualquer valor e vincula
o valor correspondido a um nome de variável ou de constante.
Por exemplo, na declaração de constante a seguir, `someValue` é um padrão de identificador
que corresponde ao valor `42` do tipo `Int`:

```swift
let someValue = 42
```

<!--
  - test: `identifier-pattern`

  ```swifttest
  -> let someValue = 42
  ```
-->

Quando a correspondência dá certo, o valor `42` é vinculado (atribuído)
ao nome da constante `someValue`.

Quando o padrão do lado esquerdo de uma declaração de variável ou de constante
é um padrão de identificador,
o padrão de identificador é implicitamente um subpadrão de um padrão de vinculação de valor.

> Gramática de um padrão de identificador:
>
> *identifier-pattern* → *identifier*

## Padrão de vinculação de valor

Um *padrão de vinculação de valor* vincula valores correspondidos
a nomes de variáveis ou de constantes.
Padrões de vinculação de valor que vinculam um valor correspondido
ao nome de uma constante começam com a palavra-chave `let`;
os que vinculam ao nome de uma variável começam com a palavra-chave `var`.

Padrões de identificador dentro de um padrão de vinculação de valor
vinculam novas variáveis ou constantes nomeadas aos seus valores correspondentes.
Por exemplo, você pode decompor os elementos de uma tupla
e vincular o valor de cada elemento a um padrão de identificador correspondente.

```swift
let point = (3, 2)
switch point {
// Bind x and y to the elements of point.
case let (x, y):
    print("The point is at (\(x), \(y)).")
}
// Prints "The point is at (3, 2)."
```

<!--
  - test: `value-binding-pattern`

  ```swifttest
  -> let point = (3, 2)
  -> switch point {
        // Bind x and y to the elements of point.
        case let (x, y):
           print("The point is at (\(x), \(y)).")
     }
  <- The point is at (3, 2).
  ```
-->

No exemplo acima, `let` se distribui a cada padrão de identificador
do padrão de tupla `(x, y)`. Por causa desse comportamento,
os casos `case let (x, y):` e `case (let x, let y):` do `switch`
correspondem aos mesmos valores.

> Gramática de um padrão de vinculação de valor:
>
> *value-binding-pattern* → **`var`** *pattern* | **`let`** *pattern*

<!--
  NOTE: We chose to call this "value-binding pattern"
  instead of "variable pattern",
  because it's a pattern that binds values to either variables or constants,
  not a pattern that varies.
  "Variable pattern" is ambiguous between those two meanings.
-->

## Padrão de tupla

Um *padrão de tupla* é uma lista, separada por vírgulas, de zero ou mais padrões,
delimitada por parênteses. Padrões de tupla correspondem a valores
de tipos de tupla correspondentes.

Você pode restringir um padrão de tupla para corresponder a certos tipos de tupla
usando anotações de tipo.
Por exemplo, o padrão de tupla `(x, y): (Int, Int)` na declaração de constante
`let (x, y): (Int, Int) = (1, 2)` corresponde apenas a tipos de tupla
em que os dois elementos são do tipo `Int`.

Quando um padrão de tupla é usado como padrão em uma instrução `for`-`in`
ou em uma declaração de variável ou de constante, ele só pode conter padrões curinga,
padrões de identificador, padrões optional ou outros padrões de tupla que contenham esses.
Por exemplo, o código a seguir não é válido, porque o elemento `0`
do padrão de tupla `(x, 0)` é um padrão de expressão:

```swift
let points = [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1)]
// This code isn't valid.
for (x, 0) in points {
    /* ... */
}
```

<!--
  - test: `tuple-pattern`

  ```swifttest
  -> let points = [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1)]
  -> // This code isn't valid.
  -> for (x, 0) in points {
  >>    _ = x
        /* ... */
     }
  !$ error: expected pattern
  !! for (x, 0) in points {
  !!         ^
  ```
-->

Os parênteses em volta de um padrão de tupla que contém um único elemento não têm efeito.
O padrão corresponde a valores do tipo desse único elemento. Por exemplo,
os trechos a seguir são equivalentes:

<!--
  This test needs to be compiled.
  The error message in the REPL is unpredictable as of
  Swift version 1.1 (swift-600.0.54.20)
-->

```swift
let a = 2        // a: Int = 2
let (a) = 2      // a: Int = 2
let (a): Int = 2 // a: Int = 2
```

<!--
  - test: `single-element-tuple-pattern`

  ```swifttest
  -> let a = 2        // a: Int = 2
  -> let (a) = 2      // a: Int = 2
  -> let (a): Int = 2 // a: Int = 2
  !$ error: invalid redeclaration of 'a'
  !! let (a) = 2      // a: Int = 2
  !! ^
  !$ note: 'a' previously declared here
  !! let a = 2        // a: Int = 2
  !! ^
  !$ error: invalid redeclaration of 'a'
  !! let (a): Int = 2 // a: Int = 2
  !! ^
  !$ note: 'a' previously declared here
  !! let a = 2        // a: Int = 2
  !! ^
  ```
-->

> Gramática de um padrão de tupla:
>
> *tuple-pattern* → **`(`** *tuple-pattern-element-list*_?_ **`)`** \
> *tuple-pattern-element-list* → *tuple-pattern-element* | *tuple-pattern-element* **`,`** *tuple-pattern-element-list* \
> *tuple-pattern-element* → *pattern* | *identifier* **`:`** *pattern*

## Padrão de caso de enumeração

Um *padrão de caso de enumeração* corresponde a um caso de um tipo de enumeração existente.
Padrões de caso de enumeração aparecem em rótulos case de instruções `switch`
e nas condições case das instruções `if`, `while`, `guard` e `for`-`in`.

Se o caso de enumeração que você está tentando corresponder tiver valores associados,
o padrão de caso de enumeração correspondente deve especificar um padrão de tupla
que contenha um elemento para cada valor associado. Para um exemplo que usa uma instrução
`switch` para corresponder casos de enumeração com valores associados,
veja <doc:Enumerations#Associated-Values>.

Um padrão de caso de enumeração também corresponde a valores
desse caso embrulhados em um optional.
Essa sintaxe simplificada permite omitir um padrão optional.
Observe que, como `Optional` é implementado como uma enumeração,
`.none` e `.some` podem aparecer no mesmo `switch` que os casos do tipo de enumeração.

```swift
enum SomeEnum { case left, right }
let x: SomeEnum? = .left
switch x {
case .left:
    print("Turn left")
case .right:
    print("Turn right")
case nil:
    print("Keep going straight")
}
// Prints "Turn left".
```

<!--
  - test: `enum-pattern-matching-optional`

  ```swifttest
  -> enum SomeEnum { case left, right }
  -> let x: SomeEnum? = .left
  -> switch x {
     case .left:
         print("Turn left")
     case .right:
         print("Turn right")
     case nil:
         print("Keep going straight")
     }
  <- Turn left
  ```
-->

> Gramática de um padrão de caso de enumeração:
>
> *enum-case-pattern* → *type-identifier*_?_ **`.`** *enum-case-name* *tuple-pattern*_?_

## Padrão optional

Um *padrão optional* corresponde a valores embrulhados em um caso `some(Wrapped)`
de uma enumeração `Optional<Wrapped>`.
Padrões optional são formados por um padrão de identificador seguido imediatamente
de um ponto de interrogação, e aparecem nos mesmos lugares que os padrões de caso de enumeração.

Como padrões optional são açúcar sintático para padrões de caso de enumeração de `Optional`,
os trechos a seguir são equivalentes:

```swift
let someOptional: Int? = 42
// Match using an enumeration case pattern.
if case .some(let x) = someOptional {
    print(x)
}

// Match using an optional pattern.
if case let x? = someOptional {
    print(x)
}
```

<!--
  - test: `optional-pattern`

  ```swifttest
  -> let someOptional: Int? = 42
  -> // Match using an enumeration case pattern.
  -> if case .some(let x) = someOptional {
        print(x)
     }
  << 42

  -> // Match using an optional pattern.
  -> if case let x? = someOptional {
        print(x)
     }
  << 42
  ```
-->

O padrão optional oferece uma forma prática de percorrer um array de valores optional
em uma instrução `for`-`in`, executando o corpo do laço apenas para os elementos diferentes de `nil`.

```swift
let arrayOfOptionalInts: [Int?] = [nil, 2, 3, nil, 5]
// Match only non-nil values.
for case let number? in arrayOfOptionalInts {
    print("Found a \(number)")
}
// Found a 2
// Found a 3
// Found a 5
```

<!--
  - test: `optional-pattern-for-in`

  ```swifttest
  -> let arrayOfOptionalInts: [Int?] = [nil, 2, 3, nil, 5]
  -> // Match only non-nil values.
  -> for case let number? in arrayOfOptionalInts {
        print("Found a \(number)")
     }
  </ Found a 2
  </ Found a 3
  </ Found a 5
  ```
-->

> Gramática de um padrão optional:
>
> *optional-pattern* → *identifier-pattern* **`?`**

## Padrões de conversão de tipo

Há dois padrões de conversão de tipo: o padrão `is` e o padrão `as`.
O padrão `is` aparece apenas em rótulos case de instruções `switch`.
Os padrões `is` e `as` têm a seguinte forma:

```swift
is <#type#>
<#pattern#> as <#type#>
```

O padrão `is` corresponde a um valor se o tipo desse valor em tempo de execução
for o mesmo tipo especificado do lado direito do padrão `is` --- ou uma subclasse desse tipo.
O padrão `is` se comporta como o operador `is`, pois os dois realizam uma conversão de tipo,
mas descartam o tipo retornado.

O padrão `as` corresponde a um valor se o tipo desse valor em tempo de execução
for o mesmo tipo especificado do lado direito do padrão `as` --- ou uma subclasse desse tipo.
Se a correspondência der certo, o tipo do valor correspondido é convertido
para o *padrão* especificado do lado direito do padrão `as`.

Para um exemplo que usa uma instrução `switch` para corresponder valores
com padrões `is` e `as`, veja <doc:TypeCasting#Type-Casting-for-Any-and-AnyObject>.

> Gramática de um padrão de conversão de tipo:
>
> *type-casting-pattern* → *is-pattern* | *as-pattern* \
> *is-pattern* → **`is`** *type* \
> *as-pattern* → *pattern* **`as`** *type*

## Padrão de expressão

Um *padrão de expressão* representa o valor de uma expressão.
Padrões de expressão aparecem apenas em rótulos case de instruções `switch`.

A expressão representada pelo padrão de expressão é comparada com o valor
de uma expressão de entrada usando o operador de correspondência de padrões (`~=`)
da biblioteca padrão do Swift.
A correspondência dá certo se o operador `~=` retornar `true`.
Por padrão, o operador `~=` compara dois valores do mesmo tipo usando o operador `==`.
Ele também pode corresponder um valor a um intervalo de valores,
verificando se o valor está contido no intervalo, como mostra o exemplo a seguir.

```swift
let point = (1, 2)
switch point {
case (0, 0):
    print("(0, 0) is at the origin.")
case (-2...2, -2...2):
    print("(\(point.0), \(point.1)) is near the origin.")
default:
    print("The point is at (\(point.0), \(point.1)).")
}
// Prints "(1, 2) is near the origin."
```

<!--
  - test: `expression-pattern`

  ```swifttest
  -> let point = (1, 2)
  -> switch point {
        case (0, 0):
           print("(0, 0) is at the origin.")
        case (-2...2, -2...2):
           print("(\(point.0), \(point.1)) is near the origin.")
        default:
           print("The point is at (\(point.0), \(point.1)).")
     }
  <- (1, 2) is near the origin.
  ```
-->

Você pode sobrecarregar o operador `~=` para oferecer um comportamento
de correspondência de expressões personalizado.
Por exemplo, você pode reescrever o exemplo acima para comparar a expressão `point`
com representações em string de pontos.

```swift
// Overload the ~= operator to match a string with an integer.
func ~= (pattern: String, value: Int) -> Bool {
    return pattern == "\(value)"
}
switch point {
case ("0", "0"):
    print("(0, 0) is at the origin.")
default:
    print("The point is at (\(point.0), \(point.1)).")
}
// Prints "The point is at (1, 2)."
```

<!--
  - test: `expression-pattern`

  ```swifttest
  -> // Overload the ~= operator to match a string with an integer.
  -> func ~= (pattern: String, value: Int) -> Bool {
        return pattern == "\(value)"
     }
  -> switch point {
        case ("0", "0"):
           print("(0, 0) is at the origin.")
        default:
           print("The point is at (\(point.0), \(point.1)).")
     }
  <- The point is at (1, 2).
  ```
-->

> Gramática de um padrão de expressão:
>
> *expression-pattern* → *expression*

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->

<!-- ia-translate: true -->
