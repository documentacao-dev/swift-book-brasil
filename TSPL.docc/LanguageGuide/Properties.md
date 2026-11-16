# Propriedades

Acesse valores armazenados e calculados que fazem parte de uma instância ou de um tipo.

*Propriedades* associam valores a uma classe, struct ou enum específico.
Propriedades armazenadas guardam valores constantes e variáveis como parte de uma instância,
enquanto propriedades computadas calculam um valor (em vez de armazená-lo).
Classes, structs e enums oferecem propriedades computadas.
Propriedades armazenadas são oferecidas apenas por classes e structs.

<!--
  - test: `enumerationsCantProvideStoredProperties`

  ```swifttest
  -> enum E { case a, b; var x = 0 }
  !$ error: enums must not contain stored properties
  !! enum E { case a, b; var x = 0 }
  !! ^
  ```
-->

Propriedades armazenadas e computadas costumam estar associadas a instâncias de um tipo específico.
No entanto, propriedades também podem estar associadas ao próprio tipo.
Essas propriedades são chamadas de propriedades de tipo.

Além disso, você pode definir observadores de propriedade para monitorar mudanças no valor de uma propriedade,
e responder a essas mudanças com ações personalizadas.
Observadores de propriedade podem ser adicionados a propriedades armazenadas que você mesmo define,
e também a propriedades que uma subclasse herda da sua superclasse.

<!--
  - test: `propertyObserverIntroClaims`

  ```swifttest
  -> class C {
        var x: Int = 0 {
           willSet { print("C willSet x to \(newValue)") }
           didSet { print("C didSet x from \(oldValue)") }
        }
     }
  -> class D: C {
        override var x: Int {
           willSet { print("D willSet x to \(newValue)") }
           didSet { print("D didSet x from \(oldValue)") }
        }
     }
  -> var c = C(); c.x = 42
  <- C willSet x to 42
  <- C didSet x from 0
  -> var d = D(); d.x = 42
  <- D willSet x to 42
  <- C willSet x to 42
  <- C didSet x from 0
  <- D didSet x from 0
  ```
-->

Você também pode usar um property wrapper
para reaproveitar código nos getters e setters de várias propriedades.

## Propriedades armazenadas

Na forma mais simples, uma propriedade armazenada é uma constante ou variável
que fica guardada como parte de uma instância de uma classe ou struct específica.
Propriedades armazenadas podem ser
*propriedades armazenadas variáveis* (introduzidas pela palavra-chave `var`)
ou *propriedades armazenadas constantes* (introduzidas pela palavra-chave `let`).

Você pode fornecer um valor padrão para uma propriedade armazenada como parte da sua definição,
conforme descrito em <doc:Initialization#Default-Property-Values>.
Você também pode definir e modificar o valor inicial de uma propriedade armazenada durante a inicialização.
Isso vale até para propriedades armazenadas constantes,
conforme descrito em <doc:Initialization#Assigning-Constant-Properties-During-Initialization>.

O exemplo abaixo define uma struct chamada `FixedLengthRange`,
que descreve um intervalo de inteiros
cujo tamanho não pode ser alterado depois de criado:

```swift
struct FixedLengthRange {
    var firstValue: Int
    let length: Int
}
var rangeOfThreeItems = FixedLengthRange(firstValue: 0, length: 3)
// the range represents integer values 0, 1, and 2
rangeOfThreeItems.firstValue = 6
// the range now represents integer values 6, 7, and 8
```

<!--
  - test: `storedProperties, storedProperties-err`

  ```swifttest
  -> struct FixedLengthRange {
        var firstValue: Int
        let length: Int
     }
  -> var rangeOfThreeItems = FixedLengthRange(firstValue: 0, length: 3)
  // the range represents integer values 0, 1, and 2
  -> rangeOfThreeItems.firstValue = 6
  // the range now represents integer values 6, 7, and 8
  ```
-->

Instâncias de `FixedLengthRange` têm
uma propriedade armazenada variável chamada `firstValue`
e uma propriedade armazenada constante chamada `length`.
No exemplo acima, `length` é inicializada quando o novo intervalo é criado
e não pode mudar depois, porque é uma propriedade constante.

### Propriedades armazenadas de instâncias constantes de struct

Se você criar uma instância de struct
e atribuí-la a uma constante,
não poderá modificar as propriedades dessa instância,
mesmo que elas tenham sido declaradas como propriedades variáveis:

```swift
let rangeOfFourItems = FixedLengthRange(firstValue: 0, length: 4)
// this range represents integer values 0, 1, 2, and 3
rangeOfFourItems.firstValue = 6
// this will report an error, even though firstValue is a variable property
```

<!--
  - test: `storedProperties-err`

  ```swifttest
  -> let rangeOfFourItems = FixedLengthRange(firstValue: 0, length: 4)
  // this range represents integer values 0, 1, 2, and 3
  -> rangeOfFourItems.firstValue = 6
  !$ error: cannot assign to property: 'rangeOfFourItems' is a 'let' constant
  !! rangeOfFourItems.firstValue = 6
  !! ~~~~~~~~~~~~~~~~ ^
  !$ note: change 'let' to 'var' to make it mutable
  !! let rangeOfFourItems = FixedLengthRange(firstValue: 0, length: 4)
  !! ^~~
  !! var
  // this will report an error, even though firstValue is a variable property
  ```
-->

Como `rangeOfFourItems` é declarada como constante (com a palavra-chave `let`),
não é possível alterar a propriedade `firstValue` dela,
mesmo que `firstValue` seja uma propriedade variável.

Esse comportamento se deve ao fato de structs serem *tipos de valor*.
Quando uma instância de tipo de valor é marcada como constante,
todas as suas propriedades também são.

O mesmo não vale para classes, que são *tipos de referência*.
Se você atribuir uma instância de tipo de referência a uma constante,
ainda poderá alterar as propriedades variáveis dessa instância.

<!--
  TODO: this explanation could still do to be improved.
-->

### Propriedades armazenadas lazy

<!--
  QUESTION: is this section too complex for this point in the book?
  Should it go in the Default Property Values section of Initialization instead?
-->

Uma *propriedade armazenada lazy* é uma propriedade cujo valor inicial só é calculado
na primeira vez que ela é usada.
Você indica uma propriedade armazenada lazy escrevendo
o modificador `lazy` antes da declaração.

> Nota: Você deve sempre declarar uma propriedade lazy como variável (com a palavra-chave `var`),
> porque o valor inicial dela pode não ser obtido até
> depois que a inicialização da instância terminar.
> Propriedades constantes precisam ter um valor *antes* de a inicialização terminar,
> por isso não podem ser declaradas como lazy.

<!--
  - test: `lazyPropertiesMustAlwaysBeVariables`

  ```swifttest
  -> class C { lazy let x = 0 }
  !$ error: 'lazy' cannot be used on a let
  !! class C { lazy let x = 0 }
  !! ^~~~~
  !!-
  ```
-->

Propriedades lazy são úteis quando o valor inicial de uma propriedade
depende de fatores externos cujos valores só são conhecidos
depois que a inicialização da instância termina.
Também são úteis quando o valor inicial de uma propriedade exige
uma configuração complexa ou custosa, que não deve ser feita
a menos que ou até que seja realmente necessária.

<!--
  TODO: add a note that if you assign a value to a lazy property before first access,
  the initial value you give in your code will be ignored.
-->

O exemplo abaixo usa uma propriedade armazenada lazy para evitar
a inicialização desnecessária de uma classe complexa.
Ele define duas classes chamadas `DataImporter` e `DataManager`,
e nenhuma das duas é mostrada por completo:

```swift
class DataImporter {
    /*
    DataImporter is a class to import data from an external file.
    The class is assumed to take a nontrivial amount of time to initialize.
    */
    var filename = "data.txt"
    // the DataImporter class would provide data importing functionality here
}

class DataManager {
    lazy var importer = DataImporter()
    var data: [String] = []
    // the DataManager class would provide data management functionality here
}

let manager = DataManager()
manager.data.append("Some data")
manager.data.append("Some more data")
// the DataImporter instance for the importer property hasn't yet been created
```

