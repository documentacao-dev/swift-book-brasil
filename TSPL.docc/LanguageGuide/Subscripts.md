# Subscripts

Acesse os elementos de uma coleção.

Classes, structs e enumerações podem definir *subscripts*,
que são atalhos para acessar os elementos membros de uma coleção, lista ou sequência.
Você usa subscripts para ler e gravar valores por índice, sem precisar
de métodos separados para leitura e escrita.
Por exemplo, você acessa os elementos de uma instância de `Array` como `someArray[index]`
e os elementos de uma instância de `Dictionary` como `someDictionary[key]`.

Você pode definir vários subscripts para um mesmo tipo,
e o subscript adequado é escolhido
com base no tipo do valor de índice que você passa para ele.
Subscripts não se limitam a uma única dimensão,
e você pode definir subscripts com vários parâmetros de entrada
para atender às necessidades do seu tipo personalizado.

<!--
  TODO: this chapter should provide an example of subscripting an enumeration,
  as per Joe Groff's example from rdar://16555559.
-->

## Sintaxe de subscript

Subscripts permitem consultar instâncias de um tipo
escrevendo um ou mais valores entre colchetes depois do nome da instância.
A sintaxe é semelhante tanto à de métodos de instância quanto à de propriedades computadas.
Você escreve definições de subscript com a palavra-chave `subscript`
e especifica um ou mais parâmetros de entrada e um tipo de retorno,
da mesma forma que em métodos de instância.
Diferente dos métodos de instância, subscripts podem ser de leitura e escrita ou somente de leitura.
Esse comportamento é definido por um getter e um setter,
da mesma forma que nas propriedades computadas:

```swift
subscript(index: Int) -> Int {
    get {
        // Return an appropriate subscript value here.
    }
    set(newValue) {
        // Perform a suitable setting action here.
    }
}
```

<!--
  - test: `subscriptSyntax`

  ```swifttest
  >> class Test1 {
  -> subscript(index: Int) -> Int {
        get {
           // Return an appropriate subscript value here.
  >>       return 1
        }
        set(newValue) {
           // Perform a suitable setting action here.
        }
     }
  >> }
  ```
-->

O tipo de `newValue` é o mesmo do valor de retorno do subscript.
Assim como nas propriedades computadas, você pode optar por não especificar
o parâmetro `(newValue)` do setter.
Se você não fornecer um, o setter recebe automaticamente um parâmetro padrão chamado `newValue`.

Assim como nas propriedades computadas somente de leitura,
você pode simplificar a declaração de um subscript somente de leitura
removendo a palavra-chave `get` e suas chaves:

```swift
subscript(index: Int) -> Int {
    // Return an appropriate subscript value here.
}
```

<!--
  - test: `subscriptSyntax`

  ```swifttest
  >> class Test2 {
  -> subscript(index: Int) -> Int {
        // Return an appropriate subscript value here.
  >>    return 1
     }
  >> }
  ```
-->

Veja um exemplo de implementação de subscript somente de leitura,
que define uma struct `TimesTable` para representar uma tabela de multiplicação de *n* de inteiros:

```swift
struct TimesTable {
    let multiplier: Int
    subscript(index: Int) -> Int {
        return multiplier * index
    }
}
let threeTimesTable = TimesTable(multiplier: 3)
print("six times three is \(threeTimesTable[6])")
// Prints "six times three is 18".
```

<!--
  - test: `timesTable`

  ```swifttest
  -> struct TimesTable {
        let multiplier: Int
        subscript(index: Int) -> Int {
           return multiplier * index
        }
     }
  -> let threeTimesTable = TimesTable(multiplier: 3)
  -> print("six times three is \(threeTimesTable[6])")
  <- six times three is 18
  ```
-->

Neste exemplo, uma nova instância de `TimesTable` é criada
para representar a tabela do três.
Isso é indicado ao passar o valor `3` para o `initializer` da struct,
como valor a ser usado no parâmetro `multiplier` da instância.

Você pode consultar a instância `threeTimesTable` chamando o subscript dela,
como mostrado na chamada `threeTimesTable[6]`.
Isso pede a sexta entrada da tabela do três,
que retorna o valor `18`, ou seja, `3` vezes `6`.

> Nota: Uma tabela de multiplicação de *n* é baseada em uma regra matemática fixa.
> Não faz sentido definir `threeTimesTable[someIndex]` com um novo valor,
> por isso o subscript de `TimesTable` é definido como somente de leitura.

## Uso de subscripts

O significado exato de “subscript” depende do contexto em que ele é usado.
Subscripts costumam ser usados como atalho para acessar
os elementos membros de uma coleção, lista ou sequência.
Você é livre para implementar subscripts da forma que for mais adequada
à funcionalidade da sua classe ou struct.

