# Histórico de revisões

Confira as mudanças recentes neste livro.

**2026-09-14**

- Atualizado para o Swift 6.4.
- Inclusão de informações sobre protocolos com requisitos de superclasse
  na seção <doc:Protocols#Class-Only-Protocols>.
- Inclusão de informações sobre identificadores raw
  na seção <doc:LexicalStructure#Identifiers>.
- Inclusão de informações sobre macros de corpo
  na seção <doc:Attributes#attached>.

**2026-03-23**

- Atualizado para o Swift 6.3.
- Pequenas correções e acréscimos em todo o livro.

**2025-12-12**

- Atualizado para o Swift 6.2.3.
- Inclusão da seção <doc:Attributes#export>
  com informações sobre como exportar definições para módulos clientes.

**2025-11-03**

- Atualizado para o Swift 6.2.1.
- Inclusão da seção <doc:GenericParametersAndArguments#Integer-Generic-Parameters>
  com informações sobre parâmetros genéricos que têm um valor numérico.
- Inclusão de informações nas seções <doc:TheBasics#Integers>
  e <doc:TheBasics#Floating-Point-Numbers>
  sobre como escolher entre inteiros e números de ponto flutuante.

**2025-09-15**

- Atualizado para o Swift 6.2.
- Inclusão da seção <doc:TheBasics#Memory-Safety>
  com informações sobre problemas que o Swift ajuda você a evitar.
- Inclusão da seção <doc:ControlFlow#Patterns>
  com informações sobre a sintaxe `if case`.
- Inclusão de informações sobre o main actor, isolamento e actors globais
  no capítulo <doc:Concurrency>.
- Inclusão da seção <doc:Protocols#Implicit-Conformance-to-a-Protocol>
  com informações sobre como conformar-se a protocolos comuns
  sem escrever a conformidade explicitamente,
  e sobre como suprimir a conformidade implícita.
- Inclusão da seção <doc:Generics#Implicit-Constraints>
  com informações sobre restrições genéricas
  que exigem conformidade a protocolos comuns.

**2025-03-31**

- Atualizado para o Swift 6.1.
- Inclusão da seção <doc:OpaqueTypes#Opaque-Parameter-Types>
  com informações sobre o uso de `some` como uma sintaxe leve para genéricos.
- Inclusão de informações sobre o argumento `noasync`
  na seção <doc:Attributes#available>.

**2024-09-23**

- Atualizado para o Swift 6.
- Inclusão da seção <doc:Attributes#preconcurrency>
  com informações sobre a migração para a verificação estrita de concorrência.
- Inclusão da seção <doc:ErrorHandling#Specifying-the-Error-Type>
  com informações sobre lançar erros de um tipo específico.
- Atualização da seção <doc:Expressions#Macro-Expansion-Expression>,
  agora que qualquer macro pode ser usada como valor padrão para um parâmetro.
- Inclusão de informações sobre acesso em nível de pacote
  no capítulo <doc:AccessControl>.

**2024-03-05**

- Atualizado para o Swift 5.10.
- Inclusão de informações sobre protocolos aninhados
  na seção <doc:Protocols#Delegation>.
- Inclusão de informações sobre obsolescência
  nas seções <doc:Attributes#UIApplicationMain>
  e <doc:Attributes#NSApplicationMain>.

**2023-12-11**

- Atualizado para o Swift 5.9.2.
- Inclusão de informações sobre os modificadores `borrowing` e `consuming`
  na seção <doc:Declarations#Parameter-Modifiers>.
- Inclusão de informações em <doc:TheBasics#Declaring-Constants-and-Variables>
  sobre definir o valor de uma constante depois da declaração.
- Mais informações sobre tasks, task groups e cancelamento de tasks
  no capítulo <doc:Concurrency>.
- Inclusão de informações no capítulo <doc:Macros>
  sobre como implementar macros em um pacote Swift existente.
- Atualização da seção <doc:Attributes#attached>,
  agora que macros de extension substituíram as macros de conformidade.
- Inclusão da seção <doc:Attributes#backDeployed>
  com informações sobre back deployment.

**2023-09-18**

- Atualizado para o Swift 5.9.
- Inclusão de informações sobre expressões `if` e `switch`
  no capítulo <doc:ControlFlow>
  e na seção <doc:Expressions#Conditional-Expression>.
- Inclusão do capítulo <doc:Macros>,
  com informações sobre geração de código em tempo de compilação.
- Ampliação da discussão sobre optionals em <doc:TheBasics>.
- Inclusão de um exemplo de concorrência em <doc:GuidedTour>.
- Inclusão de informações sobre tipos de protocolo empacotados (boxed)
  no capítulo <doc:OpaqueTypes>.
- Inclusão de informações sobre os métodos `buildPartialBlock(first:)`
  e `buildPartialBlock(accumulated:next:)`
  na seção <doc:Attributes#Result-Transformations>.
- Inclusão do visionOS nas listas de plataformas em
  <doc:Attributes#available>
  e <doc:Statements#Conditional-Compilation-Block>.
- Formatação da gramática formal, com linhas em branco para agrupar as regras.

**2023-03-30**

- Atualizado para o Swift 5.8.
- Inclusão da seção <doc:ControlFlow#Deferred-Actions>,
  mostrando `defer` fora do tratamento de erros.
- Adoção do Swift-DocC para publicação.
- Pequenas correções e acréscimos em todo o livro.

**2022-09-12**

- Atualizado para o Swift 5.7.
- Inclusão da seção <doc:Concurrency#Sendable-Types>,
  com informações sobre envio de dados entre actors e tasks,
  e inclusão de informações sobre os atributos `@Sendable` e `@unchecked`
  nas seções <doc:Attributes#Sendable> e <doc:Attributes#unchecked>.
- Inclusão da seção <doc:LexicalStructure#Regular-Expression-Literals>
  com informações sobre como criar uma expressão regular.
- Inclusão de informações sobre a forma abreviada de `if`-`let`
  na seção <doc:TheBasics#Optional-Binding>.
- Inclusão de informações sobre `#unavailable`
  na seção <doc:ControlFlow#Checking-API-Availability>.

**2022-03-14**

