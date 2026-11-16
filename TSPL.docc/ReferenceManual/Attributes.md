# Atributos

Adiciona informações a declarações e tipos.

Existem dois tipos de atributos no Swift:
os que se aplicam a declarações e os que se aplicam a tipos.
Um atributo fornece informação adicional sobre a declaração ou o tipo.
Por exemplo,
o atributo `discardableResult` numa declaração de função indica que,
embora a função retorne um valor,
o compilador não deve gerar um aviso se o valor de retorno não for usado.

Você especifica um atributo escrevendo o símbolo `@` seguido do nome do atributo
e de quaisquer argumentos que ele aceite:

```swift
@<#attribute name#>
@<#attribute name#>(<#attribute arguments#>)
```

Alguns atributos de declaração aceitam argumentos
que especificam mais informações sobre o atributo
e sobre como ele se aplica a uma declaração específica.
Esses *argumentos do atributo* ficam entre parênteses,
e o formato deles é definido pelo atributo a que pertencem.

Macros anexadas e property wrappers também usam a sintaxe de atributos.
Para saber como as macros são expandidas,
veja <doc:Expressions#Macro-Expansion-Expression>.
Para informações sobre property wrappers,
veja <doc:Attributes#propertyWrapper>.

## Atributos de declaração

Você pode aplicar um atributo de declaração apenas a declarações.

### attached

Aplique o atributo `attached` a uma declaração de macro.
Os argumentos desse atributo indicam o papel da macro.
Para uma macro que tem vários papéis,
aplique o atributo `attached` várias vezes, uma para cada papel.

<!-- TODO:
If there's a stable URL we can use, make the macro protocols below links.
-->

O primeiro argumento desse atributo
indica o papel da macro:

- term Macros de par:
  Escreva `peer` como primeiro argumento desse atributo.
  O tipo que implementa a macro conforma com o protocolo `PeerMacro`.
  Essas macros produzem declarações novas
  no mesmo escopo da declaração
  à qual a macro está anexada.
  Por exemplo,
  aplicar uma macro de par a um método de uma struct
  pode definir métodos e propriedades adicionais nessa struct.

- term Macros de membro:
  Escreva `member` como primeiro argumento desse atributo.
  O tipo que implementa a macro conforma com o protocolo `MemberMacro`.
  Essas macros produzem declarações novas
  que são membros do tipo ou da extension
  à qual a macro está anexada.
  Por exemplo,
  aplicar uma macro de membro a uma declaração de struct
  pode definir métodos e propriedades adicionais nessa struct.

- term Atributo de membro:
  Escreva `memberAttribute` como primeiro argumento desse atributo.
  O tipo que implementa a macro conforma com o protocolo `MemberAttributeMacro`.
  Essas macros adicionam atributos aos membros do tipo ou da extension
  à qual a macro está anexada.

- term Macros de acessor:
  Escreva `accessor` como primeiro argumento desse atributo.
  O tipo que implementa a macro conforma com o protocolo `AccessorMacro`.
  Essas macros adicionam acessores à propriedade armazenada à qual estão anexadas,
  transformando-a em uma propriedade computada.

- term Macros de extension:
  Escreva `extension` como primeiro argumento desse atributo.
  O tipo que implementa a macro conforma com o protocolo `ExtensionMacro`.
  Essas macros podem adicionar conformidade a protocolos,
  uma cláusula `where`,
  e declarações novas que são membros do tipo ao qual a macro está anexada.
  Se a macro adicionar conformidades a protocolos,
  inclua o argumento `conformances:` e especifique esses protocolos.
  A lista de conformidades contém nomes de protocolos,
  aliases de tipo que se referem a itens da lista de conformidades,
  ou composições de protocolos de itens da lista de conformidades.
  Uma macro de extension em um tipo aninhado
  se expande para uma extension no nível superior desse arquivo.
  Você não pode escrever uma macro de extension
  em uma extension, em um alias de tipo ou em um tipo aninhado dentro de uma função,
  nem usar uma macro de extension para adicionar uma extension que tenha uma macro de par.

- term Macros de corpo:
  Escreva `body` como primeiro argumento desse atributo.
  O tipo que implementa a macro conforma com o protocolo `BodyMacro`.
  Essas macros podem gerar, modificar ou substituir
  o corpo da função ou do acessor ao qual estão anexadas.
  Você pode escrever no máximo uma macro de corpo em cada função.
  Se o corpo original da função for fornecido,
  ele precisa estar sintaticamente correto,
  mas não é verificado quanto a tipos até depois que a macro é expandida.

Os papéis de macro de par e de membro exigem um argumento `names:`,
que lista os nomes dos símbolos que a macro gera.
O papel de macro de acessor exige um argumento `names:` se a
macro gerar um observador de propriedade `willSet` ou `didSet`. Uma
macro de acessor que gera observadores de propriedade não pode adicionar
outros acessores, porque observadores só se aplicam a propriedades armazenadas.
O papel de macro de extension também exige um argumento `names:`
se a macro adicionar declarações dentro da extension.
Quando a declaração de uma macro inclui o argumento `names:`,
a implementação da macro deve gerar
apenas símbolos com nomes que correspondam a essa lista.
Dito isso,
uma macro não precisa gerar um símbolo para cada nome listado.
O valor desse argumento é uma lista de um ou mais dos seguintes itens:

- `named(<#name#>)`
  em que *name* é esse nome fixo do símbolo,
  para um nome que é conhecido com antecedência.

- `overloaded`
  para um nome que é igual ao de um símbolo já existente.

- `prefixed(<#prefix#>)`
  em que *prefix* é colocado antes do nome do símbolo,
  para um nome que começa com uma string fixa.

- `suffixed(<#suffix#>)`
  em que *suffix* é colocado depois do nome do símbolo,
  para um nome que termina com uma string fixa.

- `arbitrary`
  para um nome que só pode ser determinado durante a expansão da macro.

Como caso especial,
você pode escrever `prefixed($)`
para uma macro que se comporta de forma semelhante a um property wrapper.
<!--
TODO TR: Is there any more detail about this case?
-->

### available

Aplique este atributo para indicar o ciclo de vida de uma declaração
em relação a certas versões da linguagem Swift
ou a certas plataformas e versões de sistema operacional.

O atributo `available` sempre aparece
com uma lista de dois ou mais argumentos de atributo separados por vírgula.
Esses argumentos começam com um dos seguintes nomes de plataforma ou de linguagem:

- `iOS`
- `iOSApplicationExtension`
- `macOS`
- `macOSApplicationExtension`
- `macCatalyst`
- `macCatalystApplicationExtension`
- `watchOS`
- `watchOSApplicationExtension`
- `tvOS`
- `tvOSApplicationExtension`
- `visionOS`
- `visionOSApplicationExtension`
- `swift`

<!--
  If you need to add a new platform to this list,
  you probably need to update platform-name in the grammar too.
-->

<!--
  For the list in source, see include/swift/AST/PlatformKinds.def
-->

Você também pode usar um asterisco (`*`) para indicar a
disponibilidade da declaração em todos os nomes de plataforma listados acima.
Um atributo `available`
que especifica a disponibilidade usando um número de versão do Swift
não pode usar o asterisco.

Os demais argumentos podem aparecer em qualquer ordem
e especificam informações adicionais sobre o ciclo de vida da declaração,
incluindo marcos importantes.

- O argumento `unavailable` indica que a declaração
  não está disponível na plataforma especificada.
  Esse argumento não pode ser usado ao especificar a disponibilidade por versão do Swift.
- O argumento `introduced` indica a primeira versão
  da plataforma ou da linguagem especificada em que a declaração foi introduzida.
  Ele tem a seguinte forma:

  ```swift
  introduced: <#version number#>
  ```
  O *número de versão* é formado por um a três inteiros positivos,
  separados por pontos.
- O argumento `deprecated` indica a primeira versão
  da plataforma ou da linguagem especificada em que a declaração foi marcada como obsoleta (deprecated).
  Ele tem a seguinte forma:

  ```swift
  deprecated: <#version number#>
  ```
  O *número de versão*, que é opcional, é formado por um a três inteiros positivos,
  separados por pontos.
  Omitir o número de versão indica que a declaração foi marcada como obsoleta (deprecated) no momento,
  sem informar quando isso aconteceu.
  Se você omitir o número de versão, omita também os dois-pontos (`:`).
- O argumento `obsoleted` indica a primeira versão
  da plataforma ou da linguagem especificada em que a declaração deixou de existir (obsoleted).
  Quando uma declaração deixa de existir (obsoleted),
  ela é removida da plataforma ou da linguagem especificada e não pode mais ser usada.
  Ele tem a seguinte forma:

  ```swift
  obsoleted: <#version number#>
  ```
  O *número de versão* é formado por um a três inteiros positivos, separados por pontos.

- O argumento `noasync` indica que
  o símbolo declarado não pode ser usado diretamente
  em um contexto assíncrono.

  Como a concorrência do Swift pode retomar em outra thread
  depois de um possível ponto de suspensão,
  usar elementos como armazenamento local de thread, locks, mutexes ou semáforos
  através de pontos de suspensão pode levar a resultados incorretos.

  Para evitar esse problema,
  adicione um atributo `@available(*, noasync)` à declaração do símbolo:

  ```swift
  extension pthread_mutex_t {

    @available(*, noasync)
    mutating func lock() {
        pthread_mutex_lock(&self)
    }

    @available(*, noasync)
    mutating func unlock() {
        pthread_mutex_unlock(&self)
    }
  }
  ```

  Esse atributo gera um erro de compilação
  quando alguém usa o símbolo em um contexto assíncrono.
  Você também pode usar o argumento `message` para fornecer informações adicionais
  sobre o símbolo.

  ```swift
  @available(*, noasync, message: "Migrate locks to Swift concurrency.")
  mutating func lock() {
    pthread_mutex_lock(&self)
  }
  ```

  Se você puder garantir que seu código
  usa um símbolo potencialmente inseguro de forma segura,
  pode envolvê-lo em uma função síncrona e chamar essa função
  a partir de um contexto assíncrono.

  ```swift

  // Provide a synchronous wrapper around methods with a noasync declaration.
  extension pthread_mutex_t {
    mutating func withLock(_ operation: () -> ()) {
      self.lock()
      operation()
      self.unlock()
    }
  }

  func downloadAndStore(key: Int,
                      dataStore: MyKeyedStorage,
                      dataLock: inout pthread_mutex_t) async {
    // Safely call the wrapper in an asynchronous context.
    dataLock.withLock {
      dataStore[key] = downloadContent()
    }
  }
  ```

  Você pode usar o argumento `noasync` na maioria das declarações;
  no entanto, não pode usá-lo ao declarar desinicializadores.
  O Swift precisa conseguir chamar os desinicializadores de uma classe a partir de qualquer contexto,
  tanto síncrono quanto assíncrono.

- O argumento `message` fornece uma mensagem de texto que o compilador exibe
  ao emitir um aviso ou um erro sobre o uso
  de uma declaração marcada como `deprecated`, `obsoleted` ou `noasync`.
  Ele tem a seguinte forma:

  ```swift
  message: <#message#>
  ```
  A *mensagem* é um literal de string.
- O argumento `renamed` fornece uma mensagem de texto
  que indica o novo nome de uma declaração que foi renomeada.
  O compilador exibe o novo nome
  ao emitir um erro sobre o uso de uma declaração renomeada.
  Ele tem a seguinte forma:

  ```swift
  renamed: <#new name#>
  ```
  O *novo nome* é um literal de string.

  Você pode aplicar o atributo `available`
  com os argumentos `renamed` e `unavailable`
  a uma declaração de alias de tipo, como mostrado abaixo,
  para indicar que o nome de uma declaração mudou
  entre versões de um framework ou de uma biblioteca.
  Essa combinação resulta em um erro de compilação
  informando que a declaração foi renomeada.

  ```swift
  // First release
  protocol MyProtocol {
      // protocol definition
  }
  ```

  <!--
    - test: `renamed1`

    ```swifttest
    -> // First release
    -> protocol MyProtocol {
           // protocol definition
       }
    ```
  -->

  ```swift
  // Subsequent release renames MyProtocol
  protocol MyRenamedProtocol {
      // protocol definition
  }

  @available(*, unavailable, renamed: "MyRenamedProtocol")
  typealias MyProtocol = MyRenamedProtocol
  ```

  <!--
    - test: `renamed2`

    ```swifttest
    -> // Subsequent release renames MyProtocol
    -> protocol MyRenamedProtocol {
           // protocol definition
       }

    -> @available(*, unavailable, renamed: "MyRenamedProtocol")
       typealias MyProtocol = MyRenamedProtocol
    ```
  -->