Por exemplo, o tipo `Dictionary` do Swift implementa um subscript
para gravar e ler os valores armazenados em uma instância de `Dictionary`.
Você pode definir um valor em um dicionário
passando uma chave do tipo de chave do dicionário entre colchetes do subscript
e atribuindo ao subscript um valor do tipo de valor do dicionário:

```swift
var numberOfLegs = ["spider": 8, "ant": 6, "cat": 4]
numberOfLegs["bird"] = 2
```

<!--
  - test: `dictionarySubscript`

  ```swifttest
  -> var numberOfLegs = ["spider": 8, "ant": 6, "cat": 4]
  -> numberOfLegs["bird"] = 2
  ```
-->

O exemplo acima define uma variável chamada `numberOfLegs`
e a inicializa com um dictionary literal que contém três pares chave-valor.
O tipo do dicionário `numberOfLegs` é inferido como `[String: Int]`.
Depois de criar o dicionário,
o exemplo usa uma atribuição por subscript para adicionar
a chave `String` `"bird"` e o valor `Int` `2` ao dicionário.

Para mais informações sobre o subscript de `Dictionary`,
veja <doc:CollectionTypes#Accessing-and-Modifying-a-Dictionary>.

> Nota: O tipo `Dictionary` do Swift implementa seu subscript de chave-valor
> como um subscript que recebe e retorna um tipo *optional*.
> Para o dicionário `numberOfLegs` acima,
> o subscript de chave-valor recebe e retorna um valor do tipo `Int?`,
> ou “`Int` optional”.
> O tipo `Dictionary` usa um tipo optional no subscript para modelar o fato de que
> nem toda chave terá um valor, e para oferecer uma forma de remover o valor de uma chave
> atribuindo a ela o valor `nil`.

## Opções de subscript

Subscripts podem receber qualquer número de parâmetros de entrada,
e esses parâmetros podem ser de qualquer tipo.
Subscripts também podem retornar um valor de qualquer tipo.

Assim como as funções,
subscripts podem receber um número variável de parâmetros
e fornecer valores padrão para os parâmetros,
como discutido em <doc:Functions#Variadic-Parameters>
e <doc:Functions#Default-Parameter-Values>.
No entanto, diferente das funções,
subscripts não podem usar parâmetros in-out.

<!--
  - test: `subscripts-can-have-default-arguments`

  ```swifttest
  >> struct Subscriptable {
  >>     subscript(x: Int, y: Int = 0) -> Int {
  >>         return 100
  >>     }
  >> }
  >> let s = Subscriptable()
  >> print(s[0])
  << 100
  ```
-->

Uma classe ou struct pode fornecer quantas implementações de subscript forem necessárias,
e o subscript adequado a ser usado é inferido
pelos tipos do valor ou valores que estão entre os colchetes
no momento em que o subscript é usado.
Essa definição de vários subscripts é conhecida como *sobrecarga de subscript*.

Embora seja mais comum um subscript receber um único parâmetro,
você também pode definir um subscript com vários parâmetros
se isso fizer sentido para o seu tipo.
O exemplo a seguir define uma struct `Matrix`,
que representa uma matriz bidimensional de valores `Double`.
O subscript da struct `Matrix` recebe dois parâmetros inteiros:

```swift
struct Matrix {
    let rows: Int, columns: Int
    var grid: [Double]
    init(rows: Int, columns: Int) {
        self.rows = rows
        self.columns = columns
        grid = Array(repeating: 0.0, count: rows * columns)
    }
    func indexIsValid(row: Int, column: Int) -> Bool {
        return row >= 0 && row < rows && column >= 0 && column < columns
    }
    subscript(row: Int, column: Int) -> Double {
        get {
            assert(indexIsValid(row: row, column: column), "Index out of range")
            return grid[(row * columns) + column]
        }
        set {
            assert(indexIsValid(row: row, column: column), "Index out of range")
            grid[(row * columns) + column] = newValue
        }
    }
}
```

<!--
  - test: `matrixSubscript, matrixSubscriptAssert`

  ```swifttest
  -> struct Matrix {
        let rows: Int, columns: Int
        var grid: [Double]
        init(rows: Int, columns: Int) {
           self.rows = rows
           self.columns = columns
           grid = Array(repeating: 0.0, count: rows * columns)
        }
        func indexIsValid(row: Int, column: Int) -> Bool {
           return row >= 0 && row < rows && column >= 0 && column < columns
        }
        subscript(row: Int, column: Int) -> Double {
           get {
              assert(indexIsValid(row: row, column: column), "Index out of range")
              return grid[(row * columns) + column]
           }
           set {
              assert(indexIsValid(row: row, column: column), "Index out of range")
              grid[(row * columns) + column] = newValue
           }
        }
     }
  ```
