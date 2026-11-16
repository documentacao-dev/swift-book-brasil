# Tipos

Use os tipos nomeados e compostos integrados da linguagem.

No Swift, existem duas categorias de tipos: tipos nomeados e tipos compostos.
Um *tipo nomeado* é um tipo que pode receber um nome específico quando é definido.
Tipos nomeados incluem classes, structs, enums e protocolos.
Por exemplo,
instâncias de uma classe definida pelo usuário chamada `MyClass` têm o tipo `MyClass`.
Além dos tipos nomeados definidos pelo usuário,
a biblioteca padrão do Swift define muitos tipos nomeados de uso comum,
incluindo os que representam arrays, dicionários e valores optional.

Tipos de dados que, em outras linguagens, costumam ser considerados básicos ou primitivos,
como os tipos que representam números, caracteres e strings,
são na verdade tipos nomeados,
definidos e implementados na biblioteca padrão do Swift usando structs.
Como são tipos nomeados,
você pode estender o comportamento deles para atender às necessidades do programa,
usando uma declaração de extension,
discutida em <doc:Extensions> e <doc:Declarations#Extension-Declaration>.

Um *tipo composto* é um tipo sem nome, definido na própria linguagem Swift.
Existem dois tipos compostos: tipos de função e tipos tupla.
Um tipo composto pode conter tipos nomeados e outros tipos compostos.
Por exemplo, o tipo tupla `(Int, (Int, Int))` tem dois elementos:
o primeiro é o tipo nomeado `Int`,
e o segundo é outro tipo composto, `(Int, Int)`.

Você pode colocar parênteses em volta de um tipo nomeado ou de um tipo composto.
No entanto, colocar parênteses em volta de um tipo não tem efeito.
Por exemplo, `(Int)` é equivalente a `Int`.

Este capítulo discute os tipos definidos na própria linguagem Swift
e descreve o comportamento de inferência de tipos do Swift.

> Gramática de um tipo:
>
> *type* → *function-type* \
> *type* → *array-type* \
> *type* → *dictionary-type* \
> *type* → *type-identifier* \
> *type* → *tuple-type* \
> *type* → *optional-type* \
> *type* → *implicitly-unwrapped-optional-type* \
> *type* → *protocol-composition-type* \
> *type* → *opaque-type* \
> *type* → *boxed-protocol-type* \
> *type* → *metatype-type* \
> *type* → *any-type* \
> *type* → *self-type* \
> *type* → **`(`** *type* **`)`**

## Anotação de tipo

Uma *anotação de tipo* especifica explicitamente o tipo de uma variável ou expressão.
Anotações de tipo começam com dois-pontos (`:`) e terminam com um tipo,
como mostram os exemplos a seguir:

```swift
let someTuple: (Double, Double) = (3.14159, 2.71828)
func someFunction(a: Int) { /* ... */ }
```

<!--
  - test: `type-annotation`

  ```swifttest
  -> let someTuple: (Double, Double) = (3.14159, 2.71828)
  -> func someFunction(a: Int) { /* ... */ }
  ```
-->

No primeiro exemplo,
a expressão `someTuple` é declarada com o tipo tupla `(Double, Double)`.
No segundo exemplo,
o parâmetro `a` da função `someFunction` é declarado com o tipo `Int`.

Anotações de tipo podem conter uma lista opcional de atributos de tipo antes do tipo.

> Gramática de uma anotação de tipo:
>
> *type-annotation* → **`:`** *attributes*_?_ *type*

## Identificador de tipo

Um *identificador de tipo* faz referência a um tipo nomeado
ou a um alias de tipo de um tipo nomeado ou composto.

Na maioria das vezes, um identificador de tipo faz referência diretamente a um tipo nomeado
com o mesmo nome do identificador.
Por exemplo, `Int` é um identificador de tipo que faz referência diretamente ao tipo nomeado `Int`,
e o identificador de tipo `Dictionary<String, Int>` faz referência diretamente
ao tipo nomeado `Dictionary<String, Int>`.

Há dois casos em que um identificador de tipo não faz referência a um tipo com o mesmo nome.
No primeiro caso, um identificador de tipo faz referência a um alias de tipo de um tipo nomeado ou composto.
Por exemplo, no exemplo abaixo,
o uso de `Point` na anotação de tipo faz referência ao tipo tupla `(Int, Int)`.

```swift
typealias Point = (Int, Int)
let origin: Point = (0, 0)
```

<!--
  - test: `type-identifier`

  ```swifttest
  -> typealias Point = (Int, Int)
  -> let origin: Point = (0, 0)
  ```
-->

No segundo caso, um identificador de tipo usa a sintaxe de ponto (`.`)
para fazer referência a tipos nomeados declarados em outros módulos
ou aninhados dentro de outros tipos.
Por exemplo, o identificador de tipo no código a seguir faz referência ao tipo nomeado `MyType`
que é declarado no módulo `ExampleModule`.

```swift
var someValue: ExampleModule.MyType
```

<!--
  - test: `type-identifier-dot`

  ```swifttest
  -> var someValue: ExampleModule.MyType
  !$ error: cannot find type 'ExampleModule' in scope
  !! var someValue: ExampleModule.MyType
  !!                ^~~~~~~~~~~~~
  ```
-->

> Gramática de um identificador de tipo:
>
> *type-identifier* → *type-name* *generic-argument-clause*_?_ | *type-name* *generic-argument-clause*_?_ **`.`** *type-identifier* \
> *type-name* → *identifier*

## Tipo tupla

Um *tipo tupla* é uma lista de tipos separados por vírgula e envolvida por parênteses.

Você pode usar um tipo tupla como tipo de retorno de uma função
para permitir que a função retorne uma única tupla contendo vários valores.
Você também pode dar nomes aos elementos de um tipo tupla e usar esses nomes para se referir
aos valores de cada elemento individual. Um nome de elemento consiste em um identificador
seguido imediatamente por dois-pontos (:). Para um exemplo que demonstra esses dois recursos,
veja <doc:Functions#Functions-with-Multiple-Return-Values>.

Quando um elemento de um tipo tupla tem nome,
esse nome faz parte do tipo.

```swift
var someTuple = (top: 10, bottom: 12)  // someTuple is of type (top: Int, bottom: Int)
someTuple = (top: 4, bottom: 42) // OK: Names match.
someTuple = (9, 99)              // OK: Names are inferred.
someTuple = (left: 5, right: 5)  // Error: Names don't match.
```

