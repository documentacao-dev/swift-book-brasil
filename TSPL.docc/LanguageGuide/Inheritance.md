# Herança

Criar uma subclasse para adicionar ou sobrescrever funcionalidades.

Uma classe pode *herdar* métodos, propriedades e outras características
de outra classe.
Quando uma classe herda de outra,
a classe que herda é chamada de *subclasse*,
e a classe da qual ela herda é chamada de sua *superclasse*.
A herança é um comportamento fundamental que diferencia classes
de outros tipos em Swift.

Classes em Swift podem chamar e acessar
métodos, propriedades e subscripts pertencentes à sua superclasse
e podem fornecer suas próprias versões sobrescritas desses métodos, propriedades e subscripts
para refinar ou modificar seu comportamento.
O Swift ajuda a garantir que suas sobrescritas estejam corretas
verificando se a definição sobrescrita tem uma definição correspondente na superclasse.

Classes também podem adicionar observadores de propriedade a propriedades herdadas
para serem notificadas quando o valor de uma propriedade muda.
Observadores de propriedade podem ser adicionados a qualquer propriedade,
independentemente de ela ter sido originalmente definida como armazenada ou computada.

## Definindo uma classe base

Qualquer classe que não herde de outra classe é chamada de *classe base*.

> Nota: Classes em Swift não herdam de uma classe base universal.
> Classes que você define sem especificar uma superclasse
> se tornam automaticamente classes base sobre as quais você pode construir.

O exemplo abaixo define uma classe base chamada `Vehicle`.
Essa classe base define uma propriedade armazenada chamada `currentSpeed`,
com valor padrão `0.0` (inferindo um tipo de propriedade `Double`).
O valor da propriedade `currentSpeed` é usado por
uma propriedade `String` computada somente leitura chamada `description`
para criar uma descrição do veículo.

A classe base `Vehicle` também define um método chamado `makeNoise`.
Esse método não faz nada de fato para uma instância base de `Vehicle`,
mas será personalizado pelas subclasses de `Vehicle` mais adiante:

```swift
class Vehicle {
    var currentSpeed = 0.0
    var description: String {
        return "traveling at \(currentSpeed) miles per hour"
    }
    func makeNoise() {
        // do nothing - an arbitrary vehicle doesn't necessarily make a noise
    }
}
```

<!--
  - test: `inheritance`

  ```swifttest
  -> class Vehicle {
        var currentSpeed = 0.0
        var description: String {
           return "traveling at \(currentSpeed) miles per hour"
        }
        func makeNoise() {
           // do nothing - an arbitrary vehicle doesn't necessarily make a noise
        }
     }
  ```
-->

Você cria uma nova instância de `Vehicle` com a *sintaxe de inicializador*,
que é escrita como um nome de tipo seguido de parênteses vazios:

```swift
let someVehicle = Vehicle()
```

<!--
  - test: `inheritance`

  ```swifttest
  -> let someVehicle = Vehicle()
  ```
-->

Depois de criar uma nova instância de `Vehicle`,
você pode acessar a propriedade `description` para imprimir
uma descrição legível por humanos da velocidade atual do veículo:

```swift
print("Vehicle: \(someVehicle.description)")
// Vehicle: traveling at 0.0 miles per hour
```

<!--
  - test: `inheritance`

  ```swifttest
  -> print("Vehicle: \(someVehicle.description)")
  </ Vehicle: traveling at 0.0 miles per hour
  ```
-->

A classe `Vehicle` define características comuns a um veículo qualquer,
mas não é muito útil por si só.
Para torná-la mais útil,
você precisa refiná-la para descrever tipos mais específicos de veículos.

## Criando subclasses

*Criar subclasses* é o ato de basear uma nova classe em uma classe existente.
A subclasse herda características da classe existente, que você pode então refinar.
Você também pode adicionar novas características à subclasse.

