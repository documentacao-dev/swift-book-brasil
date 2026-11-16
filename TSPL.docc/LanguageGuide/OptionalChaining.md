# Optional chaining

Acesse membros de um valor optional sem fazer unwrap.

*Optional chaining* é um processo para consultar e chamar
propriedades, métodos e subscripts de um optional que pode estar `nil` no momento.
Se o optional contém um valor,
a chamada da propriedade, do método ou do subscript tem sucesso;
se o optional é `nil`, a chamada da propriedade, do método ou do subscript retorna `nil`.
Várias consultas podem ser encadeadas,
e a cadeia inteira falha de forma controlada se qualquer elo dela for `nil`.

> Nota: O optional chaining em Swift é parecido com enviar mensagens para `nil` em Objective-C,
> mas funciona para qualquer tipo e pode ser verificado para saber se deu certo ou errado.

## Optional chaining como alternativa ao unwrap forçado

Você especifica o optional chaining colocando um ponto de interrogação (`?`)
depois do valor optional sobre o qual quer acessar uma propriedade, chamar um método ou usar um subscript,
caso o optional não seja `nil`.
Isso é muito parecido com colocar um ponto de exclamação (`!`)
depois de um valor optional para forçar o unwrap do seu valor.
A principal diferença é que o optional chaining falha de forma controlada quando o optional é `nil`,
enquanto o unwrap forçado dispara um erro em tempo de execução quando o optional é `nil`.

Para refletir o fato de que o optional chaining pode ser usado sobre um valor `nil`,
o resultado de uma chamada com optional chaining é sempre um valor optional,
mesmo que a propriedade, o método ou o subscript consultado retorne um valor não optional.
Você pode usar esse valor de retorno optional para verificar se
a chamada com optional chaining deu certo
(o optional retornado contém um valor),
ou se não deu certo por causa de um valor `nil` na cadeia
(o valor optional retornado é `nil`).

Especificamente, o resultado de uma chamada com optional chaining
tem o mesmo tipo do valor de retorno esperado, mas embrulhado em um optional.
Uma propriedade que normalmente retorna um `Int` vai retornar um `Int?`
quando acessada por meio de optional chaining.

Os próximos trechos de código mostram
como o optional chaining é diferente do unwrap forçado
e como ele permite verificar se a operação deu certo.

Primeiro, duas classes chamadas `Person` e `Residence` são definidas:

```swift
class Person {
    var residence: Residence?
}

class Residence {
    var numberOfRooms = 1
}
```

<!--
  - test: `optionalChainingIntro, optionalChainingIntroAssert`

  ```swifttest
  -> class Person {
        var residence: Residence?
     }

  -> class Residence {
        var numberOfRooms = 1
     }
  ```
-->

Instâncias de `Residence` têm uma única propriedade `Int` chamada `numberOfRooms`,
com valor padrão `1`.
Instâncias de `Person` têm uma propriedade `residence` optional, do tipo `Residence?`.

Se você criar uma nova instância de `Person`,
a propriedade `residence` recebe `nil` como valor inicial,
por ser optional.
No código abaixo, `john` tem o valor `nil` na propriedade `residence`:

```swift
let john = Person()
```

<!--
  - test: `optionalChainingIntro, optionalChainingIntroAssert`

  ```swifttest
  -> let john = Person()
  ```
-->

Se você tentar acessar a propriedade `numberOfRooms` da `residence` dessa pessoa,
colocando um ponto de exclamação depois de `residence` para forçar o unwrap do seu valor,
você dispara um erro em tempo de execução,
porque não há valor de `residence` para fazer o unwrap:

```swift
let roomCount = john.residence!.numberOfRooms
// this triggers a runtime error
```

<!--
  - test: `optionalChainingIntroAssert`

  ```swifttest
  -> let roomCount = john.residence!.numberOfRooms
  xx assert
  // this triggers a runtime error
  ```
-->

O código acima funciona quando `john.residence` tem um valor diferente de `nil`
e vai atribuir a `roomCount` um valor `Int` com a quantidade correta de cômodos.
No entanto, esse código sempre dispara um erro em tempo de execução quando `residence` é `nil`,
como mostrado acima.

O optional chaining oferece outra forma de acessar o valor de `numberOfRooms`.
Para usar o optional chaining, coloque um ponto de interrogação no lugar do ponto de exclamação:

```swift
if let roomCount = john.residence?.numberOfRooms {
    print("John's residence has \(roomCount) room(s).")
} else {
    print("Unable to retrieve the number of rooms.")
}
// Prints "Unable to retrieve the number of rooms."
```