<!--
  - test: `tuple-type-names`

  ```swifttest
  -> var someTuple = (top: 10, bottom: 12)  // someTuple is of type (top: Int, bottom: Int)
  -> someTuple = (top: 4, bottom: 42) // OK: Names match.
  -> someTuple = (9, 99)              // OK: Names are inferred.
  -> someTuple = (left: 5, right: 5)  // Error: Names don't match.
  !$ error: cannot assign value of type '(left: Int, right: Int)' to type '(top: Int, bottom: Int)'
  !! someTuple = (left: 5, right: 5)  // Error: Names don't match.
  !!             ^~~~~~~~~~~~~~~~~~~
  ```
-->

Todo tipo tupla contém dois ou mais tipos,
com exceção de `Void`, que é um alias de tipo para o tipo tupla vazio, `()`.

> Gramática de um tipo tupla:
>
> *tuple-type* → **`(`** **`)`** | **`(`** *tuple-type-element* **`,`** *tuple-type-element-list* **`)`** \
> *tuple-type-element-list* → *tuple-type-element* | *tuple-type-element* **`,`** *tuple-type-element-list* \
> *tuple-type-element* → *element-name* *type-annotation* | *type* \
> *element-name* → *identifier*

## Tipo de função

Um *tipo de função* representa o tipo de uma função, de um método ou de uma closure
e é formado por um tipo de parâmetro e um tipo de retorno, separados por uma seta (`->`):

```swift
(<#parameter type#>) -> <#return type#>
```

O *tipo de parâmetro* é uma lista de tipos separados por vírgula.
Como o *tipo de retorno* pode ser um tipo tupla,
os tipos de função permitem funções e métodos
que retornam vários valores.

Um parâmetro do tipo de função `() -> T`
(em que `T` é qualquer tipo)
pode aplicar o atributo `autoclosure` para criar implicitamente uma closure
nos pontos de chamada.
Isso oferece uma forma sintaticamente conveniente de adiar a avaliação de uma expressão
sem precisar escrever uma closure explícita ao chamar a função.
Para um exemplo de parâmetro de tipo de função autoclosure,
veja <doc:Closures#Autoclosures>.

Um tipo de função pode ter parâmetros variádicos no *tipo de parâmetro* dele.
Sintaticamente,
um parâmetro variádico consiste em um nome de tipo base seguido imediatamente por três pontos (`...`),
como em `Int...`. Um parâmetro variádico é tratado como um array que contém elementos
do tipo base. Por exemplo, o parâmetro variádico `Int...` é tratado
como `[Int]`. Para um exemplo que usa um parâmetro variádico,
veja <doc:Functions#Variadic-Parameters>.

Para especificar um parâmetro in-out, coloque a palavra-chave `inout` antes do tipo do parâmetro.
Você não pode marcar um parâmetro variádico nem um tipo de retorno com a palavra-chave `inout`.
Parâmetros in-out são discutidos em <doc:Functions#In-Out-Parameters>.

Se um tipo de função tiver apenas um parâmetro
e o tipo desse parâmetro for um tipo tupla,
então o tipo tupla deve estar entre parênteses ao escrever o tipo da função.
Por exemplo,
`((Int, Int)) -> Void`
é o tipo de uma função que recebe um único parâmetro
do tipo tupla `(Int, Int)` e não retorna nenhum valor.
Já sem os parênteses,
`(Int, Int) -> Void` é o tipo
de uma função que recebe dois parâmetros `Int` e não retorna nenhum valor.
Do mesmo modo, como `Void` é um alias de tipo para `()`,
o tipo de função `(Void) -> Void`
é o mesmo que `(()) -> ()`:
uma função que recebe um único argumento que é uma tupla vazia.
Esses tipos não são iguais a `() -> ()`,
que é uma função que não recebe argumentos.

Os nomes dos argumentos em funções e métodos
não fazem parte do tipo de função correspondente.
Por exemplo:

<!--
  - test: `argument-names`

  ```swifttest
  -> func someFunction(left: Int, right: Int) {}
  -> func anotherFunction(left: Int, right: Int) {}
  -> func functionWithDifferentLabels(top: Int, bottom: Int) {}

  -> var f = someFunction // The type of f is (Int, Int) -> Void, not (left: Int, right: Int) -> Void.
  >> print(type(of: f))
  << (Int, Int) -> ()
  -> f = anotherFunction              // OK
  -> f = functionWithDifferentLabels  // OK
  ```
-->

```swift
func someFunction(left: Int, right: Int) {}
func anotherFunction(left: Int, right: Int) {}
func functionWithDifferentLabels(top: Int, bottom: Int) {}

var f = someFunction // The type of f is (Int, Int) -> Void, not (left: Int, right: Int) -> Void.
f = anotherFunction              // OK
f = functionWithDifferentLabels  // OK

func functionWithDifferentArgumentTypes(left: Int, right: String) {}
f = functionWithDifferentArgumentTypes     // Error

func functionWithDifferentNumberOfArguments(left: Int, right: Int, top: Int) {}
f = functionWithDifferentNumberOfArguments // Error
```

<!--
  - test: `argument-names-err`

  ```swifttest
  -> func someFunction(left: Int, right: Int) {}
  -> func anotherFunction(left: Int, right: Int) {}
  -> func functionWithDifferentLabels(top: Int, bottom: Int) {}

  -> var f = someFunction // The type of f is (Int, Int) -> Void, not (left: Int, right: Int) -> Void.
  -> f = anotherFunction              // OK
  -> f = functionWithDifferentLabels  // OK

  -> func functionWithDifferentArgumentTypes(left: Int, right: String) {}
  -> f = functionWithDifferentArgumentTypes     // Error
  !$ error: cannot assign value of type '(Int, String) -> ()' to type '(Int, Int) -> ()'
  !! f = functionWithDifferentArgumentTypes     // Error
  !! ^

  -> func functionWithDifferentNumberOfArguments(left: Int, right: Int, top: Int) {}
  -> f = functionWithDifferentNumberOfArguments // Error
  !$ error: type of expression is ambiguous without more context
  !! f = functionWithDifferentNumberOfArguments // Error
  !! ~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ```
-->

Como os rótulos de argumento não fazem parte do tipo de uma função,
você os omite ao escrever um tipo de função.

```swift
var operation: (lhs: Int, rhs: Int) -> Int     // Error
var operation: (_ lhs: Int, _ rhs: Int) -> Int // OK
var operation: (Int, Int) -> Int               // OK
```

