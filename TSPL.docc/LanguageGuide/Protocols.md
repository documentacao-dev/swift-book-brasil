# Protocolos

Defina requisitos que os tipos em conformidade devem implementar.

Um *protocolo* define um modelo de
métodos, propriedades e outros requisitos
adequados a uma tarefa ou funcionalidade específica.
O protocolo pode então ser *adotado* por uma classe, estrutura ou enumeração
para fornecer a implementação real desses requisitos.
Qualquer tipo que satisfaça os requisitos de um protocolo é dito
*em conformidade* com esse protocolo.

Além de especificar os requisitos que os tipos em conformidade devem implementar,
você pode estender um protocolo para implementar alguns desses requisitos
ou para implementar funcionalidades adicionais de que os tipos em conformidade podem tirar proveito.

<!--
  FIXME: Protocols should also be able to support initializers,
  and indeed you can currently write them,
  but they don't work due to
  <rdar://problem/13695680> Constructor requirements in protocols (needed for NSCoding).
  I'll need to write about them once this is fixed.
  UPDATE: actually, they *can* be used right now,
  but only in a generic function, and not more generally with the protocol type.
  I'm not sure I should mention them in this chapter until they work more generally.
-->
## Sintaxe de protocolos

Você define protocolos de um jeito muito parecido com classes, estruturas e enumerações:

```swift
protocol SomeProtocol {
    // protocol definition goes here
}
```

<!--
  - test: `protocolSyntax`

  ```swifttest
  -> protocol SomeProtocol {
        // protocol definition goes here
     }
  ```
-->

Tipos personalizados declaram que adotam um protocolo específico
colocando o nome do protocolo depois do nome do tipo,
separado por dois-pontos, como parte da sua definição.
É possível listar vários protocolos, separados por vírgulas:

```swift
struct SomeStructure: FirstProtocol, AnotherProtocol {
    // structure definition goes here
}
```

<!--
  - test: `protocolSyntax`

  ```swifttest
  >> protocol FirstProtocol {}
  >> protocol AnotherProtocol {}
  -> struct SomeStructure: FirstProtocol, AnotherProtocol {
        // structure definition goes here
     }
  ```
-->

Se uma classe tem uma superclasse, coloque o nome da superclasse
antes de qualquer protocolo que ela adote, seguido de vírgula:

```swift
class SomeClass: SomeSuperclass, FirstProtocol, AnotherProtocol {
    // class definition goes here
}
```

<!--
  - test: `protocolSyntax`

  ```swifttest
  >> class SomeSuperclass {}
  -> class SomeClass: SomeSuperclass, FirstProtocol, AnotherProtocol {
        // class definition goes here
     }
  ```
-->

> Nota: Como protocolos são tipos,
> comece os nomes deles com letra maiúscula
> (como `FullyNamed` e `RandomNumberGenerator`)
> para combinar com os nomes de outros tipos em Swift
> (como `Int`, `String` e `Double`).

## Requisitos de propriedades

Um protocolo pode exigir que qualquer tipo em conformidade forneça
uma propriedade de instância ou uma propriedade de tipo com um nome e um tipo específicos.
O protocolo não especifica se a propriedade deve ser
uma propriedade armazenada ou uma propriedade computada:
ele especifica apenas o nome e o tipo exigidos.
O protocolo também especifica se cada propriedade precisa ser apenas de leitura
ou de leitura *e* escrita.

Se um protocolo exige que uma propriedade seja de leitura e escrita,
esse requisito não pode ser atendido por
uma propriedade armazenada constante nem por uma propriedade computada somente de leitura.
Se o protocolo exige apenas que a propriedade seja de leitura,
o requisito pode ser atendido por qualquer tipo de propriedade,
e é válido que a propriedade também seja de escrita,
caso isso seja útil para o seu próprio código.

Requisitos de propriedade são sempre declarados como propriedades variáveis,
precedidas da palavra-chave `var`.
Propriedades de leitura e escrita são indicadas escrevendo
`{ get set }` depois da declaração do tipo,
e propriedades somente de leitura são indicadas escrevendo `{ get }`.

```swift
protocol SomeProtocol {
    var mustBeSettable: Int { get set }
    var doesNotNeedToBeSettable: Int { get }
}
```

<!--
  - test: `instanceProperties`

  ```swifttest
  -> protocol SomeProtocol {
        var mustBeSettable: Int { get set }
        var doesNotNeedToBeSettable: Int { get }
     }
  ```
-->

Sempre coloque a palavra-chave `static` antes dos requisitos de propriedade de tipo
quando você os define em um protocolo.
Essa regra vale mesmo que os requisitos de propriedade de tipo possam ser precedidos
pela palavra-chave `class` ou `static` quando implementados por uma classe:

```swift
protocol AnotherProtocol {
    static var someTypeProperty: Int { get set }
}
```

<!--
  - test: `instanceProperties`

  ```swifttest
  -> protocol AnotherProtocol {
        static var someTypeProperty: Int { get set }
     }
  ```
-->

Aqui está um exemplo de protocolo com um único requisito de propriedade de instância:

```swift
protocol FullyNamed {
    var fullName: String { get }
}
```

<!--
  - test: `instanceProperties`

  ```swifttest
  -> protocol FullyNamed {
        var fullName: String { get }
     }
  ```
-->

O protocolo `FullyNamed` exige que um tipo em conformidade forneça um nome completo.
O protocolo não especifica mais nada sobre a natureza do tipo em conformidade:
ele apenas especifica que o tipo deve ser capaz de fornecer um nome completo para si mesmo.
O protocolo estabelece que qualquer tipo `FullyNamed` deve ter
uma propriedade de instância somente de leitura chamada `fullName`, do tipo `String`.

Aqui está um exemplo de uma estrutura simples que adota e está em conformidade com
o protocolo `FullyNamed`:

```swift
struct Person: FullyNamed {
    var fullName: String
}
let john = Person(fullName: "John Appleseed")
// john.fullName is "John Appleseed"
```

<!--
  - test: `instanceProperties`

  ```swifttest
  -> struct Person: FullyNamed {
        var fullName: String
     }
  -> let john = Person(fullName: "John Appleseed")
  /> john.fullName is \"\(john.fullName)\"
  </ john.fullName is "John Appleseed"
  ```
-->

Este exemplo define uma estrutura chamada `Person`,
que representa uma pessoa específica com nome.
Ela declara que adota o protocolo `FullyNamed`
na primeira linha da sua definição.

Cada instância de `Person` tem uma única propriedade armazenada chamada `fullName`,
do tipo `String`.
Isso corresponde ao único requisito do protocolo `FullyNamed`,
e significa que `Person` está em conformidade com o protocolo corretamente.
(O Swift informa um erro em tempo de compilação se um requisito do protocolo não for atendido.)

Aqui está uma classe mais complexa, que também adota e está em conformidade com o protocolo `FullyNamed`:

```swift
class Starship: FullyNamed {
    var prefix: String?
    var name: String
    init(name: String, prefix: String? = nil) {
        self.name = name
        self.prefix = prefix
    }
    var fullName: String {
        return (prefix != nil ? prefix! + " " : "") + name
    }
}
var ncc1701 = Starship(name: "Enterprise", prefix: "USS")
// ncc1701.fullName is "USS Enterprise"
```

<!--
  - test: `instanceProperties`

  ```swifttest
  -> class Starship: FullyNamed {
        var prefix: String?
        var name: String
        init(name: String, prefix: String? = nil) {
           self.name = name
           self.prefix = prefix
        }
        var fullName: String {
           return (prefix != nil ? prefix! + " " : "") + name
        }
     }
  -> var ncc1701 = Starship(name: "Enterprise", prefix: "USS")
  /> ncc1701.fullName is \"\(ncc1701.fullName)\"
  </ ncc1701.fullName is "USS Enterprise"
  ```
-->

Esta classe implementa o requisito de propriedade `fullName` como
uma propriedade computada somente de leitura para uma nave estelar.
Cada instância da classe `Starship` armazena um `name` obrigatório e um `prefix` opcional.
A propriedade `fullName` usa o valor de `prefix`, se ele existir,
e o coloca no início de `name` para criar um nome completo para a nave.

<!--
  TODO: add some advice on how protocols should be named
-->

## Requisitos de métodos

Protocolos podem exigir que tipos em conformidade implementem métodos de instância
e métodos de tipo específicos.
Esses métodos são escritos como parte da definição do protocolo
exatamente do mesmo jeito que os métodos de instância e de tipo comuns,
mas sem chaves nem corpo de método.
Parâmetros variádicos são permitidos, seguindo as mesmas regras dos métodos comuns.
Valores padrão, porém, não podem ser especificados para os parâmetros de método dentro da definição de um protocolo.

Assim como nos requisitos de propriedade de tipo,
você sempre coloca a palavra-chave `static` antes dos requisitos de método de tipo
quando eles são definidos em um protocolo.
Isso vale mesmo que os requisitos de método de tipo possam ser precedidos
pela palavra-chave `class` ou `static` quando implementados por uma classe:

```swift
protocol SomeProtocol {
    static func someTypeMethod()
}
```

<!--
  - test: `typeMethods`

  ```swifttest
  -> protocol SomeProtocol {
        static func someTypeMethod()
     }
  ```
-->

O exemplo a seguir define um protocolo com um único requisito de método de instância:

```swift
protocol RandomNumberGenerator {
    func random() -> Double
}
```

<!--
  - test: `protocols`

  ```swifttest
  -> protocol RandomNumberGenerator {
        func random() -> Double
     }
  ```
-->

Este protocolo, `RandomNumberGenerator`, exige que qualquer tipo em conformidade
tenha um método de instância chamado `random`,
que retorna um valor `Double` sempre que é chamado.
Embora isso não seja especificado como parte do protocolo,
presume-se que esse valor será
um número de `0.0` até (sem incluir) `1.0`.

O protocolo `RandomNumberGenerator` não faz nenhuma suposição
sobre como cada número aleatório será gerado:
ele apenas exige que o gerador forneça uma forma padrão
de gerar um novo número aleatório.

Aqui está a implementação de uma classe que adota e está em conformidade com
o protocolo `RandomNumberGenerator`.
Essa classe implementa um algoritmo de gerador de números pseudoaleatórios conhecido como
um *gerador linear congruente*:

```swift
class LinearCongruentialGenerator: RandomNumberGenerator {
    var lastRandom = 42.0
    let m = 139968.0
    let a = 3877.0
    let c = 29573.0
    func random() -> Double {
        lastRandom = ((lastRandom * a + c)
            .truncatingRemainder(dividingBy:m))
        return lastRandom / m
    }
}
let generator = LinearCongruentialGenerator()
print("Here's a random number: \(generator.random())")
// Prints "Here's a random number: 0.3746499199817101".
print("And another one: \(generator.random())")
// Prints "And another one: 0.729023776863283".
```

<!--
  - test: `protocols`

  ```swifttest
  -> class LinearCongruentialGenerator: RandomNumberGenerator {
        var lastRandom = 42.0
        let m = 139968.0
        let a = 3877.0
        let c = 29573.0
        func random() -> Double {
           lastRandom = ((lastRandom * a + c)
               .truncatingRemainder(dividingBy:m))
           return lastRandom / m
        }
     }
  -> let generator = LinearCongruentialGenerator()
  -> print("Here's a random number: \(generator.random())")
  <- Here's a random number: 0.3746499199817101
  -> print("And another one: \(generator.random())")
  <- And another one: 0.729023776863283
  ```
-->

## Requisitos de métodos mutantes

Às vezes é necessário que um método modifique (ou *mute*) a instância à qual ele pertence.
Para métodos de instância em tipos por valor (ou seja, estruturas e enumerações),
você coloca a palavra-chave `mutating` antes da palavra-chave `func` do método
para indicar que o método pode modificar a instância à qual pertence
e quaisquer propriedades dessa instância.
Esse processo é descrito em <doc:Methods#Modifying-Value-Types-from-Within-Instance-Methods>.

Se você define um requisito de método de instância em um protocolo
que deve modificar instâncias de qualquer tipo que adote o protocolo,
marque o método com a palavra-chave `mutating`
como parte da definição do protocolo.
Isso permite que estruturas e enumerações adotem o protocolo
e satisfaçam esse requisito de método.

> Nota: Se você marca um requisito de método de instância do protocolo como `mutating`,
> não precisa escrever a palavra-chave `mutating` ao escrever
> a implementação desse método em uma classe.
> A palavra-chave `mutating` é usada apenas por estruturas e enumerações.

O exemplo a seguir define um protocolo chamado `Togglable`,
que define um único requisito de método de instância chamado `toggle`.
Como o nome sugere, o método `toggle()` serve para
alternar ou inverter o estado de qualquer tipo em conformidade,
normalmente modificando uma propriedade desse tipo.

O método `toggle()` é marcado com a palavra-chave `mutating`
como parte da definição do protocolo `Togglable`,
para indicar que se espera que o método altere o estado de uma instância em conformidade
quando for chamado:

```swift
protocol Togglable {
    mutating func toggle()
}
```

<!--
  - test: `mutatingRequirements`

  ```swifttest
  -> protocol Togglable {
        mutating func toggle()
     }
  ```
-->

Se você implementar o protocolo `Togglable` para uma estrutura ou enumeração,
essa estrutura ou enumeração pode estar em conformidade com o protocolo
fornecendo uma implementação do método `toggle()`
que também seja marcada como `mutating`.

O exemplo a seguir define uma enumeração chamada `OnOffSwitch`.
Essa enumeração alterna entre dois estados,
indicados pelos casos de enumeração `on` e `off`.
A implementação de `toggle` da enumeração é marcada como `mutating`,
para corresponder aos requisitos do protocolo `Togglable`:

```swift
enum OnOffSwitch: Togglable {
    case off, on
    mutating func toggle() {
        switch self {
        case .off:
            self = .on
        case .on:
            self = .off
        }
    }
}
var lightSwitch = OnOffSwitch.off
lightSwitch.toggle()
// lightSwitch is now equal to .on
```

<!--
  - test: `mutatingRequirements`

  ```swifttest
  -> enum OnOffSwitch: Togglable {
        case off, on
        mutating func toggle() {
           switch self {
              case .off:
                 self = .on
              case .on:
                 self = .off
           }
        }
     }
  -> var lightSwitch = OnOffSwitch.off
  -> lightSwitch.toggle()
  // lightSwitch is now equal to .on
  ```
-->

## Requisitos de inicializadores

Protocolos podem exigir que tipos em conformidade implementem inicializadores específicos.
Você escreve esses inicializadores como parte da definição do protocolo
exatamente do mesmo jeito que os inicializadores comuns,
mas sem chaves nem corpo de inicializador:

```swift
protocol SomeProtocol {
    init(someParameter: Int)
}
```

<!--
  - test: `initializers`

  ```swifttest
  -> protocol SomeProtocol {
        init(someParameter: Int)
     }
  ```
-->

### Implementações em classes dos requisitos de inicializador de protocolo

Você pode implementar um requisito de inicializador de protocolo em uma classe em conformidade
como um inicializador designado ou como um inicializador de conveniência.
Nos dois casos,
você deve marcar a implementação do inicializador com o modificador `required`:

```swift
class SomeClass: SomeProtocol {
    required init(someParameter: Int) {
        // initializer implementation goes here
    }
}
```

<!--
  - test: `initializers`

  ```swifttest
  -> class SomeClass: SomeProtocol {
        required init(someParameter: Int) {
           // initializer implementation goes here
        }
     }
  ```
-->

<!--
  - test: `protocolInitializerRequirementsCanBeImplementedAsDesignatedOrConvenience`

  ```swifttest
  -> protocol P {
        init(x: Int)
     }
  -> class C1: P {
        required init(x: Int) {}
     }
  -> class C2: P {
        init() {}
        required convenience init(x: Int) {
           self.init()
        }
     }
  ```
-->

O uso do modificador `required` garante que
você forneça uma implementação explícita ou herdada do requisito de inicializador
em todas as subclasses da classe em conformidade,
de modo que elas também estejam em conformidade com o protocolo.

Para mais informações sobre inicializadores obrigatórios,
veja <doc:Initialization#Required-Initializers>.

<!--
  - test: `protocolInitializerRequirementsRequireTheRequiredModifierOnTheImplementingClass`

  ```swifttest
  -> protocol P {
        init(s: String)
     }
  -> class C1: P {
        required init(s: String) {}
     }
  -> class C2: P {
        init(s: String) {}
     }
  !$ error: initializer requirement 'init(s:)' can only be satisfied by a 'required' initializer in non-final class 'C2'
  !! init(s: String) {}
  !! ^
  !! required
  ```
-->

<!--
  - test: `protocolInitializerRequirementsRequireTheRequiredModifierOnSubclasses`

  ```swifttest
  -> protocol P {
        init(s: String)
     }
  -> class C: P {
        required init(s: String) {}
     }
  -> class D1: C {
        required init(s: String) { super.init(s: s) }
     }
  -> class D2: C {
        init(s: String) { super.init(s: s) }
     }
  !$ error: 'required' modifier must be present on all overrides of a required initializer
  !! init(s: String) { super.init(s: s) }
  !! ^
  !! required
  !$ note: overridden required initializer is here
  !! required init(s: String) {}
  !! ^
  ```
-->

> Nota: Você não precisa marcar as implementações de inicializadores de protocolo com o modificador `required`
> em classes marcadas com o modificador `final`,
> porque classes `final` não podem ser subclassificadas.
> Para saber mais sobre o modificador `final`, veja <doc:Inheritance#Preventing-Overrides>.

<!--
  - test: `finalClassesDoNotNeedTheRequiredModifierForProtocolInitializerRequirements`

  ```swifttest
  -> protocol P {
        init(s: String)
     }
  -> final class C1: P {
        required init(s: String) {}
     }
  -> final class C2: P {
        init(s: String) {}
     }
  ```
-->

Se uma subclasse sobrescreve um inicializador designado de uma superclasse
e também implementa um inicializador correspondente de um requisito de protocolo,
marque a implementação do inicializador com os dois modificadores `required` e `override`:

```swift
protocol SomeProtocol {
    init()
}

class SomeSuperClass {
    init() {
        // initializer implementation goes here
    }
}

class SomeSubClass: SomeSuperClass, SomeProtocol {
    // "required" from SomeProtocol conformance; "override" from SomeSuperClass
    required override init() {
        // initializer implementation goes here
    }
}
```

<!--
  - test: `requiredOverrideInitializers`

  ```swifttest
  -> protocol SomeProtocol {
        init()
     }

  -> class SomeSuperClass {
        init() {
           // initializer implementation goes here
        }
     }

  -> class SomeSubClass: SomeSuperClass, SomeProtocol {
        // "required" from SomeProtocol conformance; "override" from SomeSuperClass
        required override init() {
           // initializer implementation goes here
        }
     }
  ```
-->

### Requisitos de inicializadores falhíveis

Protocolos podem definir requisitos de inicializadores falhíveis para tipos em conformidade,
como definido em <doc:Initialization#Failable-Initializers>.

Um requisito de inicializador falhível pode ser atendido por
um inicializador falhível ou não falhível em um tipo em conformidade.
Um requisito de inicializador não falhível pode ser atendido por
um inicializador não falhível ou por um inicializador falhível de desembrulhamento implícito.

<!--
  - test: `failableRequirementCanBeSatisfiedByFailableInitializer`

  ```swifttest
  -> protocol P { init?(i: Int) }
  -> class C: P { required init?(i: Int) {} }
  -> struct S: P { init?(i: Int) {} }
  ```
-->

<!--
  - test: `failableRequirementCanBeSatisfiedByIUOInitializer`

  ```swifttest
  -> protocol P { init?(i: Int) }
  -> class C: P { required init!(i: Int) {} }
  -> struct S: P { init!(i: Int) {} }
  ```
-->

<!--
  - test: `iuoRequirementCanBeSatisfiedByFailableInitializer`

  ```swifttest
  -> protocol P { init!(i: Int) }
  -> class C: P { required init?(i: Int) {} }
  -> struct S: P { init?(i: Int) {} }
  ```
-->

<!--
  - test: `iuoRequirementCanBeSatisfiedByIUOInitializer`

  ```swifttest
  -> protocol P { init!(i: Int) }
  -> class C: P { required init!(i: Int) {} }
  -> struct S: P { init!(i: Int) {} }
  ```
-->

<!--
  - test: `failableRequirementCanBeSatisfiedByNonFailableInitializer`

  ```swifttest
  -> protocol P { init?(i: Int) }
  -> class C: P { required init(i: Int) {} }
  -> struct S: P { init(i: Int) {} }
  ```
-->

<!--
  - test: `iuoRequirementCanBeSatisfiedByNonFailableInitializer`

  ```swifttest
  -> protocol P { init!(i: Int) }
  -> class C: P { required init(i: Int) {} }
  -> struct S: P { init(i: Int) {} }
  ```
-->