<!--
  - test: `optionalChainingIntro`

  ```swifttest
  -> if let roomCount = john.residence?.numberOfRooms {
        print("John's residence has \(roomCount) room(s).")
     } else {
        print("Unable to retrieve the number of rooms.")
     }
  <- Unable to retrieve the number of rooms.
  ```
-->

Isso diz ao Swift para “encadear” na propriedade optional `residence`
e obter o valor de `numberOfRooms` se `residence` existir.

Como a tentativa de acessar `numberOfRooms` pode falhar,
a chamada com optional chaining retorna um valor do tipo `Int?`, ou “`Int` optional”.
Quando `residence` é `nil`, como no exemplo acima,
esse `Int` optional também será `nil`,
para refletir o fato de que não foi possível acessar `numberOfRooms`.
O `Int` optional é acessado por meio de optional binding
para extrair o inteiro e atribuir o valor não optional
à constante `roomCount`.

Observe que isso vale mesmo que `numberOfRooms` seja um `Int` não optional.
O fato de a consulta passar por uma cadeia optional
faz com que a chamada a `numberOfRooms`
sempre retorne um `Int?` em vez de um `Int`.

Você pode atribuir uma instância de `Residence` a `john.residence`,
para que ela deixe de ser `nil`:

```swift
john.residence = Residence()
```

<!--
  - test: `optionalChainingIntro`

  ```swifttest
  -> john.residence = Residence()
  ```
-->

`john.residence` agora contém uma instância real de `Residence`, em vez de `nil`.
Se você tentar acessar `numberOfRooms` com o mesmo optional chaining de antes,
ele vai retornar um `Int?` que contém
o valor padrão de `numberOfRooms`, que é `1`:

```swift
if let roomCount = john.residence?.numberOfRooms {
    print("John's residence has \(roomCount) room(s).")
} else {
    print("Unable to retrieve the number of rooms.")
}
// Prints "John's residence has 1 room(s)."
```

<!--
  - test: `optionalChainingIntro`

  ```swifttest
  -> if let roomCount = john.residence?.numberOfRooms {
        print("John's residence has \(roomCount) room(s).")
     } else {
        print("Unable to retrieve the number of rooms.")
     }
  <- John's residence has 1 room(s).
  ```
-->

## Definindo classes de modelo para o optional chaining

Você pode usar o optional chaining com chamadas de propriedades, métodos e subscripts
que estão a mais de um nível de profundidade.
Isso permite navegar por subpropriedades
dentro de modelos complexos de tipos inter-relacionados,
e verificar se é possível acessar
propriedades, métodos e subscripts nessas subpropriedades.

Os trechos de código abaixo definem quatro classes de modelo
para uso em vários exemplos seguintes,
incluindo exemplos de optional chaining em vários níveis.
Essas classes expandem o modelo de `Person` e `Residence` apresentado acima,
acrescentando as classes `Room` e `Address`,
com propriedades, métodos e subscripts associados.

A classe `Person` é definida do mesmo jeito de antes:

```swift
class Person {
    var residence: Residence?
}
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> class Person {
        var residence: Residence?
     }
  ```
-->

A classe `Residence` é mais complexa do que antes.
Desta vez, ela define uma propriedade variável chamada `rooms`,
inicializada com um array vazio do tipo `[Room]`:

```swift
class Residence {
    var rooms: [Room] = []
    var numberOfRooms: Int {
        return rooms.count
    }
    subscript(i: Int) -> Room {
        get {
            return rooms[i]
        }
        set {
            rooms[i] = newValue
        }
    }
    func printNumberOfRooms() {
        print("The number of rooms is \(numberOfRooms)")
    }
    var address: Address?
}
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> class Residence {
        var rooms: [Room] = []
        var numberOfRooms: Int {
           return rooms.count
        }
        subscript(i: Int) -> Room {
           get {
              return rooms[i]
           }
           set {
              rooms[i] = newValue
           }
        }
        func printNumberOfRooms() {
           print("The number of rooms is \(numberOfRooms)")
        }
        var address: Address?
     }
  ```
-->

Como esta versão de `Residence` armazena um array de instâncias de `Room`,
sua propriedade `numberOfRooms` é implementada como propriedade computada,
e não como propriedade armazenada.
A propriedade computada `numberOfRooms` simplesmente retorna
o valor da propriedade `count` do array `rooms`.

