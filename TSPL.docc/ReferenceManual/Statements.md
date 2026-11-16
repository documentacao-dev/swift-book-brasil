# Instruções

Agrupe expressões e controle o fluxo de execução.

Em Swift, há três tipos de instruções: instruções simples, instruções de controle do compilador
e instruções de controle de fluxo.
Instruções simples são as mais comuns e consistem em uma expressão ou uma declaração.
Instruções de controle do compilador permitem que o programa altere aspectos do comportamento do compilador
e incluem um bloco de compilação condicional e uma instrução de controle de linha.

Instruções de controle de fluxo são usadas para controlar o fluxo de execução em um programa.
Há vários tipos de instruções de controle de fluxo em Swift, incluindo
instruções de loop, instruções de desvio e instruções de transferência de controle.
Instruções de loop permitem que um bloco de código seja executado repetidamente,
instruções de desvio permitem que determinado bloco de código seja executado
somente quando certas condições são atendidas,
e instruções de transferência de controle oferecem uma forma de alterar a ordem em que o código é executado.
Além disso, Swift oferece uma instrução `do` para introduzir um escopo
e capturar e tratar erros,
e uma instrução `defer` para executar ações de limpeza logo antes de o escopo atual terminar.

Um ponto e vírgula (`;`) pode aparecer opcionalmente depois de qualquer instrução
e é usado para separar várias instruções que aparecem na mesma linha.

> Gramática de uma instrução:
>
> *statement* → *expression* **`;`**_?_ \
> *statement* → *declaration* **`;`**_?_ \
> *statement* → *loop-statement* **`;`**_?_ \
> *statement* → *branch-statement* **`;`**_?_ \
> *statement* → *labeled-statement* **`;`**_?_ \
> *statement* → *control-transfer-statement* **`;`**_?_ \
> *statement* → *defer-statement* **`;`**_?_ \
> *statement* → *do-statement* **`;`**_?_ \
> *statement* → *compiler-control-statement* \
> *statements* → *statement* *statements*_?_

<!--
  NOTE: Removed semicolon-statement as syntactic category,
  because, according to Doug, they're not really statements.
  For example, you can't have
      if foo { ; }
  but you should be able to if it's truly considered a statement.
  The semicolon isn't even required for the compiler; we just added
  rules that require them in some places to enforce a certain amount
  of readability.
-->

## Instruções de loop

Instruções de loop permitem que um bloco de código seja executado repetidamente,
dependendo das condições especificadas no loop.
Swift tem três instruções de loop:
uma instrução `for`-`in`,
uma instrução `while`
e uma instrução `repeat`-`while`.

O fluxo de controle em uma instrução de loop pode ser alterado por uma instrução `break`
e por uma instrução `continue`, discutidas em <doc:Statements#Break-Statement> e
<doc:Statements#Continue-Statement> abaixo.

> Gramática de uma instrução de loop:
>
> *loop-statement* → *for-in-statement* \
> *loop-statement* → *while-statement* \
> *loop-statement* → *repeat-while-statement*

### Instrução for-in