<!--
  - test: `omit-argument-names-in-function-type`

  ```swifttest
  -> var operation: (lhs: Int, rhs: Int) -> Int     // Error
  !$ error: function types cannot have argument labels; use '_' before 'lhs'
  !!    var operation: (lhs: Int, rhs: Int) -> Int     // Error
  !!                    ^
  !!                    _
  !$ error: function types cannot have argument labels; use '_' before 'rhs'
  !!    var operation: (lhs: Int, rhs: Int) -> Int     // Error
  !!                              ^
  !!                              _
  !$ error: invalid redeclaration of 'operation'
  !! var operation: (_ lhs: Int, _ rhs: Int) -> Int // OK
  !!     ^
  !$ note: 'operation' previously declared here
  !! var operation: (lhs: Int, rhs: Int) -> Int     // Error
  !!     ^
  !$ error: invalid redeclaration of 'operation'
  !! var operation: (Int, Int) -> Int               // OK
  !!     ^
  !$ note: 'operation' previously declared here
  !! var operation: (lhs: Int, rhs: Int) -> Int     // Error
  !!     ^
  -> var operation: (_ lhs: Int, _ rhs: Int) -> Int // OK
  -> var operation: (Int, Int) -> Int               // OK
  ```
-->

Se um tipo de função incluir mais de uma seta (`->`),
os tipos de função são agrupados da direita para a esquerda.
Por exemplo,
o tipo de função `(Int) -> (Int) -> Int` é entendido como `(Int) -> ((Int) -> Int)`:
ou seja, uma função que recebe um `Int` e retorna outra função
que recebe e retorna um `Int`.

Tipos de função para funções
que podem lançar ou relançar um erro devem incluir a palavra-chave `throws`.
Você pode incluir um tipo depois de `throws`, entre parênteses,
para especificar o tipo de erro que a função lança.
O tipo de erro lançado deve estar em conformidade com o protocolo `Error`.
Escrever `throws` sem especificar um tipo
é o mesmo que escrever `throws(any Error)`.
Omitir `throws` é o mesmo que escrever `throws(Never)`.
O tipo de erro que uma função lança
pode ser qualquer tipo que esteja em conformidade com `Error`,
incluindo tipos genéricos, tipos de protocolo boxed e tipos opacos.

O tipo de erro que uma função lança faz parte do tipo dessa função,
e uma relação de subtipo entre tipos de erro
significa que os tipos de função correspondentes também são subtipos.
Por exemplo, se você declarar um tipo `MyError` próprio,
a relação entre alguns tipos de função é a seguinte,
do supertipo para o subtipo:

1. Funções que lançam qualquer erro, marcadas com `throws(any Error)`
1. Funções que lançam um erro específico, marcadas com `throws(MyError)`
1. Funções que não lançam, marcadas com `throws(Never)`

Como consequência dessas relações de subtipo:

- Você pode usar uma função que não lança erros
  nos mesmos lugares de uma função que lança.
- Você pode usar uma função que lança um tipo de erro concreto
  nos mesmos lugares de uma função que lança.
- Você pode usar uma função que lança um tipo de erro mais específico
  nos mesmos lugares de uma função que lança um tipo de erro mais geral.

Se você usar um tipo associado ou um parâmetro de tipo genérico
como tipo de erro lançado em um tipo de função,
então é implicitamente exigido que esse tipo associado ou parâmetro de tipo genérico
esteja em conformidade com o protocolo `Error`.

Funções que lançam erros e funções que relançam erros são descritas em
<doc:Declarations#Throwing-Functions-and-Methods>
e <doc:Declarations#Rethrowing-Functions-and-Methods>.

Tipos de função para funções assíncronas
devem ser marcados com a palavra-chave `async`.
A palavra-chave `async` faz parte do tipo de uma função,
e funções síncronas são subtipos de funções assíncronas.
Como resultado, você pode usar uma função síncrona
nos mesmos lugares de uma função assíncrona.
Para informações sobre funções assíncronas,
veja <doc:Declarations#Asynchronous-Functions-and-Methods>.

<!--
  - test: `function-arrow-is-right-associative`

  ```swifttest
  >> func f(i: Int) -> (Int) -> Int {
  >>     func g(j: Int) -> Int {
  >>         return i + j
  >>     }
  >>     return g
  >> }

  >> let a: (Int) -> (Int) -> Int = f
  >> let r0 = a(3)(5)
  >> assert(r0 == 8)

  >> let b: (Int) -> ((Int) -> Int) = f
  >> let r1 = b(3)(5)
  >> assert(r1 == 8)
  ```
-->

### Restrições para closures nonescaping

Um parâmetro que é uma função nonescaping
não pode ser armazenado em uma propriedade, variável ou constante do tipo `Any`,
porque isso poderia permitir que o valor escapasse.

<!--
  - test: `cant-store-nonescaping-as-Any`

  ```swifttest
  -> func f(g: ()->Void) { let x: Any = g }
  !$ error: converting non-escaping value to 'Any' may allow it to escape
  !! func f(g: ()->Void) { let x: Any = g }
  !!                                    ^
  ```
-->

Um parâmetro que é uma função nonescaping
não pode ser passado como argumento para outro parâmetro de função nonescaping.
Essa restrição ajuda o Swift a fazer mais verificações de acesso conflitante à memória
em tempo de compilação, em vez de em tempo de execução.
Por exemplo:

```swift
let external: (() -> Void) -> Void = { _ in () }
func takesTwoFunctions(first: (() -> Void) -> Void, second: (() -> Void) -> Void) {
    first { first {} }       // Error
    second { second {}  }    // Error

    first { second {} }      // Error
    second { first {} }      // Error

    first { external {} }    // OK
    external { first {} }    // OK
}
```

<!--
  - test: `memory-nonescaping-functions`

  ```swifttest
  -> let external: (() -> Void) -> Void = { _ in () }
  -> func takesTwoFunctions(first: (() -> Void) -> Void, second: (() -> Void) -> Void) {
         first { first {} }       // Error
         second { second {}  }    // Error

         first { second {} }      // Error
         second { first {} }      // Error

         first { external {} }    // OK
         external { first {} }    // OK
     }
  !$ error: passing a closure which captures a non-escaping function parameter 'first' to a call to a non-escaping function parameter can allow re-entrant modification of a variable
  !! first { first {} }       // Error
  !! ^
  !$ error: passing a closure which captures a non-escaping function parameter 'second' to a call to a non-escaping function parameter can allow re-entrant modification of a variable
  !! second { second {}  }    // Error
  !! ^
  !$ error: passing a closure which captures a non-escaping function parameter 'second' to a call to a non-escaping function parameter can allow re-entrant modification of a variable
  !! first { second {} }      // Error
  !! ^
  !$ error: passing a closure which captures a non-escaping function parameter 'first' to a call to a non-escaping function parameter can allow re-entrant modification of a variable
  !! second { first {} }      // Error
  !! ^
  ```
