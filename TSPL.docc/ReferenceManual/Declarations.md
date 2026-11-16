# Declarações

Introduza tipos, operadores, variáveis e outros nomes e construções.

Uma *declaração* introduz um novo nome ou construção no programa.
Por exemplo, você usa declarações para introduzir funções e métodos,
para introduzir variáveis e constantes,
e para definir tipos enum, struct, classe e protocolo.
Você também pode usar uma declaração para estender o comportamento
de um tipo nomeado existente e para importar para o programa símbolos declarados em outro lugar.

Em Swift, a maioria das declarações também são definições, no sentido de que são implementadas
ou inicializadas no mesmo momento em que são declaradas. Mesmo assim, como protocolos não
implementam seus membros, a maioria dos membros de protocolos são apenas declarações. Por conveniência
e porque essa distinção não é tão importante em Swift,
o termo *declaração* abrange tanto declarações quanto definições.

> Gramática de uma declaração:
>
> *declaration* → *import-declaration* \
> *declaration* → *constant-declaration* \
> *declaration* → *variable-declaration* \
> *declaration* → *typealias-declaration* \
> *declaration* → *function-declaration* \
> *declaration* → *enum-declaration* \
> *declaration* → *struct-declaration* \
> *declaration* → *class-declaration* \
> *declaration* → *actor-declaration* \
> *declaration* → *protocol-declaration* \
> *declaration* → *initializer-declaration* \
> *declaration* → *deinitializer-declaration* \
> *declaration* → *extension-declaration* \
> *declaration* → *subscript-declaration* \
> *declaration* → *macro-declaration* \
> *declaration* → *operator-declaration* \
> *declaration* → *precedence-group-declaration*

## Código de nível superior

O código de nível superior de um arquivo de código-fonte Swift consiste em zero ou mais instruções,
declarações e expressões.
Por padrão, variáveis, constantes e outras declarações nomeadas que são declaradas
no nível superior de um arquivo de código-fonte podem ser acessadas por código
em todo arquivo de código-fonte que faz parte do mesmo módulo.
Você pode substituir esse comportamento padrão
marcando a declaração com um modificador de nível de acesso,
como descrito em <doc:Declarations#Access-Control-Levels>.

Há dois tipos de código de nível superior:
declarações de nível superior e código executável de nível superior.
Declarações de nível superior consistem apenas em declarações,
e são permitidas em todos os arquivos de código-fonte Swift.
Código executável de nível superior contém instruções e expressões,
não apenas declarações,
e é permitido somente como ponto de entrada do programa.

O código Swift que você compila para criar um executável
pode conter no máximo uma das seguintes abordagens
para marcar o ponto de entrada de nível superior,
independentemente de como o código está organizado em arquivos e módulos:
um arquivo que contém código executável de nível superior,
um arquivo `main.swift`,
o atributo `main`,
o atributo `NSApplicationMain`,
ou o atributo `UIApplicationMain`.

> Gramática de uma declaração de nível superior:
>
> *top-level-declaration* → *statements*_?_

## Blocos de código

Um *bloco de código* é usado por diversas declarações e estruturas de controle
para agrupar instruções.
Ele tem a seguinte forma:

```swift
{
   <#statements#>
}
```

As *instruções* dentro de um bloco de código incluem declarações,
expressões e outros tipos de instruções, e são executadas em ordem
de aparição no código-fonte.

<!--
  TR: What exactly are the scope rules for Swift?
-->

<!--
  TODO: Discuss scope.  I assume a code block creates a new scope?
-->

> Gramática de um bloco de código:
>
> *code-block* → **`{`** *statements*_?_ **`}`**

## Declaração de importação

Uma *declaração de importação* permite acessar símbolos
que são declarados fora do arquivo atual.
A forma básica importa o módulo inteiro;
ela consiste na palavra-chave `import` seguida do nome do módulo:

```swift
import <#module#>
```

Fornecer mais detalhes limita quais símbolos são importados ---
você pode especificar um submódulo específico
ou uma declaração específica dentro de um módulo ou submódulo.
Quando essa forma detalhada é usada,
somente o símbolo importado
(e não o módulo que o declara)
fica disponível no escopo atual.

```swift
import <#import kind#> <#module#>.<#symbol name#>
import <#module#>.<#submodule#>
```

<!--
  TODO: Need to add more to this section.
-->

> Gramática de uma declaração de importação:
>
> *import-declaration* → *attributes*_?_ **`import`** *import-kind*_?_ *import-path*
>
> *import-kind* → **`typealias`** | **`struct`** | **`class`** | **`enum`** | **`protocol`** | **`let`** | **`var`** | **`func`** \
> *import-path* → *identifier* | *identifier* **`.`** *import-path*

## Declaração de constante

Uma *declaração de constante* introduz um valor nomeado constante no programa.
Declarações de constantes são feitas com a palavra-chave `let` e têm a seguinte forma:

```swift
let <#constant name#>: <#type#> = <#expression#>
```

Uma declaração de constante define uma vinculação imutável entre o *nome da constante*
e o valor da *expressão* de inicialização;
depois que o valor de uma constante é definido, ele não pode mais ser alterado.
Mesmo assim, se uma constante for inicializada com uma instância de classe,
o objeto em si pode mudar,
mas a vinculação entre o nome da constante e o objeto ao qual ela se refere não pode.

Quando uma constante é declarada no escopo global,
ela precisa ser inicializada com um valor.
Quando uma declaração de constante ocorre no contexto de uma função ou método,
ela pode ser inicializada depois,
desde que seja garantido que ela tenha um valor definido
antes da primeira vez que seu valor for lido.
Se o compilador conseguir provar que o valor da constante nunca é lido,
a constante não precisa ter nenhum valor definido.
Essa análise é chamada de *inicialização definitiva* ---
o compilador prova que um valor é definitivamente atribuído antes de ser lido.

> Nota:
> A inicialização definitiva
> não consegue construir provas que exijam conhecimento do domínio,
> e sua capacidade de acompanhar o estado através de condicionais tem um limite.
> Se você consegue determinar que uma constante sempre tem um valor definido,
> mas o compilador não consegue provar isso,
> tente simplificar os caminhos de código que definem o valor,
> ou use uma declaração de variável.

<!--
In the most general case,
DI reduces to the halting problem,
as shown by Rice's theorem.
-->

Quando uma declaração de constante ocorre no contexto de uma declaração de classe ou struct,
ela é considerada uma *propriedade constante*.
Declarações de constantes não são propriedades computadas e, por isso, não têm getters
ou setters.

Se o *nome da constante* de uma declaração de constante for um padrão de tupla,
o nome de cada item da tupla é vinculado ao valor correspondente
na *expressão* de inicialização.

```swift
let (firstNumber, secondNumber) = (10, 42)
```

<!--
  - test: `constant-decl`

  ```swifttest
  -> let (firstNumber, secondNumber) = (10, 42)
  ```
-->

Neste exemplo,
`firstNumber` é uma constante nomeada para o valor `10`,
e `secondNumber` é uma constante nomeada para o valor `42`.
Ambas as constantes agora podem ser usadas de forma independente:

```swift
print("The first number is \(firstNumber).")
// Prints "The first number is 10."
print("The second number is \(secondNumber).")
// Prints "The second number is 42."
```

<!--
  - test: `constant-decl`

  ```swifttest
  -> print("The first number is \(firstNumber).")
  <- The first number is 10.
  -> print("The second number is \(secondNumber).")
  <- The second number is 42.
  ```
-->

A anotação de tipo (`:` *type*) é opcional em uma declaração de constante
quando o tipo do *nome da constante* pode ser inferido,
como descrito em <doc:Types#Type-Inference>.

Para declarar uma propriedade de tipo constante,
marque a declaração com o modificador de declaração `static`.
Uma propriedade de tipo constante de uma classe é sempre implicitamente final;
você não pode marcá-la com o modificador de declaração `class` ou `final`
para permitir ou proibir a sobrescrita por subclasses.
Propriedades de tipo são discutidas em <doc:Properties#Type-Properties>.

<!--
  - test: `class-constants-cant-have-class-or-final`

  ```swifttest
  -> class Super { class let x = 10 }
  !$ error: class stored properties not supported in classes; did you mean 'static'?
  !! class Super { class let x = 10 }
  !!               ~~~~~     ^
  -> class S { static final let x = 10 }
  !$ error: static declarations are already final
  !! class S { static final let x = 10 }
  !!                  ^~~~~~
  !!-
  ```
-->

Para mais informações sobre constantes e orientações sobre quando usá-las,
veja <doc:TheBasics#Constants-and-Variables> e <doc:Properties#Stored-Properties>.

> Gramática de uma declaração de constante:
>
> *constant-declaration* → *attributes*_?_ *declaration-modifiers*_?_ **`let`** *pattern-initializer-list*
>
> *pattern-initializer-list* → *pattern-initializer* | *pattern-initializer* **`,`** *pattern-initializer-list* \
> *pattern-initializer* → *pattern* *initializer*_?_ \
> *initializer* → **`=`** *expression*

## Declaração de variável

Uma *declaração de variável* introduz um valor nomeado mutável no programa
e é feita com a palavra-chave `var`.

Declarações de variáveis têm várias formas, que declaram diferentes tipos
de valores nomeados e mutáveis,
incluindo variáveis e propriedades armazenadas e computadas,
observadores de variáveis e propriedades armazenadas e propriedades de variáveis estáticas.
A forma adequada a usar depende
do escopo em que a variável é declarada e do tipo de variável que você pretende declarar.

> Nota: Você também pode declarar propriedades no contexto de uma declaração de protocolo,
> como descrito em <doc:Declarations#Protocol-Property-Declaration>.

Você pode substituir uma propriedade em uma subclasse marcando a declaração da propriedade da subclasse
com o modificador de declaração `override`, como descrito em <doc:Inheritance#Overriding>.

### Variáveis armazenadas e propriedades armazenadas

A forma a seguir declara uma variável armazenada ou uma propriedade de variável armazenada:

```swift
var <#variable name#>: <#type#> = <#expression#>
```

Você define essa forma de declaração de variável no escopo global, no escopo local
de uma função ou no contexto de uma declaração de classe ou struct.
Quando uma declaração de variável desta forma é feita no escopo global ou no escopo local
de uma função, ela é chamada de *variável armazenada*.
Quando é declarada no contexto de uma declaração de classe ou struct,
ela é chamada de *propriedade de variável armazenada*.

A *expressão* de inicialização não pode estar presente em uma declaração de protocolo,
mas em todos os outros contextos, a *expressão* de inicialização é opcional.
Ainda assim, se nenhuma *expressão* de inicialização estiver presente,
a declaração de variável precisa incluir uma anotação de tipo explícita (`:` *type*).

Assim como nas declarações de constantes,
se uma declaração de variável omitir a *expressão* de inicialização,
a variável precisa ter um valor definido antes da primeira vez que for lida.
Também como nas declarações de constantes,
se o *nome da variável* for um padrão de tupla,
o nome de cada item da tupla é vinculado ao valor correspondente
na *expressão* de inicialização.

Como o nome sugere, o valor de uma variável armazenada ou de uma propriedade de variável armazenada
é guardado na memória.

### Variáveis computadas e propriedades computadas

A forma a seguir declara uma variável computada ou uma propriedade computada:

```swift
var <#variable name#>: <#type#> {
   get {
      <#statements#>
   }
   set(<#setter name#>) {
      <#statements#>
   }
}
```

Você define essa forma de declaração de variável no escopo global, no escopo local
de uma função ou no contexto de uma declaração de classe, struct, enum ou extension.
Quando uma declaração de variável desta forma é feita no escopo global ou no escopo local
de uma função, ela é chamada de *variável computada*.
Quando é declarada no contexto de uma declaração de classe,
struct ou extension, ela é chamada de *propriedade computada*.

O getter é usado para ler o valor,
e o setter é usado para escrever o valor.
A cláusula de setter é opcional,
e quando só é preciso um getter, você pode omitir as duas cláusulas e simplesmente
retornar o valor solicitado diretamente,
como descrito em <doc:Properties#Read-Only-Computed-Properties>.
Mas se você fornecer uma cláusula de setter, também precisa fornecer uma cláusula de getter.

O *nome do setter* e os parênteses que o envolvem são opcionais.
Se você fornecer um nome para o setter, ele é usado como nome do parâmetro do setter.
Se você não fornecer um nome para o setter, o nome padrão do parâmetro do setter é `newValue`,
como descrito em <doc:Properties#Shorthand-Setter-Declaration>.

Diferentemente dos valores nomeados armazenados e das propriedades de variáveis armazenadas,
o valor de um valor nomeado computado ou de uma propriedade computada não é guardado na memória.

Para mais informações e para ver exemplos de propriedades computadas,
veja <doc:Properties#Computed-Properties>.

### Observadores de variáveis armazenadas e observadores de propriedades

Você também pode declarar uma variável ou propriedade armazenada com observadores `willSet` e `didSet`.
Uma variável ou propriedade armazenada declarada com observadores tem a seguinte forma:

```swift
var <#variable name#>: <#type#> = <#expression#> {
   willSet(<#setter name#>) {
      <#statements#>
   }
   didSet(<#setter name#>) {
      <#statements#>
   }
}
```

Você define essa forma de declaração de variável no escopo global, no escopo local
de uma função ou no contexto de uma declaração de classe ou struct.
Quando uma declaração de variável desta forma é feita no escopo global ou no escopo local
de uma função, os observadores são chamados de *observadores de variáveis armazenadas*.
Quando é declarada no contexto de uma declaração de classe ou struct,
os observadores são chamados de *observadores de propriedade*.

Você pode adicionar observadores de propriedade a qualquer propriedade armazenada. Você também pode adicionar
observadores de propriedade a qualquer propriedade herdada (armazenada ou computada) ao sobrescrever
a propriedade dentro de uma subclasse, como descrito em <doc:Inheritance#Overriding-Property-Observers>.

A *expressão* de inicialização é opcional no contexto de uma declaração de classe ou struct,
mas obrigatória nos demais casos. A anotação de *tipo* é opcional
quando o tipo pode ser inferido a partir da *expressão* de inicialização.
Essa expressão é avaliada na primeira vez que você lê o valor da propriedade.
Se você sobrescrever o valor inicial da propriedade sem lê-lo,
essa expressão é avaliada antes da primeira vez que você escrever na propriedade.

<!--
  - test: `overwriting-property-without-writing`

  ```swifttest
  >> func loudConst(_ x: Int) -> Int {
  >>     print("initial value:", x)
  >>     return x
  >> }
  >> var x = loudConst(10)
  >> x = 20
  >> print("x:", x)
  << initial value: 10
  << x: 20
  >> var y = loudConst(100)
  >> print("y:", y)
  << initial value: 100
  << y: 100
  ```
-->

Os observadores `willSet` e `didSet` oferecem uma forma de observar (e de responder adequadamente)
quando o valor de uma variável ou propriedade está sendo definido.
Os observadores não são chamados quando a variável ou propriedade
é inicializada pela primeira vez.
Em vez disso, eles são chamados somente quando o valor é definido fora de um contexto de inicialização.

Um observador `willSet` é chamado logo antes de o valor da variável ou propriedade
ser definido. O novo valor é passado ao observador `willSet` como uma constante,
por isso ele não pode ser alterado na implementação da cláusula `willSet`.
O observador `didSet` é chamado imediatamente depois que o novo valor é definido. Diferentemente
do observador `willSet`, o valor antigo da variável ou propriedade
é passado ao observador `didSet`, caso você ainda precise acessá-lo. Mesmo assim,
se você atribuir um valor a uma variável ou propriedade dentro da própria cláusula `didSet`,
esse novo valor substituirá o que acabou de ser definido e foi passado ao
observador `willSet`.

O *nome do setter* e os parênteses que o envolvem nas cláusulas `willSet` e `didSet` são opcionais.
Se você fornecer nomes para os setters,
eles são usados como nomes dos parâmetros dos observadores `willSet` e `didSet`.
Se você não fornecer nomes para os setters,
o nome padrão do parâmetro do observador `willSet` é `newValue`
e o nome padrão do parâmetro do observador `didSet` é `oldValue`.

A cláusula `didSet` é opcional quando você fornece uma cláusula `willSet`.
Da mesma forma, a cláusula `willSet` é opcional quando você fornece uma cláusula `didSet`.

Se o corpo do observador `didSet` se referir ao valor antigo,
o getter é chamado antes do observador,
para disponibilizar o valor antigo.
Caso contrário, o novo valor é armazenado sem chamar o getter da superclasse.
O exemplo abaixo mostra uma propriedade computada definida pela superclasse
e sobrescrita por suas subclasses para adicionar um observador.

```swift
class Superclass {
    private var xValue = 12
    var x: Int {
        get { print("Getter was called"); return xValue }
        set { print("Setter was called"); xValue = newValue }
    }
}

// This subclass doesn't refer to oldValue in its observer, so the
// superclass's getter is called only once to print the value.
class New: Superclass {
    override var x: Int {
        didSet { print("New value \(x)") }
    }
}
let new = New()
new.x = 100
// Prints "Setter was called".
// Prints "Getter was called".
// Prints "New value 100".

// This subclass refers to oldValue in its observer, so the superclass's
// getter is called once before the setter, and again to print the value.
class NewAndOld: Superclass {
    override var x: Int {
        didSet { print("Old value \(oldValue) - new value \(x)") }
    }
}
let newAndOld = NewAndOld()
newAndOld.x = 200
// Prints "Getter was called".
// Prints "Setter was called".
// Prints "Getter was called".
// Prints "Old value 12 - new value 200".
```

<!--
  - test: `didSet-calls-superclass-getter`

  ```swifttest
  -> class Superclass {
         private var xValue = 12
         var x: Int {
             get { print("Getter was called"); return xValue }
             set { print("Setter was called"); xValue = newValue }
         }
     }

  // This subclass doesn't refer to oldValue in its observer, so the
  // superclass's getter is called only once to print the value.
  -> class New: Superclass {
         override var x: Int {
             didSet { print("New value \(x)") }
         }
     }
     let new = New()
     new.x = 100
  <- Setter was called
  <- Getter was called
  <- New value 100

  // This subclass refers to oldValue in its observer, so the superclass's
  // getter is called once before the setter, and again to print the value.
  -> class NewAndOld: Superclass {
         override var x: Int {
             didSet { print("Old value \(oldValue) - new value \(x)") }
         }
     }
     let newAndOld = NewAndOld()
     newAndOld.x = 200
  <- Getter was called
  <- Setter was called
  <- Getter was called
  <- Old value 12 - new value 200
  ```
-->

