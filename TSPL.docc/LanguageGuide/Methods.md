# Métodos

Defina e chame funções que fazem parte de uma instância ou de um tipo.

*Métodos* são funções associadas a um tipo específico.
Classes, estruturas e enumerações podem definir métodos de instância,
que encapsulam tarefas e funcionalidades específicas para trabalhar com uma instância de um determinado tipo.
Classes, estruturas e enumerações também podem definir métodos de tipo,
que estão associados ao próprio tipo.
Métodos de tipo são parecidos com os métodos de classe do Objective-C.

O fato de estruturas e enumerações poderem definir métodos em Swift
é uma diferença importante em relação ao C e ao Objective-C.
Em Objective-C, classes são os únicos tipos que podem definir métodos.
Em Swift, você escolhe se vai definir uma classe, uma estrutura ou uma enumeração,
e ainda tem a flexibilidade de definir métodos no tipo que criar.

## Métodos de instância

*Métodos de instância* são funções que pertencem às instâncias de
uma determinada classe, estrutura ou enumeração.
Eles sustentam a funcionalidade dessas instâncias,
seja fornecendo formas de acessar e modificar propriedades da instância,
seja fornecendo funcionalidades relacionadas à finalidade da instância.
Métodos de instância têm exatamente a mesma sintaxe das funções,
como descrito em <doc:Functions>.

Você escreve um método de instância entre as chaves de abertura e de fechamento do tipo ao qual ele pertence.
Um método de instância tem acesso implícito a todos os outros métodos e propriedades desse tipo.
Um método de instância só pode ser chamado em uma instância específica do tipo ao qual pertence.
Ele não pode ser chamado isoladamente, sem uma instância existente.

Veja um exemplo que define uma classe `Counter` simples,
que pode ser usada para contar quantas vezes uma ação acontece:

```swift
class Counter {
    var count = 0
    func increment() {
        count += 1
    }
    func increment(by amount: Int) {
        count += amount
    }
    func reset() {
        count = 0
    }
}
```

<!--
  - test: `instanceMethods`

  ```swifttest
  -> class Counter {
        var count = 0
        func increment() {
           count += 1
        }
        func increment(by amount: Int) {
           count += amount
        }
        func reset() {
           count = 0
        }
     }
  ```
-->

A classe `Counter` define três métodos de instância:

- `increment()` incrementa o contador em `1`.
- `increment(by: Int)` incrementa o contador por uma quantidade inteira especificada.
- `reset()` zera o contador.

A classe `Counter` também declara uma propriedade variável, `count`,
para acompanhar o valor atual do contador.

Você chama métodos de instância com a mesma sintaxe de ponto usada para propriedades:

```swift
let counter = Counter()
// the initial counter value is 0
counter.increment()
// the counter's value is now 1
counter.increment(by: 5)
// the counter's value is now 6
counter.reset()
// the counter's value is now 0
```

<!--
  - test: `instanceMethods`

  ```swifttest
  -> let counter = Counter()
  /> the initial counter value is \(counter.count)
  </ the initial counter value is 0
  -> counter.increment()
  /> the counter's value is now \(counter.count)
  </ the counter's value is now 1
  -> counter.increment(by: 5)
  /> the counter's value is now \(counter.count)
  </ the counter's value is now 6
  -> counter.reset()
  /> the counter's value is now \(counter.count)
  </ the counter's value is now 0
  ```
-->

Parâmetros de função podem ter tanto um nome (para uso dentro do corpo da função)
quanto um rótulo de argumento (para uso na chamada da função),
como descrito em <doc:Functions#Function-Argument-Labels-and-Parameter-Names>.
O mesmo vale para parâmetros de método,
porque métodos são apenas funções associadas a um tipo.

### A propriedade self

Toda instância de um tipo tem uma propriedade implícita chamada `self`,
que é exatamente equivalente à própria instância.
Você usa a propriedade `self` para se referir à instância atual
dentro dos seus próprios métodos de instância.

O método `increment()` do exemplo acima poderia ter sido escrito assim:

```swift
func increment() {
    self.count += 1
}
```