Como atalho para acessar o array `rooms`,
esta versão de `Residence` oferece um subscript de leitura e escrita que dá acesso
ao cômodo no índice pedido do array `rooms`.

Esta versão de `Residence` também oferece um método chamado `printNumberOfRooms`,
que simplesmente imprime a quantidade de cômodos da residência.

Por fim, `Residence` define uma propriedade optional chamada `address`,
com o tipo `Address?`.
A classe `Address`, usada como tipo dessa propriedade, é definida a seguir.

A classe `Room`, usada no array `rooms`, é
uma classe simples com uma propriedade chamada `name`
e um inicializador que atribui a essa propriedade um nome adequado para o cômodo:

```swift
class Room {
    let name: String
    init(name: String) { self.name = name }
}
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> class Room {
        let name: String
        init(name: String) { self.name = name }
     }
  ```
-->

A última classe deste modelo se chama `Address`.
Essa classe tem três propriedades optional do tipo `String?`.
As duas primeiras propriedades, `buildingName` e `buildingNumber`,
são formas alternativas de identificar um prédio específico como parte de um endereço.
A terceira propriedade, `street`, guarda o nome da rua desse endereço:

```swift
class Address {
    var buildingName: String?
    var buildingNumber: String?
    var street: String?
    func buildingIdentifier() -> String? {
        if let buildingNumber = buildingNumber, let street = street {
            return "\(buildingNumber) \(street)"
        } else if buildingName != nil {
            return buildingName
        } else {
            return nil
        }
    }
}
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> class Address {
        var buildingName: String?
        var buildingNumber: String?
        var street: String?
        func buildingIdentifier() -> String? {
           if let buildingNumber, let street {
               return "\(buildingNumber) \(street)"
           } else if buildingName != nil {
               return buildingName
           } else {
               return nil
           }
        }
     }
  ```
-->

A classe `Address` também oferece um método chamado `buildingIdentifier()`,
cujo tipo de retorno é `String?`.
Esse método verifica as propriedades do endereço
e retorna `buildingName`, se ele tiver valor,
ou `buildingNumber` concatenado com `street`, se os dois tiverem valor,
ou `nil` nos demais casos.

## Acessando propriedades por meio de optional chaining

Como demonstrado em <doc:OptionalChaining#Optional-Chaining-as-an-Alternative-to-Forced-Unwrapping>,
você pode usar o optional chaining para acessar uma propriedade de um valor optional,
e verificar se o acesso à propriedade deu certo.

Use as classes definidas acima para criar uma nova instância de `Person`,
e tente acessar a propriedade `numberOfRooms` como antes:

```swift
let john = Person()
if let roomCount = john.residence?.numberOfRooms {
    print("John's residence has \(roomCount) room(s).")
} else {
    print("Unable to retrieve the number of rooms.")
}
// Prints "Unable to retrieve the number of rooms."
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> let john = Person()
  -> if let roomCount = john.residence?.numberOfRooms {
        print("John's residence has \(roomCount) room(s).")
     } else {
        print("Unable to retrieve the number of rooms.")
     }
  <- Unable to retrieve the number of rooms.
  ```
-->

Como `john.residence` é `nil`,
essa chamada com optional chaining falha da mesma forma que antes.

Você também pode tentar definir o valor de uma propriedade por meio de optional chaining:

```swift
let someAddress = Address()
someAddress.buildingNumber = "29"
someAddress.street = "Acacia Road"
john.residence?.address = someAddress
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> let someAddress = Address()
  -> someAddress.buildingNumber = "29"
  -> someAddress.street = "Acacia Road"
  -> john.residence?.address = someAddress
  ```
-->

Neste exemplo,
a tentativa de definir a propriedade `address` de `john.residence` vai falhar,
porque `john.residence` é `nil` no momento.

A atribuição faz parte do optional chaining,
o que significa que nenhum código do lado direito do operador `=` é avaliado.
No exemplo anterior,
não é fácil perceber que `someAddress` nunca é avaliado,
porque acessar uma constante não tem efeitos colaterais.
O código abaixo faz a mesma atribuição,
mas usa uma função para criar o endereço.
A função imprime “Function was called” antes de retornar um valor,
o que permite ver
se o lado direito do operador `=` foi avaliado.

```swift
func createAddress() -> Address {
    print("Function was called.")

    let someAddress = Address()
    someAddress.buildingNumber = "29"
    someAddress.street = "Acacia Road"

    return someAddress
}
john.residence?.address = createAddress()
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> func createAddress() -> Address {
         print("Function was called.")

         let someAddress = Address()
         someAddress.buildingNumber = "29"
         someAddress.street = "Acacia Road"

         return someAddress
     }
  -> john.residence?.address = createAddress()
  >> let _ = createAddress()
  << Function was called.
  ```
