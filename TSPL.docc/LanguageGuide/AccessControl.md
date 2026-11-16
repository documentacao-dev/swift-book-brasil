# Controle de acesso

Gerencie a visibilidade do código por declaração, arquivo e módulo.

*Controle de acesso* restringe o acesso a partes do seu código
a partir de código em outros arquivos-fonte e módulos.
Esse recurso permite ocultar os detalhes de implementação do seu código
e definir uma interface preferida pela qual esse código pode ser acessado e usado.

Você pode atribuir níveis de acesso específicos a tipos individuais
(classes, structs e enums),
assim como a propriedades, métodos, inicializadores e subscripts pertencentes a esses tipos.
Protocolos podem ser restritos a um determinado contexto,
assim como constantes, variáveis e funções globais.

Além de oferecer vários níveis de controle de acesso,
o Swift reduz a necessidade de especificar níveis de acesso explícitos
ao fornecer níveis de acesso padrão para cenários típicos.
Na verdade, se você estiver escrevendo um app com um único target,
talvez nem precise especificar níveis de acesso explícitos.

> Nota: Os vários aspectos do seu código aos quais o controle de acesso pode ser aplicado
> (propriedades, tipos, funções e assim por diante)
> são chamados de “entidades” nas seções abaixo, por brevidade.

## Módulos, arquivos-fonte e pacotes

O modelo de controle de acesso do Swift se baseia no conceito de
módulos, arquivos-fonte e pacotes.

Um *módulo* é uma única unidade de distribuição de código:
um framework ou app que é compilado e distribuído como uma unidade única
e que pode ser importado por outro módulo com a palavra-chave `import` do Swift.

Cada target de build (como um bundle de app ou um framework) no Xcode
é tratado como um módulo separado no Swift.
Se você agrupar aspectos do código do seu app como um framework independente
(talvez para encapsular e reutilizar esse código em vários apps),
então tudo o que você definir dentro desse framework fará parte de um módulo separado
quando for importado e usado dentro de um app,
ou quando for usado dentro de outro framework.

Um *arquivo-fonte* é um único arquivo de código-fonte Swift dentro de um módulo
(na prática, um único arquivo dentro de um app ou framework).
Embora seja comum definir tipos individuais em arquivos-fonte separados,
um único arquivo-fonte pode conter definições de vários tipos, funções e assim por diante.

Um *pacote* é um grupo de módulos que você desenvolve como uma unidade.
Você define os módulos que formam um pacote
como parte da configuração do sistema de build que você está usando,
e não como parte do seu código-fonte Swift.
Por exemplo, se você usa o Swift Package Manager para compilar seu código,
define um pacote no arquivo `Package.swift`
usando as APIs do módulo [PackageDescription][],
e se usa o Xcode, especifica o nome do pacote
na configuração de build Package Access Identifier.

[PackageDescription]: https://developer.apple.com/documentation/packagedescription

## Níveis de acesso

O Swift oferece seis *níveis de acesso* diferentes para entidades no seu código.
Esses níveis de acesso são relativos ao arquivo-fonte em que uma entidade é definida,
ao módulo a que esse arquivo-fonte pertence
e ao pacote a que o módulo pertence.

- *Acesso open* e *acesso public*
  permitem que entidades sejam usadas em qualquer arquivo-fonte do módulo que as define,
  e também em um arquivo-fonte de outro módulo que importe o módulo que as define.
  Você normalmente usa acesso open ou public ao especificar a interface pública de um framework.
  A diferença entre open e public é descrita abaixo.
- *Acesso package*
  permite que entidades sejam usadas em qualquer arquivo-fonte do pacote que as define,
  mas não em nenhum arquivo-fonte fora desse pacote.
  Você normalmente usa acesso package
  dentro de um app ou framework estruturado em vários módulos.
- *Acesso internal*
  permite que entidades sejam usadas em qualquer arquivo-fonte do módulo que as define,
  mas não em nenhum arquivo-fonte fora desse módulo.
  Você normalmente usa acesso internal ao definir
  a estrutura interna de um app ou framework.
- *Acesso file-private*
  restringe o uso de uma entidade ao seu próprio arquivo-fonte.
  Use acesso file-private para ocultar os detalhes de implementação de
  uma funcionalidade específica quando esses detalhes são usados em um arquivo inteiro.
- *Acesso private*
  restringe o uso de uma entidade à declaração que a envolve,
  e às extensões dessa declaração que estejam no mesmo arquivo.
  Use acesso private para ocultar os detalhes de implementação de
  uma funcionalidade específica quando esses detalhes são usados apenas dentro de uma única declaração.

O acesso open é o nível de acesso mais alto (menos restritivo),
e o acesso private é o nível mais baixo (mais restritivo).

O acesso open se aplica apenas a classes e membros de classes,
e difere do acesso public
por permitir que código fora do módulo crie subclasses e sobrescreva membros,
como discutido abaixo em <doc:AccessControl#Subclassing>.
Marcar uma classe como open indica explicitamente
que você considerou o impacto de código de outros módulos
usando essa classe como superclasse,
e que projetou o código da sua classe de acordo com isso.

### Princípio orientador dos níveis de acesso

Os níveis de acesso no Swift seguem um princípio orientador geral:
*Nenhuma entidade pode ser definida em termos de outra entidade que tenha
um nível de acesso mais baixo (mais restritivo).*

Por exemplo:

- Uma variável public não pode ser definida com tipo internal, file-private ou private,
  porque o tipo pode não estar disponível em todos os lugares onde a variável public é usada.
- Uma função não pode ter nível de acesso mais alto que os tipos dos parâmetros e o tipo de retorno,
  porque a função poderia ser usada em situações em que
  seus tipos constituintes não estão disponíveis para o código ao redor.

As implicações específicas desse princípio para diferentes aspectos da linguagem
são detalhadas abaixo.

### Níveis de acesso padrão

Todas as entidades do seu código
(com algumas exceções específicas, descritas mais adiante neste capítulo)
têm o nível de acesso padrão internal
se você não especificar um nível de acesso explícito.
Por isso, em muitos casos você não precisa especificar
um nível de acesso explícito no seu código.

### Níveis de acesso para apps com um único target

Quando você escreve um app simples com um único target,
o código do app normalmente é autocontido dentro do app
e não precisa ser disponibilizado fora do módulo do app.
O nível de acesso padrão internal já atende a esse requisito.
Portanto, você não precisa especificar um nível de acesso personalizado.
Talvez valha marcar algumas partes do código como file-private ou private
para ocultar seus detalhes de implementação de outros códigos dentro do módulo do app.

### Níveis de acesso para frameworks

Ao desenvolver um framework,
marque a interface voltada para o público como open ou public
para que ela possa ser vista e acessada por outros módulos,
como um app que importa o framework.
Essa interface pública é a interface de programação de aplicações (API) do framework.

> Nota: Qualquer detalhe de implementação interno do seu framework ainda pode usar
> o nível de acesso padrão internal,
> ou pode ser marcado como private ou file-private se você quiser ocultá-lo de
> outras partes do código interno do framework.
> Você só precisa marcar uma entidade como open ou public se quiser que ela se torne
> parte da API do seu framework.

