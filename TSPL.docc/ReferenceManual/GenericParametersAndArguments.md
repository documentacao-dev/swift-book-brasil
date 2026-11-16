# Parâmetros e argumentos genéricos

Generalize declarações para abstrair tipos concretos.

Este capítulo descreve os parâmetros e os argumentos para tipos, funções e
inicializadores genéricos. Ao declarar um tipo, uma função, um subscript ou um inicializador genérico,
você especifica os parâmetros de tipo com os quais o tipo, a função ou o inicializador genérico
pode trabalhar. Esses parâmetros de tipo funcionam como marcadores de posição que
são substituídos por argumentos de tipo concretos reais quando uma instância de um tipo genérico é
criada ou quando uma função ou um inicializador genérico é chamado.

Para uma visão geral de generics em Swift, consulte <doc:Generics>.

<!--
  NOTE: Generic types are sometimes referred to as :newTerm:`parameterized types`
  because they're declared with one or more type parameters.
-->

## Cláusula de parâmetro genérico

Uma *cláusula de parâmetro genérico* especifica os parâmetros de tipo de um
tipo ou função genérica, junto com quaisquer restrições e requisitos associados a esses parâmetros.
Uma cláusula de parâmetro genérico fica entre colchetes angulares (<>)
e tem a seguinte forma:

```swift
<<#generic parameter list#>>
```

A *lista de parâmetros genéricos* é uma lista de parâmetros genéricos separados por vírgula,
cada um com a seguinte forma:

```swift
<#type parameter#>: <#constraint#>
```

Um parâmetro genérico é formado por um *parâmetro de tipo* seguido de
uma *restrição* opcional. Um *parâmetro de tipo* é simplesmente o nome
de um tipo de marcador de posição
(por exemplo, `T`, `U`, `V`, `Key`, `Value` e assim por diante).
Você tem acesso aos parâmetros de tipo (e a qualquer um dos seus tipos associados) no restante da
declaração do tipo, da função ou do inicializador, incluindo na assinatura da função
ou do inicializador.

A *restrição* especifica que um parâmetro de tipo herda
de uma classe específica ou está em conformidade com um protocolo ou uma composição de protocolos.
Por exemplo, na função genérica abaixo, o parâmetro genérico `T: Comparable`
indica que qualquer argumento de tipo substituído
pelo parâmetro de tipo `T` precisa estar em conformidade com o protocolo `Comparable`.

```swift
func simpleMax<T: Comparable>(_ x: T, _ y: T) -> T {
    if x < y {
        return y
    }
    return x
}
```

<!--
  - test: `generic-params`

  ```swifttest
  -> func simpleMax<T: Comparable>(_ x: T, _ y: T) -> T {
        if x < y {
           return y
        }
        return x
     }
  ```
-->

Como `Int` e `Double`, por exemplo, estão em conformidade com o protocolo `Comparable`,
essa função aceita argumentos de qualquer um dos dois tipos. Diferente dos tipos genéricos, você
não especifica uma cláusula de argumento genérico ao usar uma função ou um inicializador genérico.
Os argumentos de tipo são inferidos a partir do tipo dos argumentos
passados para a função ou o inicializador.

```swift
simpleMax(17, 42) // T is inferred to be Int
simpleMax(3.14159, 2.71828) // T is inferred to be Double
```

<!--
  - test: `generic-params`

  ```swifttest
  >> let r0 =
  -> simpleMax(17, 42) // T is inferred to be Int
  >> assert(r0 == 42)
  >> let r1 =
  -> simpleMax(3.14159, 2.71828) // T is inferred to be Double
  >> assert(r1 == 3.14159)
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

O último parâmetro genérico de uma lista de parâmetros genéricos
pode ser seguido por uma vírgula opcional.

### Parâmetros genéricos inteiros

Um *parâmetro genérico inteiro*
funciona como um marcador de posição para um valor inteiro, e não para um tipo.
Ele tem a seguinte forma:

```swift
let <#type parameter#>: <#type>
```

O *tipo* precisa ser o tipo `Int` da biblioteca padrão do Swift,
ou um alias de tipo ou um tipo genérico que resolva para `Int`.

O valor que você fornece para um parâmetro genérico inteiro
precisa ser um literal inteiro
ou outro parâmetro genérico inteiro do contexto genérico que o envolve.
Por exemplo:

```swift
struct SomeStruct<let x: Int> { }
let a: SomeStruct<2>  // OK: integer literal

struct AnotherStruct<let x: Int, T, each U> {
    let b: SomeStruct<x>  // OK: another integer generic parameter

    static let c = 42
    let d: SomeStruct<c>  // Error: Can't use a constant.