-->

Você pode perceber que a função `createAddress()` não é chamada,
porque nada é impresso.

## Chamando métodos por meio de optional chaining

Você pode usar o optional chaining para chamar um método sobre um valor optional,
e verificar se a chamada ao método deu certo.
Isso vale até para métodos que não definem um valor de retorno.

O método `printNumberOfRooms()` da classe `Residence`
imprime o valor atual de `numberOfRooms`.
Veja como o método é definido:

```swift
func printNumberOfRooms() {
    print("The number of rooms is \(numberOfRooms)")
}
```

<!--
  - test: `optionalChainingCallouts`

  ```swifttest
  -> func printNumberOfRooms() {
  >>    let numberOfRooms = 3
        print("The number of rooms is \(numberOfRooms)")
     }
  ```
-->

Esse método não especifica um tipo de retorno.
No entanto, funções e métodos sem tipo de retorno têm, implicitamente, o tipo de retorno `Void`,
como descrito em <doc:Functions#Functions-Without-Return-Values>.
Isso significa que eles retornam um valor `()`, ou uma tupla vazia.

Se você chamar esse método sobre um valor optional com optional chaining,
o tipo de retorno do método será `Void?`, e não `Void`,
porque valores de retorno de chamadas com optional chaining são sempre de um tipo optional.
Isso permite usar uma instrução `if`
para verificar se foi possível chamar o método `printNumberOfRooms()`,
mesmo que o método não defina um valor de retorno.
Compare o valor retornado pela chamada a `printNumberOfRooms` com `nil`
para saber se a chamada ao método deu certo:

```swift
if john.residence?.printNumberOfRooms() != nil {
    print("It was possible to print the number of rooms.")
} else {
    print("It was not possible to print the number of rooms.")
}
// Prints "It was not possible to print the number of rooms."
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> if john.residence?.printNumberOfRooms() != nil {
        print("It was possible to print the number of rooms.")
     } else {
        print("It was not possible to print the number of rooms.")
     }
  <- It was not possible to print the number of rooms.
  ```
-->

O mesmo vale para a tentativa de definir uma propriedade por meio de optional chaining.
O exemplo acima, em <doc:OptionalChaining#Accessing-Properties-Through-Optional-Chaining>,
tenta definir um valor de `address` para `john.residence`,
mesmo com a propriedade `residence` sendo `nil`.
Qualquer tentativa de definir uma propriedade por meio de optional chaining retorna um valor do tipo `Void?`,
o que permite comparar com `nil` para saber se a propriedade foi definida com sucesso:

```swift
if (john.residence?.address = someAddress) != nil {
    print("It was possible to set the address.")
} else {
    print("It was not possible to set the address.")
}
// Prints "It was not possible to set the address."
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> if (john.residence?.address = someAddress) != nil {
        print("It was possible to set the address.")
     } else {
        print("It was not possible to set the address.")
     }
  <- It was not possible to set the address.
  ```
-->

## Acessando subscripts por meio de optional chaining

Você pode usar o optional chaining para tentar ler e definir
um valor por meio de um subscript sobre um valor optional,
e verificar se a chamada ao subscript deu certo.

> Nota: Ao acessar um subscript sobre um valor optional por meio de optional chaining,
> você coloca o ponto de interrogação *antes* dos colchetes do subscript, e não depois.
> O ponto de interrogação do optional chaining sempre vem logo depois
> da parte da expressão que é optional.

O exemplo abaixo tenta obter o nome do primeiro cômodo
do array `rooms` da propriedade `john.residence`,
usando o subscript definido na classe `Residence`.
Como `john.residence` é `nil` no momento,
a chamada ao subscript falha:

```swift
if let firstRoomName = john.residence?[0].name {
    print("The first room name is \(firstRoomName).")
} else {
    print("Unable to retrieve the first room name.")
}
// Prints "Unable to retrieve the first room name."
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> if let firstRoomName = john.residence?[0].name {
        print("The first room name is \(firstRoomName).")
     } else {
        print("Unable to retrieve the first room name.")
     }
  <- Unable to retrieve the first room name.
  ```
-->

O ponto de interrogação do optional chaining nessa chamada de subscript
fica logo depois de `john.residence`, antes dos colchetes do subscript,
porque `john.residence` é o valor optional
sobre o qual o optional chaining está sendo tentado.