<!--
  - test: `lazyProperties`

  ```swifttest
  -> class DataImporter {
        /*
        DataImporter is a class to import data from an external file.
        The class is assumed to take a nontrivial amount of time to initialize.
        */
        var filename = "data.txt"
        // the DataImporter class would provide data importing functionality here
  >>    init() {
  >>       print("the DataImporter instance for the importer property has now been created")
  >>    }
     }

  -> class DataManager {
        lazy var importer = DataImporter()
        var data: [String] = []
        // the DataManager class would provide data management functionality here
     }

  -> let manager = DataManager()
  -> manager.data.append("Some data")
  -> manager.data.append("Some more data")
  // the DataImporter instance for the importer property hasn't yet been created
  ```
-->

A classe `DataManager` tem uma propriedade armazenada chamada `data`,
que é inicializada com um novo array vazio de valores `String`.
Embora o restante da funcionalidade não seja mostrado,
a finalidade dessa classe `DataManager` é gerenciar e dar acesso
a esse array de dados `String`.

Parte da funcionalidade da classe `DataManager`
é a capacidade de importar dados de um arquivo.
Essa funcionalidade é oferecida pela classe `DataImporter`,
que supostamente leva um tempo considerável para ser inicializada.
Isso pode acontecer porque uma instância de `DataImporter` precisa abrir um arquivo
e ler o conteúdo dele para a memória quando é inicializada.

Como é possível que uma instância de `DataManager` gerencie seus dados
sem nunca importar dados de um arquivo,
`DataManager` não cria uma nova instância de `DataImporter`
quando ele mesmo é criado.
Em vez disso, faz mais sentido criar a instância de `DataImporter`
se e quando ela for usada pela primeira vez.

Como está marcada com o modificador `lazy`,
a instância de `DataImporter` da propriedade `importer`
só é criada quando `importer` é acessada pela primeira vez,
como quando sua propriedade `filename` é consultada:

```swift
print(manager.importer.filename)
// the DataImporter instance for the importer property has now been created
// Prints "data.txt".
```

<!--
  - test: `lazyProperties`

  ```swifttest
  -> print(manager.importer.filename)
  </ the DataImporter instance for the importer property has now been created
  <- data.txt
  ```
-->

> Nota: Se uma propriedade marcada com o modificador `lazy`
> for acessada por várias threads ao mesmo tempo
> e ainda não tiver sido inicializada,
> não há garantia de que a propriedade será inicializada apenas uma vez.

<!--
  6/19/14, 10:54 PM [Contributor 7746]: @lazy isn't thread safe.  Global variables (and static struct/enum fields) *are*.
-->

### Propriedades armazenadas e variáveis de instância

Se você tem experiência com Objective-C,
talvez você saiba que ele oferece *duas* formas
de armazenar valores e referências como parte de uma instância de classe.
Além de propriedades,
você pode usar variáveis de instância como armazenamento de apoio para os valores guardados em uma propriedade.

O Swift unifica esses conceitos em uma única declaração de propriedade.
Uma propriedade do Swift não tem uma variável de instância correspondente,
e o armazenamento de apoio de uma propriedade não é acessado diretamente.
Essa abordagem evita confusão sobre como o valor é acessado em diferentes contextos
e simplifica a declaração da propriedade em uma única instrução definitiva.
Todas as informações sobre a propriedade ---
incluindo nome, tipo e características de gerenciamento de memória ---
são definidas em um único lugar, como parte da definição do tipo.

<!--
  TODO: what happens if one property of a constant structure is an object reference?
-->

## Propriedades computadas

Além de propriedades armazenadas,
classes, structs e enums podem definir *propriedades computadas*,
que não armazenam um valor de fato.
Em vez disso, elas oferecem um getter e um setter opcional
para ler e definir outras propriedades e valores indiretamente.

```swift
struct Point {
    var x = 0.0, y = 0.0
}
struct Size {
    var width = 0.0, height = 0.0
}
struct Rect {
    var origin = Point()
    var size = Size()
    var center: Point {
        get {
            let centerX = origin.x + (size.width / 2)
            let centerY = origin.y + (size.height / 2)
            return Point(x: centerX, y: centerY)
        }
        set(newCenter) {
            origin.x = newCenter.x - (size.width / 2)
            origin.y = newCenter.y - (size.height / 2)
        }
    }
}
var square = Rect(origin: Point(x: 0.0, y: 0.0),
    size: Size(width: 10.0, height: 10.0))
let initialSquareCenter = square.center
// initialSquareCenter is at (5.0, 5.0)
square.center = Point(x: 15.0, y: 15.0)
print("square.origin is now at (\(square.origin.x), \(square.origin.y))")
// Prints "square.origin is now at (10.0, 10.0)".
```

<!--
  - test: `computedProperties`

  ```swifttest
  -> struct Point {
        var x = 0.0, y = 0.0
     }
  -> struct Size {
        var width = 0.0, height = 0.0
     }
  -> struct Rect {
        var origin = Point()
        var size = Size()
        var center: Point {
           get {
              let centerX = origin.x + (size.width / 2)
              let centerY = origin.y + (size.height / 2)
              return Point(x: centerX, y: centerY)
           }
           set(newCenter) {
              origin.x = newCenter.x - (size.width / 2)
              origin.y = newCenter.y - (size.height / 2)
           }
        }
     }
  -> var square = Rect(origin: Point(x: 0.0, y: 0.0),
        size: Size(width: 10.0, height: 10.0))
  -> let initialSquareCenter = square.center
  /> initialSquareCenter is at (\(initialSquareCenter.x), \(initialSquareCenter.y))
  </ initialSquareCenter is at (5.0, 5.0)
  -> square.center = Point(x: 15.0, y: 15.0)
  -> print("square.origin is now at (\(square.origin.x), \(square.origin.y))")
  <- square.origin is now at (10.0, 10.0)
  ```
-->

Este exemplo define três structs para trabalhar com formas geométricas:

- `Point` encapsula a coordenada x e a coordenada y de um ponto.
- `Size` encapsula uma `width` e uma `height`.
- `Rect` define um retângulo por um ponto de origem e um tamanho.

A struct `Rect` também oferece uma propriedade computada chamada `center`.
O centro atual de um `Rect` sempre pode ser determinado a partir de `origin` e `size`,
então você não precisa armazenar o ponto central como um valor `Point` explícito.
Em vez disso, `Rect` define um getter e um setter personalizados para uma variável computada chamada `center`,
para que você possa trabalhar com o centro do retângulo como se fosse uma propriedade armazenada de verdade.

O exemplo acima cria uma nova variável `Rect` chamada `square`.
A variável `square` é inicializada com um ponto de origem `(0, 0)`
e com largura e altura `10`.
Esse quadrado é representado pelo quadrado verde-claro no diagrama abaixo.

A propriedade `center` da variável `square` é então acessada pela sintaxe de ponto (`square.center`),
o que faz o getter de `center` ser chamado
para obter o valor atual da propriedade.
Em vez de retornar um valor já existente,
o getter na verdade calcula e retorna um novo `Point` que representa o centro do quadrado.
Como se vê acima, o getter retorna corretamente um ponto central `(5, 5)`.

Em seguida, a propriedade `center` recebe um novo valor `(15, 15)`,
o que move o quadrado para cima e para a direita,
até a nova posição mostrada pelo quadrado verde-escuro no diagrama abaixo.
Definir a propriedade `center` chama o setter de `center`,
que modifica os valores `x` e `y` da propriedade armazenada `origin`
e move o quadrado para a nova posição.

<!-- Apple Books screenshot begins here. -->

![](computedProperties)

### Declaração abreviada do setter

Se o setter de uma propriedade computada não define um nome para o novo valor a ser atribuído,
o Swift usa o nome padrão `newValue`.
Aqui está uma versão alternativa da struct `Rect`
que aproveita essa notação abreviada:

```swift
struct AlternativeRect {
    var origin = Point()
    var size = Size()
    var center: Point {
        get {
            let centerX = origin.x + (size.width / 2)
            let centerY = origin.y + (size.height / 2)
            return Point(x: centerX, y: centerY)
        }
        set {
            origin.x = newValue.x - (size.width / 2)
            origin.y = newValue.y - (size.height / 2)
        }
    }
}
```