- Atualizado para o Swift 5.6.
- Atualização da seção <doc:Expressions#Explicit-Member-Expression>
  com informações sobre usar `#if`
  em torno de chamadas de método encadeadas e outras expressões pós-fixadas.
- Atualização do estilo visual das figuras em todo o livro.

**2021-09-20**

- Atualizado para o Swift 5.5.
- Inclusão de informações sobre funções assíncronas, tasks e actors
  no capítulo <doc:Concurrency>,
  e nas seções <doc:Declarations#Actor-Declaration>,
  <doc:Declarations#Asynchronous-Functions-and-Methods>
  e <doc:Expressions#Await-Operator>.
- Atualização da seção <doc:LexicalStructure#Identifiers>
  com informações sobre identificadores que começam com sublinhado.

**2021-04-26**

- Atualizado para o Swift 5.4.
- Inclusão das seções <doc:AdvancedOperators#Result-Builders>
  e <doc:Attributes#resultBuilder>
  com informações sobre result builders.
- Inclusão da seção <doc:Expressions#Implicit-Conversion-to-a-Pointer-Type>
  com informações sobre como parâmetros in-out
  podem ser convertidos implicitamente em ponteiros unsafe em uma chamada de função.
- Atualização das seções <doc:Functions#Variadic-Parameters>
  e <doc:Declarations#Function-Declaration>,
  agora que uma função pode ter vários parâmetros variádicos.
- Atualização da seção <doc:Expressions#Implicit-Member-Expression>,
  agora que expressões de membro implícitas podem ser encadeadas.

**2020-09-16**

- Atualizado para o Swift 5.3.
- Inclusão de informações sobre múltiplas trailing closures
  na seção <doc:Closures#Trailing-Closures>,
  e inclusão de informações sobre como as trailing closures são associadas a parâmetros
  na seção <doc:Expressions#Function-Call-Expression>.
- Inclusão de informações sobre implementações sintetizadas de `Comparable` para enums
  na seção <doc:Protocols#Adopting-a-Protocol-Using-a-Synthesized-Implementation>.
- Inclusão da seção <doc:Generics#Contextual-Where-Clauses>,
  agora que você pode escrever uma cláusula `where` genérica em mais lugares.
- Inclusão da seção <doc:AutomaticReferenceCounting#Unowned-Optional-References>
  com informações sobre como usar referências unowned com valores optional.
- Inclusão de informações sobre o atributo `@main`
  na seção <doc:Attributes#main>.
- Inclusão de `#filePath` na seção <doc:Expressions#Literal-Expression>,
  e atualização da discussão sobre `#file`.
- Atualização da seção <doc:Closures#Escaping-Closures>,
  agora que closures podem se referir a `self` implicitamente em mais cenários.
- Atualização das seções <doc:ErrorHandling#Handling-Errors-Using-Do-Catch>
  e <doc:Statements#Do-Statement>,
  agora que uma cláusula `catch` pode corresponder a vários erros.
- Mais informações sobre `Any`, movidas para a nova seção <doc:Types#Any-Type>.
- Atualização da seção <doc:Properties#Property-Observers>,
  agora que propriedades lazy podem ter observers.
- Atualização da seção <doc:Declarations#Protocol-Declaration>,
  agora que membros de um enum podem satisfazer requisitos de protocolo.
- Atualização da seção <doc:Declarations#Stored-Variable-Observers-and-Property-Observers>
  para descrever quando o getter é chamado antes do observer.
- Atualização do capítulo <doc:MemorySafety>
  para mencionar operações atômicas.

**2020-03-24**

- Atualizado para o Swift 5.2.
- Inclusão de informações sobre passar um key path em vez de uma closure
  na seção <doc:Expressions#Key-Path-Expression>.
- Inclusão da seção <doc:Declarations#Methods-with-Special-Names>
  com informações sobre o açúcar sintático que permite
  usar instâncias de classes, structs e enums com a sintaxe de chamada de função.
- Atualização da seção <doc:Subscripts#Subscript-Options>,
  agora que subscripts aceitam parâmetros com valores padrão.
- Atualização da seção <doc:Types#Self-Type>,
  agora que `Self` pode ser usado em mais contextos.
- Atualização da seção <doc:TheBasics#Implicitly-Unwrapped-Optionals>
  para deixar mais claro que um optional com unwrap implícito
  pode ser usado como optional ou como valor não optional.

**2019-09-10**

- Atualizado para o Swift 5.1.
- Inclusão de informações sobre funções que especificam um protocolo
  ao qual o valor de retorno está em conformidade,
  em vez de informar um tipo de retorno específico e nomeado,
  no capítulo <doc:OpaqueTypes>.
- Inclusão de informações sobre property wrappers
  na seção <doc:Properties#Property-Wrappers>.
- Inclusão de informações sobre enums e structs congelados (frozen)
  para evolução de biblioteca
  na seção <doc:Attributes#frozen>.
- Inclusão das seções <doc:Functions#Functions-With-an-Implicit-Return>
  e <doc:Properties#Shorthand-Getter-Declaration>
  com informações sobre funções que omitem `return`.
- Inclusão de informações sobre o uso de subscripts em tipos
  na seção <doc:Subscripts#Type-Subscripts>.
- Atualização da seção <doc:Patterns#Enumeration-Case-Pattern>,
  agora que um padrão de case de enum pode corresponder a um optional.
- Atualização da seção <doc:Initialization#Memberwise-Initializers-for-Structure-Types>,
  agora que inicializadores memberwise aceitam omitir parâmetros
  de propriedades que têm valor padrão.
- Inclusão de informações sobre membros dinâmicos
  buscados por key path em tempo de execução
  na seção <doc:Attributes#dynamicMemberLookup>.
- Inclusão de `macCatalyst` na lista de ambientes de destino
  em <doc:Statements#Conditional-Compilation-Block>.
- Atualização da seção <doc:Types#Self-Type>,
  agora que `Self` pode ser usado para se referir ao tipo
  introduzido pela declaração atual de classe, struct ou enum.

**2019-03-25**

