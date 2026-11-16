# Extensions

Adicione funcionalidades a um tipo existente.

Uma *extension* adiciona novas funcionalidades a um tipo existente,
seja ele uma class, uma struct, um enum ou um protocolo.
Isso inclui a possibilidade de estender tipos
para os quais você não tem acesso ao código-fonte original
(conhecido como *modelagem retroativa*).
Extensions são parecidas com as categories do Objective-C.
(Diferentemente das categories do Objective-C, as extensions do Swift não têm nome.)

Extensions em Swift podem:

- Adicionar propriedades computadas de instância e propriedades computadas de tipo
- Definir métodos de instância e métodos de tipo
- Fornecer novos inicializadores
- Definir subscripts
- Definir e usar novos tipos aninhados
- Fazer um tipo existente adotar um protocolo

Em Swift,
você pode até estender um protocolo para fornecer implementações dos seus requisitos
ou adicionar funcionalidades extras que os tipos que o adotam podem aproveitar.
Para mais detalhes, veja <doc:Protocols#Protocol-Extensions>.

> Nota: Extensions podem adicionar novas funcionalidades a um tipo,
> mas não podem sobrescrever funcionalidades existentes.

<!--
  - test: `extensionsCannotOverrideExistingBehavior`

  ```swifttest
  -> class C {
        var x = 0
        func foo() {}
     }
  -> extension C {
        override var x: Int {
           didSet {
              print("new x is \(x)")
           }
        }
        override func foo() {
           print("called overridden foo")
        }
     }
  !$ error: property does not override any property from its superclass
  !! override var x: Int {
  !! ~~~~~~~~     ^
  !$ error: ambiguous use of 'x'
  !! print("new x is \(x)")
  !!            ^
  !$ note: found this candidate
  !! var x = 0
  !!     ^
  !$ note: found this candidate
  !! override var x: Int {
  !!              ^
  !$ error: invalid redeclaration of 'x'
  !! override var x: Int {
  !!              ^
  !$ note: 'x' previously declared here
  !! var x = 0
  !!     ^
  !$ error: method does not override any method from its superclass
  !! override func foo() {
  !! ~~~~~~~~      ^
  !$ error: invalid redeclaration of 'foo()'
  !! override func foo() {
  !!               ^
  !$ note: 'foo()' previously declared here
  !! func foo() {}
  !!      ^
  ```
-->

## Sintaxe de extension

Declare extensions com a palavra-chave `extension`:

```swift
extension SomeType {
    // new functionality to add to SomeType goes here
}
```

<!--
  - test: `extensionSyntax`

  ```swifttest
  >> struct SomeType {}
  -> extension SomeType {
        // new functionality to add to SomeType goes here
     }
  ```
-->

Uma extension pode estender um tipo existente para fazê-lo adotar um ou mais protocolos.
Para adicionar a conformância a um protocolo,
você escreve os nomes dos protocolos
da mesma forma que escreveria para uma class ou struct:

```swift
extension SomeType: SomeProtocol, AnotherProtocol {
    // implementation of protocol requirements goes here
}
```

<!--
  - test: `extensionSyntax`

  ```swifttest
  >> protocol SomeProtocol {}
  >> protocol AnotherProtocol {}
  -> extension SomeType: SomeProtocol, AnotherProtocol {
        // implementation of protocol requirements goes here
     }
  ```
-->

Adicionar a conformância a um protocolo dessa forma é descrito em
<doc:Protocols#Adding-Protocol-Conformance-with-an-Extension>.

Uma extension pode ser usada para estender um tipo genérico existente,
como descrito em <doc:Generics#Extending-a-Generic-Type>.
Você também pode estender um tipo genérico para adicionar funcionalidades de forma condicional,
como descrito em <doc:Generics#Extensions-with-a-Generic-Where-Clause>.

> Nota: Se você definir uma extension para adicionar uma nova funcionalidade a um tipo existente,
> a nova funcionalidade fica disponível em todas as instâncias existentes desse tipo,
> mesmo que elas tenham sido criadas antes de a extension ser definida.

## Propriedades computadas

Extensions podem adicionar propriedades computadas de instância e propriedades computadas de tipo a tipos existentes.
Este exemplo adiciona cinco propriedades computadas de instância ao tipo `Double` embutido do Swift,
para oferecer suporte básico ao trabalho com unidades de distância:

```swift
extension Double {
    var km: Double { return self * 1_000.0 }
    var m: Double { return self }
    var cm: Double { return self / 100.0 }
    var mm: Double { return self / 1_000.0 }
    var ft: Double { return self / 3.28084 }
}
let oneInch = 25.4.mm
print("One inch is \(oneInch) meters")
// Prints "One inch is 0.0254 meters".
let threeFeet = 3.ft
print("Three feet is \(threeFeet) meters")
// Prints "Three feet is 0.914399970739201 meters".
```

