# Funções

Defina e chame funções, rotule os argumentos e use os valores de retorno.

*Funções* são trechos de código autocontidos que executam uma tarefa específica.
Você dá a uma função um nome que identifica o que ela faz,
e esse nome é usado para “chamar” a função e executar sua tarefa quando necessário.

A sintaxe unificada de funções do Swift é flexível o bastante para expressar desde
uma função simples no estilo C, sem nomes de parâmetros,
até um método complexo no estilo Objective-C,
com nomes e rótulos de argumento para cada parâmetro.
Parâmetros podem ter valores padrão para simplificar as chamadas de função
e podem ser passados como parâmetros in-out,
que modificam uma variável passada depois que a função termina sua execução.

Toda função em Swift tem um tipo,
formado pelos tipos dos seus parâmetros e pelo tipo de retorno.
Você pode usar esse tipo como qualquer outro tipo em Swift,
o que facilita passar funções como parâmetros para outras funções
e retornar funções a partir de outras funções.
Funções também podem ser escritas dentro de outras funções
para encapsular funcionalidades úteis no escopo de uma função aninhada.

## Definindo e chamando funções

Ao definir uma função,
você pode, opcionalmente, definir um ou mais valores nomeados e tipados que a função recebe como entrada,
conhecidos como *parâmetros*.
Você também pode, opcionalmente, definir
um tipo de valor que a função retorna como saída ao terminar,
conhecido como seu *tipo de retorno*.

Toda função tem um *nome de função*,
que descreve a tarefa que ela executa.
Para usar uma função, você “chama” essa função pelo nome
e passa valores de entrada (conhecidos como *argumentos*)
que correspondam aos tipos dos parâmetros da função.
Os argumentos de uma função devem sempre ser passados na mesma ordem
da lista de parâmetros da função.

A função do exemplo abaixo se chama `greet(person:)`,
porque é isso que ela faz: recebe o nome de uma pessoa como entrada
e retorna uma saudação para essa pessoa.
Para isso, você define um parâmetro de entrada,
um valor `String` chamado `person`,
e um tipo de retorno `String`,
que conterá uma saudação para essa pessoa:

```swift
func greet(person: String) -> String {
    let greeting = "Hello, " + person + "!"
    return greeting
}
```

<!--
  - test: `definingAndCalling`

  ```swifttest
  -> func greet(person: String) -> String {
        let greeting = "Hello, " + person + "!"
        return greeting
     }
  ```
-->

Toda essa informação é reunida na *definição* da função,
que começa com a palavra-chave `func`.
Você indica o tipo de retorno com a *seta de retorno* `->`
(um hífen seguido de um colchete angular à direita),
que é seguida pelo nome do tipo a ser retornado.

A definição descreve o que a função faz,
o que ela espera receber
e o que retorna ao terminar.
Essa definição permite que a função seja chamada sem ambiguidade
de qualquer lugar do seu código:

```swift
print(greet(person: "Anna"))
// Prints "Hello, Anna!"
print(greet(person: "Brian"))
// Prints "Hello, Brian!"
```

<!--
  - test: `definingAndCalling`

  ```swifttest
  -> print(greet(person: "Anna"))
  <- Hello, Anna!
  -> print(greet(person: "Brian"))
  <- Hello, Brian!
  ```
-->

Você chama a função `greet(person:)`
passando a ela um valor `String` depois do rótulo de argumento `person`,
como em `greet(person: "Anna")`.
Como a função retorna um valor `String`,
`greet(person:)` pode ser envolvida em uma chamada à função `print(_:separator:terminator:)`
para imprimir essa string e ver seu valor de retorno, como mostrado acima.

> Nota: A função `print(_:separator:terminator:)`
> não tem rótulo para o primeiro argumento,
> e os outros argumentos são opcionais porque têm valor padrão.
> Essas variações da sintaxe de funções são discutidas abaixo
> em <doc:Functions#Function-Argument-Labels-and-Parameter-Names>
> e <doc:Functions#Default-Parameter-Values>.

O corpo da função `greet(person:)` começa
definindo uma nova constante `String` chamada `greeting`
e atribuindo a ela uma mensagem de saudação simples.
Essa saudação é então retornada pela função com a palavra-chave `return`.
Na linha `return greeting`,
a função termina sua execução e retorna o valor atual de `greeting`.

Você pode chamar a função `greet(person:)` várias vezes com valores de entrada diferentes.
O exemplo acima mostra o que acontece quando ela é chamada com o valor de entrada `"Anna"`
e com o valor de entrada `"Brian"`.
A função retorna uma saudação personalizada em cada caso.

Para deixar o corpo dessa função mais curto,
você pode combinar a criação da mensagem e a instrução `return` em uma única linha:

```swift
func greetAgain(person: String) -> String {
    return "Hello again, " + person + "!"
}
print(greetAgain(person: "Anna"))
// Prints "Hello again, Anna!"
```

<!--
  - test: `definingAndCalling`

  ```swifttest
  -> func greetAgain(person: String) -> String {
        return "Hello again, " + person + "!"
     }
  -> print(greetAgain(person: "Anna"))
  <- Hello again, Anna!
  ```
-->

## Parâmetros e valores de retorno de funções

