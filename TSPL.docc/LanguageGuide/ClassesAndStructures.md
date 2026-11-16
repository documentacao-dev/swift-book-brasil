# Structs e classes

Modele tipos personalizados que encapsulam dados.

*Structs* e *classes* são construções flexíveis e de uso geral,
que se tornam os blocos de construção do código do programa.
Você define propriedades e métodos para adicionar funcionalidades às suas structs e classes
usando a mesma sintaxe que usa para definir constantes, variáveis e funções.

Diferentemente de outras linguagens,
o Swift não exige que você crie arquivos separados de interface e de implementação
para structs e classes personalizadas.
No Swift, você define uma struct ou classe em um único arquivo,
e a interface externa dessa classe ou struct fica
automaticamente disponível para outros códigos usarem.

> Nota: Uma instância de classe é tradicionalmente conhecida como *objeto*.
> No entanto, as structs e as classes do Swift
> são bem mais parecidas em funcionalidade do que em outras linguagens,
> e grande parte deste capítulo descreve funcionalidades que se aplicam a
> instâncias de *um* tipo classe ou de *um* tipo struct.
> Por isso, usamos o termo mais geral *instância*.

## Comparando structs e classes

Structs e classes em Swift têm muitas coisas em comum.
Ambas podem:

- Definir propriedades para armazenar valores
- Definir métodos para fornecer funcionalidades
- Definir subscripts para dar acesso aos seus valores pela sintaxe de subscript
- Definir inicializadores para configurar seu estado inicial
- Ser estendidas para expandir sua funcionalidade além de uma implementação padrão
- Adotar protocolos para fornecer o comportamento padrão de determinado tipo

Para mais informações, veja
<doc:Properties>, <doc:Methods>, <doc:Subscripts>, <doc:Initialization>,
<doc:Extensions> e <doc:Protocols>.

Classes têm capacidades adicionais que as structs não têm:

- A herança permite que uma classe herde as características de outra.
- A conversão de tipos permite verificar e interpretar o tipo de uma instância de classe em tempo de execução.
- Os desinicializadores permitem que uma instância de classe libere os recursos que ela alocou.
- A contagem de referências permite mais de uma referência a uma mesma instância de classe.

Para mais informações, veja
<doc:Inheritance>, <doc:TypeCasting>, <doc:Deinitialization>
e <doc:AutomaticReferenceCounting>.