<!--
  - test: `nonFailableRequirementCanBeSatisfiedByNonFailableInitializer`

  ```swifttest
  -> protocol P { init(i: Int) }
  -> class C: P { required init(i: Int) {} }
  -> struct S: P { init(i: Int) {} }
  ```
-->

<!--
  - test: `nonFailableRequirementCanBeSatisfiedByIUOInitializer`

  ```swifttest
  -> protocol P { init(i: Int) }
  -> class C: P { required init!(i: Int) {} }
  -> struct S: P { init!(i: Int) {} }
  ```
-->

## Protocolos que têm apenas requisitos semânticos

Todos os exemplos de protocolo acima exigem alguns métodos ou propriedades,
mas a declaração de um protocolo não precisa incluir nenhum requisito.
Você também pode usar um protocolo para descrever requisitos *semânticos*,
ou seja, requisitos sobre como os valores desses tipos se comportam
e sobre as operações que eles suportam.
<!--
Avoiding the term "marker protocol",
which more specifically refers to @_marker on a protocol.
-->
A biblioteca padrão do Swift define vários protocolos
que não têm nenhum método ou propriedade obrigatória:

- [`Sendable`][] para valores que podem ser compartilhados entre domínios de concorrência,
  como discutido em <doc:Concurrency#Sendable-Types>.
- [`Copyable`][] para valores que o Swift pode copiar
  quando você os passa para uma função,
  como discutido em <doc:Declarations#Borrowing-and-Consuming-Parameters>.
- [`BitwiseCopyable`][] para valores que podem ser copiados bit a bit.

[`BitwiseCopyable`]: https://developer.apple.com/documentation/swift/bitwisecopyable
[`Copyable`]: https://developer.apple.com/documentation/swift/copyable
[`Sendable`]: https://developer.apple.com/documentation/swift/sendable

<!--
These link definitions are also used in the section below,
Implicit Conformance to a Protocol.
-->

Para informações sobre os requisitos desses protocolos,
veja a visão geral na documentação deles.

Você usa a mesma sintaxe para adotar esses protocolos
que usa para adotar outros protocolos.
A única diferença é que você não inclui
declarações de métodos ou propriedades que implementem os requisitos do protocolo.
Por exemplo:

```swift
struct MyStruct: Copyable {
    var counter = 12
}

extension MyStruct: BitwiseCopyable { }
```

O código acima define uma nova estrutura.
Como `Copyable` tem apenas requisitos semânticos,
não há nenhum código na declaração da estrutura para adotar o protocolo.
Da mesma forma, como `BitwiseCopyable` tem apenas requisitos semânticos,
a extensão que adota esse protocolo tem um corpo vazio.

Normalmente você não precisa escrever a conformidade com esses protocolos:
em vez disso, o Swift adiciona a conformidade automaticamente para você,
como descrito em <doc:Protocols#Implicit-Conformance-to-a-Protocol>.

<!-- TODO: Mention why you might define your own empty protocols. -->

## Protocolos como tipos

Protocolos não implementam nenhuma funcionalidade por conta própria.
Mesmo assim, você pode usar um protocolo como tipo no seu código.

A forma mais comum de usar um protocolo como tipo
é usá-lo como restrição genérica.
Código com restrições genéricas pode trabalhar com
qualquer tipo que esteja em conformidade com o protocolo,
e o tipo específico é escolhido pelo código que usa a API.
Por exemplo,
quando você chama uma função que recebe um argumento
cujo tipo é genérico, quem chama é que escolhe o tipo.

Código com um tipo opaco
trabalha com algum tipo que está em conformidade com o protocolo.
O tipo subjacente é conhecido em tempo de compilação,
e a implementação da API escolhe esse tipo,
mas a identidade desse tipo fica oculta de quem usa a API.
Usar um tipo opaco permite impedir que detalhes de implementação de uma API
vazem através da camada de abstração,
por exemplo, ocultando o tipo de retorno específico de uma função
e garantindo apenas que o valor está em conformidade com um determinado protocolo.

Código com um tipo de protocolo encaixotado
trabalha com qualquer tipo, escolhido em tempo de execução, que esteja em conformidade com o protocolo.
Para oferecer essa flexibilidade em tempo de execução,
o Swift adiciona um nível de indireção quando necessário,
conhecido como *caixa* (box),
o que tem um custo de desempenho.
Por causa dessa flexibilidade,
o Swift não conhece o tipo subjacente em tempo de compilação,
o que significa que você só pode acessar os membros
exigidos pelo protocolo.
Acessar quaisquer outras APIs do tipo subjacente
exige uma conversão em tempo de execução.

Para informações sobre o uso de protocolos como restrições genéricas,
veja <doc:Generics>.
Para informações sobre tipos opacos e tipos de protocolo encaixotados,
veja <doc:OpaqueTypes>.

<!--
Performance impact from SE-0335:

Existential types are also significantly more expensive than using concrete types.
Because they can store any value whose type conforms to the protocol,
and the type of value stored can change dynamically,
existential types require dynamic memory
unless the value is small enough to fit within an inline 3-word buffer.
In addition to heap allocation and reference counting,
code using existential types incurs pointer indirection and dynamic method dispatch
that cannot be optimized away.
-->

## Delegação

*Delegação* é um padrão de design que permite
que uma classe ou estrutura transfira (ou *delegue*)
algumas das suas responsabilidades para uma instância de outro tipo.
Esse padrão é implementado definindo
um protocolo que encapsula as responsabilidades delegadas,
de modo que um tipo em conformidade (conhecido como delegado)
tenha a garantia de fornecer a funcionalidade que foi delegada.
A delegação pode ser usada para reagir a uma ação específica,
ou para obter dados de uma fonte externa sem precisar conhecer
o tipo subjacente dessa fonte.

O exemplo a seguir define um jogo de dados
e um protocolo aninhado para um delegado
que acompanha o andamento do jogo:

```swift
class DiceGame {
    let sides: Int
    let generator = LinearCongruentialGenerator()
    weak var delegate: Delegate?

    init(sides: Int) {
        self.sides = sides
    }

    func roll() -> Int {
        return Int(generator.random() * Double(sides)) + 1
    }

    func play(rounds: Int) {
        delegate?.gameDidStart(self)
        for round in 1...rounds {
            let player1 = roll()
            let player2 = roll()
            if player1 == player2 {
                delegate?.game(self, didEndRound: round, winner: nil)
            } else if player1 > player2 {
                delegate?.game(self, didEndRound: round, winner: 1)
            } else {
                delegate?.game(self, didEndRound: round, winner: 2)
            }
        }
        delegate?.gameDidEnd(self)
    }

    protocol Delegate: AnyObject {
        func gameDidStart(_ game: DiceGame)
        func game(_ game: DiceGame, didEndRound round: Int, winner: Int?)
        func gameDidEnd(_ game: DiceGame)
    }
}
```

A classe `DiceGame` implementa um jogo em que
cada jogador tem a vez de rolar os dados,
e o jogador que tirar o maior número vence a rodada.
Ela usa um gerador linear congruente
do exemplo anterior no capítulo
para gerar os números aleatórios das jogadas de dados.

O protocolo `DiceGame.Delegate` pode ser adotado
para acompanhar o andamento de um jogo de dados.
Como o protocolo `DiceGame.Delegate`
é sempre usado no contexto de um jogo de dados,
ele fica aninhado dentro da classe `DiceGame`.
Protocolos podem ser aninhados
dentro de declarações de tipo como estruturas e classes,
desde que a declaração externa não seja genérica.
Para informações sobre tipos aninhados, veja <doc:NestedTypes>.

Para evitar ciclos de referência forte,
os delegados são declarados como referências fracas.
Para informações sobre referências fracas,
veja <doc:AutomaticReferenceCounting#Strong-Reference-Cycles-Between-Class-Instances>.
Marcar o protocolo como exclusivo de classes
permite que a classe `DiceGame`
declare que o delegado dela deve usar uma referência fraca.
Um protocolo exclusivo de classes
é marcado pela herança de `AnyObject`,
como discutido em <doc:Protocols#Class-Only-Protocols>.

`DiceGame.Delegate` oferece três métodos para acompanhar o andamento de um jogo.
Esses três métodos são incorporados à lógica do jogo
no método `play(rounds:)` acima.
A classe `DiceGame` chama os métodos do delegado quando
um novo jogo começa, uma nova rodada começa ou o jogo termina.

Como a propriedade `delegate` é um `DiceGame.Delegate` *opcional*,
o método `play(rounds:)` usa encadeamento opcional toda vez que chama um método do delegado,
como discutido em <doc:OptionalChaining>.
Se a propriedade `delegate` for nil,
essas chamadas ao delegado são ignoradas.
Se a propriedade `delegate` não for nil,
os métodos do delegado são chamados
e recebem a instância de `DiceGame` como parâmetro.

O próximo exemplo mostra uma classe chamada `DiceGameTracker`,
que adota o protocolo `DiceGame.Delegate`:

```swift
class DiceGameTracker: DiceGame.Delegate {
    var playerScore1 = 0
    var playerScore2 = 0
    func gameDidStart(_ game: DiceGame) {
        print("Started a new game")
        playerScore1 = 0
        playerScore2 = 0
    }
    func game(_ game: DiceGame, didEndRound round: Int, winner: Int?) {
        switch winner {
            case 1:
                playerScore1 += 1
                print("Player 1 won round \(round)")
            case 2: playerScore2 += 1
                print("Player 2 won round \(round)")
            default:
                print("The round was a draw")
        }
    }
    func gameDidEnd(_ game: DiceGame) {
        if playerScore1 == playerScore2 {
            print("The game ended in a draw.")
        } else if playerScore1 > playerScore2 {
            print("Player 1 won!")
        } else {
            print("Player 2 won!")
        }
    }
}
```

A classe `DiceGameTracker` implementa os três métodos
exigidos pelo protocolo `DiceGame.Delegate`.
Ela usa esses métodos para zerar a pontuação dos dois jogadores
no início de um novo jogo,
para atualizar as pontuações no fim de cada rodada
e para anunciar o vencedor no fim do jogo.

Veja como `DiceGame` e `DiceGameTracker` funcionam na prática:

```swift
let tracker = DiceGameTracker()
let game = DiceGame(sides: 6)
game.delegate = tracker
game.play(rounds: 3)
// Started a new game
// Player 2 won round 1
// Player 2 won round 2
// Player 1 won round 3
// Player 2 won!
```

## Adicionando conformidade a um protocolo com uma extensão