- Atualizado para o Swift 5.0.
- Inclusão da seção <doc:StringsAndCharacters#Extended-String-Delimiters>
  e atualização da seção <doc:LexicalStructure#String-Literals>
  com informações sobre delimitadores de string estendidos.
- Inclusão da seção <doc:Attributes#dynamicCallable>
  com informações sobre como chamar instâncias dinamicamente como funções,
  usando o atributo `dynamicCallable`.
- Inclusão das seções <doc:Attributes#unknown>
  e <doc:Statements#Switching-Over-Future-Enumeration-Cases>
  com informações sobre como tratar casos de enum futuros em instruções switch,
  usando o atributo `unknown` de case de switch.
- Inclusão de informações sobre o key path de identidade (`\.self`)
  na seção <doc:Expressions#Key-Path-Expression>.
- Inclusão de informações sobre o uso do operador menor que (`<`)
  em condições de plataforma na seção <doc:Statements#Conditional-Compilation-Block>.

**2018-09-17**

- Atualizado para o Swift 4.2.
- Inclusão de informações sobre como acessar todos os cases de um enum
  na seção <doc:Enumerations#Iterating-over-Enumeration-Cases>.
- Inclusão de informações sobre `#error` e `#warning`
  na seção <doc:Statements#Compile-Time-Diagnostic-Statement>.
- Inclusão de informações sobre inlining
  na seção <doc:Attributes#Declaration-Attributes>,
  nos atributos `inlinable` e `usableFromInline`.
- Inclusão de informações sobre membros buscados pelo nome em tempo de execução
  na seção <doc:Attributes#Declaration-Attributes>,
  no atributo `dynamicMemberLookup`.
- Inclusão de informações sobre os atributos `requires_stored_property_inits`
  e `warn_unqualified_access`
  na seção <doc:Attributes#Declaration-Attributes>.
- Inclusão de informações sobre como compilar código condicionalmente,
  de acordo com a versão do compilador Swift usada,
  na seção <doc:Statements#Conditional-Compilation-Block>.
- Inclusão de informações sobre `#dsohandle`
  na seção <doc:Expressions#Literal-Expression>.

**2018-03-29**

- Atualizado para o Swift 4.1.
- Inclusão de informações sobre implementações sintetizadas de operadores de equivalência
  na seção <doc:AdvancedOperators#Equivalence-Operators>.
- Inclusão de informações sobre conformidade condicional a protocolos
  na seção <doc:Declarations#Extension-Declaration>
  do capítulo <doc:Declarations>,
  e na seção <doc:Protocols#Conditionally-Conforming-to-a-Protocol>
  do capítulo <doc:Protocols>.
- Inclusão de informações sobre restrições recursivas de protocolo
  na seção <doc:Generics#Using-a-Protocol-in-Its-Associated-Types-Constraints>.
- Inclusão de informações sobre as condições de plataforma `canImport()`
  e `targetEnvironment()`
  em <doc:Statements#Conditional-Compilation-Block>.

**2017-12-04**

- Atualizado para o Swift 4.0.3.
- Atualização da seção <doc:Expressions#Key-Path-Expression>,
  agora que key paths aceitam componentes de subscript.

**2017-09-19**

- Atualizado para o Swift 4.0.
- Inclusão de informações sobre acesso exclusivo à memória
  no capítulo <doc:MemorySafety>.
- Inclusão da seção <doc:Generics#Associated-Types-with-a-Generic-Where-Clause>,
  agora que você pode usar cláusulas `where` genéricas
  para restringir tipos associados.
- Inclusão de informações sobre literais de string multilinha
  na seção <doc:StringsAndCharacters#String-Literals>
  do capítulo <doc:StringsAndCharacters>,
  e na seção <doc:LexicalStructure#String-Literals>
  do capítulo <doc:LexicalStructure>.
- Atualização da discussão sobre o atributo `objc`
  em <doc:Attributes#Declaration-Attributes>,
  agora que esse atributo é inferido em menos lugares.
- Inclusão da seção <doc:Generics#Generic-Subscripts>,
  agora que subscripts podem ser genéricos.
- Atualização da discussão
  na seção <doc:Protocols#Protocol-Composition> do capítulo <doc:Protocols>,
  e na seção <doc:Types#Protocol-Composition-Type> do capítulo <doc:Types>,
  agora que tipos de composição de protocolos podem conter um requisito de superclasse.
- Atualização da discussão sobre extensions de protocolo
  em <doc:Declarations#Extension-Declaration>,
  agora que `final` não é permitido nelas.
- Inclusão de informações sobre pré-condições e erros fatais
  na seção <doc:TheBasics#Assertions-and-Preconditions>.

**2017-03-27**

- Atualizado para o Swift 3.1.
- Inclusão da seção <doc:Generics#Extensions-with-a-Generic-Where-Clause>
  com informações sobre extensions que incluem requisitos.
- Inclusão de exemplos de iteração sobre um intervalo
  na seção <doc:ControlFlow#For-In-Loops>.
- Inclusão de um exemplo de conversões numéricas falíveis
  na seção <doc:Initialization#Failable-Initializers>.
- Inclusão de informações na seção <doc:Attributes#Declaration-Attributes>
  sobre o uso do atributo `available` com uma versão da linguagem Swift.
- Atualização da discussão sobre tipos de função
  na seção <doc:Types#Function-Type>,
  para observar que rótulos de argumento não são permitidos ao escrever um tipo de função.
- Atualização da discussão sobre números de versão da linguagem Swift
  na seção <doc:Statements#Conditional-Compilation-Block>,
  agora que um número de patch opcional é permitido.
- Atualização da discussão
  na seção <doc:Types#Function-Type>,
  agora que o Swift diferencia funções que recebem vários parâmetros
  de funções que recebem um único parâmetro do tipo tupla.
- Remoção da seção Expressão de tipo dinâmico
  do capítulo <doc:Expressions>,
  agora que `type(of:)` é uma função da biblioteca padrão do Swift.

**2016-10-27**

- Atualizado para o Swift 3.0.1.
- Atualização da discussão sobre referências weak e unowned
  no capítulo <doc:AutomaticReferenceCounting>.