As capacidades adicionais das classes
têm como custo uma complexidade maior.
Como orientação geral,
prefira structs, porque são mais fáceis de entender,
e use classes quando forem apropriadas ou necessárias.
Na prática, isso significa que a maioria dos tipos personalizados que você definir
será de structs e enums.
Para uma comparação mais detalhada,
veja [Choosing Between Structures and Classes](https://developer.apple.com/documentation/swift/choosing_between_structures_and_classes).

> Nota: Classes e atores compartilham muitas das mesmas características e comportamentos.
> Para informações sobre atores, veja <doc:Concurrency>.

### Sintaxe de definição

Structs e classes têm uma sintaxe de definição semelhante.
Você introduz structs com a palavra-chave `struct`
e classes com a palavra-chave `class`.
Ambas colocam a definição inteira dentro de um par de chaves:

```swift
struct SomeStructure {
    // structure definition goes here
}
class SomeClass {
    // class definition goes here
}
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> struct SomeStructure {
        // structure definition goes here
     }
  -> class SomeClass {
        // class definition goes here
     }
  ```
-->

> Nota: Sempre que você define uma nova struct ou classe,
> você define um novo tipo do Swift.
> Dê aos tipos nomes em `UpperCamelCase`
> (como `SomeStructure` e `SomeClass` aqui)
> para combinar com a capitalização dos tipos padrão do Swift
> (como `String`, `Int` e `Bool`).
> Dê às propriedades e aos métodos nomes em `lowerCamelCase`
> (como `frameRate` e `incrementCount`)
> para diferenciá-los dos nomes de tipos.

Veja um exemplo de definição de struct e de definição de classe:

```swift
struct Resolution {
    var width = 0
    var height = 0
}
class VideoMode {
    var resolution = Resolution()
    var interlaced = false
    var frameRate = 0.0
    var name: String?
}
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> struct Resolution {
        var width = 0
        var height = 0
     }
  -> class VideoMode {
        var resolution = Resolution()
        var interlaced = false
        var frameRate = 0.0
        var name: String?
     }
  ```
-->

O exemplo acima define uma nova struct chamada `Resolution`,
para descrever uma resolução de exibição baseada em pixels.
Essa struct tem duas propriedades armazenadas chamadas `width` e `height`.
Propriedades armazenadas são constantes ou variáveis que ficam empacotadas
como parte da struct ou da classe.
O Swift infere que as duas propriedades são do tipo `Int`
porque são inicializadas com o valor inteiro `0`.

O exemplo acima também define uma nova classe chamada `VideoMode`,
para descrever um modo de vídeo específico para exibição.
Essa classe tem quatro propriedades armazenadas variáveis.
A primeira, `resolution`, é inicializada com uma nova instância da struct `Resolution`,
o que faz com que seu tipo seja inferido como `Resolution`.
Para as outras três propriedades,
novas instâncias de `VideoMode` serão inicializadas com
uma configuração `interlaced` de `false` (que significa “vídeo não entrelaçado”),
uma taxa de quadros de reprodução de `0.0`
e um valor `String` optional chamado `name`.
A propriedade `name` recebe automaticamente o valor padrão `nil`,
ou “nenhum valor de `name`”, porque é de um tipo optional.

### Instâncias de structs e de classes

As definições da struct `Resolution` e da classe `VideoMode`
apenas descrevem como serão uma `Resolution` e uma `VideoMode`.
Elas não descrevem uma resolução ou um modo de vídeo específico.
Para isso, você precisa criar uma instância da struct ou da classe.

A sintaxe para criar instâncias é muito parecida para structs e classes:

```swift
let someResolution = Resolution()
let someVideoMode = VideoMode()
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> let someResolution = Resolution()
  -> let someVideoMode = VideoMode()
  ```
-->

Structs e classes usam a sintaxe de inicializador para criar novas instâncias.
A forma mais simples da sintaxe de inicializador usa o nome do tipo da classe ou da struct
seguido de parênteses vazios, como `Resolution()` ou `VideoMode()`.
Isso cria uma nova instância da classe ou da struct,
com todas as propriedades inicializadas com seus valores padrão.
A inicialização de classes e de structs é descrita com mais detalhes
em <doc:Initialization>.

<!--
  TODO: note that you can only use the default constructor if you provide default values
  for all properties on a structure or class.
-->

### Acessando propriedades

Você pode acessar as propriedades de uma instância usando a *sintaxe de ponto*.
Na sintaxe de ponto, você escreve o nome da propriedade logo depois do nome da instância,
separado por um ponto (`.`), sem espaços:

```swift
print("The width of someResolution is \(someResolution.width)")
// Prints "The width of someResolution is 0".
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> print("The width of someResolution is \(someResolution.width)")
  <- The width of someResolution is 0
  ```
-->

Neste exemplo,
`someResolution.width` se refere à propriedade `width` de `someResolution`
e retorna seu valor inicial padrão, `0`.

Você pode acessar subpropriedades,
como a propriedade `width` dentro da propriedade `resolution` de uma `VideoMode`:

```swift
print("The width of someVideoMode is \(someVideoMode.resolution.width)")
// Prints "The width of someVideoMode is 0".
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> print("The width of someVideoMode is \(someVideoMode.resolution.width)")
  <- The width of someVideoMode is 0
  ```
-->

Você também pode usar a sintaxe de ponto para atribuir um novo valor a uma propriedade variável:

```swift
someVideoMode.resolution.width = 1280
print("The width of someVideoMode is now \(someVideoMode.resolution.width)")
// Prints "The width of someVideoMode is now 1280".
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> someVideoMode.resolution.width = 1280
  -> print("The width of someVideoMode is now \(someVideoMode.resolution.width)")
  <- The width of someVideoMode is now 1280
  ```
-->

### Inicializadores memberwise para tipos struct

Todas as structs têm um *inicializador memberwise* gerado automaticamente,
que você pode usar para inicializar as propriedades membro de novas instâncias de struct.
Os valores iniciais das propriedades da nova instância
podem ser passados ao inicializador memberwise pelo nome:

```swift
let vga = Resolution(width: 640, height: 480)
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> let vga = Resolution(width: 640, height: 480)
  ```
-->

Diferentemente das structs, instâncias de classe não recebem um inicializador memberwise padrão.
Os inicializadores são descritos com mais detalhes em <doc:Initialization>.

<!--
  - test: `classesDontHaveADefaultMemberwiseInitializer`

  ```swifttest
  -> class C { var x = 0, y = 0 }
  -> let c = C(x: 1, y: 1)
  !$ error: argument passed to call that takes no arguments
  !! let c = C(x: 1, y: 1)
  !!         ^~~~~~~~~~~~
  !!-
  ```
-->

## Structs e enums são tipos por valor

Um *tipo por valor* é um tipo cujo valor é *copiado*
quando é atribuído a uma variável ou constante,
ou quando é passado para uma função.

<!--
  Alternate definition:
  A type has value semantics when
  mutation of one variable of that type
  can never be observed through a different variable of the same type.
-->

Você já vem usando tipos por valor extensivamente nos capítulos anteriores.
De fato, todos os tipos básicos do Swift ---
inteiros, números de ponto flutuante, booleanos, strings, arrays e dicionários ---
são tipos por valor e, nos bastidores, são implementados como structs.

Todas as structs e enums no Swift são tipos por valor.
Isso significa que qualquer instância de struct ou de enum que você criar ---
e quaisquer tipos por valor que elas tenham como propriedades ---
é sempre copiada quando é passada pelo código.

> Nota: As coleções definidas pela biblioteca padrão do Swift,
> como arrays, dicionários e strings,
> usam uma otimização para reduzir o custo de desempenho da cópia.
> Em vez de fazer uma cópia imediatamente,
> essas coleções compartilham a memória onde os elementos estão armazenados
> entre a instância original e as cópias.
> Se uma das cópias da coleção for modificada,
> os elementos são copiados logo antes da modificação.
> O comportamento que você vê no código
> é sempre o mesmo que aconteceria se a cópia tivesse sido feita imediatamente.

Considere este exemplo, que usa a struct `Resolution` do exemplo anterior:

```swift
let hd = Resolution(width: 1920, height: 1080)
var cinema = hd
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> let hd = Resolution(width: 1920, height: 1080)
  -> var cinema = hd
  ```
-->

Este exemplo declara uma constante chamada `hd`
e a define como uma instância de `Resolution` inicializada com
a largura e a altura do vídeo Full HD
(1920 pixels de largura por 1080 pixels de altura).

Em seguida, declara uma variável chamada `cinema`
e a define com o valor atual de `hd`.
Como `Resolution` é uma struct,
é feita uma *cópia* da instância existente,
e essa nova cópia é atribuída a `cinema`.
Mesmo que `hd` e `cinema` agora tenham a mesma largura e altura,
elas são duas instâncias completamente diferentes nos bastidores.

Depois, a propriedade `width` de `cinema` é alterada para
a largura do padrão 2K, um pouco mais largo, usado na projeção de cinema digital
(2048 pixels de largura e 1080 pixels de altura):

```swift
cinema.width = 2048
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> cinema.width = 2048
  ```
-->

Verificar a propriedade `width` de `cinema`
mostra que ela de fato mudou para `2048`:

```swift
print("cinema is now \(cinema.width) pixels wide")
// Prints "cinema is now 2048 pixels wide".
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> print("cinema is now \(cinema.width) pixels wide")
  <- cinema is now 2048 pixels wide
  ```
-->

No entanto, a propriedade `width` da instância original `hd`
ainda tem o valor antigo, `1920`:

```swift
print("hd is still \(hd.width) pixels wide")
// Prints "hd is still 1920 pixels wide".
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> print("hd is still \(hd.width) pixels wide")
  <- hd is still 1920 pixels wide
  ```
-->

Quando `cinema` recebeu o valor atual de `hd`,
os *valores* armazenados em `hd` foram copiados para a nova instância `cinema`.
O resultado final foram duas instâncias totalmente separadas
que continham os mesmos valores numéricos.
Como são instâncias separadas,
definir a largura de `cinema` como `2048`
não afeta a largura armazenada em `hd`,
como mostra a figura abaixo:

![](sharedStateStruct)

O mesmo comportamento se aplica a enums:

```swift
enum CompassPoint {
    case north, south, east, west
    mutating func turnNorth() {
        self = .north
    }
}
var currentDirection = CompassPoint.west
let rememberedDirection = currentDirection
currentDirection.turnNorth()

print("The current direction is \(currentDirection)")
print("The remembered direction is \(rememberedDirection)")
// Prints "The current direction is north".
// Prints "The remembered direction is west".
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> enum CompassPoint {
        case north, south, east, west
        mutating func turnNorth() {
           self = .north
        }
     }
  -> var currentDirection = CompassPoint.west
  -> let rememberedDirection = currentDirection
  -> currentDirection.turnNorth()

  -> print("The current direction is \(currentDirection)")
  -> print("The remembered direction is \(rememberedDirection)")
  <- The current direction is north
  <- The remembered direction is west
  ```
-->

Quando `rememberedDirection` recebe o valor de `currentDirection`,
ele na verdade é definido como uma cópia desse valor.
Alterar o valor de `currentDirection` depois disso não afeta
a cópia do valor original que ficou armazenada em `rememberedDirection`.

<!--
  TODO: Should I give an example of passing a value type to a function here?
-->

## Classes são tipos por referência

Diferentemente dos tipos por valor, *tipos por referência* **não** são copiados
quando são atribuídos a uma variável ou constante,
ou quando são passados para uma função.
Em vez de uma cópia, é usada uma referência à mesma instância que já existe.

Veja um exemplo, usando a classe `VideoMode` definida acima:

```swift
let tenEighty = VideoMode()
tenEighty.resolution = hd
tenEighty.interlaced = true
tenEighty.name = "1080i"
tenEighty.frameRate = 25.0
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> let tenEighty = VideoMode()
  -> tenEighty.resolution = hd
  -> tenEighty.interlaced = true
  -> tenEighty.name = "1080i"
  -> tenEighty.frameRate = 25.0
  ```
-->

Este exemplo declara uma nova constante chamada `tenEighty`
e a define como uma referência a uma nova instância da classe `VideoMode`.
Ao modo de vídeo é atribuída uma cópia da resolução HD de `1920` por `1080` de antes.
Ele é configurado como entrelaçado,
seu nome é definido como `"1080i"`
e sua taxa de quadros é definida como `25.0` quadros por segundo.

Em seguida, `tenEighty` é atribuída a uma nova constante chamada `alsoTenEighty`,
e a taxa de quadros de `alsoTenEighty` é modificada:

```swift
let alsoTenEighty = tenEighty
alsoTenEighty.frameRate = 30.0
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> let alsoTenEighty = tenEighty
  -> alsoTenEighty.frameRate = 30.0
  ```
-->

Como classes são tipos por referência,
`tenEighty` e `alsoTenEighty` na verdade se referem à *mesma* instância de `VideoMode`.
Na prática, são apenas dois nomes diferentes para a mesma instância única,
como mostra a figura abaixo:

![](sharedStateClass)

Verificar a propriedade `frameRate` de `tenEighty`
mostra que ela reflete corretamente a nova taxa de quadros, `30.0`,
da instância subjacente de `VideoMode`:

```swift
print("The frameRate property of tenEighty is now \(tenEighty.frameRate)")
// Prints "The frameRate property of tenEighty is now 30.0".
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> print("The frameRate property of tenEighty is now \(tenEighty.frameRate)")
  <- The frameRate property of tenEighty is now 30.0
  ```
-->

Este exemplo também mostra como tipos por referência podem ser mais difíceis de entender.
Se `tenEighty` e `alsoTenEighty` ficassem distantes uma da outra no código do programa,
poderia ser difícil encontrar todas as formas como o modo de vídeo é alterado.
Onde quer que você use `tenEighty`,
também precisa pensar no código que usa `alsoTenEighty`, e vice-versa.
Já os tipos por valor são mais fáceis de entender,
porque todo o código que interage com o mesmo valor
fica próximo nos arquivos de código-fonte.

Observe que `tenEighty` e `alsoTenEighty` são declaradas como *constantes*,
e não como variáveis.
No entanto, você ainda pode alterar `tenEighty.frameRate` e `alsoTenEighty.frameRate`,
porque os valores das próprias constantes não mudam.
`tenEighty` e `alsoTenEighty` não “armazenam” a instância de `VideoMode` ---
em vez disso, as duas *se referem* a uma instância de `VideoMode` nos bastidores.
O que muda é a propriedade `frameRate` da `VideoMode` subjacente,
não os valores das constantes de referência para essa `VideoMode`.

<!--
  TODO: reiterate here that arrays and dictionaries are value types rather than reference types,
  and demonstrate what that means for the values they store
  when they themselves are value types or reference types.
  Also make a note about what this means for key copying,
  as per the swift-discuss email thread "Dictionaries and key copying"
  started by Alex Migicovsky on Mar 1 2014.
-->

<!--
  TODO: Add discussion about how
  a struct that has a member of some reference type
  is itself actually a reference type,
  and about how you can make a class that's a value type.
-->

### Operadores de identidade

Como classes são tipos por referência,
é possível que várias constantes e variáveis se refiram à
mesma instância única de uma classe nos bastidores.
(O mesmo não vale para structs e enums,
porque elas são sempre copiadas quando são atribuídas a uma constante ou variável,
ou passadas para uma função.)

<!--
  - test: `structuresDontSupportTheIdentityOperators`

  ```swifttest
  -> struct S { var x = 0, y = 0 }
  -> let s1 = S()
  -> let s2 = S()
  -> if s1 === s2 { print("s1 === s2") } else { print("s1 !== s2") }
  !$ error: argument type 'S' expected to be an instance of a class or class-constrained type
  !! if s1 === s2 { print("s1 === s2") } else { print("s1 !== s2") }
  !!       ^
  !$ error: argument type 'S' expected to be an instance of a class or class-constrained type
  !! if s1 === s2 { print("s1 === s2") } else { print("s1 !== s2") }
  !!       ^
  ```
-->

<!--
  - test: `enumerationsDontSupportTheIdentityOperators`

  ```swifttest
  -> enum E { case a, b }
  -> let e1 = E.a
  -> let e2 = E.b
  -> if e1 === e2 { print("e1 === e2") } else { print("e1 !== e2") }
  !$ error: argument type 'E' expected to be an instance of a class or class-constrained type
  !! if e1 === e2 { print("e1 === e2") } else { print("e1 !== e2") }
  !!       ^
  !$ error: argument type 'E' expected to be an instance of a class or class-constrained type
  !! if e1 === e2 { print("e1 === e2") } else { print("e1 !== e2") }
  !!       ^
  ```
-->

Às vezes é útil descobrir se duas constantes ou variáveis se referem
exatamente à mesma instância de uma classe.
Para isso, o Swift fornece dois operadores de identidade:

- Idêntico a (`===`)
- Não idêntico a (`!==`)

Use esses operadores para verificar se duas constantes ou variáveis se referem à mesma instância única:

```swift
if tenEighty === alsoTenEighty {
    print("tenEighty and alsoTenEighty refer to the same VideoMode instance.")
}
// Prints "tenEighty and alsoTenEighty refer to the same VideoMode instance."
```

<!--
  - test: `ClassesAndStructures`

  ```swifttest
  -> if tenEighty === alsoTenEighty {
        print("tenEighty and alsoTenEighty refer to the same VideoMode instance.")
     }
  <- tenEighty and alsoTenEighty refer to the same VideoMode instance.
  ```
-->

Observe que *idêntico a* (representado por três sinais de igual, ou `===`)
não significa o mesmo que *igual a* (representado por dois sinais de igual, ou `==`).
*Idêntico a* significa que duas constantes ou variáveis de tipo classe
se referem exatamente à mesma instância de classe.
*Igual a* significa que duas instâncias são consideradas iguais ou equivalentes em valor,
para algum significado apropriado de *igual*, definido pelo criador do tipo.

Ao definir suas próprias structs e classes personalizadas,
cabe a você decidir o que qualifica duas instâncias como iguais.
O processo de definir suas próprias implementações dos operadores `==` e `!=`
é descrito em <doc:AdvancedOperators#Equivalence-Operators>.

<!--
  - test: `classesDontGetEqualityByDefault`

  ```swifttest
  -> class C { var x = 0, y = 0 }
  -> let c1 = C()
  -> let c2 = C()
  -> if c1 == c2 { print("c1 == c2") } else { print("c1 != c2") }
  !$ error: binary operator '==' cannot be applied to two 'C' operands
  !! if c1 == c2 { print("c1 == c2") } else { print("c1 != c2") }
  !!    ~~ ^  ~~
  ```
-->

<!--
  - test: `structuresDontGetEqualityByDefault`

  ```swifttest
  -> struct S { var x = 0, y = 0 }
  -> let s1 = S()
  -> let s2 = S()
  -> if s1 == s2 { print("s1 == s2") } else { print("s1 != s2") }
  !$ error: binary operator '==' cannot be applied to two 'S' operands
  !! if s1 == s2 { print("s1 == s2") } else { print("s1 != s2") }
  !!    ~~ ^  ~~
  ```
-->

<!--
  TODO: This needs clarifying with regards to function references.
-->

### Ponteiros

Se você tem experiência com C, C++ ou Objective-C,
pode saber que essas linguagens usam *ponteiros* para se referir a endereços de memória.
Uma constante ou variável do Swift que se refere a uma instância de algum tipo por referência
é parecida com um ponteiro em C,
mas não é um ponteiro direto para um endereço de memória,
e não exige que você escreva um asterisco (`*`)
para indicar que está criando uma referência.
Em vez disso, essas referências são definidas como qualquer outra constante ou variável no Swift.
A biblioteca padrão do Swift fornece tipos de ponteiro e de buffer
que você pode usar caso precise interagir diretamente com ponteiros ---
veja [Gerenciamento manual de memória](https://developer.apple.com/documentation/swift/swift_standard_library/manual_memory_management).

<!--
  TODO: functions aren't "instances". This needs clarifying.
-->

<!--
  TODO: Add a justification here to say why this is a good thing.
-->

<!--
  QUESTION: what's the deal with tuples and reference types / value types?
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
