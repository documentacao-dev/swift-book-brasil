# Generics

Escreva código que funciona com vários tipos e especifique requisitos para esses tipos.

*Código genérico* permite escrever funções e tipos flexíveis e reutilizáveis
que podem trabalhar com qualquer tipo, sujeitos a requisitos que você define.
Você pode escrever código que evita duplicação
e expressa sua intenção de forma clara e abstrata.

Generics são um dos recursos mais poderosos do Swift,
e grande parte da biblioteca padrão do Swift é construída com código genérico.
Na verdade, você já usa generics ao longo do *Guia da linguagem*,
mesmo sem perceber.
Por exemplo, os tipos `Array` e `Dictionary` do Swift
são ambos coleções genéricas.
Você pode criar um array que guarda valores `Int`,
ou um array que guarda valores `String`,
ou, na verdade, um array para qualquer outro tipo que possa ser criado em Swift.
Da mesma forma, você pode criar um dicionário para armazenar valores de qualquer tipo especificado,
e não há limitações sobre qual pode ser esse tipo.

## O problema que os generics resolvem

Aqui está uma função padrão, não genérica, chamada `swapTwoInts(_:_:)`,
que troca dois valores `Int`:

```swift
func swapTwoInts(_ a: inout Int, _ b: inout Int) {
    let temporaryA = a
    a = b
    b = temporaryA
}
```

<!--
  - test: `whyGenerics`

  ```swifttest
  -> func swapTwoInts(_ a: inout Int, _ b: inout Int) {
        let temporaryA = a
        a = b
        b = temporaryA
     }
  ```
-->

Essa função usa parâmetros in-out para trocar os valores de `a` e `b`,
conforme descrito em <doc:Functions#In-Out-Parameters>.

A função `swapTwoInts(_:_:)` coloca o valor original de `b` em `a`,
e o valor original de `a` em `b`.
Você pode chamar essa função para trocar os valores de duas variáveis `Int`:

```swift
var someInt = 3
var anotherInt = 107
swapTwoInts(&someInt, &anotherInt)
print("someInt is now \(someInt), and anotherInt is now \(anotherInt)")
// Prints "someInt is now 107, and anotherInt is now 3".
```

<!--
  - test: `whyGenerics`

  ```swifttest
  -> var someInt = 3
  -> var anotherInt = 107
  -> swapTwoInts(&someInt, &anotherInt)
  -> print("someInt is now \(someInt), and anotherInt is now \(anotherInt)")
  <- someInt is now 107, and anotherInt is now 3
  ```
-->

A função `swapTwoInts(_:_:)` é útil, mas só pode ser usada com valores `Int`.
Se você quiser trocar dois valores `String`,
ou dois valores `Double`,
precisa escrever mais funções,
como as funções `swapTwoStrings(_:_:)` e `swapTwoDoubles(_:_:)` mostradas abaixo:

```swift
func swapTwoStrings(_ a: inout String, _ b: inout String) {
    let temporaryA = a
    a = b
    b = temporaryA
}

func swapTwoDoubles(_ a: inout Double, _ b: inout Double) {
    let temporaryA = a
    a = b
    b = temporaryA
}
```

<!--
  - test: `whyGenerics`

  ```swifttest
  -> func swapTwoStrings(_ a: inout String, _ b: inout String) {
        let temporaryA = a
        a = b
        b = temporaryA
     }

  -> func swapTwoDoubles(_ a: inout Double, _ b: inout Double) {
        let temporaryA = a
        a = b
        b = temporaryA
     }
  ```
-->

Você deve ter notado que o corpo das funções
`swapTwoInts(_:_:)`, `swapTwoStrings(_:_:)` e `swapTwoDoubles(_:_:)` é idêntico.
A única diferença é o tipo dos valores que elas aceitam
(`Int`, `String` e `Double`).

É mais útil, e bem mais flexível,
escrever uma única função que troca dois valores de *qualquer* tipo.
Código genérico permite escrever essa função.
(Uma versão genérica dessas funções está definida abaixo.)

> Nota: Nas três funções,
> os tipos de `a` e `b` precisam ser iguais.
> Se `a` e `b` não forem do mesmo tipo,
> não é possível trocar os valores deles.
> Swift é uma linguagem com segurança de tipos,
> e não permite (por exemplo) que uma variável do tipo `String`
> e uma variável do tipo `Double`
> troquem valores entre si.
> Tentar fazer isso resulta em um erro de compilação.

## Funções genéricas

*Funções genéricas* podem trabalhar com qualquer tipo.
Aqui está uma versão genérica da função `swapTwoInts(_:_:)` vista acima,
chamada `swapTwoValues(_:_:)`:

```swift
func swapTwoValues<T>(_ a: inout T, _ b: inout T) {
    let temporaryA = a
    a = b
    b = temporaryA
}
```

<!--
  - test: `genericFunctions`

  ```swifttest
  -> func swapTwoValues<T>(_ a: inout T, _ b: inout T) {
        let temporaryA = a
        a = b
        b = temporaryA
     }
  ```
-->

<!--
  This could be done in one line using a tuple pattern: (a, b) = (b, a)
  That's probably not as approachable here, and the novel syntax to avoid an
  explicit placeholder variable might distract from the discussion of
  generics.
-->

O corpo da função `swapTwoValues(_:_:)`
é idêntico ao corpo da função `swapTwoInts(_:_:)`.
No entanto, a primeira linha de `swapTwoValues(_:_:)`
é um pouco diferente da de `swapTwoInts(_:_:)`.
Veja como as primeiras linhas se comparam:

```swift
func swapTwoInts(_ a: inout Int, _ b: inout Int)
func swapTwoValues<T>(_ a: inout T, _ b: inout T)
```

<!--
  - test: `genericFunctionsComparison`

  ```swifttest
  -> func swapTwoInts(_ a: inout Int, _ b: inout Int)
  >> {
  >>    let temporaryA = a
  >>    a = b
  >>    b = temporaryA
  >> }
  -> func swapTwoValues<T>(_ a: inout T, _ b: inout T)
  >> {
  >>    let temporaryA = a
  >>    a = b
  >>    b = temporaryA
  >> }
  ```
-->

A versão genérica da função
usa um nome de tipo *marcador* (chamado aqui de `T`)
no lugar de um nome de tipo *real* (como `Int`, `String` ou `Double`).
O nome de tipo marcador não diz nada sobre o que `T` precisa ser,
mas *diz* que `a` e `b` precisam ser do mesmo tipo `T`,
seja lá o que `T` representar.
O tipo real a ser usado no lugar de `T`
é determinado toda vez que a função `swapTwoValues(_:_:)` é chamada.

A outra diferença entre uma função genérica e uma não genérica
é que o nome da função genérica (`swapTwoValues(_:_:)`)
é seguido pelo nome do tipo marcador (`T`) entre colchetes angulares (`<T>`).
Os colchetes dizem ao Swift que `T` é um nome de tipo marcador
dentro da definição da função `swapTwoValues(_:_:)`.
Como `T` é um marcador, o Swift não procura um tipo real chamado `T`.

A função `swapTwoValues(_:_:)` agora pode ser chamada do mesmo jeito que `swapTwoInts`,
exceto que pode receber dois valores de *qualquer* tipo,
contanto que os dois valores sejam do mesmo tipo entre si.
Cada vez que `swapTwoValues(_:_:)` é chamada,
o tipo a ser usado para `T` é inferido a partir dos tipos dos valores passados para a função.

Nos dois exemplos abaixo, `T` é inferido como `Int` e `String`, respectivamente:

```swift
var someInt = 3
var anotherInt = 107
swapTwoValues(&someInt, &anotherInt)
// someInt is now 107, and anotherInt is now 3

var someString = "hello"
var anotherString = "world"
swapTwoValues(&someString, &anotherString)
// someString is now "world", and anotherString is now "hello"
```

<!--
  - test: `genericFunctions`

  ```swifttest
  -> var someInt = 3
  -> var anotherInt = 107
  -> swapTwoValues(&someInt, &anotherInt)
  /> someInt is now \(someInt), and anotherInt is now \(anotherInt)
  </ someInt is now 107, and anotherInt is now 3

  -> var someString = "hello"
  -> var anotherString = "world"
  -> swapTwoValues(&someString, &anotherString)
  /> someString is now \"\(someString)\", and anotherString is now \"\(anotherString)\"
  </ someString is now "world", and anotherString is now "hello"
  ```