<!--
  - test: `instanceMethodsIncrement`

  ```swifttest
  >> class Counter {
  >> var count: Int = 0
     func increment() {
        self.count += 1
     }
  >> }
  ```
-->

<!--
  NOTE: I'm slightly cheating with my testing of this excerpt, but it works!
-->

Na prática, você não precisa escrever `self` no seu código com muita frequência.
Se você não escrever `self` explicitamente,
o Swift entende que você está se referindo a uma propriedade ou método da instância atual
sempre que usar, dentro de um método, o nome de uma propriedade ou método conhecido.
Essa suposição é demonstrada pelo uso de `count` (em vez de `self.count`)
dentro dos três métodos de instância de `Counter`.

A principal exceção a essa regra acontece quando o nome de um parâmetro de método de instância
tem o mesmo nome de uma propriedade dessa instância.
Nessa situação, o nome do parâmetro tem precedência,
e fica necessário se referir à propriedade de forma mais qualificada.
Você usa a propriedade `self` para
distinguir o nome do parâmetro do nome da propriedade.

Aqui, `self` diferencia um parâmetro de método chamado `x` de uma propriedade de instância que também se chama `x`:

```swift
struct Point {
    var x = 0.0, y = 0.0
    func isToTheRightOf(x: Double) -> Bool {
        return self.x > x
    }
}
let somePoint = Point(x: 4.0, y: 5.0)
if somePoint.isToTheRightOf(x: 1.0) {
    print("This point is to the right of the line where x == 1.0")
}
// Prints "This point is to the right of the line where x == 1.0".
```

<!--
  - test: `self`

  ```swifttest
  -> struct Point {
        var x = 0.0, y = 0.0
        func isToTheRightOf(x: Double) -> Bool {
           return self.x > x
        }
     }
  -> let somePoint = Point(x: 4.0, y: 5.0)
  -> if somePoint.isToTheRightOf(x: 1.0) {
        print("This point is to the right of the line where x == 1.0")
     }
  <- This point is to the right of the line where x == 1.0
  ```
-->

Sem o prefixo `self`,
o Swift entenderia que os dois usos de `x` se referem ao parâmetro do método chamado `x`.

### Modificando tipos de valor dentro de métodos de instância

Estruturas e enumerações são *tipos de valor*.
Por padrão, as propriedades de um tipo de valor não podem ser modificadas dentro dos seus métodos de instância.

<!--
  TODO: find out why.  once I actually know why, explain it.
-->

No entanto, se você precisar modificar as propriedades da sua estrutura ou enumeração
dentro de um método específico,
pode optar pelo comportamento *mutating* para esse método.
O método pode então mutar (ou seja, alterar)
suas propriedades de dentro do método,
e as alterações que ele fizer são gravadas de volta na estrutura original quando o método terminar.
O método também pode atribuir uma instância completamente nova à propriedade implícita `self`,
e essa nova instância substituirá a existente quando o método terminar.

Você opta por esse comportamento colocando a palavra-chave `mutating`
antes da palavra-chave `func` do método:

```swift
struct Point {
    var x = 0.0, y = 0.0
    mutating func moveBy(x deltaX: Double, y deltaY: Double) {
        x += deltaX
        y += deltaY
    }
}
var somePoint = Point(x: 1.0, y: 1.0)
somePoint.moveBy(x: 2.0, y: 3.0)
print("The point is now at (\(somePoint.x), \(somePoint.y))")
// Prints "The point is now at (3.0, 4.0)".
```

<!--
  - test: `selfStructures`

  ```swifttest
  -> struct Point {
        var x = 0.0, y = 0.0
        mutating func moveBy(x deltaX: Double, y deltaY: Double) {
           x += deltaX
           y += deltaY
        }
     }
  -> var somePoint = Point(x: 1.0, y: 1.0)
  -> somePoint.moveBy(x: 2.0, y: 3.0)
  -> print("The point is now at (\(somePoint.x), \(somePoint.y))")
  <- The point is now at (3.0, 4.0)
  ```
-->

A estrutura `Point` acima define um método `mutating` chamado `moveBy(x:y:)`,
que move uma instância de `Point` em certa quantidade.
Em vez de retornar um novo ponto,
esse método de fato modifica o ponto sobre o qual é chamado.
A palavra-chave `mutating` é adicionada à sua definição
para permitir que ele modifique suas propriedades.

