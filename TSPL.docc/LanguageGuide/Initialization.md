# Inicialização

Defina os valores iniciais das propriedades armazenadas de um tipo e execute a configuração feita uma única vez.

*Inicialização* é o processo de preparar uma instância
de uma classe, struct ou enum para uso.
Esse processo envolve atribuir um valor inicial a cada propriedade armazenada dessa instância
e executar qualquer outra configuração ou inicialização necessária
antes que a nova instância esteja pronta para uso.

Você implementa esse processo de inicialização definindo *inicializadores*,
que são como métodos especiais que podem ser chamados
para criar uma nova instância de determinado tipo.
Diferentemente dos inicializadores do Objective-C, os inicializadores do Swift não retornam nenhum valor.
O papel principal deles é garantir que as novas instâncias de um tipo
sejam corretamente inicializadas antes de serem usadas pela primeira vez.

Instâncias de tipos classe também podem implementar um *desinicializador*,
que executa qualquer limpeza personalizada logo antes de a instância da classe ser desalocada.
Para mais informações sobre desinicializadores, consulte <doc:Deinitialization>.

## Definindo valores iniciais para propriedades armazenadas

Classes e structs *devem* definir todas as suas propriedades armazenadas
com um valor inicial adequado até o momento em que
uma instância dessa classe ou struct é criada.
Propriedades armazenadas não podem ficar em estado indeterminado.

Você pode definir um valor inicial para uma propriedade armazenada dentro de um inicializador,
ou atribuindo um valor padrão de propriedade como parte da definição dela.
Essas ações são descritas nas seções a seguir.

> Nota: Quando você atribui um valor padrão a uma propriedade armazenada,
> ou define o valor dela dentro de um inicializador,
> o valor da propriedade é definido diretamente,
> sem chamar nenhum observador de propriedade.

### Inicializadores

*Inicializadores* são chamados para criar uma nova instância de determinado tipo.
Na forma mais simples, um inicializador é como um método de instância sem parâmetros,
escrito com a palavra-chave `init`:

```swift
init() {
    // perform some initialization here
}
```

<!--
  - test: `initializerSyntax`

  ```swifttest
  >> class Test {
  -> init() {
        // perform some initialization here
     }
  >> }
  ```
-->

O exemplo a seguir define uma nova struct chamada `Fahrenheit`
para armazenar temperaturas expressas na escala Fahrenheit.
A struct `Fahrenheit` tem uma propriedade armazenada,
`temperature`, do tipo `Double`:

```swift
struct Fahrenheit {
    var temperature: Double
    init() {
        temperature = 32.0
    }
}
var f = Fahrenheit()
print("The default temperature is \(f.temperature)° Fahrenheit")
// Prints "The default temperature is 32.0° Fahrenheit".
```

<!--
  - test: `fahrenheitInit`

  ```swifttest
  -> struct Fahrenheit {
        var temperature: Double
        init() {
           temperature = 32.0
        }
     }
  -> var f = Fahrenheit()
  -> print("The default temperature is \(f.temperature)° Fahrenheit")
  <- The default temperature is 32.0° Fahrenheit
  ```
-->

A struct define um único inicializador, `init`, sem parâmetros,
que inicializa a temperatura armazenada com o valor `32.0`
(o ponto de congelamento da água em graus Fahrenheit).

### Valores padrão de propriedades

Você pode definir o valor inicial de uma propriedade armazenada dentro de um inicializador,
conforme mostrado acima.
Como alternativa, especifique um *valor padrão de propriedade*
como parte da declaração da propriedade.
Você especifica um valor padrão de propriedade atribuindo um valor inicial a ela
no momento em que ela é definida.

> Nota: Se uma propriedade sempre recebe o mesmo valor inicial,
> forneça um valor padrão em vez de definir um valor dentro de um inicializador.
> O resultado final é o mesmo,
> mas o valor padrão vincula a inicialização da propriedade mais de perto à sua declaração.
> Isso deixa os inicializadores mais curtos e claros,
> e permite inferir o tipo da propriedade a partir do valor padrão.
> O valor padrão também facilita aproveitar os inicializadores padrão
> e a herança de inicializadores, conforme descrito mais adiante neste capítulo.

Você pode escrever a struct `Fahrenheit` de cima de um jeito mais simples,
fornecendo um valor padrão para a propriedade `temperature`
no ponto em que a propriedade é declarada:

```swift
struct Fahrenheit {
    var temperature = 32.0
}
```

<!--
  - test: `fahrenheitDefault`

  ```swifttest
  -> struct Fahrenheit {
        var temperature = 32.0
     }
  ```
-->

## Personalizando a inicialização

Você pode personalizar o processo de inicialização
com parâmetros de entrada e tipos optional de propriedade,
ou atribuindo propriedades constantes durante a inicialização,
conforme descrito nas seções a seguir.

### Parâmetros de inicialização

Você pode fornecer *parâmetros de inicialização* como parte da definição de um inicializador,
para definir os tipos e nomes dos valores que personalizam o processo de inicialização.
Os parâmetros de inicialização têm as mesmas capacidades e a mesma sintaxe
que os parâmetros de funções e métodos.

O exemplo a seguir define uma struct chamada `Celsius`,
que armazena temperaturas expressas em graus Celsius.
A struct `Celsius` implementa dois inicializadores personalizados chamados
`init(fromFahrenheit:)` e `init(fromKelvin:)`,
que inicializam uma nova instância da struct
com um valor de outra escala de temperatura:

```swift
struct Celsius {
    var temperatureInCelsius: Double
    init(fromFahrenheit fahrenheit: Double) {
        temperatureInCelsius = (fahrenheit - 32.0) / 1.8
    }
    init(fromKelvin kelvin: Double) {
        temperatureInCelsius = kelvin - 273.15
    }
}
let boilingPointOfWater = Celsius(fromFahrenheit: 212.0)
// boilingPointOfWater.temperatureInCelsius is 100.0
let freezingPointOfWater = Celsius(fromKelvin: 273.15)
// freezingPointOfWater.temperatureInCelsius is 0.0
```

<!--
  - test: `initialization`

  ```swifttest
  -> struct Celsius {
        var temperatureInCelsius: Double
        init(fromFahrenheit fahrenheit: Double) {
           temperatureInCelsius = (fahrenheit - 32.0) / 1.8
        }
        init(fromKelvin kelvin: Double) {
           temperatureInCelsius = kelvin - 273.15
        }
     }
  -> let boilingPointOfWater = Celsius(fromFahrenheit: 212.0)
  /> boilingPointOfWater.temperatureInCelsius is \(boilingPointOfWater.temperatureInCelsius)
  </ boilingPointOfWater.temperatureInCelsius is 100.0
  -> let freezingPointOfWater = Celsius(fromKelvin: 273.15)
  /> freezingPointOfWater.temperatureInCelsius is \(freezingPointOfWater.temperatureInCelsius)
  </ freezingPointOfWater.temperatureInCelsius is 0.0
  ```
-->

O primeiro inicializador tem um único parâmetro de inicialização,
com rótulo de argumento `fromFahrenheit` e nome de parâmetro `fahrenheit`.
O segundo inicializador tem um único parâmetro de inicialização,
com rótulo de argumento `fromKelvin` e nome de parâmetro `kelvin`.
Ambos os inicializadores convertem o único argumento
no valor Celsius correspondente
e armazenam esse valor em uma propriedade chamada `temperatureInCelsius`.

<!--
  TODO: I need to provide an example of default values for initializer parameters,
  to show they can help you to get multiple initializers "for free" (after a fashion).
-->

### Nomes de parâmetros e rótulos de argumento

Assim como nos parâmetros de funções e métodos,
os parâmetros de inicialização podem ter tanto um nome de parâmetro
para uso dentro do corpo do inicializador
quanto um rótulo de argumento para uso ao chamar o inicializador.

No entanto, inicializadores não têm um nome de função identificador antes dos parênteses,
como acontece com funções e métodos.
Por isso, os nomes e os tipos dos parâmetros de um inicializador
têm um papel especialmente importante para identificar qual inicializador deve ser chamado.
Por esse motivo, o Swift fornece um rótulo de argumento automático
para *cada* parâmetro de um inicializador caso você não forneça um.

O exemplo a seguir define uma struct chamada `Color`,
com três propriedades constantes chamadas `red`, `green` e `blue`.
Essas propriedades armazenam um valor entre `0.0` e `1.0`
para indicar a quantidade de vermelho, verde e azul na cor.

`Color` fornece um inicializador com
três parâmetros adequadamente nomeados do tipo `Double`
para seus componentes vermelho, verde e azul.
`Color` também fornece um segundo inicializador com um único parâmetro `white`,
que é usado para fornecer o mesmo valor para os três componentes de cor.

```swift
struct Color {
    let red, green, blue: Double
    init(red: Double, green: Double, blue: Double) {
        self.red   = red
        self.green = green
        self.blue  = blue
    }
    init(white: Double) {
        red   = white
        green = white
        blue  = white
    }
}
```

<!--
  - test: `externalParameterNames, externalParameterNames-err`

  ```swifttest
  -> struct Color {
        let red, green, blue: Double
        init(red: Double, green: Double, blue: Double) {
           self.red   = red
           self.green = green
           self.blue  = blue
        }
        init(white: Double) {
           red   = white
           green = white
           blue  = white
        }
     }
  ```
-->

Os dois inicializadores podem ser usados para criar uma nova instância de `Color`,
fornecendo valores nomeados para cada parâmetro do inicializador:

```swift
let magenta = Color(red: 1.0, green: 0.0, blue: 1.0)
let halfGray = Color(white: 0.5)
```

<!--
  - test: `externalParameterNames`

  ```swifttest
  -> let magenta = Color(red: 1.0, green: 0.0, blue: 1.0)
  -> let halfGray = Color(white: 0.5)
  >> assert(halfGray.red == 0.5)
  >> assert(halfGray.green == 0.5)
  >> assert(halfGray.blue == 0.5)
  ```
-->

Observe que não é possível chamar esses inicializadores
sem usar rótulos de argumento.
Os rótulos de argumento devem sempre ser usados em um inicializador, se forem definidos,
e omiti-los é um erro de compilação:

```swift
let veryGreen = Color(0.0, 1.0, 0.0)
// this reports a compile-time error - argument labels are required
```

<!--
  - test: `externalParameterNames-err`

  ```swifttest
  -> let veryGreen = Color(0.0, 1.0, 0.0)
  // this reports a compile-time error - argument labels are required
  !$ error: missing argument labels 'red:green:blue:' in call
  !! let veryGreen = Color(0.0, 1.0, 0.0)
  !! ^
  !! red: green:  blue:
  ```
-->

### Parâmetros de inicializador sem rótulos de argumento

Se você não quiser usar um rótulo de argumento para um parâmetro de inicializador,
escreva um sublinhado (`_`) no lugar de um rótulo de argumento explícito para esse parâmetro
para substituir o comportamento padrão.

Aqui está uma versão expandida do exemplo `Celsius`
do <doc:Initialization#Initialization-Parameters> acima,
com um inicializador adicional para criar uma nova instância de `Celsius`
a partir de um valor `Double` que já está na escala Celsius:

```swift
struct Celsius {
    var temperatureInCelsius: Double
    init(fromFahrenheit fahrenheit: Double) {
        temperatureInCelsius = (fahrenheit - 32.0) / 1.8
    }
    init(fromKelvin kelvin: Double) {
        temperatureInCelsius = kelvin - 273.15
    }
    init(_ celsius: Double) {
        temperatureInCelsius = celsius
    }
}
let bodyTemperature = Celsius(37.0)
// bodyTemperature.temperatureInCelsius is 37.0
```

