# Conversão de tipos

Determine o tipo de tempo de execução de um valor e dê a ele informações de tipo mais específicas.

*Conversão de tipos* é uma forma de verificar o tipo de uma instância,
ou de tratar essa instância como uma superclasse ou subclasse diferente
dentro da própria hierarquia de classes.

A conversão de tipos em Swift é implementada com os operadores `is` e `as`.
Esses dois operadores oferecem uma forma simples e expressiva
de verificar o tipo de um valor ou converter um valor para outro tipo.

Você também pode usar a conversão de tipos para verificar se um tipo está em conformidade com um protocolo,
como descrito em <doc:Protocols#Checking-for-Protocol-Conformance>.

## Definindo uma hierarquia de classes para conversão de tipos

Você pode usar a conversão de tipos com uma hierarquia de classes e subclasses
para verificar o tipo de uma instância de classe específica
e para converter essa instância para outra classe dentro da mesma hierarquia.
Os três trechos de código abaixo definem uma hierarquia de classes
e um array que contém instâncias dessas classes,
para usar em um exemplo de conversão de tipos.

O primeiro trecho define uma nova classe base chamada `MediaItem`.
Essa classe oferece funcionalidades básicas para qualquer tipo de item
que aparece em uma biblioteca de mídia digital.
Especificamente, ela declara uma propriedade `name` do tipo `String`
e um inicializador `init(name:)`.
(Presume-se que todos os itens de mídia, incluindo todos os filmes e músicas, terão um nome.)

```swift
class MediaItem {
    var name: String
    init(name: String) {
        self.name = name
    }
}
```

<!--
  - test: `typeCasting, typeCasting-err`

  ```swifttest
  -> class MediaItem {
        var name: String
        init(name: String) {
           self.name = name
        }
     }
  ```
-->

O próximo trecho define duas subclasses de `MediaItem`.
A primeira subclasse, `Movie`, encapsula informações adicionais sobre um filme.
Ela acrescenta uma propriedade `director` à classe base `MediaItem`,
com o inicializador correspondente.
A segunda subclasse, `Song`, acrescenta uma propriedade `artist`
e um inicializador à classe base:

```swift
class Movie: MediaItem {
    var director: String
    init(name: String, director: String) {
        self.director = director
        super.init(name: name)
    }
}

class Song: MediaItem {
    var artist: String
    init(name: String, artist: String) {
        self.artist = artist
        super.init(name: name)
    }
}
```

<!--
  - test: `typeCasting, typeCasting-err`

  ```swifttest
  -> class Movie: MediaItem {
        var director: String
        init(name: String, director: String) {
           self.director = director
           super.init(name: name)
        }
     }

  -> class Song: MediaItem {
        var artist: String
        init(name: String, artist: String) {
           self.artist = artist
           super.init(name: name)
        }
     }
  ```
-->

O último trecho cria uma constante array chamada `library`,
que contém duas instâncias de `Movie` e três instâncias de `Song`.
O tipo do array `library` é inferido
ao inicializá-lo com o conteúdo de um literal de array.
O verificador de tipos do Swift consegue deduzir que `Movie` e `Song` têm
uma superclasse em comum, `MediaItem`,
e por isso infere o tipo `[MediaItem]` para o array `library`:

```swift
let library = [
    Movie(name: "Casablanca", director: "Michael Curtiz"),
    Song(name: "Blue Suede Shoes", artist: "Elvis Presley"),
    Movie(name: "Citizen Kane", director: "Orson Welles"),
    Song(name: "The One And Only", artist: "Chesney Hawkes"),
    Song(name: "Never Gonna Give You Up", artist: "Rick Astley")
]
// the type of "library" is inferred to be [MediaItem]
```

<!--
  - test: `typeCasting`

  ```swifttest
  -> let library = [
        Movie(name: "Casablanca", director: "Michael Curtiz"),
        Song(name: "Blue Suede Shoes", artist: "Elvis Presley"),
        Movie(name: "Citizen Kane", director: "Orson Welles"),
        Song(name: "The One And Only", artist: "Chesney Hawkes"),
        Song(name: "Never Gonna Give You Up", artist: "Rick Astley")
     ]
  >> print(type(of: library))
  << Array<MediaItem>
  // the type of "library" is inferred to be [MediaItem]
  ```
-->