### Níveis de acesso para targets de testes unitários

Ao escrever um app com um target de testes unitários,
o código do app precisa ser disponibilizado para esse módulo para que possa ser testado.
Por padrão, apenas entidades marcadas como open ou public
são acessíveis a outros módulos.
No entanto, um target de testes unitários pode acessar qualquer entidade internal,
se você marcar a declaração de import do módulo do produto com o atributo `@testable`
e compilar esse módulo do produto com testes habilitados.

## Sintaxe do controle de acesso

Defina o nível de acesso de uma entidade colocando
um dos modificadores listados em <doc:AccessControl#Access-Levels>,
como `public` ou `private`,
no início da declaração da entidade.
Por exemplo:

```swift
public class SomePublicClass {}
internal struct SomeInternalStruct() {}
private func somePrivateFunction() {}
```

O código acima declara `SomePublicClass` como public,
`SomeInternalStruct` como internal,
e `somePrivateFunction()` como private.
Se você não escrever um nível de acesso explícito,
o modificador de acesso padrão é `internal`,
como descrito em <doc:AccessControl#Default-Access-Levels>.
Por exemplo, no código abaixo, `SomeInternalStruct` é implicitamente internal:

```swift
struct SomeInternalStruct() {}
```

## Tipos personalizados

Se você quiser especificar um nível de acesso explícito para um tipo personalizado,
faça isso no momento em que define o tipo.
O novo tipo pode então ser usado em qualquer lugar que seu nível de acesso permita.
Por exemplo, se você definir uma classe file-private,
essa classe só pode ser usada como o tipo de uma propriedade,
ou como tipo de parâmetro ou de retorno de uma função,
no arquivo-fonte em que a classe file-private é definida.

O nível de controle de acesso de um tipo também afeta
o nível de acesso padrão dos *membros* desse tipo
(suas propriedades, métodos, inicializadores e subscripts).
Se você definir o nível de acesso de um tipo como private ou file-private,
o nível de acesso padrão dos membros também será private ou file-private.
Se você definir o nível de acesso de um tipo como internal ou public
(ou usar o nível de acesso padrão internal sem especificar um nível explicitamente),
o nível de acesso padrão dos membros do tipo será internal.

> Importante: Um tipo public tem membros internal por padrão, não public.
> Se você quiser que um membro do tipo seja public, precisa marcá-lo explicitamente como tal.
> Essa exigência garante que a API pública de um tipo seja
> algo que você escolhe publicar,
> e evita apresentar os detalhes internos de um tipo como API pública por engano.

```swift
public class SomePublicClass {                   // explicitly public class
    public var somePublicProperty = 0            // explicitly public class member
    var someInternalProperty = 0                 // implicitly internal class member
    fileprivate func someFilePrivateMethod() {}  // explicitly file-private class member
    private func somePrivateMethod() {}          // explicitly private class member
}

class SomeInternalClass {                        // implicitly internal class
    var someInternalProperty = 0                 // implicitly internal class member
    fileprivate func someFilePrivateMethod() {}  // explicitly file-private class member
    private func somePrivateMethod() {}          // explicitly private class member
}

fileprivate class SomeFilePrivateClass {         // explicitly file-private class
    func someFilePrivateMethod() {}              // implicitly file-private class member
    private func somePrivateMethod() {}          // explicitly private class member
}

private class SomePrivateClass {                 // explicitly private class
    func somePrivateMethod() {}                  // implicitly private class member
}
```

<!--
  - test: `accessControl, accessControlWrong`

  ```swifttest
  -> public class SomePublicClass {                  // explicitly public class
        public var somePublicProperty = 0            // explicitly public class member
        var someInternalProperty = 0                 // implicitly internal class member
        fileprivate func someFilePrivateMethod() {}  // explicitly file-private class member
        private func somePrivateMethod() {}          // explicitly private class member
     }

  -> class SomeInternalClass {                       // implicitly internal class
        var someInternalProperty = 0                 // implicitly internal class member
        fileprivate func someFilePrivateMethod() {}  // explicitly file-private class member
        private func somePrivateMethod() {}          // explicitly private class member
     }

  -> fileprivate class SomeFilePrivateClass {        // explicitly file-private class
        func someFilePrivateMethod() {}              // implicitly file-private class member
        private func somePrivateMethod() {}          // explicitly private class member
     }

  -> private class SomePrivateClass {                // explicitly private class
        func somePrivateMethod() {}                  // implicitly private class member
     }
  ```
-->

### Tipos de tupla

O nível de acesso de um tipo tupla é
o mais restritivo entre todos os tipos usados nessa tupla.
Por exemplo, se você compuser uma tupla a partir de dois tipos diferentes,
um com acesso internal e outro com acesso private,
o nível de acesso desse tipo tupla composto será private.

<!--
  - test: `tupleTypes_Module1, tupleTypes_Module1_PublicAndInternal, tupleTypes_Module1_Private`

  ```swifttest
  -> public struct PublicStruct {}
  -> internal struct InternalStruct {}
  -> fileprivate struct FilePrivateStruct {}
  -> public func returnPublicTuple() -> (PublicStruct, PublicStruct) {
        return (PublicStruct(), PublicStruct())
     }
  -> func returnInternalTuple() -> (PublicStruct, InternalStruct) {
        return (PublicStruct(), InternalStruct())
     }
  -> fileprivate func returnFilePrivateTuple() -> (PublicStruct, FilePrivateStruct) {
        return (PublicStruct(), FilePrivateStruct())
     }
  ```
-->

<!--
  - test: `tupleTypes_Module1_PublicAndInternal`

  ```swifttest
  // tuples with (at least) internal members can be accessed within their own module
  -> let publicTuple = returnPublicTuple()
  -> let internalTuple = returnInternalTuple()
  ```
-->

<!--
  - test: `tupleTypes_Module1_Private`

  ```swifttest
  // a tuple with one or more private members can't be accessed from outside of its source file
  -> let privateTuple = returnFilePrivateTuple()
  !$ error: cannot find 'returnFilePrivateTuple' in scope
  !! let privateTuple = returnFilePrivateTuple()
  !!                    ^~~~~~~~~~~~~~~~~~~~~~
  ```
-->

<!--
  - test: `tupleTypes_Module2_Public`

  ```swifttest
  // a public tuple with all-public members can be used in another module
  -> import tupleTypes_Module1
  -> let publicTuple = returnPublicTuple()
  ```
-->

<!--
  - test: `tupleTypes_Module2_InternalAndPrivate`

  ```swifttest
  // tuples with internal or private members can't be used outside of their own module
  -> import tupleTypes_Module1
  -> let internalTuple = returnInternalTuple()
  -> let privateTuple = returnFilePrivateTuple()
  !$ error: cannot find 'returnInternalTuple' in scope
  !! let internalTuple = returnInternalTuple()
  !!                     ^~~~~~~~~~~~~~~~~~~
  !$ error: cannot find 'returnFilePrivateTuple' in scope
  !! let privateTuple = returnFilePrivateTuple()
  !!                    ^~~~~~~~~~~~~~~~~~~~~~
  ```