Para indicar que uma subclasse tem uma superclasse,
escreva o nome da subclasse antes do nome da superclasse,
separados por dois-pontos:

```swift
class SomeSubclass: SomeSuperclass {
    // subclass definition goes here
}
```

<!--
  - test: `protocolSyntax`

  ```swifttest
  >> class SomeSuperclass {}
  -> class SomeSubclass: SomeSuperclass {
        // subclass definition goes here
     }
  ```
-->

O exemplo a seguir define uma subclasse chamada `Bicycle`,
com superclasse `Vehicle`:

```swift
class Bicycle: Vehicle {
    var hasBasket = false
}
```

<!--
  - test: `inheritance`

  ```swifttest
  -> class Bicycle: Vehicle {
        var hasBasket = false
     }
  ```
-->

A nova classe `Bicycle` ganha automaticamente todas as características de `Vehicle`,
como suas propriedades `currentSpeed` e `description` e seu método `makeNoise()`.

Além das características que herda,
a classe `Bicycle` define uma nova propriedade armazenada,
`hasBasket`, com valor padrão `false`
(inferindo um tipo `Bool` para a propriedade).

Por padrão, qualquer nova instância de `Bicycle` que você criar não terá cesta.
Você pode definir a propriedade `hasBasket` como `true` para uma instância específica de `Bicycle`
depois que essa instância for criada:

```swift
let bicycle = Bicycle()
bicycle.hasBasket = true
```

<!--
  - test: `inheritance`

  ```swifttest
  -> let bicycle = Bicycle()
  -> bicycle.hasBasket = true
  ```
-->

Você também pode modificar a propriedade herdada `currentSpeed` de uma instância de `Bicycle`,
e consultar a propriedade herdada `description` da instância:

```swift
bicycle.currentSpeed = 15.0
print("Bicycle: \(bicycle.description)")
// Bicycle: traveling at 15.0 miles per hour
```

<!--
  - test: `inheritance`

  ```swifttest
  -> bicycle.currentSpeed = 15.0
  -> print("Bicycle: \(bicycle.description)")
  </ Bicycle: traveling at 15.0 miles per hour
  ```
-->

Subclasses também podem ter subclasses.
O próximo exemplo cria uma subclasse de `Bicycle` para uma bicicleta de dois lugares
conhecida como “tandem”:

```swift
class Tandem: Bicycle {
    var currentNumberOfPassengers = 0
}
```

<!--
  - test: `inheritance`

  ```swifttest
  -> class Tandem: Bicycle {
        var currentNumberOfPassengers = 0
     }
  ```
-->

`Tandem` herda todas as propriedades e métodos de `Bicycle`,
que por sua vez herda todas as propriedades e métodos de `Vehicle`.
A subclasse `Tandem` também adiciona uma nova propriedade armazenada chamada `currentNumberOfPassengers`,
com valor padrão `0`.

Se você criar uma instância de `Tandem`,
pode trabalhar com qualquer uma de suas propriedades novas e herdadas,
e consultar a propriedade somente leitura `description` que ela herda de `Vehicle`:

```swift
let tandem = Tandem()
tandem.hasBasket = true
tandem.currentNumberOfPassengers = 2
tandem.currentSpeed = 22.0
print("Tandem: \(tandem.description)")
// Tandem: traveling at 22.0 miles per hour
```

<!--
  - test: `inheritance`

  ```swifttest
  -> let tandem = Tandem()
  -> tandem.hasBasket = true
  -> tandem.currentNumberOfPassengers = 2
  -> tandem.currentSpeed = 22.0
  -> print("Tandem: \(tandem.description)")
  </ Tandem: traveling at 22.0 miles per hour
  ```
-->

## Sobrescrita

Uma subclasse pode fornecer sua própria implementação personalizada de
um método de instância, método de tipo, propriedade de instância, propriedade de tipo ou subscript
que, de outro modo, herdaria de uma superclasse.
Isso é chamado de *sobrescrita*.