Você pode estender um tipo existente para adotar e estar em conformidade com um novo protocolo,
mesmo que não tenha acesso ao código-fonte do tipo existente.
Extensões podem adicionar novas propriedades, métodos e subscritos a um tipo existente,
e por isso conseguem acrescentar qualquer requisito que um protocolo possa exigir.
Para mais informações sobre extensões, veja <doc:Extensions>.

> Nota: Instâncias existentes de um tipo adotam e passam a estar em conformidade com um protocolo automaticamente
> quando essa conformidade é adicionada ao tipo da instância em uma extensão.

Por exemplo, este protocolo, chamado `TextRepresentable`, pode ser implementado por
qualquer tipo que tenha uma forma de ser representado como texto.
Isso pode ser uma descrição de si mesmo ou uma versão textual do seu estado atual:

```swift
protocol TextRepresentable {
    var textualDescription: String { get }
}
```

<!--
  - test: `protocols`

  ```swifttest
  -> protocol TextRepresentable {
        var textualDescription: String { get }
     }
  ```
-->

A classe `Dice` apresentada acima pode ser estendida para adotar e estar em conformidade com `TextRepresentable`:

<!--
  No "from above" xref because
  even though Dice isn't defined in the section immediately previous
  it's part of a running example and Dice is used in that section.
-->

```swift
extension Dice: TextRepresentable {
    var textualDescription: String {
        return "A \(sides)-sided dice"
    }
}
```

<!--
  - test: `protocols`

  ```swifttest
  -> extension Dice: TextRepresentable {
        var textualDescription: String {
           return "A \(sides)-sided dice"
        }
     }
  ```
-->

Essa extensão adota o novo protocolo exatamente da mesma forma
como se `Dice` tivesse fornecido essa conformidade na implementação original.
O nome do protocolo é informado depois do nome do tipo, separado por dois-pontos,
e uma implementação de todos os requisitos do protocolo
é fornecida dentro das chaves da extensão.

Qualquer instância de `Dice` agora pode ser tratada como `TextRepresentable`:

```swift
let d12 = Dice(sides: 12, generator: LinearCongruentialGenerator())
print(d12.textualDescription)
// Prints "A 12-sided dice".
```

<!--
  - test: `protocols`

  ```swifttest
  -> let d12 = Dice(sides: 12, generator: LinearCongruentialGenerator())
  -> print(d12.textualDescription)
  <- A 12-sided dice
  ```
-->

Do mesmo modo, a classe de jogo `SnakesAndLadders` pode ser estendida para
adotar e estar em conformidade com o protocolo `TextRepresentable`:

```swift
extension SnakesAndLadders: TextRepresentable {
    var textualDescription: String {
        return "A game of Snakes and Ladders with \(finalSquare) squares"
    }
}
print(game.textualDescription)
// Prints "A game of Snakes and Ladders with 25 squares".
```

<!--
  - test: `protocols`

  ```swifttest
  -> extension SnakesAndLadders: TextRepresentable {
        var textualDescription: String {
           return "A game of Snakes and Ladders with \(finalSquare) squares"
        }
     }
  -> print(game.textualDescription)
  <- A game of Snakes and Ladders with 25 squares
  ```
-->

### Conformidade condicional a um protocolo

Um tipo genérico pode satisfazer os requisitos de um protocolo
somente sob certas condições,
como quando o parâmetro genérico do tipo está em conformidade com o protocolo.
Você pode fazer um tipo genérico estar em conformidade condicionalmente com um protocolo
listando restrições ao estender o tipo.
Escreva essas restrições depois do nome do protocolo que você está adotando,
usando uma cláusula genérica `where`.
Para mais informações sobre cláusulas genéricas `where`, veja <doc:Generics#Generic-Where-Clauses>.

A extensão a seguir
faz instâncias de `Array` estarem em conformidade com o protocolo `TextRepresentable`
sempre que elas armazenam elementos de um tipo que está em conformidade com `TextRepresentable`.

```swift
extension Array: TextRepresentable where Element: TextRepresentable {
    var textualDescription: String {
        let itemsAsText = self.map { $0.textualDescription }
        return "[" + itemsAsText.joined(separator: ", ") + "]"
    }
}
let myDice = [d6, d12]
print(myDice.textualDescription)
// Prints "[A 6-sided dice, A 12-sided dice]".
```

<!--
  - test: `protocols`

  ```swifttest
  -> extension Array: TextRepresentable where Element: TextRepresentable {
        var textualDescription: String {
           let itemsAsText = self.map { $0.textualDescription }
           return "[" + itemsAsText.joined(separator: ", ") + "]"
        }
     }
     let myDice = [d6, d12]
  -> print(myDice.textualDescription)
  <- [A 6-sided dice, A 12-sided dice]
  ```
-->

### Declarando a adoção de um protocolo com uma extensão

Se um tipo já está em conformidade com todos os requisitos de um protocolo,
mas ainda não declarou que adota esse protocolo,
você pode fazê-lo adotar o protocolo com uma extensão vazia:

```swift
struct Hamster {
    var name: String
    var textualDescription: String {
        return "A hamster named \(name)"
    }
}
extension Hamster: TextRepresentable {}
```

<!--
  - test: `protocols`

  ```swifttest
  -> struct Hamster {
        var name: String
        var textualDescription: String {
           return "A hamster named \(name)"
        }
     }
  -> extension Hamster: TextRepresentable {}
  ```
-->

Instâncias de `Hamster` agora podem ser usadas em qualquer lugar em que `TextRepresentable` seja o tipo exigido:

```swift
let simonTheHamster = Hamster(name: "Simon")
let somethingTextRepresentable: TextRepresentable = simonTheHamster
print(somethingTextRepresentable.textualDescription)
// Prints "A hamster named Simon".
```

<!--
  - test: `protocols`

  ```swifttest
  -> let simonTheHamster = Hamster(name: "Simon")
  -> let somethingTextRepresentable: TextRepresentable = simonTheHamster
  -> print(somethingTextRepresentable.textualDescription)
  <- A hamster named Simon
  ```
-->

> Nota: Tipos não adotam um protocolo automaticamente só por atender aos seus requisitos.
> Eles sempre devem declarar explicitamente a adoção do protocolo.

## Adotando um protocolo usando uma implementação sintetizada

O Swift pode fornecer automaticamente a conformidade com protocolos
`Equatable`, `Hashable` e `Comparable`
em vários casos simples.
Usar essa implementação sintetizada
significa que você não precisa escrever código repetitivo
para implementar você mesmo os requisitos do protocolo.

<!--
  Linking directly to a section of an article like the URLs below do
  is expected to be stable --
  as long as the section stays around, that topic ID will be there too.

  Conforming to the Equatable Protocol
  https://developer.apple.com/documentation/swift/equatable#Conforming-to-the-Equatable-Protocol

  Conforming to the Hashable Protocol
  https://developer.apple.com/documentation/swift/hashable#Conforming-to-the-Hashable-Protocol

  Conforming to the Comparable Protocol
  https://developer.apple.com/documentation/swift/comparable#Conforming-to-the-Comparable-Protocol

  ^-- Need to add discussion of synthesized implementation
  to the reference for Comparable, since that's new

  Some of the information in the type references above
  is also repeated in the "Conform Automatically to Equatable and Hashable" section
  of the article "Adopting Common Protocols".
  https://developer.apple.com/documentation/swift/adopting-common-protocols#Conform-Automatically-to-Equatable-and-Hashable
-->

O Swift fornece uma implementação sintetizada de `Equatable`
para os seguintes tipos personalizados:

- Estruturas que têm apenas propriedades armazenadas que estão em conformidade com o protocolo `Equatable`
- Enumerações que têm apenas valores associados que estão em conformidade com o protocolo `Equatable`
- Enumerações que não têm valores associados

Para receber uma implementação sintetizada de `==`,
declare a conformidade com `Equatable`
no arquivo que contém a declaração original,
sem implementar você mesmo um operador `==`.
O protocolo `Equatable` fornece uma implementação padrão de `!=`.

O exemplo a seguir define uma estrutura `Vector3D`
para um vetor de posição tridimensional `(x, y, z)`,
parecida com a estrutura `Vector2D`.
Como as propriedades `x`, `y` e `z` são todas de um tipo `Equatable`,
`Vector3D` recebe implementações sintetizadas
dos operadores de equivalência.

```swift
struct Vector3D: Equatable {
    var x = 0.0, y = 0.0, z = 0.0
}

let twoThreeFour = Vector3D(x: 2.0, y: 3.0, z: 4.0)
let anotherTwoThreeFour = Vector3D(x: 2.0, y: 3.0, z: 4.0)
if twoThreeFour == anotherTwoThreeFour {
    print("These two vectors are also equivalent.")
}
// Prints "These two vectors are also equivalent."
```

<!--
  - test: `equatable_synthesis`

  ```swifttest
  -> struct Vector3D: Equatable {
        var x = 0.0, y = 0.0, z = 0.0
     }

  -> let twoThreeFour = Vector3D(x: 2.0, y: 3.0, z: 4.0)
  -> let anotherTwoThreeFour = Vector3D(x: 2.0, y: 3.0, z: 4.0)
  -> if twoThreeFour == anotherTwoThreeFour {
         print("These two vectors are also equivalent.")
     }
  <- These two vectors are also equivalent.
  ```
-->

<!--
  Need to cross reference here from "Adopting Common Protocols"
  https://developer.apple.com/documentation/swift/adopting_common_protocols

  Discussion in the article calls out that
  enums without associated values are Equatable & Hashable
  even if you don't declare the protocol conformance.
-->

O Swift fornece uma implementação sintetizada de `Hashable`
para os seguintes tipos personalizados:

- Estruturas que têm apenas propriedades armazenadas que estão em conformidade com o protocolo `Hashable`
- Enumerações que têm apenas valores associados que estão em conformidade com o protocolo `Hashable`
- Enumerações que não têm valores associados

Para receber uma implementação sintetizada de `hash(into:)`,
declare a conformidade com `Hashable`
no arquivo que contém a declaração original,
sem implementar você mesmo um método `hash(into:)`.

O Swift fornece uma implementação sintetizada de `Comparable`
para enumerações que não têm valor bruto (raw value).
Se a enumeração tiver valores associados,
todos eles devem estar em conformidade com o protocolo `Comparable`.
Para receber uma implementação sintetizada de `<`,
declare a conformidade com `Comparable`
no arquivo que contém a declaração original da enumeração,
sem implementar você mesmo um operador `<`.
A implementação padrão do protocolo `Comparable`
de `<=`, `>` e `>=` fornece os demais operadores de comparação.