<!--
  - test: `computedProperties`

  ```swifttest
  -> struct AlternativeRect {
        var origin = Point()
        var size = Size()
        var center: Point {
           get {
              let centerX = origin.x + (size.width / 2)
              let centerY = origin.y + (size.height / 2)
              return Point(x: centerX, y: centerY)
           }
           set {
              origin.x = newValue.x - (size.width / 2)
              origin.y = newValue.y - (size.height / 2)
           }
        }
     }
  ```
-->

<!-- Apple Books screenshot ends here. -->

### Declaração abreviada do getter

Se o corpo inteiro de um getter for uma única expressão,
o getter retorna implicitamente essa expressão.
Aqui está outra versão da struct `Rect`
que aproveita essa notação abreviada e a notação abreviada dos setters:

```swift
struct CompactRect {
    var origin = Point()
    var size = Size()
    var center: Point {
        get {
            Point(x: origin.x + (size.width / 2),
                  y: origin.y + (size.height / 2))
        }
        set {
            origin.x = newValue.x - (size.width / 2)
            origin.y = newValue.y - (size.height / 2)
        }
    }
}
```

<!--
  - test: `computedProperties`

  ```swifttest
  -> struct CompactRect {
        var origin = Point()
        var size = Size()
        var center: Point {
           get {
              Point(x: origin.x + (size.width / 2),
                    y: origin.y + (size.height / 2))
           }
           set {
              origin.x = newValue.x - (size.width / 2)
              origin.y = newValue.y - (size.height / 2)
           }
        }
     }
  ```
-->

Omitir o `return` de um getter
segue as mesmas regras de omitir `return` em uma função,
conforme descrito em <doc:Functions#Functions-With-an-Implicit-Return>.

### Propriedades computadas somente leitura

Uma propriedade computada com getter, mas sem setter, é conhecida como *propriedade computada somente leitura*.
Uma propriedade computada somente leitura sempre retorna um valor,
pode ser acessada pela sintaxe de ponto, mas não pode ser definida com outro valor.

> Nota: Você deve declarar propriedades computadas --- incluindo as somente leitura ---
> como propriedades variáveis, com a palavra-chave `var`, porque o valor delas não é fixo.
> A palavra-chave `let` é usada apenas para propriedades constantes,
> para indicar que os valores não podem ser alterados depois de definidos
> como parte da inicialização da instância.

<!--
  - test: `readOnlyComputedPropertiesMustBeVariables`

  ```swifttest
  -> class C {
        let x: Int { return 42 }
        let y: Int { get { return 42 } set {} }
     }
  !! /tmp/swifttest.swift:2:15: error: 'let' declarations cannot be computed properties
  !! let x: Int { return 42 }
  !! ~~~        ^
  !! var
  !! /tmp/swifttest.swift:3:15: error: 'let' declarations cannot be computed properties
  !! let y: Int { get { return 42 } set {} }
  !! ~~~        ^
  !! var
  ```
-->

Você pode simplificar a declaração de uma propriedade computada somente leitura
removendo a palavra-chave `get` e suas chaves:

```swift
struct Cuboid {
    var width = 0.0, height = 0.0, depth = 0.0
    var volume: Double {
        return width * height * depth
    }
}
let fourByFiveByTwo = Cuboid(width: 4.0, height: 5.0, depth: 2.0)
print("the volume of fourByFiveByTwo is \(fourByFiveByTwo.volume)")
// Prints "the volume of fourByFiveByTwo is 40.0".
```

<!--
  - test: `computedProperties`

  ```swifttest
  -> struct Cuboid {
        var width = 0.0, height = 0.0, depth = 0.0
        var volume: Double {
           return width * height * depth
        }
     }
  -> let fourByFiveByTwo = Cuboid(width: 4.0, height: 5.0, depth: 2.0)
  -> print("the volume of fourByFiveByTwo is \(fourByFiveByTwo.volume)")
  <- the volume of fourByFiveByTwo is 40.0
  ```
-->

Este exemplo define uma nova struct chamada `Cuboid`,
que representa uma caixa retangular 3D com as propriedades `width`, `height` e `depth`.
Essa struct também tem uma propriedade computada somente leitura chamada `volume`,
que calcula e retorna o volume atual do paralelepípedo.
Não faz sentido que o valor de `volume` possa ser definido,
porque seria ambíguo saber quais valores de `width`, `height` e `depth`
deveriam ser usados para um determinado valor de `volume`.
Ainda assim, é útil que um `Cuboid` ofereça uma propriedade computada somente leitura
para que usuários externos possam descobrir o volume calculado atual.

<!--
  NOTE: getters and setters are also allowed for constants and variables
  that aren't associated with a particular class or struct.
  Where should this be mentioned?
-->

<!--
  TODO: Anything else from https://[Internal Staging Server]/docs/StoredAndComputedVariables.html
-->

<!--
  TODO: Add an example of a computed property for an enumeration
  (now that the Enumerations chapter no longer has an example of this itself).
-->

## Observadores de propriedade

Observadores de propriedade observam e respondem a mudanças no valor de uma propriedade.
Observadores de propriedade são chamados sempre que o valor de uma propriedade é definido,
mesmo que o novo valor seja igual ao valor atual da propriedade.

<!--
  - test: `observersAreCalledEvenIfNewValueIsTheSameAsOldValue`

  ```swifttest
  -> class C { var x: Int = 0 { willSet { print("willSet") } didSet { print("didSet") } } }
  -> let c = C()
  -> c.x = 24
  <- willSet
  <- didSet
  -> c.x = 24
  <- willSet
  <- didSet
  ```
-->

Você pode adicionar observadores de propriedade nos seguintes lugares:

- Em propriedades armazenadas que você define
- Em propriedades armazenadas que você herda
- Em propriedades computadas que você herda

Para uma propriedade herdada,
você adiciona um observador de propriedade sobrescrevendo essa propriedade em uma subclasse.
Para uma propriedade computada que você define,
use o setter da propriedade para observar e responder a mudanças de valor,
em vez de tentar criar um observador.
Sobrescrever propriedades é descrito em <doc:Inheritance#Overriding>.

<!--
  - test: `lazyPropertiesCanHaveObservers`

  ```swifttest
  >> class C {
        lazy var x: Int = 0 {
           willSet { print("C willSet x to \(newValue)") }
           didSet { print("C didSet x from \(oldValue)") }
        }
     }
  >> let c = C()
  >> print(c.x)
  << 0
  >> c.x = 12
  << C willSet x to 12
  << C didSet x from 0
  >> print(c.x)
  << 12
  ```
-->

<!--
  - test: `storedAndComputedInheritedPropertiesCanBeObserved`

  ```swifttest
  -> class C {
        var x = 0
        var y: Int { get { return 42 } set {} }
     }
  -> class D: C {
        override var x: Int {
           willSet { print("D willSet x to \(newValue)") }
           didSet { print("D didSet x from \(oldValue)") }
        }
        override var y: Int {
           willSet { print("D willSet y to \(newValue)") }
           didSet { print("D didSet y from \(oldValue)") }
        }
     }
  -> var d = D()
  -> d.x = 42
  <- D willSet x to 42
  <- D didSet x from 0
  -> d.y = 42
  <- D willSet y to 42
  <- D didSet y from 42
  ```
-->

Você pode definir um ou ambos os observadores em uma propriedade:

- `willSet` é chamado logo antes de o valor ser armazenado.
- `didSet` é chamado imediatamente depois que o novo valor é armazenado.

Se você implementar um observador `willSet`,
ele recebe o novo valor da propriedade como um parâmetro constante.
Você pode especificar um nome para esse parâmetro como parte da implementação de `willSet`.
Se você não escrever o nome do parâmetro e os parênteses na implementação,
o parâmetro fica disponível com o nome padrão `newValue`.

De forma semelhante, se você implementar um observador `didSet`,
ele recebe um parâmetro constante com o valor antigo da propriedade.
Você pode dar um nome ao parâmetro ou usar o nome padrão `oldValue`.
Se você atribuir um valor a uma propriedade dentro do próprio observador `didSet`,
o novo valor que você atribuir substitui o que acabou de ser definido.

