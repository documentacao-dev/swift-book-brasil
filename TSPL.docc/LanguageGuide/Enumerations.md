# Enums

Modele tipos personalizados que definem uma lista de valores possíveis.

Um *enum* define um tipo comum para um grupo de valores relacionados
e permite trabalhar com esses valores de forma segura em relação aos tipos no seu código.

Se você conhece C,
sabe que os enums em C associam nomes relacionados a um conjunto de valores inteiros.
Os enums em Swift são bem mais flexíveis
e não precisam fornecer um valor para cada caso do enum.
Se um valor (conhecido como *raw value*) for fornecido para cada caso do enum,
esse valor pode ser uma string, um caractere,
ou um valor de qualquer tipo inteiro ou de ponto flutuante.

Como alternativa, os casos do enum podem especificar
*associated values* de *qualquer* tipo, armazenados junto com cada caso,
assim como as uniões ou variantes fazem em outras linguagens.
Você pode definir um conjunto comum de casos relacionados como parte de um mesmo enum,
e cada um deles pode ter um conjunto diferente de valores de tipos apropriados associados a ele.

Os enums em Swift são tipos de primeira classe por direito próprio.
Elas adotam muitos recursos tradicionalmente exclusivos de classes,
como propriedades computadas, que fornecem informações adicionais sobre
o valor atual do enum,
e métodos de instância, que oferecem funcionalidades relacionadas
aos valores que o enum representa.
Enums também podem definir inicializadores para fornecer um caso inicial;
podem ser estendidos com uma extension para ampliar sua funcionalidade além da implementação original;
e podem adotar protocolos para fornecer funcionalidades padrão.

Para saber mais sobre esses recursos, veja
<doc:Properties>, <doc:Methods>, <doc:Initialization>,
<doc:Extensions> e <doc:Protocols>.

<!--
  TODO: this chapter should probably mention that enums without associated values
  are hashable and equatable by default (and what that means in practice)
-->

## Sintaxe de enum

Você introduz um enum com a palavra-chave `enum`
e coloca a definição inteira entre um par de chaves:

```swift
enum SomeEnumeration {
    // enumeration definition goes here
}
```

<!--
  - test: `enums`

  ```swifttest
  -> enum SomeEnumeration {
        // enumeration definition goes here
     }
  ```
-->

Veja um exemplo com os quatro pontos principais de uma bússola:

```swift
enum CompassPoint {
    case north
    case south
    case east
    case west
}
```

<!--
  - test: `enums`

  ```swifttest
  -> enum CompassPoint {
        case north
        case south
        case east
        case west
     }
  ```
-->

Os valores definidos em um enum
(como `north`, `south`, `east` e `west`)
são os *casos do enum*.
Você usa a palavra-chave `case` para introduzir novos casos do enum.

> Nota: Os casos de enum em Swift não recebem um valor inteiro por padrão,
> diferentemente de linguagens como C e Objective-C.
> No exemplo de `CompassPoint` acima,
> `north`, `south`, `east` e `west`
> não são implicitamente iguais a
> `0`, `1`, `2` e `3`.
> Em vez disso, cada caso do enum é um valor por direito próprio,
> com o tipo explicitamente definido como `CompassPoint`.

Vários casos podem aparecer em uma mesma linha, separados por vírgulas:

```swift
enum Planet {
    case mercury, venus, earth, mars, jupiter, saturn, uranus, neptune
}
```

<!--
  - test: `enums`

  ```swifttest
  -> enum Planet {
        case mercury, venus, earth, mars, jupiter, saturn, uranus, neptune
     }
  ```
-->

Cada definição de enum cria um novo tipo.
Como outros tipos em Swift, os nomes delas
(como `CompassPoint` e `Planet`)
começam com letra maiúscula.
Dê aos tipos enum nomes no singular, e não no plural,
para que eles se leiam como algo autoevidente:

```swift
var directionToHead = CompassPoint.west
```

<!--
  - test: `enums`

  ```swifttest
  -> var directionToHead = CompassPoint.west
  ```
-->

O tipo de `directionToHead` é inferido
quando a variável é inicializada com um dos valores possíveis de `CompassPoint`.
Depois que `directionToHead` é declarada como `CompassPoint`,
você pode atribuir a ela outro valor de `CompassPoint` usando uma sintaxe de ponto mais curta:

```swift
directionToHead = .east
```

<!--
  - test: `enums`

  ```swifttest
  -> directionToHead = .east
  ```
-->

O tipo de `directionToHead` já é conhecido,
então você pode omitir o tipo ao atribuir o valor.
Isso deixa o código muito legível quando você trabalha com valores de enum de tipo explícito.

## Comparando valores de enum com uma instrução switch

Você pode comparar valores individuais de enum com uma instrução `switch`:

```swift
directionToHead = .south
switch directionToHead {
case .north:
    print("Lots of planets have a north")
case .south:
    print("Watch out for penguins")
case .east:
    print("Where the sun rises")
case .west:
    print("Where the skies are blue")
}
// Prints "Watch out for penguins".
```

<!--
  - test: `enums`

  ```swifttest
  -> directionToHead = .south
  -> switch directionToHead {
        case .north:
           print("Lots of planets have a north")
        case .south:
           print("Watch out for penguins")
        case .east:
           print("Where the sun rises")
        case .west:
           print("Where the skies are blue")
     }
  <- Watch out for penguins
  ```
-->

Você pode ler este código assim:

“Considere o valor de `directionToHead`.
No caso em que ele é igual a `.north`,
imprima `"Lots of planets have a north"`.
No caso em que ele é igual a `.south`,
imprima `"Watch out for penguins"`.”

…e assim por diante.

Como descrito em <doc:ControlFlow>,
uma instrução `switch` precisa ser exaustiva ao considerar os casos de um enum.
Se o `case` para `.west` for omitido,
este código não compila,
porque não considera a lista completa de casos de `CompassPoint`.
Exigir exaustividade garante que casos de enum não sejam omitidos por acidente.

Quando não for adequado fornecer um `case` para cada caso do enum,
você pode fornecer um caso `default` para cobrir os casos que não foram tratados explicitamente:

```swift
let somePlanet = Planet.earth
switch somePlanet {
case .earth:
    print("Mostly harmless")
default:
    print("Not a safe place for humans")
}
// Prints "Mostly harmless".
```

<!--
  - test: `enums`

  ```swifttest
  -> let somePlanet = Planet.earth
  -> switch somePlanet {
        case .earth:
           print("Mostly harmless")
        default:
           print("Not a safe place for humans")
     }
  <- Mostly harmless
  ```
-->

## Percorrendo os casos do enum

Em alguns enums,
é útil ter uma coleção com todos os casos do enum.
Você habilita isso
escrevendo `: CaseIterable` depois do nome do enum.
O Swift expõe uma coleção com todos os casos
como a propriedade `allCases` do tipo do enum.
Veja um exemplo:

```swift
enum Beverage: CaseIterable {
    case coffee, tea, juice
}
let numberOfChoices = Beverage.allCases.count
print("\(numberOfChoices) beverages available")
// Prints "3 beverages available".
```

<!--
  - test: `enums`

  ```swifttest
  -> enum Beverage: CaseIterable {
         case coffee, tea, juice
     }
  -> let numberOfChoices = Beverage.allCases.count
  -> print("\(numberOfChoices) beverages available")
  <- 3 beverages available
  ```
-->

No exemplo acima,
você escreve `Beverage.allCases` para acessar uma coleção
que contém todos os casos do enum `Beverage`.
Você pode usar `allCases` como qualquer outra coleção:
os elementos da coleção são instâncias do tipo do enum,
então, neste caso, são valores de `Beverage`.
O exemplo acima conta quantos casos existem,
e o exemplo abaixo usa um laço `for`-`in` para percorrer todos os casos.

```swift
for beverage in Beverage.allCases {
    print(beverage)
}
// coffee
// tea
// juice
```

<!--
  - test: `enums`

  ```swifttest
  -> for beverage in Beverage.allCases {
         print(beverage)
     }
  << coffee
  << tea
  << juice
  // coffee
  // tea
  // juice
  ```
-->

