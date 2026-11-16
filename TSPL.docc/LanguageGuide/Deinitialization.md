# Desinicialização

Libere recursos que precisam de uma limpeza personalizada.

Um *desinicializador* é chamado logo antes de uma instância de classe ser desalocada.
Você escreve desinicializadores com a palavra-chave `deinit`,
do mesmo jeito que escreve inicializadores com a palavra-chave `init`.
Desinicializadores só estão disponíveis em tipos classe.

## Como a desinicialização funciona

O Swift desaloca automaticamente suas instâncias quando elas não são mais necessárias,
para liberar recursos.
O Swift gerencia a memória das instâncias por meio da
*contagem automática de referências* (*ARC*),
como descrito em <doc:AutomaticReferenceCounting>.
Normalmente, você não precisa fazer uma limpeza manual quando suas instâncias são desalocadas.
No entanto, quando você trabalha com recursos próprios,
pode ser necessário fazer alguma limpeza adicional por conta própria.
Por exemplo, se você cria uma classe personalizada para abrir um arquivo e gravar alguns dados nele,
talvez precise fechar o arquivo antes de a instância da classe ser desalocada.

Uma definição de classe pode ter no máximo um desinicializador por classe.
O desinicializador não recebe parâmetros
e é escrito sem parênteses:

```swift
deinit {
    // perform the deinitialization
}
```

<!--
  - test: `deinitializer`

  ```swifttest
  >> class Test {
  -> deinit {
        // perform the deinitialization
     }
  >> }
  ```
-->

Os desinicializadores são chamados automaticamente, logo antes de a instância ser desalocada.
Você não pode chamar um desinicializador por conta própria.
Os desinicializadores da superclasse são herdados pelas subclasses,
e o desinicializador da superclasse é chamado automaticamente no fim
da implementação do desinicializador da subclasse.
Os desinicializadores da superclasse são sempre chamados,
mesmo quando uma subclasse não fornece um desinicializador próprio.

Como a instância só é desalocada depois que o desinicializador é chamado,
um desinicializador pode acessar todas as propriedades da instância à qual pertence
e pode modificar seu comportamento com base nessas propriedades
(por exemplo, procurando o nome de um arquivo que precisa ser fechado).

## Desinicializadores na prática

Veja um exemplo de desinicializador em ação.
Este exemplo define dois novos tipos, `Bank` e `Player`, para um jogo simples.
A classe `Bank` gerencia uma moeda fictícia,
que nunca pode ter mais de 10.000 moedas em circulação.
Só pode existir um `Bank` no jogo,
por isso o `Bank` é implementado como uma classe com propriedades e métodos de tipo
para armazenar e gerenciar o seu estado atual:

```swift
class Bank {
    static var coinsInBank = 10_000
    static func distribute(coins numberOfCoinsRequested: Int) -> Int {
        let numberOfCoinsToVend = min(numberOfCoinsRequested, coinsInBank)
        coinsInBank -= numberOfCoinsToVend
        return numberOfCoinsToVend
    }
    static func receive(coins: Int) {
        coinsInBank += coins
    }
}
```

<!--
  - test: `deinitializer`

  ```swifttest
  -> class Bank {
        static var coinsInBank = 10_000
        static func distribute(coins numberOfCoinsRequested: Int) -> Int {
           let numberOfCoinsToVend = min(numberOfCoinsRequested, coinsInBank)
           coinsInBank -= numberOfCoinsToVend
           return numberOfCoinsToVend
        }
        static func receive(coins: Int) {
           coinsInBank += coins
        }
     }
  ```
-->

O `Bank` mantém o controle da quantidade atual de moedas que tem,
com a propriedade `coinsInBank`.
Ele também oferece dois métodos, `distribute(coins:)` e `receive(coins:)`,
para cuidar da distribuição e do recolhimento de moedas.

O método `distribute(coins:)` verifica se há moedas suficientes no banco antes de distribuí-las.
Se não houver moedas suficientes,
o `Bank` retorna um número menor do que o que foi solicitado
(e retorna zero se não restar nenhuma moeda no banco).
Ele retorna um valor inteiro para indicar a quantidade real de moedas fornecidas.

O método `receive(coins:)` simplesmente soma o número de moedas recebidas de volta ao estoque do banco.

A classe `Player` descreve um jogador do jogo.
Cada jogador tem, a qualquer momento, certa quantidade de moedas guardada na bolsa.
Isso é representado pela propriedade `coinsInPurse` do jogador:

```swift
class Player {
    var coinsInPurse: Int
    init(coins: Int) {
        coinsInPurse = Bank.distribute(coins: coins)
    }
    func win(coins: Int) {
        coinsInPurse += Bank.distribute(coins: coins)
    }
    deinit {
        Bank.receive(coins: coinsInPurse)
    }
}
```

<!--
  - test: `deinitializer`

  ```swifttest
  -> class Player {
        var coinsInPurse: Int
        init(coins: Int) {
           coinsInPurse = Bank.distribute(coins: coins)
        }
        func win(coins: Int) {
           coinsInPurse += Bank.distribute(coins: coins)
        }
        deinit {
           Bank.receive(coins: coinsInPurse)
        }
     }
  ```
-->

Cada instância de `Player` é inicializada com uma mesada inicial,
um número determinado de moedas retiradas do banco durante a inicialização,
embora uma instância de `Player` possa receber menos do que isso
se não houver moedas suficientes disponíveis.

A classe `Player` define um método `win(coins:)`,
que retira certo número de moedas do banco
e as adiciona à bolsa do jogador.
A classe `Player` também implementa um desinicializador,
que é chamado logo antes de uma instância de `Player` ser desalocada.
Aqui, o desinicializador simplesmente devolve todas as moedas do jogador ao banco:

```swift
var playerOne: Player? = Player(coins: 100)
print("A new player has joined the game with \(playerOne!.coinsInPurse) coins")
// Prints "A new player has joined the game with 100 coins".
print("There are now \(Bank.coinsInBank) coins left in the bank")
// Prints "There are now 9900 coins left in the bank".
```

<!--
  - test: `deinitializer`

  ```swifttest
  -> var playerOne: Player? = Player(coins: 100)
  -> print("A new player has joined the game with \(playerOne!.coinsInPurse) coins")
  <- A new player has joined the game with 100 coins
  -> print("There are now \(Bank.coinsInBank) coins left in the bank")
  <- There are now 9900 coins left in the bank
  ```
-->

Uma nova instância de `Player` é criada, pedindo 100 moedas, se estiverem disponíveis.
Essa instância de `Player` é guardada em uma variável opcional de `Player` chamada `playerOne`.
Aqui usamos uma variável opcional porque jogadores podem sair do jogo a qualquer momento.
O optional permite saber se há um jogador no jogo no momento.

Como `playerOne` é um optional, ele recebe um ponto de exclamação (`!`)
ao ter a propriedade `coinsInPurse` acessada para imprimir sua quantidade padrão de moedas,
e sempre que o método `win(coins:)` é chamado:

```swift
playerOne!.win(coins: 2_000)
print("PlayerOne won 2000 coins & now has \(playerOne!.coinsInPurse) coins")
// Prints "PlayerOne won 2000 coins & now has 2100 coins".
print("The bank now only has \(Bank.coinsInBank) coins left")
// Prints "The bank now only has 7900 coins left".
```

<!--
  - test: `deinitializer`

  ```swifttest
  -> playerOne!.win(coins: 2_000)
  -> print("PlayerOne won 2000 coins & now has \(playerOne!.coinsInPurse) coins")
  <- PlayerOne won 2000 coins & now has 2100 coins
  -> print("The bank now only has \(Bank.coinsInBank) coins left")
  <- The bank now only has 7900 coins left
  ```
-->

Aqui, o jogador ganhou 2.000 moedas.
A bolsa do jogador agora contém 2.100 moedas,
e o banco tem apenas 7.900 moedas restantes.

```swift
playerOne = nil
print("PlayerOne has left the game")
// Prints "PlayerOne has left the game".
print("The bank now has \(Bank.coinsInBank) coins")
// Prints "The bank now has 10000 coins".
```

<!--
  - test: `deinitializer`

  ```swifttest
  -> playerOne = nil
  -> print("PlayerOne has left the game")
  <- PlayerOne has left the game
  -> print("The bank now has \(Bank.coinsInBank) coins")
  <- The bank now has 10000 coins
  ```
-->

O jogador agora saiu do jogo.
Isso é indicado ao definir a variável opcional `playerOne` como `nil`,
o que significa “nenhuma instância de `Player`”.
Nesse momento, a referência da variável `playerOne` à instância de `Player` é desfeita.
Nenhuma outra propriedade ou variável ainda se refere à instância de `Player`,
então ela é desalocada para liberar sua memória.
Logo antes disso acontecer, seu desinicializador é chamado automaticamente,
e suas moedas voltam para o banco.

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