Parâmetros e valores de retorno de funções são extremamente flexíveis em Swift.
Você pode definir desde uma função utilitária simples, com um único parâmetro sem nome,
até uma função complexa com nomes de parâmetros expressivos e diferentes opções de parâmetros.

### Funções sem parâmetros

Funções não são obrigadas a definir parâmetros de entrada.
Aqui está uma função sem parâmetros de entrada,
que retorna sempre a mesma mensagem `String` cada vez que é chamada:

```swift
func sayHelloWorld() -> String {
    return "hello, world"
}
print(sayHelloWorld())
// Prints "hello, world".
```

<!--
  - test: `functionsWithoutParameters`

  ```swifttest
  -> func sayHelloWorld() -> String {
        return "hello, world"
     }
  -> print(sayHelloWorld())
  <- hello, world
  ```
-->

A definição da função ainda precisa de parênteses depois do nome,
mesmo que ela não receba parâmetros.
O nome da função também é seguido de
um par de parênteses vazios quando ela é chamada.

### Funções com vários parâmetros

Funções podem ter vários parâmetros de entrada,
escritos entre os parênteses da função, separados por vírgulas.

Esta função recebe o nome de uma pessoa
e se ela já foi cumprimentada, como entrada,
e retorna uma saudação apropriada para essa pessoa:

```swift
func greet(person: String, alreadyGreeted: Bool) -> String {
    if alreadyGreeted {
        return greetAgain(person: person)
    } else {
        return greet(person: person)
    }
}
print(greet(person: "Tim", alreadyGreeted: true))
// Prints "Hello again, Tim!"
```

<!--
  - test: `definingAndCalling`

  ```swifttest
  -> func greet(person: String, alreadyGreeted: Bool) -> String {
         if alreadyGreeted {
             return greetAgain(person: person)
         } else {
             return greet(person: person)
         }
     }
  -> print(greet(person: "Tim", alreadyGreeted: true))
  <- Hello again, Tim!
  ```
-->

Você chama a função `greet(person:alreadyGreeted:)`
passando a ela um argumento `String` com o rótulo `person`
e um argumento `Bool` com o rótulo `alreadyGreeted`,
entre parênteses, separados por vírgulas.
Note que essa função é diferente da função `greet(person:)`
mostrada em uma seção anterior.
Embora as duas funções tenham nomes que começam com `greet`,
a função `greet(person:alreadyGreeted:)` recebe dois argumentos,
enquanto a função `greet(person:)` recebe apenas um.

### Funções sem valores de retorno

Funções não são obrigadas a definir um tipo de retorno.
Aqui está uma versão da função `greet(person:)`
que imprime seu próprio valor `String` em vez de retorná-lo:

```swift
func greet(person: String) {
    print("Hello, \(person)!")
}
greet(person: "Dave")
// Prints "Hello, Dave!"
```

<!--
  - test: `functionsWithoutReturnValues`

  ```swifttest
  -> func greet(person: String) {
        print("Hello, \(person)!")
     }
  -> greet(person: "Dave")
  <- Hello, Dave!
  ```
-->

Como ela não precisa retornar um valor,
a definição da função não inclui a seta de retorno (`->`)
nem um tipo de retorno.

> Nota: Estritamente falando, esta versão da função `greet(person:)` *ainda* retorna um valor,
> mesmo que nenhum valor de retorno seja definido.
> Funções sem tipo de retorno definido retornam um valor especial do tipo `Void`.
> Trata-se simplesmente de uma tupla vazia,
> escrita como `()`.

O valor de retorno de uma função pode ser ignorado na chamada:

```swift
func printAndCount(string: String) -> Int {
    print(string)
    return string.count
}
func printWithoutCounting(string: String) {
    let _ = printAndCount(string: string)
}
printAndCount(string: "hello, world")
// prints "hello, world" and returns a value of 12
printWithoutCounting(string: "hello, world")
// prints "hello, world" but doesn't return a value
```

