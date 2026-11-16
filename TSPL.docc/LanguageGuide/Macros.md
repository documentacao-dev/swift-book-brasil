# Macros

Use macros para gerar código em tempo de compilação.

Macros transformam o seu código-fonte quando você compila,
permitindo evitar escrever código repetitivo à mão.
Durante a compilação,
o Swift expande todas as macros do seu código
antes de construir o código normalmente.

![A diagram showing an overview of macro expansion.  On the left, a stylized representation of Swift code.  On the right, the same code with several lines added by the macro.](macro-expansion)

Expandir uma macro é sempre uma operação aditiva:
macros acrescentam código novo,
mas nunca apagam nem modificam o código existente.

Tanto a entrada de uma macro quanto a saída da expansão de macro
são verificadas para garantir que são código Swift sintaticamente válido.
Da mesma forma, os valores que você passa para uma macro
e os valores no código gerado por uma macro
são verificados para garantir que têm os tipos corretos.
Além disso,
se a implementação da macro encontrar um erro ao expandi-la,
o compilador trata isso como um erro de compilação.
Essas garantias facilitam raciocinar sobre código que usa macros,
e facilitam identificar problemas,
como usar uma macro incorretamente
ou uma implementação de macro com bug.

O Swift tem dois tipos de macro:

- *Macros independentes* (*freestanding macros*) aparecem sozinhas,
  sem estar anexadas a uma declaração.

- *Macros anexadas* (*attached macros*) modificam a declaração à qual estão anexadas.

Você chama macros anexadas e macros independentes de forma um pouco diferente,
mas as duas seguem o mesmo modelo de expansão de macro,
e você as implementa com a mesma abordagem.
As seções a seguir descrevem os dois tipos com mais detalhes.

## Macros independentes

Para chamar uma macro independente,
você escreve um sinal de número (`#`) antes do nome dela,
e escreve os argumentos da macro entre parênteses depois do nome.
Por exemplo:

```swift
func myFunction() {
    print("Currently running \(#function)")
    #warning("Something's wrong")
}
```

Na primeira linha,
`#function` chama a macro [`function()`][] da biblioteca padrão do Swift.
Quando você compila esse código,
o Swift chama a implementação dessa macro,
que substitui `#function` pelo nome da função atual.
Quando você executa esse código e chama `myFunction()`,
ele imprime "Currently running myFunction()".
Na segunda linha,
`#warning` chama a macro [`warning(_:)`][] da biblioteca padrão do Swift
para produzir um aviso personalizado em tempo de compilação.

[`function()`]: https://developer.apple.com/documentation/swift/function()
[`warning(_:)`]: https://developer.apple.com/documentation/swift/warning(_:)

Macros independentes podem produzir um valor, como `#function` faz,
ou podem executar uma ação em tempo de compilação, como `#warning` faz.
<!-- SE-0397: or they can generate new declarations.  -->

## Macros anexadas

Para chamar uma macro anexada,
você escreve um arroba (`@`) antes do nome dela,
e escreve os argumentos da macro entre parênteses depois do nome.

Macros anexadas modificam a declaração à qual estão anexadas.
Elas acrescentam código a essa declaração,
como definir um novo método ou adicionar conformidade a um protocolo.

Por exemplo, considere o código a seguir,
que não usa macros:

```swift
struct SundaeToppings: OptionSet {
    let rawValue: Int
    static let nuts = SundaeToppings(rawValue: 1 << 0)
    static let cherry = SundaeToppings(rawValue: 1 << 1)
    static let fudge = SundaeToppings(rawValue: 1 << 2)
}
```

Nesse código,
cada uma das opções no tipo `SundaeToppings`
inclui uma chamada ao inicializador,
o que é repetitivo e manual.
Seria fácil cometer um erro ao adicionar uma opção nova,
como digitar o número errado no fim da linha.

Aqui está uma versão desse código que usa uma macro:

```swift
@OptionSet<Int>
struct SundaeToppings {
    private enum Options: Int {
        case nuts
        case cherry
        case fudge
    }
}
```

Essa versão de `SundaeToppings` chama uma macro `@OptionSet`.
A macro lê a lista de casos do enum privado,
gera a lista de constantes para cada opção
e adiciona a conformidade com o protocolo [`OptionSet`][].

[`OptionSet`]: https://developer.apple.com/documentation/swift/optionset

<!--
When the @OptionSet macro comes back, change both links back:

[`@OptionSet`]: https://developer.apple.com/documentation/swift/optionset-swift.macro
[`OptionSet`]: https://developer.apple.com/documentation/swift/optionset-swift.protocol
-->

Para comparar,
veja como fica a versão expandida da macro `@OptionSet`.
Você não escreve este código,
e só o veria se pedisse explicitamente ao Swift
para mostrar a expansão da macro.

```swift
struct SundaeToppings {
    private enum Options: Int {
        case nuts
        case cherry
        case fudge
    }

    typealias RawValue = Int
    var rawValue: RawValue
    init() { self.rawValue = 0 }
    init(rawValue: RawValue) { self.rawValue = rawValue }
    static let nuts: Self = Self(rawValue: 1 << Options.nuts.rawValue)
    static let cherry: Self = Self(rawValue: 1 << Options.cherry.rawValue)
    static let fudge: Self = Self(rawValue: 1 << Options.fudge.rawValue)
}
extension SundaeToppings: OptionSet { }
```

Todo o código depois do enum privado
vem da macro `@OptionSet`.
A versão de `SundaeToppings`
que usa uma macro para gerar todas as propriedades estáticas
é mais fácil de ler e de manter
do que a versão escrita manualmente, mais acima.

## Declarações de macro

Na maior parte do código Swift,
quando você implementa um símbolo, como uma função ou um tipo,
não existe uma declaração separada.
No entanto, para macros, a declaração e a implementação são separadas.
A declaração de uma macro contém o nome dela,
os parâmetros que ela recebe,
onde ela pode ser usada
e que tipo de código ela gera.
A implementação de uma macro contém o código
que expande a macro gerando código Swift.

Você introduz a declaração de uma macro com a palavra-chave `macro`.
Por exemplo,
aqui está parte da declaração da macro `@OptionSet`
usada no exemplo anterior:

```swift
public macro OptionSet<RawType>() =
        #externalMacro(module: "SwiftMacros", type: "OptionSetMacro")
```

A primeira linha
especifica o nome da macro e os argumentos dela ---
o nome é `OptionSet`, e ela não recebe nenhum argumento.
A segunda linha
usa a macro [`externalMacro(module:type:)`][] da biblioteca padrão do Swift
para indicar onde está localizada a implementação da macro.
Nesse caso,
o módulo `SwiftMacros`
contém um tipo chamado `OptionSetMacro`,
que implementa a macro `@OptionSet`.

[`externalMacro(module:type:)`]: https://developer.apple.com/documentation/swift/externalmacro(module:type:)

Como `OptionSet` é uma macro anexada,
o nome dela usa upper camel case,
como os nomes de structs e classes.
Macros independentes têm nomes em lower camel case,
como os nomes de variáveis e funções.

> Nota:
> Macros são sempre declaradas como `public`.
> Como o código que declara uma macro
> está em um módulo diferente do código que usa essa macro,
> não há onde aplicar uma macro não pública.

Uma declaração de macro define os *papéis* da macro ---
os lugares no código-fonte onde ela pode ser chamada,
e os tipos de código que ela pode gerar.
Toda macro tem um ou mais papéis,
que você escreve como parte dos atributos
no início da declaração da macro.
Aqui está um pouco mais da declaração de `@OptionSet`,
incluindo os atributos dos papéis dela:

```swift
@attached(member)
@attached(extension, conformances: OptionSet)
public macro OptionSet<RawType>() =
        #externalMacro(module: "SwiftMacros", type: "OptionSetMacro")
```