-->

No código acima,
os dois parâmetros de `takesTwoFunctions(first:second:)` são funções.
Nenhum dos dois é marcado com `@escaping`,
então ambos são nonescaping como resultado.

As quatro chamadas de função marcadas com "Error" no exemplo acima
causam erros do compilador.
Como os parâmetros `first` e `second` são funções nonescaping,
eles não podem ser passados como argumentos para outro parâmetro de função nonescaping.
Em contraste, as duas chamadas marcadas com "OK"
não causam erro do compilador.
Essas chamadas não violam a restrição
porque `external` não é um dos parâmetros de `takesTwoFunctions(first:second:)`.

Se você precisar contornar essa restrição, marque um dos parâmetros como escaping,
ou converta temporariamente um dos parâmetros de função nonescaping
em uma função escaping usando a função `withoutActuallyEscaping(_:do:)`.
Para informações sobre como evitar acesso conflitante à memória,
veja <doc:MemorySafety>.

> Gramática de um tipo de função:
>
> *function-type* → *attributes*_?_ *function-type-argument-clause* **`async`**_?_ *throws-clause*_?_ **`->`** *type*
>
> *function-type-argument-clause* → **`(`** **`)`** \
> *function-type-argument-clause* → **`(`** *function-type-argument-list* **`...`**_?_ **`)`**
>
> *function-type-argument-list* → *function-type-argument* | *function-type-argument* **`,`** *function-type-argument-list* \
> *function-type-argument* → *attributes*_?_ *parameter-modifier*_?_ *type* | *argument-label* *type-annotation* \
> *argument-label* → *identifier*
>
> *throws-clause* → **`throws`** | **`throws`** **`(`** *type* **`)`**

<!--
  NOTE: Functions are first-class citizens in Swift,
  except for generic functions, i.e., parametric polymorphic functions.
  This means that monomorphic functions can be assigned to variables
  and can be passed as arguments to other functions.
  As an example, the following three lines of code are OK::

      func polymorphicF<T>(a: Int) -> T { return a }
      func monomorphicF(a: Int) -> Int { return a }
      var myMonomorphicF = monomorphicF

  But, the following is NOT allowed::

      var myPolymorphicF = polymorphicF
-->

## Tipo array

A linguagem Swift oferece o seguinte açúcar sintático para o tipo `Array<Element>` da biblioteca padrão do Swift:

```swift
[<#type#>]
```

Em outras palavras, as duas declarações a seguir são equivalentes:

```swift
let someArray: Array<String> = ["Alex", "Brian", "Dave"]
let someArray: [String] = ["Alex", "Brian", "Dave"]
```

<!--
  - test: `array-literal`

  ```swifttest
  >> let someArray1: Array<String> = ["Alex", "Brian", "Dave"]
  >> let someArray2: [String] = ["Alex", "Brian", "Dave"]
  >> assert(someArray1 == someArray2)
  ```
-->

Nos dois casos, a constante `someArray` é declarada como um array de strings.
Os elementos de um array podem ser acessados por subscript,
especificando um índice válido entre colchetes:
`someArray[0]` se refere ao elemento no índice 0, `"Alex"`.

Você pode criar arrays multidimensionais aninhando pares de colchetes,
em que o nome do tipo base dos elementos fica dentro do par de colchetes mais interno.
Por exemplo, você pode criar um array tridimensional de inteiros
usando três pares de colchetes:

```swift
var array3D: [[[Int]]] = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
```

<!--
  - test: `array-3d`

  ```swifttest
  -> var array3D: [[[Int]]] = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
  ```
-->

Ao acessar os elementos de um array multidimensional,
o índice de subscript mais à esquerda se refere ao elemento nesse índice
do array mais externo. O índice de subscript seguinte, à direita,
se refere ao elemento nesse índice do array aninhado um nível abaixo. E assim por diante.
Isso significa que no exemplo acima, `array3D[0]` se refere a `[[1, 2], [3, 4]]`,
`array3D[0][1]` se refere a `[3, 4]`, e `array3D[0][1][1]` se refere ao valor 4.

Para uma discussão detalhada do tipo `Array` da biblioteca padrão do Swift,
veja <doc:CollectionTypes#Arrays>.

> Gramática de um tipo array:
>
> *array-type* → **`[`** *type* **`]`**

## Tipo Dictionary

A linguagem Swift oferece o seguinte açúcar sintático para o tipo `Dictionary<Key, Value>` da biblioteca padrão do Swift:

```swift
[<#key type#>: <#value type#>]
```

Em outras palavras, as duas declarações a seguir são equivalentes:

```swift
let someDictionary: [String: Int] = ["Alex": 31, "Paul": 39]
let someDictionary: Dictionary<String, Int> = ["Alex": 31, "Paul": 39]
```

<!--
  - test: `dictionary-literal`

  ```swifttest
  >> let someDictionary1: [String: Int] = ["Alex": 31, "Paul": 39]
  >> let someDictionary2: Dictionary<String, Int> = ["Alex": 31, "Paul": 39]
  >> assert(someDictionary1 == someDictionary2)
  ```
-->

Nos dois casos, a constante `someDictionary`
é declarada como um dicionário com strings como chaves e inteiros como valores.

Os valores de um dicionário podem ser acessados por subscript
especificando a chave correspondente entre
colchetes: `someDictionary["Alex"]` se refere ao valor associado
à chave `"Alex"`.
O subscript retorna um valor optional do tipo de valor do dicionário.
Se a chave especificada não estiver contida no dicionário,
o subscript retorna `nil`.

O tipo da chave de um dicionário deve estar em conformidade com o protocolo `Hashable`
da biblioteca padrão do Swift.

<!--
  Used to have an xref to :ref:`CollectionTypes_HashValuesForSetTypes` here.
  But it doesn't really work now that the Hashable content moved from Dictionary to Set.
-->

Para uma discussão detalhada do tipo `Dictionary` da biblioteca padrão do Swift,
veja <doc:CollectionTypes#Dictionaries>.

> Gramática de um tipo Dictionary:
>
> *dictionary-type* → **`[`** *type* **`:`** *type* **`]`**

## Tipo optional