Para mais informações e para ver um exemplo de como usar observadores de propriedade,
veja <doc:Properties#Property-Observers>.

<!--
  - test: `cant-mix-get-set-and-didSet`

  ```swifttest
  >> struct S {
  >>     var x: Int {
  >>         get { print("S getter"); return 12 }
  >>         set { return }
  >>         didSet { print("S didSet") }
  >>     }
  >> }
  !$ error: 'didSet' cannot be provided together with a getter
  !! didSet { print("S didSet") }
  !! ^
  ```
-->

### Propriedades variáveis de tipo

Para declarar uma propriedade variável de tipo,
marque a declaração com o modificador de declaração `static`.
Classes podem, em vez disso, marcar propriedades computadas de tipo com o modificador de declaração `class`
para permitir que subclasses sobrescrevam a implementação da superclasse.
Propriedades de tipo são discutidas em <doc:Properties#Type-Properties>.

> Gramática de uma declaração de variável:
>
> *variable-declaration* → *variable-declaration-head* *pattern-initializer-list* \
> *variable-declaration* → *variable-declaration-head* *variable-name* *type-annotation* *code-block* \
> *variable-declaration* → *variable-declaration-head* *variable-name* *type-annotation* *getter-setter-block* \
> *variable-declaration* → *variable-declaration-head* *variable-name* *type-annotation* *getter-setter-keyword-block* \
> *variable-declaration* → *variable-declaration-head* *variable-name* *initializer* *willSet-didSet-block* \
> *variable-declaration* → *variable-declaration-head* *variable-name* *type-annotation* *initializer*_?_ *willSet-didSet-block*
>
> *variable-declaration-head* → *attributes*_?_ *declaration-modifiers*_?_ **`var`** \
> *variable-name* → *identifier*
>
> *getter-setter-block* → *code-block* \
> *getter-setter-block* → **`{`** *getter-clause* *setter-clause*_?_ **`}`** \
> *getter-setter-block* → **`{`** *setter-clause* *getter-clause* **`}`** \
> *getter-clause* → *attributes*_?_ *mutation-modifier*_?_ **`get`** *code-block* \
> *setter-clause* → *attributes*_?_ *mutation-modifier*_?_ **`set`** *setter-name*_?_ *code-block* \
> *setter-name* → **`(`** *identifier* **`)`**
>
> *getter-setter-keyword-block* → **`{`** *getter-keyword-clause* *setter-keyword-clause*_?_ **`}`** \
> *getter-setter-keyword-block* → **`{`** *setter-keyword-clause* *getter-keyword-clause* **`}`** \
> *getter-keyword-clause* → *attributes*_?_ *mutation-modifier*_?_ **`get`** \
> *setter-keyword-clause* → *attributes*_?_ *mutation-modifier*_?_ **`set`**
>
> *willSet-didSet-block* → **`{`** *willSet-clause* *didSet-clause*_?_ **`}`** \
> *willSet-didSet-block* → **`{`** *didSet-clause* *willSet-clause*_?_ **`}`** \
> *willSet-clause* → *attributes*_?_ **`willSet`** *setter-name*_?_ *code-block* \
> *didSet-clause* → *attributes*_?_ **`didSet`** *setter-name*_?_ *code-block*

<!--
  NOTE: Type annotations are required for computed properties -- the
  types of those properties aren't computed/inferred.
-->

## Declaração de alias de tipo

Uma *declaração de alias de tipo* introduz um alias nomeado para um tipo existente no programa.
Declarações de alias de tipo são feitas com a palavra-chave `typealias` e têm a seguinte forma:

```swift
typealias <#name#> = <#existing type#>
```

Depois que um alias de tipo é declarado, o *nome* do alias pode ser usado
no lugar do *tipo existente* em qualquer parte do programa.
O *tipo existente* pode ser um tipo nomeado ou um tipo composto.
Aliases de tipo não criam novos tipos;
eles apenas permitem que um nome se refira a um tipo existente.

Uma declaração de alias de tipo pode usar parâmetros genéricos
para dar um nome a um tipo genérico existente. O alias de tipo
pode fornecer tipos concretos para alguns ou todos os parâmetros genéricos
do tipo existente.
Por exemplo:

```swift
typealias StringDictionary<Value> = Dictionary<String, Value>

// The following dictionaries have the same type.
var dictionary1: StringDictionary<Int> = [:]
var dictionary2: Dictionary<String, Int> = [:]
```

<!--
  - test: `typealias-with-generic`

  ```swifttest
  -> typealias StringDictionary<Value> = Dictionary<String, Value>

  // The following dictionaries have the same type.
  -> var dictionary1: StringDictionary<Int> = [:]
  -> var dictionary2: Dictionary<String, Int> = [:]
  ```
-->

Quando um alias de tipo é declarado com parâmetros genéricos, as restrições sobre esses
parâmetros precisam corresponder exatamente às restrições dos parâmetros genéricos do tipo existente.
Por exemplo:

```swift
typealias DictionaryOfInts<Key: Hashable> = Dictionary<Key, Int>
```

<!--
  - test: `typealias-with-generic-constraint`

  ```swifttest
  -> typealias DictionaryOfInts<Key: Hashable> = Dictionary<Key, Int>
  ```
-->

Como o alias de tipo e o tipo existente podem ser usados de forma intercambiável,
o alias de tipo não pode introduzir restrições genéricas adicionais.

Um alias de tipo pode repassar os parâmetros genéricos de um tipo existente
omitindo todos os parâmetros genéricos da declaração.
Por exemplo,
o alias de tipo `Diccionario` declarado aqui
tem os mesmos parâmetros genéricos e restrições que `Dictionary`.

```swift
typealias Diccionario = Dictionary
```

<!--
  - test: `typealias-using-shorthand`

  ```swifttest
  -> typealias Diccionario = Dictionary
  ```
-->

<!--
  Note that the compiler doesn't currently enforce this. For example, this works but shouldn't:
  typealias ProvidingMoreSpecificConstraints<T: Comparable & Hashable> = Dictionary<T, Int>
-->

<!--
  Things that shouldn't work:
  typealias NotRedeclaringSomeOfTheGenericParameters = Dictionary<T, String>
  typealias NotRedeclaringAnyOfTheGenericParameters = Dictionary
  typealias NotProvidingTheCorrectConstraints<T> = Dictionary<T, Int>
  typealias ProvidingMoreSpecificConstraints<T: Comparable & Hashable> = Dictionary<T, Int>
-->

Dentro de uma declaração de protocolo,
um alias de tipo pode dar um nome mais curto e mais conveniente
a um tipo que é usado com frequência.
Por exemplo:

```swift
protocol Sequence {
    associatedtype Iterator: IteratorProtocol
    typealias Element = Iterator.Element
}

func sum<T: Sequence>(_ sequence: T) -> Int where T.Element == Int {
    // ...
}
```

<!--
  - test: `typealias-in-protocol`

  ```swifttest
  -> protocol Sequence {
         associatedtype Iterator: IteratorProtocol
         typealias Element = Iterator.Element
     }

  -> func sum<T: Sequence>(_ sequence: T) -> Int where T.Element == Int {
         // ...
  >>     return 9000
     }
  ```
-->

Sem esse alias de tipo,
a função `sum` teria que se referir ao tipo associado
como `T.Iterator.Element` em vez de `T.Element`.

Veja também <doc:Declarations#Protocol-Associated-Type-Declaration>.

> Gramática de uma declaração de alias de tipo:
>
> *typealias-declaration* → *attributes*_?_ *access-level-modifier*_?_ **`typealias`** *typealias-name* *generic-parameter-clause*_?_ *typealias-assignment* \
> *typealias-name* → *identifier* \
> *typealias-assignment* → **`=`** *type*

<!--
  Old grammar:
  typealias-declaration -> typealias-head typealias-assignment
  typealias-head -> ``typealias`` typealias-name type-inheritance-clause-OPT
  typealias-name -> identifier
  typealias-assignment -> ``=`` type
-->


## Declaração de função

Uma *declaração de função* introduz uma função ou método no programa.
Uma função declarada no contexto de uma classe, struct, enum ou protocolo
é chamada de *método*.
Declarações de função são feitas com a palavra-chave `func` e têm a seguinte forma:

```swift
func <#function name#>(<#parameters#>) -> <#return type#> {
   <#statements#>
}
```

Se a função tiver o tipo de retorno `Void`,
o tipo de retorno pode ser omitido, como em:

```swift
func <#function name#>(<#parameters#>) {
   <#statements#>
}
```

O tipo de cada parâmetro deve ser informado:
ele não pode ser inferido.
Se você escrever `inout` antes do tipo de um parâmetro,
o parâmetro pode ser modificado dentro do escopo da função.
Parâmetros in-out são discutidos em detalhes
em <doc:Declarations#In-Out-Parameters>, mais abaixo.

Uma declaração de função cujas *instruções*
incluem apenas uma única expressão
retorna implicitamente o valor dessa expressão.
Essa sintaxe de retorno implícito só vale
somente quando o tipo da expressão e o tipo de retorno da função
não são `Void`
e não são um enum como `Never` que não tem nenhum caso.

<!--
  As of Swift 5.3,
  the only way to make an uninhabited type is to create an empty enum,
  so just say that directly instead of using & defining the compiler jargon.
-->

Funções podem retornar múltiplos valores usando um tipo tupla
como tipo de retorno da função.

<!--
  TODO: ^-- Add some more here.
-->

A definição de uma função pode aparecer dentro de outra declaração de função.
Esse tipo de função é conhecido como *função aninhada*.

Uma função aninhada é nonescaping se capturar
um valor que é garantido nunca escapar,
como um parâmetro in-out,
ou se for passada como argumento de função nonescaping.
Caso contrário, a função aninhada é uma função escaping.

Para uma discussão sobre funções aninhadas,
veja <doc:Functions#Nested-Functions>.

### Nomes de parâmetros

Parâmetros de função formam uma lista separada por vírgulas,
em que cada parâmetro tem uma de várias formas.
A ordem dos argumentos em uma chamada de função
deve corresponder à ordem dos parâmetros na declaração da função.
A entrada mais simples em uma lista de parâmetros tem a seguinte forma:

```swift
<#parameter name#>: <#parameter type#>
```

Um parâmetro tem um nome,
que é usado dentro do corpo da função,
e também um rótulo de argumento,
que é usado ao chamar a função ou o método.
Por padrão,
os nomes dos parâmetros também são usados como rótulos de argumento.
Por exemplo:

```swift
func f(x: Int, y: Int) -> Int { return x + y }
f(x: 1, y: 2) // both x and y are labeled
```

<!--
  - test: `default-parameter-names`

  ```swifttest
  -> func f(x: Int, y: Int) -> Int { return x + y }
  >> let r0 =
  -> f(x: 1, y: 2) // both x and y are labeled
  >> assert(r0 == 3)
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

Você pode substituir o comportamento padrão dos rótulos de argumento
com uma das seguintes formas:

```swift
<#argument label#> <#parameter name#>: <#parameter type#>
_ <#parameter name#>: <#parameter type#>
```

Um nome antes do nome do parâmetro
dá ao parâmetro um rótulo de argumento explícito,
que pode ser diferente do nome do parâmetro.
O argumento correspondente deve usar esse rótulo de argumento
nas chamadas de função ou de método.

Um sublinhado (`_`) antes do nome de um parâmetro
suprime o rótulo de argumento.
O argumento correspondente não deve ter rótulo nas chamadas de função ou de método.

```swift
func repeatGreeting(_ greeting: String, count n: Int) { /* Greet n times */ }
repeatGreeting("Hello, world!", count: 2) //  count is labeled, greeting is not
```

<!--
  - test: `overridden-parameter-names`

  ```swifttest
  -> func repeatGreeting(_ greeting: String, count n: Int) { /* Greet n times */ }
  -> repeatGreeting("Hello, world!", count: 2) //  count is labeled, greeting is not
  ```
-->

### Modificadores de parâmetro

Um *modificador de parâmetro* muda a forma como um argumento é passado para a função.

```swift
<#argument label#> <#parameter name#>: <#parameter modifier#> <#parameter type#>
```

Para usar um modificador de parâmetro,
escreva `inout`, `borrowing` ou `consuming`
antes do tipo do argumento.

```swift
func someFunction(a: inout A, b: consuming B, c: C) { ... }
```

#### Parâmetros in-out

Por padrão, argumentos de função em Swift são passados por valor:
quaisquer mudanças feitas dentro da função não são visíveis para quem chamou.
Para criar um parâmetro in-out,
você aplica o modificador de parâmetro `inout`.

```swift
func someFunction(a: inout Int) {
    a += 1
}
```

Ao chamar uma função que inclui parâmetros in-out,
o argumento in-out deve ser precedido de um e comercial (`&`)
para marcar que a chamada da função pode alterar o valor do argumento.

```swift
var x = 7
someFunction(a: &x)
print(x)  // Prints "8"
```

Parâmetros in-out são passados da seguinte forma:

1. Quando a função é chamada,
   o valor do argumento é copiado.
2. No corpo da função,
   a cópia é modificada.
3. Quando a função retorna,
   o valor da cópia é atribuído ao argumento original.

Esse comportamento é conhecido como *copy-in copy-out*
ou *call by value result*.
Por exemplo,
quando uma propriedade computada ou uma propriedade com observadores
é passada como parâmetro in-out,
seu getter é chamado como parte da chamada da função
e seu setter é chamado como parte do retorno da função.

Como otimização,
quando o argumento é um valor armazenado em um endereço físico na memória,
a mesma posição de memória é usada tanto dentro quanto fora do corpo da função.
Esse comportamento otimizado é conhecido como *call by reference*;
ele atende a todos os requisitos
do modelo copy-in copy-out
e elimina o custo da cópia.
Escreva seu código seguindo o modelo copy-in copy-out,
sem depender da otimização call by reference,
para que ele se comporte corretamente com ou sem a otimização.

Dentro de uma função, não acesse um valor que foi passado como argumento in-out,
mesmo que o valor original esteja disponível no escopo atual.
Acessar o original é um acesso simultâneo ao valor,
o que viola a exclusividade de memória.

```swift
var someValue: Int
func someFunction(a: inout Int) {
    a += someValue
}

// Error: This causes a runtime exclusivity violation
someFunction(a: &someValue)
```

Pelo mesmo motivo,
você não pode passar o mesmo valor para múltiplos parâmetros in-out.

```swift
var someValue: Int
func someFunction(a: inout Int, b: inout Int) {
    a += b
    b += 1
}