O atributo `@attached` aparece duas vezes nessa declaração,
uma vez para cada papel da macro.
O primeiro uso, `@attached(member)`, indica que a macro
adiciona novos membros ao tipo ao qual é aplicada.
A macro `@OptionSet` adiciona um inicializador `init(rawValue:)`
exigido pelo protocolo `OptionSet`,
além de alguns outros membros.
O segundo uso, `@attached(extension, conformances: OptionSet)`,
informa que `@OptionSet`
adiciona conformidade ao protocolo `OptionSet`.
A macro `@OptionSet`
estende o tipo ao qual você aplica a macro,
para adicionar conformidade ao protocolo `OptionSet`.

Para uma macro independente,
você escreve o atributo `@freestanding` para especificar o papel dela:

```swift
@freestanding(expression)
public macro line<T: ExpressibleByIntegerLiteral>() -> T =
        /* ... location of the macro implementation... */
```

<!--
Elided the implementation of #line above
because it's a compiler built-in:

public macro line<T: ExpressibleByIntegerLiteral>() -> T = Builtin.LineMacro
-->

A macro `#line` acima tem o papel `expression`.
Uma macro de expressão produz um valor,
ou executa uma ação em tempo de compilação,
como gerar um aviso.

Além do papel da macro,
a declaração dela fornece informação sobre
os nomes dos símbolos que a macro gera.
Quando a declaração de uma macro traz uma lista de nomes,
o Swift garante que ela produz apenas declarações que usam esses nomes,
o que ajuda a entender e depurar o código gerado.
Aqui está a declaração completa de `@OptionSet`:

```swift
@attached(member, names: named(RawValue), named(rawValue),
        named(`init`), arbitrary)
@attached(extension, conformances: OptionSet)
public macro OptionSet<RawType>() =
        #externalMacro(module: "SwiftMacros", type: "OptionSetMacro")
```

Na declaração acima,
o `@attached(member)` inclui, depois do rótulo `names:`,
argumentos para cada um dos símbolos que a macro `@OptionSet` gera.
A macro adiciona declarações para os símbolos chamados
`RawValue`, `rawValue` e `init` ---
como esses nomes são conhecidos de antemão,
a declaração da macro os lista explicitamente.

A declaração da macro também inclui `arbitrary` depois da lista de nomes,
o que permite que a macro gere declarações
cujos nomes não são conhecidos até você usar a macro.
Por exemplo,
quando a macro `@OptionSet` é aplicada a `SundaeToppings`, acima,
ela gera propriedades de tipo que correspondem aos casos do enum,
`nuts`, `cherry` e `fudge`.

Para mais informações,
incluindo a lista completa de papéis de macro,
veja <doc:Attributes#attached> e <doc:Attributes#freestanding>
em <doc:Attributes>.

## Expansão de macro

Ao compilar código Swift que usa macros,
o compilador chama a implementação das macros para expandi-las.