Os itens armazenados em `library` continuam sendo instâncias de `Movie` e `Song` por trás dos panos.
No entanto, se você percorrer o conteúdo desse array,
os itens que você recebe são tipados como `MediaItem`,
e não como `Movie` ou `Song`.
Para trabalhar com eles no tipo nativo,
você precisa *verificar* o tipo deles,
ou fazer *downcast* para outro tipo,
como descrito a seguir.

## Verificando o tipo

Use o *operador de verificação de tipo* (`is`) para verificar
se uma instância é de determinado tipo de subclasse.
O operador de verificação de tipo retorna `true` se a instância for desse tipo de subclasse
e `false` se não for.

O exemplo abaixo define duas variáveis, `movieCount` e `songCount`,
que contam quantas instâncias de `Movie` e de `Song` há no array `library`:

```swift
var movieCount = 0
var songCount = 0

for item in library {
    if item is Movie {
        movieCount += 1
    } else if item is Song {
        songCount += 1
    }
}

print("Media library contains \(movieCount) movies and \(songCount) songs")
// Prints "Media library contains 2 movies and 3 songs".
```

<!--
  - test: `typeCasting`

  ```swifttest
  -> var movieCount = 0
  -> var songCount = 0

  -> for item in library {
        if item is Movie {
           movieCount += 1
        } else if item is Song {
           songCount += 1
        }
     }

  -> print("Media library contains \(movieCount) movies and \(songCount) songs")
  <- Media library contains 2 movies and 3 songs
  ```
-->

Este exemplo percorre todos os itens do array `library`.
A cada passagem, o laço `for`-`in` define a constante `item`
como o próximo `MediaItem` do array.

`item is Movie` retorna `true` se o `MediaItem` atual
for uma instância de `Movie`, e `false` se não for.
De forma semelhante, `item is Song` verifica se o item é uma instância de `Song`.
Ao final do laço `for`-`in`, os valores de `movieCount` e `songCount`
contêm a contagem de quantas instâncias de `MediaItem` foram encontradas de cada tipo.

## Downcasting

Uma constante ou variável de determinado tipo de classe pode, na verdade,
referenciar uma instância de uma subclasse por trás dos panos.
Quando você achar que esse é o caso,
pode tentar fazer *downcast* para o tipo da subclasse
com um *operador de conversão de tipo* (`as?` ou `as!`).

Como o downcast pode falhar,
o operador de conversão de tipo vem em duas formas diferentes.
A forma condicional, `as?`, retorna um valor optional do tipo para o qual você está tentando fazer o downcast.
A forma forçada, `as!`, tenta o downcast e faz unwrap forçado do resultado
em uma única ação composta.

Use a forma condicional do operador de conversão de tipo (`as?`)
quando não tiver certeza de que o downcast vai dar certo.
Essa forma do operador sempre retorna um optional,
e o valor será `nil` se o downcast não for possível.
Assim você pode verificar se o downcast deu certo.

Use a forma forçada do operador de conversão de tipo (`as!`)
apenas quando tiver certeza de que o downcast sempre vai dar certo.
Essa forma do operador dispara um erro de tempo de execução
se você tentar fazer downcast para um tipo de classe incorreto.

O exemplo abaixo percorre cada `MediaItem` em `library`
e imprime uma descrição apropriada para cada item.
Para isso, ele precisa acessar cada item como um `Movie` ou `Song` de verdade,
e não apenas como um `MediaItem`.
Isso é necessário para que ele consiga acessar
a propriedade `director` ou `artist` de um `Movie` ou `Song`
e usá-la na descrição.

Neste exemplo, cada item do array pode ser um `Movie`
ou pode ser um `Song`.
Você não sabe de antemão qual classe real usar para cada item,
por isso é apropriado usar a forma condicional do operador de conversão de tipo (`as?`)
para verificar o downcast em cada passagem pelo laço:

```swift
for item in library {
    if let movie = item as? Movie {
        print("Movie: \(movie.name), dir. \(movie.director)")
    } else if let song = item as? Song {
        print("Song: \(song.name), by \(song.artist)")
    }
}

// Movie: Casablanca, dir. Michael Curtiz
// Song: Blue Suede Shoes, by Elvis Presley
// Movie: Citizen Kane, dir. Orson Welles
// Song: The One And Only, by Chesney Hawkes
// Song: Never Gonna Give You Up, by Rick Astley
```