// Error: Cannot pass the same value to multiple in-out parameters
someFunction(a: &someValue, b: &someValue)
```

Para mais informações sobre segurança de memória e exclusividade de memória,
veja <doc:MemorySafety>.

<!--
  When the call-by-reference optimization is in play,
  it would happen to do what you want.
  But you still shouldn't do that --
  as noted above, you're not allowed to depend on
  behavioral differences that happen because of call by reference.
-->

Um closure ou uma função aninhada
que captura um parâmetro in-out deve ser nonescaping.
Se você precisar capturar um parâmetro in-out
sem modificá-lo,
use uma lista de captura para capturar explicitamente o parâmetro de forma imutável.

```swift
func someFunction(a: inout Int) -> () -> Int {
    return { [a] in return a + 1 }
}
```

<!--
  - test: `explicit-capture-for-inout`

  ```swifttest
  -> func someFunction(a: inout Int) -> () -> Int {
         return { [a] in return a + 1 }
     }
  >> class C { var x = 100 }
  >> let c = C()
  >> let f = someFunction(a: &c.x)
  >> c.x = 200
  >> let r = f()
  >> print(r, r == c.x)
  << 101 false
  ```
-->

Se você precisar capturar e modificar um parâmetro in-out,
use uma cópia local explícita,
como em código multithread que garante
que toda a modificação terminou antes de a função retornar.

```swift
func multithreadedFunction(queue: DispatchQueue, x: inout Int) {
    // Make a local copy and manually copy it back.
    var localX = x
    defer { x = localX }

    // Operate on localX asynchronously, then wait before returning.
    queue.async { someMutatingOperation(&localX) }
    queue.sync {}
}
```

<!--
  - test: `cant-pass-inout-aliasing`

  ```swifttest
  >> import Dispatch
  >> func someMutatingOperation(_ a: inout Int) {}
  -> func multithreadedFunction(queue: DispatchQueue, x: inout Int) {
        // Make a local copy and manually copy it back.
        var localX = x
        defer { x = localX }

        // Operate on localX asynchronously, then wait before returning.
        queue.async { someMutatingOperation(&localX) }
        queue.sync {}
     }
  ```
-->

Para mais discussão e exemplos de parâmetros in-out,
veja <doc:Functions#In-Out-Parameters>.

<!--
  - test: `escaping-cant-capture-inout`

  ```swifttest
  -> func outer(a: inout Int) -> () -> Void {
         func inner() {
             a += 1
         }
         return inner
     }
  !$ error: escaping local function captures 'inout' parameter 'a'
  !! return inner
  !! ^
  !$ note: parameter 'a' is declared 'inout'
  !! func outer(a: inout Int) -> () -> Void {
  !! ^
  !$ note: captured here
  !! a += 1
  !! ^
  -> func closure(a: inout Int) -> () -> Void {
         return { a += 1 }
     }
  !$ error: escaping closure captures 'inout' parameter 'a'
  !! return { a += 1 }
  !! ^
  !$ note: parameter 'a' is declared 'inout'
  !! func closure(a: inout Int) -> () -> Void {
  !! ^
  !$ note: captured here
  !! return { a += 1 }
  !! ^
  ```
-->

#### Parâmetros borrowing e consuming

Por padrão, Swift usa um conjunto de regras
para gerenciar automaticamente o tempo de vida dos objetos entre chamadas de função,
copiando valores quando necessário.
As regras padrão são feitas para minimizar o custo na maioria dos casos.
Se você quiser um controle mais específico,
pode aplicar o modificador de parâmetro `borrowing` ou `consuming`.
Nesse caso,
use `copy` para marcar explicitamente as operações de cópia.
Além disso,
valores de um tipo não copiável devem ser passados como borrowing ou consuming.

Independentemente de você usar as regras padrão, o Swift garante que o tempo de vida
e a posse dos objetos sejam gerenciados corretamente em todos os casos.
Esses modificadores de parâmetro afetam apenas a eficiência relativa
de padrões de uso específicos, não a corretude.

<!--
TODO: Describe the default rules.
Essentially, inits and property setters are consuming,
and everything else is borrowing.
Where are copies implicitly inserted?
-->

O modificador `borrowing` indica que a função
não guarda o valor do parâmetro.
Nesse caso, quem chama mantém a posse do objeto
e a responsabilidade pelo tempo de vida dele.
Usar `borrowing` minimiza o custo quando a função
usa o objeto apenas de forma transitória.

```swift
// `isLessThan` does not keep either argument
func isLessThan(lhs: borrowing A, rhs: borrowing A) -> Bool {
    ...
}
```

Se a função precisar guardar o valor do parâmetro,
por exemplo, armazenando-o em uma variável global,
use `copy` para copiar explicitamente esse valor.

```swift
// As above, but this `isLessThan` also wants to record the smallest value
func isLessThan(lhs: borrowing A, rhs: borrowing A) -> Bool {
    if lhs < storedValue {
        storedValue = copy lhs
    } else if rhs < storedValue {
        storedValue = copy rhs
    }
    return lhs < rhs
}
```

Por outro lado,
o modificador de parâmetro `consuming` indica
que a função toma a posse do valor,
assumindo a responsabilidade de armazená-lo ou destruí-lo
antes de a função retornar.

```swift
// `store` keeps its argument, so mark it `consuming`
func store(a: consuming A) {
    someGlobalVariable = a
}
```

Usar `consuming` minimiza o custo quando quem chama
não precisa mais usar o objeto depois da chamada da função.

```swift
// Usually, this is the last thing you do with a value
store(a: value)
```

Se você continuar usando um objeto copiável depois da chamada da função,
o compilador faz automaticamente uma cópia desse objeto
antes da chamada da função.

```swift
// The compiler inserts an implicit copy here
store(a: someValue)  // This function consumes someValue
print(someValue)  // This uses the copy of someValue
```

Diferentemente de `inout`, parâmetros `borrowing` e `consuming`
não exigem nenhuma notação especial
quando você chama a função:

```swift
func someFunction(a: borrowing A, b: consuming B) { ... }

someFunction(a: someA, b: someB)
```

O uso explícito de `borrowing` ou `consuming`
indica sua intenção de controlar com mais precisão
o custo do gerenciamento de posse em tempo de execução.
Como cópias podem causar operações inesperadas de posse em tempo de execução,
parâmetros marcados com um desses modificadores
não podem ser copiados, a menos que você
use a palavra-chave explícita `copy`:

```swift
func borrowingFunction1(a: borrowing A) {
    // Error: Cannot implicitly copy a
    // This assignment requires a copy because
    // `a` is only borrowed from the caller.
    someGlobalVariable = a
}

func borrowingFunction2(a: borrowing A) {
    // OK: Explicit copying works
    someGlobalVariable = copy a
}

func consumingFunction1(a: consuming A) {
    // Error: Cannot implicitly copy a
    // This assignment requires a copy because
    // of the following `print`
    someGlobalVariable = a
    print(a)
}

func consumingFunction2(a: consuming A) {
    // OK: Explicit copying works regardless
    someGlobalVariable = copy a
    print(a)
}

func consumingFunction3(a: consuming A) {
    // OK: No copy needed here because this is the last use
    someGlobalVariable = a
}
```

<!--
  TODO: `borrowing` and `consuming` keywords with noncopyable argument types
-->
<!--
  TODO: Any change of parameter modifier is ABI-breaking
-->

### Tipos especiais de parâmetros

Parâmetros podem ser ignorados,
receber um número variável de valores
e ter valores padrão,
usando as seguintes formas:

```swift
_ : <#parameter type#>
<#parameter name#>: <#parameter type#>...
<#parameter name#>: <#parameter type#> = <#default argument value#>
```

Um parâmetro sublinhado (`_`)
é explicitamente ignorado e não pode ser acessado dentro do corpo da função.

Um parâmetro cujo tipo base é seguido imediatamente por três pontos (`...`)
é entendido como parâmetro variádico.
Um parâmetro que vem logo depois de um parâmetro variádico
precisa ter um rótulo de argumento.
Uma função pode ter múltiplos parâmetros variádicos.
Um parâmetro variádico é tratado como um array que contém elementos do tipo base.
Por exemplo, o parâmetro variádico `Int...` é tratado como `[Int]`.
Para um exemplo que usa parâmetro variádico,
veja <doc:Functions#Variadic-Parameters>.

Um parâmetro com um sinal de igual (`=`) e uma expressão depois do tipo
é entendido como tendo um valor padrão igual à expressão dada.
A expressão dada é avaliada quando a função é chamada.
Se o parâmetro for omitido na chamada da função,
o valor padrão é usado no lugar.

```swift
func f(x: Int = 42) -> Int { return x }
f()       // Valid, uses default value
f(x: 7)   // Valid, uses the value provided
f(7)      // Invalid, missing argument label
```

<!--
  - test: `default-args-and-labels`

  ```swifttest
  -> func f(x: Int = 42) -> Int { return x }
  >> let _ =
  -> f()       // Valid, uses default value
  >> let _ =
  -> f(x: 7)   // Valid, uses the value provided
  >> let _ =
  -> f(7)      // Invalid, missing argument label
  !$ error: missing argument label 'x:' in call
  !! f(7)      // Invalid, missing argument label
  !!   ^
  !!   x:
  ```
-->

<!--
  Rewrite the above to avoid discarding the function's return value.
  Tracking bug is <rdar://problem/35301593>
-->

<!--
  - test: `default-args-evaluated-at-call-site`

  ```swifttest
  -> func shout() -> Int {
        print("evaluated")
        return 10
     }
  -> func foo(x: Int = shout()) { print("x is \(x)") }
  -> foo(x: 100)
  << x is 100
  -> foo()
  << evaluated
  << x is 10
  -> foo()
  << evaluated
  << x is 10
  ```
-->

### Tipos especiais de métodos

Métodos de um enum ou de uma struct
que modificam `self` devem ser marcados com o modificador de declaração `mutating`.

Métodos que sobrescrevem um método da superclasse
devem ser marcados com o modificador de declaração `override`.
É um erro de compilação sobrescrever um método sem o modificador `override`
ou usar o modificador `override` em um método
que não sobrescreve um método da superclasse.

Métodos associados a um tipo,
e não a uma instância do tipo,
devem ser marcados com o modificador de declaração `static` em enums e structs,
ou com `static` ou `class` em classes.
Um método de tipo de classe marcado com o modificador de declaração `class`
pode ser sobrescrito pela implementação de uma subclasse;
um método de tipo de classe marcado com `class final` ou `static` não pode ser sobrescrito.

<!--
  - test: `overriding-class-methods-err`

  ```swifttest
  -> class S { class final func f() -> Int { return 12 } }
  -> class SS: S { override class func f() -> Int { return 120 } }
  !$ error: class method overrides a 'final' class method
  !! class SS: S { override class func f() -> Int { return 120 } }
  !!                                  ^
  !$ note: overridden declaration is here
  !! class S { class final func f() -> Int { return 12 } }
  !!                           ^
  -> class S2 { static func f() -> Int { return 12 } }
  -> class SS2: S2 { override static func f() -> Int { return 120 } }
  !$ error: cannot override static method
  !! class SS2: S2 { override static func f() -> Int { return 120 } }
  !! ^
  !$ note: overridden declaration is here
  !! class S2 { static func f() -> Int { return 12 } }
  !! ^
  ```
-->

<!--
  - test: `overriding-class-methods`

  ```swifttest
  -> class S3 { class func f() -> Int { return 12 } }
  -> class SS3: S3 { override class func f() -> Int { return 120 } }
  -> print(SS3.f())
  <- 120
  ```
-->

### Métodos com nomes especiais

Vários métodos com nomes especiais
habilitam açúcar sintático para a sintaxe de chamada de função.
Se um tipo define um desses métodos,
instâncias do tipo podem ser usadas na sintaxe de chamada de função.
A chamada de função é entendida como uma chamada
a um dos métodos com nome especial nessa instância.

Uma classe, struct ou tipo enum
pode oferecer suporte à sintaxe de chamada de função
definindo um método `dynamicallyCall(withArguments:)`
ou um método `dynamicallyCall(withKeywordArguments:)`,
como descrito em <doc:Attributes#dynamicCallable>,
ou definindo um método call-as-function, como descrito abaixo.
Se o tipo definir
tanto um método call-as-function
quanto um dos métodos usados pelo atributo `dynamicCallable`,
o compilador dá preferência ao método call-as-function
em situações em que qualquer um dos dois poderia ser usado.

O nome de um método call-as-function é `callAsFunction()`,
ou outro nome que começa com `callAsFunction(`
e acrescenta argumentos com ou sem rótulo ---
por exemplo, `callAsFunction(_:_:)` e `callAsFunction(something:)`
também são nomes válidos de método call-as-function.

<!--
  Above, callAsFunction( is in code voice even though
  it's not actually a symbol that exists in the reader's code.
  Per discussion with Chuck, this is the closest typographic convention
  to what we're trying to express here.
-->

As seguintes chamadas de função são equivalentes:

```swift
struct CallableStruct {
    var value: Int
    func callAsFunction(_ number: Int, scale: Int) {
        print(scale * (number + value))
    }
}
let callable = CallableStruct(value: 100)
callable(4, scale: 2)
callable.callAsFunction(4, scale: 2)
// Both function calls print 208.
```

<!--
  - test: `call-as-function`

  ```swifttest
  -> struct CallableStruct {
         var value: Int
         func callAsFunction(_ number: Int, scale: Int) {
             print(scale * (number + value))
         }
     }
  -> let callable = CallableStruct(value: 100)
  -> callable(4, scale: 2)
  -> callable.callAsFunction(4, scale: 2)
  // Both function calls print 208.
  << 208
  << 208
  ```
-->

Os métodos call-as-function
e os métodos do atributo `dynamicCallable`
adotam compromissos diferentes entre
quanta informação você codifica no sistema de tipos
e quanto comportamento dinâmico é possível em tempo de execução.
Ao declarar um método call-as-function,
você especifica o número de argumentos,
e o tipo e o rótulo de cada argumento.
Os métodos do atributo `dynamicCallable` especificam apenas o tipo
usado para guardar o array de argumentos.

Definir um método call-as-function,
ou um método do atributo `dynamicCallable`,
não permite usar uma instância desse tipo
como se fosse uma função em qualquer contexto que não seja uma expressão de chamada de função.
Por exemplo:

```swift
let someFunction1: (Int, Int) -> Void = callable(_:scale:)  // Error
let someFunction2: (Int, Int) -> Void = callable.callAsFunction(_:scale:)
```

<!--
  - test: `call-as-function-err`

  ```swifttest
  >> struct CallableStruct {
  >>     var value: Int
  >>     func callAsFunction(_ number: Int, scale: Int) { }
  >> }
  >> let callable = CallableStruct(value: 100)
  -> let someFunction1: (Int, Int) -> Void = callable(_:scale:)  // Error
  -> let someFunction2: (Int, Int) -> Void = callable.callAsFunction(_:scale:)
  >> _ = someFunction1 // suppress unused-constant warning
  >> _ = someFunction2 // suppress unused-constant warning
  !$ error: cannot find 'callable(_:scale:)' in scope
  !! let someFunction1: (Int, Int) -> Void = callable(_:scale:)  // Error
  !! ^~~~~~~~~~~~~~~~~~
  ```
-->

O subscript `subscript(dynamicMember:)`
habilita açúcar sintático para busca de membros,
como descrito em <doc:Attributes#dynamicMemberLookup>.

### Funções e métodos que lançam erros

Funções e métodos que podem lançar um erro devem ser marcados com a palavra-chave `throws`.
Essas funções e métodos são conhecidos como *funções que lançam erros*
e *métodos que lançam erros*.
Eles têm a seguinte forma:

```swift
func <#function name#>(<#parameters#>) throws -> <#return type#> {
   <#statements#>
}
```

Uma função que lança um tipo de erro específico tem a seguinte forma:

```swift
func <#function name#>(<#parameters#>) throws(<#error type#>) -> <#return type#> {
   <#statements#>
}
```

Chamadas a uma função ou método que lança erros devem estar dentro de uma expressão `try` ou `try!`
(isto é, no escopo de um operador `try` ou `try!`).

O tipo de uma função inclui se ela pode lançar um erro
e qual tipo de erro ela lança.
Essa relação de subtipo significa, por exemplo, que você pode usar uma função que não lança erros
em um contexto em que se espera uma que lança.
Para mais informações sobre o tipo de uma função que lança erros,
veja <doc:Types#Function-Type>.
Para exemplos de trabalho com erros que têm tipo explícito,
veja <doc:ErrorHandling#Specifying-the-Error-Type>.

Você não pode sobrecarregar uma função apenas com base em se ela pode lançar um erro.
Mesmo assim,
você pode sobrecarregar uma função com base em se um *parâmetro* da função pode lançar um erro.

Um método que lança erros não pode sobrescrever um método que não lança erros,
e um método que lança erros não pode satisfazer um requisito de protocolo para um método que não lança erros.
Mesmo assim, um método que não lança erros pode sobrescrever um método que lança erros,
e um método que não lança erros pode satisfazer um requisito de protocolo para um método que lança erros.

### Funções e métodos com rethrows

Uma função ou método pode ser declarado com a palavra-chave `rethrows`
para indicar que lança um erro somente se um de seus parâmetros de função lançar um erro.
Essas funções e métodos são conhecidos como *funções com rethrows*
e *métodos com rethrows*.
Funções e métodos com rethrows
precisam ter pelo menos um parâmetro de função que lança erros.

```swift
func someFunction(callback: () throws -> Void) rethrows {
    try callback()
}
```

<!--
  - test: `rethrows`

  ```swifttest
  -> func someFunction(callback: () throws -> Void) rethrows {
         try callback()
     }
  ```
-->

Uma função ou método com rethrows pode conter uma instrução `throw`
somente dentro de uma cláusula `catch`.
Isso permite chamar a função que lança erros dentro de uma instrução `do`-`catch`
e tratar os erros na cláusula `catch` lançando um erro diferente.
Além disso,
a cláusula `catch` deve tratar
apenas erros lançados por um dos parâmetros que lançam erros
da função com rethrows.
Por exemplo, o código a seguir é inválido
porque a cláusula `catch` trataria
o erro lançado por `alwaysThrows()`.

```swift
func alwaysThrows() throws {
    throw SomeError.error
}
func someFunction(callback: () throws -> Void) rethrows {
    do {
        try callback()
        try alwaysThrows()  // Invalid, alwaysThrows() isn't a throwing parameter
    } catch {
        throw AnotherError.error
    }
}
```

<!--
  - test: `double-negative-rethrows`

  ```swifttest
  >> enum SomeError: Error { case error }
  >> enum AnotherError: Error { case error }
  -> func alwaysThrows() throws {
         throw SomeError.error
     }
  -> func someFunction(callback: () throws -> Void) rethrows {
        do {
           try callback()
           try alwaysThrows()  // Invalid, alwaysThrows() isn't a throwing parameter
        } catch {
           throw AnotherError.error
        }
     }
  !$ error: a function declared 'rethrows' may only throw if its parameter does
  !!               throw AnotherError.error
  !!               ^
  ```
-->

<!--
  - test: `throwing-in-rethrowing-function`

  ```swifttest
  -> enum SomeError: Error { case c, d }
  -> func f1(callback: () throws -> Void) rethrows {
         do {
             try callback()
         } catch {
             throw SomeError.c  // OK
         }
     }
  -> func f2(callback: () throws -> Void) rethrows {
         throw SomeError.d  // Error
     }
  !$ error: a function declared 'rethrows' may only throw if its parameter does
  !! throw SomeError.d  // Error
  !! ^
  ```
-->

Um método que lança erros não pode sobrescrever um método com rethrows,
e um método que lança erros não pode satisfazer um requisito de protocolo para um método com rethrows.
Mesmo assim, um método com rethrows pode sobrescrever um método que lança erros,
e um método com rethrows pode satisfazer um requisito de protocolo para um método que lança erros.

Uma alternativa a rethrows é lançar um tipo de erro específico em código genérico.
Por exemplo:

```swift
func someFunction<E: Error>(callback: () throws(E) -> Void) throws(E) {
    try callback()
}
```

Essa abordagem de propagar um erro
preserva a informação de tipo sobre o erro.
No entanto, diferentemente de marcar a função com `rethrows`,
essa abordagem não impede que a função
lance um erro do mesmo tipo.

<!--
TODO: Revisit the comparison between rethrows and throws(E) above,
since it seems likely that the latter will generally replace the former.

See also rdar://128972373
-->

### Funções e métodos assíncronos

Funções e métodos que rodam de forma assíncrona devem ser marcados com a palavra-chave `async`.
Essas funções e métodos são conhecidos como *funções assíncronas*
e *métodos assíncronos*.
Eles têm a seguinte forma:

```swift
func <#function name#>(<#parameters#>) async -> <#return type#> {
   <#statements#>
}
```

Chamadas a uma função ou método assíncrono
devem estar dentro de uma expressão `await`,
isto é, precisam estar no escopo de um operador `await`.

A palavra-chave `async` faz parte do tipo da função,
e funções síncronas são subtipos de funções assíncronas.
Por isso, você pode usar uma função síncrona
em um contexto em que se espera uma função assíncrona.
Por exemplo,
você pode sobrescrever um método assíncrono com um método síncrono,
e um método síncrono pode satisfazer um requisito de protocolo
que exige um método assíncrono.

Você pode sobrecarregar uma função com base em ela ser ou não assíncrona.
No ponto de chamada, o contexto determina qual sobrecarga é usada:
em um contexto assíncrono, a função assíncrona é usada,
e em um contexto síncrono, a função síncrona é usada.

Um método assíncrono não pode sobrescrever um método síncrono,
e um método assíncrono não pode satisfazer um requisito de protocolo para um método síncrono.
Mesmo assim, um método síncrono pode sobrescrever um método assíncrono,
e um método síncrono pode satisfazer um requisito de protocolo para um método assíncrono.

<!--
  - test: `sync-satisfy-async-protocol-requirements`

  ```swifttest
  >> protocol P { func f() async -> Int }
  >> class Super: P {
  >>     func f() async -> Int { return 12 }
  >> }
  >> class Sub: Super {
  >>     func f() -> Int { return 120 }
  >> }
  ```
-->

### Funções que nunca retornam

O Swift define um tipo [`Never`][],
que indica que uma função ou método não retorna para quem o chamou.
Funções e métodos com tipo de retorno `Never` são chamados de *funções que nunca retornam*.
Funções e métodos que nunca retornam ou causam um erro irrecuperável
ou iniciam uma sequência de trabalho que continua indefinidamente.
Isso significa que
o código que, de outra forma, rodaria logo após a chamada nunca é executado.
Funções que lançam erros e funções com rethrows podem transferir o controle do programa
para um bloco `catch` apropriado, mesmo quando nunca retornam.

[`Never`]: https://developer.apple.com/documentation/swift/never

Uma função ou método não retornante pode ser chamado para concluir a cláusula `else`
de uma instrução guard,
como discutido em <doc:Statements#Guard-Statement>.

Você pode sobrescrever um método não retornante,
mas o novo método deve preservar o tipo de retorno e o comportamento não retornante.

> Gramática de uma declaração de função:
>
> *function-declaration* → *function-head* *function-name* *generic-parameter-clause*_?_ *function-signature* *generic-where-clause*_?_ *function-body*_?_
>
> *function-head* → *attributes*_?_ *declaration-modifiers*_?_ **`func`** \
> *function-name* → *identifier* | *operator*
>
> *function-signature* → *parameter-clause* **`async`**_?_ *throws-clause*_?_ *function-result*_?_ \
> *function-signature* → *parameter-clause* **`async`**_?_ **`rethrows`** *function-result*_?_ \
> *function-result* → **`->`** *attributes*_?_ *type* \
> *function-body* → *code-block*
>
> *parameter-clause* → **`(`** **`)`** | **`(`** *parameter-list* **`,`**_?_ **`)`** \
> *parameter-list* → *parameter* | *parameter* **`,`** *parameter-list* \
> *parameter* → *external-parameter-name*_?_ *local-parameter-name* *parameter-type-annotation* *default-argument-clause*_?_ \
> *parameter* → *external-parameter-name*_?_ *local-parameter-name* *parameter-type-annotation* \
> *parameter* → *external-parameter-name*_?_ *local-parameter-name* *parameter-type-annotation* **`...`**
>
> *external-parameter-name* → *identifier* \
> *local-parameter-name* → *identifier* \
> *parameter-type-annotation* → **`:`** *attributes*_?_ *parameter-modifier*_?_ *type* \
> *parameter-modifier* → **`inout`** | **`borrowing`** | **`consuming`**
> *default-argument-clause* → **`=`** *expression*

<!--
  NOTE: Code block is optional in the context of a protocol.
  Everywhere else, it's required.
  We could refactor to have a separation between function definition/declaration.
  There's also the low-level "asm name" FFI
  which is a definition and declaration corner case.
  Let's just deal with this difference in prose.
-->
## Declaração de enum

Uma *declaração de enum* introduz um tipo enum com nome no programa.

As declarações de enum têm duas formas básicas e são declaradas com a palavra-chave `enum`.
O corpo de um enum declarada em qualquer uma dessas formas contém
zero ou mais valores --- chamados *casos de enum* ---
e qualquer quantidade de declarações,
incluindo propriedades computadas,
métodos de instância, métodos de tipo, inicializadores, aliases de tipo,
e até outras declarações de enum, struct, classe e actor.
Declarações de enum não podem conter declarações de desinicializador ou de protocolo.

Tipos enum podem adotar qualquer número de protocolos, mas não podem herdar de classes,
structs ou de outros enums.

Diferentemente de classes e structs,
tipos enum não têm um inicializador padrão fornecido implicitamente;
todos os inicializadores precisam ser declarados explicitamente. Inicializadores podem delegar
para outros inicializadores do enum, mas o processo de inicialização só é concluído
depois que um inicializador atribui um dos casos do enum a `self`.

Assim como structs, mas diferentemente de classes, enums são tipos de valor;
instâncias de um enum são copiadas quando atribuídas a
variáveis ou constantes, ou quando passadas como argumentos em uma chamada de função.
Para informações sobre tipos de valor,
veja <doc:ClassesAndStructures#Structures-and-Enumerations-Are-Value-Types>.

Você pode estender o comportamento de um tipo enum com uma declaração de extension,
como discutido em <doc:Declarations#Extension-Declaration>.

### Enums com casos de qualquer tipo

A forma a seguir declara um tipo enum que contém
casos de enum de qualquer tipo:

```swift
enum <#enumeration name#>: <#adopted protocols#> {
    case <#enumeration case 1#>
    case <#enumeration case 2#>(<#associated value types#>)
}
```

Enums declaradas nessa forma às vezes são chamadas de *uniões discriminadas*
em outras linguagens de programação.

Nessa forma, cada bloco de casos consiste na palavra-chave `case`
seguida de um ou mais casos de enum, separados por vírgulas.
O nome de cada caso precisa ser único.
Cada caso também pode especificar que armazena valores de um determinado tipo.
Esses tipos são especificados na tupla de *tipos de associated values*,
logo após o nome do caso.

Casos de enum que armazenam associated values podem ser usados como funções
que criam instâncias do enum com os associated values especificados.
Assim como funções, você pode obter uma referência a um caso de enum
e aplicá-la depois no seu código.

```swift
enum Number {
    case integer(Int)
    case real(Double)
}
let f = Number.integer
// f is a function of type (Int) -> Number