A linguagem Swift define o `?` pós-fixado como açúcar sintático para
o tipo nomeado `Optional<Wrapped>`, que é definido na biblioteca padrão do Swift.
Em outras palavras, as duas declarações a seguir são equivalentes:

```swift
var optionalInteger: Int?
var optionalInteger: Optional<Int>
```

<!--
  - test: `optional-literal`

  ```swifttest
  >> var optionalInteger1: Int?
  >> var optionalInteger2: Optional<Int>
  ```
-->

<!--
  We can't test the code listing above,
  because of the redeclaration of optionalInteger,
  so we at least test that the syntax shown in it compiles.
-->

Nos dois casos, a variável `optionalInteger`
é declarada com o tipo de um inteiro optional.
Observe que não pode haver espaço em branco entre o tipo e o `?`.

O tipo `Optional<Wrapped>` é um enum com dois casos, `none` e `some(Wrapped)`,
que são usados para representar valores que podem ou não estar presentes.
Qualquer tipo pode ser declarado explicitamente como optional
(ou convertido implicitamente para um tipo optional).
Se você não fornecer um valor inicial ao declarar uma variável
ou propriedade optional, o valor dela é automaticamente `nil`.

<!--
  TODO Add a link to the Optional Enum Reference page.
  For more information about the Optional type, see ...
-->

Se uma instância de um tipo optional contiver um valor,
você pode acessar esse valor usando o operador pós-fixado `!`, como mostrado abaixo:

```swift
optionalInteger = 42
optionalInteger! // 42
```

<!--
  - test: `optional-type`

  ```swifttest
  >> var optionalInteger: Int?
  -> optionalInteger = 42
  >> let r0 =
  -> optionalInteger! // 42
  >> assert(r0 == 42)
  ```
-->

<!--
  Refactor the above if possible to avoid using bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

Usar o operador `!` para fazer force unwrapping de um optional
que tem valor `nil` resulta em um erro de tempo de execução.

Você também pode usar optional chaining e optional binding para executar,
de forma condicional, uma operação sobre uma expressão optional.
Se o valor for `nil`, nenhuma operação é executada
e, portanto, nenhum erro de tempo de execução é gerado.

Para mais informações e para ver exemplos que mostram como usar tipos optional,
veja <doc:TheBasics#Optionals>.

> Gramática de um tipo optional:
>
> *optional-type* → *type* **`?`**

## Tipo implicitly unwrapped optional

A linguagem Swift define o `!` pós-fixado como açúcar sintático para
o tipo nomeado `Optional<Wrapped>`, que é definido na biblioteca padrão do Swift,
com o comportamento adicional de ser feito unwrap automaticamente quando é acessado.
Se você tentar usar um implicitly unwrapped optional com valor `nil`,
receberá um erro de tempo de execução.
Com exceção do comportamento de unwrap implícito,
as duas declarações a seguir são equivalentes:

```swift
var implicitlyUnwrappedString: String!
var explicitlyUnwrappedString: Optional<String>
```

Observe que não pode haver espaço em branco entre o tipo e o `!`.

Como o unwrap implícito altera o significado da declaração que contém esse tipo,
tipos optional aninhados dentro de um tipo tupla ou de um tipo genérico,
como os tipos dos elementos de um dicionário ou de um array,
não podem ser marcados como implicitly unwrapped.
Por exemplo:

```swift
let tupleOfImplicitlyUnwrappedElements: (Int!, Int!)  // Error
let implicitlyUnwrappedTuple: (Int, Int)!             // OK

let arrayOfImplicitlyUnwrappedElements: [Int!]        // Error
let implicitlyUnwrappedArray: [Int]!                  // OK
```

Como implicitly unwrapped optionals
têm o mesmo tipo `Optional<Wrapped>` dos optionals comuns,
você pode usar implicitly unwrapped optionals
em todos os mesmos lugares do seu código em que pode usar optionals.
Por exemplo, você pode atribuir valores de implicitly unwrapped optionals
a variáveis, constantes e propriedades optional, e vice-versa.

Assim como com optionals, se você não fornecer um valor inicial ao declarar uma
variável ou propriedade implicitly unwrapped optional,
o valor dela é `nil` automaticamente por padrão.

Use optional chaining para executar, de forma condicional, uma operação
sobre uma expressão implicitly unwrapped optional.
Se o valor for `nil`, nenhuma operação é executada
e, portanto, nenhum erro de tempo de execução é gerado.

Para mais informações sobre tipos implicitly unwrapped optional,
veja <doc:TheBasics#Implicitly-Unwrapped-Optionals>.

> Gramática de um tipo implicitly unwrapped optional:
>
> *implicitly-unwrapped-optional-type* → *type* **`!`**

## Tipo de composição de protocolos

Um *tipo de composição de protocolos* define um tipo que está em conformidade
com cada protocolo de uma lista de protocolos especificados,
ou um tipo que é subclasse de uma classe dada
e está em conformidade com cada protocolo de uma lista de protocolos especificados.
Tipos de composição de protocolos só podem ser usados ao especificar um tipo
em anotações de tipo,
em cláusulas de parâmetros genéricos
e em cláusulas `where` genéricas.

<!--
  In places where a comma-separated list of types is allowed,
  the P&Q syntax isn't allowed.
-->

Tipos de composição de protocolos têm a seguinte forma:

```swift
<#Protocol 1#> & <#Protocol 2#>
```

Um tipo de composição de protocolos permite especificar um valor cujo tipo
está em conformidade com os requisitos de vários protocolos,
sem definir explicitamente um novo protocolo nomeado
que herde de cada protocolo com o qual você quer que o tipo esteja em conformidade.
Por exemplo,
você pode usar o tipo de composição de protocolos `ProtocolA & ProtocolB & ProtocolC`
em vez de declarar um novo protocolo
que herde de `ProtocolA`, `ProtocolB` e `ProtocolC`.
Do mesmo modo, você pode usar `SuperClass & ProtocolA`
em vez de declarar um novo protocolo
que seja subclasse de `SuperClass` e esteja em conformidade com `ProtocolA`.

Cada item de uma lista de composição de protocolos é um dos seguintes itens;
a lista pode conter no máximo uma classe:

- O nome de uma classe
- O nome de um protocolo
- Um alias de tipo cujo tipo subjacente seja um tipo de composição de protocolos,
  um protocolo ou uma classe.

Quando um tipo de composição de protocolos contém aliases de tipo,
é possível que o mesmo protocolo apareça
mais de uma vez nas definições ---
duplicatas são ignoradas.
Por exemplo,
a definição de `PQR` no código abaixo
é equivalente a `P & Q & R`.