O exemplo a seguir define uma enumeração `SkillLevel`
com casos para iniciantes, intermediários e especialistas.
Os especialistas são classificados adicionalmente pelo número de estrelas que têm.

```swift
enum SkillLevel: Comparable {
    case beginner
    case intermediate
    case expert(stars: Int)
}
var levels = [SkillLevel.intermediate, SkillLevel.beginner,
              SkillLevel.expert(stars: 5), SkillLevel.expert(stars: 3)]
for level in levels.sorted() {
    print(level)
}
// Prints "beginner".
// Prints "intermediate".
// Prints "expert(stars: 3)".
// Prints "expert(stars: 5)".
```

<!--
  - test: `comparable-enum-synthesis`

  ```swifttest
  -> enum SkillLevel: Comparable {
         case beginner
         case intermediate
         case expert(stars: Int)
     }
  -> var levels = [SkillLevel.intermediate, SkillLevel.beginner,
                   SkillLevel.expert(stars: 5), SkillLevel.expert(stars: 3)]
  -> for level in levels.sorted() {
         print(level)
     }
  <- beginner
  <- intermediate
  <- expert(stars: 3)
  <- expert(stars: 5)
  ```
-->

<!--
  The example above iterates and prints instead of printing the whole array
  because printing an array gives you the debug description of each element,
  which looks like temp123908.SkillLevel.expert(5) -- not nice to read.
-->

<!--
  - test: `no-synthesized-comparable-for-raw-value-enum`

  ```swifttest
  >> enum E: Int, Comparable {
  >>     case ten = 10
  >>     case twelve = 12
  >> }
  !$ error: type 'E' does not conform to protocol 'Comparable'
  !! enum E: Int, Comparable {
  !!      ^
  !$ note: enum declares raw type 'Int', preventing synthesized conformance of 'E' to 'Comparable'
  !! enum E: Int, Comparable {
  !!         ^
  !$ note: candidate would match if 'E' conformed to 'FloatingPoint'
  !! public static func < (lhs: Self, rhs: Self) -> Bool
  !!                        ^
  !$ note: candidate has non-matching type '<Self, Other> (Self, Other) -> Bool'
  !! public static func < <Other>(lhs: Self, rhs: Other) -> Bool where Other : BinaryInteger
  !!                        ^
  !$ note: candidate would match if 'E' conformed to '_Pointer'
  !! public static func < (lhs: Self, rhs: Self) -> Bool
  !!                        ^
  !$ note: candidate would match if 'E' conformed to '_Pointer'
  !! @inlinable public static func < <Other>(lhs: Self, rhs: Other) -> Bool where Other : _Pointer
  !!                                   ^
  !$ note: candidate has non-matching type '<Self> (Self, Self) -> Bool'
  !! @inlinable public static func < (x: Self, y: Self) -> Bool
  !!                                   ^
  !$ note: candidate would match if 'E' conformed to 'StringProtocol'
  !! @inlinable public static func < <RHS>(lhs: Self, rhs: RHS) -> Bool where RHS : StringProtocol
  !!                                   ^
  !$ note: protocol requires function '<' with type '(E, E) -> Bool'
  !! static func < (lhs: Self, rhs: Self) -> Bool
  !!                 ^
  ```
-->

## Conformidade implícita a um protocolo

Alguns protocolos são tão comuns que você os escreveria quase toda vez
que declara um novo tipo.
Para os protocolos a seguir,
o Swift infere automaticamente a conformidade
quando você define um tipo que implementa os requisitos do protocolo,
então você não precisa escrevê-la:

- [`Copyable`][]
- [`Sendable`][]
- [`BitwiseCopyable`][]

<!--
The definitions for the links in this list
are in the section above, Protocols That Have Semantic Requirements.
-->

Você ainda pode escrever a conformidade explicitamente,
mas isso não muda o comportamento do seu código.
Para suprimir uma conformidade implícita,
escreva um til (`~`) antes do nome do protocolo na lista de conformidades:

```swift
struct FileDescriptor: ~Sendable {
    let rawValue: Int
}
```

<!--
The example above is based on a Swift System API.
https://github.com/apple/swift-system/blob/main/Sources/System/FileDescriptor.swift

See also this PR that adds Sendable conformance to FileDescriptor:
https://github.com/apple/swift-system/pull/112
-->

O código acima mostra parte de um invólucro (wrapper) em torno de descritores de arquivo POSIX.
A estrutura `FileDescriptor`
satisfaz todos os requisitos do protocolo `Sendable`,
o que normalmente a tornaria enviável (sendable).
No entanto,
escrever `~Sendable` suprime essa conformidade implícita.
Mesmo que descritores de arquivo usem inteiros
para identificar e interagir com arquivos abertos,
e valores inteiros sejam enviáveis,
torná-la não enviável pode ajudar a evitar certos tipos de erro.

Outra forma de suprimir a conformidade implícita
é com uma extensão que você marca como indisponível:

```swift
@available(*, unavailable)
extension FileDescriptor: Sendable { }
```

<!--
  - test: `suppressing-implied-sendable-conformance`

  -> struct FileDescriptor {
  ->     let rawValue: CInt
  -> }

  -> @available(*, unavailable)
  -> extension FileDescriptor: Sendable { }
  >> let nonsendable: Sendable = FileDescriptor(rawValue: 10)
  !$ warning: conformance of 'FileDescriptor' to 'Sendable' is unavailable; this is an error in Swift 6
  !! let nonsendable: Sendable = FileDescriptor(rawValue: 10)
  !! ^
  !$ note: conformance of 'FileDescriptor' to 'Sendable' has been explicitly marked unavailable here
  !! extension FileDescriptor: Sendable { }
  !! ^
-->

Quando você escreve `~Sendable` em um lugar do seu código,
como no exemplo anterior,
outro trecho do programa ainda pode
estender o tipo `FileDescriptor` para adicionar a conformidade com `Sendable`.
Já a extensão indisponível deste exemplo
suprime a conformidade implícita com `Sendable`
e também impede que qualquer extensão em outro lugar do seu código
adicione a conformidade com `Sendable` ao tipo.

> Nota:
> Além dos protocolos discutidos acima,
> atores distribuídos (distributed actors) estão em conformidade implicitamente com o protocolo [`Codable`][].

[`Codable`]: https://developer.apple.com/documentation/swift/codable

## Coleções de tipos de protocolo

Um protocolo pode ser usado como o tipo a ser armazenado em
uma coleção, como um array ou um dicionário,
como mencionado em <doc:Protocols#Protocols-as-Types>.
Este exemplo cria um array de coisas `TextRepresentable`:

```swift
let things: [TextRepresentable] = [game, d12, simonTheHamster]
```

<!--
  - test: `protocols`

  ```swifttest
  -> let things: [TextRepresentable] = [game, d12, simonTheHamster]
  ```
-->

Agora é possível percorrer os itens do array
e imprimir a descrição textual de cada item:

```swift
for thing in things {
    print(thing.textualDescription)
}
// A game of Snakes and Ladders with 25 squares
// A 12-sided dice
// A hamster named Simon
```

<!--
  - test: `protocols`

  ```swifttest
  -> for thing in things {
        print(thing.textualDescription)
     }
  </ A game of Snakes and Ladders with 25 squares
  </ A 12-sided dice
  </ A hamster named Simon
  ```
-->

Observe que a constante `thing` é do tipo `TextRepresentable`.
Ela não é do tipo `Dice`, `DiceGame` ou `Hamster`,
mesmo que a instância real, nos bastidores, seja de um desses tipos.
Ainda assim, como ela é do tipo `TextRepresentable`,
e qualquer coisa que seja `TextRepresentable` tem a propriedade `textualDescription`,
é seguro acessar `thing.textualDescription` a cada passagem do laço.

## Herança de protocolos

Um protocolo pode *herdar* de um ou mais outros protocolos
e pode adicionar requisitos extras sobre os requisitos que herda.
A sintaxe para herança de protocolos é parecida com a sintaxe para herança de classes,
mas com a opção de listar vários protocolos herdados, separados por vírgulas:

```swift
protocol InheritingProtocol: SomeProtocol, AnotherProtocol {
    // protocol definition goes here
}
```

<!--
  - test: `protocols`

  ```swifttest
  >> protocol SomeProtocol {}
  >> protocol AnotherProtocol {}
  -> protocol InheritingProtocol: SomeProtocol, AnotherProtocol {
        // protocol definition goes here
     }
  ```
-->

Aqui está um exemplo de um protocolo que herda
o protocolo `TextRepresentable` apresentado acima:

```swift
protocol PrettyTextRepresentable: TextRepresentable {
    var prettyTextualDescription: String { get }
}
```

<!--
  - test: `protocols`

  ```swifttest
  -> protocol PrettyTextRepresentable: TextRepresentable {
        var prettyTextualDescription: String { get }
     }
  ```
-->

Este exemplo define um novo protocolo, `PrettyTextRepresentable`,
que herda de `TextRepresentable`.
Qualquer coisa que adote `PrettyTextRepresentable` precisa satisfazer todos os requisitos
impostos por `TextRepresentable`,
*mais* os requisitos adicionais impostos por `PrettyTextRepresentable`.
Neste exemplo, `PrettyTextRepresentable` acrescenta um único requisito:
fornecer uma propriedade de leitura chamada `prettyTextualDescription` que retorna uma `String`.

A classe `SnakesAndLadders` pode ser estendida para adotar e estar em conformidade com `PrettyTextRepresentable`:

```swift
extension SnakesAndLadders: PrettyTextRepresentable {
    var prettyTextualDescription: String {
        var output = textualDescription + ":\n"
        for index in 1...finalSquare {
            switch board[index] {
            case let ladder where ladder > 0:
                output += "▲ "
            case let snake where snake < 0:
                output += "▼ "
            default:
                output += "○ "
            }
        }
        return output
    }
}
```

<!--
  - test: `protocols`

  ```swifttest
  -> extension SnakesAndLadders: PrettyTextRepresentable {
        var prettyTextualDescription: String {
           var output = textualDescription + ":\n"
           for index in 1...finalSquare {
              switch board[index] {
                 case let ladder where ladder > 0:
                    output += "▲ "
                 case let snake where snake < 0:
                    output += "▼ "
                 default:
                    output += "○ "
              }
           }
           return output
        }
     }
  ```
-->