    let e: SomeStruct<T>  // Error: Can't use a generic type parameter.
    let f: SomeStruct<U>  // Error: Can't use a parameter pack.
}
```

O valor de um parâmetro genérico inteiro em um tipo
é acessível como uma constante estática desse tipo,
com a mesma visibilidade do próprio tipo.
O valor de um parâmetro genérico inteiro em uma função
é acessível como uma constante dentro da função.
Quando usadas em uma expressão,
essas constantes têm tipo `Int`.

```swift
print(a.x)  // Prints "4"
```

O valor de um parâmetro genérico inteiro pode ser inferido
a partir dos tipos dos argumentos que você usa
ao inicializar o tipo ou chamar a função.

```swift
struct AnotherStruct<let y: Int> {
    var s: SomeStruct<y>
}
func someFunction<let z: Int>(s: SomeStruct<z>) {
    print(z)
}

let s1 = SomeStruct<12>()
let s2 = AnotherStruct(s: s1)  // AnotherStruct.y is inferred to be 12.
someFunction(s: s1)  // Prints "12"
```

### Cláusulas where genéricas

Você pode especificar requisitos adicionais para os parâmetros de tipo e para os seus tipos associados
incluindo uma cláusula `where` genérica logo antes da chave de abertura
do corpo de um tipo ou função.
Uma cláusula `where` genérica é formada pela palavra-chave `where`,
seguida de uma lista de um ou mais *requisitos* separados por vírgula.

```swift
where <#requirements#>
```

Os *requisitos* de uma cláusula `where` genérica especificam que um parâmetro de tipo herda de
uma classe ou está em conformidade com um protocolo ou uma composição de protocolos.
Embora a cláusula `where` genérica ofereça açúcar sintático para expressar
restrições simples sobre parâmetros de tipo
(por exemplo, `<T: Comparable>` é equivalente a `<T> where T: Comparable` e assim por diante),
você pode usá-la para impor restrições mais complexas sobre parâmetros de tipo
e sobre os seus tipos associados. Por exemplo,
você pode restringir os tipos associados de parâmetros de tipo para que estejam em conformidade com protocolos.
Por exemplo, `<S: Sequence> where S.Iterator.Element: Equatable`
especifica que `S` está em conformidade com o protocolo `Sequence`
e que o tipo associado `S.Iterator.Element`
está em conformidade com o protocolo `Equatable`.
Essa restrição garante que cada elemento da sequência seja comparável com `==`.
Parâmetros genéricos inteiros não podem ter requisitos de protocolo nem de superclasse.

Você também pode especificar o requisito de que dois tipos sejam idênticos,
usando o operador `==`. Por exemplo,
`<S1: Sequence, S2: Sequence> where S1.Iterator.Element == S2.Iterator.Element`
expressa as restrições de que `S1` e `S2` estão em conformidade com o protocolo `Sequence`
e de que os elementos das duas sequências precisam ser do mesmo tipo.
Para parâmetros genéricos inteiros,
o operador `==` especifica um requisito sobre os valores deles.
Você pode exigir que dois parâmetros genéricos inteiros tenham o mesmo valor,
ou pode exigir um valor inteiro específico para o parâmetro genérico inteiro.

Qualquer argumento de tipo substituído para um parâmetro de tipo precisa
atender a todas as restrições e requisitos impostos ao parâmetro de tipo.

Uma cláusula `where` genérica pode aparecer
como parte de uma declaração que inclui parâmetros de tipo,
ou como parte de uma declaração
que está aninhada dentro de uma declaração que inclui parâmetros de tipo.
A cláusula `where` genérica de uma declaração aninhada
ainda pode se referir aos parâmetros de tipo da declaração que a envolve;
porém,
os requisitos dessa cláusula `where`
se aplicam apenas à declaração onde ela está escrita.

Se a declaração que envolve também tiver uma cláusula `where`,
os requisitos das duas cláusulas são combinados.
No exemplo abaixo, `startsWithZero()` fica disponível
apenas se `Element` estiver em conformidade com `SomeProtocol` e com `Numeric`.

```swift
extension Collection where Element: SomeProtocol {
    func startsWithZero() -> Bool where Element: Numeric {
        return first == .zero
    }
}
```

<!--
  - test: `contextual-where-clauses-combine`

  ```swifttest
  >> protocol SomeProtocol { }
  >> extension Int: SomeProtocol { }
  -> extension Collection where Element: SomeProtocol {
         func startsWithZero() -> Bool where Element: Numeric {
             return first == .zero
         }
     }
  >> print( [1, 2, 3].startsWithZero() )
  << false
  ```
-->

<!--
  - test: `contextual-where-clause-combine-err`

  ```swifttest
  >> protocol SomeProtocol { }
  >> extension Bool: SomeProtocol { }

  >> extension Collection where Element: SomeProtocol {
  >>     func returnTrue() -> Bool where Element == Bool {
  >>         return true
  >>     }
  >>     func returnTrue() -> Bool where Element == Int {
  >>         return true
  >>     }
  >> }
  !$ error: no type for 'Self.Element' can satisfy both 'Self.Element == Int' and 'Self.Element : SomeProtocol'
  !! func returnTrue() -> Bool where Element == Int {
  !!                                            ^
  ```
-->

Você pode sobrecarregar uma função ou um inicializador genérico fornecendo
restrições, requisitos ou ambos diferentes sobre os parâmetros de tipo.
Ao chamar uma função ou um inicializador genérico sobrecarregado,
o compilador usa essas restrições para decidir qual função
ou inicializador sobrecarregado invocar.

Para mais informações sobre cláusulas `where` genéricas e para ver um exemplo
de uma delas em uma declaração de função genérica,
consulte <doc:Generics#Generic-Where-Clauses>.

> Gramática de uma cláusula de parâmetro genérico:
>
> *generic-parameter-clause* → **`<`** *generic-parameter-list* **`,`**_?_ **`>`** \
> *generic-parameter-list* → *generic-parameter* | *generic-parameter* **`,`** *generic-parameter-list* \
> *generic-parameter* → *type-name* \
> *generic-parameter* → *type-name* **`:`** *type-identifier* \
> *generic-parameter* → *type-name* **`:`** *protocol-composition-type* \
> *generic-parameter* → **`let`** *type-name* **`:`** *type* \
>
> *generic-where-clause* → **`where`** *requirement-list* \
> *requirement-list* → *requirement* | *requirement* **`,`** *requirement-list* \
> *requirement* → *conformance-requirement* | *same-type-requirement*
>
> *conformance-requirement* → *type-identifier* **`:`** *type-identifier* \
> *conformance-requirement* → *type-identifier* **`:`** *protocol-composition-type* \
> *same-type-requirement* → *type-identifier* **`==`** *type* \
> *same-type-requirement* → *type-identifier* **`==`** *signed-integer-literal*

<!--
  NOTE: A conformance requirement can only have one type after the colon,
  otherwise, you'd have a syntactic ambiguity
  (a comma-separated list types inside of a comma-separated list of requirements).
-->

## Cláusula de argumento genérico

Uma *cláusula de argumento genérico* especifica os argumentos de tipo de um
tipo genérico.
Uma cláusula de argumento genérico fica entre colchetes angulares (<>)
e tem a seguinte forma:

```swift
<<#generic argument list#>>
```

A *lista de argumentos genéricos* é uma lista de argumentos de tipo separados por vírgula.
Um *argumento de tipo* é o nome de um tipo concreto real que substitui
o parâmetro de tipo correspondente na cláusula de parâmetro genérico de um tipo genérico ---
ou, no caso de um parâmetro genérico inteiro,
um valor inteiro que substitui esse parâmetro genérico inteiro.
O resultado é uma versão especializada desse tipo genérico.
O exemplo abaixo mostra uma versão simplificada do tipo de dicionário genérico
da biblioteca padrão do Swift.

```swift
struct Dictionary<Key: Hashable, Value>: Collection, ExpressibleByDictionaryLiteral {
    /* ... */
}
```

<!--
  TODO: How are we supposed to wrap code lines like the above?
-->

A versão especializada do tipo genérico `Dictionary`, `Dictionary<String, Int>`,
é formada substituindo os parâmetros genéricos `Key: Hashable` e `Value`
pelos argumentos de tipo concretos `String` e `Int`. Cada argumento de tipo precisa satisfazer
todas as restrições do parâmetro genérico que ele substitui, incluindo quaisquer
requisitos adicionais especificados em uma cláusula `where` genérica. No exemplo acima,
o parâmetro de tipo `Key` é restrito a estar em conformidade com o protocolo `Hashable`,
então `String` também precisa estar em conformidade com o protocolo `Hashable`.

Você também pode substituir um parâmetro de tipo por um argumento de tipo que seja, ele mesmo,
uma versão especializada de um tipo genérico (desde que atenda às restrições
e requisitos apropriados). Por exemplo, você pode substituir o parâmetro de tipo
`Element` em `Array<Element>` por uma versão especializada de array, `Array<Int>`,
para formar um array cujos elementos são, por sua vez, arrays de inteiros.

```swift
let arrayOfArrays: Array<Array<Int>> = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

<!--
  - test: `array-of-arrays`

  ```swifttest
  -> let arrayOfArrays: Array<Array<Int>> = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
  ```
-->

O último argumento de tipo em uma lista de argumentos genéricos
pode ser seguido por uma vírgula opcional.

Como mencionado em <doc:GenericParametersAndArguments#Generic-Parameter-Clause>,
você não usa uma cláusula de argumento genérico para especificar os argumentos de tipo
de uma função ou de um inicializador genérico.

> Gramática de uma cláusula de argumento genérico:
>
> *generic-argument-clause* → **`<`** *generic-argument-list* **`,`**_?_ **`>`** \
> *generic-argument-list* → *generic-argument* | *generic-argument* **`,`** *generic-argument-list* \
> *generic-argument* → *type* | *signed-integer-literal*

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