-->

> Nota: A função `swapTwoValues(_:_:)` definida acima é inspirada
> em uma função genérica chamada `swap`, que faz parte da biblioteca padrão do Swift
> e fica disponível automaticamente para você usar nos seus apps.
> Se você precisar do comportamento da função `swapTwoValues(_:_:)` no seu próprio código,
> pode usar a função `swap(_:_:)` que já existe no Swift, em vez de escrever sua própria implementação.

## Parâmetros de tipo

No exemplo `swapTwoValues(_:_:)` acima,
o tipo marcador `T` é um exemplo de *parâmetro de tipo*.
Parâmetros de tipo especificam e nomeiam um tipo marcador,
e são escritos logo depois do nome da função,
entre um par de colchetes angulares (como `<T>`).

Depois de especificar um parâmetro de tipo,
você pode usá-lo para definir o tipo dos parâmetros de uma função
(como os parâmetros `a` e `b` da função `swapTwoValues(_:_:)`),
ou como tipo de retorno da função,
ou como anotação de tipo dentro do corpo da função.
Em todos os casos, o parâmetro de tipo
é substituído por um tipo *real* sempre que a função é chamada.
(No exemplo `swapTwoValues(_:_:)` acima,
`T` foi substituído por `Int` na primeira vez que a função foi chamada,
e por `String` na segunda vez.)

Você pode fornecer mais de um parâmetro de tipo
escrevendo vários nomes de parâmetros de tipo dentro dos colchetes angulares,
separados por vírgulas.

## Nomeando parâmetros de tipo

Na maioria dos casos, parâmetros de tipo têm nomes descritivos,
como `Key` e `Value` em `Dictionary<Key, Value>`
e `Element` em `Array<Element>`,
que informam ao leitor qual é a relação entre o parâmetro de tipo
e o tipo ou a função genérica em que ele é usado.
No entanto, quando não há uma relação significativa entre eles,
é tradicional nomeá-los com letras isoladas, como `T`, `U` e `V`,
como o `T` da função `swapTwoValues(_:_:)` acima.

Use nomes em UpperCamelCase para parâmetros de tipo,
como `T` e `MyTypeParameter`,
para indicar que são um marcador para um *tipo*, e não para um valor.

> Nota:
> Se você não precisar nomear um parâmetro de tipo
> e as restrições de tipo genérico forem simples,
> existe uma sintaxe alternativa e mais leve que você pode usar no lugar,
> conforme descrito em <doc:OpaqueTypes#Opaque-Parameter-Types>.
<!--
Comparison between this syntax and the lightweight syntax
is in the Opaque Types chapter, not here ---
the reader hasn't learned about constraints yet,
so it wouldn't make sense to list what is/isn't supported.
-->

## Tipos genéricos

Além das funções genéricas,
o Swift permite definir seus próprios *tipos genéricos*.
São classes, structs e enums personalizados
que podem trabalhar com *qualquer* tipo, de forma parecida com `Array` e `Dictionary`.

Esta seção mostra como escrever um tipo de coleção genérico chamado `Stack`.
Uma pilha é um conjunto ordenado de valores, parecido com um array,
mas com um conjunto de operações mais restrito que o tipo `Array` do Swift.
Um array permite inserir e remover novos itens em qualquer posição dele.
Já uma pilha permite adicionar novos itens apenas no fim da coleção
(chamado de *empilhar*, ou *push*, um novo valor na pilha).
Da mesma forma, uma pilha permite remover itens apenas do fim da coleção
(chamado de *desempilhar*, ou *pop*, um valor da pilha).

> Nota: O conceito de pilha é usado pela classe `UINavigationController`
> para modelar os view controllers da hierarquia de navegação dela.
> Você chama o método `pushViewController(_:animated:)` da classe `UINavigationController`
> para adicionar (ou empilhar) um view controller na pilha de navegação,
> e o método `popViewControllerAnimated(_:)` para remover (ou desempilhar)
> um view controller da pilha de navegação.
> Uma pilha é um modelo de coleção útil sempre que você precisa de uma abordagem estrita
> de “último a entrar, primeiro a sair” para gerenciar uma coleção.

A ilustração abaixo mostra o comportamento de empilhar e desempilhar de uma pilha:

![](stackPushPop)

1. No momento, há três valores na pilha.
2. Um quarto valor é empilhado no topo da pilha.
3. A pilha agora tem quatro valores, com o mais recente no topo.
4. O item do topo da pilha é desempilhado.
5. Depois de desempilhar um valor, a pilha volta a ter três valores.

Veja como escrever uma versão não genérica de uma pilha,
neste caso para uma pilha de valores `Int`:

```swift
struct IntStack {
    var items: [Int] = []
    mutating func push(_ item: Int) {
        items.append(item)
    }
    mutating func pop() -> Int {
        return items.removeLast()
    }
}
```

<!--
  - test: `genericStack`

  ```swifttest
  -> struct IntStack {
        var items: [Int] = []
        mutating func push(_ item: Int) {
           items.append(item)
        }
        mutating func pop() -> Int {
           return items.removeLast()
        }
     }
  >> var intStack = IntStack()
  >> intStack.push(1)
  >> intStack.push(2)
  >> intStack.push(3)
  >> intStack.push(4)
  >> print("the stack now contains \(intStack.items.count) integers")
  << the stack now contains 4 integers
  ```
-->

Essa struct usa uma propriedade `Array` chamada `items` para armazenar os valores da pilha.
`Stack` oferece dois métodos, `push` e `pop`,
para empilhar e desempilhar valores da pilha.
Esses métodos são marcados como `mutating`,
porque precisam modificar (ou *mutar*) o array `items` da struct.

O tipo `IntStack` mostrado acima, porém, só pode ser usado com valores `Int`.
Seria bem mais útil definir uma struct `Stack` *genérica*,
que possa gerenciar uma pilha de *qualquer* tipo de valor.

Aqui está uma versão genérica do mesmo código:

```swift
struct Stack<Element> {
    var items: [Element] = []
    mutating func push(_ item: Element) {
        items.append(item)
    }
    mutating func pop() -> Element {
        return items.removeLast()
    }
}
```

<!--
  - test: `genericStack`

  ```swifttest
  -> struct Stack<Element> {
        var items: [Element] = []
        mutating func push(_ item: Element) {
           items.append(item)
        }
        mutating func pop() -> Element {
           return items.removeLast()
        }
     }
  ```
-->

Repare que a versão genérica de `Stack`
é basicamente a mesma que a versão não genérica,
mas com um parâmetro de tipo chamado `Element`
no lugar de um tipo real como `Int`.
Esse parâmetro de tipo é escrito dentro de um par de colchetes angulares (`<Element>`)
logo depois do nome da struct.

`Element` define um nome marcador para
um tipo que será fornecido depois.
Esse tipo futuro pode ser referenciado como `Element`
em qualquer lugar da definição da struct.
Nesse caso, `Element` é usado como marcador em três lugares:

- Para criar uma propriedade chamada `items`,
  que é inicializada com um array vazio de valores do tipo `Element`
- Para especificar que o método `push(_:)` tem um único parâmetro chamado `item`,
  que precisa ser do tipo `Element`
- Para especificar que o valor retornado pelo método `pop()`
  será um valor do tipo `Element`

Como é um tipo genérico,
`Stack` pode ser usado para criar uma pilha de *qualquer* tipo válido em Swift,
de forma parecida com `Array` e `Dictionary`.

Você cria uma nova instância de `Stack` escrevendo
o tipo a ser armazenado na pilha entre colchetes angulares.
Por exemplo, para criar uma nova pilha de strings,
você escreve `Stack<String>()`:

```swift
var stackOfStrings = Stack<String>()
stackOfStrings.push("uno")
stackOfStrings.push("dos")
stackOfStrings.push("tres")
stackOfStrings.push("cuatro")
// the stack now contains 4 strings
```