- Inclusão de informações sobre os modificadores de declaração
  `unowned`, `unowned(safe)` e `unowned(unsafe)`
  na seção <doc:Declarations#Declaration-Modifiers>.
- Inclusão de uma nota na seção <doc:TypeCasting#Type-Casting-for-Any-and-AnyObject>
  sobre usar um valor optional quando se espera um valor do tipo `Any`.
- Atualização do capítulo <doc:Expressions>
  para separar a discussão sobre expressões entre parênteses
  e expressões de tupla.

**2016-09-13**

- Atualizado para o Swift 3.0.
- Atualização da discussão sobre funções no capítulo <doc:Functions>
  e na seção <doc:Declarations#Function-Declaration>,
  para observar que todos os parâmetros recebem um rótulo de argumento por padrão.
- Atualização da discussão sobre operadores no capítulo <doc:AdvancedOperators>,
  agora que você os implementa como métodos de tipo em vez de funções globais.
- Inclusão de informações sobre os modificadores de nível de acesso `open` e `fileprivate`
  no capítulo <doc:AccessControl>.
- Atualização da discussão sobre `inout` na seção <doc:Declarations#Function-Declaration>
  para observar que ele aparece antes do tipo do parâmetro,
  e não antes do nome do parâmetro.
- Atualização da discussão sobre os atributos `@noescape` e `@autoclosure`
  nas seções <doc:Closures#Escaping-Closures> e <doc:Closures#Autoclosures>
  e no capítulo <doc:Attributes>,
  agora que são atributos de tipo, e não atributos de declaração.
- Inclusão de informações sobre grupos de precedência de operadores
  na seção <doc:AdvancedOperators#Precedence-for-Custom-Infix-Operators>
  do capítulo <doc:AdvancedOperators>,
  e na seção <doc:Declarations#Precedence-Group-Declaration>
  do capítulo <doc:Declarations>.
- Atualização da discussão em todo o livro
  para usar macOS em vez de OS X,
  `Error` em vez de `ErrorProtocol`,
  e nomes de protocolo como `ExpressibleByStringLiteral`
  em vez de `StringLiteralConvertible`.
- Atualização da discussão
  na seção <doc:Generics#Generic-Where-Clauses> do capítulo <doc:Generics>
  e no capítulo <doc:GenericParametersAndArguments>,
  agora que cláusulas `where` genéricas são escritas no fim de uma declaração.
- Atualização da discussão na seção <doc:Closures#Escaping-Closures>,
  agora que closures são nonescaping por padrão.
- Atualização da discussão
  na seção <doc:TheBasics#Optional-Binding> do capítulo <doc:TheBasics>
  e na seção <doc:Statements#While-Statement> do capítulo <doc:Statements>,
  agora que instruções `if`, `while` e `guard` usam uma lista de condições
  separadas por vírgula, sem cláusulas `where`.
- Inclusão de informações sobre casos de switch que têm vários padrões
  na seção <doc:ControlFlow#Switch> do capítulo <doc:ControlFlow>
  e na seção <doc:Statements#Switch-Statement> do capítulo <doc:Statements>.
- Atualização da discussão sobre tipos de função
  na seção <doc:Types#Function-Type>,
  agora que rótulos de argumento de função não fazem mais parte do tipo da função.
- Atualização da discussão sobre tipos de composição de protocolos
  na seção <doc:Protocols#Protocol-Composition> do capítulo <doc:Protocols>
  e na seção <doc:Types#Protocol-Composition-Type> do capítulo <doc:Types>,
  para usar a nova sintaxe `Protocol1 & Protocol2`.
- Atualização da discussão na seção de expressões de tipo dinâmico
  para usar a nova sintaxe `type(of:)`.
- Atualização da discussão sobre instruções de controle de linha
  para usar a sintaxe `#sourceLocation(file:line:)`
  na seção <doc:Statements#Line-Control-Statement>.
- Atualização da discussão em <doc:Declarations#Functions-that-Never-Return>
  para usar o novo tipo `Never`.
- Inclusão de informações sobre literais de playground
  na seção <doc:Expressions#Literal-Expression>.
- Atualização da discussão na seção <doc:Declarations#In-Out-Parameters>
  para observar que apenas closures nonescaping podem capturar parâmetros in-out.
- Atualização da discussão sobre parâmetros padrão
  na seção <doc:Functions#Default-Parameter-Values>,
  agora que eles não podem mais ser reordenados em chamadas de função.
- Atualização dos argumentos de atributos para usar dois-pontos
  no capítulo <doc:Attributes>.
- Inclusão de informações sobre lançar um erro
  dentro do bloco catch de uma função rethrowing
  na seção <doc:Declarations#Rethrowing-Functions-and-Methods>.
- Inclusão de informações sobre como acessar o selector
  do getter ou do setter de uma propriedade Objective-C
  na seção <doc:Expressions#Selector-Expression>.
- Inclusão de informações na seção <doc:Declarations#Type-Alias-Declaration>
  sobre aliases de tipo genéricos e sobre o uso de aliases de tipo dentro de protocolos.
- Atualização da discussão sobre tipos de função na seção <doc:Types#Function-Type>
  para observar que os parênteses em torno dos tipos dos parâmetros são obrigatórios.
- Atualização do capítulo <doc:Attributes>
  para observar que os atributos `@IBAction`, `@IBOutlet` e `@NSManaged`
  implicam o atributo `@objc`.
- Inclusão de informações sobre o atributo `@GKInspectable`
  na seção <doc:Attributes#Declaration-Attributes>.
- Atualização da discussão sobre requisitos opcionais de protocolo
  na seção <doc:Protocols#Optional-Protocol-Requirements>
  para deixar claro que eles são usados apenas em código que interage com Objective-C.
- Remoção da discussão sobre usar `let` explicitamente em parâmetros de função
  da seção <doc:Declarations#Function-Declaration>.
- Remoção da discussão sobre o protocolo `Boolean`
  do capítulo <doc:Statements>,
  agora que o protocolo foi removido da biblioteca padrão do Swift.
- Correção da discussão sobre o atributo `@NSApplicationMain`
  na seção <doc:Attributes#Declaration-Attributes>.

**2016-03-21**