Observe que você não pode chamar um método `mutating` em uma constante de tipo estrutura,
porque as propriedades dela não podem ser alteradas, mesmo que sejam propriedades variáveis,
como descrito em <doc:Properties#Stored-Properties-of-Constant-Structure-Instances>:

```swift
let fixedPoint = Point(x: 3.0, y: 3.0)
fixedPoint.moveBy(x: 2.0, y: 3.0)
// this will report an error
```

<!--
  - test: `selfStructures-err`

  ```swifttest
  >> struct Point {
  >>    var x = 0.0, y = 0.0
  >>    mutating func moveBy(x deltaX: Double, y deltaY: Double) {
  >>       x += deltaX
  >>       y += deltaY
  >>    }
  >> }
  -> let fixedPoint = Point(x: 3.0, y: 3.0)
  -> fixedPoint.moveBy(x: 2.0, y: 3.0)
  !$ error: cannot use mutating member on immutable value: 'fixedPoint' is a 'let' constant
  !! fixedPoint.moveBy(x: 2.0, y: 3.0)
  !! ~~~~~~~~~~ ^
  !$ note: change 'let' to 'var' to make it mutable
  !! let fixedPoint = Point(x: 3.0, y: 3.0)
  !! ^~~
  !! var
  // this will report an error
  ```
-->

<!--
  TODO: talk about nonmutating as well.
  Struct setters are implicitly 'mutating' by default and thus don't work on 'let's.
  However, JoeG says that this ought to work
  if the setter for the computed property is explicitly defined as @!mutating.
-->

### Atribuindo a self dentro de um método mutating

Métodos `mutating` podem atribuir uma instância totalmente nova à propriedade implícita `self`.
O exemplo `Point` mostrado acima poderia ter sido escrito assim:

```swift
struct Point {
    var x = 0.0, y = 0.0
    mutating func moveBy(x deltaX: Double, y deltaY: Double) {
        self = Point(x: x + deltaX, y: y + deltaY)
    }
}
```

<!--
  - test: `selfStructuresAssign`

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

Esta versão do método `mutating` `moveBy(x:y:)` cria uma nova estrutura
cujos valores de `x` e `y` são definidos como a posição de destino.
O resultado final de chamar esta versão alternativa do método
será exatamente o mesmo de chamar a versão anterior.

Métodos `mutating` de enumerações podem definir o parâmetro implícito `self` como
outro caso da mesma enumeração:

```swift
enum TriStateSwitch {
    case off, low, high
    mutating func next() {
        switch self {
        case .off:
            self = .low
        case .low:
            self = .high
        case .high:
            self = .off
        }
    }
}
var ovenLight = TriStateSwitch.low
ovenLight.next()
// ovenLight is now equal to .high
ovenLight.next()
// ovenLight is now equal to .off
```

<!--
  - test: `selfEnumerations`

  ```swifttest
  -> enum TriStateSwitch {
        case off, low, high
        mutating func next() {
           switch self {
              case .off:
                 self = .low
              case .low:
                 self = .high
              case .high:
                 self = .off
           }
        }
     }
  -> var ovenLight = TriStateSwitch.low
  -> ovenLight.next()
  // ovenLight is now equal to .high
  -> ovenLight.next()
  // ovenLight is now equal to .off
  ```
-->

Este exemplo define uma enumeração para um interruptor de três estados.
O interruptor percorre três estados de energia diferentes
(`off`, `low` e `high`)
cada vez que seu método `next()` é chamado.

## Métodos de tipo

Métodos de instância, como descritos acima,
são métodos que você chama em uma instância de um determinado tipo.
Você também pode definir métodos que são chamados no próprio tipo.
Esses métodos são chamados de *métodos de tipo*.
Você indica um método de tipo escrevendo
a palavra-chave `static` antes da palavra-chave `func` do método.
Classes podem usar a palavra-chave `class` no lugar,
para permitir que subclasses sobrescrevam a implementação desse método da superclasse.