<!--
  - test: `genericStack`

  ```swifttest
  -> var stackOfStrings = Stack<String>()
  -> stackOfStrings.push("uno")
  -> stackOfStrings.push("dos")
  -> stackOfStrings.push("tres")
  -> stackOfStrings.push("cuatro")
  /> the stack now contains \(stackOfStrings.items.count) strings
  </ the stack now contains 4 strings
  ```
-->

Veja como fica `stackOfStrings` depois de empilhar esses quatro valores:

![](stackPushedFourStrings)

Desempilhar um valor da pilha remove e retorna o valor do topo, `"cuatro"`:

```swift
let fromTheTop = stackOfStrings.pop()
// fromTheTop is equal to "cuatro", and the stack now contains 3 strings
```

<!--
  - test: `genericStack`

  ```swifttest
  -> let fromTheTop = stackOfStrings.pop()
  /> fromTheTop is equal to \"\(fromTheTop)\", and the stack now contains \(stackOfStrings.items.count) strings
  </ fromTheTop is equal to "cuatro", and the stack now contains 3 strings
  ```
-->

Veja como fica a pilha depois de desempilhar seu valor do topo:

![](stackPoppedOneString)

## Estendendo um tipo genérico

Ao estender um tipo genérico,
você não fornece uma lista de parâmetros de tipo como parte da definição da extension.
Em vez disso, a lista de parâmetros de tipo da definição *original*
fica disponível dentro do corpo da extension,
e os nomes originais dos parâmetros de tipo são usados para se referir
aos parâmetros de tipo da definição original.

O exemplo a seguir estende o tipo genérico `Stack` para adicionar
uma propriedade computada somente leitura chamada `topItem`,
que retorna o item do topo da pilha sem removê-lo da pilha:

```swift
extension Stack {
    var topItem: Element? {
        return items.isEmpty ? nil : items[items.count - 1]
    }
}
```

<!--
  - test: `genericStack`

  ```swifttest
  -> extension Stack {
        var topItem: Element? {
           return items.isEmpty ? nil : items[items.count - 1]
        }
     }
  ```
-->

A propriedade `topItem` retorna um optional do tipo `Element`.
Se a pilha estiver vazia, `topItem` retorna `nil`;
se a pilha não estiver vazia, `topItem` retorna o último item do array `items`.

Observe que essa extension não define uma lista de parâmetros de tipo.
Em vez disso, o nome do parâmetro de tipo que já existe no tipo `Stack`, `Element`,
é usado dentro da extension para indicar o tipo optional da
propriedade computada `topItem`.

A propriedade computada `topItem` agora pode ser usada com qualquer instância de `Stack`
para acessar e consultar o item do topo sem removê-lo.

```swift
if let topItem = stackOfStrings.topItem {
    print("The top item on the stack is \(topItem).")
}
// Prints "The top item on the stack is tres."
```

<!--
  - test: `genericStack`

  ```swifttest
  -> if let topItem = stackOfStrings.topItem {
        print("The top item on the stack is \(topItem).")
     }
  <- The top item on the stack is tres.
  ```
-->

Extensions de um tipo genérico também podem incluir requisitos
que as instâncias do tipo estendido precisam satisfazer
para ganhar a nova funcionalidade,
como discutido em <doc:Generics#Extensions-with-a-Generic-Where-Clause> abaixo.

## Restrições de tipo

A função `swapTwoValues(_:_:)` e o tipo `Stack` podem trabalhar com qualquer tipo.
No entanto, às vezes é útil impor
certas *restrições de tipo* aos tipos que podem ser usados com
funções genéricas e tipos genéricos.
Restrições de tipo especificam que um parâmetro de tipo precisa
herdar de uma classe específica,
ou estar em conformidade com um protocolo ou uma composição de protocolos específica.

Por exemplo,
o tipo `Dictionary` do Swift impõe uma limitação sobre
os tipos que podem ser usados como chaves de um dicionário.
Como descrito em <doc:CollectionTypes#Dictionaries>,
o tipo das chaves de um dicionário precisa ser *hashable*.
Ou seja, precisa fornecer uma forma de se tornar representável de maneira única.
`Dictionary` precisa que suas chaves sejam hashable para que ele possa
verificar se já contém um valor para uma chave específica.
Sem esse requisito, `Dictionary` não conseguiria saber
se deve inserir ou substituir um valor para uma chave específica,
nem conseguiria encontrar o valor de uma chave dada que já está no dicionário.