- Atualizado para o Swift 2.2.
- Inclusão de informações sobre como compilar código condicionalmente
  de acordo com a versão do Swift usada
  na seção <doc:Statements#Conditional-Compilation-Block>.
- Inclusão de informações sobre como distinguir
  métodos ou inicializadores cujos nomes diferem
  apenas pelos nomes dos argumentos
  na seção <doc:Expressions#Explicit-Member-Expression>.
- Inclusão de informações sobre a sintaxe `#selector`
  para seletores Objective-C
  na seção <doc:Expressions#Selector-Expression>.
- Atualização da discussão sobre tipos associados
  para usar a palavra-chave `associatedtype`
  nas seções <doc:Generics#Associated-Types>
  e <doc:Declarations#Protocol-Associated-Type-Declaration>.
- Atualização das informações sobre inicializadores que retornam `nil`
  antes de a instância ser totalmente inicializada
  na seção <doc:Initialization#Failable-Initializers>.
- Inclusão de informações sobre comparação de tuplas
  na seção <doc:BasicOperators#Comparison-Operators>.
- Inclusão de informações sobre o uso de palavras-chave como nomes de parâmetros externos
  na seção <doc:LexicalStructure#Keywords-and-Punctuation>.
- Atualização da discussão sobre o atributo `@objc`
  na seção <doc:Attributes#Declaration-Attributes>,
  para observar que enums e cases de enum podem usar esse atributo.
- Atualização da seção <doc:LexicalStructure#Operators>
  com a discussão sobre operadores personalizados que contêm um ponto.
- Inclusão de uma nota
  na seção <doc:Declarations#Rethrowing-Functions-and-Methods>
  observando que funções rethrowing não podem lançar erros diretamente.
- Inclusão de uma nota na seção <doc:Properties#Property-Observers>
  sobre observers de propriedade serem chamados
  quando você passa uma propriedade como parâmetro in-out.
- Inclusão de uma seção sobre tratamento de erros
  no capítulo <doc:GuidedTour>.
- Atualização das figuras na seção
  <doc:AutomaticReferenceCounting#Weak-References>
  para mostrar o processo de desalocação com mais clareza.
- Remoção da discussão sobre loops `for` no estilo C,
  dos operadores prefixos e pós-fixos `++`,
  e dos operadores prefixos e pós-fixos `--`.
- Remoção da discussão sobre argumentos variáveis de função
  e da sintaxe especial para funções curried.

**2015-10-20**

- Atualizado para o Swift 2.1.
- Atualização das seções <doc:StringsAndCharacters#String-Interpolation>
  e <doc:LexicalStructure#String-Literals>,
  agora que interpolações de string podem conter literais de string.
- Inclusão da seção <doc:Closures#Escaping-Closures>
  com informações sobre o atributo `@noescape`.
- Atualização das seções <doc:Attributes#Declaration-Attributes>
  e <doc:Statements#Conditional-Compilation-Block>
  com informações sobre tvOS.
- Inclusão de informações sobre o comportamento de parâmetros in-out
  na seção <doc:Declarations#In-Out-Parameters>.
- Inclusão de informações na seção <doc:Expressions#Capture-Lists>
  sobre como os valores especificados em listas de captura de closures são capturados.
- Atualização da seção
  <doc:OptionalChaining#Accessing-Properties-Through-Optional-Chaining>
  para deixar claro como a atribuição por meio de optional chaining se comporta.
- Melhoria da discussão sobre autoclosures
  na seção <doc:Closures#Autoclosures>.
- Inclusão de um exemplo que usa o operador `??`
  no capítulo <doc:GuidedTour>.

**2015-09-16**

- Atualizado para o Swift 2.0.
- Inclusão de informações sobre tratamento de erros
  no capítulo <doc:ErrorHandling>,
  na seção <doc:Statements#Do-Statement>,
  na seção <doc:Statements#Throw-Statement>,
  na seção <doc:Statements#Defer-Statement>
  e na seção <doc:Expressions#Try-Operator>.
- Atualização da seção <doc:ErrorHandling#Representing-and-Throwing-Errors>,
  agora que todos os tipos podem estar em conformidade com o protocolo `ErrorType`.
- Inclusão de informações sobre a nova palavra-chave `try?`
  na seção <doc:ErrorHandling#Converting-Errors-to-Optional-Values>.
- Inclusão de informações sobre enums recursivos
  na seção <doc:Enumerations#Recursive-Enumerations>
  do capítulo <doc:Enumerations>,
  e na seção <doc:Declarations#Enumerations-with-Cases-of-Any-Type>
  do capítulo <doc:Declarations>.
- Inclusão de informações sobre a verificação de disponibilidade de APIs
  na seção <doc:ControlFlow#Checking-API-Availability>
  do capítulo <doc:ControlFlow>,
  e na seção <doc:Statements#Availability-Condition>
  do capítulo <doc:Statements>.
- Inclusão de informações sobre a nova instrução `guard`
  na seção <doc:ControlFlow#Early-Exit>
  do capítulo <doc:ControlFlow>,
  e na seção <doc:Statements#Guard-Statement>
  do capítulo <doc:Statements>.
- Inclusão de informações sobre extensions de protocolo
  na seção <doc:Protocols#Protocol-Extensions>
  do capítulo <doc:Protocols>.
- Inclusão de informações sobre controle de acesso para testes unitários
  na seção <doc:AccessControl#Access-Levels-for-Unit-Test-Targets>
  do capítulo <doc:AccessControl>.
- Inclusão de informações sobre o novo padrão optional
  na seção <doc:Patterns#Optional-Pattern>
  do capítulo <doc:Patterns>.
- Atualização da seção <doc:ControlFlow#Repeat-While>
  com informações sobre o loop `repeat`-`while`.
- Atualização do capítulo <doc:StringsAndCharacters>,
  agora que `String` não está mais em conformidade
  com o protocolo `CollectionType` da biblioteca padrão do Swift.
- Inclusão de informações sobre a nova função da biblioteca padrão do Swift
  `print(_:separator:terminator)`
  na seção <doc:TheBasics#Printing-Constants-and-Variables>.