```swift
typealias PQ = P & Q
typealias PQR = PQ & Q & R
```

<!--
  - test: `protocol-composition-can-have-repeats`

  ```swifttest
  >> protocol P {}
  >> protocol Q {}
  >> protocol R {}
  -> typealias PQ = P & Q
  -> typealias PQR = PQ & Q & R
  ```
-->

> Gramática de um tipo de composição de protocolos:
>
> *protocol-composition-type* → *type-identifier* **`&`** *protocol-composition-continuation* \
> *protocol-composition-continuation* → *type-identifier* | *protocol-composition-type*

## Tipo opaco

Um *tipo opaco* define um tipo
que está em conformidade com um protocolo ou com uma composição de protocolos,
sem especificar o tipo concreto subjacente.

Tipos opacos aparecem como tipo de retorno de uma função ou de um subscript,
como tipo de parâmetro de uma função, de um subscript ou de um inicializador,
ou como tipo de uma propriedade.
Tipos opacos não podem aparecer como parte de um tipo tupla ou de um tipo genérico,
como o tipo dos elementos de um array ou o tipo encapsulado por um optional.

Tipos opacos têm a seguinte forma:

```swift
some <#constraint#>
```

A *restrição* é um tipo de classe,
um tipo de protocolo,
um tipo de composição de protocolos ou `Any`.
Um valor só pode ser usado como instância do tipo opaco
se for uma instância de um tipo que esteja em conformidade
com o protocolo ou a composição de protocolos listados,
ou que herde da classe listada.
O código que interage com um valor opaco
só pode usar esse valor de maneiras
que façam parte da interface definida pela *restrição*.

<!--
  The wording above intentionally follows generic constraints
  because the meaning here and there is the same,
  and the compiler uses the same machinery for both under the hood.
-->

Em tempo de compilação,
um valor cujo tipo é opaco tem um tipo concreto específico,
e o Swift pode usar esse tipo subjacente para otimizações.
No entanto,
o tipo opaco forma uma fronteira
que informações sobre o tipo subjacente não podem atravessar.

Declarações de protocolo não podem incluir tipos opacos.
Classes não podem usar um tipo opaco como tipo de retorno de um método não final.

Uma função que usa um tipo opaco como tipo de retorno
deve retornar valores que compartilhem um único tipo subjacente.
O tipo de retorno pode incluir tipos
que fazem parte dos parâmetros de tipo genérico da função.
Por exemplo, uma função `someFunction<T>()`
poderia retornar um valor do tipo `T` ou `Dictionary<String, T>`.

Escrever um tipo opaco para um parâmetro
é açúcar sintático para usar um tipo genérico,
sem especificar um nome para o parâmetro de tipo genérico.
O parâmetro de tipo genérico implícito tem uma restrição
que exige que ele esteja em conformidade com o protocolo nomeado no tipo opaco.
Se você escrever vários tipos opacos,
cada um cria o próprio parâmetro de tipo genérico.
Por exemplo, as declarações a seguir são equivalentes:

```swift
func someFunction(x: some MyProtocol, y: some MyProtocol) { }
func someFunction<T1: MyProtocol, T2: MyProtocol>(x: T1, y: T2) { }
```

Na segunda declaração,
como os parâmetros de tipo genérico `T1` e `T2` têm nomes,
você pode usar esses tipos em outros pontos do código.
Em contraste,
os parâmetros de tipo genérico da primeira declaração
não têm nomes e não podem ser referenciados em outro código.

Você não pode usar um tipo opaco no tipo de um parâmetro variádico.

Você não pode usar um tipo opaco
como parâmetro de um tipo de função que está sendo retornado,
nem como parâmetro em um tipo de parâmetro que seja um tipo de função.
Nessas posições,
quem chama a função teria de construir um valor
desse tipo desconhecido.

```swift
protocol MyProtocol { }
func badFunction() -> (some MyProtocol) -> Void { }  // Error
func anotherBadFunction(callback: (some MyProtocol) -> Void) { }  // Error
```

> Gramática de um tipo opaco:
>
> *opaque-type* → **`some`** *type*

## Tipo de protocolo boxed

Um *tipo de protocolo boxed* define um tipo
que está em conformidade com um protocolo ou com uma composição de protocolos,
com a capacidade de o tipo em conformidade variar enquanto o programa está em execução.

Tipos de protocolo boxed têm a seguinte forma:

```swift
any <#constraint#>
```

A *restrição* é um tipo de protocolo,
um tipo de composição de protocolos,
um metatipo de um tipo de protocolo
ou um metatipo de um tipo de composição de protocolos.

Em tempo de execução,
uma instância de um tipo de protocolo boxed
pode conter um valor de qualquer tipo que satisfaça a *restrição*.
Esse comportamento contrasta com o funcionamento dos tipos opacos,
em que existe um tipo em conformidade específico, conhecido em tempo de compilação.
O nível adicional de indireção usado
ao trabalhar com um tipo de protocolo boxed
é chamado de *boxing*.
O boxing normalmente exige uma alocação de memória separada para o armazenamento
e um nível adicional de indireção para o acesso,
o que tem um custo de desempenho em tempo de execução.

Aplicar `any` aos tipos `Any` ou `AnyObject` não tem efeito,
porque esses tipos já são tipos de protocolo boxed.

<!--
  - test: `any-any-does-nothing`

   >> var x: any Any = 12
   >> var y: Any = 12
   >> print(type(of: x))
   << Int
   >> print(type(of: y))
   << Int
   >> print(type(of: x) == type(of: y))
   << true
-->

<!--
  - test: `any-anyobject-does-nothing`

   >> import Foundation
   >> var x: any AnyObject = NSNumber(value: 12)
   >> var y: AnyObject = NSNumber(value: 12)
   >> print(type(of: x))
   << __NSCFNumber
   >> print(type(of: y))
   << __NSCFNumber
   >> print(type(of: x) == type(of: y))
   << true
-->

<!--
Contrast P.Type with (any P.Type) and (any P).Type
https://github.com/swiftlang/swift-evolution/blob/main/proposals/0335-existential-any.md#metatypes
-->

> Gramática de um tipo de protocolo boxed:
>
> *boxed-protocol-type* → **`any`** *type*

## Tipo metatipo

Um *tipo metatipo* se refere ao tipo de qualquer tipo,
incluindo tipos de classe, tipos de struct, tipos de enum e tipos de protocolo.