<!--
  - test: `assigningANewValueInADidSetReplacesTheNewValue`

  ```swifttest
  -> class C { var x: Int = 0 { didSet { x = -273 } } }
  -> let c = C()
  -> c.x = 24
  -> print(c.x)
  <- -273
  ```
-->

> Nota: Os observadores `willSet` e `didSet` de propriedades da superclasse
> são chamados quando uma propriedade é definida em um inicializador de subclasse,
> depois que o inicializador da superclasse foi chamado.
> Eles não são chamados enquanto uma classe está definindo as próprias propriedades
> no corpo do inicializador.
>
> Para mais informações sobre delegação de inicializadores,
> veja <doc:Initialization#Initializer-Delegation-for-Value-Types>
> e <doc:Initialization#Initializer-Delegation-for-Class-Types>.

<!--
  - test: `observersDuringInitialization`

  ```swifttest
  -> class C {
        var x: Int { willSet { print("willSet x") } didSet { print("didSet x") } }
        init(x: Int) { self.x = x }
     }
  -> let c = C(x: 42)
  -> c.x = 24
  <- willSet x
  <- didSet x
  -> class C2: C {
        var y: Int { willSet { print("willSet y") } didSet { print("didSet y") } }
        init() {
            self.y = 1
            print("calling super")
            super.init(x: 100)
            self.x = 10
        }
     }
  -> let c2 = C2()
  <- calling super
  <- willSet x
  <- didSet x
  ```
-->

Aqui está um exemplo de `willSet` e `didSet` em ação.
O exemplo abaixo define uma nova classe chamada `StepCounter`,
que registra o número total de passos que uma pessoa dá caminhando.
Essa classe poderia ser usada com dados de entrada de um podômetro ou outro contador de passos
para acompanhar os exercícios de uma pessoa na rotina diária.

```swift
class StepCounter {
    var totalSteps: Int = 0 {
        willSet(newTotalSteps) {
            print("About to set totalSteps to \(newTotalSteps)")
        }
        didSet {
            if totalSteps > oldValue  {
                print("Added \(totalSteps - oldValue) steps")
            }
        }
    }
}
let stepCounter = StepCounter()
stepCounter.totalSteps = 200
// About to set totalSteps to 200
// Added 200 steps
stepCounter.totalSteps = 360
// About to set totalSteps to 360
// Added 160 steps
stepCounter.totalSteps = 896
// About to set totalSteps to 896
// Added 536 steps
```

<!--
  - test: `storedProperties`

  ```swifttest
  -> class StepCounter {
        var totalSteps: Int = 0 {
           willSet(newTotalSteps) {
              print("About to set totalSteps to \(newTotalSteps)")
           }
           didSet {
              if totalSteps > oldValue  {
                 print("Added \(totalSteps - oldValue) steps")
              }
           }
        }
     }
  -> let stepCounter = StepCounter()
  -> stepCounter.totalSteps = 200
  </ About to set totalSteps to 200
  </ Added 200 steps
  -> stepCounter.totalSteps = 360
  </ About to set totalSteps to 360
  </ Added 160 steps
  -> stepCounter.totalSteps = 896
  </ About to set totalSteps to 896
  </ Added 536 steps
  ```
-->

A classe `StepCounter` declara uma propriedade `totalSteps` do tipo `Int`.
Trata-se de uma propriedade armazenada com observadores `willSet` e `didSet`.

Os observadores `willSet` e `didSet` de `totalSteps` são chamados
sempre que a propriedade recebe um novo valor.
Isso vale mesmo se o novo valor for igual ao valor atual.

O observador `willSet` deste exemplo usa um nome de parâmetro personalizado,
`newTotalSteps`, para o próximo valor.
Neste exemplo, ele apenas imprime o valor que está prestes a ser definido.

O observador `didSet` é chamado depois que o valor de `totalSteps` é atualizado.
Ele compara o novo valor de `totalSteps` com o valor antigo.
Se o total de passos aumentou,
uma mensagem é impressa para indicar quantos passos novos foram dados.
O observador `didSet` não define um nome personalizado para o valor antigo,
e o nome padrão `oldValue` é usado.

> Nota: Se você passar para uma função, como parâmetro in-out,
> uma propriedade que tem observadores,
> os observadores `willSet` e `didSet` são sempre chamados.
> Isso acontece por causa do modelo de memória copy-in copy-out dos parâmetros in-out:
> o valor é sempre gravado de volta na propriedade no fim da função.
> Para uma discussão detalhada sobre o comportamento dos parâmetros in-out,
> veja <doc:Declarations#In-Out-Parameters>.

<!--
  - test: `observersCalledAfterInout`

  ```swifttest
  -> var a: Int = 0 {
         willSet { print("willSet") }
         didSet { print("didSet") }
     }
  -> func f(b: inout Int) { print("in f") }
  -> f(b: &a)
  << in f
  << willSet
  << didSet
  ```
-->

<!--
  TODO: If you add a property observer to a stored property of structure type,
  that property observer is fired whenever any of the subproperties
  of that structure instance are set. This is cool, but nonobvious.
  Provide an example of it here.
-->

## Property wrappers

Um property wrapper cria uma camada de separação
entre o código que gerencia como uma propriedade é armazenada
e o código que define a propriedade.
Por exemplo,
se você tem propriedades que
fazem verificações de thread-safety
ou armazenam os dados em um banco de dados,
precisa escrever esse código em cada propriedade.
Ao usar um property wrapper,
você escreve o código de gerenciamento uma vez, ao definir o wrapper,
e depois reaproveita esse código aplicando-o a várias propriedades.

Para definir um property wrapper,
você cria uma struct, enum ou classe
que define uma propriedade `wrappedValue`.
No código abaixo,
a struct `TwelveOrLess` garante que
o valor que ela envolve sempre contenha um número menor ou igual a 12.
Se você pedir para armazenar um número maior, ela armazena 12.

```swift
@propertyWrapper
struct TwelveOrLess {
    private var number = 0
    var wrappedValue: Int {
        get { return number }
        set { number = min(newValue, 12) }
    }
}
```

<!--
  - test: `small-number-wrapper, property-wrapper-expansion`

  ```swifttest
  -> @propertyWrapper
  -> struct TwelveOrLess {
         private var number = 0
         var wrappedValue: Int {
             get { return number }
             set { number = min(newValue, 12) }
         }
     }
  ```
-->

<!--
  No init(wrappedValue:) in this example -- that's in a later example.
  Always initializing the wrapped value is a simpler starting point.
-->

O setter garante que novos valores sejam menores ou iguais a 12,
e o getter retorna o valor armazenado.

> Nota: A declaração de `number` no exemplo acima
> marca a variável como `private`,
> o que garante que `number` seja usada apenas
> na implementação de `TwelveOrLess`.
> Código escrito em qualquer outro lugar
> acessa o valor pelo getter e pelo setter de `wrappedValue`,
> e não pode usar `number` diretamente.
> Para informações sobre `private`, veja <doc:AccessControl>.

<!--
  In this example,
  the number is stored in the wrapper's private ``number`` property,
  but you could write a version of ``EvenNumber``
  that implements ``wrappedValue`` as a stored property
  and uses ``didSet`` to ensure the number is always even.

  However, the general framing we use in the docs
  is that didSet is mostly for reacting to the new value,
  not changing it,
  so I'm not highlighting that fact here.
  The order of operations for willSet, set, and didSet is well defined,
  but might be something you have to pay attention to.
-->

<!--
  - test: `stored-property-wrappedValue`

  ```swifttest
  >> @propertyWrapper
  >> struct TwelveOrLess {
  >>     var wrappedValue: Int = 0 {
  >>         didSet {
  >>             if wrappedValue > 12 {
  >>                 wrappedValue = 12
  >>             }
  >>         }
  >>     }
  >> }
  >> struct SomeStructure {
  >>     @TwelveOrLess var someNumber: Int
  >> }
  >> var s = SomeStructure()
  >> print(s.someNumber)
  << 0
  >> s.someNumber = 10
  >> print(s.someNumber)
  << 10
  >> s.someNumber = 21
  >> print(s.someNumber)
  << 12
  ```