> Nota: No Objective-C, você só pode definir métodos em nível de tipo para classes do Objective-C.
> No Swift, você pode definir métodos de tipo para todas as classes, estruturas e enumerações.
> Cada método de tipo é explicitamente restrito ao tipo que ele atende.

Métodos de tipo são chamados com sintaxe de ponto, como métodos de instância.
No entanto, você chama métodos de tipo no tipo, e não em uma instância desse tipo.
Veja como chamar um método de tipo em uma classe chamada `SomeClass`:

```swift
class SomeClass {
    class func someTypeMethod() {
        // type method implementation goes here
    }
}
SomeClass.someTypeMethod()
```

<!--
  - test: `typeMethods`

  ```swifttest
  -> class SomeClass {
        class func someTypeMethod() {
           // type method implementation goes here
        }
     }
  -> SomeClass.someTypeMethod()
  ```
-->

Dentro do corpo de um método de tipo,
a propriedade implícita `self` se refere ao próprio tipo,
e não a uma instância desse tipo.
Isso significa que você pode usar `self` para diferenciar propriedades de tipo
de parâmetros de método de tipo, assim como faz com propriedades de instância
e parâmetros de método de instância.

De modo geral, quaisquer nomes de métodos e propriedades não qualificados que você usar
dentro do corpo de um método de tipo se referirão a outros métodos e propriedades de nível de tipo.
Um método de tipo pode chamar outro método de tipo pelo nome dele,
sem precisar prefixá-lo com o nome do tipo.
Da mesma forma, métodos de tipo de estruturas e enumerações podem acessar propriedades de tipo
usando o nome da propriedade, sem prefixo com o nome do tipo.

O exemplo abaixo define uma estrutura chamada `LevelTracker`,
que acompanha o progresso de um jogador pelos diferentes níveis ou fases de um jogo.
É um jogo para um jogador,
mas pode guardar informações de vários jogadores em um único dispositivo.

Todos os níveis do jogo (exceto o nível um) estão bloqueados quando o jogo é jogado pela primeira vez.
Sempre que um jogador termina um nível,
esse nível é desbloqueado para todos os jogadores do dispositivo.
A estrutura `LevelTracker` usa propriedades e métodos de tipo
para acompanhar quais níveis do jogo foram desbloqueados.
Ela também acompanha o nível atual de um jogador individual.

```swift
struct LevelTracker {
    static var highestUnlockedLevel = 1
    var currentLevel = 1

    static func unlock(_ level: Int) {
        if level > highestUnlockedLevel { highestUnlockedLevel = level }
    }

    static func isUnlocked(_ level: Int) -> Bool {
        return level <= highestUnlockedLevel
    }

    @discardableResult
    mutating func advance(to level: Int) -> Bool {
        if LevelTracker.isUnlocked(level) {
            currentLevel = level
            return true
        } else {
            return false
        }
    }
}
```

<!--
  - test: `typeMethods`

  ```swifttest
  -> struct LevelTracker {
        static var highestUnlockedLevel = 1
        var currentLevel = 1

  ->    static func unlock(_ level: Int) {
           if level > highestUnlockedLevel { highestUnlockedLevel = level }
        }

  ->    static func isUnlocked(_ level: Int) -> Bool {
           return level <= highestUnlockedLevel
        }

  ->    @discardableResult
        mutating func advance(to level: Int) -> Bool {
           if LevelTracker.isUnlocked(level) {
              currentLevel = level
              return true
           } else {
              return false
           }
        }
     }
  ```
-->

A estrutura `LevelTracker` mantém o registro do nível mais alto que qualquer jogador desbloqueou.
Esse valor fica armazenado em uma propriedade de tipo chamada `highestUnlockedLevel`.

`LevelTracker` também define duas funções de tipo para trabalhar com
a propriedade `highestUnlockedLevel`.
A primeira é uma função de tipo chamada `unlock(_:)`,
que atualiza o valor de `highestUnlockedLevel` sempre que um novo nível é desbloqueado.
A segunda é uma função de tipo de conveniência chamada `isUnlocked(_:)`,
que retorna `true` se determinado número de nível já estiver desbloqueado.
(Observe que esses métodos de tipo podem acessar a propriedade de tipo `highestUnlockedLevel`
sem que você precise escrevê-la como `LevelTracker.highestUnlockedLevel`.)