-->

> Nota: Tipos de tupla não têm uma definição independente como
> classes, structs, enums e funções têm.
> O nível de acesso de um tipo tupla é determinado automaticamente
> pelos tipos que compõem a tupla,
> e não pode ser especificado explicitamente.

### Tipos de função

O nível de acesso de um tipo de função é calculado como
o mais restritivo entre os níveis de acesso dos tipos dos parâmetros e do tipo de retorno da função.
Você deve especificar o nível de acesso explicitamente como parte da definição da função
se o nível de acesso calculado não corresponder ao padrão do contexto.

O exemplo abaixo define uma função global chamada `someFunction()`,
sem fornecer um modificador de acesso específico para a própria função.
Você pode esperar que essa função tenha o nível de acesso padrão “internal”,
mas não é isso que acontece.
Na verdade, `someFunction()` não compila como escrita abaixo:

```swift
func someFunction() -> (SomeInternalClass, SomePrivateClass) {
    // function implementation goes here
}
```

<!--
  - test: `accessControlWrong`

  ```swifttest
  -> func someFunction() -> (SomeInternalClass, SomePrivateClass) {
        // function implementation goes here
  >>    return (SomeInternalClass(), SomePrivateClass())
     }
  !! /tmp/swifttest.swift:19:6: error: function must be declared private or fileprivate because its result uses a private type
  !! func someFunction() -> (SomeInternalClass, SomePrivateClass) {
  !! ^
  ```
-->

O tipo de retorno da função é
um tipo tupla composto de duas das classes personalizadas definidas acima em <doc:AccessControl#Custom-Types>.
Uma dessas classes é definida como internal,
e a outra como private.
Portanto, o nível de acesso geral do tipo tupla composto é private
(o menor nível de acesso entre os tipos constituintes da tupla).

Como o tipo de retorno da função é private,
você deve marcar o nível de acesso geral da função com o modificador `private`
para que a declaração da função seja válida:

```swift
private func someFunction() -> (SomeInternalClass, SomePrivateClass) {
    // function implementation goes here
}
```

<!--
  - test: `accessControl`

  ```swifttest
  -> private func someFunction() -> (SomeInternalClass, SomePrivateClass) {
        // function implementation goes here
  >>    return (SomeInternalClass(), SomePrivateClass())
     }
  ```
-->

Não é válido marcar a definição de `someFunction()`
com os modificadores `public` ou `internal`,
nem usar o padrão internal,
porque usuários public ou internal da função podem não ter o acesso adequado
à classe private usada no tipo de retorno da função.

### Tipos de enum

Cada caso de um enum recebe automaticamente o mesmo nível de acesso
do enum a que pertence.
Você não pode especificar um nível de acesso diferente para casos individuais de enum.

No exemplo abaixo,
o enum `CompassPoint` tem o nível de acesso explícito public.
Os casos do enum `north`, `south`, `east` e `west`
portanto também têm nível de acesso public:

```swift
public enum CompassPoint {
    case north
    case south
    case east
    case west
}
```

<!--
  - test: `enumerationCases`

  ```swifttest
  -> public enum CompassPoint {
        case north
        case south
        case east
        case west
     }
  ```
-->

<!--
  - test: `enumerationCases_Module1`

  ```swifttest
  -> public enum CompassPoint {
        case north
        case south
        case east
        case west
     }
  ```
-->

<!--
  - test: `enumerationCases_Module2`

  ```swifttest
  -> import enumerationCases_Module1
  -> let north = CompassPoint.north
  ```
-->

#### Raw values e associated values

Os tipos usados em quaisquer raw values ou associated values em uma definição de enum
devem ter um nível de acesso pelo menos tão alto quanto o nível de acesso do enum.
Por exemplo,
você não pode usar um tipo private como tipo do raw value de
um enum com nível de acesso internal.

### Tipos aninhados

O nível de acesso de um tipo aninhado é o mesmo do seu tipo contêiner,
a menos que o tipo contêiner seja public.
Tipos aninhados definidos dentro de um tipo public
têm nível de acesso automático internal.
Se você quiser que um tipo aninhado dentro de um tipo public seja disponibilizado publicamente,
precisa declará-lo explicitamente como public.

<!--
  - test: `nestedTypes_Module1, nestedTypes_Module1_PublicAndInternal, nestedTypes_Module1_Private`

  ```swifttest
  -> public struct PublicStruct {
        public enum PublicEnumInsidePublicStruct { case a, b }
        internal enum InternalEnumInsidePublicStruct { case a, b }
        private enum PrivateEnumInsidePublicStruct { case a, b }
        enum AutomaticEnumInsidePublicStruct { case a, b }
     }
  -> internal struct InternalStruct {
        internal enum InternalEnumInsideInternalStruct { case a, b }
        private enum PrivateEnumInsideInternalStruct { case a, b }
        enum AutomaticEnumInsideInternalStruct { case a, b }
     }
  -> private struct FilePrivateStruct {
        enum AutomaticEnumInsideFilePrivateStruct { case a, b }
        private enum PrivateEnumInsideFilePrivateStruct { case a, b }
     }
  -> private struct PrivateStruct {
        enum AutomaticEnumInsidePrivateStruct { case a, b }
        private enum PrivateEnumInsidePrivateStruct { case a, b }
     }
  ```
-->

<!--
  - test: `nestedTypes_Module1_PublicAndInternal`

  ```swifttest
  // these are all expected to succeed within the same module
  -> let publicNestedInsidePublic = PublicStruct.PublicEnumInsidePublicStruct.a
  -> let internalNestedInsidePublic = PublicStruct.InternalEnumInsidePublicStruct.a
  -> let automaticNestedInsidePublic = PublicStruct.AutomaticEnumInsidePublicStruct.a

  -> let internalNestedInsideInternal = InternalStruct.InternalEnumInsideInternalStruct.a
  -> let automaticNestedInsideInternal = InternalStruct.AutomaticEnumInsideInternalStruct.a
  ```
-->

<!--
  - test: `nestedTypes_Module1_Private`

  ```swifttest
  // these are all expected to fail, because they're private to the other file
  -> let privateNestedInsidePublic = PublicStruct.PrivateEnumInsidePublicStruct.a

  -> let privateNestedInsideInternal = InternalStruct.PrivateEnumInsideInternalStruct.a

  -> let privateNestedInsidePrivate = PrivateStruct.PrivateEnumInsidePrivateStruct.a
  -> let automaticNestedInsidePrivate = PrivateStruct.AutomaticEnumInsidePrivateStruct.a

  !$ error: 'PrivateEnumInsidePublicStruct' is inaccessible due to 'private' protection level
  !! let privateNestedInsidePublic = PublicStruct.PrivateEnumInsidePublicStruct.a
  !!                                              ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  !$ note: 'PrivateEnumInsidePublicStruct' declared here
  !! private enum PrivateEnumInsidePublicStruct { case a, b }
  !! ^
  !$ error: 'PrivateEnumInsideInternalStruct' is inaccessible due to 'private' protection level
  !! let privateNestedInsideInternal = InternalStruct.PrivateEnumInsideInternalStruct.a
  !!                                                  ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  !$ note: 'PrivateEnumInsideInternalStruct' declared here
  !! private enum PrivateEnumInsideInternalStruct { case a, b }
  !! ^
  !$ error: cannot find 'PrivateStruct' in scope
  !! let privateNestedInsidePrivate = PrivateStruct.PrivateEnumInsidePrivateStruct.a
  !!                                  ^~~~~~~~~~~~~
  !$ error: cannot find 'PrivateStruct' in scope
  !! let automaticNestedInsidePrivate = PrivateStruct.AutomaticEnumInsidePrivateStruct.a
  !!                                    ^~~~~~~~~~~~~
  ```