// Apply f to create an array of Number instances with integer values
let evenInts: [Number] = [0, 2, 4, 6].map(f)
```

<!--
  - test: `enum-case-as-function`

  ```swifttest
  -> enum Number {
        case integer(Int)
        case real(Double)
     }
  -> let f = Number.integer
  -> // f is a function of type (Int) -> Number

  -> // Apply f to create an array of Number instances with integer values
  -> let evenInts: [Number] = [0, 2, 4, 6].map(f)
  ```
-->

<!--
  No expectation for evenInts because there isn't a good way to spell one.
  Using print() puts a module prefix like tmpabc in front of Number
  so the expectation would need to be a regex (which we don't have),
  and assert() would require Number to conform to Equatable.
-->

Para mais informações e para ver exemplos de casos com tipos de associated values,
veja <doc:Enumerations#Associated-Values>.

#### Enums com indireção

Enums podem ter uma estrutura recursiva,
ou seja, podem ter casos com associated values
que são instâncias do próprio tipo enum.
No entanto, instâncias de tipos enum têm semântica de valor,
o que significa que têm um layout fixo na memória.
Para dar suporte à recursão,
o compilador precisa inserir uma camada de indireção.

Para habilitar a indireção para um caso específico de enum,
marque-o com o modificador de declaração `indirect`.
Um caso indireto precisa ter um associated value.

<!--
  TODO The word "enable" is kind of a weasel word.
  Better to have a more concrete discussion of exactly when
  it is and isn't used.
  For example, does "indirect enum { X(Int) } mark X as indirect?
-->

```swift
enum Tree<T> {
    case empty
    indirect case node(value: T, left: Tree, right: Tree)
}
```

<!--
  - test: `indirect-enum`

  ```swifttest
  -> enum Tree<T> {
        case empty
        indirect case node(value: T, left: Tree, right: Tree)
     }
  >> let l1 = Tree.node(value: 10, left: Tree.empty, right: Tree.empty)
  >> let l2 = Tree.node(value: 100, left: Tree.empty, right: Tree.empty)
  >> let t = Tree.node(value: 50, left: l1, right: l2)
  ```
-->

Para habilitar a indireção para todos os casos de um enum
que têm um associated value,
marque o enum inteira com o modificador `indirect` ---
isso é prático quando o enum contém muitos casos
que precisariam, cada um, ser marcado com o modificador `indirect`.

Um enum marcada com o modificador `indirect` pode conter uma mistura de casos
que têm associated values e casos que não têm.
Mesmo assim, ela não pode conter casos que também estejam marcados com o modificador `indirect`.

<!--
  It really should be an associated value **that includes the enum type**
  but right now the compiler is satisfied with any associated value.
  Alex emailed Joe Groff 2015-07-08 about this.
-->

<!--
  assertion indirect-in-indirect

  -> indirect enum E { indirect case c(E) }
  !! <REPL Input>:1:19: error: enum case in 'indirect' enum cannot also be 'indirect'
  !! indirect enum E { indirect case c(E) }
  !!                   ^
-->

<!--
  assertion indirect-without-recursion

  -> enum E { indirect case c }
  !! <REPL Input>:1:10: error: enum case 'c' without associated value cannot be 'indirect'
  !! enum E { indirect case c }
  !!          ^

  -> enum E1 { indirect case c() }     // This is fine, but probably shouldn't be
  -> enum E2 { indirect case c(Int) }  // This is fine, but probably shouldn't be

  -> indirect enum E3 { case x }
-->

### Enums com casos de um tipo de raw value

A forma a seguir declara um tipo enum que contém
casos de enum do mesmo tipo básico:

```swift
enum <#enumeration name#>: <#raw-value type#>, <#adopted protocols#> {
    case <#enumeration case 1#> = <#raw value 1#>
    case <#enumeration case 2#> = <#raw value 2#>
}
```

Nessa forma, cada bloco de casos consiste na palavra-chave `case`,
seguida de um ou mais casos de enum, separados por vírgulas.
Diferentemente dos casos da primeira forma, cada caso tem um valor subjacente,
chamado *raw value*, do mesmo tipo básico.
O tipo desses valores é especificado no *tipo de raw value* e precisa representar
um inteiro, um número de ponto flutuante, uma string ou um único caractere.
Em particular, o *tipo de raw value* precisa estar em conformidade com o protocolo `Equatable`
e com um dos protocolos a seguir:
`ExpressibleByIntegerLiteral` para literais inteiros,
`ExpressibleByFloatLiteral` para literais de ponto flutuante,
`ExpressibleByStringLiteral` para literais de string que contêm qualquer número de caracteres,
e `ExpressibleByUnicodeScalarLiteral`
ou `ExpressibleByExtendedGraphemeClusterLiteral` para literais de string
que contêm apenas um único caractere.
Cada caso precisa ter um nome único e receber um raw value único.

<!--
  The list of ExpressibleBy... protocols above also appears in LexicalStructure_Literals.
  This list is shorter because these five protocols are explicitly supported in the compiler.
-->

Se o tipo de raw value for especificado como `Int`
e você não atribuir valores aos casos explicitamente,
eles recebem implicitamente os valores `0`, `1`, `2`, e assim por diante.
Cada caso não atribuído do tipo `Int` recebe implicitamente um raw value
que é incrementado automaticamente a partir do raw value do caso anterior.

```swift
enum ExampleEnum: Int {
    case a, b, c = 5, d
}
```

<!--
  - test: `raw-value-enum`

  ```swifttest
  -> enum ExampleEnum: Int {
        case a, b, c = 5, d
     }
  ```
-->

No exemplo acima, o raw value de `ExampleEnum.a` é `0` e o valor de
`ExampleEnum.b` é `1`. E como o valor de `ExampleEnum.c` é definido explicitamente como `5`,
o valor de `ExampleEnum.d` é incrementado automaticamente a partir de `5`
e, portanto, é `6`.

Se o tipo de raw value for especificado como `String`
e você não atribuir valores aos casos explicitamente,
cada caso não atribuído recebe implicitamente uma string com o mesmo texto do nome desse caso.

```swift
enum GamePlayMode: String {
    case cooperative, individual, competitive
}
```

<!--
  - test: `raw-value-enum-implicit-string-values`

  ```swifttest
  -> enum GamePlayMode: String {
        case cooperative, individual, competitive
     }
  ```
-->

No exemplo acima, o raw value de `GamePlayMode.cooperative` é `"cooperative"`,
o raw value de `GamePlayMode.individual` é `"individual"`,
e o raw value de `GamePlayMode.competitive` é `"competitive"`.

Enums que têm casos de um tipo de raw value implicitamente estão em conformidade com
o protocolo `RawRepresentable`, definido na biblioteca padrão do Swift.
Como resultado, elas têm uma propriedade `rawValue`
e um inicializador falível com a assinatura `init?(rawValue: RawValue)`.
Você pode usar a propriedade `rawValue` para acessar o raw value de um caso de enum,
como em `ExampleEnum.b.rawValue`.
Você também pode usar um raw value para encontrar o caso correspondente, se houver,
chamando o inicializador falível do enum,
como em `ExampleEnum(rawValue: 5)`, que retorna um caso optional.
Para mais informações e para ver exemplos de casos com tipos de raw value,
veja <doc:Enumerations#Raw-Values>.

### Como acessar casos de enum

Para referenciar um caso de um tipo enum, use a sintaxe de ponto (`.`),
como em `EnumerationType.enumerationCase`. Quando o tipo enum puder ser inferido
pelo contexto, você pode omiti-lo (o ponto continua obrigatório),
como descrito em <doc:Enumerations#Enumeration-Syntax>
e <doc:Expressions#Implicit-Member-Expression>.

Para verificar os valores de casos de enum, use uma instrução `switch`,
como mostrado em <doc:Enumerations#Matching-Enumeration-Values-with-a-Switch-Statement>.
O tipo enum é comparado com os padrões de caso de enum
nos blocos `case` da instrução `switch`,
como descrito em <doc:Patterns#Enumeration-Case-Pattern>.

<!--
  FIXME: Or use if-case:
  enum E { case c(Int) }
  let e = E.c(100)
  if case E.c(let i) = e { print(i) }
  // prints 100
-->

<!--
  NOTE: Note that you can require protocol adoption,
  by using a protocol type as the raw-value type,
  but you do need to make it be one of the types
  that support = in order for you to specify the raw values.
  You can have: <#raw-value type, protocol conformance#>.
  UPDATE: You can only have one raw-value type specified.
  I changed the grammar to be more restrictive in light of this.
-->

<!--
  NOTE: Per Doug and Ted, "('->' type)?" isn't part of the grammar.
  We removed it from our grammar, below.
-->

> Gramática de uma declaração de enum:
>
> *enum-declaration* → *attributes*_?_ *access-level-modifier*_?_ *union-style-enum* \
> *enum-declaration* → *attributes*_?_ *access-level-modifier*_?_ *raw-value-style-enum*
>
> *union-style-enum* → **`indirect`**_?_ **`enum`** *enum-name* *generic-parameter-clause*_?_ *type-inheritance-clause*_?_ *generic-where-clause*_?_ **`{`** *union-style-enum-members*_?_ **`}`** \
> *union-style-enum-members* → *union-style-enum-member* *union-style-enum-members*_?_ \
> *union-style-enum-member* → *declaration* | *union-style-enum-case-clause* | *compiler-control-statement* \
> *union-style-enum-case-clause* → *attributes*_?_ **`indirect`**_?_ **`case`** *union-style-enum-case-list* \
> *union-style-enum-case-list* → *union-style-enum-case* | *union-style-enum-case* **`,`** *union-style-enum-case-list* \
> *union-style-enum-case* → *enum-case-name* *tuple-type*_?_ \
> *enum-name* → *identifier* \
> *enum-case-name* → *identifier*
>
> *raw-value-style-enum* → **`enum`** *enum-name* *generic-parameter-clause*_?_ *type-inheritance-clause* *generic-where-clause*_?_ **`{`** *raw-value-style-enum-members* **`}`** \
> *raw-value-style-enum-members* → *raw-value-style-enum-member* *raw-value-style-enum-members*_?_ \
> *raw-value-style-enum-member* → *declaration* | *raw-value-style-enum-case-clause* | *compiler-control-statement* \
> *raw-value-style-enum-case-clause* → *attributes*_?_ **`case`** *raw-value-style-enum-case-list* \
> *raw-value-style-enum-case-list* → *raw-value-style-enum-case* | *raw-value-style-enum-case* **`,`** *raw-value-style-enum-case-list* \
> *raw-value-style-enum-case* → *enum-case-name* *raw-value-assignment*_?_ \
> *raw-value-assignment* → **`=`** *raw-value-literal* \
> *raw-value-literal* → *numeric-literal* | *static-string-literal* | *boolean-literal*

<!--
  NOTE: The two types of enums are sufficiently different enough to warrant separating
  the grammar accordingly. ([Contributor 6004] pointed this out in his email.)
  I'm not sure I'm happy with the names I've chosen for two kinds of enums,
  so please let me know if you can think of better names (Tim and Dave are OK with them)!
  I chose union-style-enum, because this kind of enum behaves like a discriminated union,
  not like an ordinary enum type. They're a kind of "sum" type in the language
  of ADTs (Algebraic Data Types). Functional languages, like F# for example,
  actually have both types (discriminated unions and enumeration types),
  because they behave differently. I'm not sure why we've blended them together,
  especially given that they have distinct syntactic declaration requirements
  and they behave differently.
-->

## Declaração de struct

Uma *declaração de struct* introduz um tipo struct com nome no programa.
Declarações de struct são feitas com a palavra-chave `struct` e têm a seguinte forma:

```swift
struct <#structure name#>: <#adopted protocols#> {
   <#declarations#>
}
```

O corpo de uma struct contém zero ou mais *declarações*.
Essas *declarações* podem incluir propriedades armazenadas e computadas,
propriedades de tipo, métodos de instância, métodos de tipo, inicializadores, subscripts,
aliases de tipo, e até outras declarações de struct, classe, actor e enum.
Declarações de struct não podem conter declarações de desinicializador ou de protocolo.
Para uma discussão e vários exemplos de structs
que incluem vários tipos de declarações,
veja <doc:ClassesAndStructures>.

Tipos struct podem adotar qualquer número de protocolos,
mas não podem herdar de classes, enums ou de outras structs.

Há três maneiras de criar uma instância de uma struct declarada anteriormente:

- Chamar um dos inicializadores declarados dentro da struct,
  como descrito em <doc:Initialization#Initializers>.
- Se nenhum inicializador for declarado,
  chamar o inicializador memberwise da struct,
  como descrito em <doc:Initialization#Memberwise-Initializers-for-Structure-Types>.
- Se nenhum inicializador for declarado,
  e todas as propriedades da declaração de struct receberam valores iniciais,
  chamar o inicializador padrão da struct,
  como descrito em <doc:Initialization#Default-Initializers>.

O processo de inicialização das propriedades declaradas de uma struct
é descrito em <doc:Initialization>.

Propriedades de uma instância de struct podem ser acessadas usando a sintaxe de ponto (`.`),
como descrito em <doc:ClassesAndStructures#Accessing-Properties>.

Structs são tipos de valor; instâncias de uma struct são copiadas quando atribuídas a
variáveis ou constantes, ou quando passadas como argumentos em uma chamada de função.
Para informações sobre tipos de valor,
veja <doc:ClassesAndStructures#Structures-and-Enumerations-Are-Value-Types>.

Você pode estender o comportamento de um tipo struct com uma declaração de extension,
como discutido em <doc:Declarations#Extension-Declaration>.

> Gramática de uma declaração de struct:
>
> *struct-declaration* → *attributes*_?_ *access-level-modifier*_?_ **`struct`** *struct-name* *generic-parameter-clause*_?_ *type-inheritance-clause*_?_ *generic-where-clause*_?_ *struct-body* \
> *struct-name* → *identifier* \
> *struct-body* → **`{`** *struct-members*_?_ **`}`**
>
> *struct-members* → *struct-member* *struct-members*_?_ \
> *struct-member* → *declaration* | *compiler-control-statement*

## Declaração de classe

Uma *declaração de classe* introduz um tipo classe com nome no programa.
Declarações de classe são feitas com a palavra-chave `class` e têm a seguinte forma:

```swift
class <#class name#>: <#superclass#>, <#adopted protocols#> {
   <#declarations#>
}
```

O corpo de uma classe contém zero ou mais *declarações*.
Essas *declarações* podem incluir propriedades armazenadas e computadas,
métodos de instância, métodos de tipo, inicializadores,
um único desinicializador, subscripts, aliases de tipo,
e até outras declarações de classe, struct, actor e enum.
Declarações de classe não podem conter declarações de protocolo.
Para uma discussão e vários exemplos de classes
que incluem vários tipos de declarações,
veja <doc:ClassesAndStructures>.

Um tipo classe pode herdar de apenas uma classe pai, sua *superclasse*,
mas pode adotar qualquer número de protocolos.
A *superclasse* aparece primeiro, depois do nome da classe e dos dois-pontos,
seguida de quaisquer *protocolos adotados*.
Classes genéricas podem herdar de outras classes genéricas e não genéricas,
mas uma classe não genérica só pode herdar de outras classes não genéricas.
Ao escrever o nome de uma superclasse genérica depois dos dois-pontos,
você precisa incluir o nome completo dessa classe genérica,
incluindo a cláusula de parâmetros genéricos.

Como discutido em <doc:Declarations#Initializer-Declaration>,
classes podem ter inicializadores designados e de conveniência.
O inicializador designado de uma classe precisa inicializar todas as propriedades declaradas da classe,
e precisa fazê-lo antes de chamar qualquer inicializador designado da superclasse.

Uma classe pode sobrescrever propriedades, métodos, subscripts e inicializadores da superclasse.
Propriedades, métodos, subscripts e inicializadores designados sobrescritos
precisam ser marcados com o modificador de declaração `override`.

<!--
  - test: `designatedInitializersRequireOverride`

  ```swifttest
  -> class C { init() {} }
  -> class D: C { override init() { super.init() } }
  ```
-->

Para exigir que subclasses implementem um inicializador da superclasse,
marque o inicializador da superclasse com o modificador de declaração `required`.
A implementação desse inicializador na subclasse também precisa ser marcada
com o modificador de declaração `required`.

Embora propriedades e métodos declarados na *superclasse* sejam herdados pela classe atual,
inicializadores designados declarados na *superclasse* só são herdados
quando a subclasse atende às condições descritas em
<doc:Initialization#Automatic-Initializer-Inheritance>.
Classes Swift não herdam de uma classe base universal.

Há duas maneiras de criar uma instância de uma classe declarada anteriormente:

- Chamar um dos inicializadores declarados dentro da classe,
  como descrito em <doc:Initialization#Initializers>.
- Se nenhum inicializador for declarado,
  e todas as propriedades da declaração de classe receberam valores iniciais,
  chamar o inicializador padrão da classe,
  como descrito em <doc:Initialization#Default-Initializers>.

Acesse propriedades de uma instância de classe com a sintaxe de ponto (`.`),
como descrito em <doc:ClassesAndStructures#Accessing-Properties>.

Classes são tipos de referência; instâncias de uma classe são referenciadas, em vez de copiadas,
quando atribuídas a variáveis ou constantes, ou quando passadas como argumentos em uma chamada de função.
Para informações sobre tipos de referência,
veja <doc:ClassesAndStructures#Classes-Are-Reference-Types>.

Você pode estender o comportamento de um tipo classe com uma declaração de extension,
como discutido em <doc:Declarations#Extension-Declaration>.

> Gramática de uma declaração de classe:
>
> *class-declaration* → *attributes*_?_ *access-level-modifier*_?_ **`final`**_?_ **`class`** *class-name* *generic-parameter-clause*_?_ *type-inheritance-clause*_?_ *generic-where-clause*_?_ *class-body* \
> *class-declaration* → *attributes*_?_ **`final`** *access-level-modifier*_?_ **`class`** *class-name* *generic-parameter-clause*_?_ *type-inheritance-clause*_?_ *generic-where-clause*_?_ *class-body* \
> *class-name* → *identifier* \
> *class-body* → **`{`** *class-members*_?_ **`}`**
>
> *class-members* → *class-member* *class-members*_?_ \
> *class-member* → *declaration* | *compiler-control-statement*

## Declaração de actor

Uma *declaração de actor* introduz um tipo actor com nome no programa.
Declarações de actor são feitas com a palavra-chave `actor` e têm a seguinte forma:

```swift
actor <#actor name#>: <#adopted protocols#> {
    <#declarations#>
}
```

O corpo de um actor contém zero ou mais *declarações*.
Essas *declarações* podem incluir propriedades armazenadas e computadas,
métodos de instância, métodos de tipo, inicializadores,
um único desinicializador, subscripts, aliases de tipo,
e até outras declarações de classe, struct e enum.
Para uma discussão e vários exemplos de actors
que incluem vários tipos de declarações,
veja <doc:Concurrency#Actors>.

Tipos actor podem adotar qualquer número de protocolos,
mas não podem herdar de classes, enums, structs ou de outros actors.
No entanto, um actor marcado com o atributo `@objc` implicitamente está em conformidade
com o protocolo `NSObjectProtocol` e é exposto ao tempo de execução (runtime)
do Objective-C como um subtipo de `NSObject`.

Há duas maneiras de criar uma instância de um actor declarado anteriormente:

- Chamar um dos inicializadores declarados dentro do actor,
  como descrito em <doc:Initialization#Initializers>.
- Se nenhum inicializador for declarado,
  e todas as propriedades da declaração de actor receberam valores iniciais,
  chamar o inicializador padrão do actor,
  como descrito em <doc:Initialization#Default-Initializers>.

Por padrão, membros de um actor são isolados a esse actor.
O código, como o corpo de um método ou o getter de uma propriedade, é executado nesse actor.
Código dentro do actor pode interagir com eles de forma síncrona,
porque esse código já está sendo executado no mesmo actor,
mas código fora do actor precisa marcá-los com `await`
para indicar que esse código está executando de forma assíncrona em outro actor.
*Key paths* não podem se referir a membros isolados de um actor.
Propriedades armazenadas isoladas ao actor podem ser passadas como parâmetros in-out
para funções síncronas, mas não para funções assíncronas.

Actors também podem ter membros não isolados, cujas declarações são marcadas
com a palavra-chave `nonisolated`.
Um membro não isolado é executado como código fora do actor:
ele não pode interagir com nenhum estado isolado do actor,
e quem o chama não o marca com `await`.

Membros de um actor só podem ser marcados com o atributo `@objc`
se forem não isolados ou assíncronos.

O processo de inicialização das propriedades declaradas de um actor
é descrito em <doc:Initialization>.

Propriedades de uma instância de actor podem ser acessadas usando a sintaxe de ponto (`.`),
como descrito em <doc:ClassesAndStructures#Accessing-Properties>.

Actors são tipos de referência; instâncias de um actor são referenciadas, em vez de copiadas,
quando atribuídas a variáveis ou constantes, ou quando passadas como argumentos em uma chamada de função.
Para informações sobre tipos de referência,
veja <doc:ClassesAndStructures#Classes-Are-Reference-Types>.

Você pode estender o comportamento de um tipo actor com uma declaração de extension,
como discutido em <doc:Declarations#Extension-Declaration>.

<!--
  TODO Additional bits from the SE-0306 actors proposal:

  Partial applications of isolated functions are only permitted
  when the expression is a direct argument
  whose corresponding parameter is non-escaping and non-Sendable.
-->

> Gramática de uma declaração de actor:
>
> *actor-declaration* → *attributes*_?_ *access-level-modifier*_?_ **`actor`** *actor-name* *generic-parameter-clause*_?_ *type-inheritance-clause*_?_ *generic-where-clause*_?_ *actor-body* \
> *actor-name* → *identifier* \
> *actor-body* → **`{`** *actor-members*_?_ **`}`**
>
> *actor-members* → *actor-member* *actor-members*_?_ \
> *actor-member* → *declaration* | *compiler-control-statement*
## Declaração de protocolo

Uma *declaração de protocolo* introduz um tipo protocolo nomeado no programa.
Declarações de protocolo são feitas com a palavra-chave `protocol` e têm a seguinte forma:

```swift
protocol <#protocol name#>: <#inherited protocols#> {
   <#protocol member declarations#>
}
```

Declarações de protocolo podem aparecer no escopo global,
ou aninhadas dentro de um tipo não genérico ou de uma função não genérica.

O corpo de um protocolo contém zero ou mais *declarações de membros do protocolo*,
que descrevem os requisitos de conformidade que qualquer tipo que adote o protocolo precisa cumprir.
Em particular, um protocolo pode declarar que os tipos em conformidade devem
implementar certas propriedades, métodos, inicializadores e subscripts.
Protocolos também podem declarar tipos especiais de alias,
chamados *tipos associados*, que podem especificar relações
entre as várias declarações do protocolo.
Declarações de protocolo não podem conter
declarações de classe, struct, enum ou de outros protocolos.
As *declarações de membros do protocolo* são discutidas em detalhes abaixo.

Tipos protocolo podem herdar de qualquer número de outros protocolos.
Quando um tipo protocolo herda de outros protocolos,
o conjunto de requisitos desses outros protocolos é agregado,
e qualquer tipo que herde do protocolo atual precisa estar em conformidade com todos esses requisitos.
Para um exemplo de como usar a herança de protocolos,
veja <doc:Protocols#Protocol-Inheritance>.

> Nota: Você também pode agregar os requisitos de conformidade de vários
> protocolos usando tipos de composição de protocolos,
> como descrito em <doc:Types#Protocol-Composition-Type>
> e <doc:Protocols#Protocol-Composition>.

Você pode adicionar conformidade com um protocolo a um tipo já declarado
adotando o protocolo em uma declaração de extension desse tipo.
Na extension, você precisa implementar todos os requisitos do protocolo adotado.
Se o tipo já implementa todos os requisitos, você pode deixar o corpo da declaração de extension vazio.

Por padrão, tipos que estão em conformidade com um protocolo precisam implementar todas as
propriedades, métodos e subscripts declarados no protocolo.
Mesmo assim, você pode marcar essas declarações de membros do protocolo com o modificador de declaração `optional`
para especificar que a implementação delas pelo tipo em conformidade é opcional.
O modificador `optional` só pode ser aplicado
a membros marcados com o atributo `objc`, e somente a membros de protocolos marcados
com o atributo `objc`. Como resultado, apenas tipos classe podem adotar e estar em conformidade
com um protocolo que contém requisitos de membros opcionais.
Para mais informações sobre como usar o modificador de declaração `optional`
e para orientações sobre como acessar membros opcionais de protocolo ---
por exemplo, quando você não tem certeza se um tipo em conformidade os implementa ---
veja <doc:Protocols#Optional-Protocol-Requirements>.

<!--
  TODO: Currently, you can't check for an optional initializer,
  so we're leaving those out of the documentation, even though you can mark
  an initializer with the @optional attribute. It's still being decided by the
  compiler team. Update this section if they decide to make everything work
  properly for optional initializer requirements.
-->

Os casos de um enum podem satisfazer
requisitos de protocolo para membros de tipo.
Especificamente,
um caso de enum sem associated values
satisfaz um requisito de protocolo para
uma variável de tipo somente leitura do tipo `Self`,
e um caso de enum com associated values
satisfaz um requisito de protocolo para uma função que retorna `Self`
cujos parâmetros e rótulos de argumento
correspondem aos associated values do caso.
Por exemplo:

```swift
protocol SomeProtocol {
    static var someValue: Self { get }
    static func someFunction(x: Int) -> Self
}
enum MyEnum: SomeProtocol {
    case someValue
    case someFunction(x: Int)
}
```

<!--
  - test: `enum-case-satisfy-protocol-requirement`

  ```swifttest
  -> protocol SomeProtocol {
         static var someValue: Self { get }
         static func someFunction(x: Int) -> Self
     }
  -> enum MyEnum: SomeProtocol {
         case someValue
         case someFunction(x: Int)
     }
  ```
-->

Para restringir a adoção de um protocolo apenas a tipos classe,
inclua o protocolo `AnyObject` na lista de *protocolos herdados*
depois dos dois-pontos.
Por exemplo, o protocolo a seguir só pode ser adotado por tipos classe:

```swift
protocol SomeProtocol: AnyObject {
    /* Protocol members go here. */
}
```

<!--
  - test: `protocol-declaration`

  ```swifttest
  -> protocol SomeProtocol: AnyObject {
         /* Protocol members go here. */
     }
  ```
-->

Qualquer protocolo que herde de um protocolo marcado com o requisito `AnyObject`
também só pode ser adotado por tipos classe.

> Nota: Se um protocolo for marcado com o atributo `objc`,
> o requisito `AnyObject` é aplicado implicitamente a esse protocolo;
> não há necessidade de marcar o protocolo com o requisito `AnyObject` explicitamente.

Você também pode nomear uma classe específica na lista de *protocolos herdados*
para restringir a adoção do protocolo a subclasses dessa classe.
Por exemplo, o protocolo a seguir só pode ser adotado por subclasses de `SomeBaseClass`:

```swift
class SomeBaseClass { /* ... */ }
protocol SomeRefinedProtocol: SomeBaseClass {
    /* Protocol members go here. */
}
```

<!--
  - test: `protocol-declaration-superclass`

  ```swifttest
  -> class SomeBaseClass {}
  -> protocol SomeRefinedProtocol: SomeBaseClass {
         /* Protocol members go here. */
     }
  ```
-->

Protocolos são tipos nomeados e, por isso, podem aparecer nos mesmos lugares
do código que outros tipos nomeados, como descrito em <doc:Protocols#Protocols-as-Types>.
Porém,
você não pode criar uma instância de um protocolo,
porque protocolos não fornecem as implementações dos requisitos
que especificam.

Você pode usar protocolos para declarar quais métodos um delegado de uma classe ou struct
deve implementar, como descrito em <doc:Protocols#Delegation>.

> Gramática de uma declaração de protocolo:
>
> *protocol-declaration* → *attributes*_?_ *access-level-modifier*_?_ **`protocol`** *protocol-name* *type-inheritance-clause*_?_ *generic-where-clause*_?_ *protocol-body* \
> *protocol-name* → *identifier* \
> *protocol-body* → **`{`** *protocol-members*_?_ **`}`**
>
> *protocol-members* → *protocol-member* *protocol-members*_?_ \
> *protocol-member* → *protocol-member-declaration* | *compiler-control-statement*
>
> *protocol-member-declaration* → *protocol-property-declaration* \
> *protocol-member-declaration* → *protocol-method-declaration* \
> *protocol-member-declaration* → *protocol-initializer-declaration* \
> *protocol-member-declaration* → *protocol-subscript-declaration* \
> *protocol-member-declaration* → *protocol-associated-type-declaration* \
> *protocol-member-declaration* → *typealias-declaration*

### Declaração de propriedade de protocolo

Protocolos declaram que os tipos em conformidade devem implementar uma propriedade
incluindo uma *declaração de propriedade de protocolo*
no corpo da declaração do protocolo.
Declarações de propriedade de protocolo têm uma forma especial de declaração de variável:

```swift
var <#property name#>: <#type#> { get set }
```

Assim como outras declarações de membros do protocolo, essas declarações de propriedade
declaram apenas os requisitos de getter e setter para os tipos
que estão em conformidade com o protocolo. Por isso, você não implementa o getter ou o setter
diretamente no protocolo em que a propriedade é declarada.

Os requisitos de getter e setter podem ser satisfeitos por um tipo em conformidade de várias maneiras.
Se uma declaração de propriedade incluir as palavras-chave `get` e `set`,
um tipo em conformidade pode implementá-la com uma propriedade armazenada de variável ou
com uma propriedade computada que seja legível e gravável (isto é, que implemente tanto um getter quanto um setter). Porém,
essa declaração de propriedade não pode ser implementada como uma propriedade constante
ou como uma propriedade computada somente leitura. Se a declaração de propriedade incluir
apenas a palavra-chave `get`, ela pode ser implementada com qualquer tipo de propriedade.
Para exemplos de tipos em conformidade que implementam os requisitos de propriedade de um protocolo,
veja <doc:Protocols#Property-Requirements>.

Para declarar um requisito de propriedade de tipo em uma declaração de protocolo,
marque a declaração da propriedade com a palavra-chave `static`.
Structs e enums que estão em conformidade com o protocolo
declaram a propriedade com a palavra-chave `static`,
e classes que estão em conformidade com o protocolo
declaram a propriedade com a palavra-chave `static` ou `class`.
Extensions que adicionam conformidade com um protocolo a uma struct, enum ou classe
usam a mesma palavra-chave que o tipo que elas estendem usa.
Extensions que fornecem uma implementação padrão para um requisito de propriedade de tipo
usam a palavra-chave `static`.

<!--
  - test: `protocols-with-type-property-requirements`

  ```swifttest
  -> protocol P { static var x: Int { get } }
  -> protocol P2 { class var x: Int { get } }
  !$ error: class properties are only allowed within classes; use 'static' to declare a requirement fulfilled by either a static or class property
  !! protocol P2 { class var x: Int { get } }
  !!              ~~~~~ ^
  !!              static
  -> struct S: P { static var x = 10 }
  -> class C1: P { static var x = 20 }
  -> class C2: P { class var x = 30 }
  !$ error: class stored properties not supported in classes; did you mean 'static'?
  !! class C2: P { class var x = 30 }
  !!               ~~~~~     ^
  ```
-->

<!--
  - test: `protocol-type-property-default-implementation`

  ```swifttest
  -> protocol P { static var x: Int { get } }
  -> extension P { static var x: Int { return 100 } }
  -> struct S1: P { }
  -> print(S1.x)
  <- 100
  -> struct S2: P { static var x = 10 }
  -> print(S2.x)
  <- 10
  ```
-->

Veja também <doc:Declarations#Variable-Declaration>.

> Gramática de uma declaração de propriedade de protocolo:
>
> *protocol-property-declaration* → *variable-declaration-head* *variable-name* *type-annotation* *getter-setter-keyword-block*

### Declaração de método de protocolo

Protocolos declaram que os tipos em conformidade devem implementar um método
incluindo uma declaração de método de protocolo no corpo da declaração do protocolo.
Declarações de método de protocolo têm a mesma forma que
declarações de função, com duas exceções: elas não incluem um corpo de função,
e você não pode fornecer valores padrão para parâmetros como parte da declaração da função.
Para exemplos de tipos em conformidade que implementam os requisitos de método de um protocolo,
veja <doc:Protocols#Method-Requirements>.

Para declarar um requisito de método de classe ou estático em uma declaração de protocolo,
marque a declaração do método com o modificador de declaração `static`.
Structs e enums que estão em conformidade com o protocolo
declaram o método com a palavra-chave `static`,
e classes que estão em conformidade com o protocolo
declaram o método com a palavra-chave `static` ou `class`.
Extensions que adicionam conformidade com um protocolo a uma struct, enum ou classe
usam a mesma palavra-chave que o tipo que elas estendem usa.
Extensions que fornecem uma implementação padrão para um requisito de método de tipo
usam a palavra-chave `static`.

Veja também <doc:Declarations#Function-Declaration>.

<!--
  TODO: Talk about using ``Self`` in parameters and return types.
-->

> Gramática de uma declaração de método de protocolo:
>
> *protocol-method-declaration* → *function-head* *function-name* *generic-parameter-clause*_?_ *function-signature* *generic-where-clause*_?_

### Declaração de inicializador de protocolo

Protocolos declaram que os tipos em conformidade devem implementar um inicializador
incluindo uma declaração de inicializador de protocolo no corpo da declaração do protocolo.
Declarações de inicializador de protocolo têm a mesma forma que
declarações de inicializador, exceto que não incluem o corpo do inicializador.

Um tipo em conformidade pode satisfazer um requisito de inicializador de protocolo não falível
implementando um inicializador não falível ou um inicializador falível `init!`.
Um tipo em conformidade pode satisfazer um requisito de inicializador de protocolo falível
implementando qualquer tipo de inicializador.

Quando uma classe implementa um inicializador para satisfazer o requisito de inicializador de um protocolo,
o inicializador precisa ser marcado com o modificador de declaração `required`
se a classe ainda não estiver marcada com o modificador de declaração `final`.

Veja também <doc:Declarations#Initializer-Declaration>.

> Gramática de uma declaração de inicializador de protocolo:
>
> *protocol-initializer-declaration* → *initializer-head* *generic-parameter-clause*_?_ *parameter-clause* *throws-clause*_?_ *generic-where-clause*_?_ \
> *protocol-initializer-declaration* → *initializer-head* *generic-parameter-clause*_?_ *parameter-clause* **`rethrows`** *generic-where-clause*_?_

### Declaração de subscript de protocolo

Protocolos declaram que os tipos em conformidade devem implementar um subscript
incluindo uma declaração de subscript de protocolo no corpo da declaração do protocolo.
Declarações de subscript de protocolo têm uma forma especial de declaração de subscript:

```swift
subscript (<#parameters#>) -> <#return type#> { get set }
```

Declarações de subscript declaram apenas os requisitos mínimos de implementação de getter e setter
para os tipos que estão em conformidade com o protocolo.
Se a declaração de subscript incluir as palavras-chave `get` e `set`,
um tipo em conformidade precisa implementar tanto a cláusula getter quanto a cláusula setter.
Se a declaração de subscript incluir apenas a palavra-chave `get`,
um tipo em conformidade precisa implementar *pelo menos* uma cláusula getter
e pode, opcionalmente, implementar uma cláusula setter.

Para declarar um requisito de subscript estático em uma declaração de protocolo,
marque a declaração do subscript com o modificador de declaração `static`.
Structs e enums que estão em conformidade com o protocolo
declaram o subscript com a palavra-chave `static`,
e classes que estão em conformidade com o protocolo
declaram o subscript com a palavra-chave `static` ou `class`.
Extensions que adicionam conformidade com um protocolo a uma struct, enum ou classe
usam a mesma palavra-chave que o tipo que elas estendem usa.
Extensions que fornecem uma implementação padrão para um requisito de subscript estático
usam a palavra-chave `static`.

Veja também <doc:Declarations#Subscript-Declaration>.

> Gramática de uma declaração de subscript de protocolo:
>
> *protocol-subscript-declaration* → *subscript-head* *subscript-result* *generic-where-clause*_?_ *getter-setter-keyword-block*

### Declaração de tipo associado de protocolo

Protocolos declaram tipos associados usando a palavra-chave `associatedtype`.
Um tipo associado fornece um alias para um tipo
que é usado como parte da declaração de um protocolo.
Tipos associados são semelhantes a parâmetros de tipo nas cláusulas de parâmetros genéricos,
mas são associados a `Self` no protocolo em que são declarados.
Nesse contexto, `Self` se refere ao tipo final que estiver em conformidade com o protocolo.
Para mais informações e exemplos,
veja <doc:Generics#Associated-Types>.

Você usa uma cláusula `where` genérica em uma declaração de protocolo
para adicionar restrições aos tipos associados herdados de outro protocolo,
sem declarar novamente os tipos associados.
Por exemplo, as declarações de `SubProtocol` abaixo são equivalentes:

```swift
protocol SomeProtocol {
    associatedtype SomeType
}

protocol SubProtocolA: SomeProtocol {
    // This syntax produces a warning.
    associatedtype SomeType: Equatable
}

// This syntax is preferred.
protocol SubProtocolB: SomeProtocol where SomeType: Equatable { }
```

<!--
  - test: `protocol-associatedtype`

  ```swifttest
  -> protocol SomeProtocol {
         associatedtype SomeType
     }

  -> protocol SubProtocolA: SomeProtocol {
         // This syntax produces a warning.
         associatedtype SomeType: Equatable
     }
  !$ warning: redeclaration of associated type 'SomeType' from protocol 'SomeProtocol' is better expressed as a 'where' clause on the protocol
  !! associatedtype SomeType: Equatable
  !! ~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~
  !!-
  !$ note: 'SomeType' declared here
  !! associatedtype SomeType
  !! ^

  // This syntax is preferred.
  -> protocol SubProtocolB: SomeProtocol where SomeType: Equatable { }
  ```
-->

<!--
  TODO: Finish writing this section after WWDC.
-->

<!--
  NOTE:
  What are associated types? What are they "associated" with? Is "Self"
  an implicit associated type of every protocol? [...]

  Here's an initial stab:
  An Associated Type is associated with an implementation of that protocol.
  The protocol declares it, and is defined as part of the protocol's implementation.

  "The ``Self`` type allows you to refer to the eventual type of ``self``
  (where ``self`` is the type that conforms to the protocol).
  In addition to ``Self``, a protocol's operations often need to refer to types
  that are related to the type of ``Self``, such as a type of data stored in a
  collection or the node and edge types of a graph." Is this still true?

    -> If we expand the discussion here,
    -> add a link from Types_SelfType
    -> to give more details about Self in protocols.

  NOTES from Doug:
  At one point, Self was an associated type, but that's the wrong modeling of
  the problem.  Self is the stand-in type for the thing that conforms to the
  protocol.  It's weird to think of it as an associated type because it's the
  primary thing.  It's certainly not an associated type.  In many ways, you
  can think of associated types as being parameters that get filled in by the
  conformance of a specific concrete type to that protocol.

  There's a substitution mapping here.  The parameters are associated with
  Self because they're derived from Self.  When you have a concrete type that
  conforms to a protocol, it supplies concrete types for Self and all the
  associated types.

  The associated types are like parameters, but they're associated with Self in
  the protocol.  Self is the eventual type of the thing that conforms to the
  protocol -- you have to have a name for it so you can do things with it.

  We use "associated" in contrast with generic parameters in interfaces in C#.
  The interesting thing there is that they don't have a name like Self for the
  actual type, but you can name any of these independent types.    In theory,
  they're often independent but in practice they're often not -- you have an
  interface parameterized on T, where all the uses of the thing are that T are
  the same as Self.  Instead of having these independent parameters to an
  interface, we have a named thing (Self) and all these other things that hand
  off of it.

  Here's a stupid simple way to see the distinction:

  C#:

  interface Sequence <Element> {}

  class String : Sequence <UnicodeScalar>
  class String : Sequence <GraphemeCluster>

  These are both fine in C#

  Swift:

  protocol Sequence { typealias Element }

  class String : Sequence { typealias Element = ... }

  Here you have to pick one or the other -- you can't have both.
-->

Veja também <doc:Declarations#Type-Alias-Declaration>.

> Gramática de uma declaração de tipo associado de protocolo:
>
> *protocol-associated-type-declaration* → *attributes*_?_ *access-level-modifier*_?_ **`associatedtype`** *typealias-name* *type-inheritance-clause*_?_ *typealias-assignment*_?_ *generic-where-clause*_?_

## Declaração de inicializador

Uma *declaração de inicializador* introduz um inicializador para uma classe,
struct ou enum no programa.
Declarações de inicializador são feitas com a palavra-chave `init` e têm
duas formas básicas.

Tipos struct, enum e classe podem ter qualquer número de inicializadores,
mas as regras e o comportamento associado dos inicializadores de classe são diferentes.
Diferentemente de structs e enums, classes têm dois tipos de inicializadores:
inicializadores designados e inicializadores de conveniência,
como descrito em <doc:Initialization>.

A forma a seguir declara inicializadores para structs, enums
e inicializadores designados de classes:

```swift
init(<#parameters#>) {
   <#statements#>
}
```

Um inicializador designado de uma classe inicializa
todas as propriedades da classe diretamente. Ele não pode chamar outros inicializadores
da mesma classe e, se a classe tiver uma superclasse, precisa chamar um dos
inicializadores designados da superclasse.
Se a classe herdar quaisquer propriedades da superclasse, um dos
inicializadores designados da superclasse precisa ser chamado antes que qualquer uma dessas
propriedades possa ser definida ou modificada na classe atual.

Inicializadores designados podem ser declarados somente no contexto de uma declaração de classe
e, por isso, não podem ser adicionados a uma classe usando uma declaração de extension.

Inicializadores em structs e enums podem chamar outros inicializadores declarados
para delegar parte ou todo o processo de inicialização.

Para declarar inicializadores de conveniência para uma classe,
marque a declaração do inicializador com o modificador de declaração `convenience`.

```swift
convenience init(<#parameters#>) {
   <#statements#>
}
```

Inicializadores de conveniência podem delegar o processo de inicialização para outro
inicializador de conveniência ou para um dos inicializadores designados da classe.
Mesmo assim, os processos de inicialização precisam terminar com uma chamada a um
inicializador designado que, no fim, inicializa as propriedades da classe.
Inicializadores de conveniência não podem chamar inicializadores da superclasse.

Você pode marcar inicializadores designados e de conveniência com o modificador de declaração `required`
para exigir que toda subclasse implemente o inicializador.
A implementação dessa subclasse para esse inicializador
também precisa ser marcada com o modificador de declaração `required`.

Por padrão, inicializadores declarados em uma superclasse
não são herdados por subclasses.
Mesmo assim, se uma subclasse inicializar todas as suas propriedades armazenadas com valores padrão
e não definir nenhum inicializador próprio,
ela herda todos os inicializadores da superclasse.
Se a subclasse sobrescrever todos os inicializadores designados da superclasse,
ela herda os inicializadores de conveniência da superclasse.

Assim como métodos, propriedades e subscripts,
você precisa marcar inicializadores designados sobrescritos com o modificador de declaração `override`.

> Nota: Se você marcar um inicializador com o modificador de declaração `required`,
> você não marca também o inicializador com o modificador `override`
> ao sobrescrever o inicializador obrigatório em uma subclasse.

Assim como funções e métodos, inicializadores podem lançar ou relançar erros.
E, assim como funções e métodos,
você usa a palavra-chave `throws` ou `rethrows` depois dos parâmetros de um inicializador
para indicar o comportamento apropriado.
Da mesma forma, inicializadores podem ser assíncronos,
e você usa a palavra-chave `async` para indicar isso.

Para ver exemplos de inicializadores em várias declarações de tipo,
veja <doc:Initialization>.

### Inicializadores falíveis

Um *inicializador falível* é um tipo de inicializador que produz uma instância optional
ou uma instância de implicitly unwrapped optional do tipo sobre o qual o inicializador é declarado.
Como resultado, um inicializador falível pode retornar `nil` para indicar que a inicialização falhou.

Para declarar um inicializador falível que produz uma instância optional,
acrescente um ponto de interrogação à palavra-chave `init` na declaração do inicializador (`init?`).
Para declarar um inicializador falível que produz uma instância de implicitly unwrapped optional,
acrescente um ponto de exclamação no lugar (`init!`). O exemplo abaixo mostra um inicializador falível `init?`
que produz uma instância optional de uma struct.

```swift
struct SomeStruct {
    let property: String
    // produces an optional instance of 'SomeStruct'
    init?(input: String) {
        if input.isEmpty {
            // discard 'self' and return 'nil'
            return nil
        }
        property = input
    }
}
```

<!--
  - test: `failable`

  ```swifttest
  -> struct SomeStruct {
         let property: String
         // produces an optional instance of 'SomeStruct'
         init?(input: String) {
             if input.isEmpty {
                 // discard 'self' and return 'nil'
                 return nil
             }
             property = input
         }
     }
  ```
-->

Você chama um inicializador falível `init?` da mesma forma que chama um inicializador não falível,
exceto que precisa lidar com o fato de o resultado ser um optional.

```swift
if let actualInstance = SomeStruct(input: "Hello") {
    // do something with the instance of 'SomeStruct'
} else {
    // initialization of 'SomeStruct' failed and the initializer returned 'nil'
}
```

<!--
  - test: `failable`

  ```swifttest
  -> if let actualInstance = SomeStruct(input: "Hello") {
         // do something with the instance of 'SomeStruct'
  >>     _ = actualInstance
     } else {
         // initialization of 'SomeStruct' failed and the initializer returned 'nil'
     }
  ```
-->

Um inicializador falível pode retornar `nil`
em qualquer ponto da implementação do corpo do inicializador.

Um inicializador falível pode delegar para qualquer tipo de inicializador.
Um inicializador não falível pode delegar para outro inicializador não falível
ou para um inicializador falível `init!`.
Um inicializador não falível pode delegar para um inicializador falível `init?`
usando force unwrapping no resultado do inicializador da superclasse ---
por exemplo, escrevendo `super.init()!`.

A falha de inicialização se propaga pela delegação de inicializadores.
Especificamente,
se um inicializador falível delegar para um inicializador que falha e retorna `nil`,
então o inicializador que delegou também falha e retorna `nil` implicitamente.
Se um inicializador não falível delegar para um inicializador falível `init!` que falha e retorna `nil`,
então um erro de tempo de execução é gerado
(como se você tivesse usado o operador `!` para fazer unwrap de um optional que tem valor `nil`).

Um inicializador designado falível pode ser sobrescrito em uma subclasse
por qualquer tipo de inicializador designado.
Um inicializador designado não falível pode ser sobrescrito em uma subclasse
somente por um inicializador designado não falível.

Para mais informações e para ver exemplos de inicializadores falíveis,
veja <doc:Initialization#Failable-Initializers>.

> Gramática de uma declaração de inicializador:
>
> *initializer-declaration* → *initializer-head* *generic-parameter-clause*_?_ *parameter-clause* **`async`**_?_ *throws-clause*_?_ *generic-where-clause*_?_ *initializer-body* \
> *initializer-declaration* → *initializer-head* *generic-parameter-clause*_?_ *parameter-clause* **`async`**_?_ **`rethrows`** *generic-where-clause*_?_ *initializer-body* \
> *initializer-head* → *attributes*_?_ *declaration-modifiers*_?_ **`init`** \
> *initializer-head* → *attributes*_?_ *declaration-modifiers*_?_ **`init`** **`?`** \
> *initializer-head* → *attributes*_?_ *declaration-modifiers*_?_ **`init`** **`!`** \
> *initializer-body* → *code-block*

## Declaração de desinicializador

Uma *declaração de desinicializador* declara um desinicializador para um tipo classe.
Desinicializadores não recebem parâmetros e têm a seguinte forma:

```swift
deinit {
   <#statements#>
}
```

Um desinicializador é chamado automaticamente quando não há mais referências
a um objeto de classe, logo antes de o objeto de classe ser desalocado.
Um desinicializador só pode ser declarado no corpo de uma declaração de classe ---
mas não em uma extension de classe ---
e cada classe pode ter no máximo um.

Uma subclasse herda o desinicializador da superclasse,
que é chamado implicitamente logo antes de o objeto da subclasse ser desalocado.
O objeto da subclasse só é desalocado depois que todos os desinicializadores na sua cadeia de herança
terminarem de executar.

Desinicializadores não são chamados diretamente.

Para um exemplo de como usar um desinicializador em uma declaração de classe,
veja <doc:Deinitialization>.

> Gramática de uma declaração de desinicializador:
>
> *deinitializer-declaration* → *attributes*_?_ **`deinit`** *code-block*
## Declaração de extension

Uma *declaração de extension* permite estender o comportamento
de tipos existentes.
Declarações de extension são feitas com a palavra-chave `extension`
e têm a seguinte forma:

```swift
extension <#type name#> where <#requirements#> {
   <#declarations#>
}
```

O corpo de uma declaração de extension contém zero ou mais *declarações*.
Essas *declarações* podem incluir propriedades computadas, propriedades computadas de tipo,
métodos de instância, métodos de tipo, inicializadores, declarações de subscript,
e até declarações de classe, struct e enum.
Declarações de extension não podem conter declarações de desinicializador ou de protocolo,
propriedades armazenadas, observadores de propriedade nem outras declarações de extension.
Declarações em uma extension de protocolo não podem ser marcadas com `final`.
Para uma discussão e vários exemplos de extensions que incluem diferentes tipos de declarações,
veja <doc:Extensions>.

Se o *nome do tipo* for um tipo classe, struct ou enum,
a extension estende esse tipo.
Se o *nome do tipo* for um tipo protocolo,
a extension estende todos os tipos que estão em conformidade com esse protocolo.

Declarações de extension que estendem um tipo genérico
ou um protocolo com tipos associados
podem incluir *requisitos*.
Se uma instância do tipo estendido
ou de um tipo que está em conformidade com o protocolo estendido
satisfizer os *requisitos*,
a instância ganha o comportamento especificado na declaração.

Declarações de extension podem conter declarações de inicializador. Ainda assim,
se o tipo que você está estendendo for definido em outro módulo,
uma declaração de inicializador deve delegar a um inicializador já definido nesse módulo
para garantir que os membros desse tipo sejam inicializados corretamente.

Propriedades, métodos e inicializadores de um tipo existente
não podem ser sobrescritos em uma extension desse tipo.

Declarações de extension podem adicionar conformidade com protocolo a um
tipo classe, struct ou enum existente, especificando os *protocolos adotados*:

```swift
extension <#type name#>: <#adopted protocols#> where <#requirements#> {
   <#declarations#>
}
```

Declarações de extension não podem adicionar herança de classe a uma classe existente,
por isso você pode especificar apenas uma lista de protocolos depois do *nome do tipo* e dos dois-pontos.

### Conformidade condicional

Você pode estender um tipo genérico
para que ele fique em conformidade condicional com um protocolo,
de modo que as instâncias do tipo estejam em conformidade com o protocolo
somente quando certos requisitos forem atendidos.
Você adiciona conformidade condicional a um protocolo
incluindo *requisitos* em uma declaração de extension.

#### Requisitos sobrescritos não são usados em alguns contextos genéricos

Em alguns contextos genéricos,
tipos que recebem comportamento pela conformidade condicional a um protocolo
nem sempre usam as implementações especializadas
dos requisitos desse protocolo.
Para ilustrar esse comportamento,
o exemplo a seguir define dois protocolos
e um tipo genérico que está em conformidade condicional com ambos.

<!--
  This test needs to be compiled so that it will recognize Pair's
  CustomStringConvertible conformance -- the deprecated REPL doesn't
  seem to use the description property at all.
-->

```swift
protocol Loggable {
    func log()
}
extension Loggable {
    func log() {
        print(self)
    }
}