- Inclusão de informações sobre o comportamento de casos de enum
  com raw values do tipo `String`
  na seção <doc:Enumerations#Implicitly-Assigned-Raw-Values>
  do capítulo <doc:Enumerations>,
  e na seção <doc:Declarations#Enumerations-with-Cases-of-a-Raw-Value-Type>
  do capítulo <doc:Declarations>.
- Inclusão de informações sobre o atributo `@autoclosure`,
  incluindo sua forma `@autoclosure(escaping)`,
  na seção <doc:Closures#Autoclosures>.
- Atualização da seção <doc:Attributes#Declaration-Attributes>
  com informações sobre os atributos `@available`
  e `@warn_unused_result`.
- Atualização da seção <doc:Attributes#Type-Attributes>
  com informações sobre o atributo `@convention`.
- Inclusão de um exemplo de uso de múltiplas cláusulas de optional binding
  com uma cláusula `where`
  na seção <doc:TheBasics#Optional-Binding>.
- Inclusão de informações na seção <doc:LexicalStructure#String-Literals>
  sobre como concatenar literais de string com o operador `+` acontece em tempo de compilação.
- Inclusão de informações na seção <doc:Types#Metatype-Type>
  sobre comparar valores de metatipo e usá-los
  para construir instâncias com expressões de inicializador.
- Inclusão de uma nota na seção <doc:TheBasics#Debugging-with-Assertions>
  sobre quando asserções definidas pelo usuário são desabilitadas.
- Atualização da discussão sobre o atributo `@NSManaged`
  na seção <doc:Attributes#Declaration-Attributes>,
  agora que o atributo pode ser aplicado a certos métodos de instância.
- Atualização da seção <doc:Functions#Variadic-Parameters>,
  agora que parâmetros variádicos podem ser declarados em qualquer posição
  da lista de parâmetros de uma função.
- Inclusão de informações na seção <doc:Initialization#Overriding-a-Failable-Initializer>
  sobre como um inicializador não falível pode delegar
  a um inicializador falível da superclasse,
  fazendo force unwrap do resultado.
- Inclusão de informações sobre o uso de casos de enum como funções
  na seção <doc:Declarations#Enumerations-with-Cases-of-Any-Type>.
- Inclusão de informações sobre como referenciar explicitamente um inicializador
  na seção <doc:Expressions#Initializer-Expression>.
- Inclusão de informações sobre configuração de build
  e instruções de controle de linha
  na seção <doc:Statements#Compiler-Control-Statements>.
- Inclusão de uma nota na seção <doc:Types#Metatype-Type>
  sobre como construir instâncias de classe a partir de valores de metatipo.
- Inclusão de uma nota
  na seção <doc:AutomaticReferenceCounting#Weak-References>
  sobre referências weak não serem adequadas para cache.
- Atualização de uma nota na seção <doc:Properties#Type-Properties>
  para mencionar que propriedades de tipo armazenadas são inicializadas de forma lazy.
- Atualização da seção <doc:Closures#Capturing-Values>
  para deixar claro como variáveis e constantes são capturadas em closures.
- Atualização da seção <doc:Attributes#Declaration-Attributes>
  para descrever quando você pode aplicar o atributo `@objc` a classes.
- Inclusão de uma nota na seção <doc:ErrorHandling#Handling-Errors>
  sobre o desempenho da execução de uma instrução `throw`.
  Inclusão de informação semelhante sobre a instrução `do`
  na seção <doc:Statements#Do-Statement>.
- Atualização da seção <doc:Properties#Type-Properties>
  com informações sobre propriedades de tipo armazenadas e computadas
  para classes, structs e enums.
- Atualização da seção <doc:Statements#Break-Statement>
  com informações sobre instruções break com rótulo.
- Atualização de uma nota na seção <doc:Properties#Property-Observers>
  para esclarecer o comportamento dos observers `willSet` e `didSet`.
- Inclusão de uma nota na seção <doc:AccessControl#Access-Levels>
  com informações sobre o escopo do acesso `private`.
- Inclusão de uma nota
  na seção <doc:AutomaticReferenceCounting#Weak-References>
  sobre as diferenças nas referências weak entre sistemas com coleta de lixo e ARC.
- Atualização da seção
  <doc:StringsAndCharacters#Special-Characters-in-String-Literals>
  com uma definição mais precisa de escalares Unicode.

**2015-04-08**

- Atualizado para o Swift 1.2.
- O Swift agora tem um tipo de coleção `Set` nativo.
  Para mais informações, consulte <doc:CollectionTypes#Sets>.
- `@autoclosure` agora é um atributo da declaração do parâmetro,
  e não do seu tipo.
  Também há um novo atributo de declaração de parâmetro `@noescape`.
  Para mais informações, consulte <doc:Attributes#Declaration-Attributes>.
- Métodos e propriedades de tipo agora usam a palavra-chave `static`
  como modificador de declaração.
  Para mais informações, consulte <doc:Declarations#Type-Variable-Properties>.
- O Swift agora inclui os operadores de downcast falíveis `as?` e `as!`.
  Para mais informações,
  consulte <doc:Protocols#Checking-for-Protocol-Conformance>.
- Inclusão de uma nova seção do guia sobre
  <doc:StringsAndCharacters#String-Indices>.
- Remoção dos operadores de divisão com overflow (`&/`) e
  de resto com overflow (`&%`)
  de <doc:AdvancedOperators#Overflow-Operators>.
- Atualização das regras para declaração e inicialização de constantes
  e de propriedades constantes.
  Para mais informações, consulte <doc:Declarations#Constant-Declaration>.
- Atualização da definição de escalares Unicode em literais de string.
  Consulte <doc:StringsAndCharacters#Special-Characters-in-String-Literals>.
- Atualização de <doc:BasicOperators#Range-Operators> para observar que
  um intervalo semiaberto com o mesmo índice inicial e final será vazio.
- Atualização de <doc:Closures#Closures-Are-Reference-Types> para esclarecer
  as regras de captura de variáveis.
- Atualização de <doc:AdvancedOperators#Value-Overflow> para esclarecer
  o comportamento de overflow de inteiros com e sem sinal.
- Atualização de <doc:Declarations#Protocol-Declaration> para esclarecer
  o escopo e os membros da declaração de protocolo.