-->

<!--
  - test: `nestedTypes_Module2_Public`

  ```swifttest
  // this is the only expected to succeed within the second module
  -> import nestedTypes_Module1
  -> let publicNestedInsidePublic = PublicStruct.PublicEnumInsidePublicStruct.a
  ```
-->

<!--
  - test: `nestedTypes_Module2_InternalAndPrivate`

  ```swifttest
  // these are all expected to fail, because they're private or internal to the other module
  -> import nestedTypes_Module1
  -> let internalNestedInsidePublic = PublicStruct.InternalEnumInsidePublicStruct.a
  -> let automaticNestedInsidePublic = PublicStruct.AutomaticEnumInsidePublicStruct.a
  -> let privateNestedInsidePublic = PublicStruct.PrivateEnumInsidePublicStruct.a

  -> let internalNestedInsideInternal = InternalStruct.InternalEnumInsideInternalStruct.a
  -> let automaticNestedInsideInternal = InternalStruct.AutomaticEnumInsideInternalStruct.a
  -> let privateNestedInsideInternal = InternalStruct.PrivateEnumInsideInternalStruct.a

  -> let privateNestedInsidePrivate = PrivateStruct.PrivateEnumInsidePrivateStruct.a
  -> let automaticNestedInsidePrivate = PrivateStruct.AutomaticEnumInsidePrivateStruct.a

  !$ error: 'InternalEnumInsidePublicStruct' is inaccessible due to 'internal' protection level
  !! let internalNestedInsidePublic = PublicStruct.InternalEnumInsidePublicStruct.a
  !!                                               ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  !$ note: 'InternalEnumInsidePublicStruct' declared here
  !! internal enum InternalEnumInsidePublicStruct {
  !!               ^
  !$ error: 'AutomaticEnumInsidePublicStruct' is inaccessible due to 'internal' protection level
  !! let automaticNestedInsidePublic = PublicStruct.AutomaticEnumInsidePublicStruct.a
  !!                                                ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  !$ note: 'AutomaticEnumInsidePublicStruct' declared here
  !! internal enum AutomaticEnumInsidePublicStruct {
  !!               ^
  !$ error: 'PrivateEnumInsidePublicStruct' is inaccessible due to 'private' protection level
  !! let privateNestedInsidePublic = PublicStruct.PrivateEnumInsidePublicStruct.a
  !!                                              ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  !$ note: 'PrivateEnumInsidePublicStruct' declared here
  !! private enum PrivateEnumInsidePublicStruct {
  !!              ^
  !$ error: cannot find 'InternalStruct' in scope
  !! let internalNestedInsideInternal = InternalStruct.InternalEnumInsideInternalStruct.a
  !!                                    ^~~~~~~~~~~~~~
  !$ error: cannot find 'InternalStruct' in scope
  !! let automaticNestedInsideInternal = InternalStruct.AutomaticEnumInsideInternalStruct.a
  !!                                     ^~~~~~~~~~~~~~
  !$ error: cannot find 'InternalStruct' in scope
  !! let privateNestedInsideInternal = InternalStruct.PrivateEnumInsideInternalStruct.a
  !!                                   ^~~~~~~~~~~~~~
  !$ error: cannot find 'PrivateStruct' in scope
  !! let privateNestedInsidePrivate = PrivateStruct.PrivateEnumInsidePrivateStruct.a
  !!                                  ^~~~~~~~~~~~~
  !$ error: cannot find 'PrivateStruct' in scope
  !! let automaticNestedInsidePrivate = PrivateStruct.AutomaticEnumInsidePrivateStruct.a
  !!                                    ^~~~~~~~~~~~~
  ```
-->

## Criando subclasses

Você pode criar uma subclasse de qualquer classe
que possa ser acessada no contexto de acesso atual
e que esteja definida no mesmo módulo da subclasse.
Você também pode criar uma subclasse de qualquer classe open
definida em outro módulo.
Uma subclasse não pode ter um nível de acesso mais alto que o da sua superclasse ---
por exemplo, você não pode escrever uma subclasse public de uma superclasse internal.

Além disso,
para classes definidas no mesmo módulo,
você pode sobrescrever qualquer membro de classe
(método, propriedade, inicializador ou subscript)
que esteja visível em determinado contexto de acesso.
Para classes definidas em outro módulo,
você pode sobrescrever qualquer membro de classe open.

Um override pode tornar um membro de classe herdado mais acessível do que a versão da superclasse.
No exemplo abaixo, a classe `A` é uma classe public com um método `someMethod()` file-private.
A classe `B` é subclasse de `A`, com nível de acesso reduzido para “internal”.
Mesmo assim, a classe `B` fornece um override de `someMethod()`
com nível de acesso “internal”, que é *mais alto* que
a implementação original de `someMethod()`:

```swift
public class A {
    fileprivate func someMethod() {}
}

internal class B: A {
    override internal func someMethod() {}
}
```

<!--
  - test: `subclassingNoCall`

  ```swifttest
  -> public class A {
        fileprivate func someMethod() {}
     }

  -> internal class B: A {
        override internal func someMethod() {}
     }
  ```
-->

É até válido um membro de subclasse chamar
um membro da superclasse que tenha permissões de acesso mais restritas que o membro da subclasse,
desde que a chamada ao membro da superclasse aconteça dentro
de um nível de acesso permitido
(ou seja, dentro do mesmo arquivo-fonte da superclasse, no caso de uma chamada a um membro file-private,
ou dentro do mesmo módulo da superclasse, no caso de uma chamada a um membro internal):

```swift
public class A {
    fileprivate func someMethod() {}
}

internal class B: A {
    override internal func someMethod() {
        super.someMethod()
    }
}
```

<!--
  - test: `subclassingWithCall`

  ```swifttest
  -> public class A {
        fileprivate func someMethod() {}
     }

  -> internal class B: A {
        override internal func someMethod() {
           super.someMethod()
        }
     }
  ```
-->

Como a superclasse `A` e a subclasse `B` são definidas no mesmo arquivo-fonte,
é válido que a implementação de `someMethod()` em `B` chame
`super.someMethod()`.

## Constantes, variáveis, propriedades e subscripts

Uma constante, variável ou propriedade não pode ser mais pública que o tipo dela.
Não é válido escrever, por exemplo, uma propriedade public com um tipo private.
Da mesma forma, um subscript não pode ser mais público que seu tipo de índice ou seu tipo de retorno.