O metatipo de uma classe, struct ou enum é o nome desse tipo seguido de `.Type`.
O metatipo de um tipo de protocolo (e não o tipo concreto que está em conformidade
com o protocolo em tempo de execução) é o nome desse protocolo seguido de `.Protocol`.
Por exemplo, o metatipo da classe `SomeClass` é `SomeClass.Type`,
e o metatipo do protocolo `SomeProtocol` é `SomeProtocol.Protocol`.

Você pode usar a expressão `self` pós-fixada para acessar um tipo como valor.
Por exemplo, `SomeClass.self` retorna o próprio `SomeClass`,
e não uma instância de `SomeClass`.
E `SomeProtocol.self` retorna o próprio `SomeProtocol`,
e não uma instância de um tipo que esteja em conformidade com `SomeProtocol` em tempo de execução.
Você pode chamar a função `type(of:)` com uma instância de um tipo
para acessar o tipo dinâmico, de tempo de execução, dessa instância como valor,
como mostra o exemplo a seguir:

```swift
class SomeBaseClass {
    class func printClassName() {
        print("SomeBaseClass")
    }
}
class SomeSubClass: SomeBaseClass {
    override class func printClassName() {
        print("SomeSubClass")
    }
}
let someInstance: SomeBaseClass = SomeSubClass()
// The compile-time type of someInstance is SomeBaseClass,
// and the runtime type of someInstance is SomeSubClass
type(of: someInstance).printClassName()
// Prints "SomeSubClass".
```

<!--
  - test: `metatype-type`

  ```swifttest
  -> class SomeBaseClass {
         class func printClassName() {
             print("SomeBaseClass")
         }
     }
  -> class SomeSubClass: SomeBaseClass {
         override class func printClassName() {
             print("SomeSubClass")
         }
     }
  -> let someInstance: SomeBaseClass = SomeSubClass()
  -> // The compile-time type of someInstance is SomeBaseClass,
  -> // and the runtime type of someInstance is SomeSubClass
  -> type(of: someInstance).printClassName()
  <- SomeSubClass
  ```
-->

