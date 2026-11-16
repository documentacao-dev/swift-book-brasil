# Tipos opacos e tipos de protocolo boxed

Oculte detalhes de implementação sobre o tipo de um valor.

O Swift oferece duas formas de ocultar detalhes sobre o tipo de um valor:
tipos opacos e tipos de protocolo boxed.
Ocultar informações de tipo
é útil nas fronteiras entre
um módulo e o código que chama o módulo,
porque o tipo concreto do valor de retorno pode continuar privado.

Uma função ou método que retorna um tipo opaco
oculta as informações de tipo do valor de retorno.
Em vez de informar um tipo concreto como tipo de retorno da função,
o valor de retorno é descrito pelos protocolos que ele oferece.
Tipos opacos preservam a identidade de tipo:
o compilador tem acesso às informações de tipo,
mas quem usa o módulo não tem.

Um tipo de protocolo boxed pode armazenar uma instância de qualquer tipo
que esteja em conformidade com o protocolo indicado.
Tipos de protocolo boxed não preservam a identidade de tipo:
o tipo específico do valor só é conhecido em tempo de execução,
e pode mudar ao longo do tempo, conforme diferentes valores são armazenados.

## O problema que os tipos opacos resolvem

Por exemplo,
suponha que você está escrevendo um módulo que desenha formas em arte ASCII.
A característica básica de uma forma em arte ASCII
é uma função `draw()` que retorna a representação em string dessa forma,
o que você pode usar como requisito do protocolo `Shape`:

```swift
protocol Shape {
    func draw() -> String
}

struct Triangle: Shape {
    var size: Int
    func draw() -> String {
       var result: [String] = []
       for length in 1...size {
           result.append(String(repeating: "*", count: length))
       }
       return result.joined(separator: "\n")
    }
}
let smallTriangle = Triangle(size: 3)
print(smallTriangle.draw())
// *
// **
// ***
```

<!--
  - test: `opaque-result`

  ```swifttest
  -> protocol Shape {
         func draw() -> String
     }

  -> struct Triangle: Shape {
        var size: Int
        func draw() -> String {
            var result: [String] = []
            for length in 1...size {
                result.append(String(repeating: "*", count: length))
            }
            return result.joined(separator: "\n")
        }
     }
  -> let smallTriangle = Triangle(size: 3)
  -> print(smallTriangle.draw())
  </ *
  </ **
  </ ***
  ```
-->

Você poderia usar generics para implementar operações como inverter uma forma verticalmente,
como mostra o código abaixo.
Porém, essa abordagem tem uma limitação importante:
a forma invertida expõe os tipos genéricos exatos
que foram usados para criá-la.

```swift
struct FlippedShape<T: Shape>: Shape {
    var shape: T
    func draw() -> String {
        let lines = shape.draw().split(separator: "\n")
        return lines.reversed().joined(separator: "\n")
    }
}
let flippedTriangle = FlippedShape(shape: smallTriangle)
print(flippedTriangle.draw())
// ***
// **
// *
```

<!--
  - test: `opaque-result`

  ```swifttest
  -> struct FlippedShape<T: Shape>: Shape {
         var shape: T
         func draw() -> String {
             let lines = shape.draw().split(separator: "\n")
             return lines.reversed().joined(separator: "\n")
         }
     }
  -> let flippedTriangle = FlippedShape(shape: smallTriangle)
  -> print(flippedTriangle.draw())
  </ ***
  </ **
  </ *
  ```
-->

Essa abordagem de definir um struct `JoinedShape<T: Shape, U: Shape>`
que une duas formas verticalmente, como mostra o código abaixo,
resulta em tipos como `JoinedShape<Triangle, FlippedShape<Triangle>>`
ao unir um triângulo com um triângulo invertido.

```swift
struct JoinedShape<T: Shape, U: Shape>: Shape {
    var top: T
    var bottom: U
    func draw() -> String {
       return top.draw() + "\n" + bottom.draw()
    }
}
let joinedTriangles = JoinedShape(top: smallTriangle, bottom: flippedTriangle)
print(joinedTriangles.draw())
// *
// **
// ***
// ***
// **
// *
```

