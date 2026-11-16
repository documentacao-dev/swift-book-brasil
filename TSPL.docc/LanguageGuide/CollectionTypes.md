# Tipos de coleção

Organize dados usando arrays, conjuntos e dicionários.

Swift oferece três *tipos de coleção* principais, conhecidos como arrays, conjuntos e dicionários, para armazenar coleções de valores.
Arrays são coleções ordenadas de valores.
Conjuntos são coleções não ordenadas de valores únicos.
Dicionários são coleções não ordenadas de associações entre chave e valor.

![](CollectionTypes_intro)

Arrays, conjuntos e dicionários em Swift sempre deixam claro o tipo dos valores e das chaves que podem armazenar.
Isso significa que você não consegue inserir, por engano, um valor do tipo errado em uma coleção.
Também significa que você pode ter certeza do tipo dos valores que vai recuperar de uma coleção.

> Nota: Os tipos array, Set e Dictionary do Swift são implementados como *coleções genéricas*.
> Para saber mais sobre tipos e coleções genéricos, consulte <doc:Generics>.

<!--
  TODO: should I mention the Collection protocol, to which both of these conform?
-->

<!--
  TODO: mention for i in indices(collection) { collection[i] }
-->

<!--
  TODO: discuss collection equality
-->

## Mutabilidade das Coleções

Se você criar um array, um conjunto ou um dicionário e atribuí-lo a uma variável, a coleção criada será *mutável*.
Isso significa que você pode alterar (ou *mutar*) a coleção depois de criada, adicionando, removendo ou trocando itens na coleção.
Se você atribuir um array, um conjunto ou um dicionário a uma constante, essa coleção será *imutável*, e seu tamanho e conteúdo não poderão ser alterados.

> Nota: É uma boa prática criar coleções imutáveis em todos os casos em que a coleção não precisa mudar.
> Fazer isso facilita o raciocínio sobre o seu código e permite que o compilador do Swift otimize o desempenho das coleções que você cria.

## Arrays

Um *array* armazena valores do mesmo tipo em uma lista ordenada.
O mesmo valor pode aparecer em um array várias vezes, em posições diferentes.