<!--
  - test: `functionsWithoutReturnValues`

  ```swifttest
  -> func printAndCount(string: String) -> Int {
        print(string)
        return string.count
     }
  -> func printWithoutCounting(string: String) {
        let _ = printAndCount(string: string)
     }
  >> let a =
  -> printAndCount(string: "hello, world")
  << hello, world
  >> assert(a == 12)
  // prints "hello, world" and returns a value of 12
  -> printWithoutCounting(string: "hello, world")
  << hello, world
  // prints "hello, world" but doesn't return a value
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

A primeira função, `printAndCount(string:)`,
imprime uma string e depois retorna sua contagem de caracteres como `Int`.
A segunda função, `printWithoutCounting(string:)`,
chama a primeira função, mas ignora seu valor de retorno.
Quando a segunda função é chamada,
a mensagem ainda é impressa pela primeira função,
mas o valor retornado não é usado.

> Nota: Valores de retorno podem ser ignorados,
> mas uma função que declara que vai retornar um valor deve sempre fazê-lo.
> Uma função com tipo de retorno definido
> não pode deixar o controle chegar ao fim do corpo sem retornar um valor,
> e tentar isso resulta em erro de compilação.

<!--
FIXME Unless the function is marked @discardableResult,
ignoring its return value triggers a compile-time warning.

If the returned value is coincidental
marking with @discardableResult is good,
like array.removeFirst(...) ---
otherwise, using `_ = foo()` at the call site is better.
-->

### Funções com vários valores de retorno

Você pode usar um tipo de tupla como tipo de retorno de uma função
para retornar vários valores como parte de um único valor de retorno composto.

O exemplo abaixo define uma função chamada `minMax(array:)`,
que encontra o menor e o maior número em um array de valores `Int`:

```swift
func minMax(array: [Int]) -> (min: Int, max: Int) {
    var currentMin = array[0]
    var currentMax = array[0]
    for value in array[1..<array.count] {
        if value < currentMin {
            currentMin = value
        } else if value > currentMax {
            currentMax = value
        }
    }
    return (currentMin, currentMax)
}
```

<!--
  - test: `tupleTypesAsReturnTypes`

  ```swifttest
  -> func minMax(array: [Int]) -> (min: Int, max: Int) {
        var currentMin = array[0]
        var currentMax = array[0]
        for value in array[1..<array.count] {
           if value < currentMin {
              currentMin = value
           } else if value > currentMax {
              currentMax = value
           }
        }
        return (currentMin, currentMax)
     }
  ```
-->

A função `minMax(array:)` retorna uma tupla contendo dois valores `Int`.
Esses valores têm os rótulos `min` e `max`
para que possam ser acessados pelo nome ao consultar o valor de retorno da função.

O corpo da função `minMax(array:)` começa definindo
duas variáveis de trabalho chamadas `currentMin` e `currentMax`
com o valor do primeiro inteiro do array.
Em seguida, a função percorre os demais valores do array
e verifica se cada valor é menor ou maior
que os valores de `currentMin` e `currentMax`, respectivamente.
Por fim, os valores mínimo e máximo gerais são retornados
como uma tupla de dois valores `Int`.

Como os membros da tupla são nomeados como parte do tipo de retorno da função,
eles podem ser acessados com a sintaxe de ponto para obter o mínimo e o máximo encontrados:

```swift
let bounds = minMax(array: [8, -6, 2, 109, 3, 71])
print("min is \(bounds.min) and max is \(bounds.max)")
// Prints "min is -6 and max is 109".
```

<!--
  - test: `tupleTypesAsReturnTypes`

  ```swifttest
  -> let bounds = minMax(array: [8, -6, 2, 109, 3, 71])
  -> print("min is \(bounds.min) and max is \(bounds.max)")
  <- min is -6 and max is 109
  ```
-->

Note que os membros da tupla não precisam ser nomeados
no momento em que a tupla é retornada pela função,
porque os nomes já estão especificados como parte do tipo de retorno da função.

#### Tipos de retorno de tupla opcionais

Se o tipo de tupla a ser retornado por uma função
pode não ter “valor nenhum” para a tupla inteira,
você pode usar um tipo de retorno de tupla *opcional* para refletir o fato de que
a tupla inteira pode ser `nil`.
Você escreve um tipo de retorno de tupla opcional colocando um ponto de interrogação
depois do parêntese de fechamento do tipo da tupla,
como `(Int, Int)?` ou `(String, Int, Bool)?`.

> Nota: Um tipo de tupla opcional, como `(Int, Int)?`,
> é diferente de uma tupla que contém tipos opcionais,
> como `(Int?, Int?)`.
> Com um tipo de tupla opcional, a tupla inteira é opcional,
> e não apenas cada valor individual dentro da tupla.

A função `minMax(array:)` acima retorna uma tupla contendo dois valores `Int`.
No entanto, a função não faz nenhuma verificação de segurança no array que recebe.
Se o argumento `array` for um array vazio,
a função `minMax(array:)`, como definida acima,
disparará um erro em tempo de execução ao tentar acessar `array[0]`.

Para lidar com um array vazio de forma segura,
escreva a função `minMax(array:)` com um tipo de retorno de tupla opcional
e retorne o valor `nil` quando o array estiver vazio:

```swift
func minMax(array: [Int]) -> (min: Int, max: Int)? {
    if array.isEmpty { return nil }
    var currentMin = array[0]
    var currentMax = array[0]
    for value in array[1..<array.count] {
        if value < currentMin {
            currentMin = value
        } else if value > currentMax {
            currentMax = value
        }
    }
    return (currentMin, currentMax)
}
```

<!--
  - test: `tupleTypesAsReturnTypes2`

  ```swifttest
  -> func minMax(array: [Int]) -> (min: Int, max: Int)? {
        if array.isEmpty { return nil }
        var currentMin = array[0]
        var currentMax = array[0]
        for value in array[1..<array.count] {
           if value < currentMin {
              currentMin = value
           } else if value > currentMax {
              currentMax = value
           }
        }
        return (currentMin, currentMax)
     }
  ```
-->

Você pode usar optional binding para verificar se esta versão da função `minMax(array:)`
retorna de fato um valor de tupla ou `nil`:

```swift
if let bounds = minMax(array: [8, -6, 2, 109, 3, 71]) {
    print("min is \(bounds.min) and max is \(bounds.max)")
}
// Prints "min is -6 and max is 109".
```

<!--
  - test: `tupleTypesAsReturnTypes2`

  ```swifttest
  -> if let bounds = minMax(array: [8, -6, 2, 109, 3, 71]) {
        print("min is \(bounds.min) and max is \(bounds.max)")
     }
  <- min is -6 and max is 109
  ```
-->

### Funções com retorno implícito

Se o corpo inteiro da função for uma única expressão,
a função retorna essa expressão implicitamente.
Por exemplo,
as duas funções abaixo têm o mesmo comportamento:

```swift
func greeting(for person: String) -> String {
    "Hello, " + person + "!"
}
print(greeting(for: "Dave"))
// Prints "Hello, Dave!"