<!--
  - test: `opaque-result`

  ```swifttest
  -> struct JoinedShape<T: Shape, U: Shape>: Shape {
        var top: T
        var bottom: U
        func draw() -> String {
            return top.draw() + "\n" + bottom.draw()
        }
     }
  -> let joinedTriangles = JoinedShape(top: smallTriangle, bottom: flippedTriangle)
  -> print(joinedTriangles.draw())
  </ *
  </ **
  </ ***
  </ ***
  </ **
  </ *
  ```
-->

Expor informações detalhadas sobre a criação de uma forma
permite que tipos que não deveriam fazer parte
da interface pública do módulo de arte ASCII vazem para fora,
porque é preciso declarar o tipo de retorno completo.
O código dentro do módulo
poderia montar a mesma forma de várias maneiras,
e o código externo que usa a forma
não deveria precisar lidar com os detalhes de implementação sobre a lista de transformações.
Tipos que encapsulam outros, como `JoinedShape` e `FlippedShape`,
não importam para quem usa o módulo,
e eles não deveriam ficar visíveis.
A interface pública do módulo
consiste em operações como unir e inverter uma forma,
e essas operações retornam outro valor do tipo `Shape`.

## Retornando um tipo opaco

Você pode pensar em um tipo opaco como o inverso de um tipo genérico.
Tipos genéricos permitem que o código que chama uma função
escolha o tipo dos parâmetros e do valor de retorno dessa função,
sem depender da implementação da função.
Por exemplo, a função do código a seguir
retorna um tipo que depende de quem a chama:

```swift
func max<T>(_ x: T, _ y: T) -> T where T: Comparable { ... }
```

<!--
  From https://developer.apple.com/documentation/swift/max(_:_:)
  Not test code because it won't actually compile
  and there's nothing to meaningfully test.
-->

O código que chama `max(_:_:)` escolhe os valores de `x` e `y`,
e o tipo desses valores determina o tipo concreto de `T`.
O código que chama pode usar qualquer tipo
que esteja em conformidade com o protocolo `Comparable`.
O código dentro da função é escrito de forma geral
para lidar com qualquer tipo que quem chama fornecer.
A implementação de `max(_:_:)` usa apenas as funcionalidades
que todos os tipos `Comparable` compartilham.

Os papéis se invertem em uma função com tipo de retorno opaco.
Um tipo opaco permite que a implementação da função escolha o tipo
do valor que ela retorna, sem depender do código que chama a função.
Por exemplo, a função do exemplo a seguir retorna um trapézio
sem expor o tipo subjacente dessa forma.

```swift
struct Square: Shape {
    var size: Int
    func draw() -> String {
        let line = String(repeating: "*", count: size)
        let result = Array<String>(repeating: line, count: size)
        return result.joined(separator: "\n")
    }
}

func makeTrapezoid() -> some Shape {
    let top = Triangle(size: 2)
    let middle = Square(size: 2)
    let bottom = FlippedShape(shape: top)
    let trapezoid = JoinedShape(
        top: top,
        bottom: JoinedShape(top: middle, bottom: bottom)
    )
    return trapezoid
}
let trapezoid = makeTrapezoid()
print(trapezoid.draw())
// *
// **
// **
// **
// **
// *
```

<!--
  - test: `opaque-result`

  ```swifttest
  -> struct Square: Shape {
         var size: Int
         func draw() -> String {
             let line = String(repeating: "*", count: size)
             let result = Array<String>(repeating: line, count: size)
             return result.joined(separator: "\n")
         }
     }

  -> func makeTrapezoid() -> some Shape {
         let top = Triangle(size: 2)
         let middle = Square(size: 2)
         let bottom = FlippedShape(shape: top)
         let trapezoid = JoinedShape(
             top: top,
             bottom: JoinedShape(top: middle, bottom: bottom)
         )
         return trapezoid
     }
  -> let trapezoid = makeTrapezoid()
  -> print(trapezoid.draw())
  </ *
  </ **
  </ **
  </ **
  </ **
  </ *
  ```