> Nota: O tipo `Array` do Swift tem ponte com a classe `NSArray` do Foundation.
>
> Para mais informações sobre como usar `Array` com Foundation e Cocoa, consulte [Ponte entre Array e NSArray](https://developer.apple.com/documentation/swift/array#Bridging-Between-Array-and-NSArray).

### Sintaxe Abreviada do Tipo Array

O tipo de um array do Swift é escrito por extenso como `Array<Element>`, em que `Element` é o tipo de valores que o array pode armazenar.
Você também pode escrever o tipo de um array em forma abreviada, como `[Element]`.
Embora as duas formas sejam funcionalmente idênticas, a forma abreviada é preferida e é usada ao longo deste guia ao se referir ao tipo de um array.

### Criando um Array Vazio

Você pode criar um array vazio no Swift usando duas abordagens.
Se o contexto já fornecer informação de tipo, como um argumento de função ou uma variável ou constante já tipada, você pode usar um literal de array vazio, que é escrito como `[]` (um par vazio de colchetes):

```swift
var someInts: [Int] = []
print("someInts is of type [Int] with \(someInts.count) items.")
// Prints "someInts is of type [Int] with 0 items."
```

<!--
  - test: `arraysEmpty`

  ```swifttest
  -> var someInts: [Int] = []
  -> print("someInts is of type [Int] with \(someInts.count) items.")
  <- someInts is of type [Int] with 0 items.
  ```
-->

Alternativamente, você pode criar um array vazio de determinado tipo usando a sintaxe explícita de inicializador, escrevendo o tipo do elemento entre colchetes seguido de parênteses, por exemplo, `[Int]()` no exemplo a seguir:

```swift
var someInts = [Int]()
print("someInts is of type [Int] with \(someInts.count) items.")
// Prints "someInts is of type [Int] with 0 items."
```

Ambas as abordagens produzem o mesmo resultado.
No entanto, um literal de array vazio é mais curto e geralmente mais fácil de ler.

Nos dois casos, você pode usar o literal de array vazio (`[]`) para atribuir novamente um array vazio a uma variável existente:

```swift
someInts.append(3)
// someInts now contains 1 value of type Int
someInts = []
// someInts is now an empty array, but is still of type [Int]
```

<!--
  - test: `arraysEmpty`

  ```swifttest
  -> someInts.append(3)
  /> someInts now contains \(someInts.count) value of type Int
  </ someInts now contains 1 value of type Int
  -> someInts = []
  // someInts is now an empty array, but is still of type [Int]
  ```
-->

### Criando um Array com um Valor Padrão

O tipo `Array` do Swift também oferece um inicializador para criar um array de determinado tamanho com todos os seus valores definidos como o mesmo valor padrão.
Você passa a esse inicializador um valor padrão do tipo apropriado (o rótulo `repeating`) e o número de vezes que esse valor se repete no novo array (o rótulo `count`):

```swift
var threeDoubles = Array(repeating: 0.0, count: 3)
// threeDoubles is of type [Double], and equals [0.0, 0.0, 0.0]
```

<!--
  - test: `arraysEmpty`

  ```swifttest
  -> var threeDoubles = Array(repeating: 0.0, count: 3)
  /> threeDoubles is of type [Double], and equals [\(threeDoubles[0]), \(threeDoubles[1]), \(threeDoubles[2])]
  </ threeDoubles is of type [Double], and equals [0.0, 0.0, 0.0]
  ```
-->

### Criando um Array Somando Dois Arrays

Você pode criar um novo array somando dois arrays existentes com tipos compatíveis usando o operador de adição (`+`).
O tipo do novo array é inferido a partir do tipo dos dois arrays somados:

```swift
var anotherThreeDoubles = Array(repeating: 2.5, count: 3)
// anotherThreeDoubles is of type [Double], and equals [2.5, 2.5, 2.5]

var sixDoubles = threeDoubles + anotherThreeDoubles
// sixDoubles is inferred as [Double], and equals [0.0, 0.0, 0.0, 2.5, 2.5, 2.5]
```

<!--
  - test: `arraysEmpty`

  ```swifttest
  -> var anotherThreeDoubles = Array(repeating: 2.5, count: 3)
  /> anotherThreeDoubles is of type [Double], and equals [\(anotherThreeDoubles[0]), \(anotherThreeDoubles[1]), \(anotherThreeDoubles[2])]
  </ anotherThreeDoubles is of type [Double], and equals [2.5, 2.5, 2.5]

  -> var sixDoubles = threeDoubles + anotherThreeDoubles
  /> sixDoubles is inferred as [Double], and equals \(sixDoubles)
  </ sixDoubles is inferred as [Double], and equals [0.0, 0.0, 0.0, 2.5, 2.5, 2.5]
  ```
-->

<!--
  TODO: func find<T: Equatable>(array: [T], value: T) -> Int?
  This is defined in Algorithm.swift,
  and gives a way to find the index of a value in an array if it exists.
  I'm holding off writing about it until NewArray lands.
-->

<!--
  TODO: mutating func sort(by: (T, T) -> Bool)
  This is defined in Array.swift.
  Likewise I'm holding off writing about it until NewArray lands.
-->

### Criando um Array com um Literal de Array

Você também pode inicializar um array com um *literal de array*, que é uma forma abreviada de escrever um ou mais valores como uma coleção do tipo array.
Um literal de array é escrito como uma lista de valores, separados por vírgulas e envoltos por um par de colchetes:

```swift
[<#value 1#>, <#value 2#>, <#value 3#>]
```

O exemplo abaixo cria um array chamado `shoppingList` para armazenar valores `String`:

```swift
var shoppingList: [String] = ["Eggs", "Milk"]
// shoppingList has been initialized with two initial items
```

<!--
  - test: `arrays`

  ```swifttest
  -> var shoppingList: [String] = ["Eggs", "Milk"]
  // shoppingList has been initialized with two initial items
  ```
-->

A variável `shoppingList` é declarada como “um array de valores string”, escrito como `[String]`.
Como esse array em particular especificou um tipo de valor `String`, ele só pode armazenar valores `String`.
Aqui, o array `shoppingList` é inicializado com dois valores `String` (`"Eggs"` e `"Milk"`), escritos dentro de um literal de array.

> Nota: A variável `shoppingList` é declarada como variável (com a palavra-chave `var`) e não como constante (com a palavra-chave `let`),
> porque mais itens são adicionados à lista de compras nos exemplos a seguir.

Nesse caso, o literal de array contém dois valores `String` e nada mais.
Isso corresponde ao tipo da declaração da variável `shoppingList` (um array que só pode conter valores `String`), e por isso a atribuição do literal de array é permitida como forma de inicializar `shoppingList` com dois itens iniciais.

Graças à inferência de tipos do Swift, você não precisa escrever o tipo do array se estiver inicializando-o com um literal de array que contém valores do mesmo tipo.
A inicialização de `shoppingList` poderia ter sido escrita de forma mais curta:

```swift
var shoppingList = ["Eggs", "Milk"]
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> var shoppingList = ["Eggs", "Milk"]
  ```
-->

Como todos os valores no literal de array são do mesmo tipo, o Swift pode inferir que `[String]` é o tipo correto para a variável `shoppingList`.

Você pode incluir uma vírgula depois do último valor em um literal de array, que é conhecida como *vírgula final*:

```swift
var shoppingList = [
    "Eggs",
    "Milk",
]
```

Como a vírgula final faz com que todas as linhas terminem da mesma forma, ela é uma forma útil de escrever arrays como o acima, que têm um valor por linha.
Ao alterar o array, você só precisa adicionar, remover ou reordenar valores; não precisa adicionar nem remover vírgulas.

### Acessando e Modificando um Array

Você acessa e modifica um array por meio de seus métodos e propriedades, ou usando a sintaxe de *subscript*.

Para descobrir o número de itens em um array, consulte a propriedade somente leitura `count`:

```swift
print("The shopping list contains \(shoppingList.count) items.")
// Prints "The shopping list contains 2 items."
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> print("The shopping list contains \(shoppingList.count) items.")
  <- The shopping list contains 2 items.
  ```
-->

Use a propriedade booleana `isEmpty` como atalho para verificar se a propriedade `count` é igual a `0`:

```swift
if shoppingList.isEmpty {
    print("The shopping list is empty.")
} else {
    print("The shopping list isn't empty.")
}
// Prints "The shopping list isn't empty."
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> if shoppingList.isEmpty {
        print("The shopping list is empty.")
     } else {
        print("The shopping list isn't empty.")
     }
  <- The shopping list isn't empty.
  ```
-->

Você pode adicionar um novo item ao final de um array chamando o método `append(_:)` do array:

```swift
shoppingList.append("Flour")
// shoppingList now contains 3 items, and someone is making pancakes
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> shoppingList.append("Flour")
  /> shoppingList now contains \(shoppingList.count) items, and someone is making pancakes
  </ shoppingList now contains 3 items, and someone is making pancakes
  ```
-->

Alternativamente, anexe um array de um ou mais itens compatíveis com o operador de atribuição por adição (`+=`):

```swift
shoppingList += ["Baking Powder"]
// shoppingList now contains 4 items
shoppingList += ["Chocolate Spread", "Cheese", "Butter"]
// shoppingList now contains 7 items
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> shoppingList += ["Baking Powder"]
  /> shoppingList now contains \(shoppingList.count) items
  </ shoppingList now contains 4 items
  -> shoppingList += ["Chocolate Spread", "Cheese", "Butter"]
  /> shoppingList now contains \(shoppingList.count) items
  </ shoppingList now contains 7 items
  ```
-->

Recupere um valor do array usando *sintaxe de subscript*, passando o índice do valor que você quer recuperar entre colchetes, logo após o nome do array:

```swift
var firstItem = shoppingList[0]
// firstItem is equal to "Eggs"
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> var firstItem = shoppingList[0]
  /> firstItem is equal to \"\(firstItem)\"
  </ firstItem is equal to "Eggs"
  ```
-->

> Nota: O primeiro item do array tem índice `0`, não `1`.
> Arrays no Swift sempre são indexados a partir de zero.

Você pode usar a sintaxe de subscript para alterar um valor existente em determinado índice:

```swift
shoppingList[0] = "Six eggs"
// the first item in the list is now equal to "Six eggs" rather than "Eggs"
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> shoppingList[0] = "Six eggs"
  /> the first item in the list is now equal to \"\(shoppingList[0])\" rather than \"Eggs\"
  </ the first item in the list is now equal to "Six eggs" rather than "Eggs"
  ```
-->

Ao usar a sintaxe de subscript, o índice especificado precisa ser válido.
Por exemplo, escrever `shoppingList[shoppingList.count] = "Salt"` para tentar adicionar um item ao final do array resulta em um erro em tempo de execução.

<!--
  Unlike Ruby and Javascript, where accessing an invalid index
  extends the array with nil or similar placeholder values,
  to make that index become valid.
-->

Você também pode usar a sintaxe de subscript para alterar um intervalo de valores de uma só vez, mesmo que o conjunto de valores de substituição tenha um tamanho diferente do intervalo que está sendo substituído.
O exemplo a seguir substitui `"Chocolate Spread"`, `"Cheese"` e `"Butter"` por `"Bananas"` e `"Apples"`:

```swift
shoppingList[4...6] = ["Bananas", "Apples"]
// shoppingList now contains 6 items
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> shoppingList[4...6] = ["Bananas", "Apples"]
  /> shoppingList now contains \(shoppingList.count) items
  </ shoppingList now contains 6 items
  ```
-->

Para inserir um item no array em um índice especificado, chame o método `insert(_:at:)` do array:

```swift
shoppingList.insert("Maple Syrup", at: 0)
// shoppingList now contains 7 items
// "Maple Syrup" is now the first item in the list
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> shoppingList.insert("Maple Syrup", at: 0)
  /> shoppingList now contains \(shoppingList.count) items
  </ shoppingList now contains 7 items
  /> \"\(shoppingList[0])\" is now the first item in the list
  </ "Maple Syrup" is now the first item in the list
  ```
-->

Essa chamada ao método `insert(_:at:)` insere um novo item com o valor `"Maple Syrup"` no início da lista de compras, indicado por um índice de `0`.

De forma semelhante, você remove um item do array com o método `remove(at:)`.
Esse método remove o item no índice especificado e retorna o item removido (embora você possa ignorar o valor retornado se não precisar dele):

```swift
let mapleSyrup = shoppingList.remove(at: 0)
// the item that was at index 0 has just been removed
// shoppingList now contains 6 items, and no Maple Syrup
// the mapleSyrup constant is now equal to the removed "Maple Syrup" string
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> let mapleSyrup = shoppingList.remove(at: 0)
  // the item that was at index 0 has just been removed
  /> shoppingList now contains \(shoppingList.count) items, and no Maple Syrup
  </ shoppingList now contains 6 items, and no Maple Syrup
  /> the mapleSyrup constant is now equal to the removed \"\(mapleSyrup)\" string
  </ the mapleSyrup constant is now equal to the removed "Maple Syrup" string
  ```
-->

> Nota: Se você tentar acessar ou modificar um valor para um índice que esteja fora dos limites existentes de um array, causará um erro em tempo de execução.
> Você pode verificar se um índice é válido antes de usá-lo, comparando-o com a propriedade `count` do array.
> O maior índice válido em um array é `count - 1`, porque os arrays são indexados a partir de zero;
> no entanto, quando `count` é `0` (o que significa que o array está vazio), não existe nenhum índice válido.

Quaisquer lacunas em um array são fechadas quando um item é removido, e por isso o valor no índice `0` volta a ser igual a `"Six eggs"`:

```swift
firstItem = shoppingList[0]
// firstItem is now equal to "Six eggs"
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> firstItem = shoppingList[0]
  /> firstItem is now equal to \"\(firstItem)\"
  </ firstItem is now equal to "Six eggs"
  ```
-->

Se você quiser remover o último item de um array, use o método `removeLast()` em vez do método `remove(at:)`, para evitar a necessidade de consultar a propriedade `count` do array.
Assim como o método `remove(at:)`, `removeLast()` retorna o item removido:

```swift
let apples = shoppingList.removeLast()
// the last item in the array has just been removed
// shoppingList now contains 5 items, and no apples
// the apples constant is now equal to the removed "Apples" string
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> let apples = shoppingList.removeLast()
  // the last item in the array has just been removed
  /> shoppingList now contains \(shoppingList.count) items, and no apples
  </ shoppingList now contains 5 items, and no apples
  /> the apples constant is now equal to the removed \"\(apples)\" string
  </ the apples constant is now equal to the removed "Apples" string
  ```
-->

### Iterando Sobre um Array

Você pode percorrer todo o conjunto de valores de um array com o laço `for`-`in`:

```swift
for item in shoppingList {
    print(item)
}
// Six eggs
// Milk
// Flour
// Baking Powder
// Bananas
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> for item in shoppingList {
        print(item)
     }
  </ Six eggs
  </ Milk
  </ Flour
  </ Baking Powder
  </ Bananas
  ```
-->

Se você precisar do índice inteiro de cada item, além do seu valor, use o método `enumerated()` para percorrer o array.
Para cada item do array, o método `enumerated()` retorna uma tupla composta de um inteiro e do item.
Os inteiros começam em zero e aumentam uma unidade para cada item; se você enumerar um array inteiro, esses inteiros correspondem aos índices dos itens.
Você pode decompor a tupla em constantes ou variáveis temporárias como parte da iteração:

```swift
for (index, value) in shoppingList.enumerated() {
    print("Item \(index + 1): \(value)")
}
// Item 1: Six eggs
// Item 2: Milk
// Item 3: Flour
// Item 4: Baking Powder
// Item 5: Bananas
```

<!--
  - test: `arraysInferred`

  ```swifttest
  -> for (index, value) in shoppingList.enumerated() {
        print("Item \(index + 1): \(value)")
     }
  </ Item 1: Six eggs
  </ Item 2: Milk
  </ Item 3: Flour
  </ Item 4: Baking Powder
  </ Item 5: Bananas
  ```
-->

Para mais informações sobre o laço `for`-`in`, consulte <doc:ControlFlow#For-In-Loops>.

## Conjuntos

Um *conjunto* armazena valores distintos do mesmo tipo em uma coleção sem ordem definida.
Você pode usar um conjunto no lugar de um array quando a ordem dos itens não for importante, ou quando precisar garantir que um item apareça apenas uma vez.

> Nota: O tipo `Set` do Swift tem ponte com a classe `NSSet` do Foundation.
>
> Para mais informações sobre como usar `Set` com Foundation e Cocoa, consulte [Ponte entre Set e NSSet](https://developer.apple.com/documentation/swift/set#Bridging-Between-Set-and-NSSet).

<!--
  TODO: Add note about performance characteristics of contains on sets as opposed to arrays?
-->

### Valores de Hash para Tipos de Conjunto

Um tipo precisa ser *hashable* para poder ser armazenado em um conjunto. Ou seja, o tipo precisa fornecer uma forma de calcular um *valor de hash* para si mesmo.
Um valor de hash é um valor `Int` que é igual para todos os objetos considerados iguais, de modo que, se `a == b`, o valor de hash de `a` é igual ao valor de hash de `b`.

Todos os tipos básicos do Swift (como `String`, `Int`, `Double` e `Bool`) são hashable por padrão, e podem ser usados como tipos de valor de conjunto ou tipos de chave de dicionário.
Valores de casos de enum sem valores associados (como descrito em <doc:Enumerations>) também são hashable por padrão.

> Nota: Você pode usar seus próprios tipos personalizados como tipos de valor de conjunto ou tipos de chave de dicionário, fazendo-os adotar o protocolo `Hashable` da biblioteca padrão do Swift.
> Para informações sobre como implementar o método obrigatório `hash(into:)`, consulte [`Hashable`](https://developer.apple.com/documentation/swift/hashable).
> Para informações sobre como adotar protocolos, consulte <doc:Protocols>.

### Sintaxe do Tipo Set

O tipo de um conjunto do Swift é escrito como `Set<Element>`, em que `Element` é o tipo que o conjunto pode armazenar.
Diferentemente dos arrays, os conjuntos não têm uma forma abreviada equivalente.

### Criando e Inicializando um Conjunto Vazio

Você pode criar um conjunto vazio de determinado tipo usando a sintaxe de inicializador:

```swift
var letters = Set<Character>()
print("letters is of type Set<Character> with \(letters.count) items.")
// Prints "letters is of type Set<Character> with 0 items."
```

<!--
  - test: `setsEmpty`

  ```swifttest
  -> var letters = Set<Character>()
  -> print("letters is of type Set<Character> with \(letters.count) items.")
  <- letters is of type Set<Character> with 0 items.
  ```
-->

> Nota: O tipo da variável `letters` é inferido como `Set<Character>` a partir do tipo do inicializador.

Alternativamente, se o contexto já fornecer informação de tipo, como um argumento de função ou uma variável ou constante já tipada, você pode criar um conjunto vazio com um literal de array vazio:

```swift
letters.insert("a")
// letters now contains 1 value of type Character
letters = []
// letters is now an empty set, but is still of type Set<Character>
```

<!--
  - test: `setsEmpty`

  ```swifttest
  -> letters.insert("a")
  /> letters now contains \(letters.count) value of type Character
  </ letters now contains 1 value of type Character
  -> letters = []
  // letters is now an empty set, but is still of type Set<Character>
  ```
-->

### Criando um Conjunto com um Literal de Array

Você também pode inicializar um conjunto com um literal de array, como uma forma abreviada de escrever um ou mais valores como uma coleção do tipo conjunto.

O exemplo abaixo cria um conjunto chamado `favoriteGenres` para armazenar valores `String`:

```swift
var favoriteGenres: Set<String> = ["Rock", "Classical", "Hip hop"]
// favoriteGenres has been initialized with three initial items
```

<!--
  - test: `sets`

  ```swifttest
  -> var favoriteGenres: Set<String> = ["Rock", "Classical", "Hip hop"]
  // favoriteGenres has been initialized with three initial items
  ```
-->

A variável `favoriteGenres` é declarada como “um conjunto de valores `String`”, escrito como `Set<String>`.
Como esse conjunto em particular especificou um tipo de valor `String`, ele *só* pode armazenar valores `String`.
Aqui, o conjunto `favoriteGenres` é inicializado com três valores `String` (`"Rock"`, `"Classical"` e `"Hip hop"`), escritos dentro de um literal de array.

> Nota: O conjunto `favoriteGenres` é declarado como variável (com a palavra-chave `var`) e não como constante (com a palavra-chave `let`),
> porque itens são adicionados e removidos nos exemplos a seguir.

Um tipo de conjunto não pode ser inferido apenas a partir de um literal de array, por isso o tipo `Set` precisa ser declarado explicitamente.
No entanto, graças à inferência de tipos do Swift, você não precisa escrever o tipo dos elementos do conjunto se estiver inicializando-o com um literal de array que contém valores de apenas um tipo.
A inicialização de `favoriteGenres` poderia ter sido escrita de forma mais curta:

```swift
var favoriteGenres: Set = ["Rock", "Classical", "Hip hop"]
```

<!--
  - test: `setsInferred`

  ```swifttest
  -> var favoriteGenres: Set = ["Rock", "Classical", "Hip hop"]
  ```
-->

Como todos os valores no literal de array são do mesmo tipo, o Swift pode inferir que `Set<String>` é o tipo correto para a variável `favoriteGenres`.

### Acessando e Modificando um Conjunto

Você acessa e modifica um conjunto por meio de seus métodos e propriedades.

Para descobrir o número de itens em um conjunto, consulte sua propriedade somente leitura `count`:

```swift
print("I have \(favoriteGenres.count) favorite music genres.")
// Prints "I have 3 favorite music genres."
```

<!--
  - test: `setUsage`

  ```swifttest
  >> var favoriteGenres: Set = ["Rock", "Classical", "Hip hop"]
  -> print("I have \(favoriteGenres.count) favorite music genres.")
  <- I have 3 favorite music genres.
  ```
-->

Use a propriedade booleana `isEmpty` como atalho para verificar se a propriedade `count` é igual a `0`:

```swift
if favoriteGenres.isEmpty {
    print("As far as music goes, I'm not picky.")
} else {
    print("I have particular music preferences.")
}
// Prints "I have particular music preferences."
```

<!--
  - test: `setUsage`

  ```swifttest
  -> if favoriteGenres.isEmpty {
        print("As far as music goes, I'm not picky.")
     } else {
        print("I have particular music preferences.")
     }
  <- I have particular music preferences.
  ```
-->

Você pode adicionar um novo item a um conjunto chamando o método `insert(_:)` do conjunto:

```swift
favoriteGenres.insert("Jazz")
// favoriteGenres now contains 4 items
```

<!--
  - test: `setUsage`

  ```swifttest
  -> favoriteGenres.insert("Jazz")
  /> favoriteGenres now contains \(favoriteGenres.count) items
  </ favoriteGenres now contains 4 items
  ```
-->

Você pode remover um item de um conjunto chamando o método `remove(_:)` do conjunto, que remove o item se ele for membro do conjunto e retorna o valor removido, ou retorna `nil` se o conjunto não o continha.
Alternativamente, todos os itens de um conjunto podem ser removidos com o método `removeAll()`.

```swift
if let removedGenre = favoriteGenres.remove("Rock") {
    print("\(removedGenre)? I'm over it.")
} else {
    print("I never much cared for that.")
}
// Prints "Rock? I'm over it."
```

<!--
  - test: `setUsage`

  ```swifttest
  -> if let removedGenre = favoriteGenres.remove("Rock") {
        print("\(removedGenre)? I'm over it.")
     } else {
        print("I never much cared for that.")
     }
  <- Rock? I'm over it.
  ```
-->

Para verificar se um conjunto contém determinado item, use o método `contains(_:)`.

```swift
if favoriteGenres.contains("Funk") {
    print("I get up on the good foot.")
} else {
    print("It's too funky in here.")
}
// Prints "It's too funky in here."
```

<!--
  - test: `setUsage`

  ```swifttest
  -> if favoriteGenres.contains("Funk") {
         print("I get up on the good foot.")
     } else {
         print("It's too funky in here.")
     }
  <- It's too funky in here.
  ```
-->

### Iterando Sobre um Conjunto

Você pode percorrer os valores de um conjunto com um laço `for`-`in`.

```swift
for genre in favoriteGenres {
    print("\(genre)")
}
// Classical
// Jazz
// Hip hop
```

<!--
  - test: `setUsage`

  ```swifttest
  -> for genre in favoriteGenres {
        print("\(genre)")
     }
  </ Classical
  </ Jazz
  </ Hip hop
  ```
-->

Para mais informações sobre o laço `for`-`in`, consulte <doc:ControlFlow#For-In-Loops>.

O tipo `Set` do Swift não tem uma ordem definida.
Para percorrer os valores de um conjunto em uma ordem específica, use o método `sorted()`, que retorna os elementos do conjunto como um array ordenado usando o operador `<`.

```swift
for genre in favoriteGenres.sorted() {
    print("\(genre)")
}
// Classical
// Hip hop
// Jazz
```

<!--
  - test: `setUsage`

  ```swifttest
  -> for genre in favoriteGenres.sorted() {
        print("\(genre)")
     }
  </ Classical
  </ Hip hop
  </ Jazz
  ```
-->

## Realizando Operações de Conjunto

Você pode executar com eficiência operações fundamentais de conjunto, como combinar dois conjuntos, determinar quais valores dois conjuntos têm em comum, ou determinar se dois conjuntos contêm todos, alguns ou nenhum dos mesmos valores.

### Operações Fundamentais de Conjunto

A ilustração abaixo mostra dois conjuntos, `a` e `b`, com os resultados de várias operações de conjunto representados pelas regiões sombreadas.

![](setVennDiagram)

- Use o método `intersection(_:)` para criar um novo conjunto apenas com os valores que são comuns aos dois conjuntos.
- Use o método `symmetricDifference(_:)` para criar um novo conjunto com os valores que estão em um dos conjuntos, mas não nos dois.
- Use o método `union(_:)` para criar um novo conjunto com todos os valores dos dois conjuntos.
- Use o método `subtracting(_:)` para criar um novo conjunto com os valores que não estão no conjunto especificado.

```swift
let oddDigits: Set = [1, 3, 5, 7, 9]
let evenDigits: Set = [0, 2, 4, 6, 8]
let singleDigitPrimeNumbers: Set = [2, 3, 5, 7]

oddDigits.union(evenDigits).sorted()
// [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
oddDigits.intersection(evenDigits).sorted()
// []
oddDigits.subtracting(singleDigitPrimeNumbers).sorted()
// [1, 9]
oddDigits.symmetricDifference(singleDigitPrimeNumbers).sorted()
// [1, 2, 9]
```

<!--
  - test: `setOperations`

  ```swifttest
  -> let oddDigits: Set = [1, 3, 5, 7, 9]
  -> let evenDigits: Set = [0, 2, 4, 6, 8]
  -> let singleDigitPrimeNumbers: Set = [2, 3, 5, 7]

  >> let a =
  -> oddDigits.union(evenDigits).sorted()
  >> assert(a == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
  // [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  >> let b =
  -> oddDigits.intersection(evenDigits).sorted()
  >> assert(b == [])
  // []
  >> let c =
  -> oddDigits.subtracting(singleDigitPrimeNumbers).sorted()
  >> assert(c == [1, 9])
  // [1, 9]
  >> let d =
  -> oddDigits.symmetricDifference(singleDigitPrimeNumbers).sorted()
  >> assert(d == [1, 2, 9])
  // [1, 2, 9]
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

### Pertinência e Igualdade de Conjuntos

A ilustração abaixo mostra três conjuntos, `a`, `b` e `c`, com regiões sobrepostas representando elementos compartilhados entre os conjuntos.
O conjunto `a` é um *superconjunto* do conjunto `b`, porque `a` contém todos os elementos de `b`.
Por outro lado, o conjunto `b` é um *subconjunto* do conjunto `a`, porque todos os elementos de `b` também estão contidos em `a`.
Os conjuntos `b` e `c` são *disjuntos* entre si, porque não compartilham nenhum elemento em comum.

![](setEulerDiagram)

- Use o operador de “igual a” (`==`) para determinar se dois conjuntos contêm exatamente os mesmos valores.
- Use o método `isSubset(of:)` para determinar se todos os valores de um conjunto estão contidos no conjunto especificado.
- Use o método `isSuperset(of:)` para determinar se um conjunto contém todos os valores de um conjunto especificado.
- Use os métodos `isStrictSubset(of:)` ou `isStrictSuperset(of:)` para determinar se um conjunto é subconjunto ou superconjunto de outro conjunto especificado, mas não igual a ele.
- Use o método `isDisjoint(with:)` para determinar se dois conjuntos não têm valores em comum.

```swift
let houseAnimals: Set = ["🐶", "🐱"]
let farmAnimals: Set = ["🐮", "🐔", "🐑", "🐶", "🐱"]
let cityAnimals: Set = ["🐦", "🐭"]

houseAnimals.isSubset(of: farmAnimals)
// true
farmAnimals.isSuperset(of: houseAnimals)
// true
farmAnimals.isDisjoint(with: cityAnimals)
// true
```

<!--
  - test: `setOperations`

  ```swifttest
  -> let houseAnimals: Set = ["🐶", "🐱"]
  -> let farmAnimals: Set = ["🐮", "🐔", "🐑", "🐶", "🐱"]
  -> let cityAnimals: Set = ["🐦", "🐭"]

  >> let aa =
  -> houseAnimals.isSubset(of: farmAnimals)
  >> assert(aa == true)
  // true
  >> let bb =
  -> farmAnimals.isSuperset(of: houseAnimals)
  >> assert(bb == true)
  // true
  >> let cc =
  -> farmAnimals.isDisjoint(with: cityAnimals)
  >> assert(cc == true)
  // true
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

## Dicionários

Um *dicionário* armazena associações entre chaves do mesmo tipo e valores do mesmo tipo, em uma coleção sem ordem definida.
Cada valor está associado a uma *chave* única, que funciona como um identificador desse valor dentro do dicionário.
Diferentemente dos itens de um array, os itens de um dicionário não têm uma ordem especificada.
Você usa um dicionário quando precisa buscar valores com base em seu identificador, de modo semelhante a como um dicionário do mundo real é usado para buscar a definição de uma palavra específica.

> Nota: O tipo `Dictionary` do Swift tem ponte com a classe `NSDictionary` do Foundation.
>
> Para mais informações sobre como usar `Dictionary` com Foundation e Cocoa, consulte [Ponte entre Dictionary e NSDictionary](https://developer.apple.com/documentation/swift/dictionary#Bridging-Between-Dictionary-and-NSDictionary).

### Sintaxe Abreviada do Tipo Dictionary

O tipo de um dicionário do Swift é escrito por extenso como `Dictionary<Key, Value>`, em que `Key` é o tipo de valor que pode ser usado como chave do dicionário, e `Value` é o tipo de valor que o dicionário armazena para essas chaves.

> Nota: O tipo de chave de um dicionário precisa adotar o protocolo `Hashable`, assim como o tipo de valor de um conjunto.

Você também pode escrever o tipo de um dicionário em forma abreviada, como `[Key: Value]`.
Embora as duas formas sejam funcionalmente idênticas, a forma abreviada é preferida e é usada ao longo deste guia ao se referir ao tipo de um dicionário.

### Criando um Dicionário Vazio

Assim como com os arrays, você pode criar um `Dictionary` vazio de determinado tipo usando a sintaxe de inicializador:

```swift
var namesOfIntegers: [Int: String] = [:]
// namesOfIntegers is an empty [Int: String] dictionary
```

<!--
  - test: `dictionariesEmpty`

  ```swifttest
  -> var namesOfIntegers: [Int: String] = [:]
  // namesOfIntegers is an empty [Int: String] dictionary
  ```
-->

Este exemplo cria um dicionário vazio do tipo `[Int: String]` para armazenar nomes legíveis de valores inteiros.
Suas chaves são do tipo `Int`, e seus valores são do tipo `String`.

Se o contexto já fornecer informação de tipo, você pode criar um dicionário vazio com um literal de dicionário vazio, que é escrito como `[:]` (dois-pontos dentro de um par de colchetes):

```swift
namesOfIntegers[16] = "sixteen"
// namesOfIntegers now contains 1 key-value pair
namesOfIntegers = [:]
// namesOfIntegers is once again an empty dictionary of type [Int: String]
```

<!--
  - test: `dictionariesEmpty`

  ```swifttest
  -> namesOfIntegers[16] = "sixteen"
  /> namesOfIntegers now contains \(namesOfIntegers.count) key-value pair
  </ namesOfIntegers now contains 1 key-value pair
  -> namesOfIntegers = [:]
  // namesOfIntegers is once again an empty dictionary of type [Int: String]
  ```
-->

### Criando um Dicionário com um Literal de Dicionário

Você também pode inicializar um dicionário com um *literal de dicionário*, que tem uma sintaxe semelhante à do literal de array visto antes.
Um literal de dicionário é uma forma abreviada de escrever um ou mais pares chave-valor como uma coleção `Dictionary`.

Um *par chave-valor* é uma combinação de uma chave e um valor.
Em um literal de dicionário, a chave e o valor de cada par chave-valor são separados por dois-pontos.
Os pares chave-valor são escritos como uma lista, separados por vírgulas e envoltos por um par de colchetes:

```swift
[<#key 1#>: <#value 1#>, <#key 2#>: <#value 2#>, <#key 3#>: <#value 3#>]
```

O exemplo abaixo cria um dicionário para armazenar os nomes de aeroportos internacionais.
Neste dicionário, as chaves são códigos de três letras da International Air Transport Association, e os valores são os nomes dos aeroportos:

```swift
var airports: [String: String] = ["YYZ": "Toronto Pearson", "DUB": "Dublin"]
```

<!--
  - test: `dictionaries`

  ```swifttest
  -> var airports: [String: String] = ["YYZ": "Toronto Pearson", "DUB": "Dublin"]
  ```
-->

O dicionário `airports` é declarado como tendo o tipo `[String: String]`, o que significa “um `Dictionary` cujas chaves são do tipo `String`, e cujos valores também são do tipo `String`”.

> Nota: O dicionário `airports` é declarado como variável (com a palavra-chave `var`) e não como constante (com a palavra-chave `let`),
> porque mais aeroportos são adicionados ao dicionário nos exemplos a seguir.

O dicionário `airports` é inicializado com um literal de dicionário contendo dois pares chave-valor.
O primeiro par tem a chave `"YYZ"` e o valor `"Toronto Pearson"`.
O segundo par tem a chave `"DUB"` e o valor `"Dublin"`.

Este literal de dicionário contém dois pares `String: String`.
Esse tipo chave-valor corresponde à declaração de tipo da variável `airports` (um dicionário com apenas chaves `String` e apenas valores `String`), e por isso a atribuição do literal de dicionário é permitida como forma de inicializar o dicionário `airports` com dois itens iniciais.

Assim como com os arrays, você não precisa escrever o tipo do dicionário se estiver inicializando-o com um literal de dicionário cujas chaves e valores têm tipos consistentes.
A inicialização de `airports` poderia ter sido escrita de forma mais curta:

```swift
var airports = ["YYZ": "Toronto Pearson", "DUB": "Dublin"]
```

<!--
  - test: `dictionariesInferred`

  ```swifttest
  -> var airports = ["YYZ": "Toronto Pearson", "DUB": "Dublin"]
  ```
-->

Como todas as chaves do literal são do mesmo tipo entre si, e da mesma forma todos os valores são do mesmo tipo entre si, o Swift pode inferir que `[String: String]` é o tipo correto para o dicionário `airports`.

Assim como os literais de array, os literais de dicionário podem incluir uma vírgula final depois do último par chave-valor:

```swift
var airports = [
    "YYZ": "Toronto Pearson",
    "DUB": "Dublin",
]
```

### Acessando e Modificando um Dicionário

Você acessa e modifica um dicionário por meio de seus métodos e propriedades, ou usando a sintaxe de *subscript*.

Assim como com um array, você descobre o número de itens em um `Dictionary` consultando a propriedade somente leitura `count`:

```swift
print("The airports dictionary contains \(airports.count) items.")
// Prints "The airports dictionary contains 2 items."
```

<!--
  - test: `dictionariesInferred`

  ```swifttest
  -> print("The airports dictionary contains \(airports.count) items.")
  <- The airports dictionary contains 2 items.
  ```
-->

Use a propriedade booleana `isEmpty` como atalho para verificar se a propriedade `count` é igual a `0`:

```swift
if airports.isEmpty {
    print("The airports dictionary is empty.")
} else {
    print("The airports dictionary isn't empty.")
}
// Prints "The airports dictionary isn't empty."
```

<!--
  - test: `dictionariesInferred`

  ```swifttest
  -> if airports.isEmpty {
        print("The airports dictionary is empty.")
     } else {
        print("The airports dictionary isn't empty.")
     }
  <- The airports dictionary isn't empty.
  ```
-->

Você pode adicionar um novo item a um dicionário com a sintaxe de subscript.
Use uma nova chave do tipo apropriado como índice de subscript, e atribua um novo valor do tipo apropriado:

```swift
airports["LHR"] = "London"
// the airports dictionary now contains 3 items
```

<!--
  - test: `dictionariesInferred`

  ```swifttest
  -> airports["LHR"] = "London"
  /> the airports dictionary now contains \(airports.count) items
  </ the airports dictionary now contains 3 items
  ```
-->

Você também pode usar a sintaxe de subscript para alterar o valor associado a uma chave específica:

```swift
airports["LHR"] = "London Heathrow"
// the value for "LHR" has been changed to "London Heathrow"
```

<!--
  - test: `dictionariesInferred`

  ```swifttest
  -> airports["LHR"] = "London Heathrow"
  /> the value for \"LHR\" has been changed to \"\(airports["LHR"]!)\"
  </ the value for "LHR" has been changed to "London Heathrow"
  ```
-->

Como alternativa à sintaxe de subscript, use o método `updateValue(_:forKey:)` do dicionário para definir ou atualizar o valor de uma chave específica.
Assim como nos exemplos de subscript acima, o método `updateValue(_:forKey:)` define um valor para a chave se nenhum existir, ou atualiza o valor se a chave já existir.
Diferentemente da sintaxe de subscript, porém, o método `updateValue(_:forKey:)` retorna o valor *antigo* depois de realizar uma atualização.
Isso permite verificar se houve ou não uma atualização.

O método `updateValue(_:forKey:)` retorna um valor optional do tipo de valor do dicionário.
Para um dicionário que armazena valores `String`, por exemplo, o método retorna um valor do tipo `String?`, ou “`String` optional”.
Esse valor optional contém o valor antigo daquela chave, caso ele existisse antes da atualização, ou `nil` se não existia nenhum valor:

```swift
if let oldValue = airports.updateValue("Dublin Airport", forKey: "DUB") {
    print("The old value for DUB was \(oldValue).")
}
// Prints "The old value for DUB was Dublin."
```

<!--
  - test: `dictionariesInferred`

  ```swifttest
  -> if let oldValue = airports.updateValue("Dublin Airport", forKey: "DUB") {
        print("The old value for DUB was \(oldValue).")
     }
  <- The old value for DUB was Dublin.
  ```
-->

Você também pode usar a sintaxe de subscript para recuperar um valor do dicionário para uma chave específica.
Como é possível consultar uma chave para a qual não existe valor, a subscript de um dicionário retorna um valor optional do tipo de valor do dicionário.
Se o dicionário contiver um valor para a chave consultada, a subscript retorna um valor optional contendo o valor existente para aquela chave.
Caso contrário, a subscript retorna `nil`:

```swift
if let airportName = airports["DUB"] {
    print("The name of the airport is \(airportName).")
} else {
    print("That airport isn't in the airports dictionary.")
}
// Prints "The name of the airport is Dublin Airport."
```

<!--
  - test: `dictionariesInferred`

  ```swifttest
  -> if let airportName = airports["DUB"] {
        print("The name of the airport is \(airportName).")
     } else {
        print("That airport isn't in the airports dictionary.")
     }
  <- The name of the airport is Dublin Airport.
  ```
-->

Você pode usar a sintaxe de subscript para remover um par chave-valor de um dicionário, atribuindo o valor `nil` a essa chave:

```swift
airports["APL"] = "Apple International"
// "Apple International" isn't the real airport for APL, so delete it
airports["APL"] = nil
// APL has now been removed from the dictionary
```

<!--
  - test: `dictionariesInferred`

  ```swifttest
  -> airports["APL"] = "Apple International"
  // "Apple International" isn't the real airport for APL, so delete it
  -> airports["APL"] = nil
  // APL has now been removed from the dictionary
  >> if let deletedName = airports["APL"] {
  >>    print("The key-value pair for APL has *not* been deleted, but it should have been!")
  >>    print("It still has a value of \(deletedName)")
  >> } else {
  >>    print("APL has now been removed from the dictionary")
  >> }
  << APL has now been removed from the dictionary
  ```
-->

Alternativamente, remova um par chave-valor de um dicionário com o método `removeValue(forKey:)`.
Esse método remove o par chave-valor se ele existir e retorna o valor removido, ou retorna `nil` se não existia nenhum valor:

```swift
if let removedValue = airports.removeValue(forKey: "DUB") {
    print("The removed airport's name is \(removedValue).")
} else {
    print("The airports dictionary doesn't contain a value for DUB.")
}
// Prints "The removed airport's name is Dublin Airport."
```

<!--
  - test: `dictionariesInferred`

  ```swifttest
  -> if let removedValue = airports.removeValue(forKey: "DUB") {
        print("The removed airport's name is \(removedValue).")
     } else {
        print("The airports dictionary doesn't contain a value for DUB.")
     }
  <- The removed airport's name is Dublin Airport.
  ```
-->

### Iterando Sobre um Dicionário

Você pode percorrer os pares chave-valor de um dicionário com um laço `for`-`in`.
Cada item do dicionário é retornado como uma tupla `(key, value)`, e você pode decompor os membros da tupla em constantes ou variáveis temporárias como parte da iteração:

```swift
for (airportCode, airportName) in airports {
    print("\(airportCode): \(airportName)")
}
// LHR: London Heathrow
// YYZ: Toronto Pearson
```

<!--
  - test: `dictionariesInferred`

  ```swifttest
  -> for (airportCode, airportName) in airports {
        print("\(airportCode): \(airportName)")
     }
  </ LHR: London Heathrow
  </ YYZ: Toronto Pearson
  ```
-->

Para mais informações sobre o laço `for`-`in`, consulte <doc:ControlFlow#For-In-Loops>.

Você também pode obter uma coleção iterável com as chaves ou os valores de um dicionário, acessando suas propriedades `keys` e `values`:

```swift
for airportCode in airports.keys {
    print("Airport code: \(airportCode)")
}
// Airport code: LHR
// Airport code: YYZ

for airportName in airports.values {
    print("Airport name: \(airportName)")
}
// Airport name: London Heathrow
// Airport name: Toronto Pearson
```

<!--
  - test: `dictionariesInferred`

  ```swifttest
  -> for airportCode in airports.keys {
        print("Airport code: \(airportCode)")
     }
  </ Airport code: LHR
  </ Airport code: YYZ

  -> for airportName in airports.values {
        print("Airport name: \(airportName)")
     }
  </ Airport name: London Heathrow
  </ Airport name: Toronto Pearson
  ```
-->

Se você precisar usar as chaves ou os valores de um dicionário com uma API que recebe uma instância de `Array`, inicialize um novo array com a propriedade `keys` ou `values`:

```swift
let airportCodes = [String](airports.keys)
// airportCodes is ["LHR", "YYZ"]

let airportNames = [String](airports.values)
// airportNames is ["London Heathrow", "Toronto Pearson"]
```

<!--
  - test: `dictionariesInferred`

  ```swifttest
  -> let airportCodes = [String](airports.keys)
  /> airportCodes is [\"\(airportCodes[0])\", \"\(airportCodes[1])\"]
  </ airportCodes is ["LHR", "YYZ"]

  -> let airportNames = [String](airports.values)
  /> airportNames is [\"\(airportNames[0])\", \"\(airportNames[1])\"]
  </ airportNames is ["London Heathrow", "Toronto Pearson"]
  ```
-->

O tipo `Dictionary` do Swift não tem uma ordem definida.
Para percorrer as chaves ou os valores de um dicionário em uma ordem específica, use o método `sorted()` sobre sua propriedade `keys` ou `values`.

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