<!--
  - test: `initializersWithoutExternalParameterNames`

  ```swifttest
  -> struct Celsius {
        var temperatureInCelsius: Double
        init(fromFahrenheit fahrenheit: Double) {
           temperatureInCelsius = (fahrenheit - 32.0) / 1.8
        }
        init(fromKelvin kelvin: Double) {
           temperatureInCelsius = kelvin - 273.15
        }
        init(_ celsius: Double) {
           temperatureInCelsius = celsius
        }
     }
  -> let bodyTemperature = Celsius(37.0)
  /> bodyTemperature.temperatureInCelsius is \(bodyTemperature.temperatureInCelsius)
  </ bodyTemperature.temperatureInCelsius is 37.0
  ```
-->

A chamada de inicializador `Celsius(37.0)` é clara em sua intenção
sem a necessidade de um rótulo de argumento.
Por isso, é apropriado escrever este inicializador como `init(_ celsius: Double)`
para que ele possa ser chamado fornecendo um valor `Double` sem nome.

### Tipos optional de propriedade

Se seu tipo personalizado tem uma propriedade armazenada que logicamente pode ter “nenhum valor”,
talvez porque o valor dela não possa ser definido durante a inicialização,
ou porque pode ficar com “nenhum valor” em algum momento posterior,
declare a propriedade com um tipo *optional*.
Propriedades de tipo optional são inicializadas automaticamente com o valor `nil`,
indicando que a propriedade foi deliberadamente feita para ter “nenhum valor ainda”
durante a inicialização.

O exemplo a seguir define uma classe chamada `SurveyQuestion`,
com uma propriedade `String` optional chamada `response`:

```swift
class SurveyQuestion {
    var text: String
    var response: String?
    init(text: String) {
        self.text = text
    }
    func ask() {
        print(text)
    }
}
let cheeseQuestion = SurveyQuestion(text: "Do you like cheese?")
cheeseQuestion.ask()
// Prints "Do you like cheese?"
cheeseQuestion.response = "Yes, I do like cheese."
```

<!--
  - test: `surveyQuestionVariable`

  ```swifttest
  -> class SurveyQuestion {
        var text: String
        var response: String?
        init(text: String) {
           self.text = text
        }
        func ask() {
           print(text)
        }
     }
  -> let cheeseQuestion = SurveyQuestion(text: "Do you like cheese?")
  -> cheeseQuestion.ask()
  <- Do you like cheese?
  -> cheeseQuestion.response = "Yes, I do like cheese."
  ```
-->

A resposta a uma pergunta de pesquisa só pode ser conhecida depois que ela é feita,
por isso a propriedade `response` é declarada com o tipo `String?`,
ou “`String` optional”.
Ela recebe automaticamente o valor padrão `nil`, que significa “nenhuma string ainda”,
quando uma nova instância de `SurveyQuestion` é inicializada.

### Atribuindo propriedades constantes durante a inicialização

Você pode atribuir um valor a uma propriedade constante
em qualquer momento durante a inicialização,
desde que ela seja definida com um valor definitivo até o fim da inicialização.
Depois que uma propriedade constante recebe um valor,
ela não pode mais ser modificada.

<!--
  - test: `constantPropertyAssignment`

  ```swifttest
  >> struct S {
        let c: Int
        init() {
           self.c = 1
           self.c = 2
        }
     }
  !$ error: immutable value 'self.c' may only be initialized once
  !! self.c = 2
  !! ^
  !$ note: change 'let' to 'var' to make it mutable
  !! let c: Int
  !! ^~~
  !! var
  ```
-->

<!--
  - test: `constantPropertyAssignmentWithInitialValue`

  ```swifttest
  >> struct S {
        let c: Int = 0
        init() {
           self.c = 1
        }
     }
  !$ error: immutable value 'self.c' may only be initialized once
  !! self.c = 1
  !! ^
  !$ note: initial value already provided in 'let' declaration
  !! let c: Int = 0
  !! ^
  !$ note: change 'let' to 'var' to make it mutable
  !! let c: Int = 0
  !! ^~~
  !! var
  ```
-->

> Nota: Para instâncias de classe,
> uma propriedade constante só pode ser modificada durante a inicialização
> pela classe que a introduz.
> Ela não pode ser modificada por uma subclasse.

Você pode revisar o exemplo `SurveyQuestion` acima para usar
uma propriedade constante em vez de uma propriedade variável para a propriedade `text` da pergunta,
para indicar que a pergunta não muda depois que uma instância de `SurveyQuestion` é criada.
Mesmo que a propriedade `text` agora seja uma constante,
ela ainda pode ser definida dentro do inicializador da classe:

```swift
class SurveyQuestion {
    let text: String
    var response: String?
    init(text: String) {
        self.text = text
    }
    func ask() {
        print(text)
    }
}
let beetsQuestion = SurveyQuestion(text: "How about beets?")
beetsQuestion.ask()
// Prints "How about beets?"
beetsQuestion.response = "I also like beets. (But not with cheese.)"
```

<!--
  - test: `surveyQuestionConstant`

  ```swifttest
  -> class SurveyQuestion {
        let text: String
        var response: String?
        init(text: String) {
           self.text = text
        }
        func ask() {
           print(text)
        }
     }
  -> let beetsQuestion = SurveyQuestion(text: "How about beets?")
  -> beetsQuestion.ask()
  <- How about beets?
  -> beetsQuestion.response = "I also like beets. (But not with cheese.)"
  ```
-->

## Inicializadores padrão

O Swift fornece um *inicializador padrão*
para qualquer struct ou classe
que forneça valores padrão para todas as suas propriedades
e não forneça pelo menos um inicializador por conta própria.
O inicializador padrão simplesmente cria uma nova instância
com todas as suas propriedades definidas com os valores padrão.

<!--
  - test: `defaultInitializersForStructAndClass`

  ```swifttest
  -> struct S { var s: String = "s" }
  -> assert(S().s == "s")
  -> class A { var a: String = "a" }
  -> assert(A().a == "a")
  -> class B: A { var b: String = "b" }
  -> assert(B().a == "a")
  -> assert(B().b ==  "b")
  ```
-->

Este exemplo define uma classe chamada `ShoppingListItem`,
que encapsula o nome, a quantidade e o estado de compra
de um item em uma lista de compras:

```swift
class ShoppingListItem {
    var name: String?
    var quantity = 1
    var purchased = false
}
var item = ShoppingListItem()
```

<!--
  - test: `initialization`

  ```swifttest
  -> class ShoppingListItem {
        var name: String?
        var quantity = 1
        var purchased = false
     }
  -> var item = ShoppingListItem()
  ```
-->

Como todas as propriedades da classe `ShoppingListItem` têm valores padrão,
e por ela ser uma classe base sem superclasse,
`ShoppingListItem` ganha automaticamente uma implementação de inicializador padrão
que cria uma nova instância com todas as suas propriedades definidas com os valores padrão.
(A propriedade `name` é uma propriedade `String` optional,
e por isso recebe automaticamente o valor padrão `nil`,
mesmo que esse valor não esteja escrito no código.)
O exemplo acima usa o inicializador padrão da classe `ShoppingListItem`
para criar uma nova instância da classe com a sintaxe de inicializador,
escrita como `ShoppingListItem()`,
e atribui essa nova instância a uma variável chamada `item`.

### Inicializadores memberwise para structs

Tipos de struct recebem automaticamente um *inicializador memberwise*
se não definirem nenhum inicializador personalizado próprio.
Diferentemente de um inicializador padrão,
a struct recebe um inicializador memberwise
mesmo que tenha propriedades armazenadas sem valores padrão.

<!--
  - test: `memberwiseInitializersDontRequireDefaultStoredPropertyValues`

  ```swifttest
  -> struct S { var int: Int; var string: String }
  -> let s = S(int: 42, string: "hello")

  -> struct SS { var int = 10; var string: String }
  -> let ss = SS(int: 42, string: "hello")
  ```
-->

O inicializador memberwise é uma forma abreviada
de inicializar as propriedades-membro de novas instâncias de struct.
Os valores iniciais das propriedades da nova instância
podem ser passados ao inicializador memberwise pelo nome.

O exemplo a seguir define uma struct chamada `Size`
com duas propriedades chamadas `width` e `height`.
Ambas as propriedades são inferidas como do tipo `Double`
ao receberem o valor padrão `0.0`.

A struct `Size` recebe automaticamente um inicializador memberwise `init(width:height:)`,
que você pode usar para inicializar uma nova instância de `Size`:

```swift
struct Size {
    var width = 0.0, height = 0.0
}
let twoByTwo = Size(width: 2.0, height: 2.0)
```

<!--
  - test: `initialization`

  ```swifttest
  -> struct Size {
        var width = 0.0, height = 0.0
     }
  -> let twoByTwo = Size(width: 2.0, height: 2.0)
  ```
-->

Ao chamar um inicializador memberwise,
você pode omitir valores de quaisquer propriedades
que tenham valores padrão.
No exemplo acima,
a struct `Size` tem um valor padrão
tanto para a propriedade `height` quanto para a `width`.
Você pode omitir uma das propriedades ou as duas,
e o inicializador usa o valor padrão para tudo o que você omitir.
Por exemplo:

```swift
let zeroByTwo = Size(height: 2.0)
print(zeroByTwo.width, zeroByTwo.height)
// Prints "0.0 2.0".

let zeroByZero = Size()
print(zeroByZero.width, zeroByZero.height)
// Prints "0.0 0.0".
```

<!--
  - test: `initialization`

  ```swifttest
  -> let zeroByTwo = Size(height: 2.0)
  -> print(zeroByTwo.width, zeroByTwo.height)
  <- 0.0 2.0

  -> let zeroByZero = Size()
  -> print(zeroByZero.width, zeroByZero.height)
  <- 0.0 0.0
  ```
-->

## Delegação de inicializadores para tipos de valor

Inicializadores podem chamar outros inicializadores para executar parte da inicialização de uma instância.
Esse processo, conhecido como *delegação de inicializadores*,
evita duplicar código entre vários inicializadores.

As regras de como a delegação de inicializadores funciona,
e de quais formas de delegação são permitidas,
são diferentes para tipos de valor e tipos classe.
Tipos de valor (structs e enums) não oferecem suporte a herança,
por isso o processo de delegação de inicializadores deles é relativamente simples,
porque eles só podem delegar para outro inicializador que eles mesmos fornecem.
Já as classes podem herdar de outras classes,
conforme descrito em <doc:Inheritance>.
Isso significa que as classes têm responsabilidades adicionais para garantir que
todas as propriedades armazenadas que elas herdam recebam um valor adequado durante a inicialização.
Essas responsabilidades são descritas em
<doc:Initialization#Class-Inheritance-and-Initialization> abaixo.

Para tipos de valor, você usa `self.init` para se referir a outros inicializadores
do mesmo tipo de valor ao escrever seus próprios inicializadores personalizados.
Você só pode chamar `self.init` dentro de um inicializador.

Observe que, se você definir um inicializador personalizado para um tipo de valor,
você não terá mais acesso ao inicializador padrão
(ou ao inicializador memberwise, se for uma struct) desse tipo.
Essa restrição evita uma situação em que uma configuração essencial adicional
fornecida em um inicializador mais complexo
seja contornada por acidente por alguém que use um dos inicializadores automáticos.

> Nota: Se você quiser que seu tipo de valor personalizado possa ser inicializado com
> o inicializador padrão e o inicializador memberwise,
> e também com seus próprios inicializadores personalizados,
> escreva esses inicializadores personalizados em uma extension
> em vez de na implementação original do tipo de valor.
> Para mais informações, consulte <doc:Extensions>.

O exemplo a seguir define uma struct `Rect` personalizada para representar um retângulo geométrico.
O exemplo exige duas structs auxiliares chamadas `Size` e `Point`,
ambas fornecendo valores padrão de `0.0` para todas as suas propriedades:

```swift
struct Size {
    var width = 0.0, height = 0.0
}
struct Point {
    var x = 0.0, y = 0.0
}
```

<!--
  - test: `valueDelegation`

  ```swifttest
  -> struct Size {
        var width = 0.0, height = 0.0
     }
  -> struct Point {
        var x = 0.0, y = 0.0
     }
  ```
-->

Você pode inicializar a struct `Rect` abaixo de uma de três maneiras:
usando os valores padrão zerados das propriedades `origin` e `size`,
fornecendo um ponto de origem e um tamanho específicos,
ou fornecendo um ponto central e um tamanho específicos.
Essas opções de inicialização são representadas por
três inicializadores personalizados que fazem parte da definição da struct `Rect`:

```swift
struct Rect {
    var origin = Point()
    var size = Size()
    init() {}
    init(origin: Point, size: Size) {
        self.origin = origin
        self.size = size
    }
    init(center: Point, size: Size) {
        let originX = center.x - (size.width / 2)
        let originY = center.y - (size.height / 2)
        self.init(origin: Point(x: originX, y: originY), size: size)
    }
}
```

<!--
  - test: `valueDelegation`

  ```swifttest
  -> struct Rect {
        var origin = Point()
        var size = Size()
        init() {}
        init(origin: Point, size: Size) {
           self.origin = origin
           self.size = size
        }
        init(center: Point, size: Size) {
           let originX = center.x - (size.width / 2)
           let originY = center.y - (size.height / 2)
           self.init(origin: Point(x: originX, y: originY), size: size)
        }
     }
  ```
-->

O primeiro inicializador de `Rect`, `init()`,
é funcionalmente igual ao inicializador padrão que a struct teria recebido
se não tivesse os próprios inicializadores personalizados.
Esse inicializador tem um corpo vazio,
representado por um par de chaves vazio `{}`.
Chamar esse inicializador retorna uma instância de `Rect` cujas
propriedades `origin` e `size` são ambas inicializadas com
os valores padrão `Point(x: 0.0, y: 0.0)`
e `Size(width: 0.0, height: 0.0)`
definidos na declaração das propriedades:

```swift
let basicRect = Rect()
// basicRect's origin is (0.0, 0.0) and its size is (0.0, 0.0)
```

<!--
  - test: `valueDelegation`

  ```swifttest
  -> let basicRect = Rect()
  /> basicRect's origin is (\(basicRect.origin.x), \(basicRect.origin.y)) and its size is (\(basicRect.size.width), \(basicRect.size.height))
  </ basicRect's origin is (0.0, 0.0) and its size is (0.0, 0.0)
  ```
-->

O segundo inicializador de `Rect`, `init(origin:size:)`,
é funcionalmente igual ao inicializador memberwise que a struct teria recebido
se não tivesse os próprios inicializadores personalizados.
Esse inicializador simplesmente atribui os valores dos argumentos `origin` e `size`
às respectivas propriedades armazenadas:

```swift
let originRect = Rect(origin: Point(x: 2.0, y: 2.0),
    size: Size(width: 5.0, height: 5.0))
// originRect's origin is (2.0, 2.0) and its size is (5.0, 5.0)
```

<!--
  - test: `valueDelegation`

  ```swifttest
  -> let originRect = Rect(origin: Point(x: 2.0, y: 2.0),
        size: Size(width: 5.0, height: 5.0))
  /> originRect's origin is (\(originRect.origin.x), \(originRect.origin.y)) and its size is (\(originRect.size.width), \(originRect.size.height))
  </ originRect's origin is (2.0, 2.0) and its size is (5.0, 5.0)
  ```
-->

O terceiro inicializador de `Rect`, `init(center:size:)`, é um pouco mais complexo.
Ele começa calculando um ponto de origem adequado com base
em um ponto `center` e em um valor `size`.
Em seguida, ele chama (ou *delega*) o inicializador `init(origin:size:)`,
que armazena os novos valores de origem e tamanho nas propriedades apropriadas:

```swift
let centerRect = Rect(center: Point(x: 4.0, y: 4.0),
    size: Size(width: 3.0, height: 3.0))
// centerRect's origin is (2.5, 2.5) and its size is (3.0, 3.0)
```

<!--
  - test: `valueDelegation`

  ```swifttest
  -> let centerRect = Rect(center: Point(x: 4.0, y: 4.0),
        size: Size(width: 3.0, height: 3.0))
  /> centerRect's origin is (\(centerRect.origin.x), \(centerRect.origin.y)) and its size is (\(centerRect.size.width), \(centerRect.size.height))
  </ centerRect's origin is (2.5, 2.5) and its size is (3.0, 3.0)
  ```
-->

O inicializador `init(center:size:)` poderia ter atribuído ele mesmo
os novos valores de `origin` e `size` às propriedades apropriadas.
No entanto, é mais conveniente (e mais claro na intenção)
que o inicializador `init(center:size:)` aproveite um inicializador existente
que já oferece exatamente essa funcionalidade.

> Nota: Para uma forma alternativa de escrever este exemplo sem definir
> os inicializadores `init()` e `init(origin:size:)` por conta própria,
> consulte <doc:Extensions>.

## Herança de classes e inicialização

Todas as propriedades armazenadas de uma classe,
inclusive quaisquer propriedades que a classe herda da sua superclasse,
*devem* receber um valor inicial durante a inicialização.

O Swift define dois tipos de inicializadores para tipos classe
para ajudar a garantir que todas as propriedades armazenadas recebam um valor inicial.
Esses inicializadores são conhecidos como inicializadores designados e inicializadores de conveniência.

### Inicializadores designados e inicializadores de conveniência

*Inicializadores designados* são os inicializadores principais de uma classe.
Um inicializador designado inicializa completamente todas as propriedades introduzidas por essa classe
e chama um inicializador apropriado da superclasse
para continuar o processo de inicialização ao longo da cadeia de superclasses.

As classes costumam ter poucos inicializadores designados,
e é bastante comum uma classe ter apenas um.
Inicializadores designados são pontos de “funil” pelos quais a inicialização acontece,
e pelos quais o processo de inicialização continua ao longo da cadeia de superclasses.

Toda classe deve ter pelo menos um inicializador designado.
Em alguns casos, esse requisito é atendido
herdando um ou mais inicializadores designados de uma superclasse,
conforme descrito em <doc:Initialization#Automatic-Initializer-Inheritance> abaixo.

*Inicializadores de conveniência* são inicializadores secundários e de apoio para uma classe.
Você pode definir um inicializador de conveniência para chamar um inicializador designado
da mesma classe do inicializador de conveniência,
com alguns dos parâmetros do inicializador designado definidos com valores padrão.
Você também pode definir um inicializador de conveniência para criar
uma instância dessa classe para um caso de uso específico ou um tipo de valor de entrada.

Você não precisa fornecer inicializadores de conveniência se a sua classe não precisar deles.
Crie inicializadores de conveniência sempre que um atalho para um padrão comum de inicialização
economizar tempo ou deixar a inicialização da classe mais clara em sua intenção.

### Sintaxe de inicializadores designados e de conveniência

Inicializadores designados de classes são escritos da mesma forma que
os inicializadores simples de tipos de valor:

```swift
init(<#parameters#>) {
   <#statements#>
}
```

Inicializadores de conveniência são escritos no mesmo estilo,
mas com o modificador `convenience` colocado antes da palavra-chave `init`,
separado por um espaço:

```swift
convenience init(<#parameters#>) {
   <#statements#>
}
```

### Delegação de inicializadores para tipos classe

Para simplificar as relações entre inicializadores designados e de conveniência,
o Swift aplica as três regras a seguir para chamadas de delegação entre inicializadores:

- term **Regra 1**:
  Um inicializador designado deve chamar um inicializador designado da sua superclasse imediata.

- term **Regra 2**:
  Um inicializador de conveniência deve chamar outro inicializador da *mesma* classe.

- term **Regra 3**:
  Um inicializador de conveniência deve, em última instância, chamar um inicializador designado.

Uma forma simples de lembrar isso é:

- Inicializadores designados devem sempre delegar *para cima*.
- Inicializadores de conveniência devem sempre delegar *para o lado*.

Essas regras são ilustradas na figura abaixo:

![](initializerDelegation01)

Aqui, a superclasse tem um único inicializador designado e dois inicializadores de conveniência.
Um inicializador de conveniência chama outro inicializador de conveniência,
que por sua vez chama o único inicializador designado.
Isso satisfaz as regras 2 e 3 acima.
A superclasse não tem uma superclasse própria, por isso a regra 1 não se aplica.

A subclasse desta figura tem dois inicializadores designados e um inicializador de conveniência.
O inicializador de conveniência deve chamar um dos dois inicializadores designados,
pois ele só pode chamar outro inicializador da mesma classe.
Isso satisfaz as regras 2 e 3 acima.
Os dois inicializadores designados devem chamar o único inicializador designado
da superclasse, para satisfazer a regra 1 acima.

> Nota: Essas regras não afetam como os usuários das suas classes *criam* instâncias de cada classe.
> Qualquer inicializador do diagrama acima pode ser usado para criar
> uma instância totalmente inicializada da classe à qual ele pertence.
> As regras afetam apenas como você escreve a implementação dos inicializadores da classe.

A figura abaixo mostra uma hierarquia de classes mais complexa, com quatro classes.
Ela ilustra como os inicializadores designados dessa hierarquia
atuam como pontos de “funil” para a inicialização das classes,
simplificando as inter-relações entre as classes da cadeia:

![](initializerDelegation02)

### Inicialização em duas fases

A inicialização de classes no Swift é um processo em duas fases.
Na primeira fase, cada propriedade armazenada recebe um valor inicial
pela classe que a introduziu.
Depois que o estado inicial de cada propriedade armazenada tiver sido determinado,
a segunda fase começa,
e cada classe tem a oportunidade de personalizar ainda mais as suas propriedades armazenadas
antes de a nova instância ser considerada pronta para uso.

O uso de um processo de inicialização em duas fases torna a inicialização segura,
ao mesmo tempo que dá total flexibilidade a cada classe de uma hierarquia de classes.
A inicialização em duas fases impede que valores de propriedades
sejam acessados antes de serem inicializados,
e impede que valores de propriedades sejam alterados para outro valor
por outro inicializador de forma inesperada.

> Nota: O processo de inicialização em duas fases do Swift é semelhante à inicialização no Objective-C.
> A principal diferença é que, durante a fase 1,
> o Objective-C atribui valores zero ou nulos (como `0` ou `nil`) a todas as propriedades.
> O fluxo de inicialização do Swift é mais flexível,
> pois permite definir valores iniciais personalizados,
> e lida com tipos para os quais `0` ou `nil` não é um valor padrão válido.

O compilador do Swift executa quatro verificações de segurança úteis para garantir que
a inicialização em duas fases seja concluída sem erros:

- term **Verificação de segurança 1**:
  Um inicializador designado deve garantir que todas as propriedades introduzidas pela sua classe
  estejam inicializadas antes de delegar para um inicializador da superclasse.

Como mencionado acima,
a memória de um objeto só é considerada totalmente inicializada
quando o estado inicial de todas as suas propriedades armazenadas for conhecido.
Para que essa regra seja cumprida, um inicializador designado deve garantir que
todas as suas próprias propriedades estejam inicializadas antes de passar a responsabilidade para cima na cadeia.

- term **Verificação de segurança 2**:
  Um inicializador designado deve delegar para um inicializador da superclasse
  antes de atribuir um valor a uma propriedade herdada.
  Se não fizer isso, o novo valor que o inicializador designado atribui
  será sobrescrito pela superclasse como parte da própria inicialização.