-->

A função `makeTrapezoid()` deste exemplo
declara seu tipo de retorno como `some Shape`;
com isso, a função
retorna um valor de algum tipo específico que está em conformidade com o protocolo `Shape`,
sem especificar nenhum tipo concreto em particular.
Escrever `makeTrapezoid()` dessa forma permite expressar
o aspecto fundamental de sua interface pública ---
o valor que ela retorna é uma forma ---
sem tornar os tipos específicos que compõem a forma
parte da interface pública.
Esta implementação usa dois triângulos e um quadrado,
mas a função poderia ser reescrita para desenhar um trapézio
de várias outras maneiras
sem mudar o tipo de retorno.

Este exemplo mostra como um tipo de retorno opaco
é o inverso de um tipo genérico.
O código dentro de `makeTrapezoid()` pode retornar qualquer tipo de que precisar,
desde que esse tipo esteja em conformidade com o protocolo `Shape`,
assim como faz o código que chama uma função genérica.
O código que chama a função precisa ser escrito de forma geral,
como a implementação de uma função genérica,
para que possa trabalhar com qualquer valor `Shape`
retornado por `makeTrapezoid()`.

Você também pode combinar tipos de retorno opacos com generics.
As funções do código a seguir retornam, ambas, um valor
de algum tipo que está em conformidade com o protocolo `Shape`.

```swift
func flip<T: Shape>(_ shape: T) -> some Shape {
    return FlippedShape(shape: shape)
}
func join<T: Shape, U: Shape>(_ top: T, _ bottom: U) -> some Shape {
    JoinedShape(top: top, bottom: bottom)
}

let opaqueJoinedTriangles = join(smallTriangle, flip(smallTriangle))
print(opaqueJoinedTriangles.draw())
// *
// **
// ***
// ***
// **
// *
```

<!--
  - test: `opaque-result`

  ```swifttest
  -> func flip<T: Shape>(_ shape: T) -> some Shape {
         return FlippedShape(shape: shape)
     }
  -> func join<T: Shape, U: Shape>(_ top: T, _ bottom: U) -> some Shape {
         JoinedShape(top: top, bottom: bottom)
     }

  -> let opaqueJoinedTriangles = join(smallTriangle, flip(smallTriangle))
  -> print(opaqueJoinedTriangles.draw())
  </ *
  </ **
  </ ***
  </ ***
  </ **
  </ *
  ```
-->

O valor de `opaqueJoinedTriangles` neste exemplo
é o mesmo que `joinedTriangles` no exemplo de generics
na seção <doc:OpaqueTypes#The-Problem-that-Opaque-Types-Solve> anterior neste capítulo.
Porém, diferente do valor daquele exemplo,
`flip(_:)` e `join(_:_:)` envolvem os tipos subjacentes
que as operações genéricas de forma retornam
em um tipo de retorno opaco,
o que impede que esses tipos fiquem visíveis.
As duas funções são genéricas porque os tipos de que dependem são genéricos,
e os parâmetros genéricos da função
repassam as informações de tipo que `FlippedShape` e `JoinedShape` precisam.

Se uma função com tipo de retorno opaco
retorna a partir de vários pontos,
todos os valores de retorno possíveis precisam ter o mesmo tipo.
Em uma função genérica,
esse tipo de retorno pode usar os parâmetros genéricos da função,
mas continua precisando ser um único tipo.
Por exemplo,
aqui está uma versão *inválida* da função que inverte formas,
com um caso especial para quadrados:

```swift
func invalidFlip<T: Shape>(_ shape: T) -> some Shape {
    if shape is Square {
        return shape // Error: Return types don't match.
    }
    return FlippedShape(shape: shape) // Error: Return types don't match.
}
```