func anotherGreeting(for person: String) -> String {
    return "Hello, " + person + "!"
}
print(anotherGreeting(for: "Dave"))
// Prints "Hello, Dave!"
```

<!--
  - test: `implicit-func-return`

  ```swifttest
  -> func greeting(for person: String) -> String {
        "Hello, " + person + "!"
     }
  -> print(greeting(for: "Dave"))
  <- Hello, Dave!

  -> func anotherGreeting(for person: String) -> String {
        return "Hello, " + person + "!"
     }
  -> print(anotherGreeting(for: "Dave"))
  <- Hello, Dave!
  ```
-->

A definição inteira da função `greeting(for:)`
é a mensagem de saudação que ela retorna,
o que significa que ela pode usar esta forma mais curta.
A função `anotherGreeting(for:)` retorna a mesma mensagem de saudação,
usando a palavra-chave `return`, como numa função mais longa.
Qualquer função que você escreva como apenas uma linha `return` pode omitir o `return`.

Como você verá em <doc:Properties#Shorthand-Getter-Declaration>,
getters de propriedades também podem usar retorno implícito.

> Nota: O código que você escreve como valor de retorno implícito
> precisa retornar algum valor.
> Por exemplo,
> você não pode usar `print(13)`
> como valor de retorno implícito.
> No entanto, você pode usar uma função que nunca retorna,
> como `fatalError("Oh no!")`,
> como valor de retorno implícito,
> porque o Swift sabe que o retorno implícito não acontece.

<!--
  - test: `implicit-return-print-instead`

  ```swifttest
  // This is ok:
  >> func testFatal() -> Int {
  >>     fatalError("Oh no!")
  >> }

  // But not this:
  >> func testPrint() -> Int {
  >>     print(13)
  >> }
  !$ error: cannot convert return expression of type '()' to return type 'Int'
  !! print(13)
  !! ^~~~~~~~~
  ```
-->

## Rótulos de argumento e nomes de parâmetros de função

Cada parâmetro de função tem tanto um *rótulo de argumento*
quanto um *nome de parâmetro*.
O rótulo de argumento é usado ao chamar a função;
cada argumento é escrito na chamada da função com seu rótulo de argumento antes dele.
O nome do parâmetro é usado na implementação da função.
Por padrão, os parâmetros
usam seu nome de parâmetro como rótulo de argumento.

```swift
func someFunction(firstParameterName: Int, secondParameterName: Int) {
    // In the function body, firstParameterName and secondParameterName
    // refer to the argument values for the first and second parameters.
}
someFunction(firstParameterName: 1, secondParameterName: 2)
```

<!--
  - test: `functionParameterNames`

  ```swifttest
  -> func someFunction(firstParameterName: Int, secondParameterName: Int) {
        // In the function body, firstParameterName and secondParameterName
        // refer to the argument values for the first and second parameters.
     }
  -> someFunction(firstParameterName: 1, secondParameterName: 2)
  ```
-->

Todos os parâmetros devem ter nomes únicos.
Embora seja possível que vários parâmetros
tenham o mesmo rótulo de argumento,
rótulos de argumento únicos ajudam a tornar seu código mais legível.

<!--
  - test: `non-unique-external-name`

  ```swifttest
  -> func foo(external a: Int, external b: Int) {}
  -> foo(external: 7, external: 12)
  ```
-->

### Especificando rótulos de argumento

Você escreve um rótulo de argumento antes do nome do parâmetro,
separado por um espaço:

```swift
func someFunction(argumentLabel parameterName: Int) {
    // In the function body, parameterName refers to the argument value
    // for that parameter.
}
```

<!--
  - test: `externalParameterNames`

  ```swifttest
  -> func someFunction(argumentLabel parameterName: Int) {
        // In the function body, parameterName refers to the argument value
        // for that parameter.
     }
  ```
-->

Aqui está uma variação da função `greet(person:)`
que recebe o nome e a cidade natal de uma pessoa
e retorna uma saudação:

```swift
func greet(person: String, from hometown: String) -> String {
    return "Hello \(person)!  Glad you could visit from \(hometown)."
}
print(greet(person: "Bill", from: "Cupertino"))
// Prints "Hello Bill!  Glad you could visit from Cupertino."
```

<!--
  - test: `externalParameterNames`

  ```swifttest
  -> func greet(person: String, from hometown: String) -> String {
         return "Hello \(person)!  Glad you could visit from \(hometown)."
     }
  -> print(greet(person: "Bill", from: "Cupertino"))
  <- Hello Bill!  Glad you could visit from Cupertino.
  ```
-->

O uso de rótulos de argumento permite que uma função
seja chamada de forma expressiva, parecida com uma frase,
mantendo um corpo de função legível e claro em sua intenção.

### Omitindo rótulos de argumento

Se você não quiser um rótulo de argumento para um parâmetro,
escreva um sublinhado (`_`) no lugar de um rótulo de argumento explícito para esse parâmetro.

```swift
func someFunction(_ firstParameterName: Int, secondParameterName: Int) {
    // In the function body, firstParameterName and secondParameterName
    // refer to the argument values for the first and second parameters.
}
someFunction(1, secondParameterName: 2)
```

<!--
  - test: `omittedExternalParameterNames`

  ```swifttest
  -> func someFunction(_ firstParameterName: Int, secondParameterName: Int) {
        // In the function body, firstParameterName and secondParameterName
        // refer to the argument values for the first and second parameters.
     }
  -> someFunction(1, secondParameterName: 2)
  ```
-->

Se um parâmetro tiver rótulo de argumento,
o argumento *deve* ser rotulado ao chamar a função.

### Valores padrão de parâmetros

Você pode definir um *valor padrão* para qualquer parâmetro de uma função
atribuindo um valor ao parâmetro depois do tipo desse parâmetro.
Se um valor padrão for definido, você pode omitir esse parâmetro ao chamar a função.

```swift
func someFunction(parameterWithoutDefault: Int, parameterWithDefault: Int = 12) {
    // If you omit the second argument when calling this function, then
    // the value of parameterWithDefault is 12 inside the function body.
}
someFunction(parameterWithoutDefault: 3, parameterWithDefault: 6) // parameterWithDefault is 6
someFunction(parameterWithoutDefault: 4) // parameterWithDefault is 12
```

<!--
  - test: `omittedExternalParameterNames`

  ```swifttest
  -> func someFunction(parameterWithoutDefault: Int, parameterWithDefault: Int = 12) {
        // If you omit the second argument when calling this function, then
        // the value of parameterWithDefault is 12 inside the function body.
     }
  -> someFunction(parameterWithoutDefault: 3, parameterWithDefault: 6) // parameterWithDefault is 6
  -> someFunction(parameterWithoutDefault: 4) // parameterWithDefault is 12
  ```
-->

Coloque os parâmetros que não têm valores padrão
no início da lista de parâmetros da função,
antes dos parâmetros que têm valores padrão.
Parâmetros sem valores padrão costumam ser mais importantes para o significado da função,
então escrevê-los primeiro facilita reconhecer
que a mesma função está sendo chamada,
independentemente de algum parâmetro padrão ser omitido.

### Parâmetros variádicos

Um *parâmetro variádico* aceita zero ou mais valores de um tipo especificado.
Você usa um parâmetro variádico para indicar que o parâmetro pode receber
um número variável de valores de entrada quando a função é chamada.
Escreva parâmetros variádicos inserindo três pontos (`...`)
depois do nome do tipo do parâmetro.

Os valores passados a um parâmetro variádico ficam disponíveis no corpo da função
como um array do tipo apropriado.
Por exemplo, um parâmetro variádico com o nome `numbers` e o tipo `Double...`
fica disponível no corpo da função como
uma constante array chamada `numbers`, do tipo `[Double]`.

O exemplo abaixo calcula a *média aritmética*
(também conhecida como *média*) de uma lista de números de qualquer tamanho:

```swift
func arithmeticMean(_ numbers: Double...) -> Double {
    var total: Double = 0
    for number in numbers {
        total += number
    }
    return total / Double(numbers.count)
}
arithmeticMean(1, 2, 3, 4, 5)
// returns 3.0, which is the arithmetic mean of these five numbers
arithmeticMean(3, 8.25, 18.75)
// returns 10.0, which is the arithmetic mean of these three numbers
```

<!--
  - test: `variadicParameters`

  ```swifttest
  -> func arithmeticMean(_ numbers: Double...) -> Double {
        var total: Double = 0
        for number in numbers {
           total += number
        }
        return total / Double(numbers.count)
     }
  >> let r0 =
  -> arithmeticMean(1, 2, 3, 4, 5)
  /> returns \(r0), which is the arithmetic mean of these five numbers
  </ returns 3.0, which is the arithmetic mean of these five numbers
  >> let r1 =
  -> arithmeticMean(3, 8.25, 18.75)
  /> returns \(r1), which is the arithmetic mean of these three numbers
  </ returns 10.0, which is the arithmetic mean of these three numbers
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