-->

Você aplica um wrapper a uma propriedade
escrevendo o nome do wrapper antes da propriedade,
como um atributo.
Aqui está uma struct que armazena um retângulo
que usa o property wrapper `TwelveOrLess`
para garantir que suas dimensões sejam sempre 12 ou menos:

```swift
struct SmallRectangle {
    @TwelveOrLess var height: Int
    @TwelveOrLess var width: Int
}

var rectangle = SmallRectangle()
print(rectangle.height)
// Prints "0".

rectangle.height = 10
print(rectangle.height)
// Prints "10".

rectangle.height = 24
print(rectangle.height)
// Prints "12".
```

<!--
  - test: `small-number-wrapper`

  ```swifttest
  -> struct SmallRectangle {
  ->     @TwelveOrLess var height: Int
  ->     @TwelveOrLess var width: Int
  -> }

  -> var rectangle = SmallRectangle()
  -> print(rectangle.height)
  <- 0

  -> rectangle.height = 10
  -> print(rectangle.height)
  <- 10

  -> rectangle.height = 24
  -> print(rectangle.height)
  <- 12
  ```
-->

As propriedades `height` e `width` recebem seus valores iniciais
da definição de `TwelveOrLess`, que define `TwelveOrLess.number` como zero.
O setter de `TwelveOrLess` aceita 10 como valor válido,
então armazenar o número 10 em `rectangle.height` funciona normalmente.
No entanto, 24 é maior do que `TwelveOrLess` permite,
então tentar armazenar 24 faz `rectangle.height` ser definido como 12, o maior valor permitido.

Quando você aplica um wrapper a uma propriedade,
o compilador sintetiza código que fornece o armazenamento para o wrapper
e código que dá acesso à propriedade por meio do wrapper.
(O property wrapper é responsável por armazenar o valor envolvido,
então não há código sintetizado para isso.)
Você poderia escrever código que usa o comportamento de um property wrapper
sem aproveitar a sintaxe especial de atributo.
Por exemplo,
aqui está uma versão de `SmallRectangle` do exemplo anterior
que envolve suas propriedades na struct `TwelveOrLess` explicitamente,
em vez de escrever `@TwelveOrLess` como atributo:

```swift
struct SmallRectangle {
    private var _height = TwelveOrLess()
    private var _width = TwelveOrLess()
    var height: Int {
        get { return _height.wrappedValue }
        set { _height.wrappedValue = newValue }
    }
    var width: Int {
        get { return _width.wrappedValue }
        set { _width.wrappedValue = newValue }
    }
}
```

<!--
  - test: `property-wrapper-expansion`

  ```swifttest
  -> struct SmallRectangle {
         private var _height = TwelveOrLess()
         private var _width = TwelveOrLess()
         var height: Int {
             get { return _height.wrappedValue }
             set { _height.wrappedValue = newValue }
         }
         var width: Int {
             get { return _width.wrappedValue }
             set { _width.wrappedValue = newValue }
         }
     }
  ```
-->

As propriedades `_height` e `_width`
armazenam uma instância do property wrapper, `TwelveOrLess`.
O getter e o setter de `height` e `width`
envolvem o acesso à propriedade `wrappedValue`.

### Definindo valores iniciais para propriedades com wrapper

O código dos exemplos acima
define o valor inicial da propriedade envolvida
dando a `number` um valor inicial na definição de `TwelveOrLess`.
O código que usa esse property wrapper
não pode especificar um valor inicial diferente para uma propriedade
envolvida por `TwelveOrLess` ---
por exemplo,
a definição de `SmallRectangle`
não pode dar valores iniciais a `height` ou `width`.
Para permitir definir um valor inicial ou outra personalização,
o property wrapper precisa adicionar um inicializador.
Aqui está uma versão expandida de `TwelveOrLess`, chamada `SmallNumber`,
que define inicializadores que configuram o valor envolvido e o valor máximo:

```swift
@propertyWrapper
struct SmallNumber {
    private var maximum: Int
    private var number: Int

    var wrappedValue: Int {
        get { return number }
        set { number = min(newValue, maximum) }
    }

    init() {
        maximum = 12
        number = 0
    }
    init(wrappedValue: Int) {
        maximum = 12
        number = min(wrappedValue, maximum)
    }
    init(wrappedValue: Int, maximum: Int) {
        self.maximum = maximum
        number = min(wrappedValue, maximum)
    }
}
```

<!--
  - test: `property-wrapper-init, property-wrapper-mixed-init`

  ```swifttest
  -> @propertyWrapper
  -> struct SmallNumber {
         private var maximum: Int
         private var number: Int

         var wrappedValue: Int {
             get { return number }
             set { number = min(newValue, maximum) }
         }

         init() {
             maximum = 12
             number = 0
         }
         init(wrappedValue: Int) {
             maximum = 12
             number = min(wrappedValue, maximum)
         }
         init(wrappedValue: Int, maximum: Int) {
             self.maximum = maximum
             number = min(wrappedValue, maximum)
         }
     }
  ```
-->

<!--
  The initializers above could be written to use
  init(wrappedValue:maximum:) as the designated initializer,
  with the other two calling it instead of doing initialization.
  However, in this case, the initialization logic is small enough
  that the risk of bugs isn't significant,
  and the reader hasn't seen init syntax/rules in detail yet
  so it's clearer to make each init stand on its own.
-->

A definição de `SmallNumber` inclui três inicializadores ---
`init()`, `init(wrappedValue:)` e `init(wrappedValue:maximum:)` ---
que os exemplos abaixo usam
para definir o valor envolvido e o valor máximo.
Para informações sobre inicialização e sintaxe de inicializadores,
veja <doc:Initialization>.

Quando você aplica um wrapper a uma propriedade e não especifica um valor inicial,
o Swift usa o inicializador `init()` para configurar o wrapper.
Por exemplo:

```swift
struct ZeroRectangle {
    @SmallNumber var height: Int
    @SmallNumber var width: Int
}

var zeroRectangle = ZeroRectangle()
print(zeroRectangle.height, zeroRectangle.width)
// Prints "0 0".
```

<!--
  - test: `property-wrapper-init`

  ```swifttest
  -> struct ZeroRectangle {
  ->     @SmallNumber var height: Int
  ->     @SmallNumber var width: Int
  -> }

  -> var zeroRectangle = ZeroRectangle()
  -> print(zeroRectangle.height, zeroRectangle.width)
  <- 0 0
  ```
-->

<!--
  - test: `property-wrapper-init`

  ```swifttest
  -> struct ZeroRectangle_equiv {
         private var _height = SmallNumber()
         private var _width = SmallNumber()
         var height: Int {
             get { return _height.wrappedValue }
             set { _height.wrappedValue = newValue }
         }
         var width: Int {
             get { return _width.wrappedValue }
             set { _width.wrappedValue = newValue }
         }
     }
  -> var zeroRectangle_equiv = ZeroRectangle_equiv()
  -> print(zeroRectangle_equiv.height, zeroRectangle_equiv.width)
  <- 0 0
  ```
-->

As instâncias de `SmallNumber` que envolvem `height` e `width`
são criadas chamando `SmallNumber()`.
O código dentro desse inicializador
define o valor envolvido inicial e o valor máximo inicial,
usando os valores padrão zero e 12.
O property wrapper ainda fornece todos os valores iniciais,
como no exemplo anterior que usou `TwelveOrLess` em `SmallRectangle`.
Diferente desse exemplo,
`SmallNumber` também permite escrever esses valores iniciais
como parte da declaração da propriedade.

Quando você especifica um valor inicial para a propriedade,
o Swift usa o inicializador `init(wrappedValue:)` para configurar o wrapper.
Por exemplo:

```swift
struct UnitRectangle {
    @SmallNumber var height: Int = 1
    @SmallNumber var width: Int = 1
}

var unitRectangle = UnitRectangle()
print(unitRectangle.height, unitRectangle.width)
// Prints "1 1".
```