Esta extensão declara que adota o protocolo `PrettyTextRepresentable`
e fornece uma implementação da propriedade `prettyTextualDescription`
para o tipo `SnakesAndLadders`.
Tudo o que é `PrettyTextRepresentable` também precisa ser `TextRepresentable`,
então a implementação de `prettyTextualDescription` começa
acessando a propriedade `textualDescription`
do protocolo `TextRepresentable` para iniciar uma string de saída.
Ela acrescenta dois-pontos e uma quebra de linha,
e usa isso como início da sua representação textual formatada.
Em seguida, percorre o array de casas do tabuleiro
e acrescenta uma forma geométrica para representar o conteúdo de cada casa:

- Se o valor da casa for maior que `0`, ela é a base de uma escada,
  e é representada por `▲`.
- Se o valor da casa for menor que `0`, ela é a cabeça de uma cobra,
  e é representada por `▼`.
- Caso contrário, o valor da casa é `0`, e ela é uma casa “livre”,
  representada por `○`.

A propriedade `prettyTextualDescription` agora pode ser usada para imprimir uma descrição textual formatada
de qualquer instância de `SnakesAndLadders`:

```swift
print(game.prettyTextualDescription)
// A game of Snakes and Ladders with 25 squares:
// ○ ○ ▲ ○ ○ ▲ ○ ○ ▲ ▲ ○ ○ ○ ▼ ○ ○ ○ ○ ▼ ○ ○ ▼ ○ ▼ ○
```

<!--
  - test: `protocols`

  ```swifttest
  -> print(game.prettyTextualDescription)
  </ A game of Snakes and Ladders with 25 squares:
  </ ○ ○ ▲ ○ ○ ▲ ○ ○ ▲ ▲ ○ ○ ○ ▼ ○ ○ ○ ○ ▼ ○ ○ ▼ ○ ▼ ○
  ```
-->

## Protocolos exclusivos de classes

Você pode limitar a adoção de um protocolo a tipos classe (e não a estruturas ou enumerações)
adicionando o protocolo `AnyObject` à lista de herança de um protocolo.

```swift
protocol SomeClassOnlyProtocol: AnyObject, SomeInheritedProtocol {
    // class-only protocol definition goes here
}
```

<!--
  - test: `classOnlyProtocols`

  ```swifttest
  >> protocol SomeInheritedProtocol {}
  -> protocol SomeClassOnlyProtocol: AnyObject, SomeInheritedProtocol {
        // class-only protocol definition goes here
     }
  ```
-->

No exemplo acima, `SomeClassOnlyProtocol` só pode ser adotado por tipos classe.
É um erro de compilação escrever a definição de uma estrutura ou enumeração
que tente adotar `SomeClassOnlyProtocol`.

> Nota: Use um protocolo exclusivo de classes quando o comportamento definido pelos requisitos desse protocolo
> pressupõe ou exige que um tipo em conformidade tenha
> semântica de referência em vez de semântica de valor.
> Para saber mais sobre semântica de referência e de valor,
> veja <doc:ClassesAndStructures#Structures-and-Enumerations-Are-Value-Types>
> e <doc:ClassesAndStructures#Classes-Are-Reference-Types>.

<!--
  - test: `anyobject-doesn't-have-to-be-first`

  ```swifttest
  >> protocol SomeInheritedProtocol {}
  -> protocol SomeClassOnlyProtocol: SomeInheritedProtocol, AnyObject {
        // class-only protocol definition goes here
     }
  ```
-->

<!--
  TODO: a Cacheable protocol might make a good example here?
-->

Você também pode nomear uma classe específica na lista de herança de um protocolo
para exigir que todos os tipos em conformidade sejam subclasses dessa classe.

```swift
class Renderer {
    func render(_ text: String) {
        print(text)
    }
}

protocol Widget: Renderer {
    var title: String { get }
}

extension Widget {
    func display() {
        render(title)
    }
}

class ButtonWidget: Renderer, Widget {
    var title: String
    init(title: String) {
        self.title = title
    }
}

let button = ButtonWidget(title: "OK")
button.display()
// Prints "OK".
```

<!--
  - test: `classNameInProtocol`

  ```swifttest
  -> class Renderer {
        func render(_ text: String) {
            print(text)
        }
     }

  -> protocol Widget: Renderer {
        var title: String { get }
     }

  -> extension Widget {
        func display() {
            render(title)
        }
     }

  -> class ButtonWidget: Renderer, Widget {
        var title: String
        init(title: String) {
            self.title = title
        }
     }

  -> let button = ButtonWidget(title: "OK")
  -> button.display()
  <- OK
  ```
-->

No exemplo acima, `Widget` só pode ser adotado por subclasses de `Renderer`.
Como o protocolo garante que todo tipo em conformidade é uma subclasse de `Renderer`,
a extensão do protocolo `Widget` pode chamar `render(_:)` diretamente.
Um requisito de superclasse é mais restritivo do que usar `AnyObject`:
ele limita a conformidade a uma hierarquia de classes específica,
e não a qualquer tipo classe.
Use isso quando a implementação do protocolo
depender do comportamento concreto de uma classe base específica.

## Composição de protocolos

Pode ser útil exigir que um tipo esteja em conformidade com vários protocolos ao mesmo tempo.
Você pode combinar vários protocolos em um único requisito
com uma *composição de protocolos*.
Composições de protocolos se comportam como se você
tivesse definido um protocolo local temporário que tem os requisitos combinados
de todos os protocolos da composição.
Composições de protocolos não definem nenhum novo tipo de protocolo.

Composições de protocolos têm a forma `SomeProtocol & AnotherProtocol`.
Você pode listar quantos protocolos precisar,
separando-os com e comercial (`&`).
Além da lista de protocolos,
uma composição de protocolos também pode conter um tipo classe,
que você pode usar para especificar uma superclasse obrigatória.

Aqui está um exemplo que combina dois protocolos chamados `Named` e `Aged`
em um único requisito de composição para um parâmetro de função:

```swift
protocol Named {
    var name: String { get }
}
protocol Aged {
    var age: Int { get }
}
struct Person: Named, Aged {
    var name: String
    var age: Int
}
func wishHappyBirthday(to celebrator: Named & Aged) {
    print("Happy birthday, \(celebrator.name), you're \(celebrator.age)!")
}
let birthdayPerson = Person(name: "Malcolm", age: 21)
wishHappyBirthday(to: birthdayPerson)
// Prints "Happy birthday, Malcolm, you're 21!"
```

<!--
  - test: `protocolComposition`

  ```swifttest
  -> protocol Named {
        var name: String { get }
     }
  -> protocol Aged {
        var age: Int { get }
     }
  -> struct Person: Named, Aged {
        var name: String
        var age: Int
     }
  -> func wishHappyBirthday(to celebrator: Named & Aged) {
        print("Happy birthday, \(celebrator.name), you're \(celebrator.age)!")
     }
  -> let birthdayPerson = Person(name: "Malcolm", age: 21)
  -> wishHappyBirthday(to: birthdayPerson)
  <- Happy birthday, Malcolm, you're 21!
  ```
-->

Neste exemplo,
o protocolo `Named`
tem um único requisito: uma propriedade `String` de leitura chamada `name`.
O protocolo `Aged`
tem um único requisito: uma propriedade `Int` de leitura chamada `age`.
Os dois protocolos são adotados por uma estrutura chamada `Person`.

O exemplo também define uma função `wishHappyBirthday(to:)`.
O tipo do parâmetro `celebrator` é `Named & Aged`,
o que significa “qualquer tipo que esteja em conformidade com os protocolos `Named` e `Aged`”.
Não importa qual tipo específico é passado para a função,
desde que esteja em conformidade com os dois protocolos exigidos.

O exemplo então cria uma nova instância de `Person` chamada `birthdayPerson`
e passa essa nova instância para a função `wishHappyBirthday(to:)`.
Como `Person` está em conformidade com os dois protocolos, essa chamada é válida,
e a função `wishHappyBirthday(to:)` pode imprimir a saudação de aniversário.

Aqui está um exemplo que combina
o protocolo `Named` do exemplo anterior
com uma classe `Location`:

```swift
class Location {
    var latitude: Double
    var longitude: Double
    init(latitude: Double, longitude: Double) {
        self.latitude = latitude
        self.longitude = longitude
    }
}
class City: Location, Named {
    var name: String
    init(name: String, latitude: Double, longitude: Double) {
        self.name = name
        super.init(latitude: latitude, longitude: longitude)
    }
}
func beginConcert(in location: Location & Named) {
    print("Hello, \(location.name)!")
}

let seattle = City(name: "Seattle", latitude: 47.6, longitude: -122.3)
beginConcert(in: seattle)
// Prints "Hello, Seattle!"
```

<!--
  - test: `protocolComposition`

  ```swifttest
  -> class Location {
         var latitude: Double
         var longitude: Double
         init(latitude: Double, longitude: Double) {
             self.latitude = latitude
             self.longitude = longitude
         }
     }
  -> class City: Location, Named {
         var name: String
         init(name: String, latitude: Double, longitude: Double) {
             self.name = name
             super.init(latitude: latitude, longitude: longitude)
         }
     }
  -> func beginConcert(in location: Location & Named) {
         print("Hello, \(location.name)!")
     }

  -> let seattle = City(name: "Seattle", latitude: 47.6, longitude: -122.3)
  -> beginConcert(in: seattle)
  <- Hello, Seattle!
  ```
-->

A função `beginConcert(in:)` recebe
um parâmetro do tipo `Location & Named`,
o que significa “qualquer tipo que seja uma subclasse de `Location`
e que esteja em conformidade com o protocolo `Named`”.
Nesse caso, `City` atende aos dois requisitos.

Passar `birthdayPerson` para a função `beginConcert(in:)`
é inválido, porque `Person` não é uma subclasse de `Location`.
Da mesma forma,
se você criasse uma subclasse de `Location`
que não estivesse em conformidade com o protocolo `Named`,
chamar `beginConcert(in:)` com uma instância desse tipo
também seria inválido.

## Verificando a conformidade a um protocolo

Você pode usar os operadores `is` e `as`, descritos em <doc:TypeCasting>,
para verificar a conformidade com um protocolo e para converter para um protocolo específico.
Verificar e converter para um protocolo
segue exatamente a mesma sintaxe de verificar e converter para um tipo:

- O operador `is` retorna `true` se uma instância está em conformidade com um protocolo
  e retorna `false` se não estiver.
- A versão `as?` do operador de conversão descendente retorna
  um valor opcional do tipo do protocolo,
  e esse valor é `nil` se a instância não estiver em conformidade com o protocolo.
- A versão `as!` do operador de conversão descendente força a conversão para o tipo do protocolo
  e dispara um erro em tempo de execução se a conversão não der certo.