- Atualização de <doc:AutomaticReferenceCounting#Defining-a-Capture-List>
  para esclarecer a sintaxe de referências weak e unowned
  em listas de captura de closures.
- Atualização de <doc:LexicalStructure#Operators> para mencionar explicitamente
  exemplos de caracteres aceitos em operadores personalizados,
  como os dos blocos Unicode Mathematical Operators, Miscellaneous Symbols
  e Dingbats.
- Constantes agora podem ser declaradas sem inicialização
  no escopo de uma função local.
  Elas devem ter um valor definido antes do primeiro uso.
  Para mais informações, consulte <doc:Declarations#Constant-Declaration>.
- Em um inicializador, propriedades constantes agora só podem receber um valor uma vez.
  Para mais informações,
  consulte <doc:Initialization#Assigning-Constant-Properties-During-Initialization>.
- Várias cláusulas de optional binding agora podem aparecer em uma única instrução `if`,
  como uma lista de expressões de atribuição separadas por vírgula.
  Para mais informações, consulte <doc:TheBasics#Optional-Binding>.
- Uma <doc:Expressions#Optional-Chaining-Expression>
  deve aparecer dentro de uma expressão pós-fixada.
- Conversões de protocolo não se limitam mais a protocolos `@objc`.
- Conversões de tipo que podem falhar em tempo de execução
  agora usam o operador `as?` ou `as!`,
  e conversões de tipo que não podem falhar usam o operador `as`.
  Para mais informações, consulte <doc:Expressions#Type-Casting-Operators>.

**2014-10-16**

- Atualizado para o Swift 1.1.
- Inclusão de um guia completo sobre <doc:Initialization#Failable-Initializers>.
- Inclusão de uma descrição de <doc:Protocols#Failable-Initializer-Requirements>
  para protocolos.
- Constantes e variáveis do tipo `Any` agora podem conter
  instâncias de função. A discussão em <doc:TypeCasting#Type-Casting-for-Any-and-AnyObject>
  foi atualizada para mostrar como verificar e converter para um tipo de função
  dentro de uma instrução `switch`.
- Enums com raw values agora têm uma propriedade `rawValue` em vez de um método `toRaw()`,
  e um inicializador falível com um parâmetro `rawValue`
  em vez de um método `fromRaw()`.
  Para mais informações, consulte <doc:Enumerations#Raw-Values>
  e <doc:Declarations#Enumerations-with-Cases-of-a-Raw-Value-Type>.
- Inclusão de uma nova seção de referência sobre
  <doc:Declarations#Failable-Initializers>,
  que pode disparar uma falha de inicialização.
- Operadores personalizados agora podem conter o caractere `?`.
  A referência <doc:LexicalStructure#Operators> foi atualizada para descrever
  as regras revisadas.
  Removida uma descrição duplicada do conjunto válido de caracteres de operador
  de <doc:AdvancedOperators#Custom-Operators>.

**2014-08-18**

- Novo documento que descreve o Swift 1.0,
  a nova linguagem de programação da Apple para criar apps para iOS e OS X.
- Inclusão de uma nova seção sobre
  <doc:Protocols#Initializer-Requirements> em protocolos.
- Inclusão de uma nova seção sobre <doc:Protocols#Class-Only-Protocols>.
- A seção <doc:TheBasics#Assertions-and-Preconditions> agora permite interpolação de string.
  Removida a nota em contrário.
- Atualização e ampliação da seção
  <doc:StringsAndCharacters#Concatenating-Strings-and-Characters>
  para refletir que os valores `String` e `Character`
  não podem mais ser combinados com o operador de adição (`+`)
  ou com o operador de atribuição por adição (`+=`).
  Esses operadores agora são usados apenas com valores `String`.
  Use o método `append(_:)` do tipo `String`
  para acrescentar um único valor `Character` ao fim de uma string.
- Inclusão de informações sobre o atributo `availability`
  na seção <doc:Attributes#Declaration-Attributes>.
- Os <doc:TheBasics#Optionals> deixaram de ser avaliados implicitamente como `true`
  quando têm valor e como `false` quando não têm,
  para evitar confusão ao trabalhar com valores `Bool` optionals.
  Em vez disso, faça uma verificação explícita contra `nil`
  com os operadores `==` ou `!=`
  para descobrir se um optional contém um valor.