Uma função pode ter vários parâmetros variádicos.
O primeiro parâmetro que vem depois de um parâmetro variádico
deve ter um rótulo de argumento.
O rótulo de argumento deixa claro
quais argumentos são passados ao parâmetro variádico
e quais argumentos são passados aos parâmetros
que vêm depois do parâmetro variádico.

<!--
  - test: `variadic-parameters-and-labels`

  ```swifttest
  // Labeled, immediately after
  >> func f(_ a: Int..., b: String) {}

  // Unlabeled, not immediately after
  >> func g(_ a: Int..., b: String, _ c: Int) {}

  // Multiple
  >> func h(_a: Int..., b: String, _ c: Int..., d: String) {}
  ```
-->

<!--
  - test: `variadic-parameters-and-labels-failure`

  ```swifttest
  // Unlabeled, immediately after
  >> func f(_ a: Int..., _ b: String) {}
  !$ error: a parameter following a variadic parameter requires a label
  !! func f(_ a: Int..., _ b: String) {}
  !! ^
  ```
-->

### Parâmetros in-out

Parâmetros de função são constantes por padrão.
Tentar alterar o valor de um parâmetro de função
dentro do corpo dessa função resulta em erro de compilação.
Isso significa que você não consegue alterar o valor de um parâmetro por engano.
Se você quiser que uma função modifique o valor de um parâmetro,
e quiser que essas mudanças permaneçam depois que a chamada da função terminar,
defina esse parâmetro como um *parâmetro in-out*.