- term **Verificação de segurança 3**:
  Um inicializador de conveniência deve delegar para outro inicializador
  antes de atribuir um valor a *qualquer* propriedade
  (inclusive propriedades definidas pela própria classe).
  Se não fizer isso, o novo valor que o inicializador de conveniência atribui
  será sobrescrito pelo inicializador designado da própria classe.

- term **Verificação de segurança 4**:
  Um inicializador não pode chamar métodos de instância,
  ler os valores de propriedades de instância,
  nem se referir a `self` como um valor
  até que a primeira fase da inicialização esteja concluída.

A instância da classe só é totalmente válida quando a primeira fase termina.
As propriedades só podem ser acessadas, e os métodos só podem ser chamados,
quando a instância da classe é considerada válida no fim da primeira fase.

Veja como a inicialização em duas fases acontece, com base nas quatro verificações de segurança acima:

**Fase 1**

- Um inicializador designado ou de conveniência é chamado em uma classe.
- Memória para uma nova instância dessa classe é alocada.
  A memória ainda não está inicializada.
- Um inicializador designado dessa classe confirma que
  todas as propriedades armazenadas introduzidas por essa classe têm um valor.
  A memória dessas propriedades armazenadas agora está inicializada.
- O inicializador designado passa a responsabilidade para um inicializador da superclasse,
  para executar a mesma tarefa para as próprias propriedades armazenadas dela.
- Isso continua subindo pela cadeia de herança de classes até chegar ao topo da cadeia.
- Quando o topo da cadeia é alcançado,
  e a última classe da cadeia garante que todas as suas propriedades armazenadas têm um valor,
  a memória da instância é considerada totalmente inicializada, e a fase 1 está concluída.

**Fase 2**

- Descendo de volta a partir do topo da cadeia,
  cada inicializador designado da cadeia tem a opção de personalizar ainda mais a instância.
  Os inicializadores agora podem acessar `self`
  e modificar as suas propriedades, chamar os seus métodos de instância e assim por diante.
- Por fim, quaisquer inicializadores de conveniência da cadeia têm a opção
  de personalizar a instância e trabalhar com `self`.

Veja como a fase 1 fica em uma chamada de inicialização para uma subclasse e uma superclasse hipotéticas:

![](twoPhaseInitialization01)

Neste exemplo, a inicialização começa com a chamada
de um inicializador de conveniência da subclasse.
Esse inicializador de conveniência ainda não pode modificar nenhuma propriedade.
Ele delega para o lado, para um inicializador designado da mesma classe.

O inicializador designado garante que todas as propriedades da subclasse tenham um valor,
conforme a verificação de segurança 1. Em seguida, ele chama um inicializador designado da sua superclasse
para continuar a inicialização pela cadeia.

O inicializador designado da superclasse garante que
todas as propriedades da superclasse tenham um valor.
Não há mais superclasses para inicializar,
e por isso não é necessária mais nenhuma delegação.

Assim que todas as propriedades da superclasse tiverem um valor inicial,
sua memória é considerada totalmente inicializada, e a fase 1 está concluída.

Veja como a fase 2 fica para a mesma chamada de inicialização:

![](twoPhaseInitialization02)

O inicializador designado da superclasse agora tem a oportunidade
de personalizar ainda mais a instância
(embora não precise fazer isso).

Quando o inicializador designado da superclasse termina,
o inicializador designado da subclasse pode executar personalizações adicionais
(embora, novamente, não precise fazer isso).

Por fim, quando o inicializador designado da subclasse termina,
o inicializador de conveniência que foi chamado originalmente
pode executar personalizações adicionais.

### Herança e sobrescrita de inicializadores

Diferentemente das subclasses no Objective-C,
as subclasses do Swift não herdam os inicializadores da superclasse por padrão.
A abordagem do Swift evita uma situação em que um inicializador simples de uma superclasse
é herdado por uma subclasse mais especializada
e usado para criar uma nova instância da subclasse
que não esteja totalmente ou corretamente inicializada.

> Nota: Inicializadores da superclasse *são* herdados em certas circunstâncias,
> mas somente quando isso é seguro e apropriado.
> Para mais informações, consulte <doc:Initialization#Automatic-Initializer-Inheritance> abaixo.

Se você quiser que uma subclasse personalizada apresente
um ou mais dos mesmos inicializadores da sua superclasse,
pode fornecer uma implementação personalizada desses inicializadores dentro da subclasse.

Quando você escreve um inicializador de subclasse que corresponde a um inicializador *designado* da superclasse,
você está, na prática, fornecendo uma sobrescrita desse inicializador designado.
Por isso, você deve escrever o modificador `override` antes da definição do inicializador da subclasse.
Isso vale mesmo quando você está sobrescrevendo um inicializador padrão fornecido automaticamente,
conforme descrito em <doc:Initialization#Default-Initializers>.

Assim como com uma propriedade, método ou subscript sobrescrito,
a presença do modificador `override` faz o Swift verificar se
a superclasse tem um inicializador designado correspondente a ser sobrescrito,
e valida se os parâmetros do seu inicializador sobrescrito foram especificados como pretendido.

> Nota: Você sempre escreve o modificador `override` ao sobrescrever um inicializador designado da superclasse,
> mesmo que a implementação do inicializador na sua subclasse seja um inicializador de conveniência.

<!--
  - test: `youHaveToWriteOverrideWhenOverridingADesignatedInitializer`

  ```swifttest
  -> class C {
        init() {}
     }
  -> class D1: C {
        // this is correct
        override init() {}
     }
  -> class D2: C {
        // this isn't correct
        init() {}
     }
  !$ error: overriding declaration requires an 'override' keyword
  !! init() {}
  !! ^
  !! override
  !$ note: overridden declaration is here
  !! init() {}
  !! ^
  ```
-->

<!--
  - test: `youHaveToWriteOverrideEvenWhenOverridingADefaultInitializer`

  ```swifttest
  -> class C {
        var i = 0
     }
  -> class D1: C {
        // this is correct
        override init() {}
     }
  -> class D2: C {
        // this isn't correct
        init() {}
     }
  !$ error: overriding declaration requires an 'override' keyword
  !! init() {}
  !! ^
  !! override
  !$ note: overridden declaration is here
  !! class C {
  !! ^
  ```
-->

Por outro lado, se você escreve um inicializador de subclasse que corresponde a um inicializador de conveniência da superclasse,
esse inicializador de conveniência da superclasse nunca pode ser chamado diretamente pela sua subclasse,
conforme as regras descritas acima em <doc:Initialization#Initializer-Delegation-for-Class-Types>.
Por isso, sua subclasse não está (estritamente falando) sobrescrevendo o inicializador da superclasse.
Como resultado, você não escreve o modificador `override` ao fornecer
uma implementação correspondente de um inicializador de conveniência da superclasse.

<!--
  - test: `youDoNotAndCannotWriteOverrideWhenOverridingAConvenienceInitializer`

  ```swifttest
  -> class C {
        var i: Int
        init(someInt: Int) {
           i = someInt
        }
        convenience init() {
           self.init(someInt: 42)
        }
     }
  -> class D1: C {
        // override for designated, so needs the override modifier
        override init(someInt: Int) {
           super.init(someInt: someInt)
        }
        // not technically an override, so doesn't need the override modifier
        convenience init() {
           self.init(someInt: 42)
        }
     }
  -> class D2: C {
        // override for designated, so needs the override modifier
        override init(someInt: Int) {
           super.init(someInt: someInt)
        }
        // this isn't correct - "override" isn't required
        override convenience init() {
           self.init(someInt: 42)
        }
     }
  !$ error: initializer does not override a designated initializer from its superclass
  !! override convenience init() {
  !! ~~~~~~~~             ^
  !$ note: attempt to override convenience initializer here
  !! convenience init() {
  !! ^
  ```
-->

O exemplo a seguir define uma classe base chamada `Vehicle`.
Essa classe base declara uma propriedade armazenada chamada `numberOfWheels`,
com valor padrão `Int` de `0`.
A propriedade `numberOfWheels` é usada por uma propriedade computada chamada `description`
para criar uma descrição `String` das características do veículo:

```swift
class Vehicle {
    var numberOfWheels = 0
    var description: String {
        return "\(numberOfWheels) wheel(s)"
    }
}
```

<!--
  - test: `initializerInheritance`

  ```swifttest
  -> class Vehicle {
        var numberOfWheels = 0
        var description: String {
           return "\(numberOfWheels) wheel(s)"
        }
     }
  ```
-->

A classe `Vehicle` fornece um valor padrão para sua única propriedade armazenada
e não fornece nenhum inicializador personalizado por conta própria.
Como resultado, ela recebe automaticamente um inicializador padrão,
conforme descrito em <doc:Initialization#Default-Initializers>.
O inicializador padrão (quando disponível) é sempre um inicializador designado de uma classe
e pode ser usado para criar uma nova instância de `Vehicle` com `numberOfWheels` igual a `0`:

```swift
let vehicle = Vehicle()
print("Vehicle: \(vehicle.description)")
// Vehicle: 0 wheel(s)
```

<!--
  - test: `initializerInheritance`

  ```swifttest
  -> let vehicle = Vehicle()
  -> print("Vehicle: \(vehicle.description)")
  </ Vehicle: 0 wheel(s)
  ```
-->

O próximo exemplo define uma subclasse de `Vehicle` chamada `Bicycle`:

```swift
class Bicycle: Vehicle {
    override init() {
        super.init()
        numberOfWheels = 2
    }
}
```

<!--
  - test: `initializerInheritance`

  ```swifttest
  -> class Bicycle: Vehicle {
        override init() {
           super.init()
           numberOfWheels = 2
        }
     }
  ```
-->

A subclasse `Bicycle` define um inicializador designado personalizado, `init()`.
Esse inicializador designado corresponde a um inicializador designado da superclasse de `Bicycle`,
por isso a versão de `Bicycle` desse inicializador é marcada com o modificador `override`.

O inicializador `init()` de `Bicycle` começa chamando `super.init()`,
que chama o inicializador padrão da superclasse de `Bicycle`, `Vehicle`.
Isso garante que a propriedade herdada `numberOfWheels` seja inicializada por `Vehicle`
antes que `Bicycle` tenha a oportunidade de modificar a propriedade.
Depois de chamar `super.init()`,
o valor original de `numberOfWheels` é substituído por um novo valor de `2`.

Se você criar uma instância de `Bicycle`,
pode chamar a propriedade computada herdada `description`
para ver como a propriedade `numberOfWheels` foi atualizada:

```swift
let bicycle = Bicycle()
print("Bicycle: \(bicycle.description)")
// Bicycle: 2 wheel(s)
```

<!--
  - test: `initializerInheritance`

  ```swifttest
  -> let bicycle = Bicycle()
  -> print("Bicycle: \(bicycle.description)")
  </ Bicycle: 2 wheel(s)
  ```
-->

Se um inicializador de subclasse não faz nenhuma personalização
na fase 2 do processo de inicialização,
e a superclasse tem um inicializador designado síncrono sem argumentos,
é possível omitir a chamada a `super.init()`
depois de atribuir valores a todas as propriedades armazenadas da subclasse.
Se o inicializador da superclasse for assíncrono,
você precisa escrever `await super.init()` explicitamente.

Este exemplo define outra subclasse de `Vehicle`, chamada `Hoverboard`.
No inicializador dela, a classe `Hoverboard` define apenas a propriedade `color`.
Em vez de fazer uma chamada explícita a `super.init()`,
este inicializador depende de uma chamada implícita ao inicializador da superclasse
para concluir o processo.

```swift
class Hoverboard: Vehicle {
    var color: String
    init(color: String) {
        self.color = color
        // super.init() implicitly called here
    }
    override var description: String {
        return "\(super.description) in a beautiful \(color)"
    }
}
```