- O Swift agora tem o operador de coalescência de nil
  (<doc:BasicOperators#Nil-Coalescing-Operator>, `a ?? b`), que faz o unwrap do valor de um optional, se ele existir,
  ou retorna um valor padrão se o optional for `nil`.
- Atualização e ampliação da seção <doc:StringsAndCharacters#Comparing-Strings>
  para refletir e demonstrar que a comparação de strings e de caracteres,
  assim como a comparação de prefixo e sufixo,
  agora se baseia na equivalência canônica Unicode de clusters de grafemas estendidos.
- Agora você pode tentar definir o valor de uma propriedade, atribuir a um subscript
  ou chamar um método ou operador mutante por meio de <doc:OptionalChaining>.
  As informações sobre
  <doc:OptionalChaining#Accessing-Properties-Through-Optional-Chaining>
  foram atualizadas de acordo,
  e os exemplos de verificação de sucesso de chamadas de método em
  <doc:OptionalChaining#Calling-Methods-Through-Optional-Chaining>
  foram ampliados para mostrar como verificar o sucesso da definição de propriedades.
- Inclusão de uma nova seção sobre
  <doc:OptionalChaining#Accessing-Subscripts-of-Optional-Type>
  por meio de optional chaining.
- Atualização da seção <doc:CollectionTypes#Accessing-and-Modifying-an-Array>
  para observar que você não pode mais acrescentar um único item a um array
  com o operador `+=`.
  Em vez disso, use o método `append(_:)`,
  ou acrescente um array de um único item com o operador `+=`.
- Inclusão de uma observação de que o valor inicial `a`
  dos intervalos <doc:BasicOperators#Range-Operators> `a...b` e `a..<b`
  não pode ser maior que o valor final `b`.
- Reescrita do capítulo <doc:Inheritance>
  para remover sua introdução aos overrides de inicializadores.
  Agora o capítulo se concentra mais na adição de
  novas funcionalidades em uma subclasse
  e na modificação de funcionalidades existentes com overrides.
  O exemplo do capítulo sobre
  <doc:Inheritance#Overriding-Property-Getters-and-Setters>
  foi reescrito para mostrar como sobrescrever a propriedade `description`.
  (Os exemplos de modificação do valor padrão de uma propriedade herdada
  em um inicializador de subclasse foram movidos para o capítulo <doc:Initialization>.)
- Atualização da seção
  <doc:Initialization#Initializer-Inheritance-and-Overriding>
  para observar que overrides de um inicializador designado
  agora devem ser marcados com o modificador `override`.
- Atualização da seção <doc:Initialization#Required-Initializers>
  para observar que o modificador `required` agora é escrito antes
  de cada implementação em subclasse de um inicializador required,
  e que os requisitos de inicializadores required
  agora podem ser atendidos por inicializadores herdados automaticamente.
- Operadores infixos de <doc:AdvancedOperators#Operator-Methods> não exigem mais
  o atributo `@infix`.
- Os atributos `@prefix` e `@postfix`
  para <doc:AdvancedOperators#Prefix-and-Postfix-Operators>
  foram substituídos pelos modificadores de declaração `prefix` e `postfix`.
- Inclusão de uma observação sobre a ordem em que
  <doc:AdvancedOperators#Prefix-and-Postfix-Operators> são aplicados
  quando um operador prefixo e um pós-fixo são aplicados
  ao mesmo operando.
- Funções de operador para
  <doc:AdvancedOperators#Compound-Assignment-Operators> não usam mais
  o atributo `@assignment` ao definir a função.
- A ordem em que os modificadores são especificados ao definir
  <doc:AdvancedOperators#Custom-Operators> mudou.
  Agora você escreve `prefix operator` em vez de `operator prefix`,
  por exemplo.
- Inclusão de informações sobre o modificador de declaração `dynamic`
  em <doc:Declarations#Declaration-Modifiers>.
- Inclusão de informações sobre como a inferência de tipos funciona
  com <doc:LexicalStructure#Literals>.
- Mais informações sobre funções curried.
- Inclusão de um novo capítulo sobre <doc:AccessControl>.
- Atualização do capítulo <doc:StringsAndCharacters>
  para refletir que o tipo `Character` do Swift agora representa
  um único cluster de grafemas estendido Unicode.
  Inclui uma nova seção sobre
  <doc:StringsAndCharacters#Extended-Grapheme-Clusters>
  e mais informações sobre
  <doc:StringsAndCharacters#Unicode-Scalar-Values>
  e <doc:StringsAndCharacters#Comparing-Strings>.
- Atualização da seção <doc:StringsAndCharacters#String-Literals>
  para observar que escalares Unicode dentro de literais de string
  agora são escritos como `\u{n}`,
  onde `n` é um número hexadecimal entre 0 e 10FFFF,
  o intervalo do espaço de códigos Unicode.
- A propriedade `length` de `NSString` agora é mapeada para o tipo nativo `String`
  do Swift como `utf16Count`, e não `utf16count`.
- O tipo nativo `String` do Swift não tem mais as propriedades
  `uppercaseString` e `lowercaseString`.
  A seção correspondente em <doc:StringsAndCharacters>
  foi removida, e vários exemplos de código foram atualizados.
- Inclusão de uma nova seção sobre
  <doc:Initialization#Initializer-Parameters-Without-Argument-Labels>.
- Inclusão de uma nova seção sobre
  <doc:Initialization#Required-Initializers>.
- Inclusão de uma nova seção sobre <doc:Functions#Optional-Tuple-Return-Types>.
- Atualização da seção <doc:TheBasics#Type-Annotations> para observar que
  várias variáveis relacionadas podem ser definidas em uma única linha
  com uma única anotação de tipo.
- Os atributos `@optional`, `@lazy`, `@final` e `@required`
  agora são os modificadores de declaração `optional`, `lazy`, `final` e `required`
  de <doc:Declarations#Declaration-Modifiers>.
- Atualização de todo o livro para se referir a `..<`
  como o <doc:BasicOperators#Half-Open-Range-Operator>
  (em vez de “operador de intervalo semifechado”).
- Atualização da seção <doc:CollectionTypes#Accessing-and-Modifying-a-Dictionary>
  para observar que `Dictionary` agora tem uma propriedade booleana `isEmpty`.
- Esclarecimento da lista completa de caracteres que podem ser usados
  ao definir <doc:AdvancedOperators#Custom-Operators>.
- `nil` e os booleanos `true` e `false` agora são <doc:LexicalStructure#Literals>.
- O tipo `Array` do Swift agora tem semântica de valor completa.
  Atualização das informações sobre <doc:CollectionTypes#Mutability-of-Collections>
  e <doc:CollectionTypes#Arrays> para refletir a nova abordagem.
  Também foram esclarecidos o comportamento de atribuição e cópia
  de arrays e dicionários de strings.
- A <doc:CollectionTypes#Array-Type-Shorthand-Syntax> agora é escrita como
  `[SomeType]` em vez de `SomeType[]`.
- Inclusão de uma nova seção sobre <doc:CollectionTypes#Dictionary-Type-Shorthand-Syntax>,
  que é escrita como `[KeyType: ValueType]`.
- Inclusão de uma nova seção sobre <doc:CollectionTypes#Hash-Values-for-Set-Types>.
- Os exemplos de <doc:Closures#Closure-Expressions> agora usam
  a função global `sorted(_:_:)`
  em vez da função global `sort(_:_:)`,
  para refletir a nova semântica de valor dos arrays.
- Atualização das informações sobre <doc:Initialization#Memberwise-Initializers-for-Structure-Types>
  para esclarecer que o inicializador memberwise de struct fica disponível
  mesmo que as propriedades armazenadas da struct não tenham valores padrão.
- Atualização para `..<` em vez de `..`
  no <doc:BasicOperators#Half-Open-Range-Operator>.
- Inclusão de um exemplo de <doc:Generics#Extending-a-Generic-Type>.

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