Você escreve um parâmetro in-out colocando a palavra-chave `inout`
logo antes do tipo do parâmetro.
Um parâmetro in-out tem um valor que é passado *para dentro* da função,
é modificado pela função
e é retornado *para fora* da função, substituindo o valor original.
Para uma discussão detalhada sobre o comportamento dos parâmetros in-out
e as otimizações do compilador associadas,
veja <doc:Declarations#In-Out-Parameters>.

Você só pode passar uma variável como argumento para um parâmetro in-out.
Não é possível passar uma constante ou um valor literal como argumento,
porque constantes e literais não podem ser modificados.
Você coloca um e comercial (`&`) diretamente antes do nome de uma variável
quando a passa como argumento para um parâmetro in-out,
para indicar que ela pode ser modificada pela função.

> Nota: Parâmetros in-out não podem ter valores padrão,
> e parâmetros variádicos não podem ser marcados como `inout`.

Aqui está um exemplo de uma função chamada `swapTwoInts(_:_:)`,
que tem dois parâmetros in-out inteiros chamados `a` e `b`:

```swift
func swapTwoInts(_ a: inout Int, _ b: inout Int) {
    let temporaryA = a
    a = b
    b = temporaryA
}
```

<!--
  - test: `inoutParameters`

  ```swifttest
  -> func swapTwoInts(_ a: inout Int, _ b: inout Int) {
        let temporaryA = a
        a = b
        b = temporaryA
     }
  ```
-->

A função `swapTwoInts(_:_:)` simplesmente troca o valor de `b` para `a`,
e o valor de `a` para `b`.
Ela faz essa troca armazenando o valor de `a` em
uma constante temporária chamada `temporaryA`, atribuindo o valor de `b` a `a`
e depois atribuindo `temporaryA` a `b`.

Você pode chamar a função `swapTwoInts(_:_:)` com duas variáveis do tipo `Int`
para trocar seus valores.
Observe que os nomes de `someInt` e `anotherInt` são precedidos por um e comercial
quando são passados à função `swapTwoInts(_:_:)`:

```swift
var someInt = 3
var anotherInt = 107
swapTwoInts(&someInt, &anotherInt)
print("someInt is now \(someInt), and anotherInt is now \(anotherInt)")
// Prints "someInt is now 107, and anotherInt is now 3".
```

<!--
  - test: `inoutParameters`

  ```swifttest
  -> var someInt = 3
  -> var anotherInt = 107
  -> swapTwoInts(&someInt, &anotherInt)
  -> print("someInt is now \(someInt), and anotherInt is now \(anotherInt)")
  <- someInt is now 107, and anotherInt is now 3
  ```
-->

O exemplo acima mostra que
os valores originais de `someInt` e `anotherInt`
são modificados pela função `swapTwoInts(_:_:)`,
mesmo tendo sido definidos originalmente fora da função.

> Nota: Parâmetros in-out não são o mesmo que retornar um valor de uma função.
> O exemplo `swapTwoInts` acima não define um tipo de retorno nem retorna um valor,
> mas ainda assim modifica os valores de `someInt` e `anotherInt`.
> Parâmetros in-out são uma forma alternativa de uma função produzir um efeito
> fora do escopo do seu corpo.

<!--
  TODO: you can pass a subproperty of something as an inout reference.
  Would be great to show an example of this as a way to avoid temporary variables.
-->

## Tipos de função

Toda função tem um *tipo de função* específico,
formado pelos tipos dos parâmetros e pelo tipo de retorno da função.

Por exemplo:

```swift
func addTwoInts(_ a: Int, _ b: Int) -> Int {
    return a + b
}
func multiplyTwoInts(_ a: Int, _ b: Int) -> Int {
    return a * b
}
```

<!--
  - test: `functionTypes`

  ```swifttest
  -> func addTwoInts(_ a: Int, _ b: Int) -> Int {
        return a + b
     }
  >> print(type(of: addTwoInts))
  << (Int, Int) -> Int
  -> func multiplyTwoInts(_ a: Int, _ b: Int) -> Int {
        return a * b
     }
  >> print(type(of: multiplyTwoInts))
  << (Int, Int) -> Int
  ```
-->

Este exemplo define duas funções matemáticas simples
chamadas `addTwoInts` e `multiplyTwoInts`.
Essas funções recebem cada uma dois valores `Int`
e retornam um valor `Int`, que é o resultado
de uma operação matemática apropriada.