Além da propriedade de tipo e dos métodos de tipo,
`LevelTracker` acompanha o progresso de um jogador individual pelo jogo.
Ele usa uma propriedade de instância chamada `currentLevel` para acompanhar
o nível que um jogador está jogando no momento.

Para ajudar a gerenciar a propriedade `currentLevel`,
`LevelTracker` define um método de instância chamado `advance(to:)`.
Antes de atualizar `currentLevel`,
esse método verifica se o novo nível solicitado já está desbloqueado.
O método `advance(to:)` retorna um valor booleano para indicar
se conseguiu ou não definir `currentLevel`.
Como não é necessariamente um erro
o código que chama `advance(to:)` ignorar o valor de retorno,
essa função é marcada com o atributo `@discardableResult`.
Para mais informações sobre esse atributo,
veja <doc:Attributes>.

A estrutura `LevelTracker` é usada com a classe `Player`, mostrada abaixo,
para acompanhar e atualizar o progresso de um jogador individual:

```swift
class Player {
    var tracker = LevelTracker()
    let playerName: String
    func complete(level: Int) {
        LevelTracker.unlock(level + 1)
        tracker.advance(to: level + 1)
    }
    init(name: String) {
        playerName = name
    }
}
```

<!--
  - test: `typeMethods`

  ```swifttest
  -> class Player {
        var tracker = LevelTracker()
        let playerName: String
        func complete(level: Int) {
           LevelTracker.unlock(level + 1)
           tracker.advance(to: level + 1)
        }
        init(name: String) {
           playerName = name
        }
     }
  ```
-->

A classe `Player` cria uma nova instância de `LevelTracker`
para acompanhar o progresso desse jogador.
Ela também oferece um método chamado `complete(level:)`,
que é chamado sempre que um jogador conclui determinado nível.
Esse método desbloqueia o próximo nível para todos os jogadores
e atualiza o progresso do jogador para levá-lo ao próximo nível.
(O valor de retorno booleano de `advance(to:)` é ignorado,
porque o nível já é conhecido como desbloqueado
pela chamada a `LevelTracker.unlock(_:)` na linha anterior.)

Você pode criar uma instância da classe `Player` para um novo jogador,
e ver o que acontece quando ele conclui o nível um:

```swift
var player = Player(name: "Argyrios")
player.complete(level: 1)
print("highest unlocked level is now \(LevelTracker.highestUnlockedLevel)")
// Prints "highest unlocked level is now 2".
```

<!--
  - test: `typeMethods`

  ```swifttest
  -> var player = Player(name: "Argyrios")
  -> player.complete(level: 1)
  -> print("highest unlocked level is now \(LevelTracker.highestUnlockedLevel)")
  <- highest unlocked level is now 2
  ```
-->

Se você criar um segundo jogador, e tentar levá-lo a um nível
que ainda não foi desbloqueado por nenhum jogador do jogo,
a tentativa de definir o nível atual do jogador falha:

```swift
player = Player(name: "Beto")
if player.tracker.advance(to: 6) {
    print("player is now on level 6")
} else {
    print("level 6 hasn't yet been unlocked")
}
// Prints "level 6 hasn't yet been unlocked".
```

<!--
  - test: `typeMethods`

  ```swifttest
  -> player = Player(name: "Beto")
  -> if player.tracker.advance(to: 6) {
        print("player is now on level 6")
     } else {
        print("level 6 hasn't yet been unlocked")
     }
  <- level 6 hasn't yet been unlocked
  ```
-->

<!--
  TODO: Method Binding
  --------------------

  TODO: you can get a function that refers to a method, either with or without the 'self' argument already being bound:
  class C {
     func foo(x: Int) -> Float { ... }
  }
  var c = C()
  var boundFunc = c.foo   // a function with type (Int) -> Float
  var unboundFunc = C.foo // a function with type (C) -> (Int) -> Float

  TODO: selector-style methods can be referenced as foo.bar:bas:
  (see Doug's comments from the 2014-03-12 release notes)
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