Você pode aplicar vários atributos `available` a uma única declaração
para especificar a disponibilidade dela em plataformas diferentes
e em versões diferentes do Swift.
A declaração à qual o atributo `available` se aplica
é ignorada se o atributo especificar
uma plataforma ou uma versão da linguagem que não corresponde ao destino atual.
Se você usar vários atributos `available`,
a disponibilidade efetiva é a combinação
das disponibilidades da plataforma e do Swift.

<!--
  - test: `multipleAvailableAttributes`

  ```swifttest
  -> @available(iOS 9, *)
  -> @available(macOS 10.9, *)
  -> func foo() { }
  -> foo()
  ```
-->

Se um atributo `available` especificar apenas o argumento `introduced`
além de um nome de plataforma ou de linguagem,
você pode usar a seguinte sintaxe abreviada:

```swift
@available(<#platform name#> <#version number#>, *)
@available(swift <#version number#>)
```

A sintaxe abreviada dos atributos `available`
expressa de forma concisa a disponibilidade em várias plataformas.
Embora as duas formas sejam funcionalmente equivalentes,
a forma abreviada é preferida sempre que possível.

```swift
@available(iOS 10.0, macOS 10.12, *)
class MyClass {
    // class definition
}
```

<!--
  - test: `availableShorthand`

  ```swifttest
  -> @available(iOS 10.0, macOS 10.12, *)
  -> class MyClass {
         // class definition
     }
  ```
-->

Um atributo `available`
que especifica a disponibilidade usando um número de versão do Swift
não pode, além disso, especificar a disponibilidade de plataforma da declaração.
Em vez disso, use atributos `available` separados para especificar a
disponibilidade por versão do Swift e uma ou mais disponibilidades de plataforma.

```swift
@available(swift 3.0.2)
@available(macOS 10.12, *)
struct MyStruct {
    // struct definition
}
```

<!--
  - test: `availableMultipleAvailabilities`

  ```swifttest
  -> @available(swift 3.0.2)
  -> @available(macOS 10.12, *)
  -> struct MyStruct {
         // struct definition
     }
  ```
-->

### backDeployed

Aplique este atributo a uma função, método, subscript ou propriedade computada
para incluir uma cópia da implementação do símbolo
nos programas que chamam ou acessam o símbolo.
Você usa esse atributo para anotar símbolos que são distribuídos como parte de uma plataforma,
como as APIs incluídas com um sistema operacional.
Esse atributo marca símbolos que podem ser disponibilizados retroativamente
ao incluir uma cópia da implementação deles nos programas que os acessam.
Copiar a implementação também é conhecido como *emitir para o cliente*.

Esse atributo recebe um argumento `before:`,
que especifica a primeira versão das plataformas que fornecem esse símbolo.
Essas versões de plataforma têm o mesmo significado
que a versão de plataforma que você especifica para o atributo `available`.
Diferentemente do atributo `available`,
a lista não pode conter um asterisco (`*`) para se referir a todas as versões.
Por exemplo, considere o seguinte código:

```swift
@available(iOS 16, *)
@backDeployed(before: iOS 17)
func someFunction() { /* ... */ }
```

No exemplo acima,
o SDK do iOS fornece `someFunction()` a partir do iOS 17.
Além disso,
o SDK disponibiliza `someFunction()` no iOS 16 usando back deployment.

Ao compilar código que chama essa função,
o Swift insere uma camada de indireção que encontra a implementação da função.
Se o código for executado usando uma versão do SDK que inclui essa função,
a implementação do SDK é usada.
Caso contrário, a cópia incluída no chamador é usada.
No exemplo acima,
chamar `someFunction()` usa a implementação do SDK
quando executado no iOS 17 ou posterior,
e, quando executado no iOS 16,
usa a cópia de `someFunction()` que está incluída no chamador.

> Nota:
> Quando a versão mínima de implantação do chamador
> é igual ou maior que
> a primeira versão do SDK que inclui o símbolo,
> o compilador pode eliminar a verificação em tempo de execução
> e chamar a implementação do SDK diretamente.
> Nesse caso,
> se você acessar o símbolo com back deployment diretamente,
> o compilador também pode omitir
> a cópia da implementação do símbolo do cliente.

<!--
Stripping out the copy emitted into the client
depends on a chain of optimizations that must all take place --
inlining the thunk,
constant-folding the availability check,
and stripping the emitted copy as dead code --
and the details could change over time,
so we don't guarantee in docs that it always happens.
-->

Funções, métodos, subscripts e propriedades computadas
que atendem aos critérios a seguir podem receber back deployment:

- A declaração é `public` ou `@usableFromInline`.
- Para métodos de instância de classe e métodos de tipo de classe,
  o método está marcado com `final` e não está marcado com `@objc`.
- A implementação satisfaz os requisitos de uma função inlinable,
  descritos em <doc:Attributes#inlinable>.

### c

Aplique este atributo a qualquer declaração que possa ser representada em C,
como funções globais
e enums não genéricos (restritos a tipos de raw value inteiros).
O atributo `c` informa ao compilador
que a declaração está disponível para uso em código C.

Aplicar o atributo `c` a um enum
expõe cada caso do enum ao código C
como a concatenação do nome do enum com o nome do caso.
A primeira letra do nome do caso fica em maiúscula.
Por exemplo, um caso chamado `venus` em um enum `Planet` do Swift
é exposto ao código C como um caso chamado `PlanetVenus`.

O atributo `c` aceita opcionalmente um único argumento de atributo,
que consiste em um identificador.
O identificador especifica o nome que será exposto ao C
para a entidade à qual o atributo `c` se aplica.

### discardableResult

Aplique este atributo a uma declaração de função ou de método
para suprimir o aviso do compilador
quando a função ou o método, que retorna um valor,
é chamado sem usar o resultado.

### dynamicCallable

Aplique este atributo a uma classe, struct, enum ou protocolo
para tratar instâncias do tipo como funções que podem ser chamadas.
O tipo precisa implementar um método `dynamicallyCall(withArguments:)`,
um método `dynamicallyCall(withKeywordArguments:)`,
ou os dois.

Você pode chamar uma instância de um tipo chamável dinamicamente
como se fosse uma função que recebe qualquer número de argumentos.

```swift
@dynamicCallable
struct TelephoneExchange {
    func dynamicallyCall(withArguments phoneNumber: [Int]) {
        if phoneNumber == [4, 1, 1] {
            print("Get Swift help on forums.swift.org")
        } else {
            print("Unrecognized number")
        }
    }
}

let dial = TelephoneExchange()

// Use a dynamic method call.
dial(4, 1, 1)
// Prints "Get Swift help on forums.swift.org".

dial(8, 6, 7, 5, 3, 0, 9)
// Prints "Unrecognized number".

// Call the underlying method directly.
dial.dynamicallyCall(withArguments: [4, 1, 1])
```

<!--
  - test: `dynamicCallable`

  ```swifttest
  -> @dynamicCallable
  -> struct TelephoneExchange {
         func dynamicallyCall(withArguments phoneNumber: [Int]) {
             if phoneNumber == [4, 1, 1] {
                 print("Get Swift help on forums.swift.org")
             } else {
                 print("Unrecognized number")
             }
         }
     }

  -> let dial = TelephoneExchange()

  -> // Use a dynamic method call.
  -> dial(4, 1, 1)
  <- Get Swift help on forums.swift.org

  -> dial(8, 6, 7, 5, 3, 0, 9)
  <- Unrecognized number

  -> // Call the underlying method directly.
  -> dial.dynamicallyCall(withArguments: [4, 1, 1])
  << Get Swift help on forums.swift.org
  ```
-->