-->

`Matrix` fornece um inicializador que recebe dois parâmetros chamados `rows` e `columns`,
e cria um array grande o bastante para guardar `rows * columns` valores do tipo `Double`.
Cada posição da matriz recebe o valor inicial `0.0`.
Para isso, o tamanho do array e o valor inicial de cada célula, `0.0`,
são passados a um inicializador de array que cria e inicializa um novo array do tamanho correto.
Esse inicializador é descrito com mais detalhes
em <doc:CollectionTypes#Creating-an-Array-with-a-Default-Value>.

Você pode criar uma nova instância de `Matrix` passando
a quantidade adequada de linhas e colunas para o inicializador:

```swift
var matrix = Matrix(rows: 2, columns: 2)
```

<!--
  - test: `matrixSubscript, matrixSubscriptAssert`

  ```swifttest
  -> var matrix = Matrix(rows: 2, columns: 2)
  >> assert(matrix.grid == [0.0, 0.0, 0.0, 0.0])
  ```
-->

O exemplo acima cria uma nova instância de `Matrix` com duas linhas e duas colunas.
O array `grid` dessa instância de `Matrix`
é, na prática, uma versão achatada da matriz,
lida do canto superior esquerdo até o canto inferior direito:

![](subscriptMatrix01)

Os valores da matriz podem ser definidos passando os valores de linha e coluna para o subscript,
separados por vírgula:

```swift
matrix[0, 1] = 1.5
matrix[1, 0] = 3.2
```

<!--
  - test: `matrixSubscript, matrixSubscriptAssert`

  ```swifttest
  -> matrix[0, 1] = 1.5
  >> print(matrix[0, 1])
  << 1.5
  -> matrix[1, 0] = 3.2
  >> print(matrix[1, 0])
  << 3.2
  ```
-->

Essas duas instruções chamam o setter do subscript para definir
o valor `1.5` na posição superior direita da matriz
(onde `row` é `0` e `column` é `1`),
e `3.2` na posição inferior esquerda
(onde `row` é `1` e `column` é `0`):

![](subscriptMatrix02)

O getter e o setter do subscript de `Matrix` contêm, ambos, uma asserção
para verificar se os valores de `row` e `column` do subscript são válidos.
Para ajudar nessas asserções,
`Matrix` inclui um método de conveniência chamado `indexIsValid(row:column:)`,
que verifica se a `row` e a `column` pedidas
estão dentro dos limites da matriz:

```swift
func indexIsValid(row: Int, column: Int) -> Bool {
    return row >= 0 && row < rows && column >= 0 && column < columns
}
```

<!--
  - test: `matrixSubscript`

  ```swifttest
  >> var rows = 2
  >> var columns = 2
  -> func indexIsValid(row: Int, column: Int) -> Bool {
        return row >= 0 && row < rows && column >= 0 && column < columns
     }
  ```
-->

Uma asserção é disparada se você tentar acessar um subscript
que esteja fora dos limites da matriz:

```swift
let someValue = matrix[2, 2]
// This triggers an assert, because [2, 2] is outside of the matrix bounds.
```

<!--
  - test: `matrixSubscriptAssert`

  ```swifttest
  -> let someValue = matrix[2, 2]
  xx assert
  // This triggers an assert, because [2, 2] is outside of the matrix bounds.
  ```
-->

## Subscripts de tipo

Subscripts de instância, como descritos acima,
são subscripts que você chama em uma instância de um tipo específico.
Você também pode definir subscripts que são chamados no próprio tipo.
Esse tipo de subscript é chamado de *subscript de tipo*.
Você indica um subscript de tipo
escrevendo a palavra-chave `static` antes da palavra-chave `subscript`.
Classes podem usar a palavra-chave `class` no lugar,
para permitir que subclasses sobrescrevam a implementação desse subscript da superclasse.
O exemplo abaixo mostra como você define e chama um subscript de tipo:

```swift
enum Planet: Int {
    case mercury = 1, venus, earth, mars, jupiter, saturn, uranus, neptune
    static subscript(n: Int) -> Planet {
        return Planet(rawValue: n)!
    }
}
let mars = Planet[4]
print(mars)
```

<!--
  - test: `static-subscript`

  ```swifttest
  -> enum Planet: Int {
        case mercury = 1, venus, earth, mars, jupiter, saturn, uranus, neptune
        static subscript(n: Int) -> Planet {
           return Planet(rawValue: n)!
        }
     }
  -> let mars = Planet[4]
  >> assert(mars == Planet.mars)
  -> print(mars)
  << mars
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