Da mesma forma, você pode tentar definir um novo valor por meio de um subscript com optional chaining:

```swift
john.residence?[0] = Room(name: "Bathroom")
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> john.residence?[0] = Room(name: "Bathroom")
  ```
-->

Essa tentativa de definir o subscript também falha, porque `residence` é `nil` no momento.

Se você criar uma instância real de `Residence` e atribuí-la a `john.residence`,
com uma ou mais instâncias de `Room` no array `rooms`,
pode usar o subscript de `Residence` para acessar
os itens reais do array `rooms` por meio de optional chaining:

```swift
let johnsHouse = Residence()
johnsHouse.rooms.append(Room(name: "Living Room"))
johnsHouse.rooms.append(Room(name: "Kitchen"))
john.residence = johnsHouse

if let firstRoomName = john.residence?[0].name {
    print("The first room name is \(firstRoomName).")
} else {
    print("Unable to retrieve the first room name.")
}
// Prints "The first room name is Living Room."
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> let johnsHouse = Residence()
  -> johnsHouse.rooms.append(Room(name: "Living Room"))
  -> johnsHouse.rooms.append(Room(name: "Kitchen"))
  -> john.residence = johnsHouse

  -> if let firstRoomName = john.residence?[0].name {
        print("The first room name is \(firstRoomName).")
     } else {
        print("Unable to retrieve the first room name.")
     }
  <- The first room name is Living Room.
  ```
-->

### Acessando subscripts de tipo optional

Se um subscript retorna um valor de tipo optional ---
como o subscript por chave do tipo `Dictionary` do Swift ---
coloque um ponto de interrogação *depois* do fechamento do colchete do subscript
para encadear na seu valor de retorno optional:

```swift
var testScores = ["Dave": [86, 82, 84], "Bev": [79, 94, 81]]
testScores["Dave"]?[0] = 91
testScores["Bev"]?[0] += 1
testScores["Brian"]?[0] = 72
// the "Dave" array is now [91, 82, 84] and the "Bev" array is now [80, 94, 81]
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> var testScores = ["Dave": [86, 82, 84], "Bev": [79, 94, 81]]
  -> testScores["Dave"]?[0] = 91
  -> testScores["Bev"]?[0] += 1
  -> testScores["Brian"]?[0] = 72
  >> let dave = "Dave"
  >> let bev = "Bev"
  /> the \"Dave\" array is now [\(testScores[dave]![0]), \(testScores[dave]![1]), \(testScores[dave]![2])] and the \"Bev\" array is now [\(testScores[bev]![0]), \(testScores[bev]![1]), \(testScores[bev]![2])]
  </ the "Dave" array is now [91, 82, 84] and the "Bev" array is now [80, 94, 81]
  ```
-->

O exemplo acima define um dicionário chamado `testScores`,
que contém dois pares chave-valor que mapeiam uma chave `String` para um array de valores `Int`.
O exemplo usa o optional chaining para definir o primeiro item do array de `"Dave"` como `91`;
para incrementar em `1` o primeiro item do array de `"Bev"`;
e para tentar definir o primeiro item de um array com a chave `"Brian"`.
As duas primeiras chamadas dão certo, porque o dicionário `testScores`
tem chaves para `"Dave"` e `"Bev"`.
A terceira chamada falha, porque o dicionário `testScores`
não tem uma chave para `"Brian"`.

## Encadeando vários níveis

Você pode encadear vários níveis de optional chaining
para chegar a propriedades, métodos e subscripts mais profundos dentro de um modelo.
No entanto, vários níveis de optional chaining
não acrescentam mais níveis de optionalidade ao valor retornado.

Dito de outra forma:

- Se o tipo que você está tentando obter não é optional,
  ele passa a ser optional por causa do optional chaining.
- Se o tipo que você está tentando obter *já* é optional,
  ele não se torna *mais* optional por causa do encadeamento.

Portanto:

- Se você tentar obter um valor `Int` por meio de optional chaining,
  sempre será retornado um `Int?`,
  não importa quantos níveis de encadeamento sejam usados.
- Da mesma forma, se você tentar obter um valor `Int?` por meio de optional chaining,
  sempre será retornado um `Int?`,
  não importa quantos níveis de encadeamento sejam usados.

O exemplo abaixo tenta acessar a propriedade `street` da propriedade `address`
da propriedade `residence` de `john`.
Há *dois* níveis de optional chaining aqui,
para navegar pelas propriedades `residence` e `address`,
ambas de tipo optional:

```swift
if let johnsStreet = john.residence?.address?.street {
    print("John's street name is \(johnsStreet).")
} else {
    print("Unable to retrieve the address.")
}
// Prints "Unable to retrieve the address."
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> if let johnsStreet = john.residence?.address?.street {
        print("John's street name is \(johnsStreet).")
     } else {
        print("Unable to retrieve the address.")
     }
  <- Unable to retrieve the address.
  ```
-->

O valor de `john.residence` contém, no momento, uma instância válida de `Residence`.
No entanto, o valor de `john.residence.address` é `nil` no momento.
Por isso, a chamada a `john.residence?.address?.street` falha.

Observe que, no exemplo acima,
você está tentando obter o valor da propriedade `street`.
O tipo dessa propriedade é `String?`.
Assim, o valor de retorno de `john.residence?.address?.street` também é `String?`,
mesmo com dois níveis de optional chaining aplicados além
do próprio tipo optional da propriedade.

Se você definir uma instância real de `Address` como valor de `john.residence.address`,
e definir um valor real para a propriedade `street` desse endereço,
poderá acessar o valor da propriedade `street` por meio de optional chaining em vários níveis:

```swift
let johnsAddress = Address()
johnsAddress.buildingName = "The Larches"
johnsAddress.street = "Laurel Street"
john.residence?.address = johnsAddress

if let johnsStreet = john.residence?.address?.street {
    print("John's street name is \(johnsStreet).")
} else {
    print("Unable to retrieve the address.")
}
// Prints "John's street name is Laurel Street."
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> let johnsAddress = Address()
  -> johnsAddress.buildingName = "The Larches"
  -> johnsAddress.street = "Laurel Street"
  -> john.residence?.address = johnsAddress

  -> if let johnsStreet = john.residence?.address?.street {
        print("John's street name is \(johnsStreet).")
     } else {
        print("Unable to retrieve the address.")
     }
  <- John's street name is Laurel Street.
  ```
-->

Neste exemplo,
a tentativa de definir a propriedade `address` de `john.residence` vai dar certo,
porque o valor de `john.residence`
contém agora uma instância válida de `Residence`.

## Encadeando em métodos com valores de retorno optional

O exemplo anterior mostra como obter o valor de
uma propriedade de tipo optional por meio de optional chaining.
Você também pode usar o optional chaining para chamar um método que retorna um valor de tipo optional,
e encadear no valor de retorno desse método, se precisar.

O exemplo abaixo chama o método `buildingIdentifier()` da classe `Address`
por meio de optional chaining. Esse método retorna um valor do tipo `String?`.
Como descrito acima, o tipo final do retorno dessa chamada, depois do optional chaining,
também é `String?`:

```swift
if let buildingIdentifier = john.residence?.address?.buildingIdentifier() {
    print("John's building identifier is \(buildingIdentifier).")
}
// Prints "John's building identifier is The Larches."
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> if let buildingIdentifier = john.residence?.address?.buildingIdentifier() {
        print("John's building identifier is \(buildingIdentifier).")
     }
  <- John's building identifier is The Larches.
  ```
-->

Se você quiser fazer mais optional chaining sobre o valor de retorno desse método,
coloque o ponto de interrogação do optional chaining *depois* dos parênteses do método:

```swift
if let beginsWithThe =
    john.residence?.address?.buildingIdentifier()?.hasPrefix("The") {
    if beginsWithThe {
        print("John's building identifier begins with \"The\".")
    } else {
        print("John's building identifier doesn't begin with \"The\".")
    }
}
// Prints "John's building identifier begins with "The"."
```

<!--
  - test: `optionalChaining`

  ```swifttest
  -> if let beginsWithThe =
        john.residence?.address?.buildingIdentifier()?.hasPrefix("The") {
        if beginsWithThe {
           print("John's building identifier begins with \"The\".")
        } else {
           print("John's building identifier doesn't begin with \"The\".")
        }
     }
  <- John's building identifier begins with "The".
  ```
-->

> Nota: No exemplo acima,
> você coloca o ponto de interrogação do optional chaining *depois* dos parênteses,
> porque o valor optional sobre o qual você está encadeando é
> o valor de retorno do método `buildingIdentifier()`,
> e não o método `buildingIdentifier()` em si.

<!--
  TODO: add an example of chaining on a property of optional function type.
  This can then be tied in to a revised description of how
  the sugar for optional protocol requirements works.
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->

<!-- ia-translate: true -->
