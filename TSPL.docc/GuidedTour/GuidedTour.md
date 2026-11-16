# Um tour pelo Swift

Conheça os recursos e a sintaxe do Swift.

A tradição sugere que o primeiro programa em uma nova linguagem
deve exibir na tela as palavras “Hello, world!”.
No Swift, isso pode ser feito em uma única linha:

<!--
  K&R uses “hello, world”.
  It seems worth breaking with tradition to use proper casing.
-->

```swift
print("Hello, world!")
// Prints "Hello, world!"
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> print("Hello, world!")
  <- Hello, world!
  ```
-->

Essa sintaxe deve parecer familiar se você conhece outra linguagem:
no Swift, essa linha de código já é um programa completo.
Você não precisa importar uma biblioteca separada para funcionalidades como
exibir texto ou manipular strings.
O código escrito no escopo global é usado
como ponto de entrada do programa,
então você não precisa de uma função `main()`.
Também não é preciso escrever ponto e vírgula
no fim de cada instrução.

Este tour dá a você informações suficientes
para começar a escrever código em Swift,
mostrando como realizar uma variedade de tarefas de programação.
Não se preocupe se não entender algo:
tudo o que é apresentado neste tour
é explicado em detalhes no restante deste livro.

## Valores simples

Use `let` para criar uma constante e `var` para criar uma variável.
O valor de uma constante
não precisa ser conhecido em tempo de compilação,
mas você precisa atribuir a ela um valor exatamente uma vez.
Isso significa que você pode usar constantes para dar nome a um valor
que você determina uma vez, mas usa em vários lugares.

```swift
var myVariable = 42
myVariable = 50
let myConstant = 42
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> var myVariable = 42
  -> myVariable = 50
  -> let myConstant = 42
  ```
-->

Uma constante ou variável precisa ter o mesmo tipo
do valor que você quer atribuir a ela.
No entanto, nem sempre é preciso escrever o tipo explicitamente.
Fornecer um valor ao criar uma constante ou variável
permite que o compilador infira o tipo dela.
No exemplo acima,
o compilador infere que `myVariable` é um inteiro
porque seu valor inicial é um inteiro.

Se o valor inicial não fornecer informação suficiente
(ou se não houver valor inicial),
especifique o tipo escrevendo-o depois da variável,
separado por dois-pontos.

```swift
let implicitInteger = 70
let implicitDouble = 70.0
let explicitDouble: Double = 70
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let implicitInteger = 70
  -> let implicitDouble = 70.0
  -> let explicitDouble: Double = 70
  ```
-->

> Experimente: crie uma constante com
> um tipo explícito `Float` e o valor `4`.

Valores nunca são convertidos implicitamente para outro tipo.
Se você precisar converter um valor para um tipo diferente,
crie explicitamente uma instância do tipo desejado.

```swift
let label = "The width is "
let width = 94
let widthLabel = label + String(width)
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let label = "The width is "
  -> let width = 94
  -> let widthLabel = label + String(width)
  >> print(widthLabel)
  << The width is 94
  ```
-->

> Experimente: tente remover a conversão para `String` da última linha.
> Que erro você recebe?

<!--
  TODO: Discuss with Core Writers ---
  are these experiments that make you familiar with errors
  helping you learn something?
-->