<!--
  - test: `opaque-result-err`

  ```swifttest
  >> protocol Shape {
  >>     func draw() -> String
  >> }
  >> struct Square: Shape {
  >>     func draw() -> String { return "#" }  // stub implementation
  >> }
  >> struct FlippedShape<T: Shape>: Shape {
  >>     var shape: T
  >>     func draw() -> String { return "#" } // stub implementation
  >> }
  -> func invalidFlip<T: Shape>(_ shape: T) -> some Shape {
         if shape is Square {
             return shape // Error: Return types don't match.
         }
         return FlippedShape(shape: shape) // Error: Return types don't match.
     }
  !$ error: function declares an opaque return type 'some Shape', but the return statements in its body do not have matching underlying types
  !! func invalidFlip<T: Shape>(_ shape: T) -> some Shape {
  !!      ^                                    ~~~~~~~~~~
  !$ note: return statement has underlying type 'T'
  !! return shape // Error: Return types don't match.
  !! ^
  !$ note: return statement has underlying type 'FlippedShape<T>'
  !! return FlippedShape(shape: shape) // Error: Return types don't match.
  !! ^
  ```
-->

Se você chamar essa função com um `Square`, ela retorna um `Square`;
caso contrário, retorna um `FlippedShape`.
Isso viola a exigência de retornar valores de um único tipo
e torna `invalidFlip(_:)` código inválido.
Uma forma de corrigir `invalidFlip(_:)` é mover o caso especial para quadrados
para dentro da implementação de `FlippedShape`,
o que permite que essa função sempre retorne um valor `FlippedShape`:

```swift
struct FlippedShape<T: Shape>: Shape {
    var shape: T
    func draw() -> String {
        if shape is Square {
           return shape.draw()
        }
        let lines = shape.draw().split(separator: "\n")
        return lines.reversed().joined(separator: "\n")
    }
}
```

<!--
  - test: `opaque-result-special-flip`

  ```swifttest
  >> protocol Shape { func draw() -> String }
  >> struct Square: Shape {
  >>     func draw() -> String { return "#" }  // stub implementation
  >> }
  -> struct FlippedShape<T: Shape>: Shape {
         var shape: T
         func draw() -> String {
             if shape is Square {
                return shape.draw()
             }
             let lines = shape.draw().split(separator: "\n")
             return lines.reversed().joined(separator: "\n")
         }
     }
  ```
-->

<!--
  Another way to fix it is with type erasure.
  Define a wrapper called AnyShape,
  and wrap whatever shape you created inside invalidFlip(_:)
  before returning it.
  That example is long enough that it breaks the flow here.
-->

A exigência de sempre retornar um único tipo
não impede você de usar generics em um tipo de retorno opaco.
Aqui está um exemplo de função que incorpora o parâmetro de tipo
ao tipo subjacente do valor que ela retorna:

```swift
func `repeat`<T: Shape>(shape: T, count: Int) -> some Collection {
    return Array<T>(repeating: shape, count: count)
}
```

<!--
  - test: `opaque-result`

  ```swifttest
  -> func `repeat`<T: Shape>(shape: T, count: Int) -> some Collection {
         return Array<T>(repeating: shape, count: count)
     }
  ```
-->

Nesse caso,
o tipo subjacente do valor de retorno
varia conforme `T`:
qualquer que seja a forma passada,
`repeat(shape:count:)` cria e retorna um array com essa forma.
Mesmo assim,
o valor de retorno sempre tem o mesmo tipo subjacente `[T]`,
então a função segue a exigência de que funções com tipo de retorno opaco
retornem valores de um único tipo.

## Tipos de protocolo boxed

Um tipo de protocolo boxed também é chamado às vezes de *tipo existencial*,
termo que vem da frase
"existe um tipo *T* tal que *T* está em conformidade com o protocolo".
Para criar um tipo de protocolo boxed,
escreva `any` antes do nome do protocolo.
Veja um exemplo:

```swift
struct VerticalShapes: Shape {
    var shapes: [any Shape]
    func draw() -> String {
        return shapes.map { $0.draw() }.joined(separator: "\n\n")
    }
}

let largeTriangle = Triangle(size: 5)
let largeSquare = Square(size: 5)
let vertical = VerticalShapes(shapes: [largeTriangle, largeSquare])
print(vertical.draw())
```

<!--
  - test: `boxed-protocol-types`

  ```swifttest
   >> protocol Shape {
   >>    func draw() -> String
   >> }
   >> struct Triangle: Shape {
   >>    var size: Int
   >>    func draw() -> String {
   >>        var result: [String] = []
   >>        for length in 1...size {
   >>            result.append(String(repeating: "*", count: length))
   >>        }
   >>        return result.joined(separator: "\n")
   >>    }
   >> }
   >> struct Square: Shape {
   >>     var size: Int
   >>     func draw() -> String {
   >>         let line = String(repeating: "*", count: size)
   >>         let result = Array<String>(repeating: line, count: size)
   >>         return result.joined(separator: "\n")
   >>     }
   >
   -> struct VerticalShapes: Shape {
          var shapes: [any Shape]
          func draw() -> String {
              return shapes.map { $0.draw() }.joined(separator: "\n\n")
          }
      }
   ->
   -> let largeTriangle = Triangle(size: 5)
   -> let largeSquare = Square(size: 5)
   -> let vertical = VerticalShapes(shapes: [largeTriangle, largeSquare])
   -> print(vertical.draw())
   << *
   << **
   << ***
   << ****
   << *****
   <<-
   << *****
   << *****
   << *****
   << *****
   << *****
  ```
-->

No exemplo acima,
`VerticalShapes` declara o tipo de `shapes` como `[any Shape]` ---
um array de elementos `Shape` boxed.
Cada elemento do array pode ser de um tipo diferente,
e cada um desses tipos precisa estar em conformidade com o protocolo `Shape`.
Para oferecer essa flexibilidade em tempo de execução,
o Swift adiciona um nível de indireção quando necessário ---
essa indireção se chama *box*,
e tem um custo de desempenho.

Dentro do tipo `VerticalShapes`,
o código pode usar métodos, propriedades e subscripts
exigidos pelo protocolo `Shape`.
Por exemplo, o método `draw()` de `VerticalShapes`
chama o método `draw()` de cada elemento do array.
Esse método está disponível porque `Shape` exige um método `draw()`.
Já tentar acessar a propriedade `size` do triângulo,
ou qualquer outra propriedade ou método que não seja exigido por `Shape`,
gera um erro.

Compare os três tipos que você poderia usar para `shapes`:

- Usando generics,
  escrevendo `struct VerticalShapes<S: Shape>` e `var shapes: [S]`,
  cria-se um array cujos elementos são um tipo específico de forma,
  e a identidade desse tipo específico
  fica visível para qualquer código que interaja com o array.

- Usando um tipo opaco,
  escrevendo `var shapes: [some Shape]`,
  cria-se um array cujos elementos são um tipo específico de forma,
  e a identidade desse tipo específico fica oculta.

- Usando um tipo de protocolo boxed,
  escrevendo `var shapes: [any Shape]`,
  cria-se um array que pode armazenar elementos de tipos diferentes,
  e a identidade desses tipos fica oculta.

Neste caso,
um tipo de protocolo boxed é a única abordagem
que permite que quem usa `VerticalShapes` misture formas de tipos diferentes.

Você pode usar uma conversão com `as`
quando souber o tipo subjacente de um valor boxed.
Por exemplo:

```swift
if let downcastTriangle = vertical.shapes[0] as? Triangle {
    print(downcastTriangle.size)
}
// Prints "5".
```

Para mais informações, consulte <doc:TypeCasting#Downcasting>.

## Diferenças entre tipos opacos e tipos de protocolo boxed