protocol TitledLoggable: Loggable {
    static var logTitle: String { get }
}
extension TitledLoggable {
    func log() {
        print("\(Self.logTitle): \(self)")
    }
}

struct Pair<T>: CustomStringConvertible {
    let first: T
    let second: T
    var description: String {
        return "(\(first), \(second))"
    }
}

extension Pair: Loggable where T: Loggable { }
extension Pair: TitledLoggable where T: TitledLoggable {
    static var logTitle: String {
        return "Pair of '\(T.logTitle)'"
    }
}

extension String: TitledLoggable {
    static var logTitle: String {
        return "String"
    }
}
```

<!--
  - test: `conditional-conformance`

  ```swifttest
  -> protocol Loggable {
         func log()
     }
     extension Loggable {
         func log() {
             print(self)
         }
     }

     protocol TitledLoggable: Loggable {
         static var logTitle: String { get }
     }
     extension TitledLoggable {
         func log() {
             print("\(Self.logTitle): \(self)")
         }
     }

     struct Pair<T>: CustomStringConvertible {
         let first: T
         let second: T
         var description: String {
             return "(\(first), \(second))"
         }
     }

     extension Pair: Loggable where T: Loggable { }
     extension Pair: TitledLoggable where T: TitledLoggable {
         static var logTitle: String {
             return "Pair of '\(T.logTitle)'"
         }
     }

     extension String: TitledLoggable {
        static var logTitle: String {
           return "String"
        }
     }
  ```
-->

A struct `Pair` está em conformidade com `Loggable` e `TitledLoggable`
sempre que seu tipo genérico estiver em conformidade com `Loggable` ou `TitledLoggable`, respectivamente.
No exemplo abaixo,
`oneAndTwo` é uma instância de `Pair<String>`,
que está em conformidade com `TitledLoggable`
porque `String` está em conformidade com `TitledLoggable`.
Quando o método `log()` é chamado diretamente em `oneAndTwo`,
a versão especializada, que contém a string de título, é usada.

```swift
let oneAndTwo = Pair(first: "one", second: "two")
oneAndTwo.log()
// Prints "Pair of 'String': (one, two)".
```

<!--
  - test: `conditional-conformance`

  ```swifttest
  -> let oneAndTwo = Pair(first: "one", second: "two")
  -> oneAndTwo.log()
  <- Pair of 'String': (one, two)
  ```
-->

No entanto, quando `oneAndTwo` é usado em um contexto genérico
ou como instância do protocolo `Loggable`,
a versão especializada não é usada.
O Swift escolhe qual implementação de `log()` chamar
considerando apenas os requisitos mínimos que `Pair` precisa cumprir para estar em conformidade com `Loggable`.
Por esse motivo,
a implementação padrão fornecida pelo protocolo `Loggable` é usada.

```swift
func doSomething<T: Loggable>(with x: T) {
    x.log()
}
doSomething(with: oneAndTwo)
// Prints "(one, two)".
```

<!--
  - test: `conditional-conformance`

  ```swifttest
  -> func doSomething<T: Loggable>(with x: T) {
        x.log()
     }
     doSomething(with: oneAndTwo)
  <- (one, two)
  ```
-->

Quando `log()` é chamado na instância passada para `doSomething(_:)`,
o título personalizado é omitido da string registrada.

### A conformidade com protocolo não pode ser redundante

Um tipo concreto pode estar em conformidade com um protocolo específico apenas uma vez.
O Swift marca conformidades redundantes a protocolo como erro.
Você provavelmente vai encontrar esse tipo de erro
em duas situações.
A primeira é quando
você declara conformidade explícita ao mesmo protocolo várias vezes,
mas com requisitos diferentes.
A segunda é quando
você herda implicitamente do mesmo protocolo várias vezes.
Essas situações são discutidas nas seções abaixo.

#### Resolvendo a redundância explícita

Várias extensions de um tipo concreto
não podem adicionar conformidade ao mesmo protocolo,
mesmo que os requisitos das extensions sejam mutuamente exclusivos.
Essa restrição é demonstrada no exemplo abaixo.
Duas declarações de extension tentam adicionar conformidade condicional
ao protocolo `Serializable`,
uma para arrays com elementos `Int`
e outra para arrays com elementos `String`.

```swift
protocol Serializable {
    func serialize() -> Any
}