Esse requisito é imposto por uma restrição de tipo sobre o tipo da chave de `Dictionary`,
que especifica que o tipo da chave precisa estar em conformidade com o protocolo `Hashable`,
um protocolo especial definido na biblioteca padrão do Swift.
Todos os tipos básicos do Swift (como `String`, `Int`, `Double` e `Bool`)
são hashable por padrão.
Para informações sobre
como fazer seus próprios tipos personalizados estarem em conformidade com o protocolo `Hashable`,
veja [Conformidade com o protocolo Hashable](https://developer.apple.com/documentation/swift/hashable#Conforming-to-the-Hashable-Protocol).

Você pode definir suas próprias restrições de tipo ao criar tipos genéricos personalizados,
e essas restrições fornecem boa parte do poder da programação genérica.
Conceitos abstratos como `Hashable`
caracterizam tipos em termos de suas características conceituais,
em vez do tipo concreto.

### Sintaxe de restrições de tipo

Você escreve restrições de tipo colocando uma única restrição de classe ou de protocolo
depois do nome de um parâmetro de tipo, separada por dois-pontos,
como parte da lista de parâmetros de tipo.
A sintaxe básica para restrições de tipo em uma função genérica é mostrada abaixo
(embora a sintaxe seja a mesma para tipos genéricos):

```swift
func someFunction<T: SomeClass, U: SomeProtocol>(someT: T, someU: U) {
    // function body goes here
}
```

<!--
  - test: `typeConstraints`

  ```swifttest
  >> class SomeClass {}
  >> protocol SomeProtocol {}
  -> func someFunction<T: SomeClass, U: SomeProtocol>(someT: T, someU: U) {
        // function body goes here
     }
  ```
-->

A função hipotética acima tem dois parâmetros de tipo.
O primeiro parâmetro de tipo, `T`, tem uma restrição de tipo
que exige que `T` seja uma subclasse de `SomeClass`.
O segundo parâmetro de tipo, `U`, tem uma restrição de tipo
que exige que `U` esteja em conformidade com o protocolo `SomeProtocol`.

### Restrições de tipo na prática

Aqui está uma função não genérica chamada `findIndex(ofString:in:)`,
que recebe um valor `String` a ser procurado
e um array de valores `String` em que fazer a busca.
A função `findIndex(ofString:in:)` retorna um `Int` optional,
que será o índice da primeira string correspondente no array, se ela for encontrada,
ou `nil` se a string não puder ser encontrada:

```swift
func findIndex(ofString valueToFind: String, in array: [String]) -> Int? {
    for (index, value) in array.enumerated() {
        if value == valueToFind {
            return index
        }
    }
    return nil
}
```

<!--
  - test: `typeConstraints`

  ```swifttest
  -> func findIndex(ofString valueToFind: String, in array: [String]) -> Int? {
        for (index, value) in array.enumerated() {
           if value == valueToFind {
              return index
           }
        }
        return nil
     }
  ```
-->

A função `findIndex(ofString:in:)` pode ser usada para encontrar um valor string em um array de strings:

```swift
let strings = ["cat", "dog", "llama", "parakeet", "terrapin"]
if let foundIndex = findIndex(ofString: "llama", in: strings) {
    print("The index of llama is \(foundIndex)")
}
// Prints "The index of llama is 2".
```

<!--
  - test: `typeConstraints`

  ```swifttest
  -> let strings = ["cat", "dog", "llama", "parakeet", "terrapin"]
  -> if let foundIndex = findIndex(ofString: "llama", in: strings) {
        print("The index of llama is \(foundIndex)")
     }
  <- The index of llama is 2
  ```
-->

O princípio de encontrar o índice de um valor em um array, porém, não é útil apenas para strings.
Você pode escrever a mesma funcionalidade como uma função genérica,
substituindo qualquer menção a strings por valores de algum tipo `T`.

Veja como você poderia esperar que uma versão genérica de `findIndex(ofString:in:)`,
chamada `findIndex(of:in:)`, fosse escrita.
Observe que o tipo de retorno dessa função continua sendo `Int?`,
pois a função retorna um número de índice optional,
não um optional do array.
Atenção, porém: essa função não compila,
pelos motivos explicados depois do exemplo:

```swift
func findIndex<T>(of valueToFind: T, in array:[T]) -> Int? {
    for (index, value) in array.enumerated() {
        if value == valueToFind {
            return index
        }
    }
    return nil
}
```

<!--
  - test: `typeConstraints-err`

  ```swifttest
  -> func findIndex<T>(of valueToFind: T, in array:[T]) -> Int? {
        for (index, value) in array.enumerated() {
           if value == valueToFind {
              return index
           }
        }
        return nil
     }
  !$ error: binary operator '==' cannot be applied to two 'T' operands
  !!       if value == valueToFind {
  !!          ~~~~~ ^  ~~~~~~~~~~~
  ```
-->

Essa função não compila como escrita acima.
O problema está na verificação de igualdade, “`if value == valueToFind`”.
Nem todo tipo em Swift pode ser comparado com o operador de igualdade (`==`).
Se você criar sua própria classe ou struct para representar um modelo de dados complexo, por exemplo,
então o significado de “igual a” para essa classe ou struct
não é algo que o Swift consegue adivinhar por você.
Por isso, não é possível garantir que esse código vai funcionar
para *todo* tipo possível `T`,
e o compilador reporta um erro apropriado quando você tenta compilar o código.

Nem tudo está perdido, porém.
A biblioteca padrão do Swift define um protocolo chamado `Equatable`,
que exige que qualquer tipo em conformidade implemente
o operador de igualdade (`==`) e o operador de desigualdade (`!=`)
para comparar quaisquer dois valores daquele tipo.
Todos os tipos padrão do Swift adotam automaticamente o protocolo `Equatable`.

<!--
  TODO: write about how to make your own types conform to Equatable
  once we have some documentation that actually describes it.
  The text to use is something like:
  and you can make your own types conform to ``Equatable`` too,
  as described in <link>.
-->

Qualquer tipo que seja `Equatable` pode ser usado com segurança na função `findIndex(of:in:)`,
pois é garantido que ele oferece suporte ao operador de igualdade.
Para expressar isso, você escreve uma restrição de tipo de `Equatable`
como parte da definição do parâmetro de tipo ao definir a função:

```swift
func findIndex<T: Equatable>(of valueToFind: T, in array:[T]) -> Int? {
    for (index, value) in array.enumerated() {
        if value == valueToFind {
            return index
        }
    }
    return nil
}
```

<!--
  - test: `typeConstraintsEquatable`

  ```swifttest
  -> func findIndex<T: Equatable>(of valueToFind: T, in array:[T]) -> Int? {
        for (index, value) in array.enumerated() {
           if value == valueToFind {
              return index
           }
        }
        return nil
     }
  ```
-->

O único parâmetro de tipo de `findIndex(of:in:)` é escrito como `T: Equatable`,
o que significa “qualquer tipo `T` que esteja em conformidade com o protocolo `Equatable`.”

A função `findIndex(of:in:)` agora compila com sucesso
e pode ser usada com qualquer tipo que seja `Equatable`, como `Double` ou `String`:

```swift
let doubleIndex = findIndex(of: 9.3, in: [3.14159, 0.1, 0.25])
// doubleIndex is an optional Int with no value, because 9.3 isn't in the array
let stringIndex = findIndex(of: "Andrea", in: ["Mike", "Malcolm", "Andrea"])
// stringIndex is an optional Int containing a value of 2
```

<!--
  - test: `typeConstraintsEquatable`

  ```swifttest
  -> let doubleIndex = findIndex(of: 9.3, in: [3.14159, 0.1, 0.25])
  /> doubleIndex is an optional Int with no value, because 9.3 isn't in the array
  </ doubleIndex is an optional Int with no value, because 9.3 isn't in the array
  -> let stringIndex = findIndex(of: "Andrea", in: ["Mike", "Malcolm", "Andrea"])
  /> stringIndex is an optional Int containing a value of \(stringIndex!)
  </ stringIndex is an optional Int containing a value of 2
  ```
-->

<!--
  TODO: providing different type parameters on individual methods within a generic type
-->

<!--
  TODO: likewise providing type parameters for initializers
-->

## Tipos associados

Ao definir um protocolo,
às vezes é útil declarar um ou mais tipos associados
como parte da definição do protocolo.
Um *tipo associado* dá um nome marcador
a um tipo que é usado como parte do protocolo.
O tipo real a ser usado para esse tipo associado
não é especificado até que o protocolo seja adotado.
Tipos associados são especificados com a palavra-chave `associatedtype`.

### Tipos associados na prática

Aqui está um exemplo de um protocolo chamado `Container`,
que declara um tipo associado chamado `Item`:

```swift
protocol Container {
    associatedtype Item
    mutating func append(_ item: Item)
    var count: Int { get }
    subscript(i: Int) -> Item { get }
}
```

<!--
  - test: `associatedTypes, associatedTypes-err`

  ```swifttest
  -> protocol Container {
        associatedtype Item
        mutating func append(_ item: Item)
        var count: Int { get }
        subscript(i: Int) -> Item { get }
     }
  ```
-->

O protocolo `Container` define três capacidades obrigatórias
que qualquer contêiner precisa fornecer:

- Deve ser possível adicionar um novo item ao contêiner com um método `append(_:)`.
- Deve ser possível acessar a quantidade de itens do contêiner
  por meio de uma propriedade `count` que retorna um valor `Int`.
- Deve ser possível recuperar cada item do contêiner com um subscript
  que recebe um índice `Int`.

Esse protocolo não especifica como os itens do contêiner devem ser armazenados
nem qual tipo eles podem ter.
O protocolo especifica apenas as três funcionalidades
que qualquer tipo precisa fornecer para ser considerado um `Container`.
Um tipo em conformidade pode fornecer funcionalidades adicionais,
contanto que satisfaça esses três requisitos.

Qualquer tipo que esteja em conformidade com o protocolo `Container` precisa conseguir especificar
o tipo dos valores que armazena.
Especificamente, precisa garantir que apenas itens do tipo certo
sejam adicionados ao contêiner,
e precisa deixar claro o tipo dos itens retornados pelo seu subscript.

Para definir esses requisitos,
o protocolo `Container` precisa de uma forma de se referir
ao tipo dos elementos que um contêiner vai guardar,
sem saber qual é esse tipo para um contêiner específico.
O protocolo `Container` precisa especificar que
qualquer valor passado ao método `append(_:)`
deve ter o mesmo tipo do tipo de elemento do contêiner,
e que o valor retornado pelo subscript do contêiner
será do mesmo tipo do tipo de elemento do contêiner.

Para isso,
o protocolo `Container` declara um tipo associado chamado `Item`,
escrito como `associatedtype Item`.
O protocolo não define o que `Item` é ---
essa informação fica para qualquer tipo em conformidade fornecer.
Mesmo assim, o alias `Item` oferece uma forma de se referir
ao tipo dos itens de um `Container`,
e de definir um tipo para uso com o método `append(_:)` e o subscript,
para garantir que o comportamento esperado de qualquer `Container` seja respeitado.

Aqui está uma versão do tipo não genérico `IntStack`
vista em <doc:Generics#Generic-Types> acima,
adaptada para estar em conformidade com o protocolo `Container`:

```swift
struct IntStack: Container {
    // original IntStack implementation
    var items: [Int] = []
    mutating func push(_ item: Int) {
        items.append(item)
    }
    mutating func pop() -> Int {
        return items.removeLast()
    }
    // conformance to the Container protocol
    typealias Item = Int
    mutating func append(_ item: Int) {
        self.push(item)
    }
    var count: Int {
        return items.count
    }
    subscript(i: Int) -> Int {
        return items[i]
    }
}
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> struct IntStack: Container {
        // original IntStack implementation
        var items: [Int] = []
        mutating func push(_ item: Int) {
           items.append(item)
        }
        mutating func pop() -> Int {
           return items.removeLast()
        }
        // conformance to the Container protocol
        typealias Item = Int
        mutating func append(_ item: Int) {
           self.push(item)
        }
        var count: Int {
           return items.count
        }
        subscript(i: Int) -> Int {
           return items[i]
        }
     }
  ```
-->

O tipo `IntStack` implementa os três requisitos do protocolo `Container`,
e em cada caso encapsula parte da funcionalidade já existente do tipo `IntStack`
para satisfazer esses requisitos.

Além disso, `IntStack` especifica que, para essa implementação de `Container`,
o `Item` apropriado a ser usado é do tipo `Int`.
A definição `typealias Item = Int` transforma o tipo abstrato `Item`
em um tipo concreto `Int` para essa implementação do protocolo `Container`.

Graças à inferência de tipos do Swift,
você não precisa declarar de fato um `Item` concreto como `Int`
como parte da definição de `IntStack`.
Como `IntStack` está em conformidade com todos os requisitos do protocolo `Container`,
o Swift consegue inferir o `Item` apropriado a ser usado,
simplesmente observando o tipo do parâmetro `item` do método `append(_:)`
e o tipo de retorno do subscript.
De fato, se você apagar a linha `typealias Item = Int` do código acima,
tudo continua funcionando, porque fica claro qual tipo deve ser usado para `Item`.

Você também pode fazer o tipo genérico `Stack` estar em conformidade com o protocolo `Container`:

```swift
struct Stack<Element>: Container {
    // original Stack<Element> implementation
    var items: [Element] = []
    mutating func push(_ item: Element) {
        items.append(item)
    }
    mutating func pop() -> Element {
        return items.removeLast()
    }
    // conformance to the Container protocol
    mutating func append(_ item: Element) {
        self.push(item)
    }
    var count: Int {
        return items.count
    }
    subscript(i: Int) -> Element {
        return items[i]
    }
}
```

<!--
  - test: `associatedTypes, associatedTypes-err`

  ```swifttest
  -> struct Stack<Element>: Container {
        // original Stack<Element> implementation
        var items: [Element] = []
        mutating func push(_ item: Element) {
           items.append(item)
        }
        mutating func pop() -> Element {
           return items.removeLast()
        }
        // conformance to the Container protocol
        mutating func append(_ item: Element) {
           self.push(item)
        }
        var count: Int {
           return items.count
        }
        subscript(i: Int) -> Element {
           return items[i]
        }
     }
  ```
-->

Dessa vez, o parâmetro de tipo `Element` é usado como
o tipo do parâmetro `item` do método `append(_:)`
e o tipo de retorno do subscript.
Por isso, o Swift consegue inferir que `Element` é o tipo apropriado a ser usado
como `Item` para esse contêiner específico.

### Estendendo um tipo existente para especificar um tipo associado

Você pode estender um tipo existente para adicionar conformidade a um protocolo,
como descrito em <doc:Protocols#Adding-Protocol-Conformance-with-an-Extension>.
Isso inclui um protocolo com um tipo associado.

O tipo `Array` do Swift já fornece um método `append(_:)`,
uma propriedade `count` e um subscript com índice `Int` para recuperar seus elementos.
Essas três capacidades correspondem aos requisitos do protocolo `Container`.
Isso significa que você pode estender `Array` para estar em conformidade com o protocolo `Container`
simplesmente declarando que `Array` adota o protocolo.
Você faz isso com uma extension vazia,
como descrito em <doc:Protocols#Declaring-Protocol-Adoption-with-an-Extension>:

```swift
extension Array: Container {}
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> extension Array: Container {}
  ```
-->

O método `append(_:)` e o subscript já existentes em `Array` permitem que o Swift infira
o tipo apropriado a ser usado para `Item`,
assim como para o tipo genérico `Stack` acima.
Depois de definir essa extension, você pode usar qualquer `Array` como `Container`.

### Adicionando restrições a um tipo associado

Você pode adicionar restrições de tipo a um tipo associado em um protocolo
para exigir que os tipos em conformidade satisfaçam essas restrições.
Por exemplo,
o código a seguir define uma versão de `Container`
que exige que os itens do contêiner sejam `Equatable`.

```swift
protocol Container {
    associatedtype Item: Equatable
    mutating func append(_ item: Item)
    var count: Int { get }
    subscript(i: Int) -> Item { get }
}
```

<!--
  - test: `associatedTypes-equatable`

  ```swifttest
  -> protocol Container {
        associatedtype Item: Equatable
        mutating func append(_ item: Item)
        var count: Int { get }
        subscript(i: Int) -> Item { get }
     }
  ```
-->

Para estar em conformidade com essa versão de `Container`,
o tipo `Item` do contêiner precisa estar em conformidade com o protocolo `Equatable`.

### Usando um protocolo nas restrições do seu próprio tipo associado

Um protocolo pode aparecer como parte dos seus próprios requisitos.
Por exemplo,
aqui está um protocolo que refina o protocolo `Container`,
adicionando o requisito de um método `suffix(_:)`.
O método `suffix(_:)`
retorna uma quantidade informada de elementos do fim do contêiner,
armazenando-os em uma instância do tipo `Suffix`.

```swift
protocol SuffixableContainer: Container {
    associatedtype Suffix: SuffixableContainer where Suffix.Item == Item
    func suffix(_ size: Int) -> Suffix
}
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> protocol SuffixableContainer: Container {
         associatedtype Suffix: SuffixableContainer where Suffix.Item == Item
         func suffix(_ size: Int) -> Suffix
     }
  ```
-->

Nesse protocolo,
`Suffix` é um tipo associado,
assim como o tipo `Item` no exemplo `Container` acima.
`Suffix` tem duas restrições:
ele precisa estar em conformidade com o protocolo `SuffixableContainer`
(o protocolo que está sendo definido agora),
e seu tipo `Item` precisa ser o mesmo
que o tipo `Item` do contêiner.
A restrição sobre `Item` é uma cláusula `where` genérica,
que é discutida em <doc:Generics#Associated-Types-with-a-Generic-Where-Clause> abaixo.

Aqui está uma extension do tipo `Stack`
visto em <doc:Generics#Generic-Types> acima
que adiciona conformidade ao protocolo `SuffixableContainer`:

```swift
extension Stack: SuffixableContainer {
    func suffix(_ size: Int) -> Stack {
        var result = Stack()
        for index in (count-size)..<count {
            result.append(self[index])
        }
        return result
    }
    // Inferred that Suffix is Stack.
}
var stackOfInts = Stack<Int>()
stackOfInts.append(10)
stackOfInts.append(20)
stackOfInts.append(30)
let suffix = stackOfInts.suffix(2)
// suffix contains 20 and 30
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> extension Stack: SuffixableContainer {
         func suffix(_ size: Int) -> Stack {
             var result = Stack()
             for index in (count-size)..<count {
                 result.append(self[index])
             }
             return result
         }
         // Inferred that Suffix is Stack.
     }
  -> var stackOfInts = Stack<Int>()
  -> stackOfInts.append(10)
  -> stackOfInts.append(20)
  -> stackOfInts.append(30)
  >> assert(stackOfInts.suffix(0).items == [])
  -> let suffix = stackOfInts.suffix(2)
  // suffix contains 20 and 30
  >> assert(suffix.items == [20, 30])
  ```
-->

No exemplo acima,
o tipo associado `Suffix` de `Stack` também é `Stack`,
então a operação de sufixo em `Stack` retorna outro `Stack`.
Como alternativa,
um tipo que está em conformidade com `SuffixableContainer`
pode ter um tipo `Suffix` diferente de si mesmo ---
ou seja, a operação de sufixo pode retornar um tipo diferente.
Por exemplo,
aqui está uma extension do tipo não genérico `IntStack`
que adiciona conformidade com `SuffixableContainer`,
usando `Stack<Int>` como seu tipo de sufixo no lugar de `IntStack`:

```swift
extension IntStack: SuffixableContainer {
    func suffix(_ size: Int) -> Stack<Int> {
        var result = Stack<Int>()
        for index in (count-size)..<count {
            result.append(self[index])
        }
        return result
    }
    // Inferred that Suffix is Stack<Int>.
}
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> extension IntStack: SuffixableContainer {
         func suffix(_ size: Int) -> Stack<Int> {
             var result = Stack<Int>()
             for index in (count-size)..<count {
                 result.append(self[index])
             }
             return result
         }
         // Inferred that Suffix is Stack<Int>.
     }
  >> var intStack = IntStack()
  >> intStack.append(10)
  >> intStack.append(20)
  >> intStack.append(30)
  >> assert(intStack.suffix(0).items == [])
  >> assert(intStack.suffix(2).items == [20, 30])
  ```
-->

## Cláusulas where genéricas

Restrições de tipo, como descritas em <doc:Generics#Type-Constraints>,
permitem definir requisitos sobre os parâmetros de tipo associados a
uma função genérica, um subscript ou um tipo genérico.

Também pode ser útil definir requisitos para tipos associados.
Você faz isso definindo uma *cláusula where genérica*.
Uma cláusula `where` genérica permite exigir que
um tipo associado esteja em conformidade com determinado protocolo,
ou que certos parâmetros de tipo e tipos associados sejam iguais.
Uma cláusula `where` genérica começa com a palavra-chave `where`,
seguida de restrições para tipos associados
ou de relações de igualdade entre tipos e tipos associados.
Você escreve uma cláusula `where` genérica logo antes da chave de abertura
do corpo de um tipo ou de uma função.

O exemplo abaixo define uma função genérica chamada `allItemsMatch`,
que verifica se duas instâncias de `Container` contêm
os mesmos itens na mesma ordem.
A função retorna o valor booleano `true` se todos os itens coincidirem
e o valor `false` se não coincidirem.

Os dois contêineres a serem comparados não precisam ser
do mesmo tipo de contêiner (embora possam ser),
mas precisam guardar o mesmo tipo de itens.
Essa exigência é expressa por uma combinação de restrições de tipo
e uma cláusula `where` genérica:

```swift
func allItemsMatch<C1: Container, C2: Container>
        (_ someContainer: C1, _ anotherContainer: C2) -> Bool
        where C1.Item == C2.Item, C1.Item: Equatable {

    // Check that both containers contain the same number of items.
    if someContainer.count != anotherContainer.count {
        return false
    }

    // Check each pair of items to see if they're equivalent.
    for i in 0..<someContainer.count {
        if someContainer[i] != anotherContainer[i] {
            return false
        }
    }

    // All items match, so return true.
    return true
}
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> func allItemsMatch<C1: Container, C2: Container>
           (_ someContainer: C1, _ anotherContainer: C2) -> Bool
           where C1.Item == C2.Item, C1.Item: Equatable {

        // Check that both containers contain the same number of items.
        if someContainer.count != anotherContainer.count {
           return false
        }

        // Check each pair of items to see if they're equivalent.
        for i in 0..<someContainer.count {
           if someContainer[i] != anotherContainer[i] {
              return false
           }
        }

        // All items match, so return true.
        return true
     }
  ```
-->

Essa função recebe dois argumentos chamados
`someContainer` e `anotherContainer`.
O argumento `someContainer` é do tipo `C1`,
e o argumento `anotherContainer` é do tipo `C2`.
Tanto `C1` quanto `C2` são parâmetros de tipo
para dois tipos de contêiner que serão determinados quando a função for chamada.

Os seguintes requisitos são impostos aos dois parâmetros de tipo da função:

- `C1` precisa estar em conformidade com o protocolo `Container` (escrito como `C1: Container`).
- `C2` também precisa estar em conformidade com o protocolo `Container` (escrito como `C2: Container`).
- O `Item` de `C1` precisa ser o mesmo que o `Item` de `C2`
  (escrito como `C1.Item == C2.Item`).
- O `Item` de `C1` precisa estar em conformidade com o protocolo `Equatable`
  (escrito como `C1.Item: Equatable`).

O primeiro e o segundo requisitos são definidos na lista de parâmetros de tipo da função,
e o terceiro e o quarto requisitos são definidos na cláusula `where` genérica da função.

Esses requisitos significam:

- `someContainer` é um contêiner do tipo `C1`.
- `anotherContainer` é um contêiner do tipo `C2`.
- `someContainer` e `anotherContainer` guardam o mesmo tipo de itens.
- Os itens de `someContainer` podem ser comparados com o operador de desigualdade (`!=`)
  para verificar se são diferentes uns dos outros.

O terceiro e o quarto requisitos, juntos, significam que
os itens de `anotherContainer` *também* podem ser comparados com o operador `!=`,
pois são exatamente do mesmo tipo que os itens de `someContainer`.

Esses requisitos permitem que a função `allItemsMatch(_:_:)` compare os dois contêineres,
mesmo que sejam de tipos de contêiner diferentes.

A função `allItemsMatch(_:_:)` começa verificando se
os dois contêineres têm a mesma quantidade de itens.
Se tiverem quantidades diferentes, não há como coincidirem,
e a função retorna `false`.

Depois dessa verificação, a função percorre todos os itens de `someContainer`
com um laço `for`-`in` e o operador de intervalo semiaberto (`..<`).
Para cada item, a função verifica se o item de `someContainer` é diferente
do item correspondente em `anotherContainer`.
Se os dois itens forem diferentes, os dois contêineres não coincidem,
e a função retorna `false`.

Se o laço terminar sem encontrar uma diferença,
os dois contêineres coincidem, e a função retorna `true`.

Veja como a função `allItemsMatch(_:_:)` funciona na prática:

```swift
var stackOfStrings = Stack<String>()
stackOfStrings.push("uno")
stackOfStrings.push("dos")
stackOfStrings.push("tres")

var arrayOfStrings = ["uno", "dos", "tres"]

if allItemsMatch(stackOfStrings, arrayOfStrings) {
    print("All items match.")
} else {
    print("Not all items match.")
}
// Prints "All items match."
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> var stackOfStrings = Stack<String>()
  -> stackOfStrings.push("uno")
  -> stackOfStrings.push("dos")
  -> stackOfStrings.push("tres")

  -> var arrayOfStrings = ["uno", "dos", "tres"]

  -> if allItemsMatch(stackOfStrings, arrayOfStrings) {
        print("All items match.")
     } else {
        print("Not all items match.")
     }
  <- All items match.
  ```
-->

O exemplo acima cria uma instância de `Stack` para guardar valores `String`,
e empilha três strings na pilha.
O exemplo também cria uma instância de `Array` inicializada com
um array literal que contém as mesmas três strings da pilha.
Mesmo que a pilha e o array sejam de tipos diferentes,
ambos estão em conformidade com o protocolo `Container`,
e ambos guardam o mesmo tipo de valores.
Por isso, você pode chamar a função `allItemsMatch(_:_:)`
com esses dois contêineres como argumentos.
No exemplo acima, a função `allItemsMatch(_:_:)` informa corretamente que
todos os itens dos dois contêineres coincidem.

## Extensions com cláusula where genérica

Você também pode usar uma cláusula `where` genérica como parte de uma extension.
O exemplo abaixo
estende a struct genérica `Stack` dos exemplos anteriores
para adicionar um método `isTop(_:)`.

```swift
extension Stack where Element: Equatable {
    func isTop(_ item: Element) -> Bool {
        guard let topItem = items.last else {
            return false
        }
        return topItem == item
    }
}
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> extension Stack where Element: Equatable {
         func isTop(_ item: Element) -> Bool {
             guard let topItem = items.last else {
                 return false
             }
             return topItem == item
         }
     }
  ```
-->

Esse novo método `isTop(_:)`
primeiro verifica se a pilha não está vazia,
e depois compara o item informado
com o item do topo da pilha.
Se você tentasse fazer isso sem uma cláusula `where` genérica,
teria um problema:
a implementação de `isTop(_:)` usa o operador `==`,
mas a definição de `Stack` não exige
que seus itens sejam `Equatable`,
então usar o operador `==` resulta em um erro de compilação.
Usar uma cláusula `where` genérica
permite adicionar um novo requisito à extension,
de modo que a extension adicione o método `isTop(_:)`
apenas quando os itens da pilha forem `Equatable`.

Veja como o método `isTop(_:)` funciona na prática:

```swift
if stackOfStrings.isTop("tres") {
    print("Top element is tres.")
} else {
    print("Top element is something else.")
}
// Prints "Top element is tres."
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> if stackOfStrings.isTop("tres") {
        print("Top element is tres.")
     } else {
        print("Top element is something else.")
     }
  <- Top element is tres.
  ```
-->

Se você tentar chamar o método `isTop(_:)`
em uma pilha cujos elementos não são `Equatable`,
você receberá um erro de compilação.

```swift
struct NotEquatable { }
var notEquatableStack = Stack<NotEquatable>()
let notEquatableValue = NotEquatable()
notEquatableStack.push(notEquatableValue)
notEquatableStack.isTop(notEquatableValue)  // Error
```

<!--
  - test: `associatedTypes-err`

  ```swifttest
  -> struct NotEquatable { }
  -> var notEquatableStack = Stack<NotEquatable>()
  -> let notEquatableValue = NotEquatable()
  -> notEquatableStack.push(notEquatableValue)
  -> notEquatableStack.isTop(notEquatableValue)  // Error
  !$ error: value of type 'Stack<NotEquatable>' has no member 'isTop'
  !! notEquatableStack.isTop(notEquatableValue)  // Error
  !! ~~~~~~~~~~~~~~~~~ ^~~~~
  ```
-->

Você pode usar uma cláusula `where` genérica com extensions de um protocolo.
O exemplo abaixo estende o protocolo `Container` dos exemplos anteriores
para adicionar um método `startsWith(_:)`.

```swift
extension Container where Item: Equatable {
    func startsWith(_ item: Item) -> Bool {
        return count >= 1 && self[0] == item
    }
}
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> extension Container where Item: Equatable {
        func startsWith(_ item: Item) -> Bool {
           return count >= 1 && self[0] == item
        }
     }
  ```
-->

<!--
  Using Container rather than Sequence/Collection
  to continue running with the same example through the chapter.
  This does, however, mean I can't use a for-in loop.
-->

O método `startsWith(_:)`
primeiro garante que o contêiner tenha pelo menos um item,
e depois verifica
se o primeiro item do contêiner corresponde ao item informado.
Esse novo método `startsWith(_:)`
pode ser usado com qualquer tipo que esteja em conformidade com o protocolo `Container`,
inclusive as pilhas e os arrays usados acima,
contanto que os itens do contêiner sejam `Equatable`.

```swift
if [9, 9, 9].startsWith(42) {
    print("Starts with 42.")
} else {
    print("Starts with something else.")
}
// Prints "Starts with something else."
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> if [9, 9, 9].startsWith(42) {
        print("Starts with 42.")
     } else {
        print("Starts with something else.")
     }
  <- Starts with something else.
  ```
-->

A cláusula `where` genérica do exemplo acima
exige que `Item` esteja em conformidade com um protocolo,
mas você também pode escrever cláusulas `where` genéricas que exigem que `Item`
seja um tipo específico.
Por exemplo:

```swift
extension Container where Item == Double {
    func average() -> Double {
        var sum = 0.0
        for index in 0..<count {
            sum += self[index]
        }
        return sum / Double(count)
    }
}
print([1260.0, 1200.0, 98.6, 37.0].average())
// Prints "648.9".
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> extension Container where Item == Double {
         func average() -> Double {
             var sum = 0.0
             for index in 0..<count {
                 sum += self[index]
             }
             return sum / Double(count)
         }
     }
  -> print([1260.0, 1200.0, 98.6, 37.0].average())
  <- 648.9
  ```
-->

Este exemplo adiciona um método `average()`
aos contêineres cujo tipo `Item` é `Double`.
Ele percorre os itens do contêiner para somá-los,
e divide pela quantidade do contêiner para calcular a média.
Ele converte explicitamente a quantidade de `Int` para `Double`
para conseguir fazer divisão de ponto flutuante.

Você pode incluir vários requisitos em uma cláusula `where` genérica
que faz parte de uma extension,
assim como pode fazer em uma cláusula `where` genérica escrita em outro lugar.
Separe cada requisito da lista com uma vírgula.

<!--
  No example of a compound where clause
  because Container only has one generic part ---
  there isn't anything to write a second constraint for.
-->

## Cláusulas where contextuais

Você pode escrever uma cláusula `where` genérica
como parte de uma declaração que não tem restrições de tipo genérico próprias,
quando já está trabalhando no contexto de tipos genéricos.
Por exemplo,
você pode escrever uma cláusula `where` genérica
em um subscript de um tipo genérico
ou em um método de uma extension de um tipo genérico.
O protocolo `Container` é genérico,
e as cláusulas `where` do exemplo abaixo
especificam quais restrições de tipo precisam ser satisfeitas
para tornar esses novos métodos disponíveis em um contêiner.

```swift
extension Container {
    func average() -> Double where Item == Int {
        var sum = 0.0
        for index in 0..<count {
            sum += Double(self[index])
        }
        return sum / Double(count)
    }
    func endsWith(_ item: Item) -> Bool where Item: Equatable {
        return count >= 1 && self[count-1] == item
    }
}
let numbers = [1260, 1200, 98, 37]
print(numbers.average())
// Prints "648.75".
print(numbers.endsWith(37))
// Prints "true".
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> extension Container {
         func average() -> Double where Item == Int {
             var sum = 0.0
             for index in 0..<count {
                 sum += Double(self[index])
             }
             return sum / Double(count)
         }
         func endsWith(_ item: Item) -> Bool where Item: Equatable {
             return count >= 1 && self[count-1] == item
         }
     }
  -> let numbers = [1260, 1200, 98, 37]
  -> print(numbers.average())
  <- 648.75
  -> print(numbers.endsWith(37))
  <- true
  ```
-->

Este exemplo
adiciona um método `average()` a `Container` quando os itens são inteiros,
e adiciona um método `endsWith(_:)` quando os itens são `Equatable`.
Ambas as funções incluem uma cláusula `where` genérica
que adiciona restrições de tipo ao parâmetro de tipo genérico `Item`
da declaração original de `Container`.

Se você quiser escrever esse código sem usar cláusulas `where` contextuais,
você escreveria duas extensions,
uma para cada cláusula `where` genérica.
O exemplo acima e o exemplo abaixo têm o mesmo comportamento.

```swift
extension Container where Item == Int {
    func average() -> Double {
        var sum = 0.0
        for index in 0..<count {
            sum += Double(self[index])
        }
        return sum / Double(count)
    }
}
extension Container where Item: Equatable {
    func endsWith(_ item: Item) -> Bool {
        return count >= 1 && self[count-1] == item
    }
}
```

<!--
  - test: `associatedTypes-err`

  ```swifttest
  -> extension Container where Item == Int {
         func average() -> Double {
             var sum = 0.0
             for index in 0..<count {
                 sum += Double(self[index])
             }
             return sum / Double(count)
         }
     }
     extension Container where Item: Equatable {
         func endsWith(_ item: Item) -> Bool {
             return count >= 1 && self[count-1] == item
         }
     }
  ```
-->

Na versão deste exemplo que usa cláusulas `where` contextuais,
a implementação de `average()` e de `endsWith(_:)`
ficam na mesma extension,
pois a cláusula `where` genérica de cada método
indica os requisitos que precisam ser satisfeitos
para que aquele método fique disponível.
Mover esses requisitos para as cláusulas `where` genéricas das extensions
torna os métodos disponíveis nas mesmas situações,
mas exige uma extension para cada requisito.

## Tipos associados com cláusula where genérica

Você pode incluir uma cláusula `where` genérica em um tipo associado.
Por exemplo, suponha que você queira criar uma versão de `Container`
que inclua um iterador,
como o que o protocolo `Sequence` usa na biblioteca padrão do Swift.
Veja como escrever isso:

```swift
protocol Container {
    associatedtype Item
    mutating func append(_ item: Item)
    var count: Int { get }
    subscript(i: Int) -> Item { get }

    associatedtype Iterator: IteratorProtocol where Iterator.Element == Item
    func makeIterator() -> Iterator
}
```

<!--
  - test: `associatedTypes-iterator`

  ```swifttest
  -> protocol Container {
        associatedtype Item
        mutating func append(_ item: Item)
        var count: Int { get }
        subscript(i: Int) -> Item { get }

        associatedtype Iterator: IteratorProtocol where Iterator.Element == Item
        func makeIterator() -> Iterator
     }
  ```
-->

<!--
  Adding makeIterator() to Container lets it conform to Sequence,
  although we don't call that out here.
-->

A cláusula `where` genérica em `Iterator` exige que
o iterador percorra elementos
do mesmo tipo de item dos itens do contêiner,
independentemente do tipo do iterador.
A função `makeIterator()` dá acesso ao iterador de um contêiner.

<!--
  This example requires SE-0157 Recursive protocol constraints
  which is tracked by rdar://20531108

   that accepts a ranged of indexes it its subscript
   and returns a subcontainer ---
   similar to how ``Collection`` works in the Swift standard library.

   .. testcode:: associatedTypes-subcontainer

      -> protocol Container {
            associatedtype Item
            associatedtype SubContainer: Container where SubContainer.Item == Item

            mutating func append(_ item: Item)
            var count: Int { get }
            subscript(i: Int) -> Item { get }
            subscript(range: Range<Int>) -> SubContainer { get }
         }

   The generic ``where`` clause on ``SubContainer`` requires that
   the subcontainer must have the same item type as the container has,
   regardless of what type the subcontainer is.
   The original container and the subcontainer
   could be represented by the same type
   or by different types.
   The new subscript that accepts a range
   uses this new associated type as its return value.
-->

Para um protocolo que herda de outro protocolo,
você adiciona uma restrição a um tipo associado herdado
incluindo a cláusula `where` genérica na declaração do protocolo.
Por exemplo, o código a seguir
declara um protocolo `ComparableContainer`
que exige que `Item` esteja em conformidade com `Comparable`:

```swift
protocol ComparableContainer: Container where Item: Comparable { }
```

<!--
  - test: `associatedTypes`

  ```swifttest
  -> protocol ComparableContainer: Container where Item: Comparable { }
  ```
-->

<!--
  This version throws a warning as of Swift commit de66b0c25c70:
  "redeclaration of associated type %0 from protocol %1 is better
  expressed as a 'where' clause on the protocol"

   -> protocol ComparableContainer: Container {
          associatedtype Item: Comparable
      }
-->

<!--
  Exercise the new container -- this might not actually be needed,
  and it adds a level of complexity.

  function < (lhs: ComparableContainer, rhs: ComparableContainer) -> Bool {
      // Sort empty containers before nonempty containers.
      if lhs.count == 0 {
          return true
      } else if rhs.count  == 0 {
          return false
      }

      // Sort nonempty containers by their first element.
      // (In real code, you would want to compare the second element
      // if the first elements are equal, and so on.)
      return lhs[0] < rhs[0]
  }
-->

## Subscripts genéricos

Subscripts podem ser genéricos,
e podem incluir cláusulas `where` genéricas.
Você escreve o nome do tipo marcador entre colchetes angulares depois de `subscript`,
e escreve uma cláusula `where` genérica logo antes da chave de abertura
do corpo do subscript.
Por exemplo:

<!--
  The paragraph above borrows the wording used to introduce
  generics and 'where' clauses earlier in this chapter.
-->

```swift
extension Container {
    subscript<Indices: Sequence>(indices: Indices) -> [Item]
            where Indices.Iterator.Element == Int {
        var result: [Item] = []
        for index in indices {
            result.append(self[index])
        }
        return result
    }
}
```

<!--
  - test: `genericSubscript`

  ```swifttest
  >> protocol Container {
  >>    associatedtype Item
  >>    mutating func append(_ item: Item)
  >>    var count: Int { get }
  >>    subscript(i: Int) -> Item { get }
  >> }
  -> extension Container {
         subscript<Indices: Sequence>(indices: Indices) -> [Item]
                 where Indices.Iterator.Element == Int {
             var result: [Item] = []
             for index in indices {
                 result.append(self[index])
             }
             return result
         }
     }
  ```
-->

<!--
  - test: `genericSubscript`

  ```swifttest
  >> struct IntStack: Container {
        // original IntStack implementation
        var items: [Int] = []
        mutating func push(_ item: Int) {
           items.append(item)
        }
        mutating func pop() -> Int {
           return items.removeLast()
        }
        // conformance to the Container protocol
        typealias Item = Int
        mutating func append(_ item: Int) {
           self.push(item)
        }
        var count: Int {
           return items.count
        }
        subscript(i: Int) -> Int {
           return items[i]
        }
     }
  >> var s = IntStack()
  >> s.push(10); s.push(20); s.push(30)
  >> let items = s[ [0, 2] ]
  >> assert(items == [10, 30])
  ```
-->

Essa extension do protocolo `Container`
adiciona um subscript que recebe uma sequência de índices
e retorna um array contendo os itens de cada índice informado.
Esse subscript genérico tem as seguintes restrições:

- O parâmetro genérico `Indices`, entre colchetes angulares,
  precisa ser um tipo que esteja em conformidade com o protocolo `Sequence`
  da biblioteca padrão do Swift.
- O subscript recebe um único parâmetro, `indices`,
  que é uma instância do tipo `Indices`.
- A cláusula `where` genérica exige
  que o iterador da sequência
  percorra elementos do tipo `Int`.
  Isso garante que os índices da sequência
  sejam do mesmo tipo dos índices usados em um contêiner.

Juntas, essas restrições significam que
o valor passado para o parâmetro `indices`
é uma sequência de inteiros.

## Restrições implícitas

Além das restrições que você escreve explicitamente,
muitos lugares do seu código genérico também exigem implicitamente
conformidade com alguns protocolos muito comuns, como [`Copyable`][].
<!-- When SE-0446 is implemented, add Escapable above. -->
Essas restrições genéricas que você não precisa escrever
são conhecidas como *restrições implícitas*.
Por exemplo, as duas declarações de função a seguir
exigem que `MyType` seja copiável:

[`Copyable`]: https://developer.apple.com/documentation/swift/copyable

```swift
function someFunction<MyType> { ... }
function someFunction<MyType: Copyable> { ... }
```

No código acima,
a primeira declaração tem uma restrição implícita,
e a segunda versão lista a conformidade explicitamente.
Na maioria dos códigos,
os tipos também estão implicitamente em conformidade com esses protocolos comuns.
Para mais informações,
veja <doc:Protocols#Implicit-Conformance-to-a-Protocol>.

Como a maioria dos tipos em Swift está em conformidade com esses protocolos,
escrevê-los quase em todo lugar seria repetitivo.
Em vez disso, marcando apenas as exceções,
você destaca os lugares que omitem uma restrição comum.
Para suprimir uma restrição implícita,
escreva o nome do protocolo com um til (`~`) na frente dele.
Você pode ler `~Copyable` como “talvez copiável” ---
essa restrição suprimida permite
tanto tipos copiáveis quanto tipos não copiáveis nessa posição.
Observe que `~Copyable` não *exige* que o tipo seja não copiável.
Por exemplo:

```swift
func f<MyType>(x: inout MyType) {
    let x1 = x  // The value of x1 is a copy of x's value.
    let x2 = x  // The value of x2 is a copy of x's value.
}

func g<AnotherType: ~Copyable>(y: inout AnotherType) {
    let y1 = y  // The assignment consumes y's value.
    let y2 = y  // Error: Value consumed more than once.
}
```

No código acima,
a função `f()` exige implicitamente que `MyType` seja copiável.
Dentro do corpo da função,
o valor de `x` é copiado para `x1` e `x2` na atribuição.
Já `g()` suprime a restrição implícita sobre `AnotherType`,
o que permite passar um valor copiável ou não copiável.
Dentro do corpo da função,
você não pode copiar o valor de `y`,
pois `AnotherType` pode ser não copiável.
A atribuição consome o valor de `y`,
e é um erro consumir esse valor mais de uma vez.
Valores não copiáveis, como `y`,
precisam ser passados como parâmetros in-out, borrowing ou consuming ---
para mais informações,
veja <doc:Declarations#Borrowing-and-Consuming-Parameters>.

Para detalhes sobre quando o código genérico
inclui uma restrição implícita para um determinado protocolo,
veja a referência desse protocolo.

<!--
  TODO: Generic Enumerations
  --------------------------
-->

<!--
  TODO: Describe how Optional<Wrapped> works
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