O tipo das duas funções é `(Int, Int) -> Int`.
Isso pode ser lido assim:

“Uma função que tem dois parâmetros, ambos do tipo `Int`,
e que retorna um valor do tipo `Int`.”

Aqui está outro exemplo, para uma função sem parâmetros nem valor de retorno:

```swift
func printHelloWorld() {
    print("hello, world")
}
```

<!--
  - test: `functionTypes`

  ```swifttest
  -> func printHelloWorld() {
        print("hello, world")
     }
  >> print(type(of: printHelloWorld))
  << () -> ()
  ```
-->

O tipo desta função é `() -> Void`,
ou “uma função que não tem parâmetros e retorna `Void`.”

### Usando tipos de função

Você usa tipos de função exatamente como qualquer outro tipo em Swift.
Por exemplo, você pode definir uma constante ou variável com um tipo de função
e atribuir a essa variável uma função apropriada:

```swift
var mathFunction: (Int, Int) -> Int = addTwoInts
```

<!--
  - test: `functionTypes`

  ```swifttest
  -> var mathFunction: (Int, Int) -> Int = addTwoInts
  ```
-->

Isso pode ser lido assim:

“Defina uma variável chamada `mathFunction`,
que tem o tipo ‘uma função que recebe dois valores `Int`
e retorna um valor `Int`.’
Atribua a essa nova variável uma referência à função chamada `addTwoInts`.”

A função `addTwoInts(_:_:)` tem o mesmo tipo que a variável `mathFunction`,
por isso essa atribuição é permitida pelo verificador de tipos do Swift.

Agora você pode chamar a função atribuída usando o nome `mathFunction`:

```swift
print("Result: \(mathFunction(2, 3))")
// Prints "Result: 5".
```

<!--
  - test: `functionTypes`

  ```swifttest
  -> print("Result: \(mathFunction(2, 3))")
  <- Result: 5
  ```
-->

Outra função com o mesmo tipo correspondente pode ser atribuída à mesma variável,
da mesma forma que para tipos que não são de função:

```swift
mathFunction = multiplyTwoInts
print("Result: \(mathFunction(2, 3))")
// Prints "Result: 6".
```

<!--
  - test: `functionTypes`

  ```swifttest
  -> mathFunction = multiplyTwoInts
  -> print("Result: \(mathFunction(2, 3))")
  <- Result: 6
  ```
-->

Como em qualquer outro tipo,
você pode deixar que o Swift infira o tipo da função
ao atribuir uma função a uma constante ou variável:

```swift
let anotherMathFunction = addTwoInts
// anotherMathFunction is inferred to be of type (Int, Int) -> Int
```

<!--
  - test: `functionTypes`

  ```swifttest
  -> let anotherMathFunction = addTwoInts
  >> print(type(of: anotherMathFunction))
  << (Int, Int) -> Int
  // anotherMathFunction is inferred to be of type (Int, Int) -> Int
  ```
-->

<!--
  TODO: talk about defining typealiases for function types somewhere?
-->

### Tipos de função como tipos de parâmetro

Você pode usar um tipo de função como `(Int, Int) -> Int`
como tipo de parâmetro de outra função.
Isso permite deixar para quem chama a função fornecer alguns aspectos da implementação
no momento da chamada.

Aqui está um exemplo para imprimir os resultados das funções matemáticas de antes:

```swift
func printMathResult(_ mathFunction: (Int, Int) -> Int, _ a: Int, _ b: Int) {
    print("Result: \(mathFunction(a, b))")
}
printMathResult(addTwoInts, 3, 5)
// Prints "Result: 8".
```

<!--
  - test: `functionTypes`

  ```swifttest
  -> func printMathResult(_ mathFunction: (Int, Int) -> Int, _ a: Int, _ b: Int) {
        print("Result: \(mathFunction(a, b))")
     }
  -> printMathResult(addTwoInts, 3, 5)
  <- Result: 8
  ```
-->

Este exemplo define uma função chamada `printMathResult(_:_:_:)`, que tem três parâmetros.
O primeiro parâmetro se chama `mathFunction` e é do tipo `(Int, Int) -> Int`.
Você pode passar qualquer função desse tipo como argumento para este primeiro parâmetro.
O segundo e o terceiro parâmetros se chamam `a` e `b`, e são ambos do tipo `Int`.
Eles são usados como os dois valores de entrada para a função matemática fornecida.

Quando `printMathResult(_:_:_:)` é chamada,
ela recebe a função `addTwoInts(_:_:)` e os valores inteiros `3` e `5`.
Ela chama a função fornecida com os valores `3` e `5` e imprime o resultado, `8`.

A função de `printMathResult(_:_:_:)` é imprimir o resultado de
uma chamada a uma função matemática de um tipo apropriado.
Não importa o que a implementação dessa função realmente faz:
o que importa é que a função seja do tipo correto.
Isso permite que `printMathResult(_:_:_:)` delegue parte de sua funcionalidade
ao chamador da função, de forma segura em relação aos tipos.

### Tipos de função como tipos de retorno

Você pode usar um tipo de função como tipo de retorno de outra função.
Para isso, você escreve um tipo de função completo
logo depois da seta de retorno (`->`) da função que retorna.