<!--
  - test: `extensionsComputedProperties`

  ```swifttest
  -> extension Double {
        var km: Double { return self * 1_000.0 }
        var m: Double { return self }
        var cm: Double { return self / 100.0 }
        var mm: Double { return self / 1_000.0 }
        var ft: Double { return self / 3.28084 }
     }
  -> let oneInch = 25.4.mm
  -> print("One inch is \(oneInch) meters")
  <- One inch is 0.0254 meters
  -> let threeFeet = 3.ft
  -> print("Three feet is \(threeFeet) meters")
  <- Three feet is 0.914399970739201 meters
  ```
-->

Essas propriedades computadas expressam que um valor `Double`
deve ser considerado como uma certa unidade de comprimento.
Embora sejam implementadas como propriedades computadas,
os nomes dessas propriedades podem ser anexados
a um literal de ponto flutuante com sintaxe de ponto,
como forma de usar esse literal para fazer conversões de distância.

Neste exemplo, um valor `Double` de `1.0` é considerado como representando “um metro”.
É por isso que a propriedade computada `m` retorna `self` ---
a expressão `1.m` é considerada como o cálculo de um valor `Double` de `1.0`.

Outras unidades precisam de alguma conversão para serem expressas em metros.
Um quilômetro equivale a 1.000 metros,
então a propriedade computada `km` multiplica o valor por `1_000.00`
para converter para um número expresso em metros.
Da mesma forma, há 3,28084 pés em um metro,
então a propriedade computada `ft` divide o valor `Double` subjacente
por `3.28084`, para convertê-lo de pés para metros.

Essas propriedades são somente leitura,
por isso são escritas sem a palavra-chave `get`, para deixar o código mais curto.
O valor de retorno delas é do tipo `Double`
e pode ser usado em cálculos matemáticos sempre que um `Double` for aceito:

```swift
let aMarathon = 42.km + 195.m
print("A marathon is \(aMarathon) meters long")
// Prints "A marathon is 42195.0 meters long".
```

<!--
  - test: `extensionsComputedProperties`

  ```swifttest
  -> let aMarathon = 42.km + 195.m
  -> print("A marathon is \(aMarathon) meters long")
  <- A marathon is 42195.0 meters long
  ```
-->

> Nota: Extensions podem adicionar novas propriedades computadas, mas não podem adicionar propriedades armazenadas
> nem adicionar observadores de propriedade a propriedades existentes.

<!--
  - test: `extensionsCannotAddStoredProperties`

  ```swifttest
  -> class C {}
  -> extension C { var x = 0 }
  !$ error: extensions must not contain stored properties
  !! extension C { var x = 0 }
  !!                   ^
  ```
-->

<!--
  TODO: change this example to something more advisable / less contentious.
-->

## Inicializadores

Extensions podem adicionar novos inicializadores a tipos existentes.
Isso permite estender outros tipos para aceitar
seus próprios tipos personalizados como parâmetros de inicialização,
ou para oferecer opções adicionais de inicialização
que não faziam parte da implementação original do tipo.

Extensions podem adicionar novos inicializadores de conveniência a uma class,
mas não podem adicionar novos inicializadores designados nem desinicializadores a uma class.
Inicializadores designados e desinicializadores
precisam sempre ser fornecidos pela implementação original da class.

Se você usar uma extension para adicionar um inicializador a um tipo de valor que fornece
valores padrão para todas as suas propriedades armazenadas
e não define nenhum inicializador personalizado,
você pode chamar o inicializador padrão e o inicializador memberwise desse tipo de valor
de dentro do inicializador da sua extension.
Isso não aconteceria se você tivesse escrito o inicializador
como parte da implementação original do tipo de valor,
como descrito em <doc:Initialization#Initializer-Delegation-for-Value-Types>.

Se você usar uma extension para adicionar um inicializador a uma struct
declarada em outro módulo,
o novo inicializador não pode acessar `self` até chamar
um inicializador do módulo que a define.

O exemplo abaixo define uma struct personalizada `Rect` para representar um retângulo geométrico.
O exemplo também define duas structs auxiliares chamadas `Size` e `Point`,
ambas com valores padrão de `0.0` para todas as suas propriedades:

```swift
struct Size {
    var width = 0.0, height = 0.0
}
struct Point {
    var x = 0.0, y = 0.0
}
struct Rect {
    var origin = Point()
    var size = Size()
}
```

<!--
  - test: `extensionsInitializers`

  ```swifttest
  -> struct Size {
        var width = 0.0, height = 0.0
     }
  -> struct Point {
        var x = 0.0, y = 0.0
     }
  -> struct Rect {
        var origin = Point()
        var size = Size()
     }
  ```
-->