Para sobrescrever uma característica que seria herdada,
você coloca a palavra-chave `override` antes da sua definição sobrescrita.
Isso deixa claro que a intenção é fornecer uma sobrescrita
e que você não forneceu uma definição correspondente por engano.
Sobrescrever por acidente pode causar comportamento inesperado,
e qualquer sobrescrita sem a palavra-chave `override` é
identificada como erro quando seu código é compilado.

A palavra-chave `override` também leva o compilador do Swift
a verificar se a superclasse da sua classe que sobrescreve (ou uma de suas superclasses ancestrais)
tem uma declaração que corresponde à que você forneceu para a sobrescrita.
Essa verificação garante que sua definição sobrescrita está correta.

### Acessando métodos, propriedades e subscripts da superclasse

Quando você fornece uma sobrescrita de método, propriedade ou subscript para uma subclasse,
às vezes é útil usar a implementação existente da superclasse
como parte da sua sobrescrita.
Por exemplo, você pode refinar o comportamento dessa implementação existente,
ou armazenar um valor modificado em uma variável herdada existente.

Quando isso for apropriado,
você acessa a versão da superclasse de um método, propriedade ou subscript
usando o prefixo `super`:

- Um método sobrescrito chamado `someMethod()` pode chamar a versão da superclasse de `someMethod()`
  chamando `super.someMethod()` dentro da implementação do método que sobrescreve.
- Uma propriedade sobrescrita chamada `someProperty` pode acessar a versão da superclasse de `someProperty`
  como `super.someProperty` dentro do getter ou setter que sobrescreve.
- Um subscript sobrescrito para `someIndex` pode acessar a versão da superclasse do mesmo subscript
  como `super[someIndex]` dentro da implementação do subscript que sobrescreve.

### Sobrescrevendo métodos

Você pode sobrescrever um método de instância ou de tipo herdado
para fornecer uma implementação sob medida ou alternativa do método dentro da sua subclasse.

O exemplo a seguir define uma nova subclasse de `Vehicle` chamada `Train`,
que sobrescreve o método `makeNoise()` que `Train` herda de `Vehicle`:

```swift
class Train: Vehicle {
    override func makeNoise() {
        print("Choo Choo")
    }
}
```

<!--
  - test: `inheritance`

  ```swifttest
  -> class Train: Vehicle {
        override func makeNoise() {
           print("Choo Choo")
        }
     }
  ```
-->

Se você criar uma nova instância de `Train` e chamar seu método `makeNoise()`,
vê que a versão do método da subclasse `Train` é chamada:

```swift
let train = Train()
train.makeNoise()
// Prints "Choo Choo".
```

<!--
  - test: `inheritance`

  ```swifttest
  -> let train = Train()
  -> train.makeNoise()
  <- Choo Choo
  ```
-->

### Sobrescrevendo propriedades

Você pode sobrescrever uma propriedade de instância ou de tipo herdada
para fornecer seu próprio getter e setter personalizados para essa propriedade,
ou para adicionar observadores de propriedade e permitir que a propriedade sobrescrita
observe quando o valor da propriedade subjacente muda.

#### Sobrescrevendo getters e setters de propriedades

Você pode fornecer um getter personalizado (e um setter, se apropriado) para sobrescrever *qualquer* propriedade herdada,
independentemente de a propriedade herdada ser implementada como
armazenada ou computada na origem.
A natureza armazenada ou computada de uma propriedade herdada não é conhecida pela subclasse:
ela sabe apenas que a propriedade herdada tem certo nome e tipo.
Você deve sempre informar o nome e o tipo da propriedade que está sobrescrevendo,
para que o compilador possa verificar se sua sobrescrita corresponde
a uma propriedade da superclasse com o mesmo nome e tipo.

Você pode apresentar uma propriedade herdada somente leitura como uma propriedade de leitura e escrita
fornecendo um getter e um setter na sobrescrita da propriedade da sua subclasse.
No entanto, você não pode apresentar uma propriedade herdada de leitura e escrita como somente leitura.