O próximo exemplo define duas funções simples chamadas `stepForward(_:)` e `stepBackward(_:)`.
A função `stepForward(_:)` retorna um valor uma unidade maior que o valor de entrada,
e a função `stepBackward(_:)` retorna um valor uma unidade menor que o valor de entrada.
As duas funções têm o tipo `(Int) -> Int`:

```swift
func stepForward(_ input: Int) -> Int {
    return input + 1
}
func stepBackward(_ input: Int) -> Int {
    return input - 1
}
```

<!--
  - test: `functionTypes`

  ```swifttest
  -> func stepForward(_ input: Int) -> Int {
        return input + 1
     }
  -> func stepBackward(_ input: Int) -> Int {
        return input - 1
     }
  ```
-->

Aqui está uma função chamada `chooseStepFunction(backward:)`,
cujo tipo de retorno é `(Int) -> Int`.
A função `chooseStepFunction(backward:)` retorna a função `stepForward(_:)`
ou a função `stepBackward(_:)`, com base em um parâmetro booleano chamado `backward`:

```swift
func chooseStepFunction(backward: Bool) -> (Int) -> Int {
    return backward ? stepBackward : stepForward
}
```

<!--
  - test: `functionTypes`

  ```swifttest
  -> func chooseStepFunction(backward: Bool) -> (Int) -> Int {
        return backward ? stepBackward : stepForward
     }
  ```
-->

Agora você pode usar `chooseStepFunction(backward:)` para obter uma função
que dá um passo em uma direção ou na outra:

```swift
var currentValue = 3
let moveNearerToZero = chooseStepFunction(backward: currentValue > 0)
// moveNearerToZero now refers to the stepBackward() function
```

<!--
  - test: `functionTypes`

  ```swifttest
  -> var currentValue = 3
  -> let moveNearerToZero = chooseStepFunction(backward: currentValue > 0)
  >> print(type(of: moveNearerToZero))
  << (Int) -> Int
  // moveNearerToZero now refers to the stepBackward() function
  ```
-->

O exemplo acima determina se é preciso um passo positivo ou negativo
para aproximar progressivamente de zero uma variável chamada `currentValue`.
`currentValue` tem valor inicial `3`,
o que significa que `currentValue > 0` retorna `true`,
fazendo com que `chooseStepFunction(backward:)` retorne a função `stepBackward(_:)`.
Uma referência à função retornada é armazenada em uma constante chamada `moveNearerToZero`.

Agora que `moveNearerToZero` se refere à função correta,
ela pode ser usada para contar até zero:

```swift
print("Counting to zero:")
// Counting to zero:
while currentValue != 0 {
    print("\(currentValue)... ")
    currentValue = moveNearerToZero(currentValue)
}
print("zero!")
// 3...
// 2...
// 1...
// zero!
```

<!--
  - test: `functionTypes`

  ```swifttest
  -> print("Counting to zero:")
  </ Counting to zero:
  -> while currentValue != 0 {
        print("\(currentValue)... ")
        currentValue = moveNearerToZero(currentValue)
     }
  -> print("zero!")
  </ 3...
  </ 2...
  </ 1...
  </ zero!
  ```
-->

## Funções aninhadas

Todas as funções que você viu até agora neste capítulo
são exemplos de *funções globais*, definidas em escopo global.
Você também pode definir funções dentro dos corpos de outras funções,
conhecidas como *funções aninhadas*.

Funções aninhadas são ocultas do mundo externo por padrão,
mas ainda podem ser chamadas e usadas pela função que as envolve.
Uma função envolvente também pode retornar uma de suas funções aninhadas
para permitir que a função aninhada seja usada em outro escopo.

Você pode reescrever o exemplo `chooseStepFunction(backward:)` acima
para usar e retornar funções aninhadas:

```swift
func chooseStepFunction(backward: Bool) -> (Int) -> Int {
    func stepForward(input: Int) -> Int { return input + 1 }
    func stepBackward(input: Int) -> Int { return input - 1 }
    return backward ? stepBackward : stepForward
}
var currentValue = -4
let moveNearerToZero = chooseStepFunction(backward: currentValue > 0)
// moveNearerToZero now refers to the nested stepForward() function
while currentValue != 0 {
    print("\(currentValue)... ")
    currentValue = moveNearerToZero(currentValue)
}
print("zero!")
// -4...
// -3...
// -2...
// -1...
// zero!
```

<!--
  - test: `nestedFunctions`

  ```swifttest
  -> func chooseStepFunction(backward: Bool) -> (Int) -> Int {
        func stepForward(input: Int) -> Int { return input + 1 }
        func stepBackward(input: Int) -> Int { return input - 1 }
        return backward ? stepBackward : stepForward
     }
  -> var currentValue = -4
  -> let moveNearerToZero = chooseStepFunction(backward: currentValue > 0)
  >> print(type(of: moveNearerToZero))
  << (Int) -> Int
  // moveNearerToZero now refers to the nested stepForward() function
  -> while currentValue != 0 {
        print("\(currentValue)... ")
        currentValue = moveNearerToZero(currentValue)
     }
  -> print("zero!")
  </ -4...
  </ -3...
  </ -2...
  </ -1...
  </ zero!
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