A declaração do método `dynamicallyCall(withArguments:)`
precisa ter um único parâmetro que esteja em conformidade com o protocolo
[`ExpressibleByArrayLiteral`](https://developer.apple.com/documentation/swift/expressiblebyarrayliteral)
--- como `[Int]` no exemplo acima.
O tipo de retorno pode ser qualquer tipo.

Você pode incluir rótulos em uma chamada de método dinâmica
se implementar o método `dynamicallyCall(withKeywordArguments:)`.

```swift
@dynamicCallable
struct Repeater {
    func dynamicallyCall(withKeywordArguments pairs: KeyValuePairs<String, Int>) -> String {
        return pairs
            .map { label, count in
                repeatElement(label, count: count).joined(separator: " ")
            }
            .joined(separator: "\n")
    }
}

let repeatLabels = Repeater()
print(repeatLabels(a: 1, b: 2, c: 3, b: 2, a: 1))
// a
// b b
// c c c
// b b
// a
```

<!--
  - test: `dynamicCallable`

  ```swifttest
  -> @dynamicCallable
     struct Repeater {
         func dynamicallyCall(withKeywordArguments pairs: KeyValuePairs<String, Int>) -> String {
             return pairs
                 .map { label, count in
                     repeatElement(label, count: count).joined(separator: " ")
                 }
                 .joined(separator: "\n")
         }
     }

  -> let repeatLabels = Repeater()
  -> print(repeatLabels(a: 1, b: 2, c: 3, b: 2, a: 1))
  </ a
  </ b b
  </ c c c
  </ b b
  </ a
  ```
-->

A declaração do método `dynamicallyCall(withKeywordArguments:)`
precisa ter um único parâmetro que esteja em conformidade com o protocolo
[`ExpressibleByDictionaryLiteral`](https://developer.apple.com/documentation/swift/expressiblebydictionaryliteral),
e o tipo de retorno pode ser qualquer tipo.
O [`Key`](https://developer.apple.com/documentation/swift/expressiblebydictionaryliteral/key) do parâmetro
precisa ser
[`ExpressibleByStringLiteral`](https://developer.apple.com/documentation/swift/expressiblebystringliteral).
O exemplo anterior usa [`KeyValuePairs`](https://developer.apple.com/documentation/swift/keyvaluepairs)
como tipo do parâmetro
para que quem chama possa incluir rótulos de parâmetro duplicados ---
`a` e `b` aparecem várias vezes na chamada a `repeat`.

Se você implementar os dois métodos `dynamicallyCall`,
`dynamicallyCall(withKeywordArguments:)` é chamado
quando a chamada do método inclui argumentos nomeados.
Em todos os outros casos, `dynamicallyCall(withArguments:)` é chamado.

Você só pode chamar uma instância chamável dinamicamente
com argumentos e um valor de retorno que correspondam aos tipos especificados
em uma das implementações de método `dynamicallyCall`.
A chamada do exemplo a seguir não compila porque
não existe uma implementação de `dynamicallyCall(withArguments:)`
que receba `KeyValuePairs<String, String>`.

```swift
repeatLabels(a: "four") // Error
```

<!--
  - test: `dynamicCallable-err`

  ```swifttest
  >> @dynamicCallable
  >> struct Repeater {
  >>     func dynamicallyCall(withKeywordArguments pairs: KeyValuePairs<String, Int>) -> String {
  >>         return pairs
  >>             .map { label, count in
  >>                 repeatElement(label, count: count).joined(separator: " ")
  >>             }
  >>             .joined(separator: "\n")
  >>     }
  >> }
  >> let repeatLabels = Repeater()
  -> repeatLabels(a: "four") // Error
  !$ error: cannot convert value of type 'String' to expected argument type 'Int'
  !! repeatLabels(a: "four") // Error
  !! ^
  ```
-->

### dynamicMemberLookup

Aplique este atributo a uma classe, struct, enum ou protocolo
para permitir que os membros sejam buscados pelo nome em tempo de execução.
O tipo precisa implementar um subscript `subscript(dynamicMember:)`.

Em uma expressão de membro explícita,
se não houver uma declaração correspondente para o membro nomeado,
a expressão é interpretada como uma chamada ao
subscript `subscript(dynamicMember:)` do tipo,
passando as informações sobre o membro como argumento.
O subscript pode aceitar um parâmetro que seja um key path ou um nome de membro;
se você implementar os dois subscripts,
é usado o subscript que recebe um argumento de key path.

Uma implementação de `subscript(dynamicMember:)`
pode aceitar key paths usando um argumento do tipo
[`KeyPath`](https://developer.apple.com/documentation/swift/keypath),
[`WritableKeyPath`](https://developer.apple.com/documentation/swift/writablekeypath),
ou [`ReferenceWritableKeyPath`](https://developer.apple.com/documentation/swift/referencewritablekeypath).
Ele pode aceitar nomes de membros usando um argumento de um tipo que esteja em conformidade com o protocolo
[`ExpressibleByStringLiteral`](https://developer.apple.com/documentation/swift/expressiblebystringliteral)
--- na maioria dos casos, `String`.
O tipo de retorno do subscript pode ser qualquer tipo.

A busca dinâmica de membros pelo nome
pode ser usada para criar um tipo wrapper em torno de dados
que não podem ser verificados quanto a tipos em tempo de compilação,
como ao trazer dados de outras linguagens para o Swift.
Por exemplo:

```swift
@dynamicMemberLookup
struct DynamicStruct {
    let dictionary = ["someDynamicMember": 325,
                      "someOtherMember": 787]
    subscript(dynamicMember member: String) -> Int {
        return dictionary[member] ?? 1054
    }
}
let s = DynamicStruct()

// Use dynamic member lookup.
let dynamic = s.someDynamicMember
print(dynamic)
// Prints "325".

// Call the underlying subscript directly.
let equivalent = s[dynamicMember: "someDynamicMember"]
print(dynamic == equivalent)
// Prints "true".
```

<!--
  - test: `dynamicMemberLookup`

  ```swifttest
  -> @dynamicMemberLookup
  -> struct DynamicStruct {
         let dictionary = ["someDynamicMember": 325,
                           "someOtherMember": 787]
         subscript(dynamicMember member: String) -> Int {
             return dictionary[member] ?? 1054
         }
     }
  -> let s = DynamicStruct()

  // Use dynamic member lookup.
  -> let dynamic = s.someDynamicMember
  -> print(dynamic)
  <- 325

  // Call the underlying subscript directly.
  -> let equivalent = s[dynamicMember: "someDynamicMember"]
  -> print(dynamic == equivalent)
  <- true
  ```
-->

A busca dinâmica de membros por key path
pode ser usada para implementar um tipo wrapper
de um jeito que permite a verificação de tipos em tempo de compilação.
Por exemplo:

```swift
struct Point { var x, y: Int }

@dynamicMemberLookup
struct PassthroughWrapper<Value> {
    var value: Value
    subscript<T>(dynamicMember member: KeyPath<Value, T>) -> T {
        get { return value[keyPath: member] }
    }
}

let point = Point(x: 381, y: 431)
let wrapper = PassthroughWrapper(value: point)
print(wrapper.x)
```

<!--
  - test: `dynamicMemberLookup`

  ```swifttest
  -> struct Point { var x, y: Int }

  -> @dynamicMemberLookup
     struct PassthroughWrapper<Value> {
         var value: Value
         subscript<T>(dynamicMember member: KeyPath<Value, T>) -> T {
             get { return value[keyPath: member] }
         }
     }

  -> let point = Point(x: 381, y: 431)
  -> let wrapper = PassthroughWrapper(value: point)
  -> print(wrapper.x)
  << 381
  ```
-->

### export

Aplique este atributo a uma declaração de função ou de método
para controlar como a definição dela é exportada para os módulos clientes.
Inclua um dos argumentos a seguir,
indicando qual aspecto da declaração exportar:

- O argumento `interface` especifica que
  apenas a interface é exportada para os clientes,
  na forma de um símbolo chamável.
  A definição (corpo da função) não fica disponível para os clientes
  para inlining, otimização ou qualquer outra finalidade.
  Use esse argumento para ocultar a implementação dos clientes.

- O argumento `implementation` especifica que
  apenas a definição (corpo da função) é exportada para os clientes.
  Não há um símbolo para essa função emitido no binário,
  e os clientes são responsáveis por emitir uma cópia da definição
  sempre que ela for necessária.
  Use esse argumento para introduzir uma nova função ou método
  sem afetar a Application Binary Interface (ABI).

### freestanding

Aplique o atributo `freestanding`
à declaração de uma macro freestanding.

<!--

For the future, when other roles are supported:

The arguments to this attribute indicate the macro's roles:

- `expression`
  A macro that produces an expression

- `declaration`
  A macro that produces a declaration

Or are those supported today?
I see #error and #warning as @freestanding(declaration)
in the stdlib already:

https://github.com/swiftlang/swift/blob/main/stdlib/public/core/Macros.swift#L102
-->

### frozen

Aplique este atributo a uma declaração de struct ou de enum
para restringir os tipos de alteração que você pode fazer no tipo.
Esse atributo só é permitido ao compilar no modo de evolução de biblioteca.
Versões futuras da biblioteca não podem alterar a declaração
adicionando, removendo ou reordenando
os casos de um enum
ou as propriedades de instância armazenadas de uma struct.
Essas alterações são permitidas em tipos não congelados,
mas quebram a compatibilidade de ABI para tipos congelados.

<!--
  - test: `can-use-frozen-without-evolution`

  ```swifttest
  >> @frozen public enum E { case x, y }
  >> @frozen public struct S { var a: Int = 10 }
  ```
-->

<!--
  <rdar://problem/54041692> Using @frozen without Library Evolution has inconsistent error messages [SE-0260]
-->

<!--
  - test: `frozen-is-fine-with-evolution`

  ```swifttest
  >> @frozen public enum E { case x, y }
  >> @frozen public struct S { var a: Int = 10 }
  ```
-->

No modo de evolução de biblioteca,
o código que interage com membros de structs e enums não congelados
é compilado de um jeito que permite que ele continue funcionando sem recompilação,
mesmo que uma versão futura da biblioteca
adicione, remova ou reordene alguns membros desse tipo.
O compilador torna isso possível com técnicas como
buscar informações em tempo de execução
e adicionar uma camada de indireção.
Marcar uma struct ou um enum como congelado
abre mão dessa flexibilidade para ganhar desempenho:
versões futuras da biblioteca podem fazer apenas alterações limitadas no tipo,
mas o compilador pode fazer otimizações adicionais
no código que interage com os membros do tipo.

Tipos congelados,
os tipos das propriedades armazenadas de structs congeladas
e os associated values aos casos de enums congelados
precisam ser públicos ou estar marcados com o atributo `usableFromInline`.
As propriedades de uma struct congelada não podem ter observadores de propriedade,
e as expressões que fornecem o valor inicial das propriedades de instância armazenadas
precisam seguir as mesmas restrições das funções inlinable,
como discutido em <doc:Attributes#inlinable>.

<!--
  - test: `frozen-struct-prop-init-cant-refer-to-private-type`

  ```swifttest
  >> public protocol P { }
  >> private struct PrivateStruct: P { }
  >>         public struct S1 { var fine: P = PrivateStruct() }
  >> @frozen public struct S2 { var nope: P = PrivateStruct() }
  !$ error: struct 'PrivateStruct' is private and cannot be referenced from a property initializer in a '@frozen' type
  !! @frozen public struct S2 { var nope: P = PrivateStruct() }
  !!                                          ^
  !$ note: struct 'PrivateStruct' is not '@usableFromInline' or public
  !! private struct PrivateStruct: P { }
  !!                ^
  !$ error: initializer 'init()' is private and cannot be referenced from a property initializer in a '@frozen' type
  !! @frozen public struct S2 { var nope: P = PrivateStruct() }
  !! ^
  !$ note: initializer 'init()' is not '@usableFromInline' or public
  !! private struct PrivateStruct: P { }
  !! ^
  ```
-->

Para ativar o modo de evolução de biblioteca na linha de comando,
passe a opção `-enable-library-evolution` para o compilador do Swift.
Para ativá-lo no Xcode,
defina a configuração de build "Build Libraries for Distribution"
(`BUILD_LIBRARY_FOR_DISTRIBUTION`) como Yes,
conforme descrito em [Xcode Help](https://help.apple.com/xcode/mac/current/#/dev04b3a04ba).

<!--
  This is the first time we're talking about a specific compiler flag/option.
  In the long term, the discussion of library evolution mode
  will need to move to a new chapter in the guide
  that also talks about things like @available and ABI.
  See <rdar://problem/51929017> TSPL: Give guidance to library authors about @available @frozen and friends
-->

Uma instrução switch sobre um enum congelado não exige um caso `default`,
como discutido em <doc:Statements#Switching-Over-Future-Enumeration-Cases>.
Incluir um caso `default` ou `@unknown default`
ao fazer `switch` sobre um enum congelado
gera um aviso, porque esse código nunca é executado.

<!--
  - test: `NoUnknownDefaultOverFrozenEnum`

  ```swifttest
  >> public enum E { case x, y }
  >> @frozen public enum F { case x, y }
  ```
-->

<!--
  - test: `NoUnknownDefaultOverFrozenEnum_Test1`

  ```swifttest
  >> import NoUnknownDefaultOverFrozenEnum
  >> func main() {
  >>     let e = NoUnknownDefaultOverFrozenEnum.E.x
  >>     switch e {
  >>         case .x: print(9)
  >>         case .y: print(8)
  >>         @unknown default: print(0)
  >>     }
  >> }
  // Note that there's no warning -- this is fine because E isn't frozen.
  ```
-->

<!--
  - test: `NoUnknownDefaultOverFrozenEnum_Test2`

  ```swifttest
  >> import NoUnknownDefaultOverFrozenEnum
  >> func main() {
  >>     let f = NoUnknownDefaultOverFrozenEnum.F.x
  >>     switch f {
  >>         case .x: print(9)
  >>         case .y: print(8)
  >>         @unknown default: print(0)
  >>     }
  >> }
  // --- Main warning ---
  !! /tmp/sourcefile_0.swift:7:18: warning: case is already handled by previous patterns; consider removing it
  !! @unknown default: print(0)
  !! ~~~~~~~~~^~~~~~~~~~~~~~~~~
  !! /tmp/sourcefile_0.swift:7:9: warning: default will never be executed
  !! @unknown default: print(0)
  !! ^
  // --- Junk/ancillary warnings ---
  !! /tmp/sourcefile_0.swift:4:12: warning: switch condition evaluates to a constant
  !! switch f {
  !! ^
  !! /tmp/sourcefile_0.swift:6:24: note: will never be executed
  !! case .y: print(8)
  !! ^
  ```
-->

### GKInspectable

Aplique este atributo para expor uma propriedade de componente personalizado do GameplayKit
na interface do editor do SpriteKit.
Aplicar este atributo também implica o atributo `objc`.

<!--
  See also <rdar://problem/27287369> Document @GKInspectable attribute
  which we will want to link to, once it's written.
-->

### globalActor

Aplique este atributo a um actor, struct, enum ou classe `final`.
O tipo precisa definir uma propriedade estática chamada `shared`,
que fornece uma instância compartilhada de um actor.

Um global actor generaliza o conceito de isolamento de actor
para estado espalhado por vários lugares do código ---
como vários tipos, arquivos e módulos ---
e torna possível acessar com segurança variáveis globais a partir de código concorrente.
O actor que o global actor fornece
como valor da sua propriedade `shared`
serializa o acesso a todo esse estado.
Você também pode usar um global actor para modelar restrições em código concorrente,
como código que precisa executar sempre na mesma thread.

Global actors implicitamente conformam com o protocolo [`GlobalActor`][].
O main actor é um global actor fornecido pela biblioteca padrão,
como discutido em <doc:Concurrency#The-Main-Actor>.
A maior parte do código pode usar o main actor em vez de definir um novo global actor.

[`GlobalActor`]: https://developer.apple.com/documentation/swift/globalactor

### implementation

Aplique este atributo a uma declaração
que fornece uma implementação em Swift
para uma declaração importada de outra linguagem.

Implementar uma interface em Swift não exige nenhuma mudança
na interface declarada no cabeçalho C ou Objective-C.
Se você já tiver uma interface,
pode usar este atributo
para substituir a implementação dela em outra linguagem
por uma implementação em Swift,
sem alterar o arquivo de cabeçalho.

#### Implementação em Swift de declarações Objective-C

Para declarações definidas em um cabeçalho Objective-C,
aplique os atributos `objc` e `implementation`
a uma extension em Swift que fornece as implementações.
Outros códigos em Swift tratam essas implementações
como se tivessem sido implementadas em Objective-C e importadas para o Swift.
A classe que a extension estende precisa ser importada de Objective-C,
não pode ser uma classe raiz
e não pode usar lightweight generics.
A extension não pode incluir nenhuma conformidade com protocolos.
Todas as declarações dessa extension
são implicitamente marcadas com o atributo `objc`.
Por exemplo,
o cabeçalho Objective-C a seguir declara uma classe com um método:

```objc
NS_HEADER_AUDIT_BEGIN(nullability, sendability)
@interface MyClass
- (void)performSomeAction;
@end
NS_HEADER_AUDIT_END(nullability, sendability)
```

<!-- Omitted the header's conventional blank lines for compactness. -->

Você implementa a classe e o método dela em Swift assim:

```swift
@objc @implementation
extension MyClass {
    func performSomeAction() { ... }
}
```

Um membro da extension que corresponde a uma declaração no arquivo de cabeçalho
é chamado de *implementação de membro*.
Para ser considerado correspondente,
uma implementação de membro precisa atender aos requisitos a seguir:

- Seu seletor e seu nome em Swift são iguais aos da declaração que ela implementa.
  Se necessário, você pode usar o atributo `objc(custom:selector:)` em Swift
  e o atributo `NS_SWIFT_NAME(custom(_:name:))` em Objective-C.
- Seu tipo corresponde ao tipo da declaração que ela implementa.
  Tipos marcados como `_Nonnull` em Objective-C podem ser implementados em Swift
  tanto como não optionals quanto como implicitly unwrapped optionals.
- Seu tratamento de erros (`throws`) corresponde ao da declaração que ela implementa.
- Sua concorrência (`async`) corresponde à da declaração que ela implementa.
  Para um método Objective-C que recebe um completion handler como argumento,
  que é importado para o Swift
  tanto como um método `async` quanto como um método que recebe uma closure,
  você pode escrever uma implementação de membro
  que corresponda a qualquer um dos dois métodos.
  No entanto, você não pode implementar os dois métodos.
- Ela não está marcada com `final` nem com `override`.
- Seu nível de controle de acesso é `open`, `public`, `package` ou `internal`.
- Ela não tem nenhuma outra característica
  que seja incompatível com o membro que ela implementa,
  como o atributo `nonobjc`, o modificador `class` ou a mutabilidade,

Toda implementação de membro na extension
precisa corresponder a um membro declarado no cabeçalho Objective-C,
e todo membro declarado nessa categoria Objective-C
precisa ter uma implementação correspondente em Swift.
Se o cabeçalho Objective-C não especificar uma categoria,
as declarações fazem parte da categoria padrão.
Ao usar este atributo para migrar código Objective-C para o Swift,
você migra uma categoria por vez
ou migra métodos individuais movendo-os entre categorias;
migrar desse jeito não quebra a compatibilidade de código-fonte nem a compatibilidade de ABI.
Para informações sobre categorias em Objective-C,
veja [Personalizando classes existentes][objc-category]
em *Programming with Objective-C*.

[objc-category]: https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/CustomizingExistingClasses/CustomizingExistingClasses.html

<!-- Alternate xrefs:
Cocoa Core Competencies article, summarizes and links to the above
https://developer.apple.com/library/archive/documentation/General/Conceptual/DevPedia-CocoaCore/Category.html

The Objective-C Programming Language, superseded by the above
https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocCategories.html
-->

Além das implementações de membros,
você pode escrever as declarações a seguir na extension,
mas elas não podem corresponder a uma declaração no cabeçalho Objective-C:

- Sobrescritas de membros da superclasse.
  Você marca essas declarações com `override`, como de costume.
- Membros auxiliares com nível de controle de acesso `fileprivate` ou `private`
  que não estejam marcados com `final`.
  Para acessá-los a partir de Objective-C,
  declare-os em um cabeçalho que não seja visível para o compilador do Swift
  ou acesse-os pelo seletor.
- Membros auxiliares com acesso `internal`, `fileprivate` ou `private`,
  que só são acessíveis a partir de outro código em Swift.
  Você marca essas declarações com `final`,
  e elas são implicitamente marcadas com o atributo `nonobjc`.
  Para inicializadores, você aplica o atributo `nonobjc`.
- APIs com acesso `public` ou `package`,
  que só são acessíveis a clientes em Swift.
  Você marca essas declarações com `final`,
  e elas são implicitamente marcadas com o atributo `nonobjc`.
  Para inicializadores, você aplica o atributo `nonobjc`.

A extension pode incluir declarações de propriedades armazenadas e de inicializadores,
o que é uma exceção à regra de que
você não pode declarar propriedades armazenadas ou inicializadores em extensions.

Para especificar uma categoria Objective-C para os membros de uma extension,
escreva o nome dela como argumento do atributo `objc`.
O nome precisa corresponder a uma categoria declarada no arquivo de cabeçalho Objective-C.
Por exemplo, se o cabeçalho contiver o seguinte:

```objc
@interface MyClass (SomeCategory)
- (void)someCategoryMethod;
@end
```

O código em Swift para implementar `someCategoryMethod()` fica assim:

```swift
@objc(SomeCategory) @implementation
extension MyClass {
	func someCategoryMethod() { ... }
}
```

#### Implementação em Swift de declarações C

Para uma declaração definida em um cabeçalho C,
aplique os atributos `c` e `implementation`
a uma declaração em Swift que fornece a implementação.
Outros códigos em Swift tratam essas implementações
como se tivessem sido implementadas em C e importadas para o Swift.
A implementação em Swift
precisa ter o mesmo nome e o mesmo tipo
de uma implementação C importada dessa declaração.
Por exemplo,
o cabeçalho C a seguir declara uma função global:

```c
int myFunction(int value);
```

Você implementa a função em Swift assim:

```swift
@c @implementation
func myFunction(_ value: CInt) -> CInt {
    return value
}
```

### inlinable

Aplique este atributo a uma declaração de função, método, propriedade computada, subscript,
inicializador de conveniência ou desinicializador
para expor a implementação dessa declaração
como parte da interface pública do módulo.
O compilador pode substituir chamadas a um símbolo inlinable
por uma cópia da implementação do símbolo no local da chamada.

Código inlinable
pode interagir com símbolos `open` e `public` declarados em qualquer módulo,
e pode interagir com símbolos `internal`
declarados no mesmo módulo
que estejam marcados com o atributo `usableFromInline`.
Código inlinable não pode interagir com símbolos `private` ou `fileprivate`.

Este atributo não pode ser aplicado
a declarações aninhadas dentro de funções
nem a declarações `fileprivate` ou `private`.
Funções e closures definidas dentro de uma função inlinable
são implicitamente inlinable,
mesmo que não possam ser marcadas com este atributo.

<!--
  - test: `cant-inline-private`

  ```swifttest
  >> @inlinable private func f() { }
  !$ error: '@inlinable' attribute can only be applied to public declarations, but 'f' is private
  !! @inlinable private func f() { }
  !! ^~~~~~~~~~~
  ```
-->

<!--
  - test: `cant-inline-nested`

  ```swifttest
  >> public func outer() {
  >>    @inlinable func f() { }
  >> }
  !$ error: '@inlinable' attribute can only be applied to public declarations, but 'f' is private
  !! @inlinable func f() { }
  !! ^~~~~~~~~~~
  !!-
  ```
-->

<!--
  TODO: When we get resilience, this will actually be a problem.
  Until then, per discussion with [Contributor 6004], there's no (supported) way
  for folks to get into the state where this behavior would be triggered.

  If a project uses a module that includes inlinable functions,
  the inlined copies aren't necessarily updated
  when the module's implementation of the function changes.
  For this reason,
  an inlinable function must be compatible with
  every past version of that function.
  In most cases, this means
  externally visible aspects of their implementation can't be changed.
  For example,
  an inlinable hash function can't change what algorithm is used ---
  inlined copies outside the module would use the old algorithm
  and the noninlined copy would use the new algorithm,
  yielding inconsistent results.
-->

### main

Aplique este atributo a uma declaração de struct, classe ou enum
para indicar que ela contém o ponto de entrada de nível superior do fluxo do programa.
O tipo precisa fornecer uma função de tipo `main`
que não recebe argumentos e retorna `Void`.
Por exemplo:

```swift
@main
struct MyTopLevel {
    static func main() {
        // Top-level code goes here
    }
}
```

<!--
  - test: `atMain`

  ```swifttest
  -> @main
  -> struct MyTopLevel {
  ->     static func main() {
  ->         // Top-level code goes here
  >>         print("Hello")
  ->     }
  -> }
  << Hello
  ```
-->

Outra forma de descrever os requisitos do atributo `main`
é dizer que o tipo em que você escreve esse atributo
precisa satisfazer os mesmos requisitos
dos tipos que conformam com o protocolo hipotético a seguir:

```swift
protocol ProvidesMain {
    static func main() throws
}
```

<!--
  - test: `atMain_ProvidesMain`

  ```swifttest
  -> protocol ProvidesMain {
         static func main() throws
     }
  ```
-->

O código Swift que você compila para criar um executável
pode conter no máximo um ponto de entrada de nível superior,
como discutido em <doc:Declarations#Top-Level-Code>.

<!--
  - test: `no-at-main-in-top-level-code`

  ```swifttest
  // This is the same example as atMain, but without :compile: true.
  >> @main
  >> struct MyTopLevel {
  >>     static func main() {
  >>         print("Hello")
  >>     }
  >> }
  !$ error: 'main' attribute cannot be used in a module that contains top-level code
  !! @main
  !! ^
  !$ note: top-level code defined in this source file
  !! @main
  !! ^
  ```
-->

<!--
  - test: `atMain_library`

  ```swifttest
  -> // In file "library.swift"
  -> open class C {
         public static func main() { print("Hello") }
     }
  ```
-->

<!--
  - test: `atMain_client`

  ```swifttest
  -> import atMain_library
  -> @main class CC: C { }
  ```
-->

### nonobjc

Aplique este atributo a uma declaração de método, propriedade, subscript ou inicializador
para suprimir o atributo `objc` implícito.
O atributo `nonobjc` informa ao compilador
que a declaração deve ficar indisponível em código Objective-C,
mesmo que seja possível representá-la em Objective-C.

Aplicar este atributo a uma extension
tem o mesmo efeito que aplicá-lo a cada membro
dessa extension que não esteja marcado explicitamente com o atributo `objc`.

Você usa o atributo `nonobjc` para resolver a circularidade
de métodos com ponte (bridging) em uma classe marcada com o atributo `objc`,
e para permitir a sobrecarga de métodos e inicializadores
em uma classe marcada com o atributo `objc`.

Um método marcado com o atributo `nonobjc`
não pode sobrescrever um método marcado com o atributo `objc`.
No entanto, um método marcado com o atributo `objc`
pode sobrescrever um método marcado com o atributo `nonobjc`.
Da mesma forma, um método marcado com o atributo `nonobjc`
não pode satisfazer um requisito de protocolo
para um método marcado com o atributo `objc`.

### NSApplicationMain

> Obsoleto:
> Este atributo está obsoleto;
> use o atributo <doc:Attributes#main> no lugar.
> No Swift 6,
> usar este atributo gera um erro de compilação.

Aplique este atributo a uma classe
para indicar que ela é o delegate do app.
Usar este atributo é equivalente a chamar a
função `NSApplicationMain(_:_:)`.

Se você não usar este atributo,
forneça um arquivo `main.swift` com código no nível superior
que chame a função `NSApplicationMain(_:_:)` assim:

```swift
import AppKit
NSApplicationMain(CommandLine.argc, CommandLine.unsafeArgv)
```

<!--
  Above code isn't tested because it hangs the REPL indefinitely,
  which is correct behavior if you call a non-returning function like this.
-->

O código Swift que você compila para criar um executável
pode conter no máximo um ponto de entrada de nível superior,
como discutido em <doc:Declarations#Top-Level-Code>.

### NSCopying

Aplique este atributo a uma propriedade de variável armazenada de uma classe.
Este atributo faz com que o setter da propriedade seja sintetizado com uma *cópia*
do valor da propriedade --- retornada pelo método `copyWithZone(_:)` --- em vez do
próprio valor da propriedade.
O tipo da propriedade precisa conformar com o protocolo `NSCopying`.

O atributo `NSCopying` se comporta de forma parecida com o atributo de propriedade
`copy` do Objective-C.

<!--
  TODO: If and when Dave includes a section about this in the Guide,
  provide a link to the relevant section.
-->

### NSManaged

Aplique este atributo a um método de instância ou a uma propriedade de variável armazenada
de uma classe que herda de `NSManagedObject`
para indicar que o Core Data fornece a implementação dela dinamicamente em tempo de execução,
com base na descrição da entidade associada.
Para uma propriedade marcada com o atributo `NSManaged`,
o Core Data também fornece o armazenamento em tempo de execução.
Aplicar este atributo também implica o atributo `objc`.

### objc

Aplique este atributo a qualquer declaração que possa ser representada em Objective-C ---
por exemplo, funções globais, classes não aninhadas, protocolos,
enums não genéricos (restritos a tipos de raw value inteiros),
propriedades e métodos (incluindo getters e setters) de classes,
protocolos e membros optional de um protocolo,
inicializadores e subscripts.
O atributo `objc` informa ao compilador
que a declaração está disponível para uso em código Objective-C.

Aplicar este atributo a uma extension
tem o mesmo efeito que aplicá-lo a cada membro
dessa extension que não esteja marcado explicitamente com o atributo `nonobjc`.

O compilador adiciona implicitamente o atributo `objc`
às subclasses de qualquer classe definida em Objective-C.
No entanto, a subclasse não pode ser genérica,
nem herdar de nenhuma classe genérica.
Você pode adicionar explicitamente o atributo `objc`
a uma subclasse que atenda a esses critérios,
para especificar o nome dela em Objective-C, como discutido a seguir.
Protocolos marcados com o atributo `objc` não podem herdar
de protocolos que não estejam marcados com esse atributo.

O atributo `objc` também é adicionado implicitamente nos casos a seguir:

- A declaração é uma sobrescrita em uma subclasse,
  e a declaração da superclasse tem o atributo `objc`.
- A declaração satisfaz um requisito
  de um protocolo que tem o atributo `objc`.
- A declaração tem o atributo `IBAction`, `IBSegueAction`, `IBOutlet`,
  `IBDesignable`, `IBInspectable`,
  `NSManaged` ou `GKInspectable`.

Se você aplicar o atributo `objc` a um enum,
cada caso do enum é exposto ao código Objective-C
como a concatenação do nome do enum com o nome do caso.
A primeira letra do nome do caso fica em maiúscula.
Por exemplo, um caso chamado `venus` em um enum `Planet` do Swift
é exposto ao código Objective-C como um caso chamado `PlanetVenus`.

O atributo `objc` aceita opcionalmente um único argumento de atributo,
que consiste em um identificador.
O identificador especifica o nome que será exposto ao Objective-C
para a entidade à qual o atributo `objc` se aplica.
Você pode usar esse argumento para dar nome a
funções globais, classes, enums, casos de enum, protocolos,
métodos, getters, setters e inicializadores.
Você também pode usar esse argumento em uma extension,
para especificar a categoria Objective-C dos membros da extension.
Se você especificar o nome em Objective-C
de uma classe, protocolo ou enum,
inclua um prefixo de três letras no nome,
como descrito em [Convenções](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Conventions/Conventions.html#//apple_ref/doc/uid/TP40011210-CH10-SW1)
em [Programming with Objective-C](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html#//apple_ref/doc/uid/TP40011210).
O exemplo a seguir expõe
o getter da propriedade `enabled` de `ExampleClass`
para o código Objective-C como `isEnabled`,
e não apenas pelo nome da própria propriedade.

```swift
class ExampleClass: NSObject {
    @objc var enabled: Bool {
        @objc(isEnabled) get {
            // Return the appropriate value
        }
    }
}
```

<!--
  - test: `objc-attribute`

  ```swifttest
  >> import Foundation
  -> class ExampleClass: NSObject {
  ->    @objc var enabled: Bool {
  ->       @objc(isEnabled) get {
  ->          // Return the appropriate value
  >>          return true
  ->       }
  ->    }
  -> }
  ```
-->

Para mais informações, veja
[Importando Swift no Objective-C](https://developer.apple.com/documentation/swift/imported_c_and_objective-c_apis/importing_swift_into_objective-c).

> Nota: O argumento do atributo `objc`
> também pode alterar o nome em tempo de execução dessa declaração.
> Você usa o nome em tempo de execução ao chamar funções
> que interagem com o runtime do Objective-C,
> como [`NSClassFromString(_:)`](https://developer.apple.com/documentation/foundation/nsclassfromstring(_:)),
> e ao especificar nomes de classes no arquivo Info.plist de um app.
> Se você especificar um nome passando um argumento,
> esse nome é usado como nome no código Objective-C
> e como nome em tempo de execução.
> Se você omitir o argumento,
> o nome usado no código Objective-C corresponde ao nome no código Swift,
> e o nome em tempo de execução segue a convenção normal do compilador do Swift
> de name mangling.

### objcMembers

Aplique este atributo a uma declaração de classe
para aplicar implicitamente o atributo `objc`
a todos os membros da classe compatíveis com Objective-C,
às suas extensions, às suas subclasses e a todas as extensions das suas subclasses.

A maior parte do código deve usar o atributo `objc`,
para expor apenas as declarações que são necessárias.
Se você precisar expor muitas declarações,
pode agrupá-las em uma extension que tenha o atributo `objc`.
O atributo `objcMembers` é uma conveniência para
bibliotecas que usam muito
os recursos de introspecção do runtime do Objective-C.
Aplicar o atributo `objc` quando ele não é necessário
pode aumentar o tamanho do binário e afetar o desempenho de forma negativa.

<!--
  The binary size comes from the additional thunks
  to translate between calling conventions.
  The performance of linking and launch are slower
  because of the larger symbol table slowing dyld down.
-->

### preconcurrency

Aplique este atributo a uma declaração
para suprimir a verificação estrita de concorrência.
Você pode aplicar este atributo
aos seguintes tipos de declaração:

- Declarações `import`
- Structs, classes e actors
- Enums e casos de enum
- Protocolos
- Variáveis e constantes
- Subscripts
- Inicializadores
- Funções

Em uma declaração de import,
este atributo reduz o rigor da verificação de concorrência
para o código que usa tipos do módulo importado.
Especificamente,
tipos do módulo importado
que não estejam explicitamente marcados como nonsendable
podem ser usados em um contexto que exige tipos sendable.

Em outras declarações,
este atributo reduz o rigor da verificação de concorrência
para o código que usa o símbolo que está sendo declarado.
Quando você usa esse símbolo em um escopo com verificação mínima de concorrência,
restrições relacionadas à concorrência especificadas por esse símbolo,
como requisitos `Sendable` ou global actors,
não são verificadas.

Você pode usar este atributo da seguinte forma,
para ajudar na migração do código para a verificação estrita de concorrência:

1. Ative a verificação estrita.
1. Anote os imports com o atributo `preconcurrency`
   para os módulos que ainda não ativaram a verificação estrita.
1. Depois de migrar um módulo para a verificação estrita,
   remova o atributo `preconcurrency`.
   O compilador emite um aviso sobre
   qualquer lugar em que o atributo `preconcurrency` em um import
   não tenha mais efeito e deva ser removido.

Para as demais declarações,
adicione o atributo `preconcurrency`
quando você incluir restrições relacionadas à concorrência na declaração,
se ainda houver clientes
que não migraram para a verificação estrita.
Remova o atributo `preconcurrency` depois que todos os seus clientes tiverem migrado.

Declarações vindas de Objective-C são sempre importadas
como se estivessem marcadas com o atributo `preconcurrency`.

### propertyWrapper

Aplique este atributo a uma declaração de classe, struct ou enum
para usar esse tipo como property wrapper.
Quando você aplica este atributo a um tipo,
cria um atributo personalizado com o mesmo nome do tipo.
Aplique esse novo atributo a uma propriedade de classe, struct ou enum
para envolver o acesso à propriedade por meio de uma instância do tipo wrapper;
aplique o atributo a uma declaração de variável armazenada local
para envolver o acesso à variável do mesmo jeito.
Variáveis computadas, variáveis globais e constantes não podem usar property wrappers.

<!--
  - test: `property-wrappers-can-go-on-stored-variable`

  ```swifttest
  >> @propertyWrapper struct UselessWrapper { var wrappedValue: Int }
  >> func f() {
  >>     @UselessWrapper var d: Int = 20
  >>     print(d)
  >> }
  >> f()
  << 20
  ```
-->

<!--
  - test: `property-wrappers-cant-go-on-constants`

  ```swifttest
  >> @propertyWrapper struct UselessWrapper { var wrappedValue: Int }
  >> func f() {
  >>     @UselessWrapper let d: Int = 20
  >>     print(d)
  >> }
  !$ error: property wrapper can only be applied to a 'var'
  !! @UselessWrapper let d: Int = 20
  !! ^
  ```
-->

<!--
  - test: `property-wrappers-cant-go-on-computed-variable`

  ```swifttest
  >> @propertyWrapper struct UselessWrapper { var wrappedValue: Int }
  >> func f() {
  >>     @UselessWrapper var d: Int { return 20 }
  >>     print(d)
  >> }
  >> f()
  !$ error: property wrapper cannot be applied to a computed property
  !! @UselessWrapper var d: Int { return 20 }
  !! ^
  ```
-->

O wrapper precisa definir uma propriedade de instância `wrappedValue`.
O *valor encapsulado* da propriedade
é o valor que o getter e o setter dessa propriedade expõem.
Na maioria dos casos, `wrappedValue` é um valor computado,
mas pode ser um valor armazenado.
O wrapper define e gerencia
qualquer armazenamento subjacente necessário para o valor encapsulado.
O compilador sintetiza o armazenamento para a instância do tipo wrapper
adicionando um sublinhado (`_`) antes do nome da propriedade encapsulada ---
por exemplo, o wrapper de `someProperty` é armazenado como `_someProperty`.
O armazenamento sintetizado para o wrapper tem nível de controle de acesso `private`.

Uma propriedade que tem um property wrapper
pode incluir blocos `willSet` e `didSet`,
mas não pode sobrescrever os blocos `get` ou `set` sintetizados pelo compilador.

O Swift oferece duas formas de açúcar sintático
para a inicialização de um property wrapper.
Você pode usar a sintaxe de atribuição na definição de um valor encapsulado
para passar a expressão do lado direito da atribuição
como argumento do parâmetro `wrappedValue`
do inicializador do property wrapper.
Você também pode fornecer argumentos ao atributo
ao aplicá-lo a uma propriedade,
e esses argumentos são passados ao inicializador do property wrapper.
Por exemplo, no código abaixo,
`SomeStruct` chama cada um dos inicializadores que `SomeWrapper` define.

```swift
@propertyWrapper
struct SomeWrapper {
    var wrappedValue: Int
    var someValue: Double
    init() {
        self.wrappedValue = 100
        self.someValue = 12.3
    }
    init(wrappedValue: Int) {
        self.wrappedValue = wrappedValue
        self.someValue = 45.6
    }
    init(wrappedValue value: Int, custom: Double) {
        self.wrappedValue = value
        self.someValue = custom
    }
}

struct SomeStruct {
    // Uses init()
    @SomeWrapper var a: Int

    // Uses init(wrappedValue:)
    @SomeWrapper var b = 10

    // Both use init(wrappedValue:custom:)
    @SomeWrapper(custom: 98.7) var c = 30
    @SomeWrapper(wrappedValue: 30, custom: 98.7) var d
}
```

<!--
  - test: `propertyWrapper`

  ```swifttest
  -> @propertyWrapper
  -> struct SomeWrapper {
         var wrappedValue: Int
         var someValue: Double
         init() {
             self.wrappedValue = 100
             self.someValue = 12.3
         }
         init(wrappedValue: Int) {
             self.wrappedValue = wrappedValue
             self.someValue = 45.6
         }
         init(wrappedValue value: Int, custom: Double) {
             self.wrappedValue = value
             self.someValue = custom
         }
     }

  -> struct SomeStruct {
  ->     // Uses init()
  ->     @SomeWrapper var a: Int

  ->     // Uses init(wrappedValue:)
  ->     @SomeWrapper var b = 10

  ->     // Both use init(wrappedValue:custom:)
  ->     @SomeWrapper(custom: 98.7) var c = 30
  ->     @SomeWrapper(wrappedValue: 30, custom: 98.7) var d
  -> }
  ```
-->

<!--
  Comments in the SomeStruct part of the example above
  are on the line before instead of at the end of the line
  because the last example gets too long to fit on one line.
-->

<!--
  Initialization of a wrapped property using ``init(wrappedValue:)``
  can be split across multiple statements.
  However, you can only see that behavior using local variables
  which currently can't have a property wrapper.
  It would look like this:

  -> @SomeWrapper var e
  -> e = 20  // Uses init(wrappedValue:)
  -> e = 30  // Uses the property setter
-->

O *valor projetado* de uma propriedade encapsulada é um segundo valor
que um property wrapper pode usar para expor funcionalidade adicional.
O autor de um tipo property wrapper
é responsável por definir o significado do valor projetado
e a interface que o valor projetado expõe.
Para projetar um valor a partir de um property wrapper,
defina uma propriedade de instância `projectedValue` no tipo wrapper.
O compilador sintetiza um identificador para o valor projetado
adicionando um cifrão (`$`) antes do nome da propriedade encapsulada ---
por exemplo, o valor projetado de `someProperty` é `$someProperty`.
O valor projetado tem o mesmo nível de controle de acesso
que a propriedade encapsulada original.

```swift
@propertyWrapper
struct WrapperWithProjection {
    var wrappedValue: Int
    var projectedValue: SomeProjection {
        return SomeProjection(wrapper: self)
    }
}
struct SomeProjection {
    var wrapper: WrapperWithProjection
}

struct SomeStruct {
    @WrapperWithProjection var x = 123
}
let s = SomeStruct()
s.x           // Int value
s.$x          // SomeProjection value
s.$x.wrapper  // WrapperWithProjection value
```

<!--
  - test: `propertyWrapper-projection`

  ```swifttest
  -> @propertyWrapper
  -> struct WrapperWithProjection {
         var wrappedValue: Int
         var projectedValue: SomeProjection {
             return SomeProjection(wrapper: self)
         }
  }
  -> struct SomeProjection {
         var wrapper: WrapperWithProjection
  }

  -> struct SomeStruct {
  ->     @WrapperWithProjection var x = 123
  -> }
  -> let s = SomeStruct()
  >> _ =
  -> s.x           // Int value
  >> _ =
  -> s.$x          // SomeProjection value
  >> _ =
  -> s.$x.wrapper  // WrapperWithProjection value
  ```
-->

Se o valor projetado encapsular uma variável nomeada com um identificador bruto (raw identifier),
você também usa um identificador bruto para se referir
ao armazenamento sintetizado do valor e ao seu valor projetado.
Escreva o sublinhado ou o cifrão dentro das crases;
por exemplo, `` someValue.`_some raw identifier` ``
se refere ao armazenamento sintetizado
de uma propriedade cujo nome inclui espaços,
e `` someValue.`$some raw identifier` ``
se refere ao seu valor projetado.

### resultBuilder

Aplique este atributo a uma classe, struct ou enum
para usar esse tipo como result builder.
Um *result builder* é um tipo
que constrói uma estrutura de dados aninhada passo a passo.
Você usa result builders para implementar uma linguagem específica de domínio (DSL)
para criar structs de dados aninhadas de forma natural e declarativa.
Para um exemplo de como usar o atributo `resultBuilder`,
veja <doc:AdvancedOperators#Result-Builders>.

#### Métodos de construção de resultado

Um result builder implementa os métodos estáticos descritos a seguir.
Como toda a funcionalidade do result builder
é exposta por meio de métodos estáticos,
você nunca inicializa uma instância desse tipo.
Um result builder precisa implementar o método `buildBlock(_:)`
ou os métodos `buildPartialBlock(first:)`
e `buildPartialBlock(accumulated:next:)`.
Os outros métodos ---
que habilitam funcionalidades adicionais na DSL ---
são opcionais.
A declaração de um tipo result builder
não precisa, de fato, incluir nenhuma conformidade com protocolo.

A descrição dos métodos estáticos usa três tipos como marcadores.
O tipo `Expression` é um marcador
para o tipo da entrada do result builder,
`Component` é um marcador para o tipo de um resultado parcial,
e `FinalResult` é um marcador
para o tipo do resultado que o result builder produz.
Você substitui esses tipos pelos tipos reais que seu result builder usa.
Se os seus métodos de construção de resultado
não especificarem um tipo para `Expression` ou `FinalResult`,
eles usam, por padrão, o mesmo tipo de `Component`.

Os métodos de construção de blocos são os seguintes:

- term `static func buildBlock(_ components: Component...) -> Component`:
  Combina um array de resultados parciais em um único resultado parcial.

- term `static func buildPartialBlock(first: Component) -> Component`:
  Constrói um componente de resultado parcial a partir do primeiro componente.
  Implemente este método e também `buildPartialBlock(accumulated:next:)`
  para oferecer suporte à construção de blocos um componente por vez.
  Em comparação com `buildBlock(_:)`,
  essa abordagem reduz a necessidade de sobrecargas genéricas
  que tratam diferentes quantidades de argumentos.

- term `static func buildPartialBlock(accumulated: Component, next: Component) -> Component`:
  Constrói um componente de resultado parcial
  combinando um componente acumulado com um novo componente.
  Implemente este método e também `buildPartialBlock(first:)`
  para oferecer suporte à construção de blocos um componente por vez.
  Em comparação com `buildBlock(_:)`,
  essa abordagem reduz a necessidade de sobrecargas genéricas
  que tratam diferentes quantidades de argumentos.

Um result builder pode implementar os três métodos de construção de blocos listados acima;
nesse caso, a disponibilidade determina qual método é chamado.
Por padrão, o Swift chama os métodos `buildPartialBlock(first:)` e `buildPartialBlock(accumulated:next:)`.
Para que o Swift chame `buildBlock(_:)` no lugar,
marque a declaração que a envolve como disponível
antes da disponibilidade que você escreve em `buildPartialBlock(first:)` e
`buildPartialBlock(accumulated:next:)`.

Os métodos adicionais de construção de resultado são os seguintes:

- term `static func buildOptional(_ component: Component?) -> Component`:
  Constrói um resultado parcial a partir de um resultado parcial que pode ser `nil`.
  Implemente este método para oferecer suporte a instruções `if`
  que não incluem uma cláusula `else`.

- term `static func buildEither(first: Component) -> Component`:
  Constrói um resultado parcial cujo valor varia dependendo de alguma condição.
  Implemente este método e também `buildEither(second:)`
  para oferecer suporte a instruções `switch`
  e a instruções `if` que incluem uma cláusula `else`.

- term `static func buildEither(second: Component) -> Component`:
  Constrói um resultado parcial cujo valor varia dependendo de alguma condição.
  Implemente este método e também `buildEither(first:)`
  para oferecer suporte a instruções `switch`
  e a instruções `if` que incluem uma cláusula `else`.

- term `static func buildArray(_ components: [Component]) -> Component`:
  Constrói um resultado parcial a partir de um array de resultados parciais.
  Implemente este método para oferecer suporte a laços `for`.

- term `static func buildExpression(_ expression: Expression) -> Component`:
  Constrói um resultado parcial a partir de uma expressão.
  Você pode implementar este método para fazer um pré-processamento ---
  por exemplo, converter expressões para um tipo interno ---
  ou para fornecer informações adicionais para a inferência de tipos nos pontos de uso.

- term `static func buildFinalResult(_ component: Component) -> FinalResult`:
  Constrói um resultado final a partir de um resultado parcial.
  Você pode implementar este método como parte de um result builder
  que usa um tipo diferente para resultados parciais e finais,
  ou para fazer outro pós-processamento em um resultado antes de retorná-lo.

- term `static func buildLimitedAvailability(_ component: Component) -> Component`:
  Constrói um resultado parcial que apaga as informações de tipo.
  Você pode implementar este método para impedir que as informações de tipo
  se propaguem para fora de uma instrução de controle do compilador
  que faz uma verificação de disponibilidade.

Por exemplo, o código abaixo define um result builder simples
que constrói um array de inteiros.
Este código define `Component` e `Expression` como aliases de tipo,
para facilitar a correspondência dos exemplos abaixo com a lista de métodos acima.

```swift
@resultBuilder
struct ArrayBuilder {
    typealias Component = [Int]
    typealias Expression = Int
    static func buildExpression(_ element: Expression) -> Component {
        return [element]
    }
    static func buildOptional(_ component: Component?) -> Component {
        guard let component = component else { return [] }
        return component
    }
    static func buildEither(first component: Component) -> Component {
        return component
    }
    static func buildEither(second component: Component) -> Component {
        return component
    }
    static func buildArray(_ components: [Component]) -> Component {
        return Array(components.joined())
    }
    static func buildBlock(_ components: Component...) -> Component {
        return Array(components.joined())
    }
}
```

<!--
  - test: `array-result-builder`

  ```swifttest
  -> @resultBuilder
  -> struct ArrayBuilder {
         typealias Component = [Int]
         typealias Expression = Int
         static func buildExpression(_ element: Expression) -> Component {
             return [element]
         }
         static func buildOptional(_ component: Component?) -> Component {
  >>         print("Building optional...", component as Any)
             guard let component = component else { return [] }
             return component
         }
         static func buildEither(first component: Component) -> Component {
  >>         print("Building first...", component)
             return component
         }
         static func buildEither(second component: Component) -> Component {
  >>         print("Building second...", component)
             return component
         }
         static func buildArray(_ components: [Component]) -> Component {
             return Array(components.joined())
         }
         static func buildBlock(_ components: Component...) -> Component {
             return Array(components.joined())
         }
     }
  ```
-->

#### Transformações de resultado

As transformações sintáticas a seguir são aplicadas recursivamente
para transformar código que usa a sintaxe de result builder
em código que chama os métodos estáticos do tipo result builder:

- Se o result builder tiver um método `buildExpression(_:)`,
  cada expressão se torna uma chamada a esse método.
  Esta transformação é sempre a primeira.
  Por exemplo, as declarações a seguir são equivalentes:

  ```swift
  @ArrayBuilder var builderNumber: [Int] { 10 }
  var manualNumber = ArrayBuilder.buildExpression(10)
  ```

  <!--
    - test: `array-result-builder`

    ```swifttest
    -> @ArrayBuilder var builderNumber: [Int] { 10 }
    -> var manualNumber = ArrayBuilder.buildExpression(10)
    >> assert(builderNumber == manualNumber)
    ```
  -->
- Uma instrução de atribuição é transformada como uma expressão,
  mas é entendida como avaliando para `()`.
  Você pode definir uma sobrecarga de `buildExpression(_:)`
  que recebe um argumento do tipo `()` para tratar atribuições de forma específica.
- Uma instrução de desvio que verifica uma condição de disponibilidade
  se torna uma chamada ao método `buildLimitedAvailability(_:)`,
  se esse método estiver implementado.
  Se você não implementar `buildLimitedAvailability(_:)`,
  então as instruções de desvio que verificam disponibilidade
  usam as mesmas transformações das demais instruções de desvio.
  Esta transformação acontece antes da transformação em uma chamada a
  `buildEither(first:)`, `buildEither(second:)` ou `buildOptional(_:)`.

  Você usa o método `buildLimitedAvailability(_:)` para apagar informações de tipo
  que mudam dependendo de qual ramo é executado.
  Por exemplo,
  os métodos `buildEither(first:)` e `buildEither(second:)` a seguir
  usam um tipo genérico que captura informações de tipo dos dois ramos.

  ```swift
  protocol Drawable {
      func draw() -> String
  }
  struct Text: Drawable {
      var content: String
      init(_ content: String) { self.content = content }
      func draw() -> String { return content }
  }
  struct Line<D: Drawable>: Drawable {
      var elements: [D]
      func draw() -> String {
          return elements.map { $0.draw() }.joined(separator: "")
      }
  }
  struct DrawEither<First: Drawable, Second: Drawable>: Drawable {
      var content: Drawable
      func draw() -> String { return content.draw() }
  }

  @resultBuilder
  struct DrawingBuilder {
      static func buildBlock<D: Drawable>(_ components: D...) -> Line<D> {
          return Line(elements: components)
      }
      static func buildEither<First, Second>(first: First)
              -> DrawEither<First, Second> {
          return DrawEither(content: first)
      }
      static func buildEither<First, Second>(second: Second)
              -> DrawEither<First, Second> {
          return DrawEither(content: second)
      }
  }
  ```

  <!-- Comment block with swifttest for the code listing above is after the end of this bulleted list, due to tooling limitations. -->

  No entanto, essa abordagem causa um problema em código que tem verificações de disponibilidade:

  ```swift
  @available(macOS 99, *)
  struct FutureText: Drawable {
      var content: String
      init(_ content: String) { self.content = content }
      func draw() -> String { return content }
  }
  @DrawingBuilder var brokenDrawing: Drawable {
      if #available(macOS 99, *) {
          FutureText("Inside.future")  // Problem
      } else {
          Text("Inside.present")
      }
  }
  // The type of brokenDrawing is Line<DrawEither<Line<FutureText>, Line<Text>>>
  ```

  <!-- Comment block with swifttest for the code listing above is after the end of this bulleted list, due to tooling limitations. -->

  No código acima,
  `FutureText` aparece como parte do tipo de `brokenDrawing`
  porque é um dos tipos no tipo genérico `DrawEither`.
  Isso pode fazer seu programa travar se `FutureText`
  não estiver disponível em tempo de execução,
  mesmo que esse tipo não seja usado explicitamente.

  Para resolver esse problema,
  implemente um método `buildLimitedAvailability(_:)`
  para apagar as informações de tipo, retornando um tipo que está sempre disponível.
  Por exemplo, o código abaixo constrói um valor `AnyDrawable`
  a partir da verificação de disponibilidade.

  ```swift
  struct AnyDrawable: Drawable {
      var content: Drawable
      func draw() -> String { return content.draw() }
  }
  extension DrawingBuilder {
      static func buildLimitedAvailability(_ content: some Drawable) -> AnyDrawable {
          return AnyDrawable(content: content)
      }
  }

  @DrawingBuilder var typeErasedDrawing: Drawable {
      if #available(macOS 99, *) {
          FutureText("Inside.future")
      } else {
          Text("Inside.present")
      }
  }
  // The type of typeErasedDrawing is Line<DrawEither<AnyDrawable, Line<Text>>>
  ```

  <!-- Comment block with swifttest for the code listing above is after the end of this bulleted list, due to tooling limitations. -->

- Uma instrução de desvio se torna uma série de chamadas aninhadas aos
  métodos `buildEither(first:)` e `buildEither(second:)`.
  As condições e os casos da instrução são mapeados para os nós folha
  de uma árvore binária, e a instrução se torna
  uma chamada aninhada aos métodos `buildEither`
  seguindo o caminho até esse nó folha a partir do nó raiz.

  Por exemplo, se você escrever uma instrução `switch` com três casos,
  o compilador usa uma árvore binária com três nós folha.
  Da mesma forma,
  como o caminho do nó raiz até o segundo caso é
  “segundo filho” e depois “primeiro filho”,
  esse caso se torna uma chamada aninhada como
  `buildEither(first: buildEither(second: ... ))`.
  As declarações a seguir são equivalentes:

  ```swift
  let someNumber = 19
  @ArrayBuilder var builderConditional: [Int] {
      if someNumber < 12 {
          31
      } else if someNumber == 19 {
          32
      } else {
          33
      }
  }

  var manualConditional: [Int]
  if someNumber < 12 {
      let partialResult = ArrayBuilder.buildExpression(31)
      let outerPartialResult = ArrayBuilder.buildEither(first: partialResult)
      manualConditional = ArrayBuilder.buildEither(first: outerPartialResult)
  } else if someNumber == 19 {
      let partialResult = ArrayBuilder.buildExpression(32)
      let outerPartialResult = ArrayBuilder.buildEither(second: partialResult)
      manualConditional = ArrayBuilder.buildEither(first: outerPartialResult)
  } else {
      let partialResult = ArrayBuilder.buildExpression(33)
      manualConditional = ArrayBuilder.buildEither(second: partialResult)
  }
  ```

  <!--
    - test: `array-result-builder`

    ```swifttest
    -> let someNumber = 19
    -> @ArrayBuilder var builderConditional: [Int] {
           if someNumber < 12 {
               31
           } else if someNumber == 19 {
               32
           } else {
               33
           }
       }
    << Building second... [32]
    << Building first... [32]

    -> var manualConditional: [Int]
    -> if someNumber < 12 {
           let partialResult = ArrayBuilder.buildExpression(31)
           let outerPartialResult = ArrayBuilder.buildEither(first: partialResult)
           manualConditional = ArrayBuilder.buildEither(first: outerPartialResult)
       } else if someNumber == 19 {
           let partialResult = ArrayBuilder.buildExpression(32)
           let outerPartialResult = ArrayBuilder.buildEither(second: partialResult)
           manualConditional = ArrayBuilder.buildEither(first: outerPartialResult)
       } else {
           let partialResult = ArrayBuilder.buildExpression(33)
           manualConditional = ArrayBuilder.buildEither(second: partialResult)
       }
    >> assert(builderConditional == manualConditional)
    << Building second... [32]
    << Building first... [32]
    ```
  -->
- Uma instrução de desvio que pode não produzir um valor,
  como uma instrução `if` sem cláusula `else`,
  se torna uma chamada a `buildOptional(_:)`.
  Se a condição da instrução `if` for satisfeita,
  o bloco de código dela é transformado e passado como argumento;
  caso contrário, `buildOptional(_:)` é chamado com `nil` como argumento.
  Por exemplo, as declarações a seguir são equivalentes:

  ```swift
  @ArrayBuilder var builderOptional: [Int] {
      if (someNumber % 2) == 1 { 20 }
  }

  var partialResult: [Int]? = nil
  if (someNumber % 2) == 1 {
      partialResult = ArrayBuilder.buildExpression(20)
  }
  var manualOptional = ArrayBuilder.buildOptional(partialResult)
  ```

  <!--
    - test: `array-result-builder`

    ```swifttest
    -> @ArrayBuilder var builderOptional: [Int] {
           if (someNumber % 2) == 1 { 20 }
       }
    << Building optional... Optional([20])

    -> var partialResult: [Int]? = nil
    -> if (someNumber % 2) == 1 {
           partialResult = ArrayBuilder.buildExpression(20)
       }
    -> var manualOptional = ArrayBuilder.buildOptional(partialResult)
    << Building optional... Optional([20])
    >> assert(builderOptional == manualOptional)
    ```
  -->
- Se o result builder implementar os métodos
  `buildPartialBlock(first:)`
  e `buildPartialBlock(accumulated:next:)`,
  um bloco de código ou uma instrução `do` se torna uma chamada a esses métodos.
  A primeira instrução dentro do bloco é transformada para se tornar um argumento
  do método `buildPartialBlock(first:)`,
  e as instruções restantes se tornam chamadas aninhadas
  ao método `buildPartialBlock(accumulated:next:)`.
  Por exemplo, as declarações a seguir são equivalentes:

  ```swift
  struct DrawBoth<First: Drawable, Second: Drawable>: Drawable {
      var first: First
      var second: Second
      func draw() -> String { return first.draw() + second.draw() }
  }

  @resultBuilder
  struct DrawingPartialBlockBuilder {
      static func buildPartialBlock<D: Drawable>(first: D) -> D {
          return first
      }
      static func buildPartialBlock<Accumulated: Drawable, Next: Drawable>(
          accumulated: Accumulated, next: Next
      ) -> DrawBoth<Accumulated, Next> {
          return DrawBoth(first: accumulated, second: next)
      }
  }

  @DrawingPartialBlockBuilder var builderBlock: some Drawable {
      Text("First")
      Line(elements: [Text("Second"), Text("Third")])
      Text("Last")
  }

  let partialResult1 = DrawingPartialBlockBuilder.buildPartialBlock(first: Text("first"))
  let partialResult2 = DrawingPartialBlockBuilder.buildPartialBlock(
      accumulated: partialResult1,
      next: Line(elements: [Text("Second"), Text("Third")])
  )
  let manualResult = DrawingPartialBlockBuilder.buildPartialBlock(
      accumulated: partialResult2,
      next: Text("Last")
  )
  ```

  <!--
    - test: `drawing-partial-block-builder`

    ```swifttest
    -> @resultBuilder
    -> struct DrawingPartialBlockBuilder {
           static func buildPartialBlock<D: Drawable>(first: D) -> D {
               return first
           }
           static func buildPartialBlock<Accumulated: Drawable, Next: Drawable>(
               accumulated: Accumulated, next: Next
           ) -> DrawBoth<Accumulated, Next> {
               return DrawBoth(first: accumulated, second: next)
           }
       }
    -> @DrawingPartialBlockBuilder var builderBlock: some Drawable {
          Text("First")
          Line(elements: [Text("Second"), Text("Third")])
          Text("Last")
       }

    -> let partialResult1 = DrawingPartialBlockBuilder.buildPartialBlock(first: Text("first"))
    -> let partialResult2 = DrawingPartialBlockBuilder.buildPartialBlock(
          accumulated: partialResult1,
          next: Line(elements: [Text("Second"), Text("Third")])
       )
       let manualResult = DrawingPartialBlockBuilder.buildPartialBlock(
           accumulated: partialResult2,
           next: Text("Last")
       )
    >> assert(type(of: builderBlock) == type(of: manualResult))
    ```
  -->
- Caso contrário, um bloco de código ou uma instrução `do`
  se torna uma chamada ao método `buildBlock(_:)`.
  Cada uma das instruções dentro do bloco é transformada,
  uma por vez,
  e se torna um argumento do método `buildBlock(_:)`.
  Por exemplo, as declarações a seguir são equivalentes:

  ```swift
  @ArrayBuilder var builderBlock: [Int] {
      100
      200
      300
  }

  var manualBlock = ArrayBuilder.buildBlock(
      ArrayBuilder.buildExpression(100),
      ArrayBuilder.buildExpression(200),
      ArrayBuilder.buildExpression(300)
  )
  ```

  <!--
    - test: `array-result-builder`

    ```swifttest
    -> @ArrayBuilder var builderBlock: [Int] {
           100
           200
           300
       }

    -> var manualBlock = ArrayBuilder.buildBlock(
           ArrayBuilder.buildExpression(100),
           ArrayBuilder.buildExpression(200),
           ArrayBuilder.buildExpression(300)
       )
    >> assert(builderBlock == manualBlock)
    ```
  -->
- Um laço `for` se torna uma variável temporária, um laço `for`
  e uma chamada ao método `buildArray(_:)`.
  O novo laço `for` percorre a sequência
  e adiciona cada resultado parcial a esse array.
  O array temporário é passado como argumento na chamada a `buildArray(_:)`.
  Por exemplo, as declarações a seguir são equivalentes:

  ```swift
  @ArrayBuilder var builderArray: [Int] {
      for i in 5...7 {
          100 + i
      }
  }

  var temporary: [[Int]] = []
  for i in 5...7 {
      let partialResult = ArrayBuilder.buildExpression(100 + i)
      temporary.append(partialResult)
  }
  let manualArray = ArrayBuilder.buildArray(temporary)
  ```

  <!--
    - test: `array-result-builder`

    ```swifttest
    -> @ArrayBuilder var builderArray: [Int] {
           for i in 5...7 {
               100 + i
           }
       }

    -> var temporary: [[Int]] = []
    -> for i in 5...7 {
           let partialResult = ArrayBuilder.buildExpression(100 + i)
           temporary.append(partialResult)
       }
    -> let manualArray = ArrayBuilder.buildArray(temporary)
    >> assert(builderArray == manualArray)
    ```
  -->
- Se o result builder tiver um método `buildFinalResult(_:)`,
  o resultado final se torna uma chamada a esse método.
  Esta transformação é sempre a última.

<!--
  - test: `result-builder-limited-availability-broken, result-builder-limited-availability-ok`, `drawing-partial-result-builder`

  ```swifttest
  -> protocol Drawable {
         func draw() -> String
     }
  -> struct Text: Drawable {
         var content: String
         init(_ content: String) { self.content = content }
         func draw() -> String { return content }
     }
  -> struct Line<D: Drawable>: Drawable {
         var elements: [D]
         func draw() -> String {
             return elements.map { $0.draw() }.joined(separator: "")
         }
     }
  -> struct DrawEither<First: Drawable, Second: Drawable>: Drawable {
         var content: Drawable
         func draw() -> String { return content.draw() }
     }

  -> @resultBuilder
     struct DrawingBuilder {
         static func buildBlock<D: Drawable>(_ components: D...) -> Line<D> {
             return Line(elements: components)
         }
         static func buildEither<First, Second>(first: First)
                 -> DrawEither<First, Second> {
             return DrawEither(content: first)
         }
         static func buildEither<First, Second>(second: Second)
                 -> DrawEither<First, Second> {
             return DrawEither(content: second)
         }
     }
  ```
-->

<!--
  - test: `result-builder-limited-availability-broken`

  ```swifttest
  -> @available(macOS 99, *)
  -> struct FutureText: Drawable {
         var content: String
         init(_ content: String) { self.content = content }
         func draw() -> String { return content }
     }
  -> @DrawingBuilder var brokenDrawing: Drawable {
         if #available(macOS 99, *) {
             FutureText("Inside.future")  // Problem
         } else {
             Text("Inside.present")
         }
     }
  /> The type of brokenDrawing is \(type(of: brokenDrawing))
  </ The type of brokenDrawing is Line<DrawEither<Line<FutureText>, Line<Text>>>
  !$ warning: result builder 'DrawingBuilder' does not implement 'buildLimitedAvailability'; this code may crash on earlier versions of the OS
  !! if #available(macOS 99, *) {
  !! ^
  !$ note: add 'buildLimitedAvailability(_:)' to the result builder 'DrawingBuilder' to erase type information for less-available types
  !! struct DrawingBuilder {
  !! ^
  ```
-->

<!--
  - test: `result-builder-limited-availability-ok`

  ```swifttest
  >> @available(macOS 99, *)
  >> struct FutureText: Drawable {
  >>     var content: String
  >>     init(_ content: String) { self.content = content }
  >>     func draw() -> String { return content }
  >> }
  >> @DrawingBuilder var x: Drawable {
  >>     if #available(macOS 99, *) {
  >>         FutureText("Inside.future")
  >>     } else {
  >>         Text("Inside.present")
  >>     }
  >> }
  -> struct AnyDrawable: Drawable {
         var content: Drawable
         func draw() -> String { return content.draw() }
     }
  -> extension DrawingBuilder {
         static func buildLimitedAvailability(_ content: some Drawable) -> AnyDrawable {
             return AnyDrawable(content: content)
         }
     }

  -> @DrawingBuilder var typeErasedDrawing: Drawable {
         if #available(macOS 99, *) {
             FutureText("Inside.future")
         } else {
             Text("Inside.present")
         }
     }
  /> The type of typeErasedDrawing is \(type(of: typeErasedDrawing))
  </ The type of typeErasedDrawing is Line<DrawEither<AnyDrawable, Line<Text>>>
  ```
-->

Embora o comportamento das transformações seja descrito em termos de variáveis temporárias,
usar um result builder não cria, de fato, nenhuma declaração nova
que seja visível para o resto do código.

Você não pode usar
instruções `break`, `continue`, `defer`, `guard` ou `return`,
instruções `while`,
nem instruções `do`-`catch`
no código que um result builder transforma.

O processo de transformação não altera declarações no código,
o que permite usar constantes e variáveis temporárias
para montar expressões peça por peça.
Ele também não altera
instruções `throw`,
instruções de diagnóstico em tempo de compilação,
nem closures que contenham uma instrução `return`.

Sempre que possível, as transformações são agrupadas.
Por exemplo, a expressão `4 + 5 * 6` se torna
`buildExpression(4 + 5 * 6)`, em vez de várias chamadas a essa função.
Da mesma forma, instruções de desvio aninhadas se tornam
uma única árvore binária de chamadas aos métodos `buildEither`.

<!--
  - test: `result-builder-transform-complex-expression`

  ```swifttest
  >> @resultBuilder
  >> struct ArrayBuilder {
  >>     static func buildExpression(_ element: Int) -> [Int] {
  >>         print("Building", element)
  >>         return [element]
  >>     }
  >>     static func buildBlock(_ components: [Int]...) -> [Int] {
  >>         return Array(components.joined())
  >>     }
  >> }
  >> @ArrayBuilder var x: [Int] {
  >>     10+12*3
  >> }
  << Building 46
  >> print(x)
  << [46]
  ```
-->

#### Atributos personalizados de result builder

Criar um tipo result builder cria um atributo personalizado com o mesmo nome.
Você pode aplicar esse atributo nos lugares a seguir:

- Em uma declaração de função, o result builder constrói o corpo da função.
- Em uma declaração de variável ou de subscript que inclui um getter,
  o result builder constrói o corpo do getter.
- Em um parâmetro de uma declaração de função,
  o result builder constrói o corpo de um closure
  que é passado como o argumento correspondente.

Aplicar um atributo de result builder não afeta a compatibilidade de ABI.
Aplicar um atributo de result builder a um parâmetro
torna esse atributo parte da interface da função,
o que pode afetar a compatibilidade de código-fonte.

### requires_stored_property_inits

Aplique este atributo a uma declaração de classe
para exigir que todas as propriedades armazenadas dentro da classe
forneçam valores padrão como parte de suas definições.
Este atributo é inferido para qualquer classe
que herde de `NSManagedObject`.

<!--
  - test: `requires_stored_property_inits-requires-default-values`

  ```swifttest
  >> @requires_stored_property_inits class DefaultValueProvided {
         var value: Int = -1
         init() { self.value = 0 }
     }
  -> @requires_stored_property_inits class NoDefaultValue {
         var value: Int
         init() { self.value = 0 }
     }
  !$ error: stored property 'value' requires an initial value
  !! var value: Int
  !! ^
  !$ note: class 'NoDefaultValue' requires all stored properties to have initial values
  !! @requires_stored_property_inits class NoDefaultValue {
  !! ^
  ```
-->

### testable

Aplique este atributo a uma declaração `import`
para importar esse módulo com alterações em seu controle de acesso
que simplificam os testes do código do módulo.
Entidades do módulo importado
que estão marcadas com o modificador de nível de acesso `internal`
são importadas como se tivessem sido declaradas com o modificador de nível de acesso `public`.
Classes e membros de classe
que estão marcados com o modificador de nível de acesso `internal` ou `public`
são importados como se tivessem sido declarados com o modificador de nível de acesso `open`.
O módulo importado precisa ser compilado com os testes habilitados.

### UIApplicationMain

> Obsoleto:
> Este atributo está obsoleto;
> use o atributo <doc:Attributes#main> no lugar.
> No Swift 6,
> usar este atributo gera um erro de compilação.

Aplique este atributo a uma classe
para indicar que ela é o delegate do app.
Usar este atributo é equivalente a chamar a
função `UIApplicationMain` e
passar o nome dessa classe como o nome da classe delegate.

Se você não usar este atributo,
forneça um arquivo `main.swift` com código no nível superior
que chame a função [`UIApplicationMain(_:_:_:_:)`](https://developer.apple.com/documentation/uikit/uiapplicationmain(_:_:_:_:)-1yub7).
Por exemplo,
se seu app usar uma subclasse personalizada de `UIApplication`
como classe principal,
chame a função `UIApplicationMain(_:_:_:_:)`
em vez de usar este atributo.

O código Swift que você compila para criar um executável
pode conter no máximo um ponto de entrada de nível superior,
como discutido em <doc:Declarations#Top-Level-Code>.

### unchecked

Aplique este atributo a um tipo de protocolo
como parte da lista de protocolos adotados por uma declaração de tipo
para desligar a aplicação dos requisitos desse protocolo.

O único protocolo aceito é [`Sendable`](https://developer.apple.com/documentation/swift/sendable).

### usableFromInline

Aplique este atributo a uma declaração de função, método, propriedade computada, subscript,
inicializador ou desinicializador
para permitir que esse símbolo seja usado em código inlinable
definido no mesmo módulo da declaração.
A declaração precisa ter o modificador de nível de acesso `internal`.
Uma struct ou classe marcada com `usableFromInline`
só pode usar tipos que sejam públicos ou `usableFromInline` em suas propriedades.
Um enum marcado com `usableFromInline`
só pode usar tipos que sejam públicos ou `usableFromInline`
para os raw values e os associated values dos seus casos.

Assim como o modificador de nível de acesso `public`,
este atributo
expõe a declaração como parte da interface pública do módulo.
Diferentemente de `public`,
o compilador não permite que declarações marcadas com `usableFromInline`
sejam referenciadas pelo nome em código fora do módulo,
mesmo que o símbolo da declaração seja exportado.
No entanto, código fora do módulo ainda pode
interagir com o símbolo da declaração usando o comportamento em tempo de execução.

Declarações marcadas com o atributo `inlinable`
são implicitamente utilizáveis a partir de código inlinable.
Embora `inlinable` ou `usableFromInline` possam ser aplicados
a declarações `internal`,
aplicar os dois atributos é um erro.

<!--
  - test: `usableFromInline-and-inlinable-is-redundant`

  ```swifttest
  >> @usableFromInline @inlinable internal func f() { }
  !$ warning: '@usableFromInline' attribute has no effect on '@inlinable' global function 'f()'
  !! @usableFromInline @inlinable internal func f() { }
  !! ^~~~~~~~~~~~~~~~~~
  ```
-->

### warn_unqualified_access

Aplique este atributo a uma
função de nível superior, método de instância, ou método de classe ou estático
para disparar avisos quando essa função ou método for usado
sem um qualificador anterior,
como um nome de módulo, um nome de tipo ou uma variável ou constante de instância.
Use este atributo para ajudar a evitar ambiguidade entre funções
com o mesmo nome que são acessíveis no mesmo escopo.

Por exemplo,
a biblioteca padrão do Swift inclui tanto uma função
[`min(_:_:)`](https://developer.apple.com/documentation/swift/min(_:_:))
de nível superior
quanto um método
[`min()`](https://developer.apple.com/documentation/swift/sequence/min())
para sequências com elementos comparáveis.
O método da sequência é declarado com o atributo `warn_unqualified_access`
para ajudar a reduzir a confusão
ao tentar usar um ou outro dentro de uma extension de `Sequence`.

### Atributos de declaração usados pelo Interface Builder

Atributos do Interface Builder são atributos de declaração
usados pelo Interface Builder para sincronizar com o Xcode.
O Swift fornece os seguintes atributos do Interface Builder:
`IBAction`, `IBSegueAction`, `IBOutlet`,
`IBDesignable` e `IBInspectable`.
Esses atributos são conceitualmente iguais aos
equivalentes em Objective-C.

<!--
  TODO: Need to link to the relevant discussion of these attributes in Objc.
-->

Você aplica os atributos `IBOutlet` e `IBInspectable`
a declarações de propriedade de uma classe.
Você aplica os atributos `IBAction` e `IBSegueAction`
a declarações de método de uma classe
e o atributo `IBDesignable` a declarações de classe.

Aplicar os atributos `IBAction`, `IBSegueAction`, `IBOutlet`,
`IBDesignable` ou `IBInspectable`
também implica o atributo `objc`.

## Atributos de tipo

Você pode aplicar atributos de tipo apenas a tipos.

### autoclosure

Aplique este atributo para adiar a avaliação de uma expressão,
envolvendo automaticamente essa expressão em um closure sem argumentos.
Você o aplica ao tipo de um parâmetro em uma declaração de função ou de método,
para um parâmetro cujo tipo é um tipo de função que não recebe argumentos
e que retorna um valor do tipo da expressão.
Para um exemplo de como usar o atributo `autoclosure`,
veja <doc:Closures#Autoclosures> e <doc:Types#Function-Type>.

### convention

Aplique este atributo ao tipo de uma função
para indicar as convenções de chamada dela.

O atributo `convention` sempre aparece com
um dos seguintes argumentos:

- O argumento `swift` indica uma referência a uma função Swift.
  Esta é a convenção de chamada padrão para valores de função no Swift.
- O argumento `block` indica uma referência a um bloco compatível com Objective-C.
  O valor da função é representado como uma referência ao objeto do bloco,
  que é um objeto Objective-C compatível com `id` que incorpora sua função de invocação
  dentro do objeto.
  A função de invocação usa a convenção de chamada C.
- O argumento `c` indica uma referência a uma função C.
  O valor da função não carrega contexto e usa a convenção de chamada C.

<!--
  Note: @convention(thin) is private, even though it doesn't have an underscore
  https://forums.swift.org/t/12087/6
-->

Com algumas exceções,
uma função de qualquer convenção de chamada pode ser usada
quando é necessária uma função com outra convenção de chamada.
Uma função global não genérica,
uma função local que não captura nenhuma variável local,
ou um closure que não captura nenhuma variável local
podem ser convertidos para a convenção de chamada C.
Outras funções Swift não podem ser convertidas para a convenção de chamada C.
Uma função com a convenção de chamada de bloco do Objective-C
não pode ser convertida para a convenção de chamada C.

### escaping

Aplique este atributo ao tipo de um parâmetro em uma declaração de função ou de método
para indicar que o valor do parâmetro pode ser armazenado para execução posterior.
Isso significa que o valor pode sobreviver ao tempo de vida da chamada.
Parâmetros de tipo função com o atributo de tipo `escaping`
exigem o uso explícito de `self.` para propriedades ou métodos.
Para um exemplo de como usar o atributo `escaping`,
veja <doc:Closures#Escaping-Closures>.

### Sendable

Aplique este atributo ao tipo de uma função
para indicar que a função ou o closure é sendable.
Aplicar este atributo a um tipo de função
tem o mesmo significado que fazer um tipo que não é de função
conformar com o protocolo [`Sendable`](https://developer.apple.com/documentation/swift/sendable).

Este atributo é inferido em funções e closures
se a função ou o closure for usado em um contexto
que espera um valor sendable,
e a função ou o closure satisfizer os requisitos para ser sendable.

Um tipo de função sendable
é um subtipo do tipo de função nonsendable correspondente.

## Atributos de caso de switch

Você pode aplicar atributos de caso de switch apenas a casos de switch.

### unknown

Aplique este atributo a um caso de switch
para indicar que não se espera que ele seja correspondido
por nenhum caso conhecido do enum
no momento em que o código é compilado.
Para um exemplo de como usar o atributo `unknown`,
veja <doc:Statements#Switching-Over-Future-Enumeration-Cases>.

> Gramática de um atributo:
>
> *attribute* → **`@`** *attribute-name* *attribute-argument-clause*_?_ \
> *attribute-name* → *identifier* \
> *attribute-argument-clause* → **`(`** *balanced-tokens*_?_ **`)`** \
> *attributes* → *attribute* *attributes*_?_
>
> *balanced-tokens* → *balanced-token* *balanced-tokens*_?_ \
> *balanced-token* → **`(`** *balanced-tokens*_?_ **`)`** \
> *balanced-token* → **`[`** *balanced-tokens*_?_ **`]`** \
> *balanced-token* → **`{`** *balanced-tokens*_?_ **`}`** \
> *balanced-token* → Any identifier, keyword, literal, or operator \
> *balanced-token* → Any punctuation except  **`(`**,  **`)`**,  **`[`**,  **`]`**,  **`{`**, or  **`}`**

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