Este exemplo define um protocolo chamado `HasArea`,
com um único requisito de propriedade: uma propriedade `Double` de leitura chamada `area`:

```swift
protocol HasArea {
    var area: Double { get }
}
```

<!--
  - test: `protocolConformance`

  ```swifttest
  -> protocol HasArea {
        var area: Double { get }
     }
  ```
-->

Aqui estão duas classes, `Circle` e `Country`,
ambas em conformidade com o protocolo `HasArea`:

```swift
class Circle: HasArea {
    let pi = 3.1415927
    var radius: Double
    var area: Double { return pi * radius * radius }
    init(radius: Double) { self.radius = radius }
}
class Country: HasArea {
    var area: Double
    init(area: Double) { self.area = area }
}
```

<!--
  - test: `protocolConformance`

  ```swifttest
  -> class Circle: HasArea {
        let pi = 3.1415927
        var radius: Double
        var area: Double { return pi * radius * radius }
        init(radius: Double) { self.radius = radius }
     }
  -> class Country: HasArea {
        var area: Double
        init(area: Double) { self.area = area }
     }
  ```
-->

A classe `Circle` implementa o requisito da propriedade `area`
como uma propriedade computada, com base em uma propriedade armazenada `radius`.
A classe `Country` implementa o requisito `area` diretamente como uma propriedade armazenada.
As duas classes estão corretamente em conformidade com o protocolo `HasArea`.

Aqui está uma classe chamada `Animal`, que não está em conformidade com o protocolo `HasArea`:

```swift
class Animal {
    var legs: Int
    init(legs: Int) { self.legs = legs }
}
```

<!--
  - test: `protocolConformance`

  ```swifttest
  -> class Animal {
        var legs: Int
        init(legs: Int) { self.legs = legs }
     }
  ```
-->

As classes `Circle`, `Country` e `Animal` não têm uma superclasse em comum.
Mesmo assim, todas são classes, então instâncias dos três tipos
podem ser usadas para inicializar um array que armazena valores do tipo `AnyObject`:

```swift
let objects: [AnyObject] = [
    Circle(radius: 2.0),
    Country(area: 243_610),
    Animal(legs: 4)
]
```

<!--
  - test: `protocolConformance`

  ```swifttest
  -> let objects: [AnyObject] = [
        Circle(radius: 2.0),
        Country(area: 243_610),
        Animal(legs: 4)
     ]
  ```
-->

O array `objects` é inicializado com um literal de array que contém
uma instância de `Circle` com raio de 2 unidades;
uma instância de `Country` inicializada com
a área superficial do Reino Unido em quilômetros quadrados;
e uma instância de `Animal` com quatro patas.

Agora é possível percorrer o array `objects`,
e verificar se cada objeto nele está em conformidade com o protocolo `HasArea`:

```swift
for object in objects {
    if let objectWithArea = object as? HasArea {
        print("Area is \(objectWithArea.area)")
    } else {
        print("Something that doesn't have an area")
    }
}
// Area is 12.5663708
// Area is 243610.0
// Something that doesn't have an area
```

<!--
  - test: `protocolConformance`

  ```swifttest
  -> for object in objects {
        if let objectWithArea = object as? HasArea {
           print("Area is \(objectWithArea.area)")
        } else {
           print("Something that doesn't have an area")
        }
     }
  </ Area is 12.5663708
  </ Area is 243610.0
  </ Something that doesn't have an area
  ```
-->

Sempre que um objeto do array está em conformidade com o protocolo `HasArea`,
o valor opcional retornado pelo operador `as?` é desembrulhado, com vinculação opcional,
em uma constante chamada `objectWithArea`.
A constante `objectWithArea` é conhecida como sendo do tipo `HasArea`,
então a sua propriedade `area` pode ser acessada e impressa de forma segura em relação aos tipos.

Observe que os objetos originais não são alterados pelo processo de conversão.
Eles continuam sendo um `Circle`, um `Country` e um `Animal`.
No entanto, no momento em que são armazenados na constante `objectWithArea`,
eles são conhecidos apenas como do tipo `HasArea`,
e por isso só a propriedade `area` pode ser acessada.

<!--
  TODO: This is an *extremely* contrived example.
  Also, it's not particularly useful to be able to get the area of these two objects,
  because there's no shared unit system.
  Also also, I'd say that a circle should probably be a structure, not a class.
  Plus, I'm having to write lots of boilerplate initializers,
  which make the example far less focused than I'd like.
  The problem is, I can't use strings within an @objc protocol
  without also having to import Foundation, so it's numbers or bust, I'm afraid.
-->

<!--
  TODO: Since the restrictions on @objc of the previous TODO are now lifted,
  Should the previous examples be revisited?
-->

## Requisitos opcionais de protocolo

<!--
  TODO: split this section into several subsections as per [Contributor 7746]'s feedback,
  and cover the missing alternative approaches that he mentioned.
-->

<!--
  TODO: you can specify optional subscripts,
  and the way you check for them / work with them is a bit esoteric.
  You have to try and access a value from the subscript,
  and see if the value you get back (which will be an optional)
  has a value or is nil.
-->

Você pode definir *requisitos opcionais* para protocolos.
Esses requisitos não precisam ser implementados pelos tipos em conformidade com o protocolo.
Requisitos opcionais são precedidos pelo modificador `optional`
como parte da definição do protocolo.
Requisitos opcionais existem para que você possa escrever código
que interopere com Objective-C.
Tanto o protocolo quanto o requisito opcional
devem ser marcados com o atributo `@objc`.
Observe que protocolos `@objc` só podem ser adotados por classes,
e não por estruturas ou enumerações.

Quando você usa um método ou propriedade em um requisito opcional,
o tipo dele se torna automaticamente opcional.
Por exemplo,
um método do tipo `(Int) -> String` se torna `((Int) -> String)?`.
Observe que o tipo de função inteiro
é envolvido pelo opcional,
e não o valor de retorno do método.

Um requisito opcional de protocolo pode ser chamado com encadeamento opcional,
para levar em conta a possibilidade de o requisito não ter sido implementado
por um tipo em conformidade com o protocolo.
Você verifica se um método opcional foi implementado
escrevendo um ponto de interrogação depois do nome do método na chamada,
como em `someOptionalMethod?(someArgument)`.
Para informações sobre encadeamento opcional, veja <doc:OptionalChaining>.

O exemplo a seguir define uma classe contadora de inteiros chamada `Counter`,
que usa uma fonte de dados externa para fornecer o valor do seu incremento.
Essa fonte de dados é definida pelo protocolo `CounterDataSource`,
que tem dois requisitos opcionais:

```swift
@objc protocol CounterDataSource {
    @objc optional func increment(forCount count: Int) -> Int
    @objc optional var fixedIncrement: Int { get }
}
```

<!--
  - test: `protocolConformance`

  ```swifttest
  >> import Foundation
  -> @objc protocol CounterDataSource {
  ->    @objc optional func increment(forCount count: Int) -> Int
  ->    @objc optional var fixedIncrement: Int { get }
  -> }
  ```
-->

O protocolo `CounterDataSource` define
um requisito de método opcional chamado `increment(forCount:)`
e um requisito de propriedade opcional chamado `fixedIncrement`.
Esses requisitos definem duas maneiras diferentes de as fontes de dados fornecerem
um valor de incremento adequado para uma instância de `Counter`.

> Nota: Estritamente falando, você pode escrever uma classe personalizada
> que esteja em conformidade com `CounterDataSource` sem implementar
> *nenhum* dos dois requisitos do protocolo.
> Afinal, os dois são opcionais.
> Embora seja tecnicamente permitido, isso não resultaria em uma fonte de dados muito boa.

A classe `Counter`, definida abaixo,
tem uma propriedade opcional `dataSource` do tipo `CounterDataSource?`:

```swift
class Counter {
    var count = 0
    var dataSource: CounterDataSource?
    func increment() {
        if let amount = dataSource?.increment?(forCount: count) {
            count += amount
        } else if let amount = dataSource?.fixedIncrement {
            count += amount
        }
    }
}
```

<!--
  - test: `protocolConformance`

  ```swifttest
  -> class Counter {
        var count = 0
        var dataSource: CounterDataSource?
        func increment() {
           if let amount = dataSource?.increment?(forCount: count) {
              count += amount
           } else if let amount = dataSource?.fixedIncrement {
              count += amount
           }
        }
     }
  ```
-->

A classe `Counter` armazena seu valor atual em uma propriedade variável chamada `count`.
A classe `Counter` também define um método chamado `increment`,
que incrementa a propriedade `count` toda vez que o método é chamado.

O método `increment()` primeiro tenta obter um valor de incremento
procurando uma implementação do método `increment(forCount:)` na sua fonte de dados.
O método `increment()` usa encadeamento opcional para tentar chamar `increment(forCount:)`,
e passa o valor atual de `count` como único argumento do método.

Observe que *dois* níveis de encadeamento opcional estão em jogo aqui.
Primeiro, é possível que `dataSource` seja `nil`,
por isso `dataSource` tem um ponto de interrogação depois do nome para indicar que
`increment(forCount:)` deve ser chamado somente se `dataSource` não for `nil`.
Segundo, mesmo que `dataSource` *exista*,
não há garantia de que ele implemente `increment(forCount:)`,
porque é um requisito opcional.
Aqui, a possibilidade de `increment(forCount:)` não ser implementado
também é tratada pelo encadeamento opcional.
A chamada a `increment(forCount:)` acontece
somente se `increment(forCount:)` existir,
ou seja, se não for `nil`.
É por isso que `increment(forCount:)` também é escrito com um ponto de interrogação depois do nome.

Como a chamada a `increment(forCount:)` pode falhar por qualquer um desses dois motivos,
a chamada retorna um valor `Int` *opcional*.
Isso vale mesmo que `increment(forCount:)` seja definido como retornando
um valor `Int` não opcional na definição de `CounterDataSource`.
Mesmo havendo duas operações de encadeamento opcional, uma depois da outra,
o resultado continua envolvido em um único opcional.
Para mais informações sobre o uso de várias operações de encadeamento opcional,
veja <doc:OptionalChaining#Linking-Multiple-Levels-of-Chaining>.

Depois de chamar `increment(forCount:)`, o `Int` opcional que ele retorna
é desembrulhado em uma constante chamada `amount`, usando vinculação opcional.
Se o `Int` opcional contiver um valor,
ou seja, se o delegado e o método existirem,
e o método tiver retornado um valor,
o `amount` desembrulhado é somado à propriedade armazenada `count`,
e o incremento está concluído.