Como a struct `Rect` fornece valores padrão para todas as suas propriedades,
ela recebe automaticamente um inicializador padrão e um inicializador memberwise,
como descrito em <doc:Initialization#Default-Initializers>.
Esses inicializadores podem ser usados para criar novas instâncias de `Rect`:

```swift
let defaultRect = Rect()
let memberwiseRect = Rect(origin: Point(x: 2.0, y: 2.0),
    size: Size(width: 5.0, height: 5.0))
```

<!--
  - test: `extensionsInitializers`

  ```swifttest
  -> let defaultRect = Rect()
  -> let memberwiseRect = Rect(origin: Point(x: 2.0, y: 2.0),
        size: Size(width: 5.0, height: 5.0))
  ```
-->

Você pode estender a struct `Rect` para fornecer um inicializador adicional
que recebe um ponto central e um tamanho específicos:

```swift
extension Rect {
    init(center: Point, size: Size) {
        let originX = center.x - (size.width / 2)
        let originY = center.y - (size.height / 2)
        self.init(origin: Point(x: originX, y: originY), size: size)
    }
}
```

<!--
  - test: `extensionsInitializers`

  ```swifttest
  -> extension Rect {
        init(center: Point, size: Size) {
           let originX = center.x - (size.width / 2)
           let originY = center.y - (size.height / 2)
           self.init(origin: Point(x: originX, y: originY), size: size)
        }
     }
  ```
-->

Esse novo inicializador começa calculando um ponto de origem adequado com base
no ponto `center` e no valor `size` fornecidos.
Em seguida, ele chama o inicializador memberwise automático da struct,
`init(origin:size:)`, que armazena os novos valores de origem e tamanho
nas propriedades apropriadas:

```swift
let centerRect = Rect(center: Point(x: 4.0, y: 4.0),
    size: Size(width: 3.0, height: 3.0))
// centerRect's origin is (2.5, 2.5) and its size is (3.0, 3.0)
```

<!--
  - test: `extensionsInitializers`

  ```swifttest
  -> let centerRect = Rect(center: Point(x: 4.0, y: 4.0),
        size: Size(width: 3.0, height: 3.0))
  /> centerRect's origin is (\(centerRect.origin.x), \(centerRect.origin.y)) and its size is (\(centerRect.size.width), \(centerRect.size.height))
  </ centerRect's origin is (2.5, 2.5) and its size is (3.0, 3.0)
  ```
-->

> Nota: Se você fornecer um novo inicializador com uma extension,
> continua sendo sua responsabilidade garantir que cada instância seja totalmente inicializada
> quando o inicializador terminar.

## Métodos

Extensions podem adicionar novos métodos de instância e métodos de tipo a tipos existentes.
O exemplo a seguir adiciona um novo método de instância chamado `repetitions` ao tipo `Int`:

```swift
extension Int {
    func repetitions(task: () -> Void) {
        for _ in 0..<self {
            task()
        }
    }
}
```

<!--
  - test: `extensionsInstanceMethods`

  ```swifttest
  -> extension Int {
        func repetitions(task: () -> Void) {
           for _ in 0..<self {
              task()
           }
        }
     }
  ```
-->

O método `repetitions(task:)` recebe um único argumento do tipo `() -> Void`,
que indica uma função sem parâmetros e que não retorna valor.

Depois de definir essa extension,
você pode chamar o método `repetitions(task:)` em qualquer inteiro
para executar uma tarefa essa quantidade de vezes:

```swift
3.repetitions {
    print("Hello!")
}
// Hello!
// Hello!
// Hello!
```

<!--
  - test: `extensionsInstanceMethods`

  ```swifttest
  -> 3.repetitions {
        print("Hello!")
     }
  </ Hello!
  </ Hello!
  </ Hello!
  ```
-->

### Métodos de instância mutantes

Métodos de instância adicionados com uma extension também podem modificar (ou *mutar*) a própria instância.
Métodos de struct e de enum que modificam `self` ou as propriedades dele
precisam marcar o método de instância como `mutating`,
assim como os métodos mutantes da implementação original.

O exemplo abaixo adiciona um novo método mutante chamado `square` ao tipo `Int` do Swift,
que eleva o valor original ao quadrado:

```swift
extension Int {
    mutating func square() {
        self = self * self
    }
}
var someInt = 3
someInt.square()
// someInt is now 9
```

<!--
  - test: `extensionsInstanceMethods`

  ```swifttest
  -> extension Int {
        mutating func square() {
           self = self * self
        }
     }
  -> var someInt = 3
  -> someInt.square()
  /> someInt is now \(someInt)
  </ someInt is now 9
  ```
-->

## Acessando valores com subscript

Extensions podem adicionar novos subscripts a um tipo existente.
Este exemplo adiciona um subscript de inteiro ao tipo `Int` embutido do Swift.
Este subscript `[n]` retorna o dígito decimal que está `n` posições
à direita do número:

- `123456789[0]` retorna `9`
- `123456789[1]` retorna `8`

…e assim por diante:

```swift
extension Int {
    subscript(digitIndex: Int) -> Int {
        var decimalBase = 1
        for _ in 0..<digitIndex {
            decimalBase *= 10
        }
        return (self / decimalBase) % 10
    }
}
746381295[0]
// returns 5
746381295[1]
// returns 9
746381295[2]
// returns 2
746381295[8]
// returns 7
```

<!--
  - test: `extensionsSubscripts`

  ```swifttest
  -> extension Int {
        subscript(digitIndex: Int) -> Int {
           var decimalBase = 1
           for _ in 0..<digitIndex {
              decimalBase *= 10
           }
           return (self / decimalBase) % 10
        }
     }
  >> let r0 =
  -> 746381295[0]
  /> returns \(r0)
  </ returns 5
  >> let r1 =
  -> 746381295[1]
  /> returns \(r1)
  </ returns 9
  >> let r2 =
  -> 746381295[2]
  /> returns \(r2)
  </ returns 2
  >> let r3 =
  -> 746381295[8]
  /> returns \(r3)
  </ returns 7
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

<!--
  TODO: Replace the for loop above with an exponent,
  if/when integer exponents land in the stdlib.
  Darwin's pow() function is only for floating point.
-->

Se o valor `Int` não tiver dígitos suficientes para o índice pedido,
a implementação do subscript retorna `0`,
como se o número tivesse sido preenchido com zeros à esquerda:

```swift
746381295[9]
// returns 0, as if you had requested:
0746381295[9]
```

<!--
  - test: `extensionsSubscripts`

  ```swifttest
  >> let r4 =
  -> 746381295[9]
  /> returns \(r4), as if you had requested:
  </ returns 0, as if you had requested:
  >> let r5 =
  -> 0746381295[9]
  ```
-->

<!--
  TODO: provide an explanation of this example
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

## Tipos aninhados

Extensions podem adicionar novos tipos aninhados a classes, structs e enums existentes:

```swift
extension Int {
    enum Kind {
        case negative, zero, positive
    }
    var kind: Kind {
        switch self {
        case 0:
            return .zero
        case let x where x > 0:
            return .positive
        default:
            return .negative
        }
    }
}
```

<!--
  - test: `extensionsNestedTypes`

  ```swifttest
  -> extension Int {
        enum Kind {
           case negative, zero, positive
        }
        var kind: Kind {
           switch self {
              case 0:
                 return .zero
              case let x where x > 0:
                 return .positive
              default:
                 return .negative
           }
        }
     }
  ```
-->

Este exemplo adiciona um novo enum aninhado a `Int`.
Esse enum, chamado `Kind`,
expressa o tipo de número que um inteiro específico representa.
Mais precisamente, ele expressa se o número é
negativo, zero ou positivo.

Este exemplo também adiciona a `Int` uma nova propriedade computada de instância,
chamada `kind`,
que retorna o caso de enum `Kind` apropriado para aquele inteiro.

Agora o enum aninhado pode ser usado com qualquer valor `Int`:

```swift
func printIntegerKinds(_ numbers: [Int]) {
    for number in numbers {
        switch number.kind {
        case .negative:
            print("- ", terminator: "")
        case .zero:
            print("0 ", terminator: "")
        case .positive:
            print("+ ", terminator: "")
        }
    }
    print("")
}
printIntegerKinds([3, 19, -27, 0, -6, 0, 7])
// Prints "+ + - 0 - 0 + ".
```

<!--
  - test: `extensionsNestedTypes`

  ```swifttest
  -> func printIntegerKinds(_ numbers: [Int]) {
        for number in numbers {
           switch number.kind {
              case .negative:
                 print("- ", terminator: "")
              case .zero:
                 print("0 ", terminator: "")
              case .positive:
                 print("+ ", terminator: "")
           }
        }
        print("")
     }
  -> printIntegerKinds([3, 19, -27, 0, -6, 0, 7])
  << + + - 0 - 0 +
  // Prints "+ + - 0 - 0 + ".
  ```
-->

<!--
  Workaround for rdar://26016325
-->

Esta função, `printIntegerKinds(_:)`,
recebe um array de valores `Int` como entrada e percorre esses valores em sequência.
Para cada inteiro do array,
a função considera a propriedade computada `kind` desse inteiro
e imprime uma descrição apropriada.

> Nota: `number.kind` já é conhecido como sendo do tipo `Int.Kind`.
> Por isso, todos os valores de caso de `Int.Kind`
> podem ser escritos na forma abreviada dentro da instrução `switch`,
> como `.negative` em vez de `Int.Kind.negative`.

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