> Nota: Se você fornecer um setter como parte de uma sobrescrita de propriedade,
> também precisa fornecer um getter para essa sobrescrita.
> Se não quiser modificar o valor da propriedade herdada dentro do getter que sobrescreve,
> pode simplesmente repassar o valor herdado
> retornando `super.someProperty` a partir do getter,
> em que `someProperty` é o nome da propriedade que você está sobrescrevendo.

O exemplo a seguir define uma nova classe chamada `Car`,
que é uma subclasse de `Vehicle`.
A classe `Car` introduz uma nova propriedade armazenada chamada `gear`,
com valor inteiro padrão `1`.
A classe `Car` também sobrescreve a propriedade `description` que herda de `Vehicle`,
para fornecer uma descrição personalizada que inclui a marcha atual:

```swift
class Car: Vehicle {
    var gear = 1
    override var description: String {
        return super.description + " in gear \(gear)"
    }
}
```

<!--
  - test: `inheritance`

  ```swifttest
  -> class Car: Vehicle {
        var gear = 1
        override var description: String {
           return super.description + " in gear \(gear)"
        }
     }
  ```
-->

A sobrescrita da propriedade `description` começa chamando `super.description`,
que retorna a propriedade `description` da classe `Vehicle`.
A versão de `description` da classe `Car` então acrescenta algum texto extra no
final dessa descrição para fornecer informações sobre a marcha atual.

Se você criar uma instância da classe `Car`
e definir suas propriedades `gear` e `currentSpeed`,
vê que a propriedade `description` retorna
a descrição sob medida definida na classe `Car`:

```swift
let car = Car()
car.currentSpeed = 25.0
car.gear = 3
print("Car: \(car.description)")
// Car: traveling at 25.0 miles per hour in gear 3
```

<!--
  - test: `inheritance`

  ```swifttest
  -> let car = Car()
  -> car.currentSpeed = 25.0
  -> car.gear = 3
  -> print("Car: \(car.description)")
  </ Car: traveling at 25.0 miles per hour in gear 3
  ```
-->

#### Sobrescrevendo observadores de propriedade

Você pode usar a sobrescrita de propriedades para adicionar observadores de propriedade a uma propriedade herdada.
Isso permite ser notificado quando o valor de uma propriedade herdada muda,
independentemente de como essa propriedade foi originalmente implementada.
Para mais informações sobre observadores de propriedade, veja <doc:Properties#Property-Observers>.

> Nota: Você não pode adicionar observadores de propriedade a
> propriedades armazenadas constantes herdadas nem a propriedades computadas somente leitura herdadas.
> O valor dessas propriedades não pode ser definido,
> então não é apropriado fornecer uma implementação de `willSet` ou `didSet`
> como parte de uma sobrescrita.
>
> Observe também que você não pode fornecer ao mesmo tempo
> um setter sobrescrito e um observador de propriedade sobrescrito para a mesma propriedade.
> Se você quer observar mudanças no valor de uma propriedade,
> e já fornece um setter personalizado para essa propriedade,
> pode simplesmente observar qualquer mudança de valor dentro do setter personalizado.

O exemplo a seguir define uma nova classe chamada `AutomaticCar`,
que é uma subclasse de `Car`.
A classe `AutomaticCar` representa um carro com câmbio automático,
que seleciona automaticamente uma marcha apropriada com base na velocidade atual:

```swift
class AutomaticCar: Car {
    override var currentSpeed: Double {
        didSet {
            gear = Int(currentSpeed / 10.0) + 1
        }
    }
}
```

<!--
  - test: `inheritance`

  ```swifttest
  -> class AutomaticCar: Car {
        override var currentSpeed: Double {
           didSet {
              gear = Int(currentSpeed / 10.0) + 1
           }
        }
     }
  ```