<!--
  - test: `initializerInheritance`

  ```swifttest
  -> class Hoverboard: Vehicle {
         var color: String
         init(color: String) {
             self.color = color
             // super.init() implicitly called here
         }
         override var description: String {
             return "\(super.description) in a beautiful \(color)"
         }
     }
  ```
-->

Uma instância de `Hoverboard` usa o número padrão de rodas
fornecido pelo inicializador de `Vehicle`.

```swift
let hoverboard = Hoverboard(color: "silver")
print("Hoverboard: \(hoverboard.description)")
// Hoverboard: 0 wheel(s) in a beautiful silver
```

<!--
  - test: `initializerInheritance`

  ```swifttest
  -> let hoverboard = Hoverboard(color: "silver")
  -> print("Hoverboard: \(hoverboard.description)")
  </ Hoverboard: 0 wheel(s) in a beautiful silver
  ```
-->

> Nota: Subclasses podem modificar propriedades variáveis herdadas durante a inicialização,
> mas não podem modificar propriedades constantes herdadas.

<!--
  - test: `youCantModifyInheritedConstantPropertiesFromASuperclass`

  ```swifttest
  -> class C {
        let constantProperty: Int
        var variableProperty: Int
        init() {
           // this is fine - a class can set its own constant and variable properties during init
           constantProperty = 0
           variableProperty = 0
        }
     }
  -> class D1: C {
        override init() {
           // this is fine - a subclass can set its superclass's variable properties during init
           super.init()
           variableProperty = 0
        }
     }
  -> class D2: C {
        override init() {
           // this is wrong - a subclass can't set its superclass's constant properties during init
           super.init()
           constantProperty = 0
        }
     }
  !$ error: cannot assign to property: 'constantProperty' is a 'let' constant
  !! constantProperty = 0
  !! ^~~~~~~~~~~~~~~~
  !$ note: change 'let' to 'var' to make it mutable
  !! let constantProperty: Int
  !! ^~~
  !! var
  ```
-->

### Herança automática de inicializadores

Como mencionado acima,
subclasses não herdam os inicializadores da superclasse por padrão.
No entanto, os inicializadores da superclasse *são* herdados automaticamente se certas condições forem atendidas.
Na prática, isso significa que
você não precisa escrever sobrescritas de inicializadores em muitos cenários comuns,
e pode herdar os inicializadores da superclasse com esforço mínimo sempre que isso for seguro.

Supondo que você forneça valores padrão para quaisquer novas propriedades que introduzir em uma subclasse,
valem as duas regras a seguir:

- term **Regra 1**:
  Se a sua subclasse não definir nenhum inicializador designado,
  ela herda automaticamente todos os inicializadores designados da superclasse.

- term **Regra 2**:
  Se a sua subclasse fornecer uma implementação de
  *todos* os inicializadores designados da superclasse,
  seja herdando-os conforme a regra 1,
  seja fornecendo uma implementação personalizada como parte da sua definição,
  então ela herda automaticamente todos os inicializadores de conveniência da superclasse.

Essas regras valem mesmo que a sua subclasse adicione mais inicializadores de conveniência.

> Nota: Uma subclasse pode implementar um inicializador designado da superclasse
> como um inicializador de conveniência da subclasse, como parte do cumprimento da regra 2.

<!--
  TODO: feedback from Beto is that this note is a little hard to parse.
  Perhaps this point should be left until the later "in action" example,
  where this principle is demonstrated?
-->

<!--
  TODO: There are rare cases in which we automatically insert a call to super.init() for you.
  When is this? Either way, I need to mention it in here.
-->

### Inicializadores designados e de conveniência na prática

O exemplo a seguir mostra inicializadores designados, inicializadores de conveniência
e herança automática de inicializadores na prática.
Este exemplo define uma hierarquia de três classes chamadas
`Food`, `RecipeIngredient` e `ShoppingListItem`,
e demonstra como os inicializadores delas interagem.

A classe base da hierarquia se chama `Food`,
uma classe simples para encapsular o nome de um alimento.
A classe `Food` introduz uma única propriedade `String` chamada `name`
e fornece dois inicializadores para criar instâncias de `Food`:

```swift
class Food {
    var name: String
    init(name: String) {
        self.name = name
    }
    convenience init() {
        self.init(name: "[Unnamed]")
    }
}
```

<!--
  - test: `designatedConvenience`

  ```swifttest
  -> class Food {
        var name: String
        init(name: String) {
           self.name = name
        }
        convenience init() {
           self.init(name: "[Unnamed]")
        }
     }
  ```
-->

A figura abaixo mostra a cadeia de inicializadores da classe `Food`:

![](initializersExample01)

Classes não têm um inicializador memberwise padrão,
por isso a classe `Food` fornece um inicializador designado
que recebe um único argumento chamado `name`.
Esse inicializador pode ser usado para criar uma nova instância de `Food` com um nome específico:

```swift
let namedMeat = Food(name: "Bacon")
// namedMeat's name is "Bacon"
```

<!--
  - test: `designatedConvenience`

  ```swifttest
  -> let namedMeat = Food(name: "Bacon")
  /> namedMeat's name is \"\(namedMeat.name)\"
  </ namedMeat's name is "Bacon"
  ```
-->

O inicializador `init(name: String)` da classe `Food`
é fornecido como *designado*,
pois garante que todas as propriedades armazenadas de
uma nova instância de `Food` sejam totalmente inicializadas.
A classe `Food` não tem superclasse,
por isso o inicializador `init(name: String)` não precisa chamar `super.init()`
para concluir a inicialização.

A classe `Food` também fornece um inicializador de *conveniência*, `init()`, sem argumentos.
O inicializador `init()` fornece um nome provisório padrão para um novo alimento
delegando para o lado, para o `init(name: String)` da classe `Food`, com
um valor `name` igual a `[Unnamed]`:

```swift
let mysteryMeat = Food()
// mysteryMeat's name is "[Unnamed]"
```

<!--
  - test: `designatedConvenience`

  ```swifttest
  -> let mysteryMeat = Food()
  /> mysteryMeat's name is \"\(mysteryMeat.name)\"
  </ mysteryMeat's name is "[Unnamed]"
  ```
-->

A segunda classe da hierarquia é uma subclasse de `Food` chamada `RecipeIngredient`.
A classe `RecipeIngredient` modela um ingrediente em uma receita de culinária.
Ela introduz uma propriedade `Int` chamada `quantity`
(além da propriedade `name` que herda de `Food`)
e define dois inicializadores para criar instâncias de `RecipeIngredient`:

```swift
class RecipeIngredient: Food {
    var quantity: Int
    init(name: String, quantity: Int) {
        self.quantity = quantity
        super.init(name: name)
    }
    override convenience init(name: String) {
        self.init(name: name, quantity: 1)
    }
}
```

<!--
  - test: `designatedConvenience`

  ```swifttest
  -> class RecipeIngredient: Food {
        var quantity: Int
        init(name: String, quantity: Int) {
           self.quantity = quantity
           super.init(name: name)
        }
        override convenience init(name: String) {
           self.init(name: name, quantity: 1)
        }
     }
  ```
-->

A figura abaixo mostra a cadeia de inicializadores da classe `RecipeIngredient`:

![](initializersExample02)

A classe `RecipeIngredient` tem um único inicializador designado,
`init(name: String, quantity: Int)`,
que pode ser usado para preencher todas as propriedades de uma nova instância de `RecipeIngredient`.
Esse inicializador começa atribuindo
o argumento `quantity` recebido à propriedade `quantity`,
que é a única propriedade nova introduzida por `RecipeIngredient`.
Depois disso, o inicializador delega para
o inicializador `init(name: String)` da classe `Food`.
Esse processo satisfaz a verificação de segurança 1
de <doc:Initialization#Two-Phase-Initialization> acima.

`RecipeIngredient` também define um inicializador de conveniência, `init(name: String)`,
usado para criar uma instância de `RecipeIngredient` apenas com o nome.
Esse inicializador de conveniência considera a quantidade igual a `1`
para qualquer instância de `RecipeIngredient` criada sem uma quantidade explícita.
A definição desse inicializador de conveniência torna
as instâncias de `RecipeIngredient` mais rápidas e convenientes de criar,
e evita duplicação de código ao criar
várias instâncias de `RecipeIngredient` com quantidade única.
Esse inicializador de conveniência simplesmente delega para o lado, para o inicializador designado da classe,
passando o valor `quantity` igual a `1`.