<!--
  - test: `property-wrapper-init`

  ```swifttest
  -> struct UnitRectangle {
  ->     @SmallNumber var height: Int = 1
  ->     @SmallNumber var width: Int = 1
  -> }

  -> var unitRectangle = UnitRectangle()
  -> print(unitRectangle.height, unitRectangle.width)
  <- 1 1
  ```
-->

<!--
  - test: `property-wrapper-init`

  ```swifttest
  -> struct UnitRectangle_equiv {
         private var _height = SmallNumber(wrappedValue: 1)
         private var _width = SmallNumber(wrappedValue: 1)
         var height: Int {
             get { return _height.wrappedValue }
             set { _height.wrappedValue = newValue }
         }
         var width: Int {
             get { return _width.wrappedValue }
             set { _width.wrappedValue = newValue }
         }
     }
  -> var unitRectangle_equiv = UnitRectangle_equiv()
  -> print(unitRectangle_equiv.height, unitRectangle_equiv.width)
  <- 1 1
  ```
-->

Quando você escreve `= 1` em uma propriedade com wrapper,
isso é traduzido em uma chamada ao inicializador `init(wrappedValue:)`.
As instâncias de `SmallNumber` que envolvem `height` e `width`
são criadas chamando `SmallNumber(wrappedValue: 1)`.
O inicializador usa o valor envolvido especificado aqui,
e usa o valor máximo padrão de 12.

Quando você escreve argumentos entre parênteses depois do atributo personalizado,
o Swift usa o inicializador que aceita esses argumentos para configurar o wrapper.
Por exemplo, se você fornecer um valor inicial e um valor máximo,
o Swift usa o inicializador `init(wrappedValue:maximum:)`:

```swift
struct NarrowRectangle {
    @SmallNumber(wrappedValue: 2, maximum: 5) var height: Int
    @SmallNumber(wrappedValue: 3, maximum: 4) var width: Int
}

var narrowRectangle = NarrowRectangle()
print(narrowRectangle.height, narrowRectangle.width)
// Prints "2 3".

narrowRectangle.height = 100
narrowRectangle.width = 100
print(narrowRectangle.height, narrowRectangle.width)
// Prints "5 4".
```

<!--
  - test: `property-wrapper-init`

  ```swifttest
  -> struct NarrowRectangle {
  ->     @SmallNumber(wrappedValue: 2, maximum: 5) var height: Int
  ->     @SmallNumber(wrappedValue: 3, maximum: 4) var width: Int
  -> }

  -> var narrowRectangle = NarrowRectangle()
  -> print(narrowRectangle.height, narrowRectangle.width)
  <- 2 3

  -> narrowRectangle.height = 100
  -> narrowRectangle.width = 100
  -> print(narrowRectangle.height, narrowRectangle.width)
  <- 5 4
  ```
-->

<!--
  - test: `property-wrapper-init`

  ```swifttest
  -> struct NarrowRectangle_equiv {
         private var _height = SmallNumber(wrappedValue: 2, maximum: 5)
         private var _width = SmallNumber(wrappedValue: 3, maximum: 4)
         var height: Int {
             get { return _height.wrappedValue }
             set { _height.wrappedValue = newValue }
         }
         var width: Int {
             get { return _width.wrappedValue }
             set { _width.wrappedValue = newValue }
         }
     }
  -> var narrowRectangle_equiv = NarrowRectangle_equiv()
  -> print(narrowRectangle_equiv.height, narrowRectangle_equiv.width)
  <- 2 3
  -> narrowRectangle_equiv.height = 100
  -> narrowRectangle_equiv.width = 100
  -> print(narrowRectangle_equiv.height, narrowRectangle_equiv.width)
  <- 5 4
  ```
-->

A instância de `SmallNumber` que envolve `height`
é criada chamando `SmallNumber(wrappedValue: 2, maximum: 5)`,
e a instância que envolve `width`
é criada chamando `SmallNumber(wrappedValue: 3, maximum: 4)`.

Ao incluir argumentos no property wrapper,
você pode definir o estado inicial no wrapper
ou passar outras opções para ele na hora da criação.
Essa sintaxe é a forma mais geral de usar um property wrapper.
Você pode fornecer os argumentos que precisar ao atributo,
e eles são passados para o inicializador.

Quando você inclui argumentos do property wrapper,
também pode especificar um valor inicial usando atribuição.
O Swift trata a atribuição como um argumento `wrappedValue`
e usa o inicializador que aceita os argumentos que você incluiu.
Por exemplo:

```swift
struct MixedRectangle {
    @SmallNumber var height: Int = 1
    @SmallNumber(maximum: 9) var width: Int = 2
}

var mixedRectangle = MixedRectangle()
print(mixedRectangle.height)
// Prints "1".

mixedRectangle.height = 20
print(mixedRectangle.height)
// Prints "12".
```

<!--
  - test: `property-wrapper-mixed-init`

  ```swifttest
  -> struct MixedRectangle {
  ->     @SmallNumber var height: Int = 1
  ->     @SmallNumber(maximum: 9) var width: Int = 2
  -> }

  -> var mixedRectangle = MixedRectangle()
  -> print(mixedRectangle.height)
  <- 1

  -> mixedRectangle.height = 20
  -> print(mixedRectangle.height)
  <- 12
  ```
-->

A instância de `SmallNumber` que envolve `height`
é criada chamando `SmallNumber(wrappedValue: 1)`,
que usa o valor máximo padrão de 12.
A instância que envolve `width`
é criada chamando `SmallNumber(wrappedValue: 2, maximum: 9)`.

### Projetando um valor de um property wrapper

Além do valor envolvido,
um property wrapper pode expor funcionalidades adicionais
definindo um *valor projetado* ---
por exemplo, um property wrapper que gerencia o acesso a um banco de dados
pode expor um método `flushDatabaseConnection()` em seu valor projetado.
O nome do valor projetado é o mesmo do valor envolvido,
exceto que começa com um cifrão (`$`).
Como seu código não pode definir propriedades que começam com `$`,
o valor projetado nunca interfere nas propriedades que você define.

No exemplo `SmallNumber` acima,
se você tentar definir a propriedade com um número grande demais,
o property wrapper ajusta o número antes de armazená-lo.
O código abaixo adiciona uma propriedade `projectedValue` à struct `SmallNumber`
para registrar se o property wrapper
ajustou o novo valor da propriedade antes de armazená-lo.

```swift
@propertyWrapper
struct SmallNumber {
    private var number: Int
    private(set) var projectedValue: Bool

    var wrappedValue: Int {
        get { return number }
        set {
            if newValue > 12 {
                number = 12
                projectedValue = true
            } else {
                number = newValue
                projectedValue = false
            }
        }
    }

    init() {
        self.number = 0
        self.projectedValue = false
    }
}
struct SomeStructure {
    @SmallNumber var someNumber: Int
}
var someStructure = SomeStructure()

someStructure.someNumber = 4
print(someStructure.$someNumber)
// Prints "false".

someStructure.someNumber = 55
print(someStructure.$someNumber)
// Prints "true".
```

<!--
  - test: `small-number-wrapper-projection`

  ```swifttest
  -> @propertyWrapper
  -> struct SmallNumber {
         private var number: Int
         private(set) var projectedValue: Bool

         var wrappedValue: Int {
             get { return number }
             set {
                 if newValue > 12 {
                     number = 12
                     projectedValue = true
                 } else {
                     number = newValue
                     projectedValue = false
                 }
             }
         }

         init() {
             self.number = 0
             self.projectedValue = false
         }
     }
  -> struct SomeStructure {
  ->     @SmallNumber var someNumber: Int
  -> }
  -> var someStructure = SomeStructure()

  -> someStructure.someNumber = 4
  -> print(someStructure.$someNumber)
  <- false

  -> someStructure.someNumber = 55
  -> print(someStructure.$someNumber)
  <- true
  ```
-->

Escrever `someStructure.$someNumber` acessa o valor projetado do wrapper.
Depois de armazenar um número pequeno como quatro,
o valor de `someStructure.$someNumber` é `false`.
No entanto,
o valor projetado é `true`
depois de tentar armazenar um número grande demais, como 55.

