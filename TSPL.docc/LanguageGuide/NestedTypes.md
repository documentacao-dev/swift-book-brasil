# Tipos aninhados

Defina tipos dentro do escopo de outro tipo.

Enums costumam ser criados para dar suporte à funcionalidade de uma classe ou struct específica.
Da mesma forma, pode ser conveniente definir structs utilitárias
usadas apenas no contexto de um tipo mais complexo,
além de protocolos normalmente usados em conjunto com um tipo específico.
Para isso, o Swift permite definir *tipos aninhados*,
em que você aninha tipos de apoio, como enums, structs e protocolos,
dentro da definição do tipo que eles apoiam.

Para aninhar um tipo dentro de outro,
escreva a definição dele dentro das chaves externas do tipo que ele apoia.
Os tipos podem ser aninhados em quantos níveis forem necessários.

## Tipos aninhados na prática

O exemplo abaixo define uma struct chamada `BlackjackCard`,
que modela uma carta de baralho usada no jogo de Blackjack.
A struct `BlackjackCard` contém dois enums aninhados,
chamados `Suit` e `Rank`.

No Blackjack, o Ás tem valor um ou onze.
Essa característica é representada por uma struct chamada `Values`,
que é aninhada dentro do enum `Rank`:

```swift
struct BlackjackCard {
    // nested Suit enumeration
    enum Suit: Character {
        case spades = "♠", hearts = "♡", diamonds = "♢", clubs = "♣"
    }

    // nested Rank enumeration
    enum Rank: Int {
        case two = 2, three, four, five, six, seven, eight, nine, ten
        case jack, queen, king, ace
        struct Values {
            let first: Int, second: Int?
        }
        var values: Values {
            switch self {
            case .ace:
                return Values(first: 1, second: 11)
            case .jack, .queen, .king:
                return Values(first: 10, second: nil)
            default:
                return Values(first: self.rawValue, second: nil)
            }
        }
    }

    // BlackjackCard properties and methods
    let rank: Rank, suit: Suit
    var description: String {
        var output = "suit is \(suit.rawValue),"
        output += " value is \(rank.values.first)"
        if let second = rank.values.second {
            output += " or \(second)"
        }
        return output
    }
}
```

<!--
  - test: `nestedTypes`

  ```swifttest
  -> struct BlackjackCard {
        // nested Suit enumeration
        enum Suit: Character {
           case spades = "♠", hearts = "♡", diamonds = "♢", clubs = "♣"
        }

        // nested Rank enumeration
        enum Rank: Int {
           case two = 2, three, four, five, six, seven, eight, nine, ten
           case jack, queen, king, ace
           struct Values {
              let first: Int, second: Int?
           }
           var values: Values {
              switch self {
                 case .ace:
                    return Values(first: 1, second: 11)
                 case .jack, .queen, .king:
                    return Values(first: 10, second: nil)
                 default:
                    return Values(first: self.rawValue, second: nil)
              }
           }
        }

        // BlackjackCard properties and methods
        let rank: Rank, suit: Suit
        var description: String {
           var output = "suit is \(suit.rawValue),"
           output += " value is \(rank.values.first)"
           if let second = rank.values.second {
              output += " or \(second)"
           }
           return output
        }
     }
  ```
-->

O enum `Suit` descreve os quatro naipes comuns de cartas,
junto com um raw value do tipo `Character` que representa o símbolo de cada um.

O enum `Rank` descreve as treze possíveis graduações de cartas,
junto com um raw value do tipo `Int` que representa o valor de face.
(Esse raw value `Int` não é usado para as cartas Valete, Dama, Rei e Ás.)

Como mencionado acima, o enum `Rank` define
uma struct aninhada própria, chamada `Values`.
Essa struct encapsula o fato de que a maioria das cartas tem um valor,
mas o Ás tem dois.
A struct `Values` define duas propriedades para representar isso:

- `first`, do tipo `Int`
- `second`, do tipo `Int?`, ou “`Int` optional”

`Rank` também define uma propriedade computada, `values`,
que retorna uma instância da struct `Values`.
Essa propriedade computada considera a graduação da carta
e inicializa uma nova instância de `Values` com os valores adequados para essa graduação.
Ela usa valores especiais para `jack`, `queen`, `king` e `ace`.
Para as cartas numéricas, usa o raw value `Int` da graduação.

A própria struct `BlackjackCard` tem duas propriedades: `rank` e `suit`.
Ela também define uma propriedade computada chamada `description`,
que usa os valores armazenados em `rank` e `suit` para montar
uma descrição do nome e do valor da carta.
A propriedade `description` usa optional binding para verificar se há
um segundo valor a exibir e, se houver,
inclui um detalhe adicional na descrição para esse segundo valor.

Como `BlackjackCard` é uma struct sem inicializadores personalizados,
ela tem um inicializador memberwise implícito,
como descrito em <doc:Initialization#Memberwise-Initializers-for-Structure-Types>.
Você pode usar esse inicializador para criar uma nova constante chamada `theAceOfSpades`:

```swift
let theAceOfSpades = BlackjackCard(rank: .ace, suit: .spades)
print("theAceOfSpades: \(theAceOfSpades.description)")
// Prints "theAceOfSpades: suit is ♠, value is 1 or 11".
```

<!--
  - test: `nestedTypes`

  ```swifttest
  -> let theAceOfSpades = BlackjackCard(rank: .ace, suit: .spades)
  -> print("theAceOfSpades: \(theAceOfSpades.description)")
  <- theAceOfSpades: suit is ♠, value is 1 or 11
  ```
-->

Mesmo que `Rank` e `Suit` estejam aninhados dentro de `BlackjackCard`,
o tipo deles pode ser inferido pelo contexto,
então a inicialização dessa instância consegue se referir aos casos do enum
apenas pelos nomes dos casos (`.ace` e `.spades`).
No exemplo acima, a propriedade `description` informa corretamente
que o Ás de Espadas tem valor `1` ou `11`.

## Como se referir a tipos aninhados

Para usar um tipo aninhado fora do contexto em que ele é definido,
coloque antes do nome dele o nome do tipo em que ele está aninhado:

```swift
let heartsSymbol = BlackjackCard.Suit.hearts.rawValue
// heartsSymbol is "♡"
```

<!--
  - test: `nestedTypes`

  ```swifttest
  -> let heartsSymbol = BlackjackCard.Suit.hearts.rawValue
  /> heartsSymbol is \"\(heartsSymbol)\"
  </ heartsSymbol is "♡"
  ```
-->

No exemplo acima,
isso permite que os nomes de `Suit`, `Rank` e `Values` sejam mantidos propositalmente curtos,
porque o contexto em que eles são definidos já os qualifica naturalmente.

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->

<!-- ia-translate: true -->