Se uma constante, variável, propriedade ou subscript usar um tipo private,
a constante, variável, propriedade ou subscript também precisa ser marcada como `private`:

```swift
private var privateInstance = SomePrivateClass()
```

<!--
  - test: `accessControl`

  ```swifttest
  -> private var privateInstance = SomePrivateClass()
  ```
-->

<!--
  - test: `useOfPrivateTypeRequiresPrivateModifier`

  ```swifttest
  -> class Scope {  // Need to be in a scope to meaningfully use private (vs fileprivate)
  -> private class SomePrivateClass {}
  -> let privateConstant = SomePrivateClass()
  !! /tmp/swifttest.swift:3:5: error: property must be declared private because its type 'Scope.SomePrivateClass' uses a private type
  !! let privateConstant = SomePrivateClass()
  !! ^
  -> var privateVariable = SomePrivateClass()
  !! /tmp/swifttest.swift:4:5: error: property must be declared private because its type 'Scope.SomePrivateClass' uses a private type
  !! var privateVariable = SomePrivateClass()
  !! ^
  -> class C {
        var privateProperty = SomePrivateClass()
        subscript(index: Int) -> SomePrivateClass {
           return SomePrivateClass()
        }
     }
  -> }  // End surrounding scope
  !! /tmp/swifttest.swift:6:8: error: property must be declared private because its type 'Scope.SomePrivateClass' uses a private type
  !! var privateProperty = SomePrivateClass()
  !! ^
  !! /tmp/swifttest.swift:7:4: error: subscript must be declared private because its element type uses a private type
  !! subscript(index: Int) -> SomePrivateClass {
  !! ^                        ~~~~~~~~~~~~~~~~
  !! /tmp/swifttest.swift:2:15: note: type declared here
  !! private class SomePrivateClass {}
  !! ^
  ```
-->

### Getters e setters

Getters e setters de constantes, variáveis, propriedades e subscripts
recebem automaticamente o mesmo nível de acesso da
constante, variável, propriedade ou subscript a que pertencem.

Você pode dar a um setter um nível de acesso *mais baixo* que o do seu getter correspondente,
para restringir o escopo de leitura e escrita dessa variável, propriedade ou subscript.
Você atribui um nível de acesso mais baixo escrevendo
`fileprivate(set)`, `private(set)`, `internal(set)` ou `package(set)`
antes da palavra-chave `var` ou `subscript`.

> Nota: Esta regra se aplica tanto a propriedades armazenadas quanto a propriedades computadas.
> Mesmo que você não escreva um getter e um setter explícitos para uma propriedade armazenada,
> o Swift ainda sintetiza um getter e um setter implícitos para dar acesso
> ao armazenamento de apoio da propriedade.
> Use `fileprivate(set)`, `private(set)`, `internal(set)` e `package(set)`
> para alterar o nível de acesso
> desse setter sintetizado exatamente da mesma forma que faria com um setter explícito
> em uma propriedade computada.

O exemplo abaixo define uma struct chamada `TrackedString`,
que registra quantas vezes uma propriedade string é modificada:

```swift
struct TrackedString {
    private(set) var numberOfEdits = 0
    var value: String = "" {
        didSet {
            numberOfEdits += 1
        }
    }
}
```

<!--
  - test: `reducedSetterScope, reducedSetterScope_error`

  ```swifttest
  -> struct TrackedString {
        private(set) var numberOfEdits = 0
        var value: String = "" {
           didSet {
              numberOfEdits += 1
           }
        }
     }
  ```
-->

A struct `TrackedString` define uma propriedade armazenada de string chamada `value`,
com valor inicial `""` (uma string vazia).
A struct também define uma propriedade armazenada de inteiro chamada `numberOfEdits`,
que é usada para contar quantas vezes `value` é modificada.
Esse controle de modificações é implementado com
um observador de propriedade `didSet` na propriedade `value`,
que incrementa `numberOfEdits` toda vez que `value` recebe um novo valor.

A struct `TrackedString` e a propriedade `value`
não fornecem um modificador explícito de nível de acesso,
por isso ambas recebem o nível de acesso padrão, `internal`.
No entanto, o nível de acesso da propriedade `numberOfEdits`
é marcado com o modificador `private(set)`
para indicar que
o getter da propriedade continua com o nível de acesso padrão, `internal`,
mas a propriedade só pode receber valores a partir de
código que faz parte da struct `TrackedString`.
Isso permite que `TrackedString` modifique a propriedade `numberOfEdits` internamente,
mas a apresente como uma propriedade somente leitura
quando usada fora da definição da struct.

<!--
  - test: `reducedSetterScope_error`

  ```swifttest
  -> extension TrackedString {
         mutating func f() { numberOfEdits += 1 }
     }
  // check that we can't set its value with from the same file
  -> var s = TrackedString()
  -> let resultA: Void = { s.numberOfEdits += 1 }()
  !! /tmp/swifttest.swift:13:39: error: left side of mutating operator isn't mutable: 'numberOfEdits' setter is inaccessible
  !! let resultA: Void = { s.numberOfEdits += 1 }()
  !!                       ~~~~~~~~~~~~~~~ ^
  ```
-->

<!--
  The assertion above must be compiled because of a REPL bug
  <rdar://problem/54089342> REPL fails to enforce private(set) on struct property
-->

Se você criar uma instância de `TrackedString` e modificar seu valor string algumas vezes,
verá o valor da propriedade `numberOfEdits` ser atualizado para refletir o número de modificações:

```swift
var stringToEdit = TrackedString()
stringToEdit.value = "This string will be tracked."
stringToEdit.value += " This edit will increment numberOfEdits."
stringToEdit.value += " So will this one."
print("The number of edits is \(stringToEdit.numberOfEdits)")
// Prints "The number of edits is 3".
```

<!--
  - test: `reducedSetterScope`

  ```swifttest
  -> var stringToEdit = TrackedString()
  -> stringToEdit.value = "This string will be tracked."
  -> stringToEdit.value += " This edit will increment numberOfEdits."
  -> stringToEdit.value += " So will this one."
  -> print("The number of edits is \(stringToEdit.numberOfEdits)")
  <- The number of edits is 3
  ```
-->

Embora você possa consultar o valor atual da propriedade `numberOfEdits`
de dentro de outro arquivo-fonte,
não pode *modificar* a propriedade a partir de outro arquivo-fonte.
Essa restrição protege os detalhes de implementação
da funcionalidade de rastreamento de edições de `TrackedString`,
ao mesmo tempo que oferece acesso prático a um aspecto dessa funcionalidade.

Observe que você pode atribuir um nível de acesso explícito tanto
para um getter quanto para um setter, se necessário.
O exemplo abaixo mostra uma versão da struct `TrackedString`
em que a struct é definida com nível de acesso explícito public.
Os membros da struct (incluindo a propriedade `numberOfEdits`)
têm, portanto, nível de acesso `internal` por padrão.
Você pode fazer o getter da propriedade `numberOfEdits` ser public,
e o setter ser private,
combinando os modificadores de nível de acesso `public` e `private(set)`:

```swift
public struct TrackedString {
    public private(set) var numberOfEdits = 0
    public var value: String = "" {
        didSet {
            numberOfEdits += 1
        }
    }
    public init() {}
}
```

<!--
  - test: `reducedSetterScopePublic`

  ```swifttest
  -> public struct TrackedString {
        public private(set) var numberOfEdits = 0
        public var value: String = "" {
           didSet {
              numberOfEdits += 1
           }
        }
        public init() {}
     }
  ```
-->

<!--
  - test: `reducedSetterScopePublic_Module1_Allowed, reducedSetterScopePublic_Module1_NotAllowed`

  ```swifttest
  -> public struct TrackedString {
        public private(set) var numberOfEdits = 0
        public var value: String = "" {
           didSet {
              numberOfEdits += 1
           }
        }
        public init() {}
     }
  ```
-->

<!--
  - test: `reducedSetterScopePublic_Module1_Allowed`

  ```swifttest
  // check that we can retrieve its value with the public getter from another file in the same module
  -> var stringToEdit_Module1B = TrackedString()
  -> let resultB = stringToEdit_Module1B.numberOfEdits
  ```
-->

<!--
  - test: `reducedSetterScopePublic_Module1_NotAllowed`

  ```swifttest
  // check that we can't set its value from another file in the same module
  -> var stringToEdit_Module1C = TrackedString()
  -> let resultC: Void = { stringToEdit_Module1C.numberOfEdits += 1 }()
  !$ error: left side of mutating operator isn't mutable: 'numberOfEdits' setter is inaccessible
  !! let resultC: Void = { stringToEdit_Module1C.numberOfEdits += 1 }()
  !!                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ^
  ```
-->

<!--
  - test: `reducedSetterScopePublic_Module2`

  ```swifttest
  // check that we can retrieve its value with the public getter from a different module
  -> import reducedSetterScopePublic_Module1_Allowed
  -> var stringToEdit_Module2 = TrackedString()
  -> let result2Read = stringToEdit_Module2.numberOfEdits
  // check that we can't change its value from another module
  -> let result2Write: Void = { stringToEdit_Module2.numberOfEdits += 1 }()
  !$ error: left side of mutating operator isn't mutable: 'numberOfEdits' setter is inaccessible
  !! let result2Write: Void = { stringToEdit_Module2.numberOfEdits += 1 }()
  !!                            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ^
  ```
-->

## Inicializadores