Um property wrapper pode retornar um valor de qualquer tipo como seu valor projetado.
Neste exemplo,
o property wrapper expõe apenas uma informação ---
se o número foi ajustado ---
então ele expõe esse valor booleano como seu valor projetado.
Um wrapper que precisa expor mais informações
pode retornar uma instância de algum outro tipo,
ou pode retornar `self`
para expor a instância do wrapper como seu valor projetado.

Quando você acessa um valor projetado a partir de código que faz parte do tipo,
como um getter de propriedade ou um método de instância,
pode omitir `self.` antes do nome da propriedade,
da mesma forma que ao acessar outras propriedades.
O código no exemplo a seguir se refere ao valor projetado
do wrapper em torno de `height` e `width` como `$height` e `$width`:

```swift
enum Size {
    case small, large
}

struct SizedRectangle {
    @SmallNumber var height: Int
    @SmallNumber var width: Int

    mutating func resize(to size: Size) -> Bool {
        switch size {
        case .small:
            height = 10
            width = 20
        case .large:
            height = 100
            width = 100
        }
        return $height || $width
    }
}
```

<!--
  - test: `small-number-wrapper-projection`

  ```swifttest
  -> enum Size {
         case small, large
     }

  -> struct SizedRectangle {
  ->     @SmallNumber var height: Int
  ->     @SmallNumber var width: Int

         mutating func resize(to size: Size) -> Bool {
             switch size {
                 case .small:
                     height = 10
                     width = 20
                 case .large:
                     height = 100
                     width = 100
             }
             return $height || $width
         }
     }
  >> var r = SizedRectangle()
  >> print(r.height, r.width)
  << 0 0
  >> var adj = r.resize(to: .large)
  >> print(adj, r.height, r.width)
  << true 12 12
  ```
-->

Como a sintaxe de property wrapper é apenas açúcar sintático
para uma propriedade com getter e setter,
acessar `height` e `width`
se comporta da mesma forma que acessar qualquer outra propriedade.
Por exemplo,
o código em `resize(to:)` acessa `height` e `width`
usando o property wrapper deles.
Se você chamar `resize(to: .large)`,
o caso `.large` do switch define a altura e a largura do retângulo como 100.
O wrapper impede que o valor dessas propriedades
seja maior que 12,
e define o valor projetado como `true`,
para registrar o fato de ter ajustado os valores.
No fim de `resize(to:)`,
a instrução return verifica `$height` e `$width`
para determinar se
o property wrapper ajustou `height` ou `width`.

## Variáveis globais e locais

As capacidades descritas acima para calcular e observar propriedades
também estão disponíveis para *variáveis globais* e *variáveis locais*.
Variáveis globais são variáveis definidas fora de qualquer
função, método, closure ou contexto de tipo.
Variáveis locais são variáveis definidas dentro
de um contexto de função, método ou closure.

As variáveis globais e locais que você viu nos capítulos anteriores
sempre foram *variáveis armazenadas*.
Variáveis armazenadas, como propriedades armazenadas,
fornecem armazenamento para um valor de determinado tipo e permitem que esse valor seja definido e lido.

No entanto, você também pode definir *variáveis computadas*
e definir observadores para variáveis armazenadas,
tanto em escopo global quanto em escopo local.
Variáveis computadas calculam o valor em vez de armazená-lo,
e são escritas da mesma forma que propriedades computadas.

<!--
  - test: `computedVariables`

  ```swifttest
  -> var a: Int { get { return 42 } set { print("set a to \(newValue)") } }
  -> a = 37
  <- set a to 37
  -> print(a)
  <- 42
  ```
-->

<!--
  - test: `observersForStoredVariables`

  ```swifttest
  -> var a: Int = 0 { willSet { print("willSet") } didSet { print("didSet") } }
  -> a = 42
  <- willSet
  <- didSet
  ```
-->

> Nota: Constantes e variáveis globais são sempre calculadas de forma lazy,
> de maneira semelhante às <doc:Properties#Lazy-Stored-Properties>.
> Ao contrário das propriedades armazenadas lazy,
> constantes e variáveis globais não precisam ser marcadas com o modificador `lazy`.
>
> Constantes e variáveis locais nunca são calculadas de forma lazy.

Você pode aplicar um property wrapper a uma variável armazenada local,
mas não a uma variável global nem a uma variável computada.
Por exemplo,
no código abaixo, `myNumber` usa `SmallNumber` como property wrapper.

```swift
func someFunction() {
    @SmallNumber var myNumber: Int = 0

    myNumber = 10
    // now myNumber is 10

    myNumber = 24
    // now myNumber is 12
}
```

<!--
  - test: `property-wrapper-init`

  ```swifttest
  -> func someFunction() {
  ->     @SmallNumber var myNumber: Int = 0

         myNumber = 10
         // now myNumber is 10
  >>     print(myNumber)

         myNumber = 24
         // now myNumber is 12
  >>     print(myNumber)
     }
  >> someFunction()
  << 10
  << 12
  ```
-->

Assim como ao aplicar `SmallNumber` a uma propriedade,
definir o valor de `myNumber` como 10 é válido.
Como o property wrapper não permite valores maiores que 12,
ele define `myNumber` como 12 em vez de 24.

<!--
  The discussion of local variables with property wrappers
  has to come later, because we need to use init(wrappedValue:)
  to work around <rdar://problem/74616133>.
-->

<!--
  TODO: clarify what we mean by "global variables" here.
  According to [Contributor 6004], anything defined in a playground, REPL, or in main.swift
  is a local variable in top-level code, not a global variable.
-->

<!--
  TODO: this also makes it impossible (at present) to test the "always lazy" assertion.
-->

## Propriedades de tipo

Propriedades de instância são propriedades que pertencem a uma instância de determinado tipo.
Toda vez que você cria uma nova instância desse tipo,
ela tem seu próprio conjunto de valores de propriedade, separado de qualquer outra instância.

Você também pode definir propriedades que pertencem ao próprio tipo,
e não a uma instância específica desse tipo.
Só existirá uma cópia dessas propriedades,
não importa quantas instâncias desse tipo você crie.
Essas propriedades são chamadas de *propriedades de tipo*.

Propriedades de tipo são úteis para definir valores universais para
*todas* as instâncias de um tipo específico,
como uma propriedade constante que todas as instâncias podem usar
(como uma constante static em C),
ou uma propriedade variável que armazena um valor global para todas as instâncias desse tipo
(como uma variável static em C).

Propriedades de tipo armazenadas podem ser variáveis ou constantes.
Propriedades de tipo computadas são sempre declaradas como propriedades variáveis,
do mesmo modo que as propriedades computadas de instância.

> Nota: Diferente das propriedades armazenadas de instância,
> você deve sempre dar um valor padrão às propriedades de tipo armazenadas.
> Isso acontece porque o próprio tipo não tem um inicializador
> que possa atribuir um valor a uma propriedade de tipo armazenada no momento da inicialização.
>
> Propriedades de tipo armazenadas são inicializadas de forma lazy na primeira vez que são acessadas.
> Elas têm a garantia de ser inicializadas apenas uma vez,
> mesmo quando acessadas por várias threads ao mesmo tempo,
> e não precisam ser marcadas com o modificador `lazy`.

### Sintaxe de propriedades de tipo

Em C e Objective-C, você define constantes e variáveis associadas a um tipo
como variáveis estáticas *globais*.
No Swift, porém, propriedades de tipo são escritas como parte da definição do tipo,
dentro das chaves externas do tipo,
e cada propriedade de tipo fica explicitamente vinculada ao tipo a que dá suporte.

Você define propriedades de tipo com a palavra-chave `static`.
Para propriedades de tipo computadas de tipos classe,
você pode usar a palavra-chave `class` em vez disso,
para permitir que subclasses sobrescrevam a implementação da superclasse.
O exemplo abaixo mostra a sintaxe de propriedades de tipo armazenadas e computadas:

```swift
struct SomeStructure {
    static var storedTypeProperty = "Some value."
    static var computedTypeProperty: Int {
        return 1
    }
}
enum SomeEnumeration {
    static var storedTypeProperty = "Some value."
    static var computedTypeProperty: Int {
        return 6
    }
}
class SomeClass {
    static var storedTypeProperty = "Some value."
    static var computedTypeProperty: Int {
        return 27
    }
    class var overrideableComputedTypeProperty: Int {
        return 107
    }
}
```