Uma instrução `for`-`in` permite que um bloco de código seja executado
uma vez para cada item de uma coleção (ou de qualquer tipo)
que esteja em conformidade com o protocolo
[`Sequence`](https://developer.apple.com/documentation/swift/sequence).

Uma instrução `for`-`in` tem a seguinte forma:

```swift
for <#item#> in <#collection#> {
   <#statements#>
}
```

O método `makeIterator()` é chamado sobre a expressão de *coleção*
para obter um valor de um tipo iterador, ou seja,
um tipo que está em conformidade com o protocolo
[`IteratorProtocol`](https://developer.apple.com/documentation/swift/iteratorprotocol).
O programa começa a executar o loop
chamando o método `next()` no iterador.
Se o valor retornado não for `nil`,
ele é atribuído ao padrão *item*,
o programa executa as *instruções*
e então continua a execução no início do loop.
Caso contrário, o programa não faz a atribuição nem executa as *instruções*,
e termina a execução da instrução `for`-`in`.

> Gramática de uma instrução for-in:
>
> *for-in-statement* → **`for`** **`case`**_?_ *pattern* **`in`** *expression* *where-clause*_?_ *code-block*

### Instrução while

Uma instrução `while` permite que um bloco de código seja executado repetidamente
enquanto uma condição continuar verdadeira.

Uma instrução `while` tem a seguinte forma:

```swift
while <#condition#> {
   <#statements#>
}
```

Uma instrução `while` é executada da seguinte forma:

1. A *condição* é avaliada.

   Se `true`, a execução continua no passo 2.
   Se `false`, o programa termina a execução da instrução `while`.
2. O programa executa as *instruções*, e a execução volta ao passo 1.

Como o valor da *condição* é avaliado antes de as *instruções* serem executadas,
as *instruções* de uma instrução `while` podem ser executadas zero ou mais vezes.

O valor da *condição*
deve ser do tipo `Bool` ou de um tipo com ponte para `Bool`.
A condição também pode ser uma declaração de optional binding,
como discutido em <doc:TheBasics#Optional-Binding>.

> Gramática de uma instrução while:
>
> *while-statement* → **`while`** *condition-list* *code-block*
>
> *condition-list* → *condition* | *condition* **`,`** *condition-list* \
> *condition* → *expression* | *availability-condition* | *case-condition* | *optional-binding-condition*
>
> *case-condition* → **`case`** *pattern* *initializer* \
> *optional-binding-condition* → **`let`** *pattern* *initializer*_?_ | **`var`** *pattern* *initializer*_?_

### Instrução repeat-while

Uma instrução `repeat`-`while` permite que um bloco de código seja executado uma ou mais vezes
enquanto uma condição continuar verdadeira.

Uma instrução `repeat`-`while` tem a seguinte forma:

```swift
repeat {
   <#statements#>
} while <#condition#>
```

Uma instrução `repeat`-`while` é executada da seguinte forma:

1. O programa executa as *instruções*,
   e a execução continua no passo 2.
2. A *condição* é avaliada.

   Se `true`, a execução volta ao passo 1.
   Se `false`, o programa termina a execução da instrução `repeat`-`while`.

Como o valor da *condição* é avaliado depois de as *instruções* serem executadas,
as *instruções* de uma instrução `repeat`-`while` são executadas pelo menos uma vez.

O valor da *condição*
deve ser do tipo `Bool` ou de um tipo com ponte para `Bool`.

> Gramática de uma instrução repeat-while:
>
> *repeat-while-statement* → **`repeat`** *code-block* **`while`** *expression*

## Instruções de desvio

Instruções de desvio permitem que o programa execute determinadas partes do código
dependendo do valor de uma ou mais condições.
Os valores das condições especificadas em uma instrução de desvio
controlam como o programa se desvia e, portanto, qual bloco de código é executado.
Swift tem três instruções de desvio:
uma instrução `if`, uma instrução `guard` e uma instrução `switch`.

O fluxo de controle em uma instrução `if` ou em uma instrução `switch` pode ser alterado por uma instrução `break`
e é discutido em <doc:Statements#Break-Statement> abaixo.

> Gramática de uma instrução de desvio:
>
> *branch-statement* → *if-statement* \
> *branch-statement* → *guard-statement* \
> *branch-statement* → *switch-statement*

### Instrução if

Uma instrução `if` é usada para executar código
com base na avaliação de uma ou mais condições.

Há duas formas básicas de instrução `if`.
Em ambas, as chaves de abertura e de fechamento são obrigatórias.

A primeira forma permite que o código seja executado somente quando uma condição é verdadeira
e tem a seguinte forma:

```swift
if <#condition#> {
   <#statements#>
}
```

A segunda forma da instrução `if` oferece uma cláusula *else* adicional
(introduzida pela palavra-chave `else`)
e é usada para executar uma parte do código quando a condição é verdadeira
e outra parte quando a mesma condição é falsa.
Quando há uma única cláusula else, a instrução `if` tem a seguinte forma:

```swift
if <#condition#> {
   <#statements to execute if condition is true#>
} else {
   <#statements to execute if condition is false#>
}
```

A cláusula else de uma instrução `if` pode conter outra instrução `if`
para testar mais de uma condição.
Uma instrução `if` encadeada dessa forma tem a seguinte forma:

```swift
if <#condition 1#> {
   <#statements to execute if condition 1 is true#>
} else if <#condition 2#> {
   <#statements to execute if condition 2 is true#>
} else {
   <#statements to execute if both conditions are false#>
}
```

O valor de qualquer condição em uma instrução `if`
deve ser do tipo `Bool` ou de um tipo com ponte para `Bool`.
A condição também pode ser uma declaração de optional binding,
como discutido em <doc:TheBasics#Optional-Binding>.

> Gramática de uma instrução if:
>
> *if-statement* → **`if`** *condition-list* *code-block* *else-clause*_?_ \
> *else-clause* → **`else`** *code-block* | **`else`** *if-statement*

### Instrução guard

Uma instrução `guard` é usada para transferir o controle do programa para fora de um escopo
quando uma ou mais condições não são atendidas.

Uma instrução `guard` tem a seguinte forma:

```swift
guard <#condition#> else {
   <#statements#>
}
```

O valor de qualquer condição em uma instrução `guard`
deve ser do tipo `Bool` ou de um tipo com ponte para `Bool`.
A condição também pode ser uma declaração de optional binding,
como discutido em <doc:TheBasics#Optional-Binding>.

Quaisquer constantes ou variáveis que recebam um valor
de uma declaração de optional binding na condição de uma instrução `guard`
podem ser usadas pelo restante do escopo que contém a instrução guard.

A cláusula `else` de uma instrução `guard` é obrigatória
e deve chamar uma função com tipo de retorno `Never`
ou transferir o controle do programa para fora do escopo que contém a instrução guard
usando uma das seguintes instruções:

- `return`
- `break`
- `continue`
- `throw`

As instruções de transferência de controle são discutidas em <doc:Statements#Control-Transfer-Statements> abaixo.
Para mais informações sobre funções com tipo de retorno `Never`,
veja <doc:Declarations#Functions-that-Never-Return>.

> Gramática de uma instrução guard:
>
> *guard-statement* → **`guard`** *condition-list* **`else`** *code-block*

### Instrução switch

Uma instrução `switch` permite que determinados blocos de código sejam executados
dependendo do valor de uma expressão de controle.

Uma instrução `switch` tem a seguinte forma:

```swift
switch <#control expression#> {
case <#pattern 1#>:
    <#statements#>
case <#pattern 2#> where <#condition#>:
    <#statements#>
case <#pattern 3#> where <#condition#>,
    <#pattern 4#> where <#condition#>:
    <#statements#>
default:
    <#statements#>
}
```

A *expressão de controle* da instrução `switch` é avaliada
e depois comparada com os padrões especificados em cada caso.
Se uma correspondência for encontrada,
o programa executa as *instruções* listadas dentro do escopo desse caso.
O escopo de cada caso não pode estar vazio.
Por isso, você precisa incluir pelo menos uma instrução
depois do dois-pontos (`:`) de cada rótulo de caso. Use uma única instrução `break`
se não pretende executar nenhum código no corpo de um caso correspondido.

Os valores das expressões em que seu código pode desviar são muito flexíveis. Por exemplo,
além dos valores de tipos escalares, como inteiros e caracteres,
seu código pode desviar com base nos valores de qualquer tipo, incluindo números de ponto flutuante, strings,
tuplas, instâncias de classes personalizadas e optionals.
O valor da *expressão de controle* pode até ser comparado com o valor de um caso de uma enumeração
e verificado quanto à inclusão em um intervalo especificado de valores.
Para exemplos de como usar esses vários tipos de valores em instruções `switch`,
veja <doc:ControlFlow#Switch> em <doc:ControlFlow>.

Um caso de `switch` pode, opcionalmente, conter uma cláusula `where` depois de cada padrão.
Uma *cláusula where* é introduzida pela palavra-chave `where`, seguida de uma expressão,
e é usada para fornecer uma condição adicional
antes de um padrão de um caso ser considerado correspondente à *expressão de controle*.
Se houver uma cláusula `where`, as *instruções* do caso relevante
são executadas somente se o valor da *expressão de controle*
corresponder a um dos padrões do caso e a expressão da cláusula `where` for avaliada como `true`.
Por exemplo, uma *expressão de controle* corresponde ao caso do exemplo abaixo
somente se for uma tupla com dois elementos de mesmo valor, como `(1, 1)`.

```swift
case let (x, y) where x == y:
```

<!--
  - test: `switch-case-statement`

  ```swifttest
  >> switch (1, 1) {
  -> case let (x, y) where x == y:
  >> break
  >> default: break
  >> }
  ```
-->

Como o exemplo acima mostra, padrões em um caso também podem vincular constantes
usando a palavra-chave `let` (também podem vincular variáveis usando a palavra-chave `var`).
Essas constantes (ou variáveis) podem então ser referenciadas em uma cláusula `where` correspondente
e em todo o restante do código dentro do escopo do caso.
Se o caso contiver vários padrões que correspondem à expressão de controle,
todos os padrões devem conter as mesmas vinculações de constantes ou variáveis,
e cada constante ou variável vinculada deve ter o mesmo tipo
em todos os padrões do caso.

<!--
  The discussion above about multi-pattern cases
  matches discussion of multi-pattern catch under Do Statement.
-->

Uma instrução `switch` também pode incluir um caso default, introduzido pela palavra-chave `default`.
O código dentro de um caso default é executado somente se nenhum outro caso corresponder à expressão de controle.
Uma instrução `switch` pode incluir apenas um caso default,
que deve aparecer no fim da instrução `switch`.

Embora a ordem real de execução das operações de correspondência de padrões,
e em particular a ordem de avaliação dos padrões nos casos, não seja especificada,
a correspondência de padrões em uma instrução `switch` se comporta
como se a avaliação fosse feita na ordem do código-fonte, ou seja,
na ordem em que aparecem no código-fonte.
Por isso, se vários casos contiverem padrões que resultam no mesmo valor
e, assim, puderem corresponder ao valor da expressão de controle,
o programa executa somente o código do primeiro caso correspondente na ordem do código-fonte.

<!--
  - test: `switch-case-with-multiple-patterns`

  ```swifttest
  >> let tuple = (1, 1)
  >> switch tuple {
  >>     case (let x, 5), (let x, 1): print(x)
  >>     default: print(2)
  >> }
  << 1
  ```
-->

<!--
  - test: `switch-case-with-multiple-patterns-err`

  ```swifttest
  >> let tuple = (1, 1)
  >> switch tuple {
  >>     case (let x, 5), (let x as Any, 1): print(1)
  >>     default: print(2)
  >> }
  !$ error: pattern variable bound to type 'Any', expected type 'Int'
  !! case (let x, 5), (let x as Any, 1): print(1)
  !!                       ^
  ```
-->

#### Instruções switch devem ser exaustivas

Em Swift,
todo valor possível do tipo da expressão de controle
deve corresponder ao valor de pelo menos um padrão de um caso.
Quando isso simplesmente não é viável
(por exemplo, quando o tipo da expressão de controle é `Int`),
você pode incluir um caso default para atender a esse requisito.

#### Alternando sobre casos futuros de enumeração

Uma *enumeração não congelada* é um tipo especial de enumeração
que pode ganhar novos casos no futuro, mesmo depois de você compilar e distribuir um app.
Alternar sobre uma enumeração não congelada exige atenção extra.
Quando os autores de uma biblioteca marcam uma enumeração como não congelada,
eles se reservam o direito de adicionar novos casos,
e qualquer código que interaja com essa enumeração
*precisa* conseguir tratar esses casos futuros sem ser recompilado.
Código compilado no modo de evolução de biblioteca,
código da biblioteca padrão do Swift,
overlays Swift para frameworks da Apple,
e código C e Objective-C podem declarar enumerações não congeladas.
Para informações sobre enumerações congeladas e não congeladas,
veja <doc:Attributes#frozen>.

Ao alternar sobre um valor de enumeração não congelada,
você sempre precisa incluir um caso default,
mesmo que todos os casos da enumeração já tenham um caso switch correspondente.
Você pode aplicar o atributo `@unknown` ao caso default,
o que indica que o caso default deve corresponder somente a casos de enumeração
adicionados no futuro.
O Swift emite um aviso
se o caso default corresponder
a qualquer caso de enumeração conhecido em tempo de compilação.
Esse aviso futuro informa que o autor da biblioteca
adicionou um novo caso à enumeração
que não tem um caso switch correspondente.

O exemplo a seguir alterna sobre os três casos existentes da
enumeração da biblioteca padrão do Swift
[`Mirror.AncestorRepresentation`](https://developer.apple.com/documentation/swift/mirror/ancestorrepresentation).
Se você adicionar casos no futuro,
o compilador gera um aviso para indicar
que você precisa atualizar a instrução switch
para levar os novos casos em consideração.

```swift
let representation: Mirror.AncestorRepresentation = .generated
switch representation {
case .customized:
    print("Use the nearest ancestor’s implementation.")
case .generated:
    print("Generate a default mirror for all ancestor classes.")
case .suppressed:
    print("Suppress the representation of all ancestor classes.")
@unknown default:
    print("Use a representation that was unknown when this code was compiled.")
}
// Prints "Generate a default mirror for all ancestor classes."
```

<!--
  - test: `unknown-case`

  ```swifttest
  -> let representation: Mirror.AncestorRepresentation = .generated
  -> switch representation {
     case .customized:
         print("Use the nearest ancestor’s implementation.")
     case .generated:
         print("Generate a default mirror for all ancestor classes.")
     case .suppressed:
         print("Suppress the representation of all ancestor classes.")
  -> @unknown default:
         print("Use a representation that was unknown when this code was compiled.")
     }
  <- Generate a default mirror for all ancestor classes.
  ```
-->

#### A execução não passa de um caso para o outro implicitamente

Depois que o código de um caso correspondido termina de ser executado,
o programa sai da instrução `switch`.
A execução do programa não continua nem "passa" para o próximo caso ou para o caso default.
Dito isso, se você quiser que a execução continue de um caso para o seguinte,
inclua explicitamente uma instrução `fallthrough`,
que consiste simplesmente na palavra-chave `fallthrough`,
no caso a partir do qual você quer que a execução continue.
Para mais informações sobre a instrução `fallthrough`,
veja <doc:Statements#Fallthrough-Statement> abaixo.

> Gramática de uma instrução switch:
>
> *switch-statement* → **`switch`** *expression* **`{`** *switch-cases*_?_ **`}`** \
> *switch-cases* → *switch-case* *switch-cases*_?_ \
> *switch-case* → *case-label* *statements* \
> *switch-case* → *default-label* *statements* \
> *switch-case* → *conditional-switch-case*
>
> *case-label* → *attributes*_?_ **`case`** *case-item-list* **`:`** \
> *case-item-list* → *pattern* *where-clause*_?_ | *pattern* *where-clause*_?_ **`,`** *case-item-list* \
> *default-label* → *attributes*_?_ **`default`** **`:`**
>
> *where-clause* → **`where`** *where-expression* \
> *where-expression* → *expression*
>
> *conditional-switch-case* → *switch-if-directive-clause* *switch-elseif-directive-clauses*_?_ *switch-else-directive-clause*_?_ *endif-directive* \
> *switch-if-directive-clause* → *if-directive* *compilation-condition* *switch-cases*_?_ \
> *switch-elseif-directive-clauses* → *elseif-directive-clause* *switch-elseif-directive-clauses*_?_ \
> *switch-elseif-directive-clause* → *elseif-directive* *compilation-condition* *switch-cases*_?_ \
> *switch-else-directive-clause* → *else-directive* *switch-cases*_?_

<!--
  The grammar above uses attributes-OPT to match what's used
  in all other places where attributes are allowed,
  although as of Swift 4.2 only a single attribute (@unknown) is allowed.
-->

## Instrução rotulada

Você pode prefixar uma instrução de loop, uma instrução `if`, uma instrução `switch`
ou uma instrução `do` com um *rótulo de instrução*,
que consiste no nome do rótulo seguido imediatamente de dois-pontos (:).
Use rótulos de instrução com instruções `break` e `continue` para deixar explícito
como você quer alterar o fluxo de controle em uma instrução de loop ou em uma instrução `switch`,
como discutido em <doc:Statements#Break-Statement> e
<doc:Statements#Continue-Statement> abaixo.

O escopo de uma instrução rotulada é toda a instrução que segue o rótulo.
Você pode aninhar instruções rotuladas, mas o nome de cada rótulo de instrução deve ser único.

Para mais informações e para ver exemplos
de como usar rótulos de instrução,
veja <doc:ControlFlow#Labeled-Statements> em <doc:ControlFlow>.

<!--
  - test: `backtick-identifier-is-legal-label`

  ```swifttest
  -> var i = 0
  -> `return`: while i < 100 {
         i += 1
         if i == 10 {
             break `return`
         }
     }
  -> print(i)
  << 10
  ```
-->

> Gramática de uma instrução rotulada:
>
> *labeled-statement* → *statement-label* *loop-statement* \
> *labeled-statement* → *statement-label* *if-statement* \
> *labeled-statement* → *statement-label* *switch-statement* \
> *labeled-statement* → *statement-label* *do-statement*
>
> *statement-label* → *label-name* **`:`** \
> *label-name* → *identifier*

## Instruções de transferência de controle

Instruções de transferência de controle podem alterar a ordem em que o código do programa é executado,
transferindo incondicionalmente o controle do programa de um trecho de código para outro.
Swift tem cinco instruções de transferência de controle: uma instrução `break`, uma instrução `continue`,
uma instrução `fallthrough`, uma instrução `return` e uma instrução `throw`.

> Gramática de uma instrução de transferência de controle:
>
> *control-transfer-statement* → *break-statement* \
> *control-transfer-statement* → *continue-statement* \
> *control-transfer-statement* → *fallthrough-statement* \
> *control-transfer-statement* → *return-statement* \
> *control-transfer-statement* → *throw-statement*

### Instrução break

Uma instrução `break` encerra a execução de um loop,
de uma instrução `if` ou de uma instrução `switch`.
Uma instrução `break` pode consistir apenas na palavra-chave `break`,
ou pode consistir na palavra-chave `break` seguida do nome de um rótulo de instrução,
como mostrado abaixo.

```swift
break
break <#label name#>
```

Quando uma instrução `break` é seguida do nome de um rótulo de instrução,
ela encerra a execução do loop,
da instrução `if` ou da instrução `switch` identificada por esse rótulo.

Quando uma instrução `break` não é seguida do nome de um rótulo de instrução,
ela encerra a execução da instrução `switch` ou do loop mais interno
no qual ela ocorre.
Você não pode usar uma instrução `break` sem rótulo para sair de uma instrução `if`.

Nos dois casos, o controle do programa é então transferido para a primeira linha
de código depois do loop ou da instrução `switch` que a contém, se houver.

Para exemplos de como usar uma instrução `break`,
veja <doc:ControlFlow#Break> e <doc:ControlFlow#Labeled-Statements>
em <doc:ControlFlow>.

> Gramática de uma instrução break:
>
> *break-statement* → **`break`** *label-name*_?_

### Instrução continue

Uma instrução `continue` encerra a execução da iteração atual de uma instrução de loop,
mas não interrompe a execução da instrução de loop.
Uma instrução `continue` pode consistir apenas na palavra-chave `continue`,
ou pode consistir na palavra-chave `continue` seguida do nome de um rótulo de instrução,
como mostrado abaixo.

```swift
continue
continue <#label name#>
```

Quando uma instrução `continue` é seguida do nome de um rótulo de instrução,
ela encerra a execução da iteração atual
da instrução de loop identificada por esse rótulo.

Quando uma instrução `continue` não é seguida do nome de um rótulo de instrução,
ela encerra a execução da iteração atual
do loop mais interno no qual ela ocorre.

Nos dois casos, o controle do programa é então transferido para a condição
da instrução de loop que a contém.

Em uma instrução `for`,
a expressão de incremento ainda é avaliada depois que a instrução `continue` é executada,
porque a expressão de incremento é avaliada depois da execução do corpo do loop.

Para exemplos de como usar uma instrução `continue`,
veja <doc:ControlFlow#Continue> e <doc:ControlFlow#Labeled-Statements>
em <doc:ControlFlow>.

> Gramática de uma instrução continue:
>
> *continue-statement* → **`continue`** *label-name*_?_

### Instrução fallthrough

Uma instrução `fallthrough` consiste na palavra-chave `fallthrough`
e ocorre somente em um bloco de caso de uma instrução `switch`.
Uma instrução `fallthrough` faz a execução do programa continuar
de um caso de uma instrução `switch` para o próximo caso.
A execução continua para o próximo caso
mesmo que os padrões do rótulo de caso não correspondam
ao valor da expressão de controle da instrução `switch`.

Uma instrução `fallthrough` pode aparecer em qualquer lugar dentro de uma instrução `switch`,
não apenas como última instrução de um bloco de caso,
mas não pode ser usada no último bloco de caso.
Ela também não pode transferir o controle para um bloco de caso
cujo padrão contenha padrões de vinculação de valor.

Para um exemplo de como usar uma instrução `fallthrough` em uma instrução `switch`,
veja <doc:ControlFlow#Control-Transfer-Statements>
em <doc:ControlFlow>.

> Gramática de uma instrução fallthrough:
>
> *fallthrough-statement* → **`fallthrough`**

### Instrução return

Uma instrução `return` ocorre no corpo de uma definição de função ou método
e faz a execução do programa retornar para a função ou o método que a chamou.
A execução do programa continua no ponto imediatamente seguinte à chamada da função ou do método.

Uma instrução `return` pode consistir apenas na palavra-chave `return`,
ou pode consistir na palavra-chave `return` seguida de uma expressão, como mostrado abaixo.

```swift
return
return <#expression#>
```

Quando uma instrução `return` é seguida de uma expressão,
o valor da expressão é retornado para a função ou o método que a chamou.
Se o valor da expressão não corresponder ao valor do tipo de retorno
declarado na declaração da função ou do método,
o valor da expressão é convertido para o tipo de retorno
antes de ser retornado para a função ou o método que a chamou.

> Nota: Como descrito em <doc:Declarations#Failable-Initializers>, uma forma especial da instrução `return` (`return nil`)
> pode ser usada em um inicializador falível para indicar falha na inicialização.

<!--
  TODO: Discuss how the conversion takes place and what is allowed to be converted
  in the (yet to be written) chapter on subtyping and type conversions.
-->

Quando uma instrução `return` não é seguida de uma expressão,
ela só pode ser usada para retornar de uma função ou método que não define tipo de retorno
(ou seja, quando o tipo de retorno da função ou do método é `Void` ou `()`).

> Gramática de uma instrução return:
>
> *return-statement* → **`return`** *expression*_?_

### Instrução throw

Uma instrução `throw` ocorre no corpo de uma função ou método que lança erros,
ou no corpo de uma expressão de closure cujo tipo está marcado com a palavra-chave `throws`.

Uma instrução `throw` faz o programa encerrar a execução do escopo atual
e começar a propagação do erro para o escopo que o contém.
O erro lançado continua se propagando até ser tratado por uma cláusula `catch`
de uma instrução `do`.

Uma instrução `throw` consiste na palavra-chave `throw`
seguida de uma expressão, como mostrado abaixo.

```swift
throw <#expression#>
```

O valor da *expressão* deve ter um tipo que esteja em conformidade com
o protocolo `Error`.
Se a instrução `do` ou a função que contém a instrução `throw`
declarar o tipo de erros que lança,
o valor da *expressão* deve ser uma instância desse tipo.

Para um exemplo de como usar uma instrução `throw`,
veja <doc:ErrorHandling#Propagating-Errors-Using-Throwing-Functions>
em <doc:ErrorHandling>.

> Gramática de uma instrução throw:
>
> *throw-statement* → **`throw`** *expression*

## Instrução defer

Uma instrução `defer` é usada para executar código
logo antes de transferir o controle do programa para fora do escopo
no qual a instrução `defer` aparece.

Uma instrução `defer` tem a seguinte forma:

```swift
defer {
    <#statements#>
}
```

As instruções dentro da instrução `defer` são executadas
independentemente de como o controle do programa é transferido.
Isso significa que uma instrução `defer` pode ser usada, por exemplo,
para fazer gerenciamento manual de recursos, como fechar descritores de arquivo,
e para executar ações que precisam acontecer mesmo quando um erro é lançado.

As *instruções* da instrução `defer`
são executadas no fim do escopo que contém a instrução `defer`.

```swift
func f(x: Int) {
  defer { print("First defer") }

  if x < 10 {
    defer { print("Second defer") }
    print("End of if")
  }

  print("End of function")
}
f(x: 5)
// Prints "End of if".
// Prints "Second defer".
// Prints "End of function".
// Prints "First defer".
```

<!--
  ```swifttest
  -> func f(x: Int) {
    defer { print("First defer") }

    if x < 10 {
      defer { print("Second defer") }
      print("End of if")
    }

    print("End of function")
  }
  f(x: 5)
  <- End of if
  <- Second defer
  <- End of function
  <- First defer
  ```
-->

No código acima,
o `defer` dentro da instrução `if`
é executado antes do `defer` declarado na função `f`,
porque o escopo da instrução `if` termina
antes do escopo da função.

Se várias instruções `defer` aparecerem no mesmo escopo,
a ordem em que aparecem é o inverso da ordem em que são executadas.
Executar primeiro a última instrução `defer` de um escopo
significa que as instruções dentro dessa última instrução `defer`
podem se referir a recursos que serão limpos por outras instruções `defer`.

```swift
func f() {
    defer { print("First defer") }
    defer { print("Second defer") }
    print("End of function")
}
f()
// Prints "End of function".
// Prints "Second defer".
// Prints "First defer".
```

<!--
  ```swifttest
  -> func f() {
         defer { print("First defer") }
         defer { print("Second defer") }
         print("End of function")
     }
     f()
  <- End of function
  <- Second defer
  <- First defer
  ```
-->

As instruções dentro da instrução `defer` não podem
transferir o controle do programa para fora da instrução `defer`.

> Gramática de uma instrução defer:
>
> *defer-statement* → **`defer`** *code-block*

## Instrução do

A instrução `do` é usada para introduzir um novo escopo
e pode, opcionalmente, conter uma ou mais cláusulas `catch`,
que contêm padrões que correspondem a condições de erro definidas.
Variáveis e constantes declaradas no escopo de uma instrução `do`
só podem ser acessadas dentro desse escopo.

Uma instrução `do` em Swift é semelhante às chaves (`{}`) do C usadas para delimitar um bloco de código,
e não tem custo de desempenho em tempo de execução.

Uma instrução `do` tem a seguinte forma:

```swift
do {
    try <#expression#>
    <#statements#>
} catch <#pattern 1#> {
    <#statements#>
} catch <#pattern 2#> where <#condition#> {
    <#statements#>
} catch <#pattern 3#>, <#pattern 4#> where <#condition#> {
    <#statements#>
} catch {
    <#statements#>
}
```

Uma instrução `do` pode, opcionalmente, especificar o tipo de erro que lança,
o que tem a seguinte forma:

```swift
do throws(<#type#>) {
    try <#expression#>
} catch <#pattern> {
    <#statements#>
} catch {
    <#statements#>
}
```

Se a instrução `do` incluir uma cláusula `throws`,
o bloco `do` só pode lançar erros do *tipo* especificado.
O *tipo* deve ser
um tipo concreto que esteja em conformidade com o protocolo `Error`,
um tipo opaco que esteja em conformidade com o protocolo `Error`,
ou o tipo de protocolo encaixotado `any Error`.
Se a instrução `do` não especificar o tipo de erro que lança,
o Swift infere o tipo de erro da seguinte forma:

- Se toda instrução `throw` e toda expressão `try` no bloco de código `do`
  estiver aninhada dentro de um mecanismo exaustivo de tratamento de erros,
  então o Swift infere que a instrução `do` não lança erros.

- Se o bloco de código `do` contiver código que lança
  erros de apenas um único tipo
  fora de um tratamento de erros exaustivo,
  diferente de lançar `Never`,
  então o Swift infere que a instrução `do` lança esse tipo concreto de erro.

- Se o bloco de código `do` contiver código que lança
  erros de mais de um tipo
  fora de um tratamento de erros exaustivo,
  então o Swift infere que a instrução `do` lança `any Error`.

Para mais informações sobre como trabalhar com erros que têm tipos explícitos,
veja <doc:ErrorHandling#Specifying-the-Error-Type>.

Se qualquer instrução no bloco de código `do` lançar um erro,
o controle do programa é transferido
para a primeira cláusula `catch` cujo padrão corresponda ao erro.
Se nenhuma das cláusulas corresponder,
o erro se propaga para o escopo que o contém.
Se um erro não tratado chegar ao nível superior,
a execução do programa para com um erro em tempo de execução.

Assim como uma instrução `switch`,
o compilador tenta inferir se as cláusulas `catch` são exaustivas.
Se for possível determinar isso, o erro é considerado tratado.
Caso contrário, o erro pode se propagar para fora do escopo que o contém,
o que significa que
o erro precisa ser tratado por uma cláusula `catch` que o envolva
ou a função que o contém precisa ser declarada com `throws`.

Uma cláusula `catch` que tem vários padrões
corresponde ao erro se qualquer um dos seus padrões corresponder ao erro.
Se uma cláusula `catch` contiver vários padrões,
todos os padrões devem conter as mesmas vinculações de constantes ou variáveis,
e cada constante ou variável vinculada deve ter o mesmo tipo
em todos os padrões da cláusula `catch`.

<!--
  The discussion above of multi-pattern catch
  matches the discussion of multi-pattern case under Switch Statement.
-->

Para garantir que um erro seja tratado,
use uma cláusula `catch` com um padrão que corresponda a todos os erros,
como o padrão curinga (`_`).
Se uma cláusula `catch` não especificar um padrão,
ela corresponde a qualquer erro e o vincula a uma constante local chamada `error`.
Para mais informações sobre os padrões que você pode usar em uma cláusula `catch`,
veja <doc:Patterns>.

Para ver um exemplo de como usar uma instrução `do` com várias cláusulas `catch`,
veja <doc:ErrorHandling#Handling-Errors>.

> Gramática de uma instrução do:
>
> *do-statement* → **`do`** *throws-clause*_?_ *code-block* *catch-clauses*_?_ \
> *catch-clauses* → *catch-clause* *catch-clauses*_?_ \
> *catch-clause* → **`catch`** *catch-pattern-list*_?_ *code-block* \
> *catch-pattern-list* → *catch-pattern* | *catch-pattern* **`,`** *catch-pattern-list* \
> *catch-pattern* → *pattern* *where-clause*_?_

## Instruções de controle do compilador

Instruções de controle do compilador permitem que o programa altere aspectos do comportamento do compilador.
Swift tem três instruções de controle do compilador:
um bloco de compilação condicional,
uma instrução de controle de linha
e uma instrução de diagnóstico em tempo de compilação.

> Gramática de uma instrução de controle do compilador:
>
> *compiler-control-statement* → *conditional-compilation-block* \
> *compiler-control-statement* → *line-control-statement* \
> *compiler-control-statement* → *diagnostic-statement*

### Bloco de compilação condicional

Um bloco de compilação condicional permite que o código seja compilado condicionalmente
dependendo do valor de uma ou mais condições de compilação.

Todo bloco de compilação condicional começa com a diretiva de compilação `#if`
e termina com a diretiva de compilação `#endif`.
Um bloco de compilação condicional simples tem a seguinte forma:

```swift
#if <#compilation condition#>
    <#statements#>
#endif
```

Diferente da condição de uma instrução `if`,
a *condição de compilação* é avaliada em tempo de compilação.
Por isso, as *instruções* são compiladas e executadas somente se a *condição de compilação*
for avaliada como `true` em tempo de compilação.

A *condição de compilação* pode incluir os literais booleanos `true` e `false`,
um identificador usado com o flag de linha de comando `-D`, ou qualquer uma das condições de plataforma
listadas na tabela abaixo.

| Condição de plataforma | Argumentos válidos |
| ------------------ | --------------- |
| `os()` | `macOS`, `iOS`, `watchOS`, `tvOS`, `visionOS`, `Linux`, `Windows` |
| `arch()` | `arm`, `arm64`, `i386`, `wasm32`, `x86_64`, |
| `swift()` | `>=` ou `<` seguido de um número de versão |
| `compiler()` | `>=` ou `<` seguido de um número de versão |
| `canImport()` | Um nome de módulo |
| `targetEnvironment()` | `simulator`, `macCatalyst` |

<!--
  The lists above match <https://www.swift.org/platform-support/>
  and include only platforms with *official* support.
  For the full list of operating systems and architectures,
  including those with unofficial or experimental support,
  see the values of
  SupportedConditionalCompilationOSs and SupportedConditionalCompilationArches
  in the file lib/Basic/LangOptions.cpp.
  The compiler also accepts pretty much any string --
  for example "#if os(toaster)" compiles just fine,
  but Swift doesn't actually support running on a toaster oven --
  so don't rely on that when checking possible os/arch values.
-->

<!--
  The target environment "UIKitForMac"
  is understood by the compiler as a synonym for "macCatalyst",
  but that spelling is marked "Must be removed" outside of a few places,
  so it's omitted from the table above.
-->

O número de versão das condições de plataforma `swift()` e `compiler()`
consiste em um número principal, um número secundário opcional, um número de correção opcional e assim por diante,
com um ponto (`.`) separando cada parte do número de versão.
Não pode haver espaço em branco entre o operador de comparação e o número de versão.
A versão de `compiler()` é a versão do compilador,
independentemente da versão da linguagem passada como configuração ao compilador.
A versão de `swift()` é a versão da linguagem que está sendo compilada.
Por exemplo, se você compilar seu código usando o compilador do Swift 5 no modo Swift 4.2,
a versão do compilador é 5 e a versão da linguagem é 4.2.
Com essas configurações,
o código a seguir imprime as três mensagens:

```swift
#if compiler(>=5)
print("Compiled with the Swift 5 compiler or later")
#endif
#if swift(>=4.2)
print("Compiled in Swift 4.2 mode or later")
#endif
#if compiler(>=5) && swift(<5)
print("Compiled with the Swift 5 compiler or later in a Swift mode earlier than 5")
#endif
// Prints "Compiled with the Swift 5 compiler or later".
// Prints "Compiled in Swift 4.2 mode or later".
// Prints "Compiled with the Swift 5 compiler or later in a Swift mode earlier than 5".
```

<!--
  ```swifttest
  -> #if compiler(>=5)
     print("Compiled with the Swift 5 compiler or later")
     #endif
     #if swift(>=4.2)
     print("Compiled in Swift 4.2 mode or later")
     #endif
     #if compiler(>=5) && swift(<5)
     print("Compiled with the Swift 5 compiler or later in a Swift mode earlier than 5")
     #endif
  <- Compiled with the Swift 5 compiler or later
  <- Compiled in Swift 4.2 mode or later
  // Prints "Compiled with the Swift 5 compiler or later in a Swift mode earlier than 5".
  ```
-->

<!--
  That testcode is cheating by explicitly printing the third line of output,
  since it's not actually running in Swift 4.2 mode.
-->

O argumento da condição de plataforma `canImport()`
é o nome de um módulo que pode não estar presente em todas as plataformas.
O módulo pode incluir pontos (`.`) no nome.
Essa condição verifica se é possível importar o módulo,
mas não o importa de fato.
Se o módulo estiver presente, a condição de plataforma retorna `true`;
caso contrário, retorna `false`.

<!--
  - test: `canImport_A, canImport`

  ```swifttest
  >> public struct SomeStruct {
  >>     public init() { }
  >> }
  ```
-->

<!--
  - test: `canImport_A.B, canImport`

  ```swifttest
  >> public struct AnotherStruct {
  >>     public init() { }
  >> }
  ```
-->

<!--
  - test: `canImport`

  ```swifttest
  >> import canImport_A
  >> let s = SomeStruct()
  >> #if canImport(canImport_A)
  >> #else
  >> #error("Can't import A")
  >> #endif

  >> #if canImport(canImport_A.B)
  >> #else
  >> #error("Can't import A.B")
  >> #endif
  ```
-->

A condição de plataforma `targetEnvironment()`
retorna `true` quando o código está sendo compilado para o ambiente especificado;
caso contrário, retorna `false`.

> Nota: A condição de plataforma `arch(arm)` não retorna `true` para dispositivos ARM de 64 bits.
> A condição de plataforma `arch(i386)` retorna `true`
> quando o código é compilado para o simulador do iOS de 32 bits.

<!--
  - test: `pound-if-swift-version`

  ```swifttest
  -> #if swift(>=2.1)
         print(1)
     #endif
  << 1
  -> #if swift(>=2.1) && true
         print(2)
     #endif
  << 2
  -> #if swift(>=2.1) && false
         print(3)
     #endif
  -> #if swift(>=2.1.9.9.9.9.9.9.9.9.9)
         print(5)
     #endif
  << 5
  ```
-->

<!--
  - test: `pound-if-swift-version-err`

  ```swifttest
  -> #if swift(>= 2.1)
         print(4)
     #endif
  !$ error: unary operator cannot be separated from its operand
  !! #if swift(>= 2.1)
  !!           ^ ~
  !!-
  ```
-->

<!--
  - test: `pound-if-compiler-version`

  ```swifttest
  -> #if compiler(>=4.2)
         print(1)
     #endif
  << 1
  -> #if compiler(>=4.2) && true
         print(2)
     #endif
  << 2
  -> #if compiler(>=4.2) && false
         print(3)
     #endif
  ```
-->

Você pode combinar e negar condições de compilação usando os operadores lógicos
`&&`, `||` e `!`, e usar parênteses para agrupar.
Esses operadores têm a mesma associatividade e precedência dos
operadores lógicos usados para combinar expressões booleanas comuns.

Assim como em uma instrução `if`,
você pode adicionar vários ramos condicionais para testar condições de compilação diferentes.
Você pode adicionar quantos ramos extras quiser usando cláusulas `#elseif`.
Você também pode adicionar um último ramo usando uma cláusula `#else`.
Blocos de compilação condicional com vários ramos
têm a seguinte forma:

```swift
#if <#compilation condition 1#>
    <#statements to compile if compilation condition 1 is true#>
#elseif <#compilation condition 2#>
    <#statements to compile if compilation condition 2 is true#>
#else
    <#statements to compile if both compilation conditions are false#>
#endif
```

> Nota: Cada instrução no corpo de um bloco de compilação condicional é analisada
> mesmo que não seja compilada.
> Há uma exceção se a condição de compilação incluir uma condição de plataforma `swift()` ou `compiler()`:
> as instruções são analisadas
> somente se a versão da linguagem ou do compilador corresponder
> ao que está especificado na condição de plataforma.
> Essa exceção garante que um compilador mais antigo não tente analisar
> a sintaxe introduzida em uma versão mais nova do Swift.

Para informações sobre como você pode envolver
expressões de membro explícitas em blocos de compilação condicional,
veja <doc:Expressions#Explicit-Member-Expression>.

> Gramática de um bloco de compilação condicional:
>
> *conditional-compilation-block* → *if-directive-clause* *elseif-directive-clauses*_?_ *else-directive-clause*_?_ *endif-directive*
>
> *if-directive-clause* → *if-directive* *compilation-condition* *statements*_?_ \
> *elseif-directive-clauses* → *elseif-directive-clause* *elseif-directive-clauses*_?_ \
> *elseif-directive-clause* → *elseif-directive* *compilation-condition* *statements*_?_ \
> *else-directive-clause* → *else-directive* *statements*_?_ \
> *if-directive* → **`#if`** \
> *elseif-directive* → **`#elseif`** \
> *else-directive* → **`#else`** \
> *endif-directive* → **`#endif`**
>
> *compilation-condition* → *platform-condition* \
> *compilation-condition* → *identifier* \
> *compilation-condition* → *boolean-literal* \
> *compilation-condition* → **`(`** *compilation-condition* **`)`** \
> *compilation-condition* → **`!`** *compilation-condition* \
> *compilation-condition* → *compilation-condition* **`&&`** *compilation-condition* \
> *compilation-condition* → *compilation-condition* **`||`** *compilation-condition*
>
> *platform-condition* → **`os`** **`(`** *operating-system* **`)`** \
> *platform-condition* → **`arch`** **`(`** *architecture* **`)`** \
> *platform-condition* → **`swift`** **`(`** **`>=`** *swift-version* **`)`** | **`swift`** **`(`** **`<`** *swift-version* **`)`** \
> *platform-condition* → **`compiler`** **`(`** **`>=`** *swift-version* **`)`** | **`compiler`** **`(`** **`<`** *swift-version* **`)`** \
> *platform-condition* → **`canImport`** **`(`** *import-path* **`)`** \
> *platform-condition* → **`targetEnvironment`** **`(`** *environment* **`)`**
>
> *operating-system* → **`macOS`** | **`iOS`** | **`watchOS`** | **`tvOS`** | **`visionOS`** | **`Linux`** | **`Windows`** \
> *architecture* → **`arm`** | **`arm64`** | **`i386`** | **`wasm32`** | **`x86_64`** \
> *swift-version* → *decimal-digits* *swift-version-continuation*_?_ \
> *swift-version-continuation* → **`.`** *decimal-digits* *swift-version-continuation*_?_ \
> *environment* → **`simulator`** | **`macCatalyst`**

<!--
  Testing notes:

  !!true doesn't work but !(!true) does -- this matches normal expressions
  #if can be nested, as expected

  Also, the body of a conditional compilation block contains *zero* or more statements.
  Thus, this is allowed:
      #if
      #elseif
      #else
      #endif
-->

### Instrução de controle de linha

Uma instrução de controle de linha é usada para especificar um número de linha e um nome de arquivo
que podem ser diferentes do número de linha e do nome de arquivo do código-fonte que está sendo compilado.
Use uma instrução de controle de linha para alterar a localização do código-fonte
usada pelo Swift em diagnósticos e para depuração.

Uma instrução de controle de linha tem as seguintes formas:

```swift
#sourceLocation(file: <#file path#>, line: <#line number#>)
#sourceLocation()
```

A primeira forma de instrução de controle de linha altera os valores
das expressões literais `#line`, `#file`, `#fileID` e `#filePath`,
começando na linha de código que segue a instrução de controle de linha.
O *número de linha* altera o valor de `#line`
e é qualquer literal inteiro maior que zero.
O *caminho do arquivo* altera o valor de `#file`, `#fileID` e `#filePath`,
e é um literal de string.
A string especificada se torna o valor de `#filePath`,
e o último componente do caminho da string é usado pelo valor de `#fileID`.
Para informações sobre `#file`, `#fileID` e `#filePath`,
veja <doc:Expressions#Literal-Expression>.

A segunda forma de instrução de controle de linha, `#sourceLocation()`,
restaura a localização do código-fonte para a numeração de linhas e o caminho de arquivo padrão.

> Gramática de uma instrução de controle de linha:
>
> *line-control-statement* → **`#sourceLocation`** **`(`** **`file:`** *file-path* **`,`** **`line:`** *line-number* **`)`** \
> *line-control-statement* → **`#sourceLocation`** **`(`** **`)`** \
> *line-number* → Um inteiro decimal maior que zero \
> *file-path* → *static-string-literal*

### Instrução de diagnóstico em tempo de compilação

Antes do Swift 5.9,
as instruções `#warning` e `#error` emitiam um diagnóstico durante a compilação.
Esse comportamento agora é oferecido pelas macros
[`warning(_:)`][] e [`error(_:)`][] da biblioteca padrão do Swift.

[`warning(_:)`]: https://developer.apple.com/documentation/swift/warning(_:)
[`error(_:)`]: https://developer.apple.com/documentation/swift/error(_:)

## Condição de disponibilidade

Uma *condição de disponibilidade* é usada como condição de uma instrução `if`, `while`
e `guard` para consultar a disponibilidade de APIs em tempo de execução,
com base nos argumentos de plataforma especificados.

Uma condição de disponibilidade tem a seguinte forma:

```swift
if #available(<#platform name#> <#version#>, <#...#>, *) {
    <#statements to execute if the APIs are available#>
} else {
    <#fallback statements to execute if the APIs are unavailable#>
}
```

Você usa uma condição de disponibilidade para executar um bloco de código,
dependendo de as APIs que você quer usar estarem disponíveis em tempo de execução.
O compilador usa as informações da condição de disponibilidade
ao verificar se as APIs naquele bloco de código estão disponíveis.

A condição de disponibilidade recebe uma lista de nomes de plataforma e versões separada por vírgulas.
Use `iOS`, `macOS`, `watchOS`, `tvOS` e `visionOS` para os nomes de plataforma,
e inclua os números de versão correspondentes.
O argumento `*` é obrigatório e especifica que, em qualquer outra plataforma,
o corpo do bloco de código protegido pela condição de disponibilidade
é executado na versão mínima de implantação especificada pelo seu target.

Diferente das condições booleanas, você não pode combinar condições de disponibilidade
usando operadores lógicos como `&&` e `||`.
Em vez de usar `!` para negar uma condição de disponibilidade,
use uma condição de indisponibilidade, que tem a seguinte forma:

```swift
if #unavailable(<#platform name#> <#version#>, <#...#>) {
    <#fallback statements to execute if the APIs are unavailable#>
} else {
    <#statements to execute if the APIs are available#>
}
```

A forma `#unavailable` é um açúcar sintático que nega a condição.
Em uma condição de indisponibilidade, o argumento `*` é implícito
e não deve ser incluído.
Ele tem o mesmo significado que o argumento `*` em uma condição de disponibilidade.

> Gramática de uma condição de disponibilidade:
>
> *availability-condition* → **`#available`** **`(`** *availability-arguments* **`)`** \
> *availability-condition* → **`#unavailable`** **`(`** *availability-arguments* **`)`** \
> *availability-arguments* → *availability-argument* | *availability-argument* **`,`** *availability-arguments* \
> *availability-argument* → *platform-name* *platform-version* \
> *availability-argument* → **`*`**
>
> *platform-name* → **`iOS`** | **`iOSApplicationExtension`** \
> *platform-name* → **`macOS`** | **`macOSApplicationExtension`** \
> *platform-name* → **`macCatalyst`** | **`macCatalystApplicationExtension`** \
> *platform-name* → **`watchOS`** | **`watchOSApplicationExtension`** \
> *platform-name* → **`tvOS`** | **`tvOSApplicationExtension`** \
> *platform-name* → **`visionOS`** | **`visionOSApplicationExtension`** \
> *platform-version* → *decimal-digits* \
> *platform-version* → *decimal-digits* **`.`** *decimal-digits* \
> *platform-version* → *decimal-digits* **`.`** *decimal-digits* **`.`** *decimal-digits*

<!--
  If you need to add a new platform to this list,
  you probably need to update the list under @available too.
-->

<!--
  - test: `pound-available-platform-names`

  ```swifttest
  >> if #available(iOS 1, iOSApplicationExtension 1,
  >>               macOS 1, macOSApplicationExtension 1,
  >>               macCatalyst 1, macCatalystApplicationExtension 1,
  >>               watchOS 1, watchOSApplicationExtension 1,
  >>               tvOS 1, tvOSApplicationExtension 1,
  >>               visionOS 1, visionOSApplicationExtension 1, *) {
  >>     print("a")
  >> } else {
  >>     print("b")
  >> }
  >> if #available(madeUpPlatform 1, *) {
  >>     print("c")
  >> }
  >> if #unavailable(fakePlatform 1) {
  >>     print("d")
  >> } else {
  >>     print("dd")
  >> }
  !$ warning: unrecognized platform name 'madeUpPlatform'
  !$ if #available(madeUpPlatform 1, *) {
  !$               ^
  !$ warning: unrecognized platform name 'fakePlatform'
  !$ if #unavailable(fakePlatform 1) {
  !$                 ^
  << a
  << c
  << dd
  ```
-->

<!--
  - test: `empty-availability-condition`

  ```swifttest
  >> if #available(*) { print("1") }
  << 1
  ```
-->

<!--
  - test: `empty-unavailability-condition`

  ```swifttest
  >> if #unavailable() { print("2") }
  !$ error: expected platform name
  !$ if #unavailable() { print("2") }
  !$                ^
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