Inicializadores personalizados podem receber um nível de acesso menor ou igual
ao do tipo que eles inicializam.
A única exceção são os inicializadores required
(como definidos em <doc:Initialization#Required-Initializers>).
Um inicializador required deve ter o mesmo nível de acesso da classe a que pertence.

Assim como ocorre com parâmetros de funções e métodos,
os tipos dos parâmetros de um inicializador não podem ser mais private que
o nível de acesso do próprio inicializador.

### Inicializadores padrão

Como descrito em <doc:Initialization#Default-Initializers>,
o Swift fornece automaticamente um *inicializador padrão* sem argumentos
para qualquer struct ou classe base
que forneça valores padrão para todas as suas propriedades
e não forneça pelo menos um inicializador próprio.

Um inicializador padrão tem o mesmo nível de acesso do tipo que ele inicializa,
a menos que esse tipo seja definido como `public`.
Para um tipo definido como `public`,
o inicializador padrão é considerado internal.
Se você quiser que um tipo public possa ser inicializado com um inicializador sem argumentos
quando usado em outro módulo,
você precisa fornecer explicitamente um inicializador public sem argumentos
como parte da definição do tipo.

### Inicializadores memberwise padrão para structs

O inicializador memberwise padrão de uma struct é considerado private
se alguma das propriedades armazenadas da struct for private.
Do mesmo modo, se alguma das propriedades armazenadas da struct for file-private,
o inicializador é file-private.
Caso contrário, o inicializador tem nível de acesso internal.

Assim como no caso do inicializador padrão acima,
se você quiser que uma struct public possa ser inicializada com um inicializador memberwise
quando usada em outro módulo,
você precisa fornecer explicitamente um inicializador memberwise public como parte da definição do tipo.

## Protocolos

Se você quiser atribuir um nível de acesso explícito a um tipo de protocolo,
faça isso no ponto em que você define o protocolo.
Isso permite criar protocolos que só podem ser adotados dentro
de um certo contexto de acesso.

O nível de acesso de cada requisito dentro da definição de um protocolo
é definido automaticamente como o mesmo nível de acesso do protocolo.
Você não pode definir um requisito de protocolo com um nível de acesso
diferente do protocolo ao qual ele pertence.
Isso garante que todos os requisitos do protocolo fiquem visíveis
em qualquer tipo que adote o protocolo.

<!--
  - test: `protocolRequirementsCannotBeDifferentThanTheProtocol`

  ```swifttest
  -> public protocol PublicProtocol {
        public var publicProperty: Int { get }
        internal var internalProperty: Int { get }
        fileprivate var filePrivateProperty: Int { get }
        private var privateProperty: Int { get }
     }
  !$ error: 'public' modifier cannot be used in protocols
  !! public var publicProperty: Int { get }
  !! ^~~~~~~
  !!-
  !$ note: protocol requirements implicitly have the same access as the protocol itself
  !! public var publicProperty: Int { get }
  !! ^
  !$ error: 'internal' modifier cannot be used in protocols
  !! internal var internalProperty: Int { get }
  !! ^~~~~~~~~
  !!-
  !$ note: protocol requirements implicitly have the same access as the protocol itself
  !! internal var internalProperty: Int { get }
  !! ^
  !$ error: 'fileprivate' modifier cannot be used in protocols
  !! fileprivate var filePrivateProperty: Int { get }
  !! ^~~~~~~~~~~~
  !!-
  !$ note: protocol requirements implicitly have the same access as the protocol itself
  !! fileprivate var filePrivateProperty: Int { get }
  !! ^
  !$ error: 'private' modifier cannot be used in protocols
  !! private var privateProperty: Int { get }
  !! ^~~~~~~~
  !!-
  !$ note: protocol requirements implicitly have the same access as the protocol itself
  !! private var privateProperty: Int { get }
  !! ^
  ```
-->

> Nota: Se você definir um protocolo public,
> os requisitos do protocolo exigem um nível de acesso public
> para esses requisitos quando forem implementados.
> Esse comportamento é diferente dos outros tipos,
> em que a definição de um tipo public implica
> um nível de acesso internal para os membros do tipo.

<!--
  - test: `protocols_Module1, protocols_Module1_PublicAndInternal, protocols_Module1_Private`

  ```swifttest
  -> public protocol PublicProtocol {
        var publicProperty: Int { get }
        func publicMethod()
     }
  -> internal protocol InternalProtocol {
        var internalProperty: Int { get }
        func internalMethod()
     }
  -> fileprivate protocol FilePrivateProtocol {
        var filePrivateProperty: Int { get }
        func filePrivateMethod()
     }
  -> private protocol PrivateProtocol {
        var privateProperty: Int { get }
        func privateMethod()
     }
  ```
-->

<!--
  - test: `protocols_Module1_PublicAndInternal`

  ```swifttest
  // these should all be allowed without problem
  -> public class PublicClassConformingToPublicProtocol: PublicProtocol {
        public var publicProperty = 0
        public func publicMethod() {}
     }
  -> internal class InternalClassConformingToPublicProtocol: PublicProtocol {
        var publicProperty = 0
        func publicMethod() {}
     }
  -> private class PrivateClassConformingToPublicProtocol: PublicProtocol {
        var publicProperty = 0
        func publicMethod() {}
     }

  -> public class PublicClassConformingToInternalProtocol: InternalProtocol {
        var internalProperty = 0
        func internalMethod() {}
     }
  -> internal class InternalClassConformingToInternalProtocol: InternalProtocol {
        var internalProperty = 0
        func internalMethod() {}
     }
  -> private class PrivateClassConformingToInternalProtocol: InternalProtocol {
        var internalProperty = 0
        func internalMethod() {}
     }
  ```
-->

<!--
  - test: `protocols_Module1_Private`

  ```swifttest
  // these will fail, because FilePrivateProtocol isn't visible outside of its file
  -> public class PublicClassConformingToFilePrivateProtocol: FilePrivateProtocol {
        var filePrivateProperty = 0
        func filePrivateMethod() {}
     }
  !$ error: cannot find type 'FilePrivateProtocol' in scope
  !! public class PublicClassConformingToFilePrivateProtocol: FilePrivateProtocol {
  !! ^~~~~~~~~~~~~~~~~~~

  // these will fail, because PrivateProtocol isn't visible outside of its file
  -> public class PublicClassConformingToPrivateProtocol: PrivateProtocol {
        var privateProperty = 0
        func privateMethod() {}
     }
  !$ error: cannot find type 'PrivateProtocol' in scope
  !! public class PublicClassConformingToPrivateProtocol: PrivateProtocol {
  !! ^~~~~~~~~~~~~~~
  ```
-->

<!--
  - test: `protocols_Module2_Public`

  ```swifttest
  // these should all be allowed without problem
  -> import protocols_Module1
  -> public class PublicClassConformingToPublicProtocol: PublicProtocol {
        public var publicProperty = 0
        public func publicMethod() {}
     }
  -> internal class InternalClassConformingToPublicProtocol: PublicProtocol {
        var publicProperty = 0
        func publicMethod() {}
     }
  -> private class PrivateClassConformingToPublicProtocol: PublicProtocol {
        var publicProperty = 0
        func publicMethod() {}
     }
  ```
-->

<!--
  - test: `protocols_Module2_InternalAndPrivate`

  ```swifttest
  // these will all fail, because InternalProtocol, FilePrivateProtocol, and PrivateProtocol
  // aren't visible to other modules
  -> import protocols_Module1
  -> public class PublicClassConformingToInternalProtocol: InternalProtocol {
        var internalProperty = 0
        func internalMethod() {}
     }
  -> public class PublicClassConformingToFilePrivateProtocol: FilePrivateProtocol {
        var filePrivateProperty = 0
        func filePrivateMethod() {}
     }
  -> public class PublicClassConformingToPrivateProtocol: PrivateProtocol {
        var privateProperty = 0
        func privateMethod() {}
     }
  !$ error: cannot find type 'InternalProtocol' in scope
  !! public class PublicClassConformingToInternalProtocol: InternalProtocol {
  !! ^~~~~~~~~~~~~~~~
  !$ error: cannot find type 'FilePrivateProtocol' in scope
  !! public class PublicClassConformingToFilePrivateProtocol: FilePrivateProtocol {
  !! ^~~~~~~~~~~~~~~~~~~
  !$ error: cannot find type 'PrivateProtocol' in scope
  !! public class PublicClassConformingToPrivateProtocol: PrivateProtocol {
  !! ^~~~~~~~~~~~~~~
  ```
-->

### Herança de protocolos

Se você definir um novo protocolo que herda de um protocolo existente,
o novo protocolo pode ter no máximo o mesmo nível de acesso
do protocolo do qual ele herda.
Por exemplo,
você não pode escrever um protocolo public que herde de um protocolo internal.

### Conformidade a protocolos

Um tipo pode estar em conformidade com um protocolo de nível de acesso
mais baixo que o próprio tipo.
Por exemplo, você pode definir um tipo public que pode ser usado em outros módulos,
mas cuja conformidade a um protocolo internal só pode ser usada
dentro do módulo que define esse protocolo.

O contexto em que um tipo está em conformidade com um protocolo específico
é o mínimo entre o nível de acesso do tipo e o nível de acesso do protocolo.
Por exemplo, se um tipo é public, mas um protocolo com o qual ele está em conformidade
é internal, a conformidade do tipo a esse protocolo também é internal.

Ao escrever ou estender um tipo para que ele esteja em conformidade com um protocolo,
você deve garantir que a implementação do tipo de cada requisito do protocolo
tenha pelo menos o mesmo nível de acesso da conformidade do tipo a esse protocolo.
Por exemplo, se um tipo public está em conformidade com um protocolo internal,
a implementação do tipo de cada requisito do protocolo deve ser pelo menos internal.

> Nota: No Swift, assim como no Objective-C, a conformidade a protocolos é global:
> não é possível que um tipo esteja em conformidade com um protocolo de duas formas diferentes
> dentro do mesmo programa.

## Extensions

Você pode estender uma classe, struct ou enum em qualquer contexto de acesso
em que a classe, struct ou enum esteja disponível.
Quaisquer membros de tipo adicionados em uma extension têm o mesmo nível de acesso padrão
que os membros de tipo declarados no tipo original que está sendo estendido.
Se você estender um tipo public ou internal, quaisquer novos membros de tipo que você adicionar
têm nível de acesso padrão internal.
Se você estender um tipo file-private, quaisquer novos membros de tipo que você adicionar
têm nível de acesso padrão file-private.
Se você estender um tipo private, quaisquer novos membros de tipo que você adicionar
têm nível de acesso padrão private.

Como alternativa, você pode marcar uma extension com um modificador de nível de acesso explícito
(por exemplo, `private`) para definir um novo nível de acesso padrão
para todos os membros definidos dentro da extension.
Esse novo padrão ainda pode ser sobrescrito dentro da extension
para membros de tipo individuais.

Você não pode fornecer um modificador de nível de acesso explícito para uma extension
se estiver usando essa extension para adicionar conformidade a um protocolo.
Em vez disso, o nível de acesso do próprio protocolo é usado para definir
o nível de acesso padrão de cada implementação de requisito de protocolo dentro da extension.

<!--
  - test: `extensions_Module1, extensions_Module1_PublicAndInternal, extensions_Module1_Private`

  ```swifttest
  -> public struct PublicStruct {
        public init() {}
        func implicitlyInternalMethodFromStruct() -> Int { return 0 }
     }
  -> extension PublicStruct {
        func implicitlyInternalMethodFromExtension() -> Int { return 0 }
     }
  -> fileprivate extension PublicStruct {
        func filePrivateMethod() -> Int { return 0 }
     }
  -> var publicStructInSameFile = PublicStruct()
  -> let sameFileA = publicStructInSameFile.implicitlyInternalMethodFromStruct()
  -> let sameFileB = publicStructInSameFile.implicitlyInternalMethodFromExtension()
  -> let sameFileC = publicStructInSameFile.filePrivateMethod()
  ```
-->

<!--
  - test: `extensions_Module1_PublicAndInternal`

  ```swifttest
  -> var publicStructInDifferentFile = PublicStruct()
  -> let differentFileA = publicStructInDifferentFile.implicitlyInternalMethodFromStruct()
  -> let differentFileB = publicStructInDifferentFile.implicitlyInternalMethodFromExtension()
  ```
-->

<!--
  - test: `extensions_Module1_Private`

  ```swifttest
  -> var publicStructInDifferentFile = PublicStruct()
  -> let differentFileC = publicStructInDifferentFile.filePrivateMethod()
  !$ error: 'filePrivateMethod' is inaccessible due to 'fileprivate' protection level
  !! let differentFileC = publicStructInDifferentFile.filePrivateMethod()
  !!                                                  ^~~~~~~~~~~~~~~~~
  !$ note: 'filePrivateMethod()' declared here
  !! func filePrivateMethod() -> Int { return 0 }
  !! ^
  ```
-->

<!--
  - test: `extensions_Module2`

  ```swifttest
  -> import extensions_Module1
  -> var publicStructInDifferentModule = PublicStruct()
  -> let differentModuleA = publicStructInDifferentModule.implicitlyInternalMethodFromStruct()
  !$ error: 'implicitlyInternalMethodFromStruct' is inaccessible due to 'internal' protection level
  !! let differentModuleA = publicStructInDifferentModule.implicitlyInternalMethodFromStruct()
  !!                                                      ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  !$ note: 'implicitlyInternalMethodFromStruct()' declared here
  !! internal func implicitlyInternalMethodFromStruct() -> Int
  !!               ^
  -> let differentModuleB = publicStructInDifferentModule.implicitlyInternalMethodFromExtension()
  !$ error: 'implicitlyInternalMethodFromExtension' is inaccessible due to 'internal' protection level
  !! let differentModuleB = publicStructInDifferentModule.implicitlyInternalMethodFromExtension()
  !!                                                      ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  !$ note: 'implicitlyInternalMethodFromExtension()' declared here
  !! internal func implicitlyInternalMethodFromExtension() -> Int
  !!               ^
  -> let differentModuleC = publicStructInDifferentModule.filePrivateMethod()
  !$ error: 'filePrivateMethod' is inaccessible due to 'fileprivate' protection level
  !! let differentModuleC = publicStructInDifferentModule.filePrivateMethod()
  !!                                                      ^~~~~~~~~~~~~~~~~
  !$ note: 'filePrivateMethod()' declared here
  !! fileprivate func filePrivateMethod() -> Int
  !!                  ^
  ```
-->

### Membros private em extensions

Extensions que estão no mesmo arquivo da classe, struct ou enum que elas estendem
se comportam como se o código da extension tivesse sido escrito
como parte da declaração do tipo original.
Por isso, você pode:

- Declarar um membro private na declaração original
  e acessar esse membro a partir de extensions no mesmo arquivo.
- Declarar um membro private em uma extension
  e acessar esse membro a partir de outra extension no mesmo arquivo.
- Declarar um membro private em uma extension
  e acessar esse membro a partir da declaração original no mesmo arquivo.

Esse comportamento significa que você pode usar extensions da mesma forma
para organizar seu código,
independentemente de seus tipos terem ou não entidades private.
Por exemplo, dado o seguinte protocolo simples:

```swift
protocol SomeProtocol {
    func doSomething()
}
```

<!--
  - test: `extensions_privatemembers`

  ```swifttest
  -> protocol SomeProtocol {
         func doSomething()
     }
  ```
-->

Você pode usar uma extension para adicionar conformidade a protocolo, assim:

```swift
struct SomeStruct {
    private var privateVariable = 12
}

extension SomeStruct: SomeProtocol {
    func doSomething() {
        print(privateVariable)
    }
}
```

<!--
  - test: `extensions_privatemembers`

  ```swifttest
  -> struct SomeStruct {
         private var privateVariable = 12
     }

  -> extension SomeStruct: SomeProtocol {
         func doSomething() {
             print(privateVariable)
         }
     }
  >> let s = SomeStruct()
  >> s.doSomething()
  << 12
  ```
-->

## Generics

O nível de acesso de um tipo genérico ou de uma função genérica é
o mínimo entre o nível de acesso do próprio tipo ou função
e o nível de acesso de quaisquer restrições de tipo sobre os parâmetros de tipo dele.

## Aliases de tipo

Os aliases de tipo que você define contam como tipos distintos
para fins de controle de acesso.
Um alias de tipo pode ter nível de acesso menor ou igual ao nível de acesso
do tipo para o qual ele aponta.
Por exemplo, um alias de tipo private pode apontar para um tipo private, file-private,
internal, public ou open, mas um alias de tipo public não pode apontar para
um tipo internal, file-private ou private.

> Nota: Esta regra também vale para aliases de tipo de tipos associados usados para satisfazer conformidades a protocolos.

<!--
  - test: `typeAliases`

  ```swifttest
  -> public struct PublicStruct {}
  -> internal struct InternalStruct {}
  -> private struct PrivateStruct {}

  -> public typealias PublicAliasOfPublicType = PublicStruct
  -> internal typealias InternalAliasOfPublicType = PublicStruct
  -> private typealias PrivateAliasOfPublicType = PublicStruct

  -> public typealias PublicAliasOfInternalType = InternalStruct     // not allowed
  -> internal typealias InternalAliasOfInternalType = InternalStruct
  -> private typealias PrivateAliasOfInternalType = InternalStruct

  -> public typealias PublicAliasOfPrivateType = PrivateStruct       // not allowed
  -> internal typealias InternalAliasOfPrivateType = PrivateStruct   // not allowed
  -> private typealias PrivateAliasOfPrivateType = PrivateStruct

  !$ error: type alias cannot be declared public because its underlying type uses an internal type
  !! public typealias PublicAliasOfInternalType = InternalStruct     // not allowed
  !! ^                           ~~~~~~~~~~~~~~
  !$ note: type declared here
  !! internal struct InternalStruct {}
  !! ^
  !$ error: type alias cannot be declared public because its underlying type uses a private type
  !! public typealias PublicAliasOfPrivateType = PrivateStruct       // not allowed
  !! ^                          ~~~~~~~~~~~~~
  !$ note: type declared here
  !! private struct PrivateStruct {}
  !! ^
  !$ error: type alias cannot be declared internal because its underlying type uses a private type
  !! internal typealias InternalAliasOfPrivateType = PrivateStruct   // not allowed
  !! ^                            ~~~~~~~~~~~~~
  !$ note: type declared here
  !! private struct PrivateStruct {}
  !! ^
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