<!--
  - test: `typePropertySyntax`

  ```swifttest
  -> struct SomeStructure {
        static var storedTypeProperty = "Some value."
        static var computedTypeProperty: Int {
           return 1
        }
     }
  -> enum SomeEnumeration {
        static var storedTypeProperty = "Some value."
        static var computedTypeProperty: Int {
           return 6
        }
     }
  -> class SomeClass {
        static var storedTypeProperty = "Some value."
        static var computedTypeProperty: Int {
           return 27
        }
        class var overrideableComputedTypeProperty: Int {
           return 107
        }
     }
  ```
-->

<!--
  - test: `classComputedTypePropertiesAreOverrideable`

  ```swifttest
  -> class A { class var cp: String { return "A" } }
  -> class B: A { override class var cp: String { return "B" } }
  -> assert(A.cp == "A")
  -> assert(B.cp == "B")
  ```
-->

<!--
  - test: `staticComputedTypePropertiesAreFinal`

  ```swifttest
  -> class A { static var cp: String { return "A" } }
  -> class B: A { override static var cp: String { return "B" } }
  !$ error: cannot override static property
  !! class B: A { override static var cp: String { return "B" } }
  !!                                  ^
  !$ note: overridden declaration is here
  !! class A { static var cp: String { return "A" } }
  !!                      ^
  ```
-->

> Nota: Os exemplos de propriedades de tipo computadas acima são de propriedades de tipo computadas somente leitura,
> mas você também pode definir propriedades de tipo computadas de leitura e escrita
> com a mesma sintaxe das propriedades computadas de instância.

### Consultando e definindo propriedades de tipo

Propriedades de tipo são consultadas e definidas com a sintaxe de ponto, assim como as propriedades de instância.
No entanto, propriedades de tipo são consultadas e definidas no *tipo*, e não em uma instância desse tipo.
Por exemplo:

```swift
print(SomeStructure.storedTypeProperty)
// Prints "Some value."
SomeStructure.storedTypeProperty = "Another value."
print(SomeStructure.storedTypeProperty)
// Prints "Another value."
print(SomeEnumeration.computedTypeProperty)
// Prints "6".
print(SomeClass.computedTypeProperty)
// Prints "27".
```

<!--
  - test: `typePropertySyntax`

  ```swifttest
  -> print(SomeStructure.storedTypeProperty)
  <- Some value.
  -> SomeStructure.storedTypeProperty = "Another value."
  -> print(SomeStructure.storedTypeProperty)
  <- Another value.
  -> print(SomeEnumeration.computedTypeProperty)
  <- 6
  -> print(SomeClass.computedTypeProperty)
  <- 27
  ```
-->

Os exemplos a seguir usam duas propriedades de tipo armazenadas como parte de uma struct
que modela um medidor de nível de áudio para vários canais de áudio.
Cada canal tem um nível de áudio inteiro entre `0` e `10`, inclusive.

A figura abaixo mostra como dois desses canais de áudio podem ser combinados
para modelar um medidor de nível estéreo.
Quando o nível de um canal é `0`, nenhuma das luzes desse canal fica acesa.
Quando o nível de áudio é `10`, todas as luzes desse canal ficam acesas.
Nessa figura, o canal esquerdo tem nível atual `9`,
e o canal direito tem nível atual `7`:

![](staticPropertiesVUMeter)

Os canais de áudio descritos acima são representados por
instâncias da struct `AudioChannel`:

```swift
struct AudioChannel {
    static let thresholdLevel = 10
    static var maxInputLevelForAllChannels = 0
    var currentLevel: Int = 0 {
        didSet {
            if currentLevel > AudioChannel.thresholdLevel {
                // cap the new audio level to the threshold level
                currentLevel = AudioChannel.thresholdLevel
            }
            if currentLevel > AudioChannel.maxInputLevelForAllChannels {
                // store this as the new overall maximum input level
                AudioChannel.maxInputLevelForAllChannels = currentLevel
            }
        }
    }
}
```

<!--
  - test: `staticProperties`

  ```swifttest
  -> struct AudioChannel {
        static let thresholdLevel = 10
        static var maxInputLevelForAllChannels = 0
        var currentLevel: Int = 0 {
           didSet {
              if currentLevel > AudioChannel.thresholdLevel {
                 // cap the new audio level to the threshold level
                 currentLevel = AudioChannel.thresholdLevel
              }
              if currentLevel > AudioChannel.maxInputLevelForAllChannels {
                 // store this as the new overall maximum input level
                 AudioChannel.maxInputLevelForAllChannels = currentLevel
              }
           }
        }
     }
  ```
-->

A struct `AudioChannel` define duas propriedades de tipo armazenadas para dar suporte às suas funcionalidades.
A primeira, `thresholdLevel`, define o valor limite máximo que um nível de áudio pode ter.
Este é um valor constante de `10` para todas as instâncias de `AudioChannel`.
Se um sinal de áudio chegar com um valor maior que `10`,
ele é limitado a esse valor limite (como descrito abaixo).

A segunda propriedade de tipo é
uma propriedade armazenada variável chamada `maxInputLevelForAllChannels`.
Ela registra o valor máximo de entrada recebido
por *qualquer* instância de `AudioChannel`.
Ela começa com o valor inicial `0`.

A struct `AudioChannel` também define
uma propriedade armazenada de instância chamada `currentLevel`,
que representa o nível de áudio atual do canal, em uma escala de `0` a `10`.

A propriedade `currentLevel` tem um observador de propriedade `didSet`
que verifica o valor de `currentLevel` sempre que ele é definido.
Esse observador faz duas verificações:

- Se o novo valor de `currentLevel` for maior que o `thresholdLevel` permitido,
  o observador de propriedade limita `currentLevel` a `thresholdLevel`.
- Se o novo valor de `currentLevel` (depois de qualquer limitação) for maior que
  qualquer valor recebido anteriormente por *qualquer* instância de `AudioChannel`,
  o observador de propriedade armazena o novo valor de `currentLevel`
  na propriedade de tipo `maxInputLevelForAllChannels`.

> Nota: Na primeira dessas duas verificações,
> o observador `didSet` define `currentLevel` com um valor diferente.
> Isso, porém, não faz o observador ser chamado de novo.

Você pode usar a struct `AudioChannel` para criar
dois novos canais de áudio chamados `leftChannel` e `rightChannel`,
para representar os níveis de áudio de um sistema de som estéreo:

```swift
var leftChannel = AudioChannel()
var rightChannel = AudioChannel()
```

<!--
  - test: `staticProperties`

  ```swifttest
  -> var leftChannel = AudioChannel()
  -> var rightChannel = AudioChannel()
  ```
-->

Se você definir o `currentLevel` do canal *esquerdo* como `7`,
verá que a propriedade de tipo `maxInputLevelForAllChannels`
é atualizada para ser igual a `7`:

```swift
leftChannel.currentLevel = 7
print(leftChannel.currentLevel)
// Prints "7".
print(AudioChannel.maxInputLevelForAllChannels)
// Prints "7".
```

<!--
  - test: `staticProperties`

  ```swifttest
  -> leftChannel.currentLevel = 7
  -> print(leftChannel.currentLevel)
  <- 7
  -> print(AudioChannel.maxInputLevelForAllChannels)
  <- 7
  ```
-->

Se você tentar definir o `currentLevel` do canal *direito* como `11`,
verá que a propriedade `currentLevel` do canal direito
é limitada ao valor máximo de `10`,
e a propriedade de tipo `maxInputLevelForAllChannels` é atualizada para ser igual a `10`:

```swift
rightChannel.currentLevel = 11
print(rightChannel.currentLevel)
// Prints "10".
print(AudioChannel.maxInputLevelForAllChannels)
// Prints "10".
```

<!--
  - test: `staticProperties`

  ```swifttest
  -> rightChannel.currentLevel = 11
  -> print(rightChannel.currentLevel)
  <- 10
  -> print(AudioChannel.maxInputLevelForAllChannels)
  <- 10
  ```
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