Há uma forma ainda mais simples de incluir valores em strings:
escreva o valor entre parênteses
e escreva uma barra invertida (`\`) antes dos parênteses.
Por exemplo:

```swift
let apples = 3
let oranges = 5
let appleSummary = "I have \(apples) apples."
let fruitSummary = "I have \(apples + oranges) pieces of fruit."
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let apples = 3
  -> let oranges = 5
  -> let appleSummary = "I have \(apples) apples."
  >> print(appleSummary)
  << I have 3 apples.
  -> let fruitSummary = "I have \(apples + oranges) pieces of fruit."
  >> print(fruitSummary)
  << I have 8 pieces of fruit.
  ```
-->

> Experimente: use `\()` para
> incluir um cálculo de ponto flutuante em uma string
> e incluir o nome de alguém em uma saudação.

Use três aspas duplas (`"""`) para strings
que ocupam várias linhas.
A indentação no início de cada linha entre aspas é removida,
desde que corresponda à indentação das aspas de fechamento.
Por exemplo:

```swift
let quotation = """
        Even though there's whitespace to the left,
        the actual lines aren't indented.
            Except for this line.
        Double quotes (") can appear without being escaped.

        I still have \(apples + oranges) pieces of fruit.
        """
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let quotation = """
     I said "I have \(apples) apples."
     And then I said "I have \(apples + oranges) pieces of fruit."
     """
  ```
-->

Crie arrays e dicionários usando colchetes (`[]`),
e acesse os elementos escrevendo
o índice ou a chave entre colchetes.
É permitida uma vírgula após o último elemento.

<!--
  REFERENCE
  The list of fruits comes from the colors that the original iMac came in,
  following the initial launch of the iMac in Bondi Blue, ordered by SKU --
  which also lines up with the order they appeared in ads:

       M7389LL/A (266 MHz Strawberry)
       M7392LL/A (266 MHz Lime)
       M7391LL/A (266 MHz Tangerine)
       M7390LL/A (266 MHz Grape)
       M7345LL/A (266 MHz Blueberry)

       M7441LL/A (333 MHz Strawberry)
       M7444LL/A (333 MHz Lime)
       M7443LL/A (333 MHz Tangerine)
       M7442LL/A (333 MHz Grape)
       M7440LL/A (333 MHz Blueberry)
-->

<!--
  REFERENCE
  Occupations is a reference to Firefly,
  specifically to Mal's joke about Jayne's job on the ship.

  Can't find the specific episode,
  but it shows up in several lists of Firefly "best of" quotes:

  Mal: Jayne, you will keep a civil tongue in that mouth, or I will sew it shut.
       Is there an understanding between us?
  Jayne: You don't pay me to talk pretty. [...]
  Mal: Walk away from this table. Right now.
  [Jayne loads his plate with food and leaves]
  Simon: What *do* you pay him for?
  Mal: What?
  Simon: I was just wondering what his job is - on the ship.
  Mal: Public relations.
-->

```swift
var fruits = ["strawberries", "limes", "tangerines"]
fruits[1] = "grapes"

var occupations = [
    "Malcolm": "Captain",
    "Kaylee": "Mechanic",
 ]
occupations["Jayne"] = "Public Relations"
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> var fruits = ["strawberries", "limes", "tangerines"]
  -> fruits[1] = "grapes"

  -> var occupations = [
         "Malcolm": "Captain",
         "Kaylee": "Mechanic",
      ]
  -> occupations["Jayne"] = "Public Relations"
  ```
-->

<!-- Apple Books screenshot begins here. -->

Arrays crescem automaticamente à medida que você adiciona elementos.

```swift
fruits.append("blueberries")
print(fruits)
// Prints "["strawberries", "grapes", "tangerines", "blueberries"]".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> fruits.append("blueberries")
  -> print(fruits)
  <- ["strawberries", "grapes", "tangerines", "blueberries"]
  ```
-->

Você também usa colchetes para escrever um array ou dicionário vazio.
Para um array, escreva `[]`,
e para um dicionário, escreva `[:]`.

```swift
fruits = []
occupations = [:]
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> fruits = []
  -> occupations = [:]
  ```
-->

Se você estiver atribuindo um array ou dicionário vazio a uma nova variável,
ou a outro lugar onde não há informação de tipo,
é preciso especificar o tipo.

```swift
let emptyArray: [String] = []
let emptyDictionary: [String: Float] = [:]
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let emptyArray: [String] = []
  -> let emptyDictionary: [String: Float] = [:]

  -> let anotherEmptyArray = [String]()
  -> let emptyDictionary = [String: Float]()
  ```
-->

## Controle de fluxo

Use `if` e `switch` para criar condicionais,
e use `for`-`in`, `while` e `repeat`-`while`
para criar laços.
Parênteses em volta da condição ou da variável do laço são opcionais.
Chaves em volta do corpo são obrigatórias.

```swift
let individualScores = [75, 43, 103, 87, 12]
var teamScore = 0
for score in individualScores {
    if score > 50 {
        teamScore += 3
    } else {
        teamScore += 1
    }
}
print(teamScore)
// Prints "11".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let individualScores = [75, 43, 103, 87, 12]
  -> var teamScore = 0
  -> for score in individualScores {
         if score > 50 {
             teamScore += 3
         } else {
             teamScore += 1
         }
     }
  -> print(teamScore)
  <- 11
  ```
-->

<!--
  REFERENCE
  Jelly babies are a candy/sweet that was closely associated
  with past incarnations of the Doctor in Dr. Who.
-->

<!--
  -> let haveJellyBabies = true
  -> if haveJellyBabies {
     }
  << Would you like a jelly baby?
-->

Em uma instrução `if`,
a condição precisa ser uma expressão booleana:
isso significa que código como `if score { ... }` é um erro,
e não uma comparação implícita com zero.

Você pode escrever `if` ou `switch`
depois do sinal de igual (`=`) de uma atribuição
ou depois de `return`,
para escolher um valor com base na condição.

```swift
let scoreDecoration = if teamScore > 10 {
    "🎉"
} else {
    ""
}
print("Score:", teamScore, scoreDecoration)
// Prints "Score: 11 🎉".
```

Você pode usar `if` e `let` juntos
para trabalhar com valores que podem estar ausentes.
Esses valores são representados como optionals.
Um optional ou contém um valor
ou contém `nil`, indicando que o valor está ausente.
Escreva um ponto de interrogação (`?`) depois do tipo de um valor
para marcar o valor como optional.

<!-- Apple Books screenshot ends here. -->

<!--
  REFERENCE
  John Appleseed is a stock Apple fake name,
  going back at least to the contacts database
  that ships with the SDK in the simulator.
-->

```swift
var optionalString: String? = "Hello"
print(optionalString == nil)
// Prints "false".

var optionalName: String? = "John Appleseed"
var greeting = "Hello!"
if let name = optionalName {
    greeting = "Hello, \(name)"
}
print(greeting)
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> var optionalString: String? = "Hello"
  -> print(optionalString == nil)
  <- false

  -> var optionalName: String? = "John Appleseed"
  -> var greeting = "Hello!"
  -> if let name = optionalName {
         greeting = "Hello, \(name)"
     }
  >> print(greeting)
  << Hello, John Appleseed
  ```
-->

> Experimente: altere `optionalName` para `nil`.
> Qual saudação você recebe?
> Adicione uma cláusula `else` que defina outra saudação
> se `optionalName` for `nil`.

Se o valor optional for `nil`,
a condição é `false` e o código entre chaves é ignorado.
Caso contrário, é feito o unwrap do valor optional e ele é atribuído
à constante depois de `let`,
o que deixa o valor unwrapped disponível
dentro do bloco de código.

Outra forma de tratar valores optional
é fornecer um valor padrão usando o operador `??`.
Se o valor optional estiver ausente,
o valor padrão é usado no lugar.

```swift
let nickname: String? = nil
let fullName: String = "John Appleseed"
let informalGreeting = "Hi \(nickname ?? fullName)"
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let nickname: String? = nil
  -> let fullName: String = "John Appleseed"
  -> let informalGreeting = "Hi \(nickname ?? fullName)"
  >> print(informalGreeting)
  << Hi John Appleseed
  ```
-->

Você pode usar uma grafia mais curta para fazer o unwrap de um valor,
mantendo o mesmo nome para o valor unwrapped.

```swift
if let nickname {
    print("Hey, \(nickname)")
}
// Doesn't print anything, because nickname is nil.
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> if let nickname {
         print("Hey, \(nickname)")
     }
  ```
-->

As instruções `switch` aceitam qualquer tipo de dado
e uma grande variedade de operações de comparação:
elas não se limitam a inteiros
e a testes de igualdade.

<!--
  REFERENCE
  The vegetables and foods made from vegetables
  were just a convenient choice for a switch statement.
  They have various properties
  and fit with the apples & oranges used in an earlier example.
-->

```swift
let vegetable = "red pepper"
switch vegetable {
case "celery":
    print("Add some raisins and make ants on a log.")
case "cucumber", "watercress":
    print("That would make a good tea sandwich.")
case let x where x.hasSuffix("pepper"):
    print("Is it a spicy \(x)?")
default:
    print("Everything tastes good in soup.")
}
// Prints "Is it a spicy red pepper?"
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let vegetable = "red pepper"
  -> switch vegetable {
         case "celery":
             print("Add some raisins and make ants on a log.")
         case "cucumber", "watercress":
             print("That would make a good tea sandwich.")
         case let x where x.hasSuffix("pepper"):
             print("Is it a spicy \(x)?")
         default:
             print("Everything tastes good in soup.")
     }
  <- Is it a spicy red pepper?
  ```
-->

> Experimente: remova o caso default.
> Que erro você recebe?

Repare em como `let` pode ser usado em um padrão
para atribuir a uma constante o valor que correspondeu ao padrão.

Depois de executar o código do caso do `switch` que correspondeu,
o programa sai da instrução `switch`.
A execução não continua para o próximo caso,
então você não precisa sair explicitamente do `switch`
no fim do código de cada caso.

<!--
  Omitting mention of "fallthrough" keyword.
  It's in the guide/reference if you need it.
-->

Você usa `for`-`in` para iterar sobre os itens de um dicionário,
fornecendo um par de nomes a serem usados
para cada par chave-valor.
Dicionários são uma coleção não ordenada,
então suas chaves e valores são percorridos
em uma ordem arbitrária.

<!--
  REFERENCE
  Prime, square, and Fibonacci numbers
  are just convenient sets of numbers
  that many developers are already familiar with
  that we can use for some simple math.
-->

```swift
let interestingNumbers = [
    "Prime": [2, 3, 5, 7, 11, 13],
    "Fibonacci": [1, 1, 2, 3, 5, 8],
    "Square": [1, 4, 9, 16, 25],
]
var largest = 0
for (_, numbers) in interestingNumbers {
    for number in numbers {
        if number > largest {
            largest = number
        }
    }
}
print(largest)
// Prints "25".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let interestingNumbers = [
         "Prime": [2, 3, 5, 7, 11, 13],
         "Fibonacci": [1, 1, 2, 3, 5, 8],
         "Square": [1, 4, 9, 16, 25],
     ]
  -> var largest = 0
  -> for (_, numbers) in interestingNumbers {
         for number in numbers {
             if number > largest {
                 largest = number
             }
         }
     }
  -> print(largest)
  <- 25
  ```
-->

> Experimente: substitua o `_` por um nome de variável,
> e acompanhe qual tipo de número foi o maior.

Use `while` para repetir um bloco de código até que uma condição mude.
A condição de um laço também pode ficar no fim,
garantindo que o laço seja executado pelo menos uma vez.

<!--
  REFERENCE
  This example is rather skeletal -- m and n are pretty boring.
  I couldn't come up with anything suitably interesting at the time though,
  so I just went ahead and used this.
-->

```swift
var n = 2
while n < 100 {
    n *= 2
}
print(n)
// Prints "128".

var m = 2
repeat {
    m *= 2
} while m < 100
print(m)
// Prints "128".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> var n = 2
  -> while n < 100 {
         n *= 2
     }
  -> print(n)
  <- 128

  -> var m = 2
  -> repeat {
         m *= 2
     } while m < 100
  -> print(m)
  <- 128
  ```
-->

> Experimente:
> Altere a condição de `m < 100` para `m < 0`
> para ver como `while` e `repeat`-`while` se comportam de forma diferente
> quando a condição do laço já é falsa.

Você pode manter um índice em um laço
usando `..<` para criar um intervalo de índices.

```swift
var total = 0
for i in 0..<4 {
    total += i
}
print(total)
// Prints "6".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> var total = 0
  -> for i in 0..<4 {
         total += i
     }
  -> print(total)
  <- 6
  ```
-->

Use `..<` para criar um intervalo que omite seu valor superior,
e use `...` para criar um intervalo que inclui os dois valores.

## Funções e closures

Use `func` para declarar uma função.
Chame uma função escrevendo seu nome
seguido de uma lista de argumentos entre parênteses.
Use `->` para separar os nomes e tipos dos parâmetros
do tipo de retorno da função.

<!--
  REFERENCE
  Bob is used as just a generic name,
  but also a callout to Alex's dad.
  Tuesday is used on the assumption that lots of folks would be reading
  on the Tuesday after the WWDC keynote.
-->

```swift
func greet(person: String, day: String) -> String {
    return "Hello \(person), today is \(day)."
}
greet(person: "Bob", day: "Tuesday")
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> func greet(person: String, day: String) -> String {
         return "Hello \(person), today is \(day)."
     }
  >> let greetBob =
  -> greet(person: "Bob", day: "Tuesday")
  >> print(greetBob)
  << Hello Bob, today is Tuesday.
  ```
-->

> Experimente: remova o parâmetro `day`.
> Adicione um parâmetro para incluir o prato do dia de hoje na saudação.

Por padrão,
as funções usam os nomes dos parâmetros
como rótulos para seus argumentos.
Escreva um rótulo de argumento personalizado antes do nome do parâmetro,
ou escreva `_` para não usar rótulo de argumento.

```swift
func greet(_ person: String, on day: String) -> String {
    return "Hello \(person), today is \(day)."
}
greet("John", on: "Wednesday")
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> func greet(_ person: String, on day: String) -> String {
         return "Hello \(person), today is \(day)."
     }
  >> let greetJohn =
  -> greet("John", on: "Wednesday")
  >> print(greetJohn)
  << Hello John, today is Wednesday.
  ```
-->

Use uma tupla para criar um valor composto:
por exemplo, para retornar vários valores de uma função.
Os elementos de uma tupla podem ser acessados
pelo nome ou pelo número.

<!--
  REFERENCE
  Min, max, and sum are convenient for this example
  because they're all simple operations
  that are performed on the same kind of data.
  This gives the function a reason to return a tuple.
-->

```swift
func calculateStatistics(scores: [Int]) -> (min: Int, max: Int, sum: Int) {
    var min = scores[0]
    var max = scores[0]
    var sum = 0

    for score in scores {
        if score > max {
            max = score
        } else if score < min {
            min = score
        }
        sum += score
    }

    return (min, max, sum)
}
let statistics = calculateStatistics(scores: [5, 3, 100, 3, 9])
print(statistics.sum)
// Prints "120".
print(statistics.2)
// Prints "120".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> func calculateStatistics(scores: [Int]) -> (min: Int, max: Int, sum: Int) {
         var min = scores[0]
         var max = scores[0]
         var sum = 0

         for score in scores {
             if score > max {
                 max = score
             } else if score < min {
                 min = score
             }
             sum += score
         }

         return (min, max, sum)
     }
  -> let statistics = calculateStatistics(scores: [5, 3, 100, 3, 9])
  >> print(statistics)
  << (min: 3, max: 100, sum: 120)
  -> print(statistics.sum)
  <- 120
  -> print(statistics.2)
  <- 120
  ```
-->

Funções podem ser aninhadas.
Funções aninhadas têm acesso a variáveis
que foram declaradas na função externa.
Você pode usar funções aninhadas
para organizar o código de uma função
que é longa ou complexa.

```swift
func returnFifteen() -> Int {
    var y = 10
    func add() {
        y += 5
    }
    add()
    return y
}
returnFifteen()
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> func returnFifteen() -> Int {
         var y = 10
         func add() {
             y += 5
         }
         add()
         return y
     }
  >> let fifteen =
  -> returnFifteen()
  >> print(fifteen)
  << 15
  ```
-->

Funções são um tipo de primeira classe.
Isso significa que uma função pode retornar outra função como seu valor.

```swift
func makeIncrementer() -> ((Int) -> Int) {
    func addOne(number: Int) -> Int {
        return 1 + number
    }
    return addOne
}
var increment = makeIncrementer()
increment(7)
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> func makeIncrementer() -> ((Int) -> Int) {
         func addOne(number: Int) -> Int {
             return 1 + number
         }
         return addOne
     }
  -> var increment = makeIncrementer()
  >> let incrementResult =
  -> increment(7)
  >> print(incrementResult)
  << 8
  ```
-->

Uma função pode receber outra função como um de seus argumentos.

```swift
func hasAnyMatches(list: [Int], condition: (Int) -> Bool) -> Bool {
    for item in list {
        if condition(item) {
            return true
        }
    }
    return false
}
func lessThanTen(number: Int) -> Bool {
    return number < 10
}
var numbers = [20, 19, 7, 12]
hasAnyMatches(list: numbers, condition: lessThanTen)
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> func hasAnyMatches(list: [Int], condition: (Int) -> Bool) -> Bool {
         for item in list {
             if condition(item) {
                 return true
             }
         }
         return false
     }
  -> func lessThanTen(number: Int) -> Bool {
         return number < 10
     }
  -> var numbers = [20, 19, 7, 12]
  >> let anyMatches =
  -> hasAnyMatches(list: numbers, condition: lessThanTen)
  >> print(anyMatches)
  << true
  ```
-->

Funções são, na verdade, um caso especial de closures:
blocos de código que podem ser chamados mais tarde.
O código de uma closure tem acesso a coisas como variáveis e funções
que estavam disponíveis no escopo onde a closure foi criada,
mesmo que a closure esteja em outro escopo quando é executada:
você já viu um exemplo disso com funções aninhadas.
Você pode escrever uma closure sem nome
envolvendo o código com chaves (`{}`).
Use `in` para separar os argumentos e o tipo de retorno do corpo.

```swift
numbers.map({ (number: Int) -> Int in
    let result = 3 * number
    return result
})
```

<!--
  - test: `guided-tour`

  ```swifttest
  >> let numbersMap =
  -> numbers.map({ (number: Int) -> Int in
         let result = 3 * number
         return result
     })
  >> print(numbersMap)
  << [60, 57, 21, 36]
  ```
-->

> Experimente: reescreva a closure para retornar zero para todos os números ímpares.

Você tem várias opções para escrever closures de forma mais concisa.
Quando o tipo de uma closure já é conhecido,
como o callback de um delegate,
você pode omitir o tipo de seus parâmetros,
o tipo de retorno, ou ambos.
Closures de uma única instrução retornam implicitamente o valor
de sua única instrução.

```swift
let mappedNumbers = numbers.map({ number in 3 * number })
print(mappedNumbers)
// Prints "[60, 57, 21, 36]".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let mappedNumbers = numbers.map({ number in 3 * number })
  -> print(mappedNumbers)
  <- [60, 57, 21, 36]
  ```
-->

Você pode se referir aos parâmetros pelo número, em vez do nome:
essa abordagem é especialmente útil em closures muito curtas.
Uma closure passada como último argumento de uma função
pode aparecer logo depois dos parênteses.
Quando uma closure é o único argumento de uma função,
você pode omitir os parênteses por completo.

```swift
let sortedNumbers = numbers.sorted { $0 > $1 }
print(sortedNumbers)
// Prints "[20, 19, 12, 7]".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let sortedNumbers = numbers.sorted { $0 > $1 }
  -> print(sortedNumbers)
  <- [20, 19, 12, 7]
  ```
-->

<!--
  Called sorted() on a variable rather than a literal to work around an issue in Xcode.  See <rdar://17540974>.
-->

<!--
  Omitted sort(foo, <) because it often causes a spurious warning in Xcode.  See <rdar://17047529>.
-->

<!--
  Omitted custom operators as "advanced" topics.
-->

## Objetos e classes

Use `class` seguido do nome da classe para criar uma classe.
A declaração de uma propriedade em uma classe é escrita da mesma forma
que a declaração de uma constante ou variável,
exceto que ela está no contexto de uma classe.
Da mesma forma, as declarações de métodos e funções são escritas do mesmo jeito.

<!--
  REFERENCE
  Shapes are used as the example object
  because they're familiar and they have a sense of properties
  and a sense of inheritance/subcategorization.
  They're not a perfect fit --
  they might be better off modeled as structures --
  but that wouldn't let them inherit behavior.
-->

```swift
class Shape {
    var numberOfSides = 0
    func simpleDescription() -> String {
        return "A shape with \(numberOfSides) sides."
    }
}
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> class Shape {
         var numberOfSides = 0
         func simpleDescription() -> String {
             return "A shape with \(numberOfSides) sides."
         }
     }
  >> print(Shape().simpleDescription())
  << A shape with 0 sides.
  ```
-->

> Experimente: adicione uma propriedade constante com `let`,
> e adicione outro método que receba um argumento.

Crie uma instância de uma classe
colocando parênteses depois do nome da classe.
Use a sintaxe de ponto para acessar
as propriedades e os métodos da instância.

```swift
var shape = Shape()
shape.numberOfSides = 7
var shapeDescription = shape.simpleDescription()
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> var shape = Shape()
  -> shape.numberOfSides = 7
  -> var shapeDescription = shape.simpleDescription()
  >> print(shapeDescription)
  << A shape with 7 sides.
  ```
-->

Esta versão da classe `Shape` está faltando algo importante:
um inicializador para configurar a classe quando uma instância é criada.
Use `init` para criar um.

```swift
class NamedShape {
    var numberOfSides: Int = 0
    var name: String

    init(name: String) {
       self.name = name
    }

    func simpleDescription() -> String {
       return "A shape with \(numberOfSides) sides."
    }
}
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> class NamedShape {
         var numberOfSides: Int = 0
         var name: String

         init(name: String) {
            self.name = name
         }

         func simpleDescription() -> String {
            return "A shape with \(numberOfSides) sides."
         }
     }
  >> print(NamedShape(name: "test name").name)
  << test name
  >> print(NamedShape(name: "test name").simpleDescription())
  << A shape with 0 sides.
  ```
-->

Repare em como `self` é usado para distinguir a propriedade `name`
do argumento `name` do inicializador.
Os argumentos do inicializador são passados como em uma chamada de função
quando você cria uma instância da classe.
Toda propriedade precisa ter um valor atribuído:
seja na sua declaração (como em `numberOfSides`)
ou no inicializador (como em `name`).

Use `deinit` para criar um desinicializador
se você precisar executar alguma limpeza
antes que o objeto seja desalocado.

Subclasses incluem o nome da superclasse
depois do nome da classe,
separado por dois-pontos.
Não há exigência de que classes herdem de alguma classe raiz padrão,
então você pode incluir ou omitir uma superclasse conforme necessário.

Métodos de uma subclasse que substituem a implementação da superclasse
são marcados com `override`:
sobrescrever um método sem querer, sem `override`,
é detectado pelo compilador como um erro.
O compilador também detecta métodos marcados com `override`
que não sobrescrevem nenhum método da superclasse.

```swift
class Square: NamedShape {
    var sideLength: Double

    init(sideLength: Double, name: String) {
        self.sideLength = sideLength
        super.init(name: name)
        numberOfSides = 4
    }

    func area() -> Double {
        return sideLength * sideLength
    }

    override func simpleDescription() -> String {
        return "A square with sides of length \(sideLength)."
    }
}
let test = Square(sideLength: 5.2, name: "my test square")
test.area()
test.simpleDescription()
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> class Square: NamedShape {
         var sideLength: Double

         init(sideLength: Double, name: String) {
             self.sideLength = sideLength
             super.init(name: name)
             numberOfSides = 4
         }

         func area() -> Double {
             return sideLength * sideLength
         }

         override func simpleDescription() -> String {
             return "A square with sides of length \(sideLength)."
         }
     }
  -> let test = Square(sideLength: 5.2, name: "my test square")
  >> let testArea =
  -> test.area()
  >> print(testArea)
  << 27.040000000000003
  >> let testDesc =
  -> test.simpleDescription()
  >> print(testDesc)
  << A square with sides of length 5.2.
  ```
-->

> Experimente: crie outra subclasse de `NamedShape`
> chamada `Circle`
> que receba um raio e um nome
> como argumentos do seu inicializador.
> Implemente um método `area()` e um método `simpleDescription()`
> na classe `Circle`.

Além de propriedades simples armazenadas,
propriedades podem ter um getter e um setter.

```swift
class EquilateralTriangle: NamedShape {
    var sideLength: Double = 0.0

    init(sideLength: Double, name: String) {
        self.sideLength = sideLength
        super.init(name: name)
        numberOfSides = 3
    }

    var perimeter: Double {
        get {
             return 3.0 * sideLength
        }
        set {
            sideLength = newValue / 3.0
        }
    }

    override func simpleDescription() -> String {
        return "An equilateral triangle with sides of length \(sideLength)."
    }
}
var triangle = EquilateralTriangle(sideLength: 3.1, name: "a triangle")
print(triangle.perimeter)
// Prints "9.3".
triangle.perimeter = 9.9
print(triangle.sideLength)
// Prints "3.3000000000000003".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> class EquilateralTriangle: NamedShape {
         var sideLength: Double = 0.0

         init(sideLength: Double, name: String) {
             self.sideLength = sideLength
             super.init(name: name)
             numberOfSides = 3
         }

         var perimeter: Double {
             get {
                  return 3.0 * sideLength
             }
             set {
                 sideLength = newValue / 3.0
             }
         }

         override func simpleDescription() -> String {
             return "An equilateral triangle with sides of length \(sideLength)."
         }
     }
  -> var triangle = EquilateralTriangle(sideLength: 3.1, name: "a triangle")
  -> print(triangle.perimeter)
  <- 9.3
  -> triangle.perimeter = 9.9
  -> print(triangle.sideLength)
  <- 3.3000000000000003
  ```
-->

No setter de `perimeter`,
o novo valor recebe o nome implícito `newValue`.
Você pode fornecer um nome explícito entre parênteses depois de `set`.

Repare que o inicializador da classe `EquilateralTriangle`
tem três etapas diferentes:

1. Definir o valor das propriedades que a subclasse declara.
2. Chamar o inicializador da superclasse.
3. Alterar o valor das propriedades definidas pela superclasse.
   Qualquer trabalho adicional de configuração que use métodos, getters ou setters
   também pode ser feito neste ponto.

Se você não precisa calcular a propriedade,
mas ainda precisa de código que execute antes e depois de atribuir um novo valor,
use `willSet` e `didSet`.
O código que você fornece é executado sempre que o valor muda fora de um inicializador.
Por exemplo, a classe abaixo garante
que o lado do triângulo
seja sempre igual ao lado do quadrado.

<!--
  This triangle + square example could use improvement.
  The goal is to show why you would want to use willSet,
  but it was constrained by the fact that
  we're working in the context of geometric shapes.
-->

```swift
class TriangleAndSquare {
    var triangle: EquilateralTriangle {
        willSet {
            square.sideLength = newValue.sideLength
        }
    }
    var square: Square {
        willSet {
            triangle.sideLength = newValue.sideLength
        }
    }
    init(size: Double, name: String) {
        square = Square(sideLength: size, name: name)
        triangle = EquilateralTriangle(sideLength: size, name: name)
    }
}
var triangleAndSquare = TriangleAndSquare(size: 10, name: "another test shape")
print(triangleAndSquare.square.sideLength)
// Prints "10.0".
print(triangleAndSquare.triangle.sideLength)
// Prints "10.0".
triangleAndSquare.square = Square(sideLength: 50, name: "larger square")
print(triangleAndSquare.triangle.sideLength)
// Prints "50.0".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> class TriangleAndSquare {
         var triangle: EquilateralTriangle {
             willSet {
                 square.sideLength = newValue.sideLength
             }
         }
         var square: Square {
             willSet {
                 triangle.sideLength = newValue.sideLength
             }
         }
         init(size: Double, name: String) {
             square = Square(sideLength: size, name: name)
             triangle = EquilateralTriangle(sideLength: size, name: name)
         }
     }
  -> var triangleAndSquare = TriangleAndSquare(size: 10, name: "another test shape")
  -> print(triangleAndSquare.square.sideLength)
  <- 10.0
  -> print(triangleAndSquare.triangle.sideLength)
  <- 10.0
  -> triangleAndSquare.square = Square(sideLength: 50, name: "larger square")
  -> print(triangleAndSquare.triangle.sideLength)
  <- 50.0
  ```
-->

<!--
  Grammatically, these clauses are general to variables.
  Not sure what it would look like
  (or if it's even allowed)
  to use them outside a class or a struct.
-->

Ao trabalhar com valores optional,
você pode escrever `?` antes de operações como métodos, propriedades e subscripts.
Se o valor antes do `?` for `nil`,
tudo depois do `?` é ignorado
e o valor de toda a expressão é `nil`.
Caso contrário, o valor optional é unwrapped,
e tudo depois do `?` age sobre o valor unwrapped.
Nos dois casos,
o valor de toda a expressão é um valor optional.

```swift
let optionalSquare: Square? = Square(sideLength: 2.5, name: "optional square")
let sideLength = optionalSquare?.sideLength
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let optionalSquare: Square? = Square(sideLength: 2.5, name: "optional square")
  -> let sideLength = optionalSquare?.sideLength
  ```
-->

## Enums e structs

Use `enum` para criar um enum.
Assim como classes e todos os outros tipos nomeados,
enums podem ter métodos associados a eles.

<!--
  REFERENCE
  Playing cards work pretty well to demonstrate enumerations
  because they have two aspects, suit and rank,
  both of which come from a small finite set.
  The deck used here is probably the most common,
  at least through most of Europe and the Americas,
  but there are many other regional variations.
-->

```swift
enum Rank: Int {
    case ace = 1
    case two, three, four, five, six, seven, eight, nine, ten
    case jack, queen, king

    func simpleDescription() -> String {
        switch self {
        case .ace:
            return "ace"
        case .jack:
            return "jack"
        case .queen:
            return "queen"
        case .king:
            return "king"
        default:
            return String(self.rawValue)
        }
    }
}
let ace = Rank.ace
let aceRawValue = ace.rawValue
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> enum Rank: Int {
         case ace = 1
         case two, three, four, five, six, seven, eight, nine, ten
         case jack, queen, king

         func simpleDescription() -> String {
             switch self {
                 case .ace:
                     return "ace"
                 case .jack:
                     return "jack"
                 case .queen:
                     return "queen"
                 case .king:
                     return "king"
                 default:
                     return String(self.rawValue)
             }
         }
     }
  -> let ace = Rank.ace
  -> let aceRawValue = ace.rawValue
  >> print(aceRawValue)
  << 1
  ```
-->

> Experimente: escreva uma função que compara dois valores de `Rank`
> comparando os seus raw values.

Por padrão, o Swift atribui os raw values começando em zero
e incrementando um a cada vez,
mas você pode mudar esse comportamento especificando valores explicitamente.
No exemplo acima, `Ace` recebe explicitamente o raw value `1`,
e os demais raw values são atribuídos em ordem.
Você também pode usar strings ou números de ponto flutuante
como raw type de um enum.
Use a propriedade `rawValue` para acessar o raw value de um caso do enum.

Use o inicializador `init?(rawValue:)`
para criar uma instância de um enum a partir de um raw value.
Ele retorna o caso do enum que corresponde ao raw value,
ou `nil` se não houver nenhum `Rank` correspondente.

```swift
if let convertedRank = Rank(rawValue: 3) {
    let threeDescription = convertedRank.simpleDescription()
}
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> if let convertedRank = Rank(rawValue: 3) {
         let threeDescription = convertedRank.simpleDescription()
  >> print(threeDescription)
  << 3
  -> }
  ```
-->

Os valores dos casos de um enum são valores de verdade,
não apenas outra forma de escrever seus raw values.
Na verdade,
nos casos em que não há um raw value significativo,
você não precisa fornecer um.

```swift
enum Suit {
    case spades, hearts, diamonds, clubs

    func simpleDescription() -> String {
        switch self {
        case .spades:
            return "spades"
        case .hearts:
            return "hearts"
        case .diamonds:
            return "diamonds"
        case .clubs:
            return "clubs"
        }
    }
}
let hearts = Suit.hearts
let heartsDescription = hearts.simpleDescription()
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> enum Suit {
         case spades, hearts, diamonds, clubs

         func simpleDescription() -> String {
             switch self {
                 case .spades:
                     return "spades"
                 case .hearts:
                     return "hearts"
                 case .diamonds:
                     return "diamonds"
                 case .clubs:
                     return "clubs"
             }
         }
     }
  -> let hearts = Suit.hearts
  -> let heartsDescription = hearts.simpleDescription()
  >> print(heartsDescription)
  << hearts
  ```
-->

> Experimente: adicione um método `color()` a `Suit` que retorna "black"
> para espadas e paus, e retorna "red" para copas e ouros.

<!--
  Suits are in Bridge order, which matches Unicode order.
  In other games, orders differ.
  Wikipedia lists a good half dozen orders.
-->

Repare nas duas formas como o caso `hearts` do enum é mencionado acima:
ao atribuir um valor à constante `hearts`,
o caso do enum `Suit.hearts` é referenciado pelo nome completo,
porque a constante não tem um tipo explícito especificado.
Dentro do `switch`,
o caso do enum é referenciado pela forma abreviada `.hearts`,
porque já se sabe que o valor de `self` é um naipe.
Você pode usar a forma abreviada
sempre que o tipo do valor já for conhecido.

Se um enum tem raw values,
esses valores são determinados como parte da declaração,
o que significa que toda instância de um determinado caso do enum
sempre tem o mesmo raw value.
Outra opção para os casos de enum
é ter associated values ao caso:
esses valores são determinados quando você cria a instância,
e podem ser diferentes para cada instância de um caso do enum.
Você pode pensar nos associated values
como se comportando como propriedades armazenadas da instância do caso do enum.
Por exemplo,
considere o caso de solicitar
os horários de nascer e pôr do sol a um servidor.
O servidor responde com a informação solicitada
ou com uma descrição do que deu errado.

<!--
  REFERENCE
  The server response is a simple way to essentially re-implement Optional
  while sidestepping the fact that I'm doing so.

  "Out of cheese" is a reference to a Terry Pratchett book,
  which features a computer named Hex.
  Hex's other error messages include:

       - Out of Cheese Error. Redo From Start.
       - Mr. Jelly! Mr. Jelly! Error at Address Number 6, Treacle Mine Road.
       - Melon melon melon
       - +++ Wahhhhhhh! Mine! +++
       - +++ Divide By Cucumber Error. Please Reinstall Universe And Reboot +++
       - +++Whoops! Here comes the cheese! +++

  These messages themselves are references to BASIC interpreters
  (REDO FROM START) and old Hayes-compatible modems (+++).

  The "out of cheese error" may be a reference to a military computer
  although I can't find the source of this story anymore.
  As the story goes, during the course of a rather wild party,
  one of the computer's vacuum tube cabinets
  was opened to provide heat to a cold room in the winter.
  Through great coincidence,
  when a cheese tray got bashed into it during the celebration,
  the computer kept on working even though some of the tubes were broken
  and had cheese splattered & melted all over them.
  Tech were dispatched to make sure the computer was ok
  and told add more cheese if necessary --
  the officer in charge said that he didn't want
  an "out of cheese error" interrupting the calculation.
-->

```swift
enum ServerResponse {
    case result(String, String)
    case failure(String)
}

let success = ServerResponse.result("6:00 am", "8:09 pm")
let failure = ServerResponse.failure("Out of cheese.")

switch success {
case let .result(sunrise, sunset):
    print("Sunrise is at \(sunrise) and sunset is at \(sunset).")
case let .failure(message):
    print("Failure...  \(message)")
}
// Prints "Sunrise is at 6:00 am and sunset is at 8:09 pm."
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> enum ServerResponse {
         case result(String, String)
         case failure(String)
     }

  -> let success = ServerResponse.result("6:00 am", "8:09 pm")
  -> let failure = ServerResponse.failure("Out of cheese.")

  -> switch success {
         case let .result(sunrise, sunset):
             print("Sunrise is at \(sunrise) and sunset is at \(sunset).")
         case let .failure(message):
             print("Failure...  \(message)")
     }
  <- Sunrise is at 6:00 am and sunset is at 8:09 pm.
  ```
-->

> Experimente: adicione um terceiro caso a `ServerResponse` e ao `switch`.

Repare em como os horários de nascer e pôr do sol
são extraídos do valor de `ServerResponse`
como parte da correspondência do valor com os casos do `switch`.

Use `struct` para criar uma struct.
Structs oferecem muitos dos mesmos comportamentos das classes,
incluindo métodos e inicializadores.
Uma das diferenças mais importantes
entre structs e classes é que
structs são sempre copiadas quando são passadas pelo seu código,
mas classes são passadas por referência.

```swift
struct Card {
    var rank: Rank
    var suit: Suit
    func simpleDescription() -> String {
        return "The \(rank.simpleDescription()) of \(suit.simpleDescription())"
    }
}
let threeOfSpades = Card(rank: .three, suit: .spades)
let threeOfSpadesDescription = threeOfSpades.simpleDescription()
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> struct Card {
         var rank: Rank
         var suit: Suit
         func simpleDescription() -> String {
             return "The \(rank.simpleDescription()) of \(suit.simpleDescription())"
         }
     }
  -> let threeOfSpades = Card(rank: .three, suit: .spades)
  -> let threeOfSpadesDescription = threeOfSpades.simpleDescription()
  >> print(threeOfSpadesDescription)
  << The 3 of spades
  ```
-->

> Experimente: escreva uma função que retorne um array contendo
> um baralho completo de cartas,
> com uma carta de cada combinação de valor e naipe.

## Concorrência

Use `async` para marcar uma função que roda de forma assíncrona.

```swift
func fetchUserID(from server: String) async -> Int {
    if server == "primary" {
        return 97
    }
    return 501
}
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> func fetchUserID(from server: String) async -> Int {
         if server == "primary" {
             return 97
         }
         return 501
     }
  ```
-->

Você marca uma chamada a uma função assíncrona escrevendo `await` na frente dela.

```swift
func fetchUsername(from server: String) async -> String {
    let userID = await fetchUserID(from: server)
    if userID == 501 {
        return "John Appleseed"
    }
    return "Guest"
}
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> func fetchUsername(from server: String) async -> String {
         let userID = await fetchUserID(from: server)
         if userID == 501 {
             return "John Appleseed"
         }
         return "Guest"
     }
  ```
-->

Use `async let` para chamar uma função assíncrona,
deixando-a rodar em paralelo com outro código assíncrono.
Ao usar o valor que ela retorna, escreva `await`.

```swift
func connectUser(to server: String) async {
    async let userID = fetchUserID(from: server)
    async let username = fetchUsername(from: server)
    let greeting = await "Hello \(username), user ID \(userID)"
    print(greeting)
}
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> func connectUser(to server: String) async {
         async let userID = fetchUserID(from: server)
         async let username = fetchUsername(from: server)
         let greeting = await "Hello \(username), user ID \(userID)"
         print(greeting)
     }
  ```
-->

Use `Task` para chamar funções assíncronas a partir de código síncrono,
sem esperar que elas retornem.

```swift
Task {
    await connectUser(to: "primary")
}
// Prints "Hello Guest, user ID 97".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> Task {
         await connectUser(to: "primary")
     }
  >> import Darwin; sleep(1)  // Pause for task to run
  <- Hello Guest, user ID 97
  ```
-->

Use task groups para estruturar código concorrente.

```swift
let userIDs = await withTaskGroup(of: Int.self) { group in
    for server in ["primary", "secondary", "development"] {
        group.addTask {
            return await fetchUserID(from: server)
        }
    }

    var results: [Int] = []
    for await result in group {
        results.append(result)
    }
    return results
}
```

Actors são semelhantes a classes,
exceto que garantem que diferentes funções assíncronas
possam interagir com segurança com uma mesma instância do actor ao mesmo tempo.

```swift
actor ServerConnection {
    var server: String = "primary"
    private var activeUsers: [Int] = []
    func connect() async -> Int {
        let userID = await fetchUserID(from: server)
        // ... communicate with server ...
        activeUsers.append(userID)
        return userID
    }
}
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> actor Oven {
         var contents: [String] = []
         func bake(_ food: String) -> String {
             contents.append(food)
             // ... wait for food to bake ...
             return contents.removeLast()
         }
     }
  ```
-->

Quando você chama um método de um actor ou acessa uma de suas propriedades,
marque esse código com `await`
para indicar que ele pode precisar esperar outro código
que já está rodando no actor terminar.

```swift
let server = ServerConnection()
let userID = await server.connect()
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let oven = Oven()
  -> let biscuits = await oven.bake("biscuits")
  ```
-->

## Protocolos e extensions

Use `protocol` para declarar um protocolo.

```swift
protocol ExampleProtocol {
     var simpleDescription: String { get }
     mutating func adjust()
}
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> protocol ExampleProtocol {
          var simpleDescription: String { get }
          mutating func adjust()
     }
  ```
-->

Classes, enums e structs podem todas adotar protocolos.

<!--
  REFERENCE
  The use of adjust() is totally a placeholder
  for some more interesting operation.
  Likewise for the struct and classes -- placeholders
  for some more interesting data structure.
-->

```swift
class SimpleClass: ExampleProtocol {
     var simpleDescription: String = "A very simple class."
     var anotherProperty: Int = 69105
     func adjust() {
          simpleDescription += "  Now 100% adjusted."
     }
}
var a = SimpleClass()
a.adjust()
let aDescription = a.simpleDescription

struct SimpleStructure: ExampleProtocol {
     var simpleDescription: String = "A simple structure"
     mutating func adjust() {
          simpleDescription += " (adjusted)"
     }
}
var b = SimpleStructure()
b.adjust()
let bDescription = b.simpleDescription
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> class SimpleClass: ExampleProtocol {
          var simpleDescription: String = "A very simple class."
          var anotherProperty: Int = 69105
          func adjust() {
               simpleDescription += "  Now 100% adjusted."
          }
     }
  -> var a = SimpleClass()
  -> a.adjust()
  -> let aDescription = a.simpleDescription
  >> print(aDescription)
  << A very simple class.  Now 100% adjusted.

  -> struct SimpleStructure: ExampleProtocol {
          var simpleDescription: String = "A simple structure"
          mutating func adjust() {
               simpleDescription += " (adjusted)"
          }
     }
  -> var b = SimpleStructure()
  -> b.adjust()
  -> let bDescription = b.simpleDescription
  >> print(bDescription)
  << A simple structure (adjusted)
  ```
-->

> Experimente: adicione outro requisito a `ExampleProtocol`.
> Que mudanças você precisa fazer
> em `SimpleClass` e `SimpleStructure`
> para que elas continuem em conformidade com o protocolo?

Repare no uso da palavra-chave `mutating`
na declaração de `SimpleStructure`,
para marcar um método que modifica a struct.
A declaração de `SimpleClass` não precisa
de nenhum de seus métodos marcados como `mutating`,
porque métodos de uma classe sempre podem modificar a classe.

Use `extension` para adicionar funcionalidade a um tipo existente,
como novos métodos e propriedades computadas.
Você pode usar uma extension para adicionar conformidade com um protocolo
a um tipo declarado em outro lugar,
ou até mesmo a um tipo que você importou de uma biblioteca ou framework.

```swift
extension Int: ExampleProtocol {
    var simpleDescription: String {
        return "The number \(self)"
    }
    mutating func adjust() {
        self += 42
    }
 }
print(7.simpleDescription)
// Prints "The number 7".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> extension Int: ExampleProtocol {
         var simpleDescription: String {
             return "The number \(self)"
         }
         mutating func adjust() {
             self += 42
         }
      }
  -> print(7.simpleDescription)
  <- The number 7
  ```
-->

> Experimente: escreva uma extension para o tipo `Double`
> que adicione uma propriedade `absoluteValue`.

Você pode usar o nome de um protocolo como qualquer outro tipo nomeado:
por exemplo, para criar uma coleção de objetos
que têm tipos diferentes,
mas que todos estão em conformidade com um único protocolo.
Ao trabalhar com valores cujo tipo é um boxed protocol type,
métodos fora da definição do protocolo não ficam disponíveis.

```swift
let protocolValue: any ExampleProtocol = a
print(protocolValue.simpleDescription)
// Prints "A very simple class.  Now 100% adjusted."
// print(protocolValue.anotherProperty)  // Uncomment to see the error
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let protocolValue: ExampleProtocol = a
  -> print(protocolValue.simpleDescription)
  <- A very simple class.  Now 100% adjusted.
  // print(protocolValue.anotherProperty)  // Uncomment to see the error
  ```
-->

Mesmo que a variável `protocolValue`
tenha um tipo em tempo de execução de `SimpleClass`,
o compilador a trata como o tipo `ExampleProtocol` declarado.
Isso significa que você não consegue acessar acidentalmente
métodos ou propriedades que a classe implementa
além da conformidade com o protocolo.

## Tratamento de erros

Você representa erros usando qualquer tipo que adote o protocolo `Error`.

<!--
  REFERENCE
  PrinterError.OnFire is a reference to the Unix printing system's "lp0 on
  fire" error message, used when the kernel can't identify the specific error.
  The names of printers used in the examples in this section are names of
  people who were important in the development of printing.

  Bi Sheng is credited with inventing the first movable type out of porcelain
  in China in the 1040s.  It was a mixed success, in large part because of the
  vast number of characters needed to write Chinese, and failed to replace
  wood block printing.  Johannes Gutenberg is credited as the first European
  to use movable type in the 1440s --- his metal type enabled the printing
  revolution.  Ottmar Mergenthaler invented the Linotype machine in the 1884,
  which dramatically increased the speed of setting type for printing compared
  to the previous manual typesetting.  It set an entire line of type (hence
  the name) at a time, and was controlled by a keyboard.  The Monotype
  machine, invented in 1885 by Tolbert Lanston, performed similar work.
-->

```swift
enum PrinterError: Error {
    case outOfPaper
    case noToner
    case onFire
}
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> enum PrinterError: Error {
         case outOfPaper
         case noToner
         case onFire
     }
  ```
-->

Use `throw` para lançar um erro
e `throws` para marcar uma função que pode lançar um erro.
Se você lançar um erro em uma função,
a função retorna imediatamente e o código que a chamou trata o erro.

```swift
func send(job: Int, toPrinter printerName: String) throws -> String {
    if printerName == "Never Has Toner" {
        throw PrinterError.noToner
    }
    return "Job sent"
}
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> func send(job: Int, toPrinter printerName: String) throws -> String {
         if printerName == "Never Has Toner" {
             throw PrinterError.noToner
         }
         return "Job sent"
     }
  ```
-->

Há várias formas de tratar erros.
Uma delas é usar `do`-`catch`.
Dentro do bloco `do`,
você marca o código que pode lançar um erro escrevendo `try` na frente dele.
Dentro do bloco `catch`,
o erro recebe automaticamente o nome `error`,
a menos que você dê a ele outro nome.

```swift
do {
    let printerResponse = try send(job: 1040, toPrinter: "Bi Sheng")
    print(printerResponse)
} catch {
    print(error)
}
// Prints "Job sent".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> do {
         let printerResponse = try send(job: 1040, toPrinter: "Bi Sheng")
         print(printerResponse)
     } catch {
         print(error)
     }
  <- Job sent
  ```
-->

> Experimente: altere o nome da impressora para `"Never Has Toner"`,
> de modo que a função `send(job:toPrinter:)` lance um erro.

<!--
  Assertion tests the change that the Experiment box instructs you to make.
-->

<!--
  - test: `guided-tour`

  ```swifttest
  >> do {
         let printerResponse = try send(job: 500, toPrinter: "Never Has Toner")
         print(printerResponse)
     } catch {
         print(error)
     }
  <- noToner
  ```
-->

Você pode fornecer vários blocos `catch`
que tratam erros específicos.
Você escreve um padrão depois de `catch`, assim como faz
depois de `case` em um `switch`.

<!--
  REFERENCE
  The "rest of the fire" quote comes from The IT Crowd, season 1 episode 2.
-->

```swift
do {
    let printerResponse = try send(job: 1440, toPrinter: "Gutenberg")
    print(printerResponse)
} catch PrinterError.onFire {
    print("I'll just put this over here, with the rest of the fire.")
} catch let printerError as PrinterError {
    print("Printer error: \(printerError).")
} catch {
    print(error)
}
// Prints "Job sent".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> do {
         let printerResponse = try send(job: 1440, toPrinter: "Gutenberg")
         print(printerResponse)
     } catch PrinterError.onFire {
         print("I'll just put this over here, with the rest of the fire.")
     } catch let printerError as PrinterError {
         print("Printer error: \(printerError).")
     } catch {
         print(error)
     }
  <- Job sent
  ```
-->

> Experimente: adicione código que lance um erro dentro do bloco `do`.
> Que tipo de erro você precisa lançar
> para que ele seja tratado pelo primeiro bloco `catch`?
> E pelo segundo e terceiro blocos?

Outra forma de tratar erros
é usar `try?` para converter o resultado em um optional.
Se a função lançar um erro,
o erro específico é descartado e o resultado é `nil`.
Caso contrário, o resultado é um optional contendo
o valor que a função retornou.

```swift
let printerSuccess = try? send(job: 1884, toPrinter: "Mergenthaler")
let printerFailure = try? send(job: 1885, toPrinter: "Never Has Toner")
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> let printerSuccess = try? send(job: 1884, toPrinter: "Mergenthaler")
  >> print(printerSuccess as Any)
  << Optional("Job sent")
  -> let printerFailure = try? send(job: 1885, toPrinter: "Never Has Toner")
  >> print(printerFailure as Any)
  << nil
  ```
-->

Use `defer` para escrever um bloco de código
que é executado depois de todo o restante do código da função,
logo antes de a função retornar.
O código é executado independentemente de a função lançar um erro ou não.
Você pode usar `defer` para escrever código de configuração e de limpeza lado a lado,
mesmo que eles precisem ser executados em momentos diferentes.

```swift
var fridgeIsOpen = false
let fridgeContent = ["milk", "eggs", "leftovers"]

func fridgeContains(_ food: String) -> Bool {
    fridgeIsOpen = true
    defer {
        fridgeIsOpen = false
    }

    let result = fridgeContent.contains(food)
    return result
}
if fridgeContains("banana") {
    print("Found a banana")
}
print(fridgeIsOpen)
// Prints "false".
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> var fridgeIsOpen = false
  -> let fridgeContent = ["milk", "eggs", "leftovers"]

  -> func fridgeContains(_ food: String) -> Bool {
         fridgeIsOpen = true
         defer {
             fridgeIsOpen = false
         }

         let result = fridgeContent.contains(food)
         return result
     }
  >> let containsBanana =
  -> fridgeContains("banana")
  >> print(containsBanana)
  << false
  -> print(fridgeIsOpen)
  <- false
  ```
-->

## Genéricos

Escreva um nome entre colchetes angulares
para criar uma função ou um tipo genérico.

<!--
  REFERENCE
  The four knocks is a reference to Dr Who series 4,
  in which knocking four times is a running aspect
  of the season's plot.
-->

```swift
func makeArray<Item>(repeating item: Item, numberOfTimes: Int) -> [Item] {
    var result: [Item] = []
    for _ in 0..<numberOfTimes {
         result.append(item)
    }
    return result
}
makeArray(repeating: "knock", numberOfTimes: 4)
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> func makeArray<Item>(repeating item: Item, numberOfTimes: Int) -> [Item] {
         var result: [Item] = []
         for _ in 0..<numberOfTimes {
              result.append(item)
         }
         return result
     }
  >> let fourKnocks =
  -> makeArray(repeating: "knock", numberOfTimes: 4)
  >> print(fourKnocks)
  << ["knock", "knock", "knock", "knock"]
  ```
-->

Você pode criar formas genéricas de funções e métodos,
assim como de classes, enums e structs.

```swift
// Reimplement the Swift standard library's optional type
enum OptionalValue<Wrapped> {
    case none
    case some(Wrapped)
}
var possibleInteger: OptionalValue<Int> = .none
possibleInteger = .some(100)
```

<!--
  - test: `guided-tour`

  ```swifttest
  // Reimplement the Swift standard library's optional type
  -> enum OptionalValue<Wrapped> {
         case none
         case some(Wrapped)
     }
  -> var possibleInteger: OptionalValue<Int> = .none
  -> possibleInteger = .some(100)
  ```
-->

Use `where` logo antes do corpo
para especificar uma lista de requisitos:
por exemplo,
para exigir que o tipo implemente um protocolo,
para exigir que dois tipos sejam iguais,
ou para exigir que uma classe tenha uma superclasse específica.

```swift
func anyCommonElements<T: Sequence, U: Sequence>(_ lhs: T, _ rhs: U) -> Bool
    where T.Element: Equatable, T.Element == U.Element
{
    for lhsItem in lhs {
        for rhsItem in rhs {
            if lhsItem == rhsItem {
                return true
            }
        }
    }
   return false
}
anyCommonElements([1, 2, 3], [3])
```

<!--
  - test: `guided-tour`

  ```swifttest
  -> func anyCommonElements<T: Sequence, U: Sequence>(_ lhs: T, _ rhs: U) -> Bool
         where T.Element: Equatable, T.Element == U.Element
     {
         for lhsItem in lhs {
             for rhsItem in rhs {
                 if lhsItem == rhsItem {
                     return true
                 }
             }
         }
        return false
     }
  >> let hasAnyCommon =
  -> anyCommonElements([1, 2, 3], [3])
  >> print(hasAnyCommon)
  << true
  ```
-->

> Experimente: modifique a função `anyCommonElements(_:_:)`
> para criar uma função que retorne um array
> com os elementos que quaisquer duas sequências têm em comum.

Escrever `<T: Equatable>`
é o mesmo que escrever `<T> ... where T: Equatable`.

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->

<!-- ia-translate: true -->