extension Array: Serializable where Element == Int {
    func serialize() -> Any {
        // implementation
    }
}
extension Array: Serializable where Element == String {
    func serialize() -> Any {
        // implementation
    }
}
// Error: Redundant conformance of 'Array<Element>' to protocol 'Serializable'.
```

<!--
  - test: `multiple-conformances`

  ```swifttest
  -> protocol Serializable {
        func serialize() -> Any
     }

     extension Array: Serializable where Element == Int {
         func serialize() -> Any {
             // implementation
  >>         return 0
  ->     }
     }
     extension Array: Serializable where Element == String {
         func serialize() -> Any {
             // implementation
  >>         return 0
  ->     }
     }
  // Error: Redundant conformance of 'Array<Element>' to protocol 'Serializable'.
  !$ error: conflicting conformance of 'Array<Element>' to protocol 'Serializable'; there cannot be more than one conformance, even with different conditional bounds
  !! extension Array: Serializable where Element == String {
  !! ^
  !$ note: 'Array<Element>' declares conformance to protocol 'Serializable' here
  !! extension Array: Serializable where Element == Int {
  !! ^
  ```
-->

Se você precisar adicionar conformidade condicional com base em vários tipos concretos,
crie um novo protocolo ao qual cada tipo possa estar em conformidade
e use esse protocolo como requisito ao declarar a conformidade condicional.

```swift
protocol SerializableInArray { }
extension Int: SerializableInArray { }
extension String: SerializableInArray { }

extension Array: Serializable where Element: SerializableInArray {
    func serialize() -> Any {
        // implementation
    }
}
```

<!--
  - test: `multiple-conformances-success`

  ```swifttest
  >> protocol Serializable { }
  -> protocol SerializableInArray { }
     extension Int: SerializableInArray { }
     extension String: SerializableInArray { }

  -> extension Array: Serializable where Element: SerializableInArray {
         func serialize() -> Any {
             // implementation
  >>         return 0
  ->     }
     }
  ```
-->

#### Resolvendo a redundância implícita

Quando um tipo concreto está em conformidade condicional com um protocolo,
esse tipo passa a estar implicitamente em conformidade com quaisquer protocolos pais
que tenham os mesmos requisitos.

Se você precisar que um tipo esteja em conformidade condicional com dois protocolos
que herdam de um único pai,
declare explicitamente a conformidade com o protocolo pai.
Isso evita que o tipo fique implicitamente em conformidade com o protocolo pai duas vezes,
com requisitos diferentes.

O exemplo a seguir declara explicitamente
a conformidade condicional de `Array` a `Loggable`
para evitar um conflito ao declarar sua conformidade condicional
tanto a `TitledLoggable` quanto ao novo protocolo `MarkedLoggable`.

```swift
protocol MarkedLoggable: Loggable {
    func markAndLog()
}

extension MarkedLoggable {
    func markAndLog() {
        print("----------")
        log()
    }
}

extension Array: Loggable where Element: Loggable { }
extension Array: TitledLoggable where Element: TitledLoggable {
    static var logTitle: String {
        return "Array of '\(Element.logTitle)'"
    }
}
extension Array: MarkedLoggable where Element: MarkedLoggable { }
```

<!--
  - test: `conditional-conformance`

  ```swifttest
  -> protocol MarkedLoggable: Loggable {
        func markAndLog()
     }

     extension MarkedLoggable {
        func markAndLog() {
           print("----------")
           log()
        }
     }

     extension Array: Loggable where Element: Loggable { }
     extension Array: TitledLoggable where Element: TitledLoggable {
        static var logTitle: String {
           return "Array of '\(Element.logTitle)'"
        }
     }
     extension Array: MarkedLoggable where Element: MarkedLoggable { }
  ```
-->

Sem a extension que declara explicitamente a conformidade condicional a `Loggable`,
as outras extensions de `Array` criariam implicitamente essas declarações,
resultando em um erro:

```swift
extension Array: Loggable where Element: TitledLoggable { }
extension Array: Loggable where Element: MarkedLoggable { }
// Error: Redundant conformance of 'Array<Element>' to protocol 'Loggable'.
```

<!--
  - test: `conditional-conformance-implicit-overlap`

  ```swifttest
  >> protocol Loggable { }
  >> protocol MarkedLoggable : Loggable { }
  >> protocol TitledLoggable : Loggable { }
  -> extension Array: Loggable where Element: TitledLoggable { }
     extension Array: Loggable where Element: MarkedLoggable { }
  // Error: Redundant conformance of 'Array<Element>' to protocol 'Loggable'.
  !$ error: conflicting conformance of 'Array<Element>' to protocol 'Loggable'; there cannot be more than one conformance, even with different conditional bounds
  !! extension Array: Loggable where Element: MarkedLoggable { }
  !! ^
  !$ note: 'Array<Element>' declares conformance to protocol 'Loggable' here
  !! extension Array: Loggable where Element: TitledLoggable { }
  !! ^
  ```
-->

<!--
  - test: `types-cant-have-multiple-implicit-conformances`

  ```swifttest
  >> protocol Loggable { }
     protocol TitledLoggable: Loggable { }
     protocol MarkedLoggable: Loggable { }
     extension Array: TitledLoggable where Element: TitledLoggable {
         // ...
     }
     extension Array: MarkedLoggable where Element: MarkedLoggable { }
  !$ error: conditional conformance of type 'Array<Element>' to protocol 'TitledLoggable' does not imply conformance to inherited protocol 'Loggable'
  !! extension Array: TitledLoggable where Element: TitledLoggable {
  !! ^
  !$ note: did you mean to explicitly state the conformance like 'extension Array: Loggable where ...'?
  !! extension Array: TitledLoggable where Element: TitledLoggable {
  !! ^
  !$ error: type 'Array<Element>' does not conform to protocol 'MarkedLoggable'
  !! extension Array: MarkedLoggable where Element: MarkedLoggable { }
  !! ^
  !$ error: type 'Element' does not conform to protocol 'TitledLoggable'
  !! extension Array: MarkedLoggable where Element: MarkedLoggable { }
  !! ^
  !$ error: 'MarkedLoggable' requires that 'Element' conform to 'TitledLoggable'
  !! extension Array: MarkedLoggable where Element: MarkedLoggable { }
  !! ^
  !$ note: requirement specified as 'Element' : 'TitledLoggable'
  !! extension Array: MarkedLoggable where Element: MarkedLoggable { }
  !! ^
  !$ note: requirement from conditional conformance of 'Array<Element>' to 'Loggable'
  !! extension Array: MarkedLoggable where Element: MarkedLoggable { }
  !! ^
  ```
-->

<!--
  - test: `extension-can-have-where-clause`

  ```swifttest
  >> extension Array where Element: Equatable {
         func f(x: Array) -> Int { return 7 }
     }
  >> let x = [1, 2, 3]
  >> let y = [10, 20, 30]
  >> let r0 = x.f(x: y)
  >> assert(r0 == 7)
  ```
-->

<!--
  - test: `extensions-can-have-where-clause-and-inheritance-together`

  ```swifttest
  >> protocol P { func foo() -> Int }
  >> extension Array: P where Element: Equatable {
  >>    func foo() -> Int { return 0 }
  >> }
  >> let r0 = [1, 2, 3].foo()
  >> assert(r0 == 0)
  ```
-->

> Gramática de uma declaração de extension:
>
> *extension-declaration* → *attributes*_?_ *access-level-modifier*_?_ **`extension`** *type-identifier* *type-inheritance-clause*_?_ *generic-where-clause*_?_ *extension-body* \
> *extension-body* → **`{`** *extension-members*_?_ **`}`**
>
> *extension-members* → *extension-member* *extension-members*_?_ \
> *extension-member* → *declaration* | *compiler-control-statement*

## Declaração de subscript

Uma declaração de *subscript* permite adicionar suporte a subscripts para objetos
de um tipo específico, e geralmente é usada para oferecer uma sintaxe prática
para acessar os elementos de uma coleção, lista ou sequência.
Declarações de subscript são feitas com a palavra-chave `subscript`
e têm a seguinte forma:

```swift
subscript (<#parameters#>) -> <#return type#> {
   get {
      <#statements#>
   }
   set(<#setter name#>) {
      <#statements#>
   }
}
```

Declarações de subscript só podem aparecer no contexto de uma declaração de classe, struct,
enum, extension ou protocolo.

Os *parâmetros* especificam um ou mais índices usados para acessar elementos do tipo correspondente
em uma expressão de subscript (por exemplo, o `i` na expressão `object[i]`).
Embora os índices usados para acessar os elementos possam ser de qualquer tipo,
cada parâmetro precisa ter uma anotação de tipo para especificar o tipo de cada índice.
O *tipo de retorno* especifica o tipo do elemento acessado.

Assim como nas propriedades computadas,
as declarações de subscript permitem ler e escrever o valor dos elementos acessados.
O getter é usado para ler o valor,
e o setter é usado para escrever o valor.
A cláusula setter é opcional,
e, quando só é preciso um getter, você pode omitir as duas cláusulas e simplesmente
retornar o valor pedido diretamente.
Ainda assim, se você fornecer uma cláusula setter, também precisa fornecer uma cláusula getter.

O *nome do setter* e os parênteses que o envolvem são opcionais.
Se você fornecer um nome de setter, ele é usado como o nome do parâmetro do setter.
Se não fornecer um nome de setter, o nome padrão do parâmetro do setter é `newValue`.
O tipo do parâmetro do setter é o mesmo do *tipo de retorno*.

Você pode sobrecarregar uma declaração de subscript no tipo em que ela é declarada,
desde que os *parâmetros* ou o *tipo de retorno* sejam diferentes do que está sendo sobrecarregado.
Você também pode sobrescrever uma declaração de subscript herdada de uma superclasse. Ao fazer isso,
é preciso marcar a declaração de subscript sobrescrita com o modificador de declaração `override`.

Os parâmetros de subscript seguem as mesmas regras dos parâmetros de função,
com duas exceções.
Por padrão, os parâmetros usados em subscripts não têm rótulos de argumento,
diferentemente de funções, métodos e inicializadores.
No entanto, você pode fornecer rótulos de argumento explícitos
usando a mesma sintaxe que funções, métodos e inicializadores usam.
Além disso, subscripts não podem ter parâmetros in-out.
Um parâmetro de subscript pode ter um valor padrão,
usando a sintaxe descrita em <doc:Declarations#Special-Kinds-of-Parameters>.

Você também pode declarar subscripts no contexto de uma declaração de protocolo,
como descrito em <doc:Declarations#Protocol-Subscript-Declaration>.

Para mais informações sobre subscripts e para ver exemplos de declarações de subscript,
veja <doc:Subscripts>.

### Declarações de subscript de tipo

Para declarar um subscript exposto pelo tipo,
e não pelas instâncias do tipo,
marque a declaração de subscript com o modificador de declaração `static`.
Classes podem, em vez disso, marcar propriedades computadas de tipo com o modificador de declaração `class`
para permitir que subclasses sobrescrevam a implementação da superclasse.
Em uma declaração de classe,
a palavra-chave `static` tem o mesmo efeito que marcar a declaração
com os modificadores de declaração `class` e `final`.

<!--
  - test: `cant-override-static-subscript-in-subclass`

  ```swifttest
  -> class Super { static subscript(i: Int) -> Int { return 10 } }
  -> class Sub: Super { override static subscript(i: Int) -> Int { return 100 } }
  !$ error: cannot override static subscript
  !! class Sub: Super { override static subscript(i: Int) -> Int { return 100 } }
  !!                                    ^
  !$ note: overridden declaration is here
  !! class Super { static subscript(i: Int) -> Int { return 10 } }
  !!                      ^
  ```
-->

> Gramática de uma declaração de subscript:
>
> *subscript-declaration* → *subscript-head* *subscript-result* *generic-where-clause*_?_ *code-block* \
> *subscript-declaration* → *subscript-head* *subscript-result* *generic-where-clause*_?_ *getter-setter-block* \
> *subscript-declaration* → *subscript-head* *subscript-result* *generic-where-clause*_?_ *getter-setter-keyword-block* \
> *subscript-head* → *attributes*_?_ *declaration-modifiers*_?_ **`subscript`** *generic-parameter-clause*_?_ *parameter-clause* \
> *subscript-result* → **`->`** *attributes*_?_ *type*

## Declaração de macro

Uma *declaração de macro* introduz uma nova macro.
Ela começa com a palavra-chave `macro`
e tem a seguinte forma:

```swift
macro <#name#> = <#macro implementation#>
```

A *implementação da macro* é outra macro
e indica a localização do código que realiza a expansão da macro.
O código que realiza a expansão de macro é um programa Swift separado,
que usa o módulo [SwiftSyntax][] para interagir com código Swift.
Chame a macro `externalMacro(module:type:)` da biblioteca padrão do Swift,
passando o nome de um tipo que contém a implementação da macro
e o nome do módulo que contém esse tipo.

[SwiftSyntax]: https://github.com/swiftlang/swift-syntax

Macros podem ser sobrecarregadas,
seguindo o mesmo modelo usado por funções.
Uma declaração de macro aparece apenas no escopo de arquivo.

Para uma visão geral das macros em Swift, veja <doc:Macros>.

> Gramática de uma declaração de macro:
>
> *macro-declaration* → *macro-head* *identifier* *generic-parameter-clause*_?_ *macro-signature* *macro-definition*_?_ *generic-where-clause* \
> *macro-head* → *attributes*_?_ *declaration-modifiers*_?_ **`macro`** \
> *macro-signature* → *parameter-clause* *macro-function-signature-result*_?_ \
> *macro-function-signature-result* → **`->`** *type* \
> *macro-definition* → **`=`** *expression*


## Declaração de operador

Uma *declaração de operador* introduz um novo operador infixo, prefixo
ou pós-fixo no programa,
e é declarada com a palavra-chave `operator`.

Você pode declarar operadores de três fixidades diferentes:
infixa, prefixa e pós-fixa.
A *fixidade* de um operador especifica a posição relativa do operador
em relação aos operandos.

Há três formas básicas de declaração de operador,
uma para cada fixidade.
A fixidade do operador é especificada marcando a declaração do operador com o
modificador de declaração `infix`, `prefix` ou `postfix` antes da palavra-chave `operator`.
Em cada forma, o nome do operador pode conter apenas os caracteres de operador
definidos em <doc:LexicalStructure#Operators>.

A forma a seguir declara um novo operador infixo:

```swift
infix operator <#operator name#>: <#precedence group#>
```

Um *operador infixo* é um operador binário escrito entre seus dois operandos,
como o conhecido operador de adição (`+`) na expressão `1 + 2`.

Operadores infixos podem, opcionalmente, especificar um grupo de precedência.
Se você omitir o grupo de precedência de um operador,
o Swift usa o grupo de precedência padrão, `DefaultPrecedence`,
que especifica uma precedência logo acima de `TernaryPrecedence`.
Para mais informações, veja <doc:Declarations#Precedence-Group-Declaration>.

A forma a seguir declara um novo operador prefixo:

```swift
prefix operator <#operator name#>
```

Um *operador prefixo* é um operador unário escrito imediatamente antes do seu operando,
como o operador prefixo de negação lógica (`!`) na expressão `!a`.

Declarações de operadores prefixos não especificam um nível de precedência.
Operadores prefixos são não associativos.

A forma a seguir declara um novo operador pós-fixo:

```swift
postfix operator <#operator name#>
```

Um *operador pós-fixo* é um operador unário escrito imediatamente depois do seu operando,
como o operador pós-fixo de force unwrapping (`!`) na expressão `a!`.

Assim como nos operadores prefixos, declarações de operadores pós-fixos não especificam um nível de precedência.
Operadores pós-fixos são não associativos.

Depois de declarar um novo operador,
você o implementa declarando um método estático com o mesmo nome do operador.
O método estático é um membro de
um dos tipos cujos valores o operador recebe como argumento ---
por exemplo, um operador que multiplica um `Double` por um `Int`
é implementado como um método estático na struct `Double` ou `Int`.
Se você estiver implementando um operador prefixo ou pós-fixo,
também precisa marcar a declaração desse método com o modificador de declaração `prefix` ou `postfix` correspondente.
Para ver um exemplo de como criar e implementar um novo operador,
veja <doc:AdvancedOperators#Custom-Operators>.

> Gramática de uma declaração de operador:
>
> *operator-declaration* → *prefix-operator-declaration* | *postfix-operator-declaration* | *infix-operator-declaration*
>
> *prefix-operator-declaration* → **`prefix`** **`operator`** *operator* \
> *postfix-operator-declaration* → **`postfix`** **`operator`** *operator* \
> *infix-operator-declaration* → **`infix`** **`operator`** *operator* *infix-operator-group*_?_
>
> *infix-operator-group* → **`:`** *precedence-group-name*

## Declaração de grupo de precedência

Uma *declaração de grupo de precedência* introduz
um novo agrupamento de precedência para operadores infixos no programa.
A precedência de um operador especifica o quão firmemente o operador
se liga aos operandos, na ausência de parênteses de agrupamento.

Uma declaração de grupo de precedência tem a seguinte forma:

```swift
precedencegroup <#precedence group name#> {
    higherThan: <#lower group names#>
    lowerThan: <#higher group names#>
    associativity: <#associativity#>
    assignment: <#assignment#>
}
```

As listas de *nomes de grupos inferiores* e *nomes de grupos superiores* especificam
a relação do novo grupo de precedência com os grupos de precedência existentes.
O atributo `lowerThan` do grupo de precedência só pode ser usado
para se referir a grupos de precedência declarados fora do módulo atual.
Quando dois operadores competem entre si pelos operandos,
como na expressão `2 + 3 * 5`,
o operador com maior precedência relativa
se liga mais firmemente aos operandos.

> Nota: Grupos de precedência relacionados entre si
> por meio de *nomes de grupos inferiores* e *nomes de grupos superiores*
> precisam caber em uma única hierarquia relacional,
> mas eles *não* precisam formar uma hierarquia linear.
> Isso significa que é possível ter grupos de precedência
> com precedência relativa indefinida.
> Operadores desses grupos de precedência
> não podem ser usados lado a lado sem parênteses de agrupamento.

O Swift define vários grupos de precedência para acompanhar os operadores
fornecidos pela biblioteca padrão do Swift.
Por exemplo, os operadores de adição (`+`) e subtração (`-`)
pertencem ao grupo `AdditionPrecedence`,
e os operadores de multiplicação (`*`) e divisão (`/`)
pertencem ao grupo `MultiplicationPrecedence`.
Para ver a lista completa dos grupos de precedência
fornecidos pela biblioteca padrão do Swift,
veja [Declarações de operador](https://developer.apple.com/documentation/swift/operator_declarations).

A *associatividade* de um operador especifica como uma sequência de operadores
com o mesmo nível de precedência é agrupada na ausência de parênteses de agrupamento.
Você especifica a associatividade de um operador escrevendo
uma das palavras-chave contextuais `left`, `right` ou `none` ---
se você omitir a associatividade, o padrão é `none`.
Operadores associativos à esquerda agrupam da esquerda para a direita.
Por exemplo,
o operador de subtração (`-`) é associativo à esquerda,
então a expressão `4 - 5 - 6` é agrupada como `(4 - 5) - 6`
e resulta em `-7`.
Operadores associativos à direita agrupam da direita para a esquerda,
e operadores especificados com associatividade `none`
não se associam de forma alguma.
Operadores não associativos de mesmo nível de precedência
não podem aparecer lado a lado um do outro.
Por exemplo,
o operador `<` tem associatividade `none`,
o que significa que `1 < 2 < 3` não é uma expressão válida.

A *atribuição* de um grupo de precedência especifica a precedência de um operador
quando usado em uma operação que inclui optional chaining.
Quando definida como `true`, um operador do grupo de precedência correspondente
usa as mesmas regras de agrupamento durante o optional chaining
que os operadores de atribuição da biblioteca padrão do Swift.
Caso contrário, quando definida como `false` ou omitida,
os operadores do grupo de precedência seguem as mesmas regras de optional chaining
que os operadores que não realizam atribuição.

> Gramática de uma declaração de grupo de precedência:
>
> *precedence-group-declaration* → **`precedencegroup`** *precedence-group-name* **`{`** *precedence-group-attributes*_?_ **`}`**
>
> *precedence-group-attributes* → *precedence-group-attribute* *precedence-group-attributes*_?_ \
> *precedence-group-attribute* → *precedence-group-relation* \
> *precedence-group-attribute* → *precedence-group-assignment* \
> *precedence-group-attribute* → *precedence-group-associativity*
>
> *precedence-group-relation* → **`higherThan`** **`:`** *precedence-group-names* \
> *precedence-group-relation* → **`lowerThan`** **`:`** *precedence-group-names*
>
> *precedence-group-assignment* → **`assignment`** **`:`** *boolean-literal*
>
> *precedence-group-associativity* → **`associativity`** **`:`** **`left`** \
> *precedence-group-associativity* → **`associativity`** **`:`** **`right`** \
> *precedence-group-associativity* → **`associativity`** **`:`** **`none`**
>
> *precedence-group-names* → *precedence-group-name* | *precedence-group-name* **`,`** *precedence-group-names* \
> *precedence-group-name* → *identifier*

## Modificadores de declaração

*Modificadores de declaração* são palavras-chave ou palavras-chave contextuais que modificam o comportamento
ou o significado de uma declaração. Você especifica um modificador de declaração escrevendo a palavra-chave
apropriada ou a palavra-chave contextual entre os atributos da declaração (se houver) e a palavra-chave
que introduz a declaração.

- term `class`:
  Aplique este modificador a um membro de uma classe
  para indicar que o membro é um membro da própria classe,
  e não de instâncias da classe.
  Membros de uma superclasse que têm este modificador
  e não têm o modificador `final`
  podem ser sobrescritos por subclasses.

- term `dynamic`:
  Aplique este modificador a qualquer membro de uma classe que possa ser representado em Objective-C.
  Quando você marca uma declaração de membro com o modificador `dynamic`,
  o acesso a esse membro é sempre despachado dinamicamente usando o tempo de execução (runtime) do Objective-C.
  O acesso a esse membro nunca é embutido (inlined) nem desvirtualizado pelo compilador.

  Como declarações marcadas com o modificador `dynamic` são despachadas
  usando o tempo de execução (runtime) do Objective-C, elas precisam ser marcadas com o
  atributo `objc`.

- term `final`:
  Aplique este modificador a uma classe ou a uma propriedade, método
  ou subscript membro de uma classe. Ele é aplicado a uma classe para indicar que a classe
  não pode ter subclasses. Ele é aplicado a uma propriedade, método ou subscript de uma classe
  para indicar que um membro da classe não pode ser sobrescrito em nenhuma subclasse.
  Para um exemplo de como usar o atributo `final`,
  veja <doc:Inheritance#Preventing-Overrides>.

- term `lazy`:
  Aplique este modificador a uma propriedade de variável armazenada de uma classe ou struct
  para indicar que o valor inicial da propriedade é calculado e armazenado no máximo
  uma vez, quando a propriedade é acessada pela primeira vez.
  Para um exemplo de como usar o modificador `lazy`,
  veja <doc:Properties#Lazy-Stored-Properties>.

- term `optional`:
  Aplique este modificador aos membros de propriedade, método
  ou subscript de um protocolo para indicar que um tipo que o adota não é obrigado
  a implementar esses membros.

  Você só pode aplicar o modificador `optional` a protocolos marcados
  com o atributo `objc`. Por isso, apenas tipos classe podem adotar e estar em conformidade
  com um protocolo que contém requisitos optional de membros.
  Para mais informações sobre como usar o modificador `optional`
  e orientações sobre como acessar membros optional de protocolo ---
  por exemplo, quando você não tem certeza se um tipo em conformidade os implementa ---
  veja <doc:Protocols#Optional-Protocol-Requirements>.

<!--
  TODO: Currently, you can't check for an optional initializer,
  so we're leaving those out of the documentation, even though you can mark
  an initializer with the @optional attribute. It's still being decided by the
  compiler team. Update this section if they decide to make everything work
  properly for optional initializer requirements.
-->

- term `required`:
  Aplique este modificador a um inicializador designado ou de conveniência
  de uma classe para indicar que toda subclasse deve implementar esse inicializador.
  A implementação desse inicializador na subclasse
  também deve ser marcada com o modificador `required`.

- term `static`:
  Aplique este modificador a um membro de uma struct, classe, enum ou protocolo
  para indicar que o membro é um membro do tipo,
  e não de instâncias desse tipo.
  No escopo de uma declaração de classe,
  escrever o modificador `static` em uma declaração de membro
  tem o mesmo efeito que escrever os modificadores `class` e `final`
  nessa declaração de membro.
  No entanto, propriedades de tipo constantes de uma classe são uma exceção:
  ali, `static` tem seu significado normal, de não classe,
  porque você não pode escrever `class` ou `final` nessas declarações.

- term `unowned`:
  Aplique este modificador a uma variável, constante ou propriedade armazenada
  para indicar que a variável ou propriedade tem uma referência unowned
  para o objeto armazenado como seu valor.
  Se você tentar acessar a variável ou propriedade
  depois que o objeto foi desalocado,
  um erro de tempo de execução é gerado.
  Assim como uma referência weak,
  o tipo da propriedade ou do valor deve ser um tipo classe;
  diferente de uma referência weak,
  o tipo não é optional.
  Para um exemplo e mais informações sobre o modificador `unowned`,
  veja <doc:AutomaticReferenceCounting#Unowned-References>.

- term `unowned(safe)`:
  Uma forma explícita de escrever `unowned`.

- term `unowned(unsafe)`:
  Aplique este modificador a uma variável, constante ou propriedade armazenada
  para indicar que a variável ou propriedade tem uma referência unowned
  para o objeto armazenado como seu valor.
  Se você tentar acessar a variável ou propriedade
  depois que o objeto foi desalocado,
  você acessará a memória no local onde o objeto costumava estar,
  o que é uma operação insegura para a memória.
  Assim como uma referência weak,
  o tipo da propriedade ou do valor deve ser um tipo classe;
  diferente de uma referência weak,
  o tipo não é optional.
  Para um exemplo e mais informações sobre o modificador `unowned`,
  veja <doc:AutomaticReferenceCounting#Unowned-References>.

- term `weak`:
  Aplique este modificador a uma variável armazenada ou a uma propriedade de variável armazenada
  para indicar que a variável ou propriedade tem uma referência weak para o
  objeto armazenado como seu valor. O tipo da variável ou propriedade
  deve ser um tipo classe optional.
  Se você acessar a variável ou propriedade
  depois que o objeto foi desalocado,
  seu valor é `nil`.
  Para um exemplo e mais informações sobre o modificador `weak`,
  veja <doc:AutomaticReferenceCounting#Weak-References>.

### Níveis de controle de acesso

O Swift oferece cinco níveis de controle de acesso: open, public, internal, file private e private.
Você pode marcar uma declaração com um dos modificadores de nível de acesso abaixo
para especificar o nível de acesso da declaração.
O controle de acesso é discutido em detalhes em <doc:AccessControl>.

- term `open`:
  Aplique este modificador a uma declaração para indicar que a declaração pode ser acessada e ter subclasses
  por código no mesmo módulo da declaração.
  Declarações marcadas com o modificador de nível de acesso `open` também podem ser acessadas e ter subclasses
  por código em um módulo que importa o módulo que contém essa declaração.

- term `public`:
  Aplique este modificador a uma declaração para indicar que a declaração pode ser acessada e ter subclasses
  por código no mesmo módulo da declaração.
  Declarações marcadas com o modificador de nível de acesso `public` também podem ser acessadas (mas não ter subclasses)
  por código em um módulo que importa o módulo que contém essa declaração.

- term `package`:
  Aplique este modificador a uma declaração
  para indicar que a declaração só pode ser acessada
  por código no mesmo pacote da declaração.
  Um pacote é uma unidade de distribuição de código
  que você define no sistema de build que está usando.
  Quando o sistema de build compila o código,
  ele especifica o nome do pacote
  passando a flag `-package-name` para o compilador do Swift.
  Dois módulos fazem parte do mesmo pacote
  se o sistema de build especificar o mesmo nome de pacote ao compilá-los.

- term `internal`:
  Aplique este modificador a uma declaração para indicar que a declaração pode ser acessada
  apenas por código no mesmo módulo da declaração.
  Por padrão,
  a maioria das declarações é marcada implicitamente com o modificador de nível de acesso `internal`.

- term `fileprivate`:
  Aplique este modificador a uma declaração para indicar que a declaração pode ser acessada
  apenas por código no mesmo arquivo de código-fonte da declaração.

- term `private`:
  Aplique este modificador a uma declaração para indicar que a declaração pode ser acessada
  apenas por código dentro do escopo imediatamente envolvente da declaração.

Para fins de controle de acesso,
extensions se comportam da seguinte forma:

- Se houver várias extensions no mesmo arquivo,
  e todas essas extensions estenderem o mesmo tipo,
  então todas elas terão o mesmo escopo de controle de acesso.
  As extensions e o tipo que elas estendem podem estar em arquivos diferentes.

- Se houver extensions no mesmo arquivo que o tipo que elas estendem,
  as extensions têm o mesmo escopo de controle de acesso que o tipo estendido.

- Membros private declarados na declaração de um tipo
  podem ser acessados a partir de extensions desse tipo.
  Membros private declarados em uma extension
  podem ser acessados a partir de outras extensions
  e da declaração do tipo estendido.

Cada modificador de nível de acesso acima aceita opcionalmente um único argumento,
que consiste na palavra-chave `set` entre parênteses ---
por exemplo, `private(set)`.
Use essa forma de modificador de nível de acesso quando quiser especificar um nível de acesso
para o setter de uma variável ou subscript que seja menor ou igual
ao nível de acesso da própria variável ou subscript,
como discutido em <doc:AccessControl#Getters-and-Setters>.

> Gramática de um modificador de declaração:
>
> *declaration-modifier* → **`class`** | **`convenience`** | **`dynamic`** | **`final`** | **`infix`** | **`lazy`** | **`optional`** | **`override`** | **`postfix`** | **`prefix`** | **`required`** | **`static`** | **`unowned`** | **`unowned`** **`(`** **`safe`** **`)`** | **`unowned`** **`(`** **`unsafe`** **`)`** | **`weak`** \
> *declaration-modifier* → *access-level-modifier* \
> *declaration-modifier* → *mutation-modifier* \
> *declaration-modifier* → *actor-isolation-modifier* \
> *declaration-modifiers* → *declaration-modifier* *declaration-modifiers*_?_
>
> *access-level-modifier* → **`private`** | **`private`** **`(`** **`set`** **`)`** \
> *access-level-modifier* → **`fileprivate`** | **`fileprivate`** **`(`** **`set`** **`)`** \
> *access-level-modifier* → **`internal`** | **`internal`** **`(`** **`set`** **`)`** \
> *access-level-modifier* → **`package`** | **`package`** **`(`** **`set`** **`)`** \
> *access-level-modifier* → **`public`** | **`public`** **`(`** **`set`** **`)`** \
> *access-level-modifier* → **`open`** | **`open`** **`(`** **`set`** **`)`**
>
> *mutation-modifier* → **`mutating`** | **`nonmutating`**
>
> *actor-isolation-modifier* → **`nonisolated`**

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->

<!-- ia-translate: true -->
