# Expressões

Acesse, modifique e atribua valores.

Em Swift, existem quatro tipos de expressões:
expressões prefixas, expressões infixas, expressões primárias e expressões pós-fixas.
Avaliar uma expressão retorna um valor,
causa um efeito colateral, ou ambos.

Expressões prefixas e infixas permitem
aplicar operadores a expressões menores.
Expressões primárias são, conceitualmente, o tipo mais simples de expressão,
e oferecem uma forma de acessar valores.
Expressões pós-fixas,
assim como as prefixas e infixas,
permitem construir expressões mais complexas
usando pós-fixos como chamadas de função e acesso a membros.
Cada tipo de expressão é descrito em detalhes
nas seções abaixo.

> Gramática de uma expressão:
>
> *expression* → *try-operator*_?_ *await-operator*_?_ *prefix-expression* *infix-expressions*_?_

## Expressões prefixas

*Expressões prefixas* combinam
um operador prefixo opcional com uma expressão.
Operadores prefixos recebem um argumento,
que é a expressão que vem depois deles.

Para informações sobre o comportamento desses operadores,
veja <doc:BasicOperators> e <doc:AdvancedOperators>.

Para informações sobre os operadores fornecidos pela biblioteca padrão do Swift,
veja [Declarações de operadores](https://developer.apple.com/documentation/swift/operator_declarations).

> Gramática de uma expressão prefixa:
>
> *prefix-expression* → *prefix-operator*_?_ *postfix-expression* \
> *prefix-expression* → *in-out-expression*

### Expressão in-out

Uma *expressão in-out* marca uma variável
que está sendo passada
como argumento in-out para uma chamada de função.

```swift
&<#expression#>
```

Para mais informações sobre parâmetros in-out e para ver um exemplo,
veja <doc:Functions#In-Out-Parameters>.

Expressões in-out também são usadas
ao fornecer um argumento que não é ponteiro
em um contexto em que um ponteiro é necessário,
como descrito em <doc:Expressions#Implicit-Conversion-to-a-Pointer-Type>.

> Gramática de uma expressão in-out:
>
> *in-out-expression* → **`&`** *primary-expression*

### Operador try

Uma *expressão try* consiste no operador `try`
seguido de uma expressão que pode lançar um erro.
Ela tem a seguinte forma:

```swift
try <#expression#>
```

O valor de uma expressão `try` é o valor da *expressão*.

Uma *expressão try opcional* consiste no operador `try?`
seguido de uma expressão que pode lançar um erro.
Ela tem a seguinte forma:

```swift
try? <#expression#>
```

Se a *expressão* não lançar um erro,
o valor da expressão try opcional
é um optional que contém o valor da *expressão*.
Caso contrário, o valor da expressão try opcional é `nil`.

Uma *expressão try forçada* consiste no operador `try!`
seguido de uma expressão que pode lançar um erro.
Ela tem a seguinte forma:

```swift
try! <#expression#>
```

O valor de uma expressão try forçada é o valor da *expressão*.
Se a *expressão* lançar um erro,
um erro de tempo de execução é gerado.

Quando a expressão do lado esquerdo de um operador infixo
é marcada com `try`, `try?` ou `try!`,
esse operador se aplica à expressão infixa inteira.
Dito isso, você pode usar parênteses para deixar explícito o escopo de aplicação do operador.

```swift
// Writing 'try' applies to both function calls.
sum = try someThrowingFunction() + anotherThrowingFunction()

// Writing 'try' applies to both function calls.
sum = try (someThrowingFunction() + anotherThrowingFunction())

// Error: Writing 'try' applies only to the first function call.
sum = (try someThrowingFunction()) + anotherThrowingFunction()
```

<!--
  - test: `placement-of-try`

  ```swifttest
  >> func someThrowingFunction() throws -> Int { return 10 }
  >> func anotherThrowingFunction() throws -> Int { return 5 }
  >> var sum = 0
  // Writing 'try' applies to both function calls.
  -> sum = try someThrowingFunction() + anotherThrowingFunction()

  // Writing 'try' applies to both function calls.
  -> sum = try (someThrowingFunction() + anotherThrowingFunction())

  // Error: Writing 'try' applies only to the first function call.
  -> sum = (try someThrowingFunction()) + anotherThrowingFunction()
  !$ error: call can throw but is not marked with 'try'
  !! sum = (try someThrowingFunction()) + anotherThrowingFunction()
  !!                                      ^~~~~~~~~~~~~~~~~~~~~~~~~
  !$ note: did you mean to use 'try'?
  !! sum = (try someThrowingFunction()) + anotherThrowingFunction()
  !!                                      ^
  !!                                      try
  !$ note: did you mean to handle error as optional value?
  !! sum = (try someThrowingFunction()) + anotherThrowingFunction()
  !!                                      ^
  !!                                      try?
  !$ note: did you mean to disable error propagation?
  !! sum = (try someThrowingFunction()) + anotherThrowingFunction()
  !!                                      ^
  !!                                      try!
  ```
-->

Uma expressão `try` não pode aparecer do lado direito de um operador infixo,
a menos que o operador infixo seja o operador de atribuição
ou que a expressão `try` esteja entre parênteses.

<!--
  - test: `try-on-right`

  ```swifttest
  >> func someThrowingFunction() throws -> Int { return 10 }
  >> var sum = 0
  -> sum = 7 + try someThrowingFunction() // Error
  !$ error: 'try' cannot appear to the right of a non-assignment operator
  !! sum = 7 + try someThrowingFunction() // Error
  !!           ^
  -> sum = 7 + (try someThrowingFunction()) // OK
  ```
-->

Se uma expressão incluir os operadores `try` e `await`,
o operador `try` deve aparecer primeiro.

<!--
  The "try await" ordering is also part of the grammar for 'expression',
  but it's important enough to be worth re-stating in prose.
-->

Para mais informações e exemplos de como usar `try`, `try?` e `try!`,
veja <doc:ErrorHandling>.

> Gramática de uma expressão try:
>
> *try-operator* → **`try`** | **`try`** **`?`** | **`try`** **`!`**

### Operador await

Uma *expressão await* consiste no operador `await`
seguido de uma expressão que usa o resultado de uma operação assíncrona.
Ela tem a seguinte forma:

```swift
await <#expression#>
```

O valor de uma expressão `await` é o valor da *expressão*.

Uma expressão marcada com `await` é chamada de *ponto potencial de suspensão*.
A execução de uma função assíncrona pode ser suspensa
em cada expressão marcada com `await`.
Além disso,
a execução de código concorrente nunca é suspensa em nenhum outro ponto.
Isso significa que o código entre pontos potenciais de suspensão
pode atualizar, com segurança, um estado que exige quebrar temporariamente invariantes,
desde que conclua a atualização
antes do próximo ponto potencial de suspensão.

Uma expressão `await` só pode aparecer dentro de um contexto assíncrono,
como o trailing closure passado à função `async(priority:operation:)`.
Ela não pode aparecer no corpo de uma instrução `defer`
nem em um autoclosure de tipo de função síncrona.

Quando a expressão do lado esquerdo de um operador infixo
é marcada com o operador `await`,
esse operador se aplica à expressão infixa inteira.
Dito isso, você pode usar parênteses
para deixar explícito o escopo de aplicação do operador.

```swift
// Writing 'await' applies to both function calls.
sum = await someAsyncFunction() + anotherAsyncFunction()

// Writing 'await' applies to both function calls.
sum = await (someAsyncFunction() + anotherAsyncFunction())

// Error: Writing 'await' applies only to the first function call.
sum = (await someAsyncFunction()) + anotherAsyncFunction()
```

<!--
  - test: `placement-of-await`

  ```swifttest
  >> func someAsyncFunction() async -> Int { return 10 }
  >> func anotherAsyncFunction() async -> Int { return 5 }
  >> func f() async {
  >> var sum = 0
  // Writing 'await' applies to both function calls.
  -> sum = await someAsyncFunction() + anotherAsyncFunction()

  // Writing 'await' applies to both function calls.
  -> sum = await (someAsyncFunction() + anotherAsyncFunction())

  // Error: Writing 'await' applies only to the first function call.
  -> sum = (await someAsyncFunction()) + anotherAsyncFunction()
  >> _ = sum  // Suppress irrelevant written-but-not-read warning
  >> }
  !$ error: expression is 'async' but is not marked with 'await'
  !! sum = (await someAsyncFunction()) + anotherAsyncFunction()
  !! ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  !! await
  !$ note: call is 'async'
  !! sum = (await someAsyncFunction()) + anotherAsyncFunction()
  !! ^
  ```
-->

Uma expressão `await` não pode aparecer do lado direito de um operador infixo,
a menos que o operador infixo seja o operador de atribuição
ou que a expressão `await` esteja entre parênteses.

<!--
  - test: `await-on-right`

  ```swifttest
  >> func f() async {
  >> func someAsyncFunction() async -> Int { return 10 }
  >> var sum = 0
  >> sum = 7 + await someAsyncFunction()    // Error
  !$ error: 'await' cannot appear to the right of a non-assignment operator
  !! sum = 7 + await someAsyncFunction()    // Error
  !! ^
  >> sum = 7 + (await someAsyncFunction())  // OK
  >> _ = sum  // Suppress irrelevant written-but-not-read warning
  >> }
  ```
-->

Se uma expressão incluir os operadores `await` e `try`,
o operador `try` deve aparecer primeiro.

<!--
  The "try await" ordering is also part of the grammar for 'expression',
  but it's important enough to be worth re-stating in prose.
-->

> Gramática de uma expressão await:
>
> *await-operator* → **`await`**

## Expressões infixas

*Expressões infixas* combinam
um operador binário infixo com a expressão que ele recebe
como argumentos da esquerda e da direita.
Elas têm a seguinte forma:

```swift
<#left-hand argument#> <#operator#> <#right-hand argument#>
```

Para informações sobre o comportamento desses operadores,
veja <doc:BasicOperators> e <doc:AdvancedOperators>.

Para informações sobre os operadores fornecidos pela biblioteca padrão do Swift,
veja [Declarações de operadores](https://developer.apple.com/documentation/swift/operator_declarations).

<!--
  You have essentially expression sequences here, and within it are
  parts of the expressions.  We're calling them "expressions" even
  though they aren't what we ordinarily think of as expressions.  We
  have this two-phase thing where we do the expression sequence parsing
  which gives a rough parse tree.  Then after name binding we know
  operator precedence and we do a second phase of parsing that builds
  something that's a more traditional tree.
-->

> Nota: No momento da análise sintática,
> uma expressão formada por operadores infixos é representada
> como uma lista plana.
> Essa lista é transformada em uma árvore
> aplicando a precedência dos operadores.
> Por exemplo, a expressão `2 + 3 * 5`
> é inicialmente entendida como uma lista plana de cinco itens,
> `2`, `+`, `3`, `*` e `5`.
> Esse processo a transforma na árvore (2 + (3 * 5)).

> Gramática de uma expressão infixa:
>
> *infix-expression* → *infix-operator* *prefix-expression* \
> *infix-expression* → *assignment-operator* *try-operator*_?_ *await-operator*_?_ *prefix-expression* \
> *infix-expression* → *conditional-operator* *try-operator*_?_ *await-operator*_?_ *prefix-expression* \
> *infix-expression* → *type-casting-operator* \
> *infix-expressions* → *infix-expression* *infix-expressions*_?_

### Operador de atribuição

O *operador de atribuição* define um novo valor
para uma determinada expressão.
Ele tem a seguinte forma:

```swift
<#expression#> = <#value#>
```

O valor da *expressão* é definido como o valor obtido ao avaliar o *valor*.
Se a *expressão* for uma tupla,
o *valor* precisa ser uma tupla
com o mesmo número de elementos.
(Tuplas aninhadas são permitidas.)
A atribuição é feita de cada parte do *valor*
para a parte correspondente da *expressão*.
Por exemplo:

```swift
(a, _, (b, c)) = ("test", 9.45, (12, 3))
// a is "test", b is 12, c is 3, and 9.45 is ignored
```

<!--
  - test: `assignmentOperator`

  ```swifttest
  >> var (a, _, (b, c)) = ("test", 9.45, (12, 3))
  -> (a, _, (b, c)) = ("test", 9.45, (12, 3))
  /> a is \"\(a)\", b is \(b), c is \(c), and 9.45 is ignored
  </ a is "test", b is 12, c is 3, and 9.45 is ignored
  ```
-->

O operador de atribuição não retorna nenhum valor.

> Gramática de um operador de atribuição:
>
> *assignment-operator* → **`=`**

### Operador condicional ternário

O *operador condicional ternário* avalia para um de dois valores dados,
com base no valor de uma condição.
Ele tem a seguinte forma:

```swift
<#condition#> ? <#expression used if true#> : <#expression used if false#>
```

Se a *condição* for avaliada como `true`,
o operador condicional avalia a primeira expressão
e retorna o valor dela.
Caso contrário, avalia a segunda expressão e retorna o valor dela.
A expressão não utilizada não é avaliada.

Para um exemplo que usa o operador condicional ternário,
veja <doc:BasicOperators#Ternary-Conditional-Operator>.

> Gramática de um operador condicional:
>
> *conditional-operator* → **`?`** *expression* **`:`**

### Operadores de conversão de tipo

Há quatro operadores de conversão de tipo:
o operador `is`,
o operador `as`,
o operador `as?`
e o operador `as!`.

Eles têm a seguinte forma:

```swift
<#expression#> is <#type#>
<#expression#> as <#type#>
<#expression#> as? <#type#>
<#expression#> as! <#type#>
```

O operador `is` verifica em tempo de execução se a *expressão*
pode ser convertida para o *tipo* especificado.
Ele retorna `true` se a *expressão* puder ser convertida para o *tipo* especificado;
caso contrário, retorna `false`.

<!--
  - test: `triviallyTrueIsAndAs`

  ```swifttest
  -> assert("hello" is String)
  -> assert(!("hello" is Int))
  !$ warning: 'is' test is always true
  !! assert("hello" is String)
  !!                ^
  !$ warning: cast from 'String' to unrelated type 'Int' always fails
  !! assert(!("hello" is Int))
  !!          ~~~~~~~ ^  ~~~
  ```
-->

<!--
  - test: `is-operator-tautology`

  ```swifttest
  -> class Base {}
  -> class Subclass: Base {}
  -> var s = Subclass()
  -> var b = Base()

  -> assert(s is Base)
  !$ warning: 'is' test is always true
  !! assert(s is Base)
  !!          ^
  ```
-->

O operador `as` realiza uma conversão quando se sabe em tempo de compilação
que a conversão sempre dá certo,
como upcasting ou ter ponte com (bridging).
Upcasting permite usar uma expressão como uma instância do supertipo do tipo dela,
sem usar uma variável intermediária.
As abordagens a seguir são equivalentes:

```swift
func f(_ any: Any) { print("Function for Any") }
func f(_ int: Int) { print("Function for Int") }
let x = 10
f(x)
// Prints "Function for Int".

let y: Any = x
f(y)
// Prints "Function for Any".

f(x as Any)
// Prints "Function for Any".
```

<!--
  - test: `explicit-type-with-as-operator`

  ```swifttest
  -> func f(_ any: Any) { print("Function for Any") }
  -> func f(_ int: Int) { print("Function for Int") }
  -> let x = 10
  -> f(x)
  <- Function for Int

  -> let y: Any = x
  -> f(y)
  <- Function for Any

  -> f(x as Any)
  <- Function for Any
  ```
-->

Ter ponte com (bridging) permite usar uma expressão de um tipo
da biblioteca padrão do Swift, como `String`,
como o tipo correspondente do Foundation, como `NSString`,
sem precisar criar uma nova instância.
Para mais informações sobre bridging,
veja [Trabalhando com tipos do Foundation](https://developer.apple.com/documentation/swift/imported_c_and_objective_c_apis/working_with_foundation_types).

O operador `as?` realiza uma conversão condicional
da *expressão* para o *tipo* especificado.
O operador `as?` retorna um optional do *tipo* especificado.
Em tempo de execução, se a conversão tiver sucesso,
o valor da *expressão* é embrulhado em um optional e retornado;
caso contrário, o valor retornado é `nil`.
Se a conversão para o *tipo* especificado
for garantidamente falha ou garantidamente bem-sucedida,
um erro de compilação é gerado.

O operador `as!` realiza uma conversão forçada
da *expressão* para o *tipo* especificado.
O operador `as!` retorna um valor do *tipo* especificado, não um tipo optional.
Se a conversão falhar, um erro de tempo de execução é gerado.
O comportamento de `x as! T` é o mesmo de `(x as? T)!`.

Para mais informações sobre conversão de tipos
e para ver exemplos que usam os operadores de conversão,
veja <doc:TypeCasting>.

> Gramática de um operador type-casting:
>
> *type-casting-operator* → **`is`** *type* \
> *type-casting-operator* → **`as`** *type* \
> *type-casting-operator* → **`as`** **`?`** *type* \
> *type-casting-operator* → **`as`** **`!`** *type*

## Expressões primárias

*Expressões primárias* são o tipo mais básico de expressão.
Elas podem ser usadas como expressões por conta própria
e podem ser combinadas com outros tokens
para formar expressões prefixas, infixas e pós-fixas.

> Gramática de uma expressão primária:
>
> *primary-expression* → *identifier* *generic-argument-clause*_?_ \
> *primary-expression* → *literal-expression* \
> *primary-expression* → *self-expression* \
> *primary-expression* → *superclass-expression* \
> *primary-expression* → *conditional-expression* \
> *primary-expression* → *closure-expression* \
> *primary-expression* → *parenthesized-expression* \
> *primary-expression* → *tuple-expression* \
> *primary-expression* → *implicit-member-expression* \
> *primary-expression* → *wildcard-expression* \
> *primary-expression* → *macro-expansion-expression* \
> *primary-expression* → *key-path-expression* \
> *primary-expression* → *selector-expression* \
> *primary-expression* → *key-path-string-expression*

<!--
  NOTE: One reason for breaking primary expressions out of postfix
  expressions is for exposition -- it makes it easier to organize the
  prose surrounding the production rules.
-->

<!--
  TR: Is a generic argument clause allowed
  after an identifier in expression context?
  It seems like that should only occur when an identifier
  is a *type* identifier.
-->

### Expressão literal

Uma *expressão literal* consiste em um literal comum,
como uma string ou um número,
em um literal de array ou de dicionário,
ou em um literal de playground.

> Nota: Antes do Swift 5.9,
> os seguintes literais especiais eram reconhecidos:
> `#column`,
> `#dsohandle`,
> `#fileID`,
> `#filePath`,
> `#file`,
> `#function`,
> e `#line`.
> Agora eles são implementados como macros na biblioteca padrão do Swift:
> [`column()`](https://developer.apple.com/documentation/swift/column()),
> [`dsohandle()`](https://developer.apple.com/documentation/swift/dsohandle()),
> [`fileID()`](https://developer.apple.com/documentation/swift/fileID()),
> [`filePath()`](https://developer.apple.com/documentation/swift/filePath()),
> [`file()`](https://developer.apple.com/documentation/swift/file()),
> [`function()`](https://developer.apple.com/documentation/swift/function()),
> e [`line()`](https://developer.apple.com/documentation/swift/line()).

<!--
  - test: `pound-file-flavors`

  ```swifttest
  >> print(#file == #filePath)
  << true
  >> print(#file == #fileID)
  << false
  ```
-->

Um *literal de array* é uma coleção ordenada de valores.
Ele tem a seguinte forma:

```swift
[<#value 1#>, <#value 2#>, <#...#>]
```

A última expressão do array pode ser seguida de uma vírgula opcional.
O valor de um literal de array tem o tipo `[T]`,
em que `T` é o tipo das expressões dentro dele.
Se houver expressões de vários tipos,
`T` é o supertipo comum mais próximo delas.
Literais de array vazios são escritos com um par de colchetes vazio
e podem ser usados para criar um array vazio de um tipo especificado.

```swift
var emptyArray: [Double] = []
```

<!--
  - test: `array-literal-brackets`

  ```swifttest
  -> var emptyArray: [Double] = []
  ```
-->

Um *literal de dicionário* é uma coleção não ordenada de pares chave-valor.
Ele tem a seguinte forma:

```swift
[<#key 1#>: <#value 1#>, <#key 2#>: <#value 2#>, <#...#>]
```

A última expressão do dicionário pode ser seguida de uma vírgula opcional.
O valor de um literal de dicionário tem o tipo `[Key: Value]`,
em que `Key` é o tipo das suas expressões de chave
e `Value` é o tipo das suas expressões de valor.
Se houver expressões de vários tipos,
`Key` e `Value` são o supertipo comum mais próximo de seus respectivos valores.
Um literal de dicionário vazio é escrito como dois-pontos dentro de um par de colchetes (`[:]`),
para diferenciá-lo de um literal de array vazio.
Você pode usar um literal de dicionário vazio para criar um dicionário vazio
dos tipos de chave e de valor especificados.

```swift
var emptyDictionary: [String: Double] = [:]
```

<!--
  - test: `dictionary-literal-brackets`

  ```swifttest
  -> var emptyDictionary: [String: Double] = [:]
  ```
-->

Um *literal de playground* é usado pelo Xcode
para criar uma representação interativa de uma cor, de um arquivo ou de uma imagem
dentro do editor do programa.
Literais de playground em texto puro, fora do Xcode,
são representados por uma sintaxe especial de literal.

Para informações sobre como usar literais de playground no Xcode,
veja [Adicionar um literal de cor, arquivo ou imagem](https://help.apple.com/xcode/mac/current/#/dev4c60242fc)
na Ajuda do Xcode.

> Gramática de uma expressão literal:
>
> *literal-expression* → *literal* \
> *literal-expression* → *array-literal* | *dictionary-literal* | *playground-literal*
>
> *array-literal* → **`[`** *array-literal-items*_?_ **`,`**_?_ **`]`** \
> *array-literal-items* → *array-literal-item* | *array-literal-item* **`,`** *array-literal-items* \
> *array-literal-item* → *expression*
>
> *dictionary-literal* → **`[`** *dictionary-literal-items* **`,`**_?_ **`]`** | **`[`** **`:`** **`]`** \
> *dictionary-literal-items* → *dictionary-literal-item* | *dictionary-literal-item* **`,`** *dictionary-literal-items* \
> *dictionary-literal-item* → *expression* **`:`** *expression*
>
> *playground-literal* → **`#colorLiteral`** **`(`** **`red`** **`:`** *expression* **`,`** **`green`** **`:`** *expression* **`,`** **`blue`** **`:`** *expression* **`,`** **`alpha`** **`:`** *expression* **`)`** \
> *playground-literal* → **`#fileLiteral`** **`(`** **`resourceName`** **`:`** *expression* **`)`** \
> *playground-literal* → **`#imageLiteral`** **`(`** **`resourceName`** **`:`** *expression* **`)`**

### Expressão self

A expressão `self` é uma referência explícita ao tipo atual
ou à instância do tipo em que ela aparece.
Ela tem as seguintes formas:

```swift
self
self.<#member name#>
self[<#subscript index#>]
self(<#initializer arguments#>)
self.init(<#initializer arguments#>)
```

<!--
  TODO: Come back and explain the second to last form (i.e., self(arg: value)).
-->

Em um inicializador, em um subscript ou em um método de instância,
`self` se refere à instância atual do tipo em que ocorre.
Em um método de tipo,
`self` se refere ao tipo atual em que ocorre.

A expressão `self` é usada para especificar o escopo ao acessar membros,
fornecendo desambiguação quando há outra variável com o mesmo nome no escopo,
como um parâmetro de função.
Por exemplo:

```swift
class SomeClass {
    var greeting: String
    init(greeting: String) {
        self.greeting = greeting
    }
}
```

<!--
  - test: `self-expression`

  ```swifttest
  -> class SomeClass {
         var greeting: String
         init(greeting: String) {
             self.greeting = greeting
         }
     }
  ```
-->

Em um método mutante de um tipo de valor,
você pode atribuir uma nova instância desse tipo de valor a `self`.
Por exemplo:

```swift
struct Point {
    var x = 0.0, y = 0.0
    mutating func moveBy(x deltaX: Double, y deltaY: Double) {
        self = Point(x: x + deltaX, y: y + deltaY)
    }
}
```

<!--
  - test: `self-expression`

  ```swifttest
  -> struct Point {
        var x = 0.0, y = 0.0
        mutating func moveBy(x deltaX: Double, y deltaY: Double) {
           self = Point(x: x + deltaX, y: y + deltaY)
        }
     }
  >> var somePoint = Point(x: 1.0, y: 1.0)
  >> somePoint.moveBy(x: 2.0, y: 3.0)
  >> print("The point is now at (\(somePoint.x), \(somePoint.y))")
  << The point is now at (3.0, 4.0)
  ```
-->

<!-- Apple Books screenshot begins here. -->

> Gramática de uma expressão self:
>
> *self-expression* → **`self`** | *self-method-expression* | *self-subscript-expression* | *self-initializer-expression*
>
> *self-method-expression* → **`self`** **`.`** *identifier* \
> *self-subscript-expression* → **`self`** **`[`** *function-call-argument-list* **`]`** \
> *self-initializer-expression* → **`self`** **`.`** **`init`**

### Expressão superclass

Uma *expressão superclass* permite que uma classe interaja com a sua superclasse.
Ela tem uma das seguintes formas:

```swift
super.<#member name#>
super[<#subscript index#>]
super.init(<#initializer arguments#>)
```

A primeira forma é usada para acessar um membro da superclasse.
A segunda forma é usada para acessar a implementação de subscript da superclasse.
A terceira forma é usada para acessar um inicializador da superclasse.

Subclasses podem usar uma expressão superclass
na implementação de membros, subscripts e inicializadores
para aproveitar a implementação da superclasse.

> Gramática de uma expressão superclass:
>
> *superclass-expression* → *superclass-method-expression* | *superclass-subscript-expression* | *superclass-initializer-expression*
>
> *superclass-method-expression* → **`super`** **`.`** *identifier* \
> *superclass-subscript-expression* → **`super`** **`[`** *function-call-argument-list* **`]`** \
> *superclass-initializer-expression* → **`super`** **`.`** **`init`**

### Expressão condicional

Uma *expressão condicional* avalia para um de vários valores dados,
com base no valor de uma condição.
Ela tem uma das seguintes formas:

```swift
if <#condition 1#> {
   <#expression used if condition 1 is true#>
} else if <#condition 2#> {
   <#expression used if condition 2 is true#>
} else {
   <#expression used if both conditions are false#>
}

switch <#expression#> {
case <#pattern 1#>:
    <#expression 1#>
case <#pattern 2#> where <#condition#>:
    <#expression 2#>
default:
    <#expression 3#>
}
```

Uma expressão condicional tem o mesmo comportamento e a mesma sintaxe
de uma instrução `if` ou de uma instrução `switch`,
exceto pelas diferenças descritas nos parágrafos abaixo.

Uma expressão condicional aparece apenas nos seguintes contextos:

  - Como o valor atribuído a uma variável.
  - Como o valor inicial em uma declaração de variável ou constante.
  - Como o erro lançado por uma expressão `throw`.
  - Como o valor retornado por uma função, closure ou getter de propriedade.
  - Como o valor dentro de um ramo de uma expressão condicional.

Os ramos de uma expressão condicional são exaustivos,
o que garante que a expressão sempre produz um valor,
independentemente da condição.
Isso significa que cada ramo `if` precisa de um ramo `else` correspondente.

Cada ramo contém uma única expressão,
que é usada como valor da expressão condicional
quando a condição desse ramo é verdadeira,
uma instrução `throw`
ou uma chamada a uma função que nunca retorna.

Cada ramo deve produzir um valor do mesmo tipo.
Como a verificação de tipo de cada ramo é independente,
às vezes é preciso especificar o tipo do valor explicitamente,
como quando os ramos incluem literais de tipos diferentes
ou quando o valor de um ramo é `nil`.
Quando for preciso fornecer essa informação,
adicione uma anotação de tipo à variável que recebe o resultado
ou adicione uma conversão `as` aos valores dos ramos.

```swift
let number: Double = if someCondition { 10 } else { 12.34 }
let number = if someCondition { 10 as Double } else { 12.34 }
```

Dentro de um result builder,
expressões condicionais só podem aparecer
como valor inicial de uma variável ou constante.
Esse comportamento significa que, quando você escreve `if` ou `switch` em um result builder,
fora de uma declaração de variável ou constante,
esse código é entendido como uma instrução de ramificação,
e um dos métodos do result builder transforma esse código.

Não coloque uma expressão condicional dentro de uma expressão `try`,
mesmo que um dos ramos da expressão condicional seja um ramo que lança erro.

> Gramática de uma expressão condicional:
>
> *conditional-expression* → *if-expression* | *switch-expression*
>
> *if-expression* → **`if`** *condition-list* **`{`** *statement* **`}`** *if-expression-tail* \
> *if-expression-tail* → **`else`** *if-expression* \
> *if-expression-tail* → **`else`** **`{`** *statement* **`}`**
>
> *switch-expression* → **`switch`** *expression* **`{`** *switch-expression-cases* **`}`** \
> *switch-expression-cases* → *switch-expression-case* *switch-expression-cases*_?_ \
> *switch-expression-case* → *case-label* *statement* \
> *switch-expression-case* → *default-label* *statement*

### Expressão de closure

Uma *expressão de closure* cria um closure,
também conhecido como *lambda* ou *função anônima* em outras linguagens de programação.
Assim como uma declaração de função, um closure contém instruções
e captura constantes e variáveis do escopo em que está inserido.
Ele tem a seguinte forma:

```swift
{ (<#parameters#>) -> <#return type#> in
   <#statements#>
}
```

Os *parâmetros* têm a mesma forma que os parâmetros em uma declaração de função,
como descrito em <doc:Declarations#Function-Declaration>.

Escrever `throws` ou `async` em uma expressão de closure
marca explicitamente o closure como capaz de lançar erros ou como assíncrono.

```swift
{ (<#parameters#>) async throws -> <#return type#> in
   <#statements#>
}
```

Se o corpo de um closure incluir uma instrução `throw` ou uma expressão `try`
que não esteja aninhada dentro de uma instrução `do` com tratamento de erros exaustivo,
o closure é entendido como lançador de erros.
Se um closure lançador lançar erros de um único tipo,
ele é entendido como lançador desse tipo de erro;
caso contrário, é entendido como lançador de `any Error`.
Da mesma forma, se o corpo incluir uma expressão `await`,
ele é entendido como assíncrono.

Há várias formas especiais que permitem escrever closures de forma mais concisa:

<!-- Apple Books screenshot ends here. -->

- Um closure pode omitir os tipos dos seus parâmetros, o tipo de retorno ou ambos.
  Se você omitir os nomes dos parâmetros e os dois tipos,
  omita a palavra-chave `in` antes das instruções.
  Se os tipos omitidos não puderem ser inferidos,
  um erro de compilação é gerado.
- Um closure pode omitir os nomes dos seus parâmetros.
  Os parâmetros são então nomeados implicitamente
  com `$` seguido da posição deles:
  `$0`, `$1`, `$2` e assim por diante.
- Um closure formado por uma única expressão é entendido como retornando o valor dessa expressão.
  O conteúdo dessa expressão também é considerado
  ao realizar a inferência de tipo da expressão que a envolve.

As seguintes expressões de closure são equivalentes:

```swift
myFunction { (x: Int, y: Int) -> Int in
    return x + y
}

myFunction { x, y in
    return x + y
}

myFunction { return $0 + $1 }

myFunction { $0 + $1 }
```

<!--
  - test: `closure-expression-forms`

  ```swifttest
  >> func myFunction(f: (Int, Int) -> Int) {}
  -> myFunction { (x: Int, y: Int) -> Int in
         return x + y
     }

  -> myFunction { x, y in
         return x + y
     }

  -> myFunction { return $0 + $1 }

  -> myFunction { $0 + $1 }
  ```
-->

Para informações sobre como passar um closure como argumento de uma função,
veja <doc:Expressions#Function-Call-Expression>.

Expressões de closure podem ser usadas
sem serem armazenadas em uma variável ou constante,
como quando você usa imediatamente um closure como parte de uma chamada de função.
As expressões de closure passadas a `myFunction` no código acima
são exemplos desse uso imediato.
Como resultado,
se uma expressão de closure é escaping ou nonescaping depende
do contexto em que a expressão está inserida.
Uma expressão de closure é nonescaping
se for chamada imediatamente
ou passada como argumento de função nonescaping.
Caso contrário, a expressão de closure é escaping.

Para mais informações sobre closures escaping, veja <doc:Closures#Escaping-Closures>.

#### Listas de captura

Por padrão, uma expressão de closure captura
constantes e variáveis do escopo que a envolve
com referências fortes a esses valores.
Você pode usar uma *lista de captura* para controlar explicitamente
como os valores são capturados em um closure.

Uma lista de captura é escrita como uma lista de expressões separadas por vírgula,
delimitada por colchetes, antes da lista de parâmetros.
Se você usar uma lista de captura, também precisa usar a palavra-chave `in`,
mesmo que omita os nomes dos parâmetros, os tipos dos parâmetros e o tipo de retorno.
A última expressão da lista de captura pode ser seguida de uma vírgula opcional.

As entradas da lista de captura são inicializadas
quando o closure é criado.
Para cada entrada da lista de captura,
uma constante é inicializada
com o valor da constante ou variável de mesmo nome no escopo que a envolve.
Por exemplo, no código abaixo,
`a` está na lista de captura, mas `b` não está,
o que faz com que eles tenham comportamentos diferentes.

```swift
var a = 0
var b = 0
let closure = { [a] in
 print(a, b)
}

a = 10
b = 10
closure()
// Prints "0 10".
```

<!--
  - test: `capture-list-value-semantics`

  ```swifttest
  -> var a = 0
  -> var b = 0
  -> let closure = { [a] in
      print(a, b)
  }

  -> a = 10
  -> b = 10
  -> closure()
  <- 0 10
  ```
-->

Há duas coisas diferentes chamadas `a`:
a variável do escopo externo
e a constante do escopo do closure,
mas há apenas uma variável chamada `b`.
O `a` do escopo interno é inicializado
com o valor do `a` do escopo externo
quando o closure é criado,
mas os valores deles não estão conectados de nenhuma forma especial.
Isso significa que uma mudança no valor de `a` no escopo externo
não afeta o valor de `a` no escopo interno,
nem uma mudança em `a` dentro do closure
afeta o `a` fora dele.
Em contraste, há apenas uma variável chamada `b`:
o `b` do escopo externo.
Assim, mudanças feitas de dentro ou de fora do closure
são visíveis nos dois lugares.

<!--
  [Contributor 6004] also describes the distinction as
  "capturing the variable, not the value"
  but he notes that we don't have a rigorous definition of
  capturing a variable in Swift
  (unlike some other languages)
  so that description's not likely to be very helpful for developers.
-->

Essa distinção não é visível
quando o tipo da variável capturada tem semântica de referência.
Por exemplo,
há duas coisas chamadas `x` no código abaixo,
uma variável no escopo externo e uma constante no escopo interno,
mas as duas se referem ao mesmo objeto
por causa da semântica de referência.

```swift
class SimpleClass {
    var value: Int = 0
}
var x = SimpleClass()
var y = SimpleClass()
let closure = { [x] in
    print(x.value, y.value)
}

x.value = 10
y.value = 10
closure()
// Prints "10 10".
```

<!--
  - test: `capture-list-reference-semantics`

  ```swifttest
  -> class SimpleClass {
         var value: Int = 0
     }
  -> var x = SimpleClass()
  -> var y = SimpleClass()
  -> let closure = { [x] in
         print(x.value, y.value)
     }

  -> x.value = 10
  -> y.value = 10
  -> closure()
  <- 10 10
  ```
-->

<!--
  - test: `capture-list-with-commas`

  ```swifttest
  -> var x = 100
  -> var y = 7
  -> var f: () -> Int = { [x, y] in x+y }
  >> let r0 = f()
  >> assert(r0 == 107)
  ```
-->

<!--
  It's not an error to capture things that aren't included in the capture list,
  although maybe it should be.  See also rdar://17024367.
-->

<!--
  - test: `capture-list-is-not-exhaustive`

  ```swifttest
  -> var x = 100
     var y = 7
     var f: () -> Int = { [x] in x }
     var g: () -> Int = { [x] in x+y }

  -> let r0 = f()
  -> assert(r0 == 100)
  -> let r1 = g()
  -> assert(r1 == 107)
  ```
-->

Se o tipo do valor da expressão for uma classe,
você pode marcar a expressão em uma lista de captura com `weak` ou `unowned`
para capturar uma referência fraca ou não proprietária ao valor da expressão.

```swift
myFunction { print(self.title) }                    // implicit strong capture
myFunction { [self] in print(self.title) }          // explicit strong capture
myFunction { [weak self] in print(self!.title) }    // weak capture
myFunction { [unowned self] in print(self.title) }  // unowned capture
```

<!--
  - test: `closure-expression-weak`

  ```swifttest
  >> func myFunction(f: () -> Void) { f() }
  >> class C {
  >> let title = "Title"
  >> func method() {
  -> myFunction { print(self.title) }                    // implicit strong capture
  -> myFunction { [self] in print(self.title) }          // explicit strong capture
  -> myFunction { [weak self] in print(self!.title) }    // weak capture
  -> myFunction { [unowned self] in print(self.title) }  // unowned capture
  >> } }
  >> C().method()
  << Title
  << Title
  << Title
  << Title
  ```
-->

Você também pode vincular uma expressão arbitrária
a um valor nomeado em uma lista de captura.
A expressão é avaliada quando o closure é criado,
e o valor é capturado com a força especificada.
Por exemplo:

```swift
// Weak capture of "self.parent" as "parent".
myFunction { [weak parent = self.parent] in print(parent!.title) }
```

<!--
  - test: `closure-expression-capture`

  ```swifttest
  >> func myFunction(f: () -> Void) { f() }
  >> class P { let title = "Title" }
  >> class C {
  >> let parent = P()
  >> func method() {
  // Weak capture of "self.parent" as "parent".
  -> myFunction { [weak parent = self.parent] in print(parent!.title) }
  >> } }
  >> C().method()
  << Title
  ```
-->

Para mais informações e exemplos de expressões de closure,
veja <doc:Closures#Closure-Expressions>.
Para mais informações e exemplos de listas de captura,
veja <doc:AutomaticReferenceCounting#Resolving-Strong-Reference-Cycles-for-Closures>.

<!--
  - test: `async-throwing-closure-syntax`

  ```swifttest
  >> var a = 12
  >> let c1 = { [a] in return a }                  // OK: No async or throws
  >> let c2 = { [a] async in return a }            // Error
  >> let c3 = { [a] async -> in return a }         // Error
  >> let c4 = { [a] () async -> Int in return a }  // OK: Has () and ->
  !$ error: expected expression
  !! let c3 = { [a] async -> in return a }         // Error
  !! ^
  !$ error: unable to infer type of a closure parameter 'async' in the current context
  !! let c2 = { [a] async in return a }            // Error
  !! ^
  // NOTE: The error message for c3 gets printed by the REPL before the c2 error.
  ```
-->

> Gramática de uma expressão de closure:
>
> *closure-expression* → **`{`** *attributes*_?_ *closure-signature*_?_ *statements*_?_ **`}`**
>
> *closure-signature* → *capture-list*_?_ *closure-parameter-clause* **`async`**_?_ *throws-clause*_?_ *function-result*_?_ **`in`** \
> *closure-signature* → *capture-list* **`in`**
>
> *closure-parameter-clause* → **`(`** **`)`** | **`(`** *closure-parameter-list* **`,`**_?_ **`)`** | *identifier-list* \
> *closure-parameter-list* → *closure-parameter* | *closure-parameter* **`,`** *closure-parameter-list* \
> *closure-parameter* → *closure-parameter-name* *type-annotation*_?_ \
> *closure-parameter* → *closure-parameter-name* *type-annotation* **`...`** \
> *closure-parameter-name* → *identifier*
>
> *capture-list* → **`[`** *capture-list-items* **`,`**_?_ **`]`** \
> *capture-list-items* → *capture-list-item* | *capture-list-item* **`,`** *capture-list-items* \
> *capture-list-item* → *capture-specifier*_?_ *identifier* \
> *capture-list-item* → *capture-specifier*_?_ *identifier* **`=`** *expression* \
> *capture-list-item* → *capture-specifier*_?_ *self-expression* \
> *capture-specifier* → **`weak`** | **`unowned`** | **`unowned(safe)`** | **`unowned(unsafe)`**

### Expressão de membro implícito

Uma *expressão de membro implícito* é uma forma abreviada de acessar um membro de um tipo,
como um caso de enumeração ou um método de tipo,
em um contexto em que a inferência de tipo consegue determinar o tipo implícito.
Ela tem a seguinte forma:

```swift
.<#member name#>
```

Por exemplo:

```swift
var x = MyEnumeration.someValue
x = .anotherValue
```

<!--
  - test: `implicitMemberEnum`

  ```swifttest
  >> enum MyEnumeration { case someValue, anotherValue }
  -> var x = MyEnumeration.someValue
  -> x = .anotherValue
  ```
-->

Se o tipo inferido for um optional,
você também pode usar um membro do tipo não opcional
em uma expressão de membro implícito.

```swift
var someOptional: MyEnumeration? = .someValue
```

<!--
  - test: `implicitMemberEnum`

  ```swifttest
  -> var someOptional: MyEnumeration? = .someValue
  ```
-->

Expressões de membro implícito podem ser seguidas de um operador pós-fixo
ou de outra sintaxe pós-fixa listada em
<doc:Expressions#Postfix-Expressions>.
Isso se chama *expressão de membro implícito encadeada*.
Embora seja comum que todas as expressões pós-fixas encadeadas
tenham o mesmo tipo,
o único requisito é que a expressão de membro implícito encadeada inteira
seja conversível para o tipo implícito pelo contexto.
Especificamente,
se o tipo implícito for um optional,
você pode usar um valor do tipo não opcional;
e se o tipo implícito for um tipo classe,
você pode usar um valor de uma das suas subclasses.
Por exemplo:

```swift
class SomeClass {
    static var shared = SomeClass()
    static var sharedSubclass = SomeSubclass()
    var a = AnotherClass()
}
class SomeSubclass: SomeClass { }
class AnotherClass {
    static var s = SomeClass()
    func f() -> SomeClass { return AnotherClass.s }
}
let x: SomeClass = .shared.a.f()
let y: SomeClass? = .shared
let z: SomeClass = .sharedSubclass
```

<!--
  - test: `implicit-member-chain`

  ```swifttest
  -> class SomeClass {
         static var shared = SomeClass()
         static var sharedSubclass = SomeSubclass()
         var a = AnotherClass()
     }
  -> class SomeSubclass: SomeClass { }
  -> class AnotherClass {
         static var s = SomeClass()
         func f() -> SomeClass { return AnotherClass.s }
     }
  -> let x: SomeClass = .shared.a.f()
  -> let y: SomeClass? = .shared
  -> let z: SomeClass = .sharedSubclass
  ```
-->

No código acima,
o tipo de `x` corresponde exatamente ao tipo implícito pelo contexto,
o tipo de `y` é conversível de `SomeClass` para `SomeClass?`,
e o tipo de `z` é conversível de `SomeSubclass` para `SomeClass`.

> Gramática de uma expressão de membro implícito:
>
> *implicit-member-expression* → **`.`** *identifier* \
> *implicit-member-expression* → **`.`** *identifier* **`.`** *postfix-expression*

<!--
  The grammar above allows the additional pieces tested below,
  which work even though they're omitted from the SE-0287 list.
  The grammar also overproduces, allowing any primary expression
  because of the definition of postfix-expression.
-->

<!--
  - test: `implicit-member-grammar`

  ```swifttest
  // self expression
  >> enum E { case left, right }
  >> let e: E = .left
  >> let e2: E = .left.self
  >> assert(e == e2)

  // postfix operator
  >> postfix operator ~
  >> extension E {
  >>     static postfix func ~ (e: E) -> E {
  >>         switch e {
  >>         case .left: return .right
  >>         case .right: return .left
  >>         }
  >>     }
  >> }
  >> let e3: E = .left~
  >> assert(e3 == .right)

  // initializer expression
  >> class S {
  >>     var num: Int
  >>     init(bestNumber: Int) { self.num = bestNumber }
  >> }
  >> let s: S = .init(bestNumber: 42)
  ```
-->

### Expressão entre parênteses

Uma *expressão entre parênteses* consiste em uma expressão
delimitada por parênteses.
Você pode usar parênteses para especificar a precedência das operações,
agrupando expressões explicitamente.
Parênteses de agrupamento não mudam o tipo de uma expressão:
por exemplo, o tipo de `(1)` é simplesmente `Int`.

<!--
  See "Tuple Expression" below for langref grammar.
-->

> Gramática de uma expressão entre parênteses:
>
> *parenthesized-expression* → **`(`** *expression* **`)`**

### Expressão de tupla

Uma *expressão de tupla* consiste em
uma lista de expressões separadas por vírgula e delimitada por parênteses.
Cada expressão pode ter um identificador opcional antes dela,
separado por dois-pontos (`:`).
Ela tem a seguinte forma:

```swift
(<#identifier 1#>: <#expression 1#>, <#identifier 2#>: <#expression 2#>, <#...#>)
```

Cada identificador em uma expressão de tupla precisa ser único
dentro do escopo da expressão de tupla.
Em uma expressão de tupla aninhada,
os identificadores no mesmo nível de aninhamento precisam ser únicos.
Por exemplo,
`(a: 10, a: 20)` é inválida
porque o rótulo `a` aparece duas vezes no mesmo nível.
No entanto, `(a: 10, b: (a: 1, x: 2))` é válida:
embora `a` apareça duas vezes,
ele aparece uma vez na tupla externa e uma vez na tupla interna.

<!--
  - test: `tuple-labels-must-be-unique`

  ```swifttest
  >> let bad = (a: 10, a: 20)
  >> let good = (a: 10, b: (a: 1, x: 2))
  !$ error: cannot create a tuple with a duplicate element label
  !! let bad = (a: 10, a: 20)
  !! ^
  ```
-->

Uma expressão de tupla pode conter zero expressões
ou duas ou mais expressões.
Uma única expressão entre parênteses é uma expressão entre parênteses.

> Nota: Tanto a expressão de tupla vazia quanto o tipo de tupla vazio
> são escritos `()` em Swift.
> Como `Void` é um alias de tipo para `()`,
> você pode usá-lo para escrever um tipo de tupla vazio.
> No entanto, como todos os aliases de tipo, `Void` é sempre um tipo:
> você não pode usá-lo para escrever uma expressão de tupla vazia.

A última expressão de uma tupla pode ser seguida de uma vírgula opcional.

> Gramática de uma expressão de tupla:
>
> *tuple-expression* → **`(`** **`)`** | **`(`** *tuple-element* **`,`** *tuple-element-list* **`,`**_?_ **`)`** \
> *tuple-element-list* → *tuple-element* | *tuple-element* **`,`** *tuple-element-list* \
> *tuple-element* → *expression* | *identifier* **`:`** *expression*

### Expressão curinga

Uma *expressão curinga* é usada para ignorar explicitamente um valor durante uma atribuição.
Por exemplo, na atribuição a seguir,
10 é atribuído a `x` e 20 é ignorado:

```swift
(x, _) = (10, 20)
// x is 10, and 20 is ignored
```

<!--
  - test: `wildcardTuple`

  ```swifttest
  >> var (x, _) = (10, 20)
  -> (x, _) = (10, 20)
  -> // x is 10, and 20 is ignored
  ```
-->

> Gramática de uma expressão curinga:
>
> *wildcard-expression* → **`_`**

### Expressão de expansão de macro

Uma *expressão de expansão de macro* consiste em um nome de macro
seguido de uma lista de argumentos da macro separados por vírgula e delimitados por parênteses.
A macro é expandida em tempo de compilação.
Expressões de expansão de macro têm a seguinte forma:

```swift
<#macro name#>(<#macro argument 1#>, <#macro argument 2#>)
```

Uma expressão de expansão de macro omite os parênteses depois do nome da macro
se a macro não receber nenhum argumento.

Uma expressão de expansão de macro pode aparecer como valor padrão de um parâmetro.
Quando usada como valor padrão de um parâmetro de função ou método,
as macros são avaliadas usando a localização no código-fonte do ponto de chamada,
e não o lugar onde aparecem na definição da função.
No entanto, quando um valor padrão é uma expressão maior
que contém uma macro além de outros códigos,
essas macros são avaliadas onde aparecem na definição da função.

```swift
func f(a: Int = #line, b: Int = (#line), c: Int = 100 + #line) {
    print(a, b, c)
}
f()  // Prints "4 1 101"
```

Na função acima,
o valor padrão de `a` é uma única expressão de macro,
então essa macro é avaliada usando a localização no código-fonte
onde `f(a:b:c:)` é chamada.
Em contraste, os valores de `b` e `c`
são expressões que contêm uma macro:
as macros nessas expressões são avaliadas
usando a localização no código-fonte onde `f(a:b:c:)` é definida.

Quando você usa uma macro como valor padrão,
ela é verificada quanto ao tipo sem ser expandida,
para checar os seguintes requisitos:

- O nível de acesso da macro
  é igual ao da função que a usa, ou menos restritivo que ele.
- A macro não recebe argumentos,
  ou seus argumentos são literais sem interpolação de string.
- O tipo de retorno da macro corresponde ao tipo do parâmetro.

Você usa expressões de macro para chamar macros freestanding.
Para chamar uma macro anexada, use a sintaxe de atributo personalizado
descrita em <doc:Attributes>.
Tanto macros freestanding quanto macros anexadas se expandem da seguinte forma:

1. O Swift analisa o código-fonte
   para produzir uma árvore de sintaxe abstrata (AST).

2. A implementação da macro recebe os nós da AST como entrada
   e realiza as transformações necessárias para essa macro.

3. Os nós da AST transformados que a implementação da macro produziu
   são adicionados à AST original.

A expansão de cada macro é independente e autocontida.
No entanto, como otimização de desempenho,
o Swift pode iniciar um processo externo que implementa a macro
e reutilizar o mesmo processo para expandir várias macros.
Ao implementar uma macro,
esse código não pode depender das macros que seu código expandiu antes,
nem de qualquer outro estado externo, como a hora atual.

Para macros aninhadas e macros anexadas com vários papéis,
o processo de expansão se repete.
Expressões de expansão de macro aninhadas se expandem de fora para dentro.
Por exemplo, no código abaixo,
`outerMacro(_:)` se expande primeiro,
e a chamada ainda não expandida a `innerMacro(_:)`
aparece na árvore de sintaxe abstrata que `outerMacro(_:)` recebe como entrada.

```swift
#outerMacro(12, #innerMacro(34), "some text")
```

Uma macro anexada com vários papéis se expande uma vez para cada papel.
Cada expansão recebe a mesma AST original como entrada.
O Swift forma a expansão completa reunindo todos os nós de AST gerados
e colocando-os nos seus lugares correspondentes na AST.

Para uma visão geral das macros em Swift, veja <doc:Macros>.

> Gramática de uma expressão macro-expansion:
>
> *macro-expansion-expression* → **`#`** *identifier* *generic-argument-clause*_?_ *function-call-argument-clause*_?_ *trailing-closures*_?_

### Expressão de key path

Uma *expressão de key path* faz referência a uma propriedade ou a um subscript de um tipo.
Você usa expressões de key path em tarefas de programação dinâmica,
como key-value observing.
Elas têm a seguinte forma:

```swift
\<#type name#>.<#path#>
```

O *nome do tipo* é o nome de um tipo concreto,
incluindo quaisquer parâmetros genéricos,
como `String`, `[Int]` ou `Set<Int>`.

O *caminho* consiste em nomes de propriedades, subscripts,
expressões de optional chaining e expressões de force unwrapping.
Cada um desses componentes do key path pode ser repetido
quantas vezes for necessário, em qualquer ordem.

Em tempo de compilação, uma expressão de key path é substituída
por uma instância da classe [`KeyPath`](https://developer.apple.com/documentation/swift/keypath).

Para acessar um valor usando um key path,
passe o key path para o subscript `subscript(keyPath:)`,
que está disponível em todos os tipos.
Por exemplo:

<!--
  The subscript name subscript(keyPath:) above is a little odd,
  but it matches what would be displayed on the web.
  There isn't actually an extension on Any that implements this subscript;
  it's a special case in the compiler.
-->

```swift
struct SomeStructure {
    var someValue: Int
}

let s = SomeStructure(someValue: 12)
let pathToProperty = \SomeStructure.someValue

let value = s[keyPath: pathToProperty]
// value is 12
```

<!--
  - test: `keypath-expression`

  ```swifttest
  -> struct SomeStructure {
         var someValue: Int
     }

  -> let s = SomeStructure(someValue: 12)
  -> let pathToProperty = \SomeStructure.someValue

  -> let value = s[keyPath: pathToProperty]
  /> value is \(value)
  </ value is 12
  ```
-->

O *nome do tipo* pode ser omitido
em contextos em que a inferência de tipo consegue determinar o tipo implícito.
O código a seguir usa `\.someProperty`
em vez de `\SomeClass.someProperty`:

```swift
class SomeClass: NSObject {
    @objc dynamic var someProperty: Int
    init(someProperty: Int) {
        self.someProperty = someProperty
    }
}

let c = SomeClass(someProperty: 10)
c.observe(\.someProperty) { object, change in
    // ...
}
```

<!--
  - test: `keypath-expression-implicit-type-name`

  ```swifttest
  >> import Foundation
  -> class SomeClass: NSObject {
  ->     @objc dynamic var someProperty: Int
  ->     init(someProperty: Int) {
  ->         self.someProperty = someProperty
  ->     }
  -> }

  -> let c = SomeClass(someProperty: 10)
  >> let r0 =
  -> c.observe(\.someProperty) { object, change in
         // ...
     }
  ```
-->

<!--
  Rewrite the above to avoid discarding the function's return value.
  Tracking bug is <rdar://problem/35301593>
-->

O *caminho* pode se referir a `self` para criar o key path de identidade (`\.self`).
O key path de identidade se refere a uma instância inteira,
então você pode usá-lo para acessar e alterar todos os dados armazenados em uma variável
em uma única etapa.
Por exemplo:

```swift
var compoundValue = (a: 1, b: 2)
// Equivalent to compoundValue = (a: 10, b: 20)
compoundValue[keyPath: \.self] = (a: 10, b: 20)
```

<!--
  - test: `keypath-expression-self-keypath`

  ```swifttest
  -> var compoundValue = (a: 1, b: 2)
  // Equivalent to compoundValue = (a: 10, b: 20)
  -> compoundValue[keyPath: \.self] = (a: 10, b: 20)
  ```
-->

O *caminho* pode conter vários nomes de propriedades,
separados por pontos,
para se referir a uma propriedade do valor de outra propriedade.
Este código usa a expressão de key path
`\OuterStructure.outer.someValue`
para acessar a propriedade `someValue`
da propriedade `outer` do tipo `OuterStructure`:

```swift
struct OuterStructure {
    var outer: SomeStructure
    init(someValue: Int) {
        self.outer = SomeStructure(someValue: someValue)
    }
}

let nested = OuterStructure(someValue: 24)
let nestedKeyPath = \OuterStructure.outer.someValue

let nestedValue = nested[keyPath: nestedKeyPath]
// nestedValue is 24
```

<!--
  - test: `keypath-expression`

  ```swifttest
  -> struct OuterStructure {
         var outer: SomeStructure
         init(someValue: Int) {
             self.outer = SomeStructure(someValue: someValue)
         }
     }

  -> let nested = OuterStructure(someValue: 24)
  -> let nestedKeyPath = \OuterStructure.outer.someValue

  -> let nestedValue = nested[keyPath: nestedKeyPath]
  /> nestedValue is \(nestedValue)
  </ nestedValue is 24
  ```
-->

O *caminho* pode incluir subscripts entre colchetes,
desde que o tipo do parâmetro do subscript esteja em conformidade com o protocolo `Hashable`.
Este exemplo usa um subscript em um key path
para acessar o segundo elemento de um array:

```swift
let greetings = ["hello", "hola", "bonjour", "안녕"]
let myGreeting = greetings[keyPath: \[String].[1]]
// myGreeting is 'hola'
```

<!--
  - test: `keypath-expression`

  ```swifttest
  -> let greetings = ["hello", "hola", "bonjour", "안녕"]
  -> let myGreeting = greetings[keyPath: \[String].[1]]
  /> myGreeting is '\(myGreeting)'
  </ myGreeting is 'hola'
  ```
-->

<!--
  TODO: Update examples here and below to remove type names once
  inference bugs are fixed. The compiler currently gives an error
  that the usage is ambiguous.
  <rdar://problem/34376681> [SR-5865]: Key path expression is "ambiguous without more context"
-->

O valor usado em um subscript pode ser um valor nomeado ou um literal.
Os valores são capturados em key paths usando semântica de valor.
O código a seguir usa a variável `index`
tanto em uma expressão de key path quanto em um closure
para acessar o terceiro elemento do array `greetings`.
Quando `index` é modificada,
a expressão de key path continua se referindo ao terceiro elemento,
enquanto o closure usa o novo índice.

```swift
var index = 2
let path = \[String].[index]
let fn: ([String]) -> String = { strings in strings[index] }

print(greetings[keyPath: path])
// Prints "bonjour".
print(fn(greetings))
// Prints "bonjour".

// Setting 'index' to a new value doesn't affect 'path'
index += 1
print(greetings[keyPath: path])
// Prints "bonjour".

// Because 'fn' closes over 'index', it uses the new value
print(fn(greetings))
// Prints "안녕".
```

<!--
  - test: `keypath-expression`

  ```swifttest
  -> var index = 2
  -> let path = \[String].[index]
  -> let fn: ([String]) -> String = { strings in strings[index] }

  -> print(greetings[keyPath: path])
  <- bonjour
  -> print(fn(greetings))
  <- bonjour

  // Setting 'index' to a new value doesn't affect 'path'
  -> index += 1
  -> print(greetings[keyPath: path])
  <- bonjour

  // Because 'fn' closes over 'index', it uses the new value
  -> print(fn(greetings))
  <- 안녕
  ```
-->

O *caminho* pode usar optional chaining e force unwrapping.
Este código usa optional chaining em um key path
para acessar uma propriedade de uma string opcional:

```swift
let firstGreeting: String? = greetings.first
print(firstGreeting?.count as Any)
// Prints "Optional(5)".

// Do the same thing using a key path.
let count = greetings[keyPath: \[String].first?.count]
print(count as Any)
// Prints "Optional(5)".
```

<!--
  - test: `keypath-expression`

  ```swifttest
  -> let firstGreeting: String? = greetings.first
  -> print(firstGreeting?.count as Any)
  <- Optional(5)

  // Do the same thing using a key path.
  -> let count = greetings[keyPath: \[String].first?.count]
  -> print(count as Any)
  <- Optional(5)
  ```
-->

<!--
  The test above is failing, which appears to be a compiler bug.
  <rdar://problem/58484319> Swift 5.2 regression in keypaths
-->

Você pode misturar e combinar componentes de key paths
para acessar valores que estão profundamente aninhados dentro de um tipo.
O código a seguir acessa valores e propriedades diferentes
de um dicionário de arrays,
usando expressões de key path que combinam esses componentes.

```swift
let interestingNumbers = ["prime": [2, 3, 5, 7, 11, 13, 17],
                          "triangular": [1, 3, 6, 10, 15, 21, 28],
                          "hexagonal": [1, 6, 15, 28, 45, 66, 91]]
print(interestingNumbers[keyPath: \[String: [Int]].["prime"]] as Any)
// Prints "Optional([2, 3, 5, 7, 11, 13, 17])".
print(interestingNumbers[keyPath: \[String: [Int]].["prime"]![0]])
// Prints "2".
print(interestingNumbers[keyPath: \[String: [Int]].["hexagonal"]!.count])
// Prints "7".
print(interestingNumbers[keyPath: \[String: [Int]].["hexagonal"]!.count.bitWidth])
// Prints "64".
```

<!--
  - test: `keypath-expression`

  ```swifttest
  -> let interestingNumbers = ["prime": [2, 3, 5, 7, 11, 13, 17],
                               "triangular": [1, 3, 6, 10, 15, 21, 28],
                               "hexagonal": [1, 6, 15, 28, 45, 66, 91]]
  -> print(interestingNumbers[keyPath: \[String: [Int]].["prime"]] as Any)
  <- Optional([2, 3, 5, 7, 11, 13, 17])
  -> print(interestingNumbers[keyPath: \[String: [Int]].["prime"]![0]])
  <- 2
  -> print(interestingNumbers[keyPath: \[String: [Int]].["hexagonal"]!.count])
  <- 7
  -> print(interestingNumbers[keyPath: \[String: [Int]].["hexagonal"]!.count.bitWidth])
  <- 64
  ```
-->

Você pode usar uma expressão de key path
nos contextos em que normalmente forneceria uma função ou um closure.
Especificamente,
você pode usar uma expressão de key path
cujo tipo raiz é `SomeType`
e cujo caminho produz um valor do tipo `Value`,
no lugar de uma função ou closure do tipo `(SomeType) -> Value`.

```swift
struct Task {
    var description: String
    var completed: Bool
}
var toDoList = [
    Task(description: "Practice ping-pong.", completed: false),
    Task(description: "Buy a pirate costume.", completed: true),
    Task(description: "Visit Boston in the Fall.", completed: false),
]

// Both approaches below are equivalent.
let descriptions = toDoList.filter(\.completed).map(\.description)
let descriptions2 = toDoList.filter { $0.completed }.map { $0.description }
```

<!--
  - test: `keypath-expression`

  ```swifttest
  -> struct Task {
         var description: String
         var completed: Bool
     }
  -> var toDoList = [
         Task(description: "Practice ping-pong.", completed: false),
         Task(description: "Buy a pirate costume.", completed: true),
         Task(description: "Visit Boston in the Fall.", completed: false),
     ]

  // Both approaches below are equivalent.
  -> let descriptions = toDoList.filter(\.completed).map(\.description)
  -> let descriptions2 = toDoList.filter { $0.completed }.map { $0.description }
  >> assert(descriptions == descriptions2)
  ```
-->

<!--
  REFERENCE
  The to-do list above draws from the lyrics of the song
  "The Pirates Who Don't Do Anything".
-->

Quaisquer efeitos colaterais de uma expressão de key path
são avaliados somente no ponto em que a expressão é avaliada.
Por exemplo,
se você fizer uma chamada de função dentro de um subscript em uma expressão de key path,
a função é chamada apenas uma vez, como parte da avaliação da expressão,
e não toda vez que o key path é usado.

```swift
func makeIndex() -> Int {
    print("Made an index")
    return 0
}
// The line below calls makeIndex().
let taskKeyPath = \[Task][makeIndex()]
// Prints "Made an index".

// Using taskKeyPath doesn't call makeIndex() again.
let someTask = toDoList[keyPath: taskKeyPath]
```

<!--
  - test: `keypath-expression`

  ```swifttest
  -> func makeIndex() -> Int {
         print("Made an index")
         return 0
     }
  // The line below calls makeIndex().
  -> let taskKeyPath = \[Task][makeIndex()]
  <- Made an index
  >> print(type(of: taskKeyPath))
  << WritableKeyPath<Array<Task>, Task>

  // Using taskKeyPath doesn't call makeIndex() again.
  -> let someTask = toDoList[keyPath: taskKeyPath]
  ```
-->

Para mais informações sobre o uso de key paths
em código que interage com APIs do Objective-C,
veja [Usando recursos do runtime do Objective-C no Swift](https://developer.apple.com/documentation/swift/using_objective_c_runtime_features_in_swift).
Para informações sobre key-value coding e key-value observing,
veja [Guia de programação de Key-Value Coding](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/KeyValueCoding/index.html#//apple_ref/doc/uid/10000107i)
e [Guia de programação de Key-Value Observing](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/KeyValueObserving/KeyValueObserving.html#//apple_ref/doc/uid/10000177i).

> Gramática de uma expressão key-path:
>
> *key-path-expression* → **`\`** *type*_?_ **`.`** *key-path-components* \
> *key-path-components* → *key-path-component* | *key-path-component* **`.`** *key-path-components* \
> *key-path-component* → *identifier* *key-path-postfixes*_?_ | *key-path-postfixes*
>
> *key-path-postfixes* → *key-path-postfix* *key-path-postfixes*_?_ \
> *key-path-postfix* → **`?`** | **`!`** | **`self`** | **`[`** *function-call-argument-list* **`]`**

### Expressão de seletor

Uma expressão de seletor permite acessar o seletor usado para se referir a um método
ou ao getter ou setter de uma propriedade no Objective-C.
Ela tem a seguinte forma:

```swift
#selector(<#method name#>)
#selector(getter: <#property name#>)
#selector(setter: <#property name#>)
```

O *nome do método* e o *nome da propriedade* precisam ser uma referência
a um método ou a uma propriedade que esteja disponível no runtime do Objective-C.
O valor de uma expressão de seletor é uma instância do tipo `Selector`.
Por exemplo:

```swift
class SomeClass: NSObject {
    @objc let property: String

    @objc(doSomethingWithInt:)
    func doSomething(_ x: Int) { }

    init(property: String) {
        self.property = property
    }
}
let selectorForMethod = #selector(SomeClass.doSomething(_:))
let selectorForPropertyGetter = #selector(getter: SomeClass.property)
```

<!--
  - test: `selector-expression`

  ```swifttest
  >> import Foundation
  -> class SomeClass: NSObject {
  ->     @objc let property: String

  ->     @objc(doSomethingWithInt:)
         func doSomething(_ x: Int) { }

         init(property: String) {
             self.property = property
         }
     }
  -> let selectorForMethod = #selector(SomeClass.doSomething(_:))
  -> let selectorForPropertyGetter = #selector(getter: SomeClass.property)
  ```
-->

Ao criar um seletor para o getter de uma propriedade,
o *nome da propriedade* pode ser uma referência a uma propriedade variável ou constante.
Em contraste, ao criar um seletor para o setter de uma propriedade,
o *nome da propriedade* precisa ser uma referência apenas a uma propriedade variável.

O *nome do método* pode conter parênteses para agrupamento,
assim como o operador `as` para desambiguar métodos que compartilham um nome
mas têm assinaturas de tipo diferentes.
Por exemplo:

```swift
extension SomeClass {
    @objc(doSomethingWithString:)
    func doSomething(_ x: String) { }
}
let anotherSelector = #selector(SomeClass.doSomething(_:) as (SomeClass) -> (String) -> Void)
```

<!--
  - test: `selector-expression-with-as`

  ```swifttest
  >> import Foundation
  >> class SomeClass: NSObject {
  >>     @objc let property: String
  >>     @objc(doSomethingWithInt:)
  >>     func doSomething(_ x: Int) {}
  >>     init(property: String) {
  >>         self.property = property
  >>     }
  >> }
  -> extension SomeClass {
  ->     @objc(doSomethingWithString:)
         func doSomething(_ x: String) { }
     }
  -> let anotherSelector = #selector(SomeClass.doSomething(_:) as (SomeClass) -> (String) -> Void)
  ```
-->

Como um seletor é criado em tempo de compilação, não em tempo de execução,
o compilador consegue verificar se um método ou uma propriedade existe
e se eles estão expostos ao runtime do Objective-C.

> Nota: Embora o *nome do método* e o *nome da propriedade* sejam expressões,
> elas nunca são avaliadas.

Para mais informações sobre o uso de seletores
em código Swift que interage com APIs do Objective-C,
veja [Usando recursos do runtime do Objective-C no Swift](https://developer.apple.com/documentation/swift/using_objective_c_runtime_features_in_swift).

> Gramática de uma expressão de seletor:
>
> *selector-expression* → **`#selector`** **`(`** *expression* **`)`** \
> *selector-expression* → **`#selector`** **`(`** **`getter:`** *expression* **`)`** \
> *selector-expression* → **`#selector`** **`(`** **`setter:`** *expression* **`)`**

<!--
  Note: The parser does allow an arbitrary expression inside #selector(), not
  just a member name.  For example, see changes in Swift commit ef60d7289d in
  lib/Sema/CSApply.cpp -- there's explicit code to look through parens and
  optional binding.
-->

### Expressão de string de key path

Uma expressão de string de key path permite acessar a string
usada para se referir a uma propriedade no Objective-C,
para uso nas APIs de key-value coding e key-value observing.
Ela tem a seguinte forma:

```swift
#keyPath(<#property name#>)
```

O *nome da propriedade* precisa ser uma referência a uma propriedade
que esteja disponível no runtime do Objective-C.
Em tempo de compilação, a expressão de string de key path é substituída por um literal de string.
Por exemplo:

```swift
class SomeClass: NSObject {
    @objc var someProperty: Int
    init(someProperty: Int) {
       self.someProperty = someProperty
    }
}

let c = SomeClass(someProperty: 12)
let keyPath = #keyPath(SomeClass.someProperty)

if let value = c.value(forKey: keyPath) {
    print(value)
}
// Prints "12".
```

<!--
  - test: `keypath-string-expression`

  ```swifttest
  >> import Foundation
  -> class SomeClass: NSObject {
  ->    @objc var someProperty: Int
        init(someProperty: Int) {
            self.someProperty = someProperty
        }
     }

  -> let c = SomeClass(someProperty: 12)
  -> let keyPath = #keyPath(SomeClass.someProperty)

  -> if let value = c.value(forKey: keyPath) {
  ->     print(value)
  -> }
  <- 12
  ```
-->

Quando você usa uma expressão de string de key path dentro de uma classe,
pode se referir a uma propriedade dessa classe
escrevendo apenas o nome da propriedade, sem o nome da classe.

```swift
extension SomeClass {
    func getSomeKeyPath() -> String {
        return #keyPath(someProperty)
    }
}
print(keyPath == c.getSomeKeyPath())
// Prints "true".
```

<!--
  - test: `keypath-string-expression`

  ```swifttest
  -> extension SomeClass {
        func getSomeKeyPath() -> String {
           return #keyPath(someProperty)
        }
     }
  -> print(keyPath == c.getSomeKeyPath())
  <- true
  ```
-->

Como a string do key path é criada em tempo de compilação, não em tempo de execução,
o compilador consegue verificar se a propriedade existe
e se ela está exposta ao runtime do Objective-C.

Para mais informações sobre o uso de key paths
em código Swift que interage com APIs do Objective-C,
veja [Usando recursos do runtime do Objective-C no Swift](https://developer.apple.com/documentation/swift/using_objective_c_runtime_features_in_swift).
Para informações sobre key-value coding e key-value observing,
veja [Guia de programação de Key-Value Coding](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/KeyValueCoding/index.html#//apple_ref/doc/uid/10000107i)
e [Guia de programação de Key-Value Observing](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/KeyValueObserving/KeyValueObserving.html#//apple_ref/doc/uid/10000177i).

> Nota: Embora o *nome da propriedade* seja uma expressão, ela nunca é avaliada.

> Gramática de uma expressão key-path string:
>
> *key-path-string-expression* → **`#keyPath`** **`(`** *expression* **`)`**

## Expressões pós-fixas

*Expressões pós-fixas* são formadas
aplicando um operador pós-fixo ou outra sintaxe pós-fixa a uma expressão.
Sintaticamente, toda expressão primária também é uma expressão pós-fixa.

Para informações sobre o comportamento desses operadores,
veja <doc:BasicOperators> e <doc:AdvancedOperators>.

Para informações sobre os operadores fornecidos pela biblioteca padrão do Swift,
veja [Declarações de operadores](https://developer.apple.com/documentation/swift/operator_declarations).

> Gramática de uma expressão pós-fixa:
>
> *postfix-expression* → *primary-expression* \
> *postfix-expression* → *postfix-expression* *postfix-operator* \
> *postfix-expression* → *function-call-expression* \
> *postfix-expression* → *initializer-expression* \
> *postfix-expression* → *explicit-member-expression* \
> *postfix-expression* → *postfix-self-expression* \
> *postfix-expression* → *subscript-expression* \
> *postfix-expression* → *forced-value-expression* \
> *postfix-expression* → *optional-chaining-expression*

### Expressão de chamada de função

<!--
  TODO: After we rewrite function decls,
  revisit this section to make sure that the names for things match.
-->

Uma *expressão de chamada de função* consiste em um nome de função
seguido de uma lista de argumentos da função separados por vírgula e delimitados por parênteses.
Expressões de chamada de função têm a seguinte forma:

```swift
<#function name#>(<#argument value 1#>, <#argument value 2#>)
```

O *nome da função* pode ser qualquer expressão cujo valor seja de um tipo função.

Se a definição da função incluir nomes para os parâmetros,
a chamada da função precisa incluir os nomes antes dos valores dos argumentos,
separados por dois-pontos (`:`).
Esse tipo de expressão de chamada de função tem a seguinte forma:

```swift
<#function name#>(<#argument name 1#>: <#argument value 1#>, <#argument name 2#>: <#argument value 2#>)
```

O último argumento entre parênteses pode ser seguido de uma vírgula opcional.

Uma expressão de chamada de função pode incluir trailing closures,
na forma de expressões de closure imediatamente após o parêntese de fechamento.
Os trailing closures são entendidos como argumentos da função,
adicionados depois do último argumento entre parênteses.
O primeiro closure não tem rótulo;
qualquer closure adicional é precedido pelo rótulo do seu argumento.
O exemplo abaixo mostra as versões equivalentes de chamadas de função
que usam e que não usam a sintaxe de trailing closure:

```swift
// someFunction takes an integer and a closure as its arguments
someFunction(x: x, f: { $0 == 13 })
someFunction(x: x) { $0 == 13 }

// anotherFunction takes an integer and two closures as its arguments
anotherFunction(x: x, f: { $0 == 13 }, g: { print(99) })
anotherFunction(x: x) { $0 == 13 } g: { print(99) }
```

<!--
  - test: `trailing-closure`

  ```swifttest
  >> func someFunction (x: Int, f: (Int) -> Bool) -> Bool {
  >>    return f(x)
  >> }
  >> let x = 10
  // someFunction takes an integer and a closure as its arguments
  >> let r0 =
  -> someFunction(x: x, f: { $0 == 13 })
  >> assert(r0 == false)
  >> let r1 =
  -> someFunction(x: x) { $0 == 13 }
  >> assert(r1 == false)

  >> func anotherFunction(x: Int, f: (Int) -> Bool, g: () -> Void) -> Bool {
  >>    g(); return f(x)
  >> }
  // anotherFunction takes an integer and two closures as its arguments
  >> let r2 =
  -> anotherFunction(x: x, f: { $0 == 13 }, g: { print(99) })
  << 99
  >> assert(r2 == false)
  >> let r3 =
  -> anotherFunction(x: x) { $0 == 13 } g: { print(99) }
  << 99
  >> assert(r3 == false)
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

Se o trailing closure for o único argumento da função,
você pode omitir os parênteses.

```swift
// someMethod takes a closure as its only argument
myData.someMethod() { $0 == 13 }
myData.someMethod { $0 == 13 }
```

<!--
  - test: `no-paren-trailing-closure`

  ```swifttest
  >> class Data {
  >>    let data = 10
  >>    func someMethod(f: (Int) -> Bool) -> Bool {
  >>       return f(self.data)
  >>    }
  >> }
  >> let myData = Data()
  // someMethod takes a closure as its only argument
  >> let r0 =
  -> myData.someMethod() { $0 == 13 }
  >> assert(r0 == false)
  >> let r1 =
  -> myData.someMethod { $0 == 13 }
  >> assert(r1 == false)
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

Para incluir os trailing closures nos argumentos,
o compilador examina os parâmetros da função da esquerda para a direita, assim:

| Trailing closure | Parâmetro | Ação |
| ---------------- | --------- | ------ |
| Com rótulo | Com rótulo | Se os rótulos forem iguais, o closure corresponde ao parâmetro; caso contrário, o parâmetro é ignorado. |
| Com rótulo | Sem rótulo | O parâmetro é ignorado. |
| Sem rótulo | Com ou sem rótulo | Se o parâmetro se parecer estruturalmente com um tipo função, como definido abaixo, o closure corresponde ao parâmetro; caso contrário, o parâmetro é ignorado. |

O trailing closure é passado como argumento do parâmetro com o qual ele corresponde.
Parâmetros que foram ignorados durante a varredura não recebem argumento:
por exemplo, eles podem usar um valor padrão.
Depois de encontrar uma correspondência,
a varredura continua com o próximo trailing closure e o próximo parâmetro.
Ao final do processo de correspondência,
todos os trailing closures precisam ter uma correspondência.

Um parâmetro *se parece estruturalmente* com um tipo função
se o parâmetro não for in-out
e se for um dos seguintes:

- Um parâmetro cujo tipo é um tipo função,
  como `(Bool) -> Int`
- Um parâmetro autoclosure
  cujo tipo da expressão embrulhada é um tipo função,
  como `@autoclosure () -> ((Bool) -> Int)`
- Um parâmetro variádico
  cujo tipo de elemento do array é um tipo função,
  como `((Bool) -> Int)...`
- Um parâmetro cujo tipo é embrulhado em uma ou mais camadas de optional,
  como `Optional<(Bool) -> Int>`
- Um parâmetro cujo tipo combina esses tipos permitidos,
  como `(Optional<(Bool) -> Int>)...`

Quando um trailing closure é associado a um parâmetro
cujo tipo se parece estruturalmente com um tipo função, mas não é uma função,
o closure é embrulhado conforme necessário.
Por exemplo, se o tipo do parâmetro for um tipo optional,
o closure é embrulhado em `Optional` automaticamente.

<!--
  - test: `when-can-you-use-trailing-closure`

  ```swifttest
  // These tests match the example types given above
  // when describing what "structurally resembles" a function type.

  >> func f1(x: Int, y: (Bool)->Int) { print(x + y(true)) }
  >> f1(x: 10) { $0 ? 1 : 100 }
  << 11
  >> func f2(x: Int, y: @autoclosure ()->((Bool)->Int)) { print(x + y()(false)) }
  >> f2(x: 20) { $0 ? 2 : 200 }
  << 220
  >> func f3(x: Int, y: ((Bool)->Int)...) { print(x + y[0](true)) }
  >> f3(x: 30) { $0 ? 3 : 300}
  << 33
  >> func f4(x: Int, y: Optional<(Bool)->Int>) { print(x + y!(false)) }
  >> f4(x: 40) { $0 ? 4 : 400 }
  << 440
  >> func f5(x: Int, y: (Optional<(Bool) -> Int>)...) { print(x + y[0]!(true)) }
  >> f5(x: 50) { $0 ? 5 : 500 }
  << 55
  ```
-->

Para facilitar a migração de código de versões do Swift anteriores à 5.3,
que fazia essa correspondência da direita para a esquerda,
o compilador verifica as duas ordens, da esquerda para a direita e da direita para a esquerda.
Se as direções de varredura produzirem resultados diferentes,
a ordem antiga, da direita para a esquerda, é usada
e o compilador gera um aviso.
Uma versão futura do Swift sempre usará a ordem da esquerda para a direita.

<!-- FIXME: What future version? -->

```swift
typealias Callback = (Int) -> Int
func someFunction(firstClosure: Callback? = nil,
                secondClosure: Callback? = nil) {
    let first = firstClosure?(10)
    let second = secondClosure?(20)
    print(first ?? "-", second ?? "-")
}

someFunction()  // Prints "- -"
someFunction { return $0 + 100 }  // Ambiguous
someFunction { return $0 } secondClosure: { return $0 }  // Prints "10 20"
```

<!--
  - test: `trailing-closure-scanning-direction`

  ```swifttest
  -> typealias Callback = (Int) -> Int
  -> func someFunction(firstClosure: Callback? = nil,
                     secondClosure: Callback? = nil) {
         let first = firstClosure?(10)
         let second = secondClosure?(20)
         print(first ?? "-", second ?? "-")
     }

  -> someFunction()  // Prints "- -"
  << - -
  -> someFunction { return $0 + 100 }  // Ambiguous
  << - 120
  !$ warning: backward matching of the unlabeled trailing closure is deprecated; label the argument with 'secondClosure' to suppress this warning
  !! someFunction { return $0 + 100 }  // Ambiguous
  !!              ^
  !!              (secondClosure:     )
  !$ note: 'someFunction(firstClosure:secondClosure:)' declared here
  !! func someFunction(firstClosure: Callback? = nil,
  !!      ^
  -> someFunction { return $0 } secondClosure: { return $0 }  // Prints "10 20"
  << 10 20
  ```
-->

No exemplo acima,
a chamada de função marcada como "Ambiguous"
imprime "- 120" e gera um aviso do compilador no Swift 5.3.
Uma versão futura do Swift vai imprimir “110 -”.

<!--
  Smart quotes on the line above are needed
  because the regex heuristics gets the close quote wrong.
-->

Uma classe, uma estrutura ou um tipo enumeração
pode habilitar açúcar sintático para a sintaxe de chamada de função
ao declarar um de vários métodos,
como descrito em <doc:Declarations#Methods-with-Special-Names>.

#### Conversão implícita para um tipo ponteiro

Em uma expressão de chamada de função,
se o argumento e o parâmetro tiverem tipos diferentes,
o compilador tenta fazer os tipos corresponderem
aplicando uma das conversões implícitas da lista a seguir:

- `inout SomeType` pode se tornar
  `UnsafePointer<SomeType>` ou `UnsafeMutablePointer<SomeType>`
- `inout Array<SomeType>` pode se tornar
  `UnsafePointer<SomeType>` ou `UnsafeMutablePointer<SomeType>`
- `Array<SomeType>` pode se tornar `UnsafePointer<SomeType>`
- `String` pode se tornar `UnsafePointer<CChar>`

As duas chamadas de função a seguir são equivalentes:

```swift
func unsafeFunction(pointer: UnsafePointer<Int>) {
    // ...
}
var myNumber = 1234

unsafeFunction(pointer: &myNumber)
withUnsafePointer(to: myNumber) { unsafeFunction(pointer: $0) }
```

<!--
  - test: `inout-unsafe-pointer`

  ```swifttest
  -> func unsafeFunction(pointer: UnsafePointer<Int>) {
  ->     // ...
  >>     print(pointer.pointee)
  -> }
  -> var myNumber = 1234

  -> unsafeFunction(pointer: &myNumber)
  -> withUnsafePointer(to: myNumber) { unsafeFunction(pointer: $0) }
  << 1234
  << 1234
  ```
-->

Um ponteiro criado por essas conversões implícitas
é válido apenas durante a chamada de função.
Para evitar comportamento indefinido,
garanta que seu código nunca persista o ponteiro depois que a chamada de função terminar.

> Nota: Ao converter implicitamente um array para um ponteiro não seguro,
> o Swift garante que o armazenamento do array seja contíguo,
> convertendo ou copiando o array quando necessário.
> Por exemplo, você pode usar essa sintaxe com um array que teve ponte com `Array`
> a partir de uma subclasse de `NSArray` que não faz nenhum contrato de API sobre o seu armazenamento.
> Se você precisar garantir que o armazenamento do array já seja contíguo,
> para que a conversão implícita nunca precise fazer esse trabalho,
> use `ContiguousArray` em vez de `Array`.

Usar `&` em vez de uma função explícita como `withUnsafePointer(to:)`
pode ajudar a tornar as chamadas para funções C de baixo nível mais legíveis,
especialmente quando a função recebe vários argumentos de ponteiro.
No entanto, ao chamar funções a partir de outro código Swift,
evite usar `&` no lugar de usar as APIs não seguras explicitamente.

<!--
  - test: `implicit-conversion-to-pointer`

  ```swifttest
  >> import Foundation
  >> func takesUnsafePointer(p: UnsafePointer<Int>) { }
  >> func takesUnsafeMutablePointer(p: UnsafeMutablePointer<Int>) { }
  >> func takesUnsafePointerCChar(p: UnsafePointer<CChar>) { }
  >> func takesUnsafeMutablePointerCChar(p: UnsafeMutablePointer<CChar>) { }
  >> var n = 12
  >> var array = [1, 2, 3]
  >> var nsarray: NSArray = [10, 20, 30]
  >> var bridgedNSArray = nsarray as! Array<Int>
  >> var string = "Hello"

  // bullet 1
  >> takesUnsafePointer(p: &n)
  >> takesUnsafeMutablePointer(p: &n)

  // bullet 2
  >> takesUnsafePointer(p: &array)
  >> takesUnsafeMutablePointer(p: &array)
  >> takesUnsafePointer(p: &bridgedNSArray)
  >> takesUnsafeMutablePointer(p: &bridgedNSArray)

  // bullet 3
  >> takesUnsafePointer(p: array)
  >> takesUnsafePointer(p: bridgedNSArray)

  // bullet 4
  >> takesUnsafePointerCChar(p: string)

  // invalid conversions
  >> takesUnsafeMutablePointer(p: array)
  !$ error: cannot convert value of type '[Int]' to expected argument type 'UnsafeMutablePointer<Int>'
  !! takesUnsafeMutablePointer(p: array)
  !!                              ^
  >> takesUnsafeMutablePointerCChar(p: string)
  !$ error: cannot convert value of type 'String' to expected argument type 'UnsafeMutablePointer<CChar>' (aka 'UnsafeMutablePointer<Int8>')
  !! takesUnsafeMutablePointerCChar(p: string)
  !!                                   ^
  ```
-->

> Gramática de uma expressão de chamada de função:
>
> *function-call-expression* → *postfix-expression* *function-call-argument-clause* \
> *function-call-expression* → *postfix-expression* *function-call-argument-clause*_?_ *trailing-closures*
>
> *function-call-argument-clause* → **`(`** **`)`** | **`(`** *function-call-argument-list* **`,`**_?_ **`)`** \
> *function-call-argument-list* → *function-call-argument* | *function-call-argument* **`,`** *function-call-argument-list* \
> *function-call-argument* → *expression* | *identifier* **`:`** *expression* \
> *function-call-argument* → *operator* | *identifier* **`:`** *operator*
>
> *trailing-closures* → *closure-expression* *labeled-trailing-closures*_?_ \
> *labeled-trailing-closures* → *labeled-trailing-closure* *labeled-trailing-closures*_?_ \
> *labeled-trailing-closure* → *identifier* **`:`** *closure-expression*

### Expressão de inicializador

Uma *expressão de inicializador* dá acesso ao inicializador de um tipo.
Ela tem a seguinte forma:

```swift
<#expression#>.init(<#initializer arguments#>)
```

Você usa a expressão de inicializador em uma expressão de chamada de função
para inicializar uma nova instância de um tipo.
Você também usa uma expressão de inicializador
para delegar ao inicializador de uma superclasse.

```swift
class SomeSubClass: SomeSuperClass {
    override init() {
        // subclass initialization goes here
        super.init()
    }
}
```

<!--
  - test: `init-call-superclass`

  ```swifttest
  >> class SomeSuperClass { }
  -> class SomeSubClass: SomeSuperClass {
  ->     override init() {
  ->         // subclass initialization goes here
  ->         super.init()
  ->     }
  -> }
  ```
-->

Assim como uma função, um inicializador pode ser usado como valor.
Por exemplo:

```swift
// Type annotation is required because String has multiple initializers.
let initializer: (Int) -> String = String.init
let oneTwoThree = [1, 2, 3].map(initializer).reduce("", +)
print(oneTwoThree)
// Prints "123".
```

<!--
  - test: `init-as-value`

  ```swifttest
  // Type annotation is required because String has multiple initializers.
  -> let initializer: (Int) -> String = String.init
  -> let oneTwoThree = [1, 2, 3].map(initializer).reduce("", +)
  -> print(oneTwoThree)
  <- 123
  ```
-->

Se você especificar um tipo pelo nome,
pode acessar o inicializador desse tipo sem usar uma expressão de inicializador.
Em todos os outros casos, você precisa usar uma expressão de inicializador.

```swift
let s1 = SomeType.init(data: 3)  // Valid
let s2 = SomeType(data: 1)       // Also valid

let s3 = type(of: someValue).init(data: 7)  // Valid
let s4 = type(of: someValue)(data: 5)       // Error
```

<!--
  - test: `explicit-implicit-init`

  ```swifttest
  >> struct SomeType {
  >>     let data: Int
  >> }
  -> let s1 = SomeType.init(data: 3)  // Valid
  -> let s2 = SomeType(data: 1)       // Also valid

  >> let someValue = s1
  -> let s3 = type(of: someValue).init(data: 7)  // Valid
  -> let s4 = type(of: someValue)(data: 5)       // Error
  !$ error: initializing from a metatype value must reference 'init' explicitly
  !! let s4 = type(of: someValue)(data: 5)       // Error
  !!                              ^
  !!                              .init
  ```
-->

> Gramática de uma expressão de inicializador:
>
> *initializer-expression* → *postfix-expression* **`.`** **`init`** \
> *initializer-expression* → *postfix-expression* **`.`** **`init`** **`(`** *argument-names* **`)`**

### Expressão de membro explícito

Uma *expressão de membro explícito* permite acessar os membros
de um tipo nomeado, de uma tupla ou de um módulo.
Ela consiste em um ponto (`.`) entre o item
e o identificador do membro dele.

```swift
<#expression#>.<#member name#>
```

Os membros de um tipo nomeado são definidos
como parte da declaração ou da extensão do tipo.
Por exemplo:

```swift
class SomeClass {
    var someProperty = 42
}
let c = SomeClass()
let y = c.someProperty  // Member access
```

<!--
  - test: `explicitMemberExpression`

  ```swifttest
  -> class SomeClass {
         var someProperty = 42
     }
  -> let c = SomeClass()
  -> let y = c.someProperty  // Member access
  ```
-->

Os membros de uma tupla são nomeados implicitamente com inteiros,
na ordem em que aparecem, começando em zero.
Por exemplo:

```swift
var t = (10, 20, 30)
t.0 = t.1
// Now t is (20, 20, 30)
```

<!--
  - test: `explicit-member-expression`

  ```swifttest
  -> var t = (10, 20, 30)
  -> t.0 = t.1
  -> // Now t is (20, 20, 30)
  ```
-->

Os membros de um módulo acessam as declarações de nível superior desse módulo.

Tipos declarados com o atributo `dynamicMemberLookup`
incluem membros que são buscados em tempo de execução,
como descrito em <doc:Attributes>.

Para distinguir métodos ou inicializadores
cujos nomes diferem apenas pelos nomes dos seus argumentos,
inclua os nomes dos argumentos entre parênteses,
com cada nome de argumento seguido de dois-pontos (`:`).
Escreva um sublinhado (`_`) para um argumento sem nome.
Para distinguir métodos sobrecarregados, use uma anotação de tipo.
Por exemplo:

```swift
class SomeClass {
    func someMethod(x: Int, y: Int) {}
    func someMethod(x: Int, z: Int) {}
    func overloadedMethod(x: Int, y: Int) {}
    func overloadedMethod(x: Int, y: Bool) {}
}
let instance = SomeClass()

let a = instance.someMethod              // Ambiguous
let b = instance.someMethod(x:y:)        // Unambiguous

let d = instance.overloadedMethod        // Ambiguous
let d = instance.overloadedMethod(x:y:)  // Still ambiguous
let d: (Int, Bool) -> Void  = instance.overloadedMethod(x:y:)  // Unambiguous
```

<!--
  - test: `function-with-argument-names`

  ```swifttest
  -> class SomeClass {
         func someMethod(x: Int, y: Int) {}
         func someMethod(x: Int, z: Int) {}
         func overloadedMethod(x: Int, y: Int) {}
         func overloadedMethod(x: Int, y: Bool) {}
     }
  -> let instance = SomeClass()

  -> let a = instance.someMethod              // Ambiguous
  !$ error: ambiguous use of 'someMethod'
  !! let a = instance.someMethod              // Ambiguous
  !!         ^
  !$ note: found this candidate
  !!              func someMethod(x: Int, y: Int) {}
  !!                   ^
  !$ note: found this candidate
  !!              func someMethod(x: Int, z: Int) {}
  !!                   ^
  -> let b = instance.someMethod(x:y:)        // Unambiguous

  -> let d = instance.overloadedMethod        // Ambiguous
  !$ error: ambiguous use of 'overloadedMethod(x:y:)'
  !! let d = instance.overloadedMethod        // Ambiguous
  !!         ^
  !$ note: found this candidate
  !!              func overloadedMethod(x: Int, y: Int) {}
  !!                   ^
  !$ note: found this candidate
  !!              func overloadedMethod(x: Int, y: Bool) {}
  !!                   ^
  -> let d = instance.overloadedMethod(x:y:)  // Still ambiguous
  !$ error: ambiguous use of 'overloadedMethod(x:y:)'
  !!     let d = instance.overloadedMethod(x:y:)  // Still ambiguous
  !!             ^
  !$ note: found this candidate
  !!              func overloadedMethod(x: Int, y: Int) {}
  !!                   ^
  !$ note: found this candidate
  !!              func overloadedMethod(x: Int, y: Bool) {}
  !!                   ^
  -> let d: (Int, Bool) -> Void  = instance.overloadedMethod(x:y:)  // Unambiguous
  ```
-->

Se um ponto aparecer no início de uma linha,
ele é entendido como parte de uma expressão de membro explícito,
e não de uma expressão de membro implícito.
Por exemplo, a listagem a seguir mostra chamadas de método encadeadas
divididas em várias linhas:

```swift
let x = [10, 3, 20, 15, 4]
    .sorted()
    .filter { $0 > 5 }
    .map { $0 * 100 }
```

<!--
  - test: `period-at-start-of-line`

  ```swifttest
  -> let x = [10, 3, 20, 15, 4]
  ->     .sorted()
  ->     .filter { $0 > 5 }
  ->     .map { $0 * 100 }
  >> print(x)
  << [1000, 1500, 2000]
  ```
-->

Você pode combinar essa sintaxe encadeada em várias linhas
com diretivas de controle de compilação
para controlar quando cada método é chamado.
Por exemplo,
o código a seguir usa uma regra de filtragem diferente no iOS:

```swift
let numbers = [10, 20, 33, 43, 50]
#if os(iOS)
    .filter { $0 < 40 }
#else
    .filter { $0 > 25 }
#endif
```

<!--
  - test: `pound-if-inside-postfix-expression`

  ```swifttest
  -> let numbers = [10, 20, 33, 43, 50]
     #if os(iOS)
         .filter { $0 < 40 }
     #else
         .filter { $0 > 25 }
     #endif
  >> print(numbers)
  << [33, 43, 50]
  ```
-->

Entre `#if`, `#endif` e outras diretivas de compilação,
o bloco de compilação condicional pode conter
uma expressão de membro implícito
seguida de zero ou mais pós-fixos,
para formar uma expressão pós-fixa.
Ele também pode conter
outro bloco de compilação condicional,
ou uma combinação dessas expressões e blocos.

Você pode usar essa sintaxe em qualquer lugar em que pode escrever
uma expressão de membro explícito,
e não apenas em código de nível superior.

No bloco de compilação condicional,
o ramo da diretiva `#if` precisa conter pelo menos uma expressão.
Os outros ramos podem ser vazios.

<!--
  - test: `pound-if-empty-if-not-allowed`

  ```swifttest
  >> let numbers = [10, 20, 33, 43, 50]
  >> #if os(iOS)
  >> #else
  >>     .filter { $0 > 25 }
  >> #endif
  !$ error: reference to member 'filter' cannot be resolved without a contextual type
  !! .filter { $0 > 25 }
  !! ~^~~~~~
  ```
-->

<!--
  - test: `pound-if-else-can-be-empty`

  ```swifttest
  >> let numbers = [10, 20, 33, 43, 50]
  >> #if os(iOS)
  >>     .filter { $0 > 25 }
  >> #else
  >> #endif
  >> print(numbers)
  << [10, 20, 33, 43, 50]
  ```
-->

<!--
  - test: `pound-if-cant-use-binary-operators`

  ```swifttest
  >> let s = "some string"
  >> #if os(iOS)
  >>     + " on iOS"
  >> #endif
  !$ error: unary operator cannot be separated from its operand
  !! + " on iOS"
  !! ^~
  !!-
  ```
-->

> Gramática de uma expressão de membro explícito:
>
> *explicit-member-expression* → *postfix-expression* **`.`** *decimal-digits* \
> *explicit-member-expression* → *postfix-expression* **`.`** *identifier* *generic-argument-clause*_?_ \
> *explicit-member-expression* → *postfix-expression* **`.`** *identifier* **`(`** *argument-names* **`)`** \
> *explicit-member-expression* → *postfix-expression* *conditional-compilation-block*
>
> *argument-names* → *argument-name* *argument-names*_?_ \
> *argument-name* → *identifier* **`:`**

<!--
  The grammar for method-name doesn't include the following:
      method-name -> identifier argument-names-OPT
  because the "postfix-expression . identifier" line above already covers that case.
-->

<!--
  See grammar for initializer-expression for the related "argument name" production there.
-->

### Expressão self pós-fixa

Uma expressão `self` pós-fixa consiste em uma expressão ou no nome de um tipo,
seguido imediatamente de `.self`.
Ela tem as seguintes formas:

```swift
<#expression#>.self
<#type#>.self
```

A primeira forma avalia para o valor da *expressão*.
Por exemplo, `x.self` avalia para `x`.

A segunda forma avalia para o valor do *tipo*.
Use essa forma para acessar um tipo como valor.
Por exemplo, como `SomeClass.self` avalia para o próprio tipo `SomeClass`,
você pode passá-lo a uma função ou método que aceita um argumento de nível de tipo.

> Gramática de uma expressão self pós-fixa:
>
> *postfix-self-expression* → *postfix-expression* **`.`** **`self`**

### Expressão de subscript

Uma *expressão de subscript* fornece acesso por subscript
usando o getter e o setter da declaração de subscript correspondente.
Ela tem a seguinte forma:

```swift
<#expression#>[<#index expressions#>]
```

Para avaliar o valor de uma expressão de subscript,
o getter de subscript para o tipo da *expressão* é chamado
com as *expressões de índice* passadas como parâmetros do subscript.
Para definir o valor dela,
o setter de subscript é chamado da mesma forma.

<!--
  TR: Confirm that indexing on
  a comma-separated list of expressions
  is intentional, not just a side effect.
  I see this working, for example:
  (swift) class Test {
            subscript(a: Int, b: Int) -> Int { return 12 }
          }
  (swift) var t = Test()
  // t : Test = <Test instance>
  (swift) t[1, 2]
  // r0 : Int = 12
-->

Para informações sobre declarações de subscript,
veja <doc:Declarations#Protocol-Subscript-Declaration>.

> Gramática de uma expressão de subscript:
>
> *subscript-expression* → *postfix-expression* **`[`** *function-call-argument-list* **`]`**

<!--
  - test: `subscripts-can-take-operators`

  ```swifttest
  >> struct S {
         let x: Int
         let y: Int
         subscript(operation: (Int, Int) -> Int) -> Int {
             return operation(x, y)
         }
     }
  >> let s = S(x: 10, y: 20)
  >> assert(s[+] == 30)
  ```
-->

### Expressão de valor forçado

Uma *expressão de valor forçado* desembrulha um valor optional
que você tem certeza de que não é `nil`.
Ela tem a seguinte forma:

```swift
<#expression#>!
```

Se o valor da *expressão* não for `nil`,
o valor optional é desembrulhado e retornado com o tipo não opcional correspondente.
Caso contrário, um erro de tempo de execução é gerado.

O valor desembrulhado de uma expressão de valor forçado pode ser modificado,
seja mutando o próprio valor,
seja atribuindo a um dos membros do valor.
Por exemplo:

```swift
var x: Int? = 0
x! += 1
// x is now 1

var someDictionary = ["a": [1, 2, 3], "b": [10, 20]]
someDictionary["a"]![0] = 100
// someDictionary is now ["a": [100, 2, 3], "b": [10, 20]]
```

<!--
  - test: `optional-as-lvalue`

  ```swifttest
  -> var x: Int? = 0
  -> x! += 1
  /> x is now \(x!)
  </ x is now 1

  -> var someDictionary = ["a": [1, 2, 3], "b": [10, 20]]
  -> someDictionary["a"]![0] = 100
  /> someDictionary is now \(someDictionary)
  </ someDictionary is now ["a": [100, 2, 3], "b": [10, 20]]
  ```
-->

> Gramática de uma expressão de valor forçado:
>
> *forced-value-expression* → *postfix-expression* **`!`**

### Expressão de optional chaining

Uma *expressão de optional chaining* oferece uma sintaxe simplificada
para usar valores opcionais em expressões pós-fixas.
Ela tem a seguinte forma:

```swift
<#expression#>?
```

O operador pós-fixo `?` cria uma expressão de optional chaining
a partir de uma expressão, sem mudar o valor dessa expressão.

Expressões de optional chaining precisam aparecer dentro de uma expressão pós-fixa,
e elas fazem a expressão pós-fixa ser avaliada de forma especial.
Se o valor da expressão de optional chaining for `nil`,
todas as outras operações na expressão pós-fixa são ignoradas
e a expressão pós-fixa inteira avalia para `nil`.
Se o valor da expressão de optional chaining não for `nil`,
o valor dela é desembrulhado e usado para avaliar o restante da expressão pós-fixa.
Em ambos os casos,
o valor da expressão pós-fixa continua sendo de um tipo optional.

Se uma expressão pós-fixa que contém uma expressão de optional chaining
estiver aninhada dentro de outras expressões pós-fixas,
somente a expressão mais externa retorna um tipo optional.
No exemplo abaixo,
quando `c` não é `nil`,
o valor dele é desembrulhado e usado para avaliar `.property`,
cujo valor é usado para avaliar `.performAction()`.
A expressão inteira `c?.property.performAction()`
tem um valor de tipo optional.

```swift
var c: SomeClass?
var result: Bool? = c?.property.performAction()
```

<!--
  - test: `optional-chaining`

  ```swifttest
  >> class OtherClass { func performAction() -> Bool {return true} }
  >> class SomeClass { var property: OtherClass = OtherClass() }
  -> var c: SomeClass?
  -> var result: Bool? = c?.property.performAction()
  >> assert(result == nil)
  ```
-->

O exemplo a seguir mostra o comportamento do exemplo acima
sem usar optional chaining.

```swift
var result: Bool?
if let unwrappedC = c {
    result = unwrappedC.property.performAction()
}
```

<!--
  - test: `optional-chaining-alt`

  ```swifttest
  >> class OtherClass { func performAction() -> Bool {return true} }
  >> class SomeClass { var property: OtherClass = OtherClass() }
  >> var c: SomeClass?
  -> var result: Bool?
  -> if let unwrappedC = c {
        result = unwrappedC.property.performAction()
     }
  ```
-->

O valor desembrulhado de uma expressão de optional chaining pode ser modificado,
seja mutando o próprio valor,
seja atribuindo a um dos membros do valor.
Se o valor da expressão de optional chaining for `nil`,
a expressão do lado direito do operador de atribuição não é avaliada.
Por exemplo:

```swift
func someFunctionWithSideEffects() -> Int {
    return 42  // No actual side effects.
}
var someDictionary = ["a": [1, 2, 3], "b": [10, 20]]

someDictionary["not here"]?[0] = someFunctionWithSideEffects()
// someFunctionWithSideEffects isn't evaluated
// someDictionary is still ["a": [1, 2, 3], "b": [10, 20]]

someDictionary["a"]?[0] = someFunctionWithSideEffects()
// someFunctionWithSideEffects is evaluated and returns 42
// someDictionary is now ["a": [42, 2, 3], "b": [10, 20]]
```

<!--
  - test: `optional-chaining-as-lvalue`

  ```swifttest
  -> func someFunctionWithSideEffects() -> Int {
        return 42  // No actual side effects.
     }
  -> var someDictionary = ["a": [1, 2, 3], "b": [10, 20]]

  -> someDictionary["not here"]?[0] = someFunctionWithSideEffects()
  // someFunctionWithSideEffects isn't evaluated
  /> someDictionary is still \(someDictionary)
  </ someDictionary is still ["a": [1, 2, 3], "b": [10, 20]]

  -> someDictionary["a"]?[0] = someFunctionWithSideEffects()
  /> someFunctionWithSideEffects is evaluated and returns \(someFunctionWithSideEffects())
  </ someFunctionWithSideEffects is evaluated and returns 42
  /> someDictionary is now \(someDictionary)
  </ someDictionary is now ["a": [42, 2, 3], "b": [10, 20]]
  ```
-->

> Gramática de uma expressão de optional chaining:
>
> *optional-chaining-expression* → *postfix-expression* **`?`**

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->

<!-- ia-translate: true -->