A sintaxe usada nos exemplos acima
marca o enum como em conformidade com o protocolo
[`CaseIterable`](https://developer.apple.com/documentation/swift/caseiterable).
Para saber mais sobre protocolos, veja <doc:Protocols>.

## Associated values

Os exemplos da seção anterior mostram que os casos de um enum são
valores definidos (e tipados) por direito próprio.
Você pode atribuir a uma constante ou variável `Planet.earth`
e verificar esse valor depois.
No entanto, às vezes é útil armazenar
valores de outros tipos junto com esses valores de caso.
Essa informação adicional é chamada de *associated value*,
e ela varia cada vez que você usa esse caso como valor no seu código.

Você pode definir enums em Swift para armazenar associated values de qualquer tipo,
e os tipos de valor podem ser diferentes para cada caso do enum, se necessário.
Enums como esses são conhecidos como
*discriminated unions*, *tagged unions* ou *variants*
em outras linguagens de programação.

Por exemplo, suponha que um sistema de controle de estoque precise
acompanhar produtos por dois tipos diferentes de código de barras.
Alguns produtos têm códigos de barras 1D no formato UPC,
que usa os números de `0` a `9`.
Cada código de barras tem um dígito de sistema numérico,
seguido de cinco dígitos do código do fabricante e cinco dígitos do código do produto.
Em seguida vem um dígito verificador, que confirma que o código foi lido corretamente:

![](barcode_UPC)

Outros produtos têm códigos de barras 2D no formato de QR code,
que podem usar qualquer caractere ISO 8859-1
e podem codificar uma string de até 2.953 caracteres:

![](barcode_QR)

Para um sistema de controle de estoque, é conveniente armazenar códigos UPC
como uma tupla de quatro inteiros,
e códigos QR como uma string de qualquer tamanho.

Em Swift, um enum para definir códigos de barras de produtos de qualquer um dos dois tipos pode ser assim:

```swift
enum Barcode {
    case upc(Int, Int, Int, Int)
    case qrCode(String)
}
```

<!--
  - test: `enums`

  ```swifttest
  -> enum Barcode {
        case upc(Int, Int, Int, Int)
        case qrCode(String)
     }
  ```
-->

Você pode ler isso assim:

“Defina um tipo enum chamado `Barcode`,
que pode receber um valor `upc`
com um associated value do tipo (`Int`, `Int`, `Int`, `Int`),
ou um valor `qrCode` com um associated value do tipo `String`.”

Essa definição não fornece nenhum valor real de `Int` ou `String` ---
ela apenas define o *tipo* dos associated values
que as constantes e variáveis de `Barcode` podem armazenar
quando são iguais a `Barcode.upc` ou `Barcode.qrCode`.

Depois, você pode criar novos códigos de barras usando qualquer um dos tipos:

```swift
var productBarcode = Barcode.upc(8, 85909, 51226, 3)
```

<!--
  - test: `enums`

  ```swifttest
  -> var productBarcode = Barcode.upc(8, 85909, 51226, 3)
  ```
-->

Este exemplo cria uma nova variável chamada `productBarcode`
e atribui a ela o valor `Barcode.upc`
com uma tupla como associated value, `(8, 85909, 51226, 3)`.

Você pode atribuir ao mesmo produto um tipo diferente de código de barras:

```swift
productBarcode = .qrCode("ABCDEFGHIJKLMNOP")
```

<!--
  - test: `enums`

  ```swifttest
  -> productBarcode = .qrCode("ABCDEFGHIJKLMNOP")
  ```
-->

Nesse momento,
o `Barcode.upc` original e seus valores inteiros são substituídos pelo
novo `Barcode.qrCode` e pelo valor string dele.
Constantes e variáveis do tipo `Barcode` podem armazenar um `.upc` ou um `.qrCode`
(junto com os respectivos associated values),
mas só podem armazenar um deles por vez.

Você pode verificar os diferentes tipos de código de barras usando uma instrução switch,
parecido com o exemplo em
<doc:Enumerations#Matching-Enumeration-Values-with-a-Switch-Statement>.
Desta vez, porém,
os associated values são extraídos como parte da instrução switch.
Você extrai cada associated value como uma constante (com o prefixo `let`)
ou uma variável (com o prefixo `var`)
para usar dentro do corpo do `case` do switch:

```swift
switch productBarcode {
case .upc(let numberSystem, let manufacturer, let product, let check):
    print("UPC: \(numberSystem), \(manufacturer), \(product), \(check).")
case .qrCode(let productCode):
    print("QR code: \(productCode).")
}
// Prints "QR code: ABCDEFGHIJKLMNOP."
```

<!--
  - test: `enums`

  ```swifttest
  -> switch productBarcode {
        case .upc(let numberSystem, let manufacturer, let product, let check):
           print("UPC: \(numberSystem), \(manufacturer), \(product), \(check).")
        case .qrCode(let productCode):
           print("QR code: \(productCode).")
     }
  <- QR code: ABCDEFGHIJKLMNOP.
  ```
-->

Se todos os associated values de um caso do enum
forem extraídos como constantes, ou se todos forem extraídos como variáveis,
você pode colocar uma única anotação `let` ou `var` antes do nome do caso, para deixar o código mais curto:

```swift
switch productBarcode {
case let .upc(numberSystem, manufacturer, product, check):
    print("UPC : \(numberSystem), \(manufacturer), \(product), \(check).")
case let .qrCode(productCode):
    print("QR code: \(productCode).")
}
// Prints "QR code: ABCDEFGHIJKLMNOP."
```

<!--
  - test: `enums`

  ```swifttest
  -> switch productBarcode {
        case let .upc(numberSystem, manufacturer, product, check):
           print("UPC : \(numberSystem), \(manufacturer), \(product), \(check).")
        case let .qrCode(productCode):
           print("QR code: \(productCode).")
     }
  <- QR code: ABCDEFGHIJKLMNOP.
  ```
-->

Quando você compara apenas um caso de um enum ---
por exemplo,
para extrair o associated value dele ---
você pode usar uma instrução `if`-`case`
em vez de escrever um switch completo.
Veja como fica:

```swift
if case .qrCode(let productCode) = productBarcode {
    print("QR code: \(productCode).")
}
```

Assim como na instrução switch anterior,
a variável `productBarcode` é comparada com
o padrão `.qrCode(let productCode)` aqui.
E, como no case do switch,
o `let` extrai o associated value como uma constante.
Para mais informações sobre instruções `if`-`case`,
veja <doc:ControlFlow#Patterns>.

## Raw values

O exemplo do código de barras em <doc:Enumerations#Associated-Values>
mostra como os casos de um enum podem declarar que armazenam
associated values de tipos diferentes.
Como alternativa aos associated values,
os casos de enum podem vir preenchidos com valores padrão
(chamados de *raw values*),
que são todos do mesmo tipo.

Veja um exemplo que armazena valores ASCII brutos junto com casos de enum nomeados:

```swift
enum ASCIIControlCharacter: Character {
    case tab = "\t"
    case lineFeed = "\n"
    case carriageReturn = "\r"
}
```

<!--
  - test: `rawValues`

  ```swifttest
  -> enum ASCIIControlCharacter: Character {
        case tab = "\t"
        case lineFeed = "\n"
        case carriageReturn = "\r"
     }
  ```
-->

Aqui, os raw values de um enum chamado `ASCIIControlCharacter`
são definidos como do tipo `Character`,
e recebem alguns dos caracteres de controle ASCII mais comuns.
Valores de `Character` são descritos em <doc:StringsAndCharacters>.

Raw values podem ser
strings, caracteres ou qualquer tipo numérico inteiro ou de ponto flutuante.
Cada raw value precisa ser único dentro da declaração do enum.

Embora você possa usar tanto raw values quanto associated values
para dar a um enum um valor adicional,
é importante entender a diferença entre eles.
Você escolhe o raw value de um caso do enum
quando define esse caso no seu código,
como os três códigos ASCII acima.
O raw value de um caso específico é sempre o mesmo.
Já os associated values você escolhe ao criar uma nova constante ou variável
usando um dos casos do enum,
e pode escolher um valor diferente cada vez que fizer isso.

### Raw values atribuídos implicitamente

Quando você trabalha com enums que armazenam raw values inteiros ou string,
não precisa atribuir explicitamente um raw value a cada caso.
Quando não atribui, o Swift define os valores automaticamente.

Por exemplo, quando raw values são inteiros,
o valor implícito de cada caso é um a mais que o do caso anterior.
Se o primeiro caso não tiver um valor definido, o valor dele é `0`.

O enum abaixo é um refinamento do enum `Planet` visto antes,
com raw values inteiros para representar a ordem de cada planeta a partir do sol:

```swift
enum Planet: Int {
    case mercury = 1, venus, earth, mars, jupiter, saturn, uranus, neptune
}
```

<!--
  - test: `rawValues`

  ```swifttest
  -> enum Planet: Int {
        case mercury = 1, venus, earth, mars, jupiter, saturn, uranus, neptune
     }
  ```
-->

No exemplo acima,
`Planet.mercury` tem o raw value explícito `1`,
`Planet.venus` tem o raw value implícito `2`, e assim por diante.

Quando strings são usadas como raw values,
o valor implícito de cada caso é o texto do nome desse caso.

O enum abaixo é um refinamento do enum `CompassPoint` visto antes,
com raw values string para representar o nome de cada direção:

```swift
enum CompassPoint: String {
    case north, south, east, west
}
```

<!--
  - test: `rawValues`

  ```swifttest
  -> enum CompassPoint: String {
        case north, south, east, west
     }
  ```
-->

No exemplo acima,
`CompassPoint.south` tem o raw value implícito `"south"`, e assim por diante.

Você acessa o raw value de um caso do enum pela propriedade `rawValue`:

```swift
let earthsOrder = Planet.earth.rawValue
// earthsOrder is 3

let sunsetDirection = CompassPoint.west.rawValue
// sunsetDirection is "west"
```

<!--
  - test: `rawValues`

  ```swifttest
  -> let earthsOrder = Planet.earth.rawValue
  /> earthsOrder is \(earthsOrder)
  </ earthsOrder is 3

  -> let sunsetDirection = CompassPoint.west.rawValue
  /> sunsetDirection is \"\(sunsetDirection)\"
  </ sunsetDirection is "west"
  ```
-->

### Inicializando a partir de um raw value

Se você definir um enum com um tipo de raw value,
o enum recebe automaticamente um inicializador
que aceita um valor do tipo do raw value (como um parâmetro chamado `rawValue`)
e retorna um caso do enum ou `nil`.
Você pode usar esse inicializador para tentar criar uma nova instância do enum.

Este exemplo identifica Urano pelo seu raw value `7`:

```swift
let possiblePlanet = Planet(rawValue: 7)
// possiblePlanet is of type Planet? and equals Planet.uranus
```

<!--
  - test: `rawValues`

  ```swifttest
  -> let possiblePlanet = Planet(rawValue: 7)
  >> print(type(of: possiblePlanet))
  << Optional<Planet>
  >> assert(possiblePlanet == .uranus)
  // possiblePlanet is of type Planet? and equals Planet.uranus
  ```
-->

No entanto, nem todo valor `Int` possível vai encontrar um planeta correspondente.
Por isso, o inicializador de raw value sempre retorna um caso de enum *optional*.
No exemplo acima, `possiblePlanet` é do tipo `Planet?`,
ou “`Planet` optional.”

> Nota: O inicializador de raw value é um inicializador falhável,
> porque nem todo raw value vai retornar um caso do enum.
> Para mais informações, veja <doc:Declarations#Failable-Initializers>.

Se você tentar encontrar um planeta na posição `11`,
o `Planet` optional retornado pelo inicializador de raw value será `nil`:

```swift
let positionToFind = 11
if let somePlanet = Planet(rawValue: positionToFind) {
    switch somePlanet {
    case .earth:
        print("Mostly harmless")
    default:
        print("Not a safe place for humans")
    }
} else {
    print("There isn't a planet at position \(positionToFind)")
}
// Prints "There isn't a planet at position 11".
```

<!--
  - test: `rawValues`

  ```swifttest
  -> let positionToFind = 11
  -> if let somePlanet = Planet(rawValue: positionToFind) {
        switch somePlanet {
           case .earth:
              print("Mostly harmless")
           default:
              print("Not a safe place for humans")
        }
     } else {
        print("There isn't a planet at position \(positionToFind)")
     }
  <- There isn't a planet at position 11
  ```
-->

Este exemplo usa optional binding para tentar acessar um planeta com raw value `11`.
A instrução `if let somePlanet = Planet(rawValue: 11)` cria um `Planet` optional
e atribui a `somePlanet` o valor desse `Planet` optional, se ele puder ser obtido.
Neste caso, não é possível obter um planeta na posição `11`,
então o ramo `else` é executado.

<!--
  TODO: Switch around the order of this chapter so that all of the non-union stuff
  is together, and the union bits (aka Associated Values) come last.
-->

## Enums recursivos

Um *enum recursivo* é um enum
que tem outra instância do próprio enum
como associated value de um ou mais casos.
Você indica que um caso do enum é recursivo
escrevendo `indirect` antes dele,
o que diz ao compilador para inserir a camada de indireção necessária.

Por exemplo, veja um enum que armazena expressões aritméticas simples:

```swift
enum ArithmeticExpression {
    case number(Int)
    indirect case addition(ArithmeticExpression, ArithmeticExpression)
    indirect case multiplication(ArithmeticExpression, ArithmeticExpression)
}
```

<!--
  - test: `recursive-enum-intro`

  ```swifttest
  -> enum ArithmeticExpression {
         case number(Int)
         indirect case addition(ArithmeticExpression, ArithmeticExpression)
         indirect case multiplication(ArithmeticExpression, ArithmeticExpression)
     }
  ```
-->

Você também pode escrever `indirect` antes do início do enum
para habilitar a indireção em todos os casos do enum que têm associated value:

```swift
indirect enum ArithmeticExpression {
    case number(Int)
    case addition(ArithmeticExpression, ArithmeticExpression)
    case multiplication(ArithmeticExpression, ArithmeticExpression)
}
```

<!--
  - test: `recursive-enum`

  ```swifttest
  -> indirect enum ArithmeticExpression {
         case number(Int)
         case addition(ArithmeticExpression, ArithmeticExpression)
         case multiplication(ArithmeticExpression, ArithmeticExpression)
     }
  ```
-->

Esse enum pode armazenar três tipos de expressões aritméticas:
um número simples,
a soma de duas expressões
e a multiplicação de duas expressões.
Os casos `addition` e `multiplication` têm associated values
que também são expressões aritméticas ---
esses associated values tornam possível aninhar expressões.
Por exemplo, a expressão `(5 + 4) * 2`
tem um número do lado direito da multiplicação
e outra expressão do lado esquerdo.
Como os dados são aninhados,
o enum usado para armazená-los também precisa aceitar aninhamento ---
ou seja, o enum precisa ser recursivo.
O código abaixo mostra o enum recursivo `ArithmeticExpression`
sendo criado para `(5 + 4) * 2`:

```swift
let five = ArithmeticExpression.number(5)
let four = ArithmeticExpression.number(4)
let sum = ArithmeticExpression.addition(five, four)
let product = ArithmeticExpression.multiplication(sum, ArithmeticExpression.number(2))
```

<!--
  - test: `recursive-enum`

  ```swifttest
  -> let five = ArithmeticExpression.number(5)
  -> let four = ArithmeticExpression.number(4)
  -> let sum = ArithmeticExpression.addition(five, four)
  -> let product = ArithmeticExpression.multiplication(sum, ArithmeticExpression.number(2))
  ```
-->

Uma função recursiva é uma forma direta
de trabalhar com dados que têm estrutura recursiva.
Por exemplo, veja uma função que avalia uma expressão aritmética:

```swift
func evaluate(_ expression: ArithmeticExpression) -> Int {
    switch expression {
    case let .number(value):
        return value
    case let .addition(left, right):
        return evaluate(left) + evaluate(right)
    case let .multiplication(left, right):
        return evaluate(left) * evaluate(right)
    }
}

print(evaluate(product))
// Prints "18".
```

<!--
  - test: `recursive-enum`

  ```swifttest
  -> func evaluate(_ expression: ArithmeticExpression) -> Int {
         switch expression {
             case let .number(value):
                 return value
             case let .addition(left, right):
                 return evaluate(left) + evaluate(right)
             case let .multiplication(left, right):
                 return evaluate(left) * evaluate(right)
         }
     }

  -> print(evaluate(product))
  <- 18
  ```
-->

Essa função avalia um número simples
simplesmente retornando o associated value.
Ela avalia uma soma ou multiplicação
avaliando a expressão do lado esquerdo,
avaliando a expressão do lado direito
e, depois, somando ou multiplicando os dois resultados.

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