Retornar um tipo opaco se parece muito com usar um tipo de protocolo boxed
como tipo de retorno de uma função,
mas esses dois tipos de retorno diferem
em preservar ou não a identidade de tipo.
Um tipo opaco se refere a um tipo específico,
embora quem chama a função não consiga ver qual é esse tipo;
um tipo de protocolo boxed pode se referir a qualquer tipo que esteja em conformidade com o protocolo.
Em geral,
tipos de protocolo boxed dão mais flexibilidade
quanto aos tipos subjacentes dos valores que armazenam,
e tipos opacos permitem garantias mais fortes
sobre esses tipos subjacentes.

Por exemplo,
veja uma versão de `flip(_:)`
que usa um tipo de protocolo boxed como tipo de retorno
em vez de um tipo de retorno opaco:

```swift
func protoFlip<T: Shape>(_ shape: T) -> Shape {
    return FlippedShape(shape: shape)
}
```

<!--
  - test: `opaque-result-existential-error`

  ```swifttest
  >> protocol Shape {
  >>     func draw() -> String
  >> }
  >> struct Triangle: Shape {
  >>     var size: Int
  >>     func draw() -> String { return "#" }  // stub implementation
  >> }
  >> struct Square: Shape {
  >>     var size: Int
  >>     func draw() -> String { return "#" }  // stub implementation
  >> }
  >> struct FlippedShape<T: Shape>: Shape {
  >>     var shape: T
  >>     func draw() -> String { return "#" } // stub implementation
  >> }
  -> func protoFlip<T: Shape>(_ shape: T) -> Shape {
        return FlippedShape(shape: shape)
     }
  ```
-->

Esta versão de `protoFlip(_:)`
tem o mesmo corpo de `flip(_:)`,
e sempre retorna um valor do mesmo tipo.
Diferente de `flip(_:)`,
o valor que `protoFlip(_:)` retorna não é obrigado
a sempre ter o mesmo tipo ---
ele só precisa estar em conformidade com o protocolo `Shape`.
Dito de outra forma,
`protoFlip(_:)` estabelece com quem a chama um contrato de API muito mais frouxo
do que `flip(_:)` faz.
Ela se reserva a flexibilidade de retornar valores de vários tipos:

```swift
func protoFlip<T: Shape>(_ shape: T) -> Shape {
    if shape is Square {
        return shape
    }

    return FlippedShape(shape: shape)
}
```

<!--
  - test: `opaque-result-existential-error`

  ```swifttest
  -> func protoFlip<T: Shape>(_ shape: T) -> Shape {
        if shape is Square {
           return shape
        }

        return FlippedShape(shape: shape)
     }
  !$ error: invalid redeclaration of 'protoFlip'
  !! func protoFlip<T: Shape>(_ shape: T) -> Shape {
  !!      ^
  !$ note: 'protoFlip' previously declared here
  !! func protoFlip<T: Shape>(_ shape: T) -> Shape {
  !!      ^
  ```
-->

A versão revisada do código retorna
uma instância de `Square` ou uma instância de `FlippedShape`,
dependendo da forma passada.
Duas formas invertidas retornadas por essa função
podem ter tipos completamente diferentes.
Outras versões válidas desta função poderiam retornar valores de tipos diferentes
ao inverter várias instâncias da mesma forma.
A informação de tipo menos específica de `protoFlip(_:)` faz com que
muitas operações que dependem de informações de tipo
não estejam disponíveis no valor retornado.
Por exemplo, não é possível escrever um operador `==`
que compare os resultados retornados por esta função.

```swift
let protoFlippedTriangle = protoFlip(smallTriangle)
let sameThing = protoFlip(smallTriangle)
protoFlippedTriangle == sameThing  // Error
```

<!--
  - test: `opaque-result-existential-error`

  ```swifttest
  >> let smallTriangle = Triangle(size: 3)
  -> let protoFlippedTriangle = protoFlip(smallTriangle)
  -> let sameThing = protoFlip(smallTriangle)
  -> protoFlippedTriangle == sameThing  // Error
  !$ error: binary operator '==' cannot be applied to two 'any Shape' operands
  !! protoFlippedTriangle == sameThing  // Error
  !! ~~~~~~~~~~~~~~~~~~~~ ^  ~~~~~~~~~
  ```