Para mais informações,
veja [`type(of:)`](https://developer.apple.com/documentation/swift/type(of:))
na biblioteca padrão do Swift.

Use uma expressão de inicializador para construir uma instância de um tipo
a partir do valor de metatipo desse tipo.
Para instâncias de classe,
o inicializador chamado deve ser marcado com a palavra-chave `required`
ou toda a classe deve ser marcada com a palavra-chave `final`.

```swift
class AnotherSubClass: SomeBaseClass {
    let string: String
    required init(string: String) {
        self.string = string
    }
    override class func printClassName() {
        print("AnotherSubClass")
    }
}
let metatype: AnotherSubClass.Type = AnotherSubClass.self
let anotherInstance = metatype.init(string: "some string")
```

<!--
  - test: `metatype-type`

  ```swifttest
  -> class AnotherSubClass: SomeBaseClass {
        let string: String
        required init(string: String) {
           self.string = string
        }
        override class func printClassName() {
           print("AnotherSubClass")
        }
     }
  -> let metatype: AnotherSubClass.Type = AnotherSubClass.self
  -> let anotherInstance = metatype.init(string: "some string")
  ```
-->

> Gramática de um tipo metatipo:
>
> *metatype-type* → *type* **`.`** **`Type`** | *type* **`.`** **`Protocol`**

## Tipo Any

O tipo `Any` pode conter valores de todos os outros tipos.
`Any` pode ser usado como o tipo concreto
de uma instância de qualquer um dos seguintes tipos:

- Uma classe, struct ou enum
- Um metatipo, como `Int.self`
- Uma tupla com componentes de quaisquer tipos
- Uma closure ou um tipo de função

```swift
let mixed: [Any] = ["one", 2, true, (4, 5.3), { () -> Int in return 6 }]
```

<!--
  - test: `any-type`

  ```swifttest
  -> let mixed: [Any] = ["one", 2, true, (4, 5.3), { () -> Int in return 6 }]
  ```
-->

Quando você usa `Any` como tipo concreto de uma instância,
precisa converter a instância para um tipo conhecido
antes de acessar suas propriedades ou métodos.
Instâncias com tipo concreto `Any` mantêm o tipo dinâmico original
e podem ser convertidas para esse tipo usando um dos operadores de conversão de tipo ---
`as`, `as?` ou `as!`.
Por exemplo,
use `as?` para fazer um downcast condicional do primeiro objeto de um array heterogêneo
para `String`, da seguinte forma:

```swift
if let first = mixed.first as? String {
    print("The first item, '\(first)', is a string.")
}
// Prints "The first item, 'one', is a string."
```

<!--
  - test: `any-type`

  ```swifttest
  -> if let first = mixed.first as? String {
         print("The first item, '\(first)', is a string.")
     }
  <- The first item, 'one', is a string.
  ```
-->

Para mais informações sobre conversões de tipo, veja <doc:TypeCasting>.

O protocolo `AnyObject` é semelhante ao tipo `Any`.
Todas as classes estão implicitamente em conformidade com `AnyObject`.
Diferentemente de `Any`, que é definido pela linguagem,
`AnyObject` é definido pela biblioteca padrão do Swift.
Para mais informações, veja
<doc:Protocols#Class-Only-Protocols>
e [`AnyObject`](https://developer.apple.com/documentation/swift/anyobject).

> Gramática de um tipo Any:
>
> *any-type* → **`Any`**

## Tipo Self

O tipo `Self` não é um tipo específico,
mas sim um recurso que permite se referir de forma conveniente ao tipo atual
sem repetir nem precisar conhecer o nome desse tipo.

Em uma declaração de protocolo ou em uma declaração de membro de protocolo,
o tipo `Self` se refere ao tipo final que estiver em conformidade com o protocolo.

Em uma declaração de struct, classe ou enum,
o tipo `Self` se refere ao tipo introduzido pela declaração.
Dentro da declaração de um membro de um tipo,
o tipo `Self` se refere a esse tipo.
Nos membros de uma declaração de classe,
`Self` só pode aparecer nos seguintes casos:

- Como tipo de retorno de um método
- Como tipo de retorno de um subscript somente leitura
- Como tipo de uma propriedade computada somente leitura
- No corpo de um método

Por exemplo,
o código abaixo mostra um método de instância `f`
cujo tipo de retorno é `Self`.

<!--
  - test: `self-in-class-cant-be-a-parameter-type`

  ```swifttest
  -> class C { func f(c: Self) { } }
  !$ error: covariant 'Self' or 'Self?' can only appear as the type of a property, subscript or method result; did you mean 'C'?
  !! class C { func f(c: Self) { } }
  !!                     ^~~~
  !!                     C
  ```
-->

<!--
  - test: `self-in-class-can-be-a-subscript-param`

  ```swifttest
  >> class C { subscript(s: Int) -> Self { return self } }
  >> let c = C()
  >> _ = c[12]
  ```
-->

<!--
  - test: `self-in-class-can-be-a-computed-property-type`

  ```swifttest
  >> class C { var s: Self { return self } }
  >> let c = C()
  >> _ = c.s
  ```
-->

```swift
class Superclass {
    func f() -> Self { return self }
}
let x = Superclass()
print(type(of: x.f()))
// Prints "Superclass".

class Subclass: Superclass { }
let y = Subclass()
print(type(of: y.f()))
// Prints "Subclass".

let z: Superclass = Subclass()
print(type(of: z.f()))
// Prints "Subclass".
```

<!--
  - test: `self-gives-dynamic-type`

  ```swifttest
  -> class Superclass {
         func f() -> Self { return self }
     }
  -> let x = Superclass()
  -> print(type(of: x.f()))
  <- Superclass

  -> class Subclass: Superclass { }
  -> let y = Subclass()
  -> print(type(of: y.f()))
  <- Subclass

  -> let z: Superclass = Subclass()
  -> print(type(of: z.f()))
  <- Subclass
  ```
-->

A última parte do exemplo acima mostra que
`Self` se refere ao tipo de tempo de execução `Subclass` do valor de `z`,
e não ao tipo de tempo de compilação `Superclass` da própria variável.

<!--
  TODO: Using Self as the return type from a subscript or property doesn't
  currently work.  The compiler allows it, but you get the wrong type back,
  and the compiler doesn't enforce that the subscript/property must be
  read-only.  See https://bugs.swift.org/browse/SR-10326
-->

Dentro de uma declaração de tipo aninhada,
o tipo `Self` se refere ao tipo introduzido
pela declaração de tipo mais interna.

O tipo `Self` se refere ao mesmo tipo que a função
[`type(of:)`](https://developer.apple.com/documentation/swift/type(of:))
da biblioteca padrão do Swift.
Escrever `Self.someStaticMember` para acessar um membro do tipo atual
é o mesmo que escrever `type(of: self).someStaticMember`.

> Gramática de um tipo Self:
>
> *self-type* → **`Self`**

## Cláusula de herança de tipo

Uma *cláusula de herança de tipo* é usada para especificar de qual classe um tipo nomeado herda
e em conformidade com quais protocolos um tipo nomeado está.
Uma cláusula de herança de tipo começa com dois-pontos (`:`),
seguido de uma lista de identificadores de tipo.

Tipos de classe podem herdar de uma única superclasse e estar em conformidade com qualquer número de protocolos.
Ao definir uma classe,
o nome da superclasse deve aparecer primeiro na lista de identificadores de tipo,
seguido de quaisquer protocolos com os quais a classe deve estar em conformidade.
Se a classe não herdar de outra classe,
a lista pode começar com um protocolo.
Para uma discussão estendida e vários exemplos de herança de classes,
veja <doc:Inheritance>.

Outros tipos nomeados só podem herdar de uma lista de protocolos ou estar em conformidade com ela.
Tipos de protocolo podem herdar de qualquer número de outros protocolos.
Quando um tipo de protocolo herda de outros protocolos,
os requisitos desses outros protocolos são agregados,
e qualquer tipo que herde do protocolo atual deve estar em conformidade com todos esses requisitos.
Escrever um til (`~`) na frente do nome de um protocolo nessa lista
suprime a conformidade implícita com esse protocolo,
como descrito em <doc:Protocols#Implicit-Conformance-to-a-Protocol>.

Uma cláusula de herança de tipo em uma definição de enum pode ser
uma lista de protocolos
ou, no caso de um enum que atribui raw values aos seus casos,
um único tipo nomeado que especifica o tipo desses raw values.
Para um exemplo de definição de enum que usa uma cláusula de herança de tipo
para especificar o tipo dos seus raw values,
veja <doc:Enumerations#Raw-Values>.

> Gramática de uma cláusula de herança de tipo:
>
> *type-inheritance-clause* → **`:`** *type-inheritance-list* \
> *type-inheritance-list* → *attributes*_?_ **`~`**_?_ *type-identifier* | *attributes*_?_ **`~`**_?_ *type-identifier* **`,`** *type-inheritance-list*

## Inferência de tipos

O Swift usa *inferência de tipos* extensivamente,
permitindo que você omita o tipo, ou parte do tipo, de muitas variáveis e expressões do seu código.
Por exemplo,
em vez de escrever `var x: Int = 0`, você pode escrever `var x = 0`,
omitindo o tipo por completo:
o compilador infere corretamente que `x` nomeia um valor do tipo `Int`.
Do mesmo modo, você pode omitir parte de um tipo quando o tipo completo
puder ser inferido a partir do contexto.
Por exemplo, se você escrever `let dict: Dictionary = ["A": 1]`,
o compilador infere que `dict` tem o tipo `Dictionary<String, Int>`.

Nos dois exemplos acima,
a informação de tipo é passada das folhas da árvore de expressão até a raiz.
Ou seja,
o tipo de `x` em `var x: Int = 0` é inferido primeiro verificando o tipo de `0`
e depois passando essa informação de tipo para a raiz (a variável `x`).

No Swift, a informação de tipo também pode fluir no sentido contrário, da raiz para as folhas.
No exemplo a seguir, por exemplo,
a anotação de tipo explícita (`: Float`) na constante `eFloat`
faz com que o literal numérico `2.71828` tenha o tipo inferido `Float`, em vez de `Double`.

```swift
let e = 2.71828 // The type of e is inferred to be Double.
let eFloat: Float = 2.71828 // The type of eFloat is Float.
```

<!--
  - test: `type-inference`

  ```swifttest
  -> let e = 2.71828 // The type of e is inferred to be Double.
  -> let eFloat: Float = 2.71828 // The type of eFloat is Float.
  ```
-->

A inferência de tipos no Swift opera no nível de uma única expressão ou instrução.
Isso significa que todas as informações necessárias para inferir um tipo omitido,
ou parte dele, em uma expressão
precisam estar acessíveis durante a verificação de tipos da expressão
ou de uma de suas subexpressões.

<!--
  TODO: Email Doug for a list of rules or situations describing when type-inference
  is allowed and when types must be fully typed.
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