Se *não* for possível obter um valor do método `increment(forCount:)`,
seja porque `dataSource` é nil,
seja porque a fonte de dados não implementa `increment(forCount:)`,
o método `increment()` tenta obter um valor
da propriedade `fixedIncrement` da fonte de dados.
A propriedade `fixedIncrement` também é um requisito opcional,
então o valor dela é um `Int` opcional,
mesmo que `fixedIncrement` esteja definido como uma propriedade `Int` não opcional
na definição do protocolo `CounterDataSource`.

Aqui está uma implementação simples de `CounterDataSource` em que a fonte de dados
retorna um valor constante `3` toda vez que é consultada.
Ela faz isso implementando o requisito de propriedade opcional `fixedIncrement`:

```swift
class ThreeSource: NSObject, CounterDataSource {
    let fixedIncrement = 3
}
```

<!--
  - test: `protocolConformance`

  ```swifttest
  -> class ThreeSource: NSObject, CounterDataSource {
        let fixedIncrement = 3
     }
  ```
-->

Você pode usar uma instância de `ThreeSource` como fonte de dados de uma nova instância de `Counter`:

```swift
var counter = Counter()
counter.dataSource = ThreeSource()
for _ in 1...4 {
    counter.increment()
    print(counter.count)
}
// 3
// 6
// 9
// 12
```

<!--
  - test: `protocolConformance`

  ```swifttest
  -> var counter = Counter()
  -> counter.dataSource = ThreeSource()
  -> for _ in 1...4 {
        counter.increment()
        print(counter.count)
     }
  </ 3
  </ 6
  </ 9
  </ 12
  ```
-->

O código acima cria uma nova instância de `Counter`;
define a fonte de dados dela como uma nova instância de `ThreeSource`;
e chama quatro vezes o método `increment()` do contador.
Como esperado, a propriedade `count` do contador aumenta três
a cada vez que `increment()` é chamado.

Aqui está uma fonte de dados mais complexa, chamada `TowardsZeroSource`,
que faz uma instância de `Counter` contar para cima ou para baixo em direção a zero
a partir do seu valor atual de `count`:

```swift
class TowardsZeroSource: NSObject, CounterDataSource {
    func increment(forCount count: Int) -> Int {
        if count == 0 {
            return 0
        } else if count < 0 {
            return 1
        } else {
            return -1
        }
    }
}
```

<!--
  - test: `protocolConformance`

  ```swifttest
  -> class TowardsZeroSource: NSObject, CounterDataSource {
        func increment(forCount count: Int) -> Int {
           if count == 0 {
              return 0
           } else if count < 0 {
              return 1
           } else {
              return -1
           }
        }
     }
  ```
-->

A classe `TowardsZeroSource` implementa
o método opcional `increment(forCount:)` do protocolo `CounterDataSource`
e usa o valor do argumento `count` para descobrir em que direção contar.
Se `count` já for zero, o método retorna `0`
para indicar que nenhuma contagem adicional deve acontecer.

Você pode usar uma instância de `TowardsZeroSource` com a instância existente de `Counter`
para contar de `-4` até zero.
Quando o contador chega a zero, nenhuma contagem adicional acontece:

```swift
counter.count = -4
counter.dataSource = TowardsZeroSource()
for _ in 1...5 {
    counter.increment()
    print(counter.count)
}
// -3
// -2
// -1
// 0
// 0
```

<!--
  - test: `protocolConformance`

  ```swifttest
  -> counter.count = -4
  -> counter.dataSource = TowardsZeroSource()
  -> for _ in 1...5 {
        counter.increment()
        print(counter.count)
     }
  </ -3
  </ -2
  </ -1
  </ 0
  </ 0
  ```
-->

## Extensões de protocolos

Protocolos podem ser estendidos para fornecer implementações de métodos,
inicializadores, subscritos e propriedades computadas aos tipos em conformidade.
Isso permite definir comportamento nos próprios protocolos,
em vez de em cada conformidade individual de cada tipo ou em uma função global.

Por exemplo, o protocolo `RandomNumberGenerator` pode ser estendido
para fornecer um método `randomBool()`,
que usa o resultado do método obrigatório `random()`
para retornar um valor `Bool` aleatório:

```swift
extension RandomNumberGenerator {
    func randomBool() -> Bool {
        return random() > 0.5
    }
}
```

<!--
  - test: `protocols`

  ```swifttest
  -> extension RandomNumberGenerator {
        func randomBool() -> Bool {
           return random() > 0.5
        }
     }
  ```
-->

Ao criar uma extensão sobre o protocolo,
todos os tipos em conformidade ganham automaticamente essa implementação de método
sem nenhuma modificação adicional.

```swift
let generator = LinearCongruentialGenerator()
print("Here's a random number: \(generator.random())")
// Prints "Here's a random number: 0.3746499199817101".
print("And here's a random Boolean: \(generator.randomBool())")
// Prints "And here's a random Boolean: true".
```

<!--
  - test: `protocols`

  ```swifttest
  >> do {
  -> let generator = LinearCongruentialGenerator()
  -> print("Here's a random number: \(generator.random())")
  <- Here's a random number: 0.3746499199817101
  -> print("And here's a random Boolean: \(generator.randomBool())")
  <- And here's a random Boolean: true
  >> }
  ```
-->

<!--
  The extra scope in the above test code allows this 'generator' variable to shadow
  the variable that already exists from a previous testcode block.
-->

Extensões de protocolo podem adicionar implementações aos tipos em conformidade,
mas não podem fazer um protocolo estender ou herdar de outro protocolo.
A herança de protocolos é sempre especificada na própria declaração do protocolo.

### Fornecendo implementações padrão

Você pode usar extensões de protocolo para fornecer uma implementação padrão
para qualquer requisito de método ou propriedade computada desse protocolo.
Se um tipo em conformidade fornecer a sua própria implementação de um método ou propriedade obrigatórios,
essa implementação será usada no lugar da fornecida pela extensão.

> Nota: Requisitos de protocolo com implementações padrão fornecidas por extensões
> são diferentes dos requisitos opcionais de protocolo.
> Embora os tipos em conformidade não precisem fornecer a própria implementação de nenhum dos dois,
> requisitos com implementação padrão podem ser chamados sem encadeamento opcional.

Por exemplo, o protocolo `PrettyTextRepresentable`,
que herda do protocolo `TextRepresentable`,
pode fornecer uma implementação padrão da sua propriedade obrigatória `prettyTextualDescription`
que simplesmente retorna o resultado de acessar a propriedade `textualDescription`:

```swift
extension PrettyTextRepresentable  {
    var prettyTextualDescription: String {
        return textualDescription
    }
}
```

<!--
  - test: `protocols`

  ```swifttest
  -> extension PrettyTextRepresentable  {
        var prettyTextualDescription: String {
           return textualDescription
        }
     }
  ```
-->

<!--
  TODO <rdar://problem/32211512> TSPL: Explain when you can/can't override a protocol default implementation
-->

<!--
  If something is a protocol requirement,
  types that conform to the protocol can override the default implementation.
-->

<!--
  If something isn't a requirement,
  you get wonky behavior when you try to override the default implementation.
-->

<!--
  If the static type is the conforming type,
  your override is used.
-->

<!--
  If the static type is the protocol type,
  the default implementation is used.
-->

<!--
  You can't write ``final`` on a default implementation
  to prevent someone from overriding it in a conforming type.
-->

### Adicionando restrições a extensões de protocolo

Ao definir uma extensão de protocolo,
você pode especificar restrições que os tipos em conformidade
devem satisfazer antes que os métodos e propriedades da extensão fiquem disponíveis.
Você escreve essas restrições depois do nome do protocolo que está estendendo,
usando uma cláusula genérica `where`.
Para mais informações sobre cláusulas genéricas `where`, veja <doc:Generics#Generic-Where-Clauses>.

Por exemplo,
você pode definir uma extensão do protocolo `Collection`
que se aplica a qualquer coleção cujos elementos estejam em conformidade
com o protocolo `Equatable`.
Ao restringir os elementos de uma coleção ao protocolo `Equatable`,
que faz parte da biblioteca padrão do Swift,
você pode usar os operadores `==` e `!=` para verificar igualdade e desigualdade entre dois elementos.

```swift
extension Collection where Element: Equatable {
    func allEqual() -> Bool {
        for element in self {
            if element != self.first {
                return false
            }
        }
        return true
    }
}
```

<!--
  - test: `protocols`

  ```swifttest
  -> extension Collection where Element: Equatable {
         func allEqual() -> Bool {
             for element in self {
                 if element != self.first {
                     return false
                 }
             }
             return true
         }
     }
  ```
-->

O método `allEqual()` retorna `true`
somente se todos os elementos da coleção forem iguais.

Considere dois arrays de inteiros,
um em que todos os elementos são iguais,
e outro em que não são:

```swift
let equalNumbers = [100, 100, 100, 100, 100]
let differentNumbers = [100, 100, 200, 100, 200]
```

<!--
  - test: `protocols`

  ```swifttest
  -> let equalNumbers = [100, 100, 100, 100, 100]
  -> let differentNumbers = [100, 100, 200, 100, 200]
  ```
-->

Como arrays estão em conformidade com `Collection`
e inteiros estão em conformidade com `Equatable`,
`equalNumbers` e `differentNumbers` podem usar o método `allEqual()`:

```swift
print(equalNumbers.allEqual())
// Prints "true".
print(differentNumbers.allEqual())
// Prints "false".
```

<!--
  - test: `protocols`

  ```swifttest
  -> print(equalNumbers.allEqual())
  <- true
  -> print(differentNumbers.allEqual())
  <- false
  ```
-->

> Nota: Se um tipo em conformidade satisfizer os requisitos de várias extensões com restrições
> que fornecem implementações para o mesmo método ou propriedade,
> o Swift usa a implementação correspondente às restrições mais específicas.

<!--
  TODO: It would be great to pull this out of a note,
  but we should wait until we have a better narrative that shows how this
  works with some examples.
-->

<!--
  TODO: Other things to be included
  ---------------------------------
  Class-only protocols
  Protocols marked @objc
  Standard-library protocols such as Sequence, Equatable etc.?
  Show how to make a custom type conform to Boolean or some other protocol
  Show a protocol being used by an enumeration
  accessing protocol methods, properties etc.  through a constant or variable that's *just* of protocol type
  Protocols can't be nested, but nested types can implement protocols
  Protocol requirements can be marked as @unavailable, but this currently only works if they're also marked as @objc.
  Checking for (and calling) optional implementations via optional binding and closures
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