-->

O erro na última linha do exemplo acontece por vários motivos.
O problema imediato é que `Shape` não inclui um operador `==`
entre os requisitos do protocolo.
Se você tentar adicionar um, o próximo problema
é que o operador `==` precisa conhecer
os tipos dos seus argumentos da esquerda e da direita.
Esse tipo de operador costuma receber argumentos do tipo `Self`,
correspondendo ao tipo concreto que adota o protocolo,
mas adicionar um requisito `Self` ao protocolo
não permite o apagamento de tipo que acontece
quando você usa o protocolo como tipo.

Usar um tipo de protocolo boxed como tipo de retorno de uma função
dá a flexibilidade de retornar qualquer tipo que esteja em conformidade com o protocolo.
Porém, o custo dessa flexibilidade
é que algumas operações não são possíveis nos valores retornados.
O exemplo mostra que o operador `==` não está disponível ---
ele depende de informações de tipo específicas
que não são preservadas ao usar um tipo de protocolo boxed.

Outro problema dessa abordagem é que as transformações de forma não se aninham.
O resultado de inverter um triângulo é um valor do tipo `Shape`,
e a função `protoFlip(_:)` recebe um argumento
de algum tipo que está em conformidade com o protocolo `Shape`.
Porém, um valor de tipo de protocolo boxed não está em conformidade com esse protocolo;
o valor retornado por `protoFlip(_:)` não está em conformidade com `Shape`.
Isso significa que código como `protoFlip(protoFlip(smallTriangle))`,
que aplica várias transformações, é inválido,
porque a forma invertida não é um argumento válido para `protoFlip(_:)`.

Em contraste,
tipos opacos preservam a identidade do tipo subjacente.
O Swift consegue inferir tipos associados,
o que permite usar um valor de retorno opaco
em lugares onde um tipo de protocolo boxed não pode ser usado como valor de retorno.
Por exemplo,
veja uma versão do protocolo `Container` de <doc:Generics>:

```swift
protocol Container {
    associatedtype Item
    var count: Int { get }
    subscript(i: Int) -> Item { get }
}
extension Array: Container { }
```

<!--
  - test: `opaque-result, opaque-result-existential-error`

  ```swifttest
  -> protocol Container {
         associatedtype Item
         var count: Int { get }
         subscript(i: Int) -> Item { get }
     }
  -> extension Array: Container { }
  ```
-->

Você não pode usar `Container` como tipo de retorno de uma função
porque esse protocolo tem um tipo associado.
Também não pode usá-lo como restrição em um tipo de retorno genérico,
porque não há informação suficiente fora do corpo da função
para inferir qual deve ser o tipo genérico.

```swift
// Error: Protocol with associated types can't be used as a return type.
func makeProtocolContainer<T>(item: T) -> Container {
    return [item]
}

// Error: Not enough information to infer C.
func makeProtocolContainer<T, C: Container>(item: T) -> C {
    return [item]
}
```

<!--
  - test: `opaque-result-existential-error`

  ```swifttest
  // Error: Protocol with associated types can't be used as a return type.
  -> func makeProtocolContainer<T>(item: T) -> Container {
         return [item]
     }

  // Error: Not enough information to infer C.
  -> func makeProtocolContainer<T, C: Container>(item: T) -> C {
         return [item]
     }
  !$ error: use of protocol 'Container' as a type must be written 'any Container'
  !! func makeProtocolContainer<T>(item: T) -> Container {
  !!                                           ^~~~~~~~~
  !! any Container
  !$ error: cannot convert return expression of type '[T]' to return type 'C'
  !! return [item]
  !! ^~~~~~
  !! as! C
  ```
-->

Usar o tipo opaco `some Container` como tipo de retorno
expressa o contrato de API desejado: a função retorna um container,
mas não especifica o tipo desse container:

```swift
func makeOpaqueContainer<T>(item: T) -> some Container {
    return [item]
}
let opaqueContainer = makeOpaqueContainer(item: 12)
let twelve = opaqueContainer[0]
print(type(of: twelve))
// Prints "Int".
```

<!--
  - test: `opaque-result`

  ```swifttest
  -> func makeOpaqueContainer<T>(item: T) -> some Container {
         return [item]
     }
  -> let opaqueContainer = makeOpaqueContainer(item: 12)
  -> let twelve = opaqueContainer[0]
  -> print(type(of: twelve))
  <- Int
  ```
-->

O tipo de `twelve` é inferido como `Int`,
o que mostra que a inferência de tipos funciona com tipos opacos.
Na implementação de `makeOpaqueContainer(item:)`,
o tipo subjacente do container opaco é `[T]`.
Neste caso, `T` é `Int`,
então o valor retornado é um array de inteiros
e o tipo associado `Item` é inferido como `Int`.
O subscript de `Container` retorna `Item`,
o que significa que o tipo de `twelve` também é inferido como `Int`.

<!--
  TODO: Expansion for the future

  You can combine the flexibility of returning a value of protocol type
  with the API-boundary enforcement of opaque types
  by using type erasure
  like the Swift standard library uses in the
  `AnySequence <//apple_ref/fake/AnySequence`_ type.

  protocol P { func f() -> Int }

  struct AnyP: P {
      var p: P
      func f() -> Int { return p.f() }
  }

  struct P1 {
      func f() -> Int { return 100 }
  }
  struct P2 {
      func f() -> Int { return 200 }
  }

  func opaque(x: Int) -> some P {
      let result: P
      if x > 100 {
          result = P1()
      }  else {
          result = P2()
      }
      return AnyP(p: result)
  }
-->


## Tipos de parâmetro opacos

Além de escrever `some` para retornar um tipo opaco,
você também pode escrever `some` no tipo de um parâmetro
de uma função, subscript ou inicializador.
Porém, quando você escreve `some` no tipo de um parâmetro,
trata-se apenas de uma sintaxe mais curta para generics, e não de um tipo opaco.
Por exemplo,
as duas funções abaixo são equivalentes:

```swift
func drawTwiceGeneric<SomeShape: Shape>(_ shape: SomeShape) -> String {
    let drawn = shape.draw()
    return drawn + "\n" + drawn
}

func drawTwiceSome(_ shape: some Shape) -> String {
    let drawn = shape.draw()
    return drawn + "\n" + drawn
}
```

A função `drawTwiceGeneric(_:)` declara um parâmetro de tipo genérico chamado `SomeShape`,
com uma restrição que exige que `SomeShape` esteja em conformidade com o protocolo `Shape`.
A função `drawTwiceSome(_:)`
usa o tipo `some Shape` para o argumento.
Isso cria um novo parâmetro de tipo genérico, sem nome, para a função,
com uma restrição que exige que o tipo esteja em conformidade com o protocolo `Shape`.
Como o tipo genérico não tem nome,
você não consegue se referir a esse tipo em outro lugar da função.

Se você escrever `some` antes do tipo de mais de um parâmetro,
cada um dos tipos genéricos é independente.
Por exemplo:

```swift
func combine(shape s1: some Shape, with s2: some Shape) -> String {
    return s1.draw() + "\n" + s2.draw()
}

combine(smallTriangle, trapezoid)
```

Na função `combine(shape:with:)`,
os tipos do primeiro e do segundo parâmetro
precisam estar, ambos, em conformidade com o protocolo `Shape`,
mas não há restrição que exija que sejam o mesmo tipo.
Ao chamar `combine(shape:with)`,
você pode passar duas formas diferentes ---
neste caso, um triângulo e um trapézio.

Diferente da sintaxe para parâmetros de tipo genérico nomeados,
descrita no capítulo <doc:Generics>,
essa sintaxe mais leve não pode incluir
uma cláusula `where` genérica nem restrições de mesmo tipo (`==`).
Além disso,
usar a sintaxe mais leve para restrições muito complexas
pode dificultar a leitura.

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