![Diagram showing the four steps of expanding macros.  The input is Swift source code.  This becomes a tree, representing the code's structure.  The macro implementation adds branches to the tree.  The result is Swift source with additional code.](macro-expansion-full)

Especificamente, o Swift faz a expansão de macros da seguinte forma:

1. O compilador lê o código,
   criando uma representação em memória da sintaxe.

1. O compilador envia parte dessa representação em memória
   para a implementação da macro,
   que faz a expansão.

1. O compilador substitui a chamada da macro pela forma expandida.

1. O compilador continua a compilação,
   usando o código-fonte expandido.

Para ver as etapas específicas, considere o seguinte:

```swift
let magicNumber = #fourCharacterCode("ABCD")
```

A macro `#fourCharacterCode` recebe uma string com quatro caracteres
e retorna um inteiro de 32 bits sem sinal
que corresponde aos valores ASCII dos caracteres da string unidos.
Alguns formatos de arquivo usam inteiros assim para identificar dados,
porque são compactos e ainda assim legíveis em um depurador.
A seção <doc:Macros#Implementing-a-Macro> abaixo
mostra como implementar essa macro.

Para expandir as macros no código acima,
o compilador lê o arquivo Swift
e cria uma representação em memória desse código
conhecida como *árvore de sintaxe abstrata* (*abstract syntax tree*, ou AST).
A AST torna explícita a estrutura do código,
o que facilita escrever código que interage com essa estrutura ---
como um compilador ou a implementação de uma macro.
Aqui está uma representação da AST do código acima,
um pouco simplificada, omitindo alguns detalhes extras:

![A tree diagram, with a constant as the root element.  The constant has a name, magic number, and a value.  The constant's value is a macro call.  The macro call has a name, fourCharacterCode, and arguments.  The argument is a string literal, ABCD.](macro-ast-original)

O diagrama acima mostra como a estrutura desse código
é representada em memória.
Cada elemento da AST
corresponde a uma parte do código-fonte.
O elemento "Constant declaration"
tem dois elementos filhos,
que representam as duas partes de uma declaração de constante:
o nome e o valor.
O elemento "Macro call" tem elementos filhos
que representam o nome da macro
e a lista de argumentos passados à macro.

Como parte da construção dessa AST,
o compilador verifica que o código-fonte é Swift válido.
Por exemplo, `#fourCharacterCode` recebe um único argumento,
que precisa ser uma string.
Se você tentasse passar um argumento inteiro,
ou esquecesse a aspa (`"`) no fim do literal de string,
receberia um erro nesse ponto do processo.

O compilador encontra os lugares no código onde você chama uma macro,
e carrega o binário externo que implementa essas macros.
Para cada chamada de macro,
o compilador passa parte da AST para a implementação dessa macro.
Aqui está uma representação dessa AST parcial:

![A tree diagram, with a macro call as the root element.  The macro call has a name, fourCharacterCode, and arguments.  The argument is a string literal, ABCD.](macro-ast-input)

A implementação da macro `#fourCharacterCode`
lê essa AST parcial como entrada ao expandir a macro.
A implementação de uma macro
opera apenas sobre a AST parcial que recebe como entrada,
o que significa que uma macro sempre se expande do mesmo modo,
independentemente do código que vem antes e depois dela.
Essa limitação ajuda a tornar a expansão de macro mais fácil de entender,
e ajuda seu código a compilar mais rápido,
porque o Swift pode evitar expandir macros que não mudaram.
<!-- TODO TR: Confirm -->
O Swift ajuda os autores de macros a não ler acidentalmente outras entradas,
restringindo o código que implementa macros:

- A AST passada a uma implementação de macro
  contém apenas os elementos da AST que representam a macro,
  e não qualquer código que venha antes ou depois dela.

- A implementação da macro roda em um ambiente em sandbox
  que a impede de acessar o sistema de arquivos ou a rede.

Além dessas salvaguardas,
o autor da macro é responsável por não ler nem modificar nada
fora das entradas da macro.
Por exemplo, a expansão de uma macro não pode depender da hora do dia atual.

A implementação de `#fourCharacterCode`
gera uma nova AST contendo o código expandido.
Aqui está o que esse código devolve ao compilador:

![A tree diagram with the integer literal 1145258561 of type UInt32.](macro-ast-output)

Quando o compilador recebe essa expansão,
ele substitui o elemento da AST que contém a chamada da macro
pelo elemento que contém a expansão da macro.
Depois da expansão de macro,
o compilador verifica de novo que o programa
continua sendo Swift sintaticamente válido
e que todos os tipos estão corretos.
Isso produz uma AST final que pode ser compilada normalmente:

![A tree diagram, with a constant as the root element.  The constant has a name, magic number, and a value.  The constant's value is the integer literal 1145258561 of type UInt32.](macro-ast-result)

Essa AST corresponde ao código Swift a seguir:

```swift
let magicNumber = 1145258561 as UInt32
```

Neste exemplo, o código-fonte de entrada tem apenas uma macro,
mas um programa real pode ter várias instâncias da mesma macro
e várias chamadas a macros diferentes.
O compilador expande as macros uma de cada vez.

Se uma macro aparece dentro de outra,
a macro externa é expandida primeiro ---
isso permite que a macro externa modifique a macro interna antes de ela ser expandida.

<!-- OUTLINE

- TR: Is there any limit to nesting?
  TR: Is it valid to nest like this -- if so, anything to note about it?

  ```
  let something = #someMacro {
      struct A { }
      @someMacro struct B { }
  }
  ```

- Macro recursion is limited.
  One macro can call another,
  but a given macro can't directly or indirectly call itself.
  The result of macro expansion can include other macros,
  but it can't include a macro that uses this macro in its expansion
  or declare a new macro.
  (TR: Likely need to iterate on details here)
-->

## Implementando uma macro

Para implementar uma macro, você cria dois componentes:
um tipo que faz a expansão de macro,
e uma biblioteca que declara a macro para expô-la como API.
Essas partes são compiladas separadamente do código que usa a macro,
mesmo que você esteja desenvolvendo a macro e os clientes dela juntos,
porque a implementação da macro roda
como parte da compilação dos clientes da macro.

Para criar uma nova macro usando o Swift Package Manager,
execute `swift package init --type macro` ---
isso cria vários arquivos,
incluindo um modelo de implementação e de declaração de macro.

Para adicionar macros a um projeto existente,
edite o início do arquivo `Package.swift` da seguinte forma:

- Defina uma versão de ferramentas do Swift 5.9 ou posterior no comentário `swift-tools-version`.
- Importe o módulo `CompilerPluginSupport`.
- Inclua o macOS 10.15 como alvo mínimo de implantação na lista `platforms`.

O código abaixo mostra o início de um arquivo `Package.swift` de exemplo.

```swift
// swift-tools-version: 5.9

import PackageDescription
import CompilerPluginSupport

let package = Package(
    name: "MyPackage",
    platforms: [ .iOS(.v17), .macOS(.v13)],
    // ...
)
```

Em seguida, adicione um alvo para a implementação da macro
e um alvo para a biblioteca da macro
ao seu arquivo `Package.swift` existente.
Por exemplo,
você pode adicionar algo como o seguinte,
trocando os nomes para combinar com o seu projeto:

```swift
targets: [
    // Macro implementation that performs the source transformations.
    .macro(
        name: "MyProjectMacros",
        dependencies: [
            .product(name: "SwiftSyntaxMacros", package: "swift-syntax"),
            .product(name: "SwiftCompilerPlugin", package: "swift-syntax")
        ]
    ),

    // Library that exposes a macro as part of its API.
    .target(name: "MyProject", dependencies: ["MyProjectMacros"]),
]
```

O código acima define dois alvos:
`MyProjectMacros` contém a implementação das macros,
e `MyProject` disponibiliza essas macros.

A implementação de uma macro
usa o módulo [SwiftSyntax][] para interagir com código Swift
de forma estruturada, usando uma AST.
Se você criou um novo pacote de macros com o Swift Package Manager,
o arquivo `Package.swift` gerado
já inclui automaticamente uma dependência do SwiftSyntax.
Se você estiver adicionando macros a um projeto existente,
adicione uma dependência do SwiftSyntax no seu arquivo `Package.swift`:

[SwiftSyntax]: https://github.com/swiftlang/swift-syntax

```swift
dependencies: [
    .package(url: "https://github.com/swiftlang/swift-syntax", from: "509.0.0")
],
```

Dependendo do papel da macro,
há um protocolo correspondente do SwiftSyntax
que a implementação da macro adota.
Por exemplo,
considere `#fourCharacterCode` da seção anterior.
Aqui está um struct que implementa essa macro:

```swift
import SwiftSyntax
import SwiftSyntaxMacros

public struct FourCharacterCode: ExpressionMacro {
    public static func expansion(
        of node: some FreestandingMacroExpansionSyntax,
        in context: some MacroExpansionContext
    ) throws -> ExprSyntax {
        guard let argument = node.argumentList.first?.expression,
              let segments = argument.as(StringLiteralExprSyntax.self)?.segments,
              segments.count == 1,
              case .stringSegment(let literalSegment)? = segments.first
        else {
            throw CustomError.message("Need a static string")
        }

        let string = literalSegment.content.text
        guard let result = fourCharacterCode(for: string) else {
            throw CustomError.message("Invalid four-character code")
        }

        return "\(raw: result) as UInt32"
    }
}

private func fourCharacterCode(for characters: String) -> UInt32? {
    guard characters.count == 4 else { return nil }

    var result: UInt32 = 0
    for character in characters {
        result = result << 8
        guard let asciiValue = character.asciiValue else { return nil }
        result += UInt32(asciiValue)
    }
    return result
}
enum CustomError: Error { case message(String) }
```

Se você estiver adicionando essa macro a um projeto existente do Swift Package Manager,
adicione um tipo que funcione como ponto de entrada do alvo da macro
e liste as macros que o alvo define:

```swift
import SwiftCompilerPlugin

@main
struct MyProjectMacros: CompilerPlugin {
    var providingMacros: [Macro.Type] = [FourCharacterCode.self]
}
```

A macro `#fourCharacterCode`
é uma macro independente que produz uma expressão,
por isso o tipo `FourCharacterCode` que a implementa
adota o protocolo `ExpressionMacro`.
O protocolo `ExpressionMacro` tem um único requisito,
um método `expansion(of:in:)` que expande a AST.
Para a lista de papéis de macro e os protocolos correspondentes do SwiftSyntax,
veja <doc:Attributes#attached> e <doc:Attributes#freestanding>
em <doc:Attributes>.

Para expandir a macro `#fourCharacterCode`,
o Swift envia a AST do código que usa essa macro
para a biblioteca que contém a implementação da macro.
Dentro da biblioteca, o Swift chama `FourCharacterCode.expansion(of:in:)`,
passando a AST e o contexto como argumentos do método.
A implementação de `expansion(of:in:)`
encontra a string que foi passada como argumento para `#fourCharacterCode`
e calcula o valor literal correspondente de inteiro sem sinal de 32 bits.

No exemplo acima,
o primeiro bloco `guard` extrai o literal de string da AST,
atribuindo esse elemento da AST a `literalSegment`.
O segundo bloco `guard`
chama a função privada `fourCharacterCode(for:)`.
Ambos os blocos lançam um erro se a macro for usada incorretamente ---
a mensagem de erro se torna um erro de compilação
no ponto de chamada malformado.
Por exemplo,
se você tentar chamar a macro como `#fourCharacterCode("AB" + "CD")`,
o compilador mostra o erro "Need a static string".

O método `expansion(of:in:)` retorna uma instância de `ExprSyntax`,
um tipo do SwiftSyntax que representa uma expressão em uma AST.
Como esse tipo adota o protocolo `StringLiteralConvertible`,
a implementação da macro usa um literal de string
como uma sintaxe leve para criar o resultado.
Todos os tipos do SwiftSyntax que você retorna de uma implementação de macro
adotam `StringLiteralConvertible`,
então você pode usar essa abordagem ao implementar qualquer tipo de macro.

<!-- TODO contrast the `\(raw:)` and non-raw version.  -->

<!--
The return-a-string APIs come from here

https://github.com/swiftlang/swift-syntax/blob/main/Sources/SwiftSyntaxBuilder/Syntax%2BStringInterpolation.swift
-->

<!-- OUTLINE:

- Note:
  Behind the scenes, Swift serializes and deserializes the AST,
  to pass the data across process boundaries,
  but your macro implementation doesn't need to deal with any of that.

- This method is also passed a macro-expansion context, which you use to:

    + Generate unique symbol names
    + Produce diagnostics (`Diagnostic` and `SimpleDiagnosticMessage`)
    + Find a node's location in source

- Macro expansion happens in their surrounding context.
  A macro can affect that environment if it needs to ---
  and a macro that has bugs can interfere with that environment.
  (Give guidance on when you'd do this.  It should be rare.)

- Generated symbol names let a macro
  avoid accidentally interacting with symbols in that environment.
  To generate a unique symbol name,
  call the `MacroExpansionContext.makeUniqueName()` method.

- Ways to create a syntax node include
  Making an instance of the `Syntax` struct,
  or `SyntaxToken`
  or `ExprSyntax`.
  (Need to give folks some general ideas,
  and enough guidance so they can sort through
  all the various `SwiftSyntax` node types and find the right one.)

- Attached macros follow the same general model as expression macros,
  but with more moving parts.

- Pick the subprotocol of `AttachedMacro` to conform to,
  depending on which kind of attached macro you're making.
  [This is probably a table]

  + `AccessorMacro` goes with `@attached(accessor)`
  + `ConformanceMacro` goes with `@attached(conformance)`
    [missing from the list under Declaring a Macro]
  + `MemberMacro` goes with `@attached(member)`
  + `PeerMacro` goes with `@attached(peer)`
  + `MemberAttributeMacro` goes with `@member(memberAttribute)`

- Code example of conforming to `MemberMacro`.

  ```
  static func expansion<
    Declaration: DeclGroupSyntax,
    Context: MacroExpansionContext
  >(
    of node: AttributeSyntax,
    providingMembersOf declaration: Declaration,
    in context: Context
  ) throws -> [DeclSyntax]
  ```

- Adding a new member by making an instance of `Declaration`,
  and returning it as part of the `[DeclSyntax]` list.

-->

## Desenvolvendo e depurando macros

Macros são bem adequadas ao desenvolvimento com testes:
elas transformam uma AST em outra AST
sem depender de nenhum estado externo,
e sem fazer alterações em nenhum estado externo.
Além disso, você pode criar nós de sintaxe a partir de um literal de string,
o que simplifica preparar a entrada para um teste.
Você também pode ler a propriedade `description` de uma AST
para obter uma string e comparar com um valor esperado.
Por exemplo,
aqui está um teste da macro `#fourCharacterCode` das seções anteriores:

```swift
let source: SourceFileSyntax =
    """
    let abcd = #fourCharacterCode("ABCD")
    """

let file = BasicMacroExpansionContext.KnownSourceFile(
    moduleName: "MyModule",
    fullFilePath: "test.swift"
)

let context = BasicMacroExpansionContext(sourceFiles: [source: file])

let transformedSF = source.expand(
    macros:["fourCharacterCode": FourCharacterCode.self],
    in: context
)

let expectedDescription =
    """
    let abcd = 1145258561 as UInt32
    """

precondition(transformedSF.description == expectedDescription)
```

O exemplo acima testa a macro usando uma precondition,
mas você poderia usar um framework de testes no lugar.

<!-- OUTLINE:

- Ways to view the macro expansion while debugging.
  The SE prototype provides `-Xfrontend -dump-macro-expansions` for this.
  [TR: Is this flag what we should suggest folks use,
  or will there be better command-line options coming?]

- Use diagnostics for macros that have constraints/requirements
  so your code can give a meaningful error to users when those aren't met,
  instead of letting the compiler try & fail to build the generated code.

Additional APIs and concepts to introduce in the future,
in no particular order:

- Using `SyntaxRewriter` and the visitor pattern for modifying the AST

- Adding a suggested correction using `FixIt`

- concept of trivia

- `TokenSyntax`
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2023 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