<!--
  - test: `typeCasting`

  ```swifttest
  -> for item in library {
        if let movie = item as? Movie {
           print("Movie: \(movie.name), dir. \(movie.director)")
        } else if let song = item as? Song {
           print("Song: \(song.name), by \(song.artist)")
        }
     }

  </ Movie: Casablanca, dir. Michael Curtiz
  </ Song: Blue Suede Shoes, by Elvis Presley
  </ Movie: Citizen Kane, dir. Orson Welles
  </ Song: The One And Only, by Chesney Hawkes
  </ Song: Never Gonna Give You Up, by Rick Astley
  ```
-->

O exemplo começa tentando fazer o downcast do `item` atual para `Movie`.
Como `item` é uma instância de `MediaItem`, é possível que ele *seja* um `Movie`;
da mesma forma, também é possível que seja um `Song`,
ou mesmo apenas um `MediaItem` da base.
Por causa dessa incerteza, a forma `as?` do operador de conversão de tipo retorna um valor *optional*
ao tentar fazer o downcast para um tipo de subclasse.
O resultado de `item as? Movie` é do tipo `Movie?`, ou “`Movie` optional”.

O downcast para `Movie` falha quando aplicado às
instâncias de `Song` no array `library`.
Para lidar com isso, o exemplo acima usa optional binding
para verificar se o `Movie` optional realmente contém um valor
(ou seja, para descobrir se o downcast deu certo).
Esse optional binding é escrito como “`if let movie = item as? Movie`”,
que pode ser lido assim:

“Tente acessar `item` como um `Movie`.
Se isso der certo,
defina uma nova constante temporária chamada `movie` com
o valor armazenado no `Movie` optional retornado.”

Se o downcast der certo, as propriedades de `movie` são então usadas
para imprimir uma descrição dessa instância de `Movie`, incluindo o nome do `director`.
Um princípio semelhante é usado para verificar instâncias de `Song`
e imprimir uma descrição apropriada (incluindo o nome do `artist`)
sempre que um `Song` for encontrado na biblioteca.

> Nota: A conversão não modifica a instância nem altera os valores dela.
> A instância subjacente continua a mesma; ela simplesmente é tratada e acessada
> como uma instância do tipo para o qual foi convertida.

<!--
  TODO: This example should be followed by the same example written with switch,
  to introduce type casting in a pattern matching context
  and to set up the crazy Any example at the end of the chapter.
-->

<!--
  TODO: No section on upcasting because nobody can come up with
  an example that isn't excessively contrived.
  The reference shows the behavior in a contrived example.
-->

## Conversão de tipos para Any e AnyObject

O Swift oferece dois tipos especiais para trabalhar com tipos não específicos:

- `Any` pode representar uma instância de qualquer tipo, incluindo tipos de função.
- `AnyObject` pode representar uma instância de qualquer tipo de classe.

Use `Any` e `AnyObject` somente quando precisar explicitamente
do comportamento e dos recursos que eles oferecem.
É sempre melhor ser específico quanto aos tipos com os quais você espera trabalhar no código.

Aqui está um exemplo de uso de `Any` para trabalhar com uma mistura de tipos diferentes,
incluindo tipos de função e tipos que não são de classe.
O exemplo cria um array chamado `things`, que pode armazenar valores do tipo `Any`:

```swift
var things: [Any] = []

things.append(0)
things.append(0.0)
things.append(42)
things.append(3.14159)
things.append("hello")
things.append((3.0, 5.0))
things.append(Movie(name: "Ghostbusters", director: "Ivan Reitman"))
things.append({ (name: String) -> String in "Hello, \(name)" })
```

<!--
  - test: `typeCasting, typeCasting-err`

  ```swifttest
  -> var things: [Any] = []

  -> things.append(0)
  -> things.append(0.0)
  -> things.append(42)
  -> things.append(3.14159)
  -> things.append("hello")
  -> things.append((3.0, 5.0))
  -> things.append(Movie(name: "Ghostbusters", director: "Ivan Reitman"))
  -> things.append({ (name: String) -> String in "Hello, \(name)" })
  ```
-->

O array `things` contém
dois valores `Int`, dois valores `Double`, um valor `String`,
uma tupla do tipo `(Double, Double)`,
o filme “Ghostbusters”
e uma expressão de closure que recebe um valor `String`
e retorna outro valor `String`.

Para descobrir o tipo específico de uma constante ou variável
que se sabe ser apenas do tipo `Any` ou `AnyObject`,
você pode usar um padrão `is` ou `as` nos casos de uma instrução `switch`.
O exemplo abaixo percorre os itens do array `things`
e consulta o tipo de cada item com uma instrução `switch`.
Vários casos da instrução `switch` vinculam o valor correspondido a
uma constante do tipo especificado, para que o valor possa ser impresso:

```swift
for thing in things {
    switch thing {
    case 0 as Int:
        print("zero as an Int")
    case 0 as Double:
        print("zero as a Double")
    case let someInt as Int:
        print("an integer value of \(someInt)")
    case let someDouble as Double where someDouble > 0:
        print("a positive double value of \(someDouble)")
    case is Double:
        print("some other double value that I don't want to print")
    case let someString as String:
        print("a string value of \"\(someString)\"")
    case let (x, y) as (Double, Double):
        print("an (x, y) point at \(x), \(y)")
    case let movie as Movie:
        print("a movie called \(movie.name), dir. \(movie.director)")
    case let stringConverter as (String) -> String:
        print(stringConverter("Michael"))
    default:
        print("something else")
    }
}

// zero as an Int
// zero as a Double
// an integer value of 42
// a positive double value of 3.14159
// a string value of "hello"
// an (x, y) point at 3.0, 5.0
// a movie called Ghostbusters, dir. Ivan Reitman
// Hello, Michael
```

<!--
  - test: `typeCasting`

  ```swifttest
  -> for thing in things {
        switch thing {
           case 0 as Int:
              print("zero as an Int")
           case 0 as Double:
              print("zero as a Double")
           case let someInt as Int:
              print("an integer value of \(someInt)")
           case let someDouble as Double where someDouble > 0:
              print("a positive double value of \(someDouble)")
           case is Double:
              print("some other double value that I don't want to print")
           case let someString as String:
              print("a string value of \"\(someString)\"")
           case let (x, y) as (Double, Double):
              print("an (x, y) point at \(x), \(y)")
           case let movie as Movie:
              print("a movie called \(movie.name), dir. \(movie.director)")
           case let stringConverter as (String) -> String:
              print(stringConverter("Michael"))
           default:
              print("something else")
        }
     }

  </ zero as an Int
  </ zero as a Double
  </ an integer value of 42
  </ a positive double value of 3.14159
  </ a string value of "hello"
  </ an (x, y) point at 3.0, 5.0
  </ a movie called Ghostbusters, dir. Ivan Reitman
  </ Hello, Michael
  ```
-->

> Nota: O tipo `Any` representa valores de qualquer tipo, incluindo tipos optional.
> O Swift mostra um aviso se você usar um valor optional
> onde um valor do tipo `Any` é esperado.
> Se você realmente precisar usar um valor optional como um valor `Any`,
> pode usar o operador `as` para converter explicitamente o optional para `Any`,
> como mostrado abaixo.
>
> ```swift
> let optionalNumber: Int? = 3
> things.append(optionalNumber)        // Warning
> things.append(optionalNumber as Any) // No warning
> ```

<!--
  - test: `typeCasting-err`

  ```swifttest
  -> let optionalNumber: Int? = 3
  -> things.append(optionalNumber)        // Warning
  !$ warning: expression implicitly coerced from 'Int?' to 'Any'
  !! things.append(optionalNumber)        // Warning
  !!               ^~~~~~~~~~~~~~
  !$ note: provide a default value to avoid this warning
  !! things.append(optionalNumber)        // Warning
  !!               ^~~~~~~~~~~~~~
  !!                              ?? <#default value#>
  !$ note: force-unwrap the value to avoid this warning
  !! things.append(optionalNumber)        // Warning
  !!               ^~~~~~~~~~~~~~
  !!                              !
  !$ note: explicitly cast to 'Any' with 'as Any' to silence this warning
  !! things.append(optionalNumber)        // Warning
  !!               ^~~~~~~~~~~~~~
  !!                              as Any
  -> things.append(optionalNumber as Any) // No warning
  ```
-->

<!--
  Rejected examples to illustrate AnyObject:

  Array of delegates which may conform to one or more of the class's delegate protocols.

  ```
  protocol MovieDelegate {
      func willPlay(movie: Movie)
  }

  class Library {
      var delegates = [AnyObject]
      ...
  }

  for delegate in delegates {
      guard let delegate = delegate as MovieDelegate else { continue }
      delegate.willPlay(movie: m)
  }
  ```

  A userData object for associating some opaque piece of data or state with an API call.

  ```
  class C {
      // Not userInfo -- that's usually a Dictionary
      let userData: AnyObject?  // In Cocoa APIs, userData is a void*
  }
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