-->

Sempre que você define a propriedade `currentSpeed` de uma instância de `AutomaticCar`,
o observador `didSet` da propriedade define a propriedade `gear` da instância como
uma marcha apropriada para a nova velocidade.
Especificamente, o observador de propriedade escolhe uma marcha que é
o novo valor de `currentSpeed` dividido por `10`,
arredondado para baixo até o inteiro mais próximo, mais `1`.
Uma velocidade de `35.0` produz a marcha `4`:

```swift
let automatic = AutomaticCar()
automatic.currentSpeed = 35.0
print("AutomaticCar: \(automatic.description)")
// AutomaticCar: traveling at 35.0 miles per hour in gear 4
```

<!--
  - test: `inheritance`

  ```swifttest
  -> let automatic = AutomaticCar()
  -> automatic.currentSpeed = 35.0
  -> print("AutomaticCar: \(automatic.description)")
  </ AutomaticCar: traveling at 35.0 miles per hour in gear 4
  ```
-->

## Impedindo sobrescritas

Você pode impedir que um método, propriedade ou subscript seja sobrescrito
marcando-o como *final*.
Para fazer isso, escreva o modificador `final` antes
da palavra-chave introdutora do método, da propriedade ou do subscript
(como `final var`, `final func`, `final class func` e `final subscript`).

Qualquer tentativa de sobrescrever um método, propriedade ou subscript final em uma subclasse
é reportada como erro de compilação.
Métodos, propriedades ou subscripts que você adiciona a uma classe em uma extension
também podem ser marcados como final na definição da extension.
Para mais informações, veja <doc:Extensions>.

<!--
  - test: `finalPreventsOverriding`

  ```swifttest
  -> class C {
        final var someVar = 0
        final func someFunction() {
           print("In someFunction")
        }
     }
  -> class D : C {
        override var someVar: Int {
           get { return 1 }
           set {}
        }
        override func someFunction() {
           print("In overridden someFunction")
        }
     }
  !$ error: property overrides a 'final' property
  !! override var someVar: Int {
  !! ^
  !$ note: overridden declaration is here
  !! final var someVar = 0
  !! ^
  !$ error: instance method overrides a 'final' instance method
  !! override func someFunction() {
  !! ^
  !$ note: overridden declaration is here
  !! final func someFunction() {
  !! ^
  ```
-->

Você pode marcar uma classe inteira como final escrevendo o modificador `final`
antes da palavra-chave `class` na definição da classe (`final class`).
Qualquer tentativa de criar uma subclasse de uma classe final é reportada como erro de compilação.

<!--
  - test: `finalClassPreventsOverriding`

  ```swifttest
  -> final class C {
        var someVar = 0
        func someFunction() {
           print("In someFunction")
        }
     }
  -> class D : C {
        override var someVar: Int {
           get { return 1 }
           set {}
        }
        override func someFunction() {
           print("In overridden someFunction")
        }
     }
  !$ error: property overrides a 'final' property
  !!      override var someVar: Int {
  !!                   ^
  !$ note: overridden declaration is here
  !!      var someVar = 0
  !!          ^
  !$ error: instance method overrides a 'final' instance method
  !!      override func someFunction() {
  !!                    ^
  !$ note: overridden declaration is here
  !!      func someFunction() {
  !!           ^
  !$ error: inheritance from a final class 'C'
  !! class D : C {
  !!       ^
  ```
-->

<!--
  TODO: I should probably provide an example here.
-->

<!--
  TODO: provide more information about function signatures,
  and what does / doesn't make them unique.
  For example, the parameter names don't have to match
  in order for a function to override a similar signature in its parent.
  (This is true for both of the function declaration syntaxes.)
-->

<!--
  TODO: Mention that you can return more-specific types, and take less-specific types,
  when overriding methods that use optionals / unchecked optionals.

  TODO: Overriding Type Methods
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->

<!-- ia-translate: true -->