O inicializador de conveniência `init(name: String)` fornecido por `RecipeIngredient`
recebe os mesmos parâmetros do inicializador *designado* `init(name: String)` de `Food`.
Como esse inicializador de conveniência sobrescreve um inicializador designado da sua superclasse,
ele deve ser marcado com o modificador `override`
(conforme descrito em <doc:Initialization#Initializer-Inheritance-and-Overriding>).

Mesmo que `RecipeIngredient` forneça
o inicializador `init(name: String)` como um inicializador de conveniência,
`RecipeIngredient` ainda assim forneceu uma implementação de
todos os inicializadores designados da sua superclasse.
Por isso, `RecipeIngredient` herda automaticamente
todos os inicializadores de conveniência da superclasse também.

Neste exemplo, a superclasse de `RecipeIngredient` é `Food`,
que tem um único inicializador de conveniência chamado `init()`.
Esse inicializador, portanto, é herdado por `RecipeIngredient`.
A versão herdada de `init()` funciona exatamente da mesma forma que a versão de `Food`,
exceto que ela delega para a versão de `RecipeIngredient` de `init(name: String)`
em vez da versão de `Food`.

Todos esses três inicializadores podem ser usados para criar novas instâncias de `RecipeIngredient`:

```swift
let oneMysteryItem = RecipeIngredient()
let oneBacon = RecipeIngredient(name: "Bacon")
let sixEggs = RecipeIngredient(name: "Eggs", quantity: 6)
```

<!--
  - test: `designatedConvenience`

  ```swifttest
  -> let oneMysteryItem = RecipeIngredient()
  -> let oneBacon = RecipeIngredient(name: "Bacon")
  -> let sixEggs = RecipeIngredient(name: "Eggs", quantity: 6)
  ```
-->

A terceira e última classe da hierarquia é
uma subclasse de `RecipeIngredient` chamada `ShoppingListItem`.
A classe `ShoppingListItem` modela um ingrediente de receita como ele aparece em uma lista de compras.

Todo item da lista de compras começa como “não comprado”.
Para representar esse fato,
`ShoppingListItem` introduz uma propriedade booleana chamada `purchased`,
com valor padrão `false`.
`ShoppingListItem` também adiciona uma propriedade computada `description`,
que fornece uma descrição textual de uma instância de `ShoppingListItem`:

```swift
class ShoppingListItem: RecipeIngredient {
    var purchased = false
    var description: String {
        var output = "\(quantity) x \(name)"
        output += purchased ? " ✔" : " ✘"
        return output
    }
}
```

<!--
  - test: `designatedConvenience`

  ```swifttest
  -> class ShoppingListItem: RecipeIngredient {
        var purchased = false
        var description: String {
           var output = "\(quantity) x \(name)"
           output += purchased ? " ✔" : " ✘"
           return output
        }
     }
  ```
-->

> Nota: `ShoppingListItem` não define um inicializador para fornecer
> um valor inicial para `purchased`,
> porque itens de uma lista de compras (como modelados aqui) sempre começam como não comprados.

Como ela fornece um valor padrão para todas as propriedades que introduz
e não define nenhum inicializador por conta própria,
`ShoppingListItem` herda automaticamente
*todos* os inicializadores designados e de conveniência da sua superclasse.

A figura abaixo mostra a cadeia geral de inicializadores das três classes:

![](initializersExample03)

Você pode usar os três inicializadores herdados
para criar uma nova instância de `ShoppingListItem`:

```swift
var breakfastList = [
    ShoppingListItem(),
    ShoppingListItem(name: "Bacon"),
    ShoppingListItem(name: "Eggs", quantity: 6),
]
breakfastList[0].name = "Orange juice"
breakfastList[0].purchased = true
for item in breakfastList {
    print(item.description)
}
// 1 x Orange juice ✔
// 1 x Bacon ✘
// 6 x Eggs ✘
```

<!--
  - test: `designatedConvenience`

  ```swifttest
  -> var breakfastList = [
        ShoppingListItem(),
        ShoppingListItem(name: "Bacon"),
        ShoppingListItem(name: "Eggs", quantity: 6),
     ]
  -> breakfastList[0].name = "Orange juice"
  -> breakfastList[0].purchased = true
  -> for item in breakfastList {
        print(item.description)
     }
  </ 1 x Orange juice ✔
  </ 1 x Bacon ✘
  </ 6 x Eggs ✘
  ```
-->

Aqui, um novo array chamado `breakfastList` é criado a partir
de um literal de array que contém três novas instâncias de `ShoppingListItem`.
O tipo do array é inferido como `[ShoppingListItem]`.
Depois que o array é criado,
o nome do `ShoppingListItem` no início do array
é alterado de `"[Unnamed]"` para `"Orange juice"`
e ele é marcado como comprado.
Imprimir a descrição de cada item do array
mostra que os estados padrão deles foram definidos conforme o esperado.

<!--
  TODO: talk about the general factory initializer pattern,
  and how Swift's approach to initialization removes the need for most factories.
-->

<!--
  NOTE: We import some Obj-C-imported factory initializers as init() -> MyType,
  but you can't currently write these in Swift yourself.
  After conferring with Doug, I've decided not to include these in the Guide
  if you can't write them yourself in pure Swift.
-->

<!--
  TODO: Feedback from Beto is that it would be useful to indicate the flow
  through these inherited initializers.
-->

## Inicializadores falíveis

Às vezes é útil definir uma classe, struct ou enum
cuja inicialização possa falhar.
Essa falha pode ser causada por valores inválidos nos parâmetros de inicialização,
pela ausência de um recurso externo obrigatório,
ou por alguma outra condição que impeça a inicialização de ter sucesso.

Para lidar com condições de inicialização que podem falhar,
defina um ou mais inicializadores falíveis como parte
da definição de uma classe, struct ou enum.
Você escreve um inicializador falível
colocando um ponto de interrogação depois da palavra-chave `init` (`init?`).

> Nota: Você não pode definir um inicializador falível e um não falível
> com os mesmos tipos e nomes de parâmetros.

<!--
  - test: `failableAndNonFailableInitializersCannotMatch`

  ```swifttest
  -> struct S {
        let s: String
        init(s: String) { self.s = s }
        init?(s: String) { self.s = s }
     }
  !$ error: invalid redeclaration of 'init(s:)'
  !!            init?(s: String) { self.s = s }
  !!            ^
  !$ note: 'init(s:)' previously declared here
  !!            init(s: String) { self.s = s }
  !!            ^
  ```
-->

Um inicializador falível cria um valor *optional* do tipo que ele inicializa.
Você escreve `return nil` dentro de um inicializador falível
para indicar um ponto em que a falha da inicialização pode ser disparada.

> Nota: Estritamente falando, inicializadores não retornam um valor.
> O papel deles é garantir que `self` esteja totalmente e corretamente inicializado
> até o fim da inicialização.
> Embora você escreva `return nil` para disparar uma falha de inicialização,
> não usa a palavra-chave `return` para indicar sucesso na inicialização.

Por exemplo, inicializadores falíveis são implementados para conversões entre tipos numéricos.
Para garantir que a conversão entre tipos numéricos mantenha o valor exatamente,
use o inicializador `init(exactly:)`.
Se a conversão de tipo não puder manter o valor,
o inicializador falha.

```swift
let wholeNumber: Double = 12345.0
let pi = 3.14159

if let valueMaintained = Int(exactly: wholeNumber) {
    print("\(wholeNumber) conversion to Int maintains value of \(valueMaintained)")
}
// Prints "12345.0 conversion to Int maintains value of 12345".

let valueChanged = Int(exactly: pi)
// valueChanged is of type Int?, not Int

if valueChanged == nil {
    print("\(pi) conversion to Int doesn't maintain value")
}
// Prints "3.14159 conversion to Int doesn't maintain value".
```

<!--
  - test: `failableInitializers`

  ```swifttest
  -> let wholeNumber: Double = 12345.0
  -> let pi = 3.14159

  -> if let valueMaintained = Int(exactly: wholeNumber) {
         print("\(wholeNumber) conversion to Int maintains value of \(valueMaintained)")
     }
  <- 12345.0 conversion to Int maintains value of 12345

  -> let valueChanged = Int(exactly: pi)
  // valueChanged is of type Int?, not Int

  -> if valueChanged == nil {
         print("\(pi) conversion to Int doesn't maintain value")
     }
  <- 3.14159 conversion to Int doesn't maintain value
  ```
-->

O exemplo a seguir define uma struct chamada `Animal`,
com uma propriedade `String` constante chamada `species`.
A struct `Animal` também define um inicializador falível
com um único parâmetro chamado `species`.
Esse inicializador verifica se o valor de `species` passado a ele é uma string vazia.
Se uma string vazia for encontrada, a falha da inicialização é disparada.
Caso contrário, o valor da propriedade `species` é definido, e a inicialização tem sucesso:

```swift
struct Animal {
    let species: String
    init?(species: String) {
        if species.isEmpty { return nil }
        self.species = species
    }
}
```

<!--
  - test: `failableInitializers`

  ```swifttest
  -> struct Animal {
        let species: String
        init?(species: String) {
           if species.isEmpty { return nil }
           self.species = species
        }
     }
  ```
-->

Você pode usar esse inicializador falível para tentar inicializar uma nova instância de `Animal`
e verificar se a inicialização teve sucesso:

```swift
let someCreature = Animal(species: "Giraffe")
// someCreature is of type Animal?, not Animal

if let giraffe = someCreature {
    print("An animal was initialized with a species of \(giraffe.species)")
}
// Prints "An animal was initialized with a species of Giraffe".
```

<!--
  - test: `failableInitializers`

  ```swifttest
  -> let someCreature = Animal(species: "Giraffe")
  // someCreature is of type Animal?, not Animal

  -> if let giraffe = someCreature {
        print("An animal was initialized with a species of \(giraffe.species)")
     }
  <- An animal was initialized with a species of Giraffe
  ```
-->

Se você passar uma string vazia para o parâmetro `species` do inicializador falível,
o inicializador dispara uma falha de inicialização:

```swift
let anonymousCreature = Animal(species: "")
// anonymousCreature is of type Animal?, not Animal

if anonymousCreature == nil {
    print("The anonymous creature couldn't be initialized")
}
// Prints "The anonymous creature couldn't be initialized".
```

<!--
  - test: `failableInitializers`

  ```swifttest
  -> let anonymousCreature = Animal(species: "")
  // anonymousCreature is of type Animal?, not Animal

  -> if anonymousCreature == nil {
        print("The anonymous creature couldn't be initialized")
     }
  <- The anonymous creature couldn't be initialized
  ```
-->

> Nota: Verificar um valor de string vazia (como `""` em vez de `"Giraffe"`)
> não é o mesmo que verificar `nil` para indicar a ausência de um valor `String` *optional*.
> No exemplo acima, uma string vazia (`""`) é um `String` válido e não optional.
> No entanto, não é apropriado que um animal
> tenha uma string vazia como valor da propriedade `species`.
> Para modelar essa restrição,
> o inicializador falível dispara uma falha de inicialização se uma string vazia for encontrada.

### Inicializadores falíveis para enums

Você pode usar um inicializador falível para selecionar um caso de enum adequado
com base em um ou mais parâmetros.
O inicializador pode então falhar se os parâmetros fornecidos
não corresponderem a nenhum caso de enum adequado.

O exemplo a seguir define um enum chamado `TemperatureUnit`,
com três estados possíveis (`kelvin`, `celsius` e `fahrenheit`).
Um inicializador falível é usado para encontrar um caso de enum adequado
para um valor `Character` que representa um símbolo de temperatura:

```swift
enum TemperatureUnit {
    case kelvin, celsius, fahrenheit
    init?(symbol: Character) {
        switch symbol {
        case "K":
            self = .kelvin
        case "C":
            self = .celsius
        case "F":
            self = .fahrenheit
        default:
            return nil
        }
    }
}
```

<!--
  - test: `failableInitializers`

  ```swifttest
  -> enum TemperatureUnit {
        case kelvin, celsius, fahrenheit
        init?(symbol: Character) {
           switch symbol {
              case "K":
                 self = .kelvin
              case "C":
                 self = .celsius
              case "F":
                 self = .fahrenheit
              default:
                 return nil
           }
        }
     }
  ```
-->

Você pode usar esse inicializador falível para escolher
um caso de enum adequado entre os três estados possíveis
e fazer a inicialização falhar se o parâmetro não corresponder a nenhum desses
estados:

```swift
let fahrenheitUnit = TemperatureUnit(symbol: "F")
if fahrenheitUnit != nil {
    print("This is a defined temperature unit, so initialization succeeded.")
}
// Prints "This is a defined temperature unit, so initialization succeeded."

let unknownUnit = TemperatureUnit(symbol: "X")
if unknownUnit == nil {
    print("This isn't a defined temperature unit, so initialization failed.")
}
// Prints "This isn't a defined temperature unit, so initialization failed."
```

<!--
  - test: `failableInitializers`

  ```swifttest
  -> let fahrenheitUnit = TemperatureUnit(symbol: "F")
  -> if fahrenheitUnit != nil {
        print("This is a defined temperature unit, so initialization succeeded.")
     }
  <- This is a defined temperature unit, so initialization succeeded.

  -> let unknownUnit = TemperatureUnit(symbol: "X")
  -> if unknownUnit == nil {
        print("This isn't a defined temperature unit, so initialization failed.")
     }
  <- This isn't a defined temperature unit, so initialization failed.
  ```
-->

### Inicializadores falíveis para enums com raw value

Enumerações com raw value recebem automaticamente um inicializador falível,
`init?(rawValue:)`,
que recebe um parâmetro chamado `rawValue` do tipo de raw value apropriado
e seleciona um caso de enum correspondente, se encontrar um,
ou dispara uma falha de inicialização se nenhum valor correspondente existir.

Você pode reescrever o exemplo `TemperatureUnit` acima
para usar raw values do tipo `Character`
e aproveitar o inicializador `init?(rawValue:)`:

```swift
enum TemperatureUnit: Character {
    case kelvin = "K", celsius = "C", fahrenheit = "F"
}

let fahrenheitUnit = TemperatureUnit(rawValue: "F")
if fahrenheitUnit != nil {
    print("This is a defined temperature unit, so initialization succeeded.")
}
// Prints "This is a defined temperature unit, so initialization succeeded."

let unknownUnit = TemperatureUnit(rawValue: "X")
if unknownUnit == nil {
    print("This isn't a defined temperature unit, so initialization failed.")
}
// Prints "This isn't a defined temperature unit, so initialization failed."
```

<!--
  - test: `failableInitializersForEnumerations`

  ```swifttest
  -> enum TemperatureUnit: Character {
        case kelvin = "K", celsius = "C", fahrenheit = "F"
     }

  -> let fahrenheitUnit = TemperatureUnit(rawValue: "F")
  -> if fahrenheitUnit != nil {
        print("This is a defined temperature unit, so initialization succeeded.")
     }
  <- This is a defined temperature unit, so initialization succeeded.

  -> let unknownUnit = TemperatureUnit(rawValue: "X")
  -> if unknownUnit == nil {
        print("This isn't a defined temperature unit, so initialization failed.")
     }
  <- This isn't a defined temperature unit, so initialization failed.
  ```
-->

### Propagação da falha de inicialização

Um inicializador falível de uma classe, struct ou enum
pode delegar para o lado, para outro inicializador falível da mesma classe, struct ou enum.
Da mesma forma, um inicializador falível de subclasse pode delegar para cima, para um inicializador falível da superclasse.

Em qualquer um dos casos, se você delegar para outro inicializador que faça a inicialização falhar,
o processo de inicialização inteiro falha imediatamente,
e nenhum código de inicialização adicional é executado.

<!--
  - test: `delegatingAcrossInAStructurePropagatesInitializationFailureImmediately`

  ```swifttest
  -> struct S {
        init?(string1: String) {
           self.init(string2: string1)
           print("Hello!") // this should never be printed, because initialization has already failed
        }
        init?(string2: String) { return nil }
     }
  -> let s = S(string1: "bing")
  -> assert(s == nil)
  ```
-->

<!--
  - test: `delegatingAcrossInAClassPropagatesInitializationFailureImmediately`

  ```swifttest
  -> class C {
        convenience init?(string1: String) {
           self.init(string2: string1)
           print("Hello!") // this should never be printed, because initialization has already failed
        }
        init?(string2: String) { return nil }
     }
  -> let c = C(string1: "bing")
  -> assert(c == nil)
  ```
-->

<!--
  - test: `delegatingUpInAClassPropagatesInitializationFailureImmediately`

  ```swifttest
  -> class C {
        init?(string1: String) { return nil }
     }
  -> class D: C {
        init?(string2: String) {
           super.init(string1: string2)
           print("Hello!") // this should never be printed, because initialization has already failed
        }
     }
  -> let d = D(string2: "bing")
  -> assert(d == nil)
  ```
-->

> Nota: Um inicializador falível também pode delegar para um inicializador não falível.
> Use essa abordagem se precisar adicionar um possível estado de falha
> a um processo de inicialização existente que, fora isso, não falha.

O exemplo a seguir define uma subclasse de `Product` chamada `CartItem`.
A classe `CartItem` modela um item em um carrinho de compras online.
`CartItem` introduz uma propriedade armazenada constante chamada `quantity`
e garante que essa propriedade sempre tenha um valor de pelo menos `1`:

```swift
class Product {
    let name: String
    init?(name: String) {
        if name.isEmpty { return nil }
        self.name = name
    }
}

class CartItem: Product {
    let quantity: Int
    init?(name: String, quantity: Int) {
        if quantity < 1 { return nil }
        self.quantity = quantity
        super.init(name: name)
    }
}
```

<!--
  - test: `failableInitializers`

  ```swifttest
  -> class Product {
        let name: String
        init?(name: String) {
           if name.isEmpty { return nil }
           self.name = name
        }
     }
  >> let p = Product(name: "")

  -> class CartItem: Product {
        let quantity: Int
        init?(name: String, quantity: Int) {
           if quantity < 1 { return nil }
           self.quantity = quantity
           super.init(name: name)
        }
     }
  ```
-->

O inicializador falível de `CartItem` começa
validando se recebeu um valor `quantity` igual a `1` ou mais.
Se o `quantity` for inválido,
o processo de inicialização inteiro falha imediatamente
e nenhum código de inicialização adicional é executado.
Da mesma forma, o inicializador falível de `Product`
verifica o valor `name`,
e o processo de inicialização falha imediatamente
se `name` for uma string vazia.

Se você criar uma instância de `CartItem` com um nome não vazio e uma quantidade igual a `1` ou mais,
a inicialização tem sucesso:

```swift
if let twoSocks = CartItem(name: "sock", quantity: 2) {
    print("Item: \(twoSocks.name), quantity: \(twoSocks.quantity)")
}
// Prints "Item: sock, quantity: 2".
```

<!--
  - test: `failableInitializers`

  ```swifttest
  -> if let twoSocks = CartItem(name: "sock", quantity: 2) {
        print("Item: \(twoSocks.name), quantity: \(twoSocks.quantity)")
     }
  <- Item: sock, quantity: 2
  ```
-->

Se você tentar criar uma instância de `CartItem` com um valor `quantity` igual a `0`,
o inicializador de `CartItem` faz a inicialização falhar:

```swift
if let zeroShirts = CartItem(name: "shirt", quantity: 0) {
    print("Item: \(zeroShirts.name), quantity: \(zeroShirts.quantity)")
} else {
    print("Unable to initialize zero shirts")
}
// Prints "Unable to initialize zero shirts".
```

<!--
  - test: `failableInitializers`

  ```swifttest
  -> if let zeroShirts = CartItem(name: "shirt", quantity: 0) {
        print("Item: \(zeroShirts.name), quantity: \(zeroShirts.quantity)")
     } else {
        print("Unable to initialize zero shirts")
     }
  <- Unable to initialize zero shirts
  ```
-->

Da mesma forma, se você tentar criar uma instância de `CartItem` com um valor `name` vazio,
o inicializador da superclasse `Product` faz a inicialização falhar:

```swift
if let oneUnnamed = CartItem(name: "", quantity: 1) {
    print("Item: \(oneUnnamed.name), quantity: \(oneUnnamed.quantity)")
} else {
    print("Unable to initialize one unnamed product")
}
// Prints "Unable to initialize one unnamed product".
```

<!--
  - test: `failableInitializers`

  ```swifttest
  -> if let oneUnnamed = CartItem(name: "", quantity: 1) {
        print("Item: \(oneUnnamed.name), quantity: \(oneUnnamed.quantity)")
     } else {
        print("Unable to initialize one unnamed product")
     }
  <- Unable to initialize one unnamed product
  ```
-->

### Sobrescrevendo um inicializador falível

Você pode sobrescrever um inicializador falível da superclasse em uma subclasse,
assim como qualquer outro inicializador.
Como alternativa, você pode sobrescrever um inicializador falível da superclasse
com um inicializador *não falível* da subclasse.
Isso permite definir uma subclasse para a qual a inicialização não pode falhar,
mesmo que a inicialização da superclasse possa falhar.

Observe que, se você sobrescrever um inicializador falível da superclasse com um inicializador não falível da subclasse,
a única forma de delegar para o inicializador da superclasse
é fazer force unwrapping do resultado do inicializador falível da superclasse.

> Nota: Você pode sobrescrever um inicializador falível com um inicializador não falível,
> mas não o contrário.

<!--
  - test: `youCannotOverrideANonFailableInitializerWithAFailableInitializer`

  ```swifttest
  -> class C {
        init() {}
     }
  -> class D: C {
        override init?() {}
     }
  !$ error: failable initializer 'init()' cannot override a non-failable initializer
  !!            override init?() {}
  !!                     ^
  !$ note: non-failable initializer 'init()' overridden here
  !!            init() {}
  !!            ^
  ```
-->

O exemplo a seguir define uma classe chamada `Document`.
Essa classe modela um documento que pode ser inicializado com
uma propriedade `name` que é um valor de string não vazio ou `nil`,
mas que não pode ser uma string vazia:

```swift
class Document {
    var name: String?
    // this initializer creates a document with a nil name value
    init() {}
    // this initializer creates a document with a nonempty name value
    init?(name: String) {
        if name.isEmpty { return nil }
        self.name = name
    }
}
```

<!--
  - test: `failableInitializers`

  ```swifttest
  -> class Document {
        var name: String?
        // this initializer creates a document with a nil name value
        init() {}
        // this initializer creates a document with a nonempty name value
        init?(name: String) {
           if name.isEmpty { return nil }
           self.name = name
        }
     }
  ```
-->

O próximo exemplo define uma subclasse de `Document` chamada `AutomaticallyNamedDocument`.
A subclasse `AutomaticallyNamedDocument` sobrescreve
ambos os inicializadores designados introduzidos por `Document`.
Essas sobrescritas garantem que uma instância de `AutomaticallyNamedDocument` tenha
um valor inicial `name` igual a `"[Untitled]"`
se a instância for inicializada sem um nome,
ou se uma string vazia for passada ao inicializador `init(name:)`:

```swift
class AutomaticallyNamedDocument: Document {
    override init() {
        super.init()
        self.name = "[Untitled]"
    }
    override init(name: String) {
        super.init()
        if name.isEmpty {
            self.name = "[Untitled]"
        } else {
            self.name = name
        }
    }
}
```

<!--
  - test: `failableInitializers`

  ```swifttest
  -> class AutomaticallyNamedDocument: Document {
        override init() {
           super.init()
           self.name = "[Untitled]"
        }
        override init(name: String) {
           super.init()
           if name.isEmpty {
              self.name = "[Untitled]"
           } else {
              self.name = name
           }
        }
     }
  ```
-->

A classe `AutomaticallyNamedDocument` sobrescreve o inicializador falível `init?(name:)`
da superclasse com um inicializador não falível `init(name:)`.
Como `AutomaticallyNamedDocument` lida com o caso da string vazia
de uma forma diferente da superclasse,
seu inicializador não precisa falhar,
e por isso fornece uma versão não falível do inicializador.

Você pode usar force unwrapping em um inicializador
para chamar um inicializador falível da superclasse
como parte da implementação de um inicializador não falível de uma subclasse.
Por exemplo, a subclasse `UntitledDocument` abaixo sempre se chama `"[Untitled]"`,
e usa o inicializador falível `init(name:)`
da superclasse durante a inicialização.

```swift
class UntitledDocument: Document {
    override init() {
        super.init(name: "[Untitled]")!
    }
}
```

<!--
  - test: `failableInitializers`

  ```swifttest
  -> class UntitledDocument: Document {
        override init() {
           super.init(name: "[Untitled]")!
        }
     }
  ```
-->

Nesse caso, se o inicializador `init(name:)` da superclasse
fosse chamado com uma string vazia como nome,
a operação de force unwrapping resultaria em um erro de tempo de execução.
No entanto, como ele é chamado com um literal de string,
você pode ver que o inicializador não vai falhar,
portanto nenhum erro de tempo de execução pode ocorrer neste caso.

### O inicializador falível init!

Normalmente você define um inicializador falível
que cria uma instância optional do tipo apropriado
colocando um ponto de interrogação depois da palavra-chave `init` (`init?`).
Como alternativa, você pode definir um inicializador falível que cria
uma instância de optional implicitamente unwrapped do tipo apropriado.
Para isso, coloque um ponto de exclamação depois da palavra-chave `init` (`init!`)
em vez de um ponto de interrogação.

Você pode delegar de `init?` para `init!` e vice-versa,
e pode sobrescrever `init?` com `init!` e vice-versa.
Você também pode delegar de `init` para `init!`,
embora isso dispare uma asserção
se o inicializador `init!` fizer a inicialização falhar.

<!--
  - test: `structuresCanDelegateAcrossFromOptionalToIUO`

  ```swifttest
  -> struct S {
        init?(optional: Int) { self.init(iuo: optional) }
        init!(iuo: Int) {}
     }
  ```
-->

<!--
  - test: `structuresCanDelegateAcrossFromIUOToOptional`

  ```swifttest
  -> struct S {
        init!(iuo: Int) { self.init(optional: iuo) }
        init?(optional: Int) {}
     }
  ```
-->

<!--
  - test: `classesCanDelegateAcrossFromOptionalToIUO`

  ```swifttest
  -> class C {
        convenience init?(optional: Int) { self.init(iuo: optional) }
        init!(iuo: Int) {}
     }
  ```
-->

<!--
  - test: `classesCanDelegateAcrossFromIUOToOptional`

  ```swifttest
  -> class C {
        convenience init!(iuo: Int) { self.init(optional: iuo) }
        init?(optional: Int) {}
     }
  ```
-->

<!--
  - test: `classesCanDelegateUpFromOptionalToIUO`

  ```swifttest
  -> class C {
        init!(iuo: Int) {}
     }
  -> class D: C {
        init?(optional: Int) { super.init(iuo: optional) }
     }
  ```
-->

<!--
  - test: `classesCanDelegateUpFromIUOToOptional`

  ```swifttest
  -> class C {
        init?(optional: Int) {}
     }
  -> class D: C {
        init!(iuo: Int) { super.init(optional: iuo) }
     }
  ```
-->

<!--
  - test: `classesCanOverrideOptionalWithIUO`

  ```swifttest
  -> class C {
        init?(i: Int) {}
     }
  -> class D: C {
        override init!(i: Int) { super.init(i: i) }
     }
  ```
-->

<!--
  - test: `classesCanOverrideIUOWithOptional`

  ```swifttest
  -> class C {
        init!(i: Int) {}
     }
  -> class D: C {
        override init?(i: Int) { super.init(i: i) }
     }
  ```
-->

<!--
  - test: `structuresCanDelegateAcrossFromNonFailingToIUO`

  ```swifttest
  -> struct S {
        init(nonFailing: Int) { self.init(iuo: nonFailing) }
        init!(iuo: Int) {}
     }
  ```
-->

<!--
  - test: `classesCanDelegateAcrossFromNonFailingToIUO`

  ```swifttest
  -> class C {
        convenience init(nonFailing: Int) { self.init(iuo: nonFailing) }
        init!(iuo: Int) {}
     }
  ```
-->

<!--
  - test: `classesCanDelegateUpFromNonFailingToIUO`

  ```swifttest
  -> class C {
        init!(iuo: Int) {}
     }
  -> class D: C {
        init(nonFailing: Int) { super.init(iuo: nonFailing) }
     }
  ```
-->

<!--
  - test: `structuresAssertWhenDelegatingAcrossFromNonFailingToNilIUO`

  ```swifttest
  -> struct S {
        init(nonFailing: Int) { self.init(iuo: nonFailing) }
        init!(iuo: Int) { return nil }
     }
  -> let s = S(nonFailing: 42)
  xx assertion
  ```
-->

<!--
  - test: `classesAssertWhenDelegatingAcrossFromNonFailingToNilIUO`

  ```swifttest
  -> class C {
        convenience init(nonFailing: Int) { self.init(iuo: nonFailing) }
        init!(iuo: Int) { return nil }
     }
  -> let c = C(nonFailing: 42)
  xx assertion
  ```
-->

<!--
  - test: `classesAssertWhenDelegatingUpFromNonFailingToNilIUO`

  ```swifttest
  -> class C {
        init!(iuo: Int) { return nil }
     }
  -> class D: C {
        init(nonFailing: Int) { super.init(iuo: nonFailing) }
     }
  -> let d = D(nonFailing: 42)
  xx assertion
  ```
-->

## Inicializadores required

Escreva o modificador `required` antes da definição de um inicializador de classe
para indicar que toda subclasse da classe deve implementar esse inicializador:

```swift
class SomeClass {
    required init() {
        // initializer implementation goes here
    }
}
```

<!--
  - test: `requiredInitializers`

  ```swifttest
  -> class SomeClass {
        required init() {
           // initializer implementation goes here
        }
     }
  ```
-->

<!--
  - test: `requiredDesignatedInitializersMustBeImplementedBySubclasses`

  ```swifttest
  -> class C {
        required init(i: Int) {}
     }
  -> class D: C {
        init() {}
     }
  !$ error: 'required' initializer 'init(i:)' must be provided by subclass of 'C'
  !! }
  !! ^
  !$ note: 'required' initializer is declared in superclass here
  !!    required init(i: Int) {}
  !!             ^
  ```
-->

<!--
  - test: `requiredConvenienceInitializersMustBeImplementedBySubclasses`

  ```swifttest
  -> class C {
        init() {}
        required convenience init(i: Int) {
           self.init()
        }
     }
  -> class D: C {
        init(s: String) {}
     }
  !$ error: 'required' initializer 'init(i:)' must be provided by subclass of 'C'
  !! }
  !! ^
  !$ note: 'required' initializer is declared in superclass here
  !!    required convenience init(i: Int) {
  !!                         ^
  ```
-->

Você também deve escrever o modificador `required` antes
de cada implementação em subclasse de um inicializador required,
para indicar que o requisito do inicializador se aplica às subclasses seguintes na cadeia.
Você não escreve o modificador `override` ao sobrescrever um inicializador designado required:

```swift
class SomeSubclass: SomeClass {
    required init() {
        // subclass implementation of the required initializer goes here
    }
}
```

<!--
  - test: `requiredInitializers`

  ```swifttest
  -> class SomeSubclass: SomeClass {
        required init() {
           // subclass implementation of the required initializer goes here
        }
     }
  ```
-->

<!--
  - test: `youCannotWriteOverrideWhenOverridingARequiredDesignatedInitializer`

  ```swifttest
  -> class C {
        required init() {}
     }
  -> class D: C {
        override required init() {}
     }
  !$ warning: 'override' is implied when overriding a required initializer
  !!    override required init() {}
  !! ~~~~~~~~~         ^
  !!-
  !$ note: overridden required initializer is here
  !!    required init() {}
  !!             ^
  ```
-->

> Nota: Você não precisa fornecer uma implementação explícita de um inicializador required
> se puder atender ao requisito com um inicializador herdado.

<!--
  - test: `youCanSatisfyARequiredDesignatedInitializerWithAnInheritedInitializer`

  ```swifttest
  -> class C {
        var x = 0
        required init(i: Int) {}
     }
  -> class D: C {
        var y = 0
     }
  ```
-->

<!--
  - test: `youCanSatisfyARequiredConvenienceInitializerWithAnInheritedInitializer`

  ```swifttest
  -> class C {
        var x = 0
        init(i: Int) {}
        required convenience init() {
           self.init(i: 42)
        }
     }
  -> class D: C {
        var y = 0
     }
  ```
-->

<!--
  FIXME: This section still doesn't describe why required initializers are useful.
  This is because the reason for their usefulness -
  construction through a metatype of some protocol type with an initializer requirement -
  used to be broken due to
  <rdar://problem/13695680> Constructor requirements in protocols (needed for NSCoding).
  As of early 2015 that bug has been fixed.
  See the corresponding FIXME in the Protocols chapter introduction too.
-->

## Definindo o valor padrão de uma propriedade com uma closure ou função

Se o valor padrão de uma propriedade armazenada exigir alguma personalização ou configuração,
você pode usar uma closure ou uma função global para fornecer
um valor padrão personalizado para essa propriedade.
Sempre que uma nova instância do tipo ao qual a propriedade pertence é inicializada,
a closure ou função é chamada,
e o valor de retorno dela é atribuído como valor padrão da propriedade.

Esses tipos de closures ou funções normalmente criam
um valor temporário do mesmo tipo da propriedade,
ajustam esse valor para representar o estado inicial desejado
e então retornam esse valor temporário para ser usado como valor padrão da propriedade.

Veja um esboço básico de como uma closure pode ser usada
para fornecer um valor padrão de propriedade:

```swift
class SomeClass {
    let someProperty: SomeType = {
        // create a default value for someProperty inside this closure
        // someValue must be of the same type as SomeType
        return someValue
    }()
}
```

<!--
  - test: `defaultPropertyWithClosure`

  ```swifttest
  >> class SomeType {}
  -> class SomeClass {
        let someProperty: SomeType = {
           // create a default value for someProperty inside this closure
           // someValue must be of the same type as SomeType
  >>       let someValue = SomeType()
           return someValue
        }()
     }
  ```
-->

Observe que a chave de fechamento da closure é seguida por um par de parênteses vazio.
Isso diz ao Swift para executar a closure imediatamente.
Se você omitir esses parênteses,
você estará tentando atribuir a própria closure à propriedade,
e não o valor de retorno da closure.

<!--
  TODO: feedback from Peter is that this is very close to the syntax for
  a computed property that doesn't define a separate getter.
  He's right, and it would be good to provide an additional example -
  perhaps with a stored property that's assigned the result of a function -
  to make the difference more explicit.
-->

> Nota: Se você usar uma closure para inicializar uma propriedade,
> lembre-se de que o restante da instância ainda não foi inicializado
> no momento em que a closure é executada.
> Isso significa que você não pode acessar nenhum outro valor de propriedade dentro da closure,
> mesmo que essas propriedades tenham valores padrão.
> Você também não pode usar a propriedade `self` implícita,
> nem chamar nenhum dos métodos da instância.

O exemplo a seguir define uma struct chamada `Chessboard`,
que modela um tabuleiro para o jogo de xadrez.
O xadrez é jogado em um tabuleiro de 8 x 8,
com casas pretas e brancas alternadas.

![](chessBoard)

Para representar esse tabuleiro, a struct `Chessboard` tem uma única propriedade chamada `boardColors`,
que é um array de 64 valores `Bool`.
Um valor `true` no array representa uma casa preta
e um valor `false` representa uma casa branca.
O primeiro item do array representa a casa do canto superior esquerdo do tabuleiro
e o último item do array representa a casa do canto inferior direito do tabuleiro.

O array `boardColors` é inicializado com uma closure que define seus valores de cor:

```swift
struct Chessboard {
    let boardColors: [Bool] = {
        var temporaryBoard: [Bool] = []
        var isBlack = false
        for i in 1...8 {
            for j in 1...8 {
                temporaryBoard.append(isBlack)
                isBlack = !isBlack
            }
            isBlack = !isBlack
        }
        return temporaryBoard
    }()
    func squareIsBlackAt(row: Int, column: Int) -> Bool {
        return boardColors[(row * 8) + column]
    }
}
```

<!--
  - test: `chessboard`

  ```swifttest
  -> struct Chessboard {
        let boardColors: [Bool] = {
           var temporaryBoard: [Bool] = []
           var isBlack = false
           for i in 1...8 {
              for j in 1...8 {
                 temporaryBoard.append(isBlack)
                 isBlack = !isBlack
              }
              isBlack = !isBlack
           }
           return temporaryBoard
        }()
        func squareIsBlackAt(row: Int, column: Int) -> Bool {
           return boardColors[(row * 8) + column]
        }
     }
  ```
-->

Sempre que uma nova instância de `Chessboard` é criada, a closure é executada,
e o valor padrão de `boardColors` é calculado e retornado.
A closure do exemplo acima calcula e define
a cor apropriada para cada casa do tabuleiro
em um array temporário chamado `temporaryBoard`,
e retorna esse array temporário como valor de retorno da closure
quando a configuração estiver concluída.
O valor de array retornado é armazenado em `boardColors`
e pode ser consultado com a função utilitária `squareIsBlackAt(row:column:)`:

```swift
let board = Chessboard()
print(board.squareIsBlackAt(row: 0, column: 1))
// Prints "true".
print(board.squareIsBlackAt(row: 7, column: 7))
// Prints "false".
```

<!--
  - test: `chessboard`

  ```swifttest
  -> let board = Chessboard()
  >> assert(board.boardColors == [false, true, false, true, false, true, false, true, true, false, true, false, true, false, true, false, false, true, false, true, false, true, false, true, true, false, true, false, true, false, true, false, false, true, false, true, false, true, false, true, true, false, true, false, true, false, true, false, false, true, false, true, false, true, false, true, true, false, true, false, true, false, true, false])
  -> print(board.squareIsBlackAt(row: 0, column: 1))
  <- true
  -> print(board.squareIsBlackAt(row: 7, column: 7))
  <- false
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
