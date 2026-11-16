# Tratamento de erros

Responda a erros e recupere-se deles.

*Tratamento de erros* é o processo de responder a condições de erro no seu programa e de se recuperar delas.
O Swift tem suporte de primeira classe para lançar, capturar, propagar e manipular erros recuperáveis em tempo de execução.

Algumas operações não têm garantia de sempre terminar a execução ou de produzir uma saída útil.
Os optionals representam a ausência de um valor, mas, quando uma operação falha,
costuma ser útil entender o que causou a falha,
para que o seu código possa reagir de acordo.

Como exemplo, considere a tarefa de ler e processar dados de um arquivo em disco.
Essa tarefa pode falhar de várias maneiras, incluindo
o arquivo não existir no caminho especificado,
o arquivo não ter permissão de leitura ou
o arquivo não estar codificado em um formato compatível.
Distinguir essas situações diferentes permite que um programa resolva alguns erros
e comunique ao usuário os erros que não consegue resolver.

> Nota: O tratamento de erros no Swift interopera com os padrões de tratamento de erros
> que usam a classe `NSError` no Cocoa e no Objective-C.
> Para mais informações sobre essa classe,
> veja [Tratamento de erros do Cocoa em Swift](https://developer.apple.com/documentation/swift/cocoa_design_patterns/handling_cocoa_errors_in_swift).

## Representando e lançando erros

No Swift, erros são representados por valores de tipos que estão em conformidade com o protocolo `Error`.
Esse protocolo vazio indica que um tipo pode ser usado para tratamento de erros.

Enumerações do Swift são especialmente adequadas para modelar um grupo de condições de erro relacionadas,
com valores associados que permitem comunicar informações adicionais sobre a natureza do erro.
Por exemplo, veja como você poderia representar as condições de erro de operar uma máquina de venda dentro de um jogo:

```swift
enum VendingMachineError: Error {
    case invalidSelection
    case insufficientFunds(coinsNeeded: Int)
    case outOfStock
}
```

<!--
  - test: `throw-enum-error`

  ```swifttest
  -> enum VendingMachineError: Error {
         case invalidSelection
         case insufficientFunds(coinsNeeded: Int)
         case outOfStock
     }
  ```
-->

Lançar um erro permite indicar que algo inesperado aconteceu e que o fluxo normal da execução não pode continuar.
Você usa a instrução `throw` para lançar um erro.
Por exemplo, o código a seguir lança um erro para indicar que a máquina de venda precisa de cinco moedas adicionais:

```swift
throw VendingMachineError.insufficientFunds(coinsNeeded: 5)
```

<!--
  - test: `throw-enum-error`

  ```swifttest
  -> throw VendingMachineError.insufficientFunds(coinsNeeded: 5)
  xx fatal error
  ```
-->

## Tratando erros

Quando um erro é lançado, algum trecho de código ao redor precisa ser responsável por tratá-lo:
por exemplo, corrigindo o problema, tentando uma abordagem alternativa ou informando o usuário sobre a falha.

Há quatro maneiras de tratar erros no Swift.
Você pode propagar o erro de uma função para o código que chama essa função,
tratar o erro com uma instrução `do`-`catch`,
tratá-lo como um valor optional
ou afirmar que o erro não vai ocorrer.
Cada abordagem é descrita em uma seção abaixo.

Quando uma função lança um erro, o fluxo do programa muda,
então é importante identificar rapidamente os pontos do código que podem lançar erros.
Para marcar esses pontos, escreva a palavra-chave `try` (ou a variação `try?` ou `try!`)
antes do trecho de código que chama uma função, um método ou um inicializador que pode lançar um erro.
Essas palavras-chave são descritas nas seções abaixo.

> Nota: O tratamento de erros no Swift lembra o tratamento de exceções em outras linguagens,
> com o uso das palavras-chave `try`, `catch` e `throw`.
> Diferente do tratamento de exceções em muitas linguagens,
> incluindo o Objective-C,
> o tratamento de erros no Swift não envolve desfazer a pilha de chamadas,
> um processo que pode ser caro em termos computacionais.
> Por isso, o desempenho de uma instrução `throw` é comparável ao de uma instrução `return`.

### Propagando erros com funções que lançam

Para indicar que uma função, um método ou um inicializador pode lançar um erro,
escreva a palavra-chave `throws` na declaração, depois dos parâmetros.
Uma função marcada com `throws` é chamada de *função que lança*.
Se a função especifica um tipo de retorno, escreva `throws` antes da seta de retorno (`->`).

<!--
  TODO Add discussion of throwing initializers
-->

```swift
func canThrowErrors() throws -> String

func cannotThrowErrors() -> String
```

<!--
  - test: `throwingFunctionDeclaration`

  ```swifttest
  -> func canThrowErrors() throws -> String
  >> { return "foo" }

  -> func cannotThrowErrors() -> String
  >> { return "foo" }
  ```
-->

<!--
  - test: `throwing-function-cant-overload-nonthrowing`

  ```swifttest
  -> func f() -> Int { return 10 }
  -> func f() throws -> Int { return 10 } // Error
  !$ error: invalid redeclaration of 'f()'
  !! func f() throws -> Int { return 10 } // Error
  !! ^
  !$ note: 'f()' previously declared here
  !! func f() -> Int { return 10 }
  !! ^
  ```
-->

<!--
  - test: `throwing-parameter-can-overload-nonthrowing`

  ```swifttest
  -> func f(callback: () -> Int) {}
  -> func f(callback: () throws -> Int) {} // Allowed
  ```
-->

<!--
  TODO: Add more assertions to test these behaviors
-->

<!--
  TODO: Write about the fact the above rules that govern overloading
  for throwing and nonthrowing functions.
-->

Uma função que lança propaga os erros lançados dentro dela para o escopo de onde ela é chamada.

> Nota: Somente funções que lançam podem propagar erros.
> Qualquer erro lançado dentro de uma função que não lança precisa ser tratado dentro da própria função.

No exemplo abaixo, a classe `VendingMachine` tem um método `vend(itemNamed:)` que lança um `VendingMachineError` apropriado
se o item pedido não estiver disponível, estiver esgotado
ou tiver um custo maior que o valor depositado no momento:

```swift
struct Item {
    var price: Int
    var count: Int
}

class VendingMachine {
    var inventory = [
        "Candy Bar": Item(price: 12, count: 7),
        "Chips": Item(price: 10, count: 4),
        "Pretzels": Item(price: 7, count: 11)
    ]
    var coinsDeposited = 0

    func vend(itemNamed name: String) throws {
        guard let item = inventory[name] else {
            throw VendingMachineError.invalidSelection
        }

        guard item.count > 0 else {
            throw VendingMachineError.outOfStock
        }

        guard item.price <= coinsDeposited else {
            throw VendingMachineError.insufficientFunds(coinsNeeded: item.price - coinsDeposited)
        }

        coinsDeposited -= item.price

        var newItem = item
        newItem.count -= 1
        inventory[name] = newItem

        print("Dispensing \(name)")
    }
}
```

<!--
  - test: `errorHandling`

  ```swifttest
  >> enum VendingMachineError: Error {
  >>     case invalidSelection
  >>     case insufficientFunds(coinsNeeded: Int)
  >>     case outOfStock
  >> }
  -> struct Item {
        var price: Int
        var count: Int
     }

  -> class VendingMachine {
  ->     var inventory = [
             "Candy Bar": Item(price: 12, count: 7),
             "Chips": Item(price: 10, count: 4),
             "Pretzels": Item(price: 7, count: 11)
         ]
  ->     var coinsDeposited = 0

  ->     func vend(itemNamed name: String) throws {
             guard let item = inventory[name] else {
                 throw VendingMachineError.invalidSelection
             }

             guard item.count > 0 else {
                 throw VendingMachineError.outOfStock
             }

             guard item.price <= coinsDeposited else {
                 throw VendingMachineError.insufficientFunds(coinsNeeded: item.price - coinsDeposited)
             }

             coinsDeposited -= item.price

             var newItem = item
             newItem.count -= 1
             inventory[name] = newItem

             print("Dispensing \(name)")
         }
     }
  ```
-->

A implementação do método `vend(itemNamed:)` usa instruções `guard` para sair do método logo no início
e lançar os erros apropriados se algum dos requisitos para comprar um lanche não for atendido.
Como uma instrução `throw` transfere o controle do programa imediatamente,
um item só é liberado se todos esses requisitos forem atendidos.

Como o método `vend(itemNamed:)` propaga os erros que lança,
qualquer código que chame esse método precisa tratar os erros
(com uma instrução `do`-`catch`, `try?` ou `try!`)
ou continuar propagando-os.
Por exemplo, a função `buyFavoriteSnack(person:vendingMachine:)`, do exemplo abaixo,
também é uma função que lança,
e os erros que `vend(itemNamed:)` lança sobem até o ponto em que `buyFavoriteSnack(person:vendingMachine:)` é chamada.

```swift
let favoriteSnacks = [
    "Alice": "Chips",
    "Bob": "Licorice",
    "Eve": "Pretzels",
]
func buyFavoriteSnack(person: String, vendingMachine: VendingMachine) throws {
    let snackName = favoriteSnacks[person] ?? "Candy Bar"
    try vendingMachine.vend(itemNamed: snackName)
}
```

<!--
  - test: `errorHandling`

  ```swifttest
  -> let favoriteSnacks = [
         "Alice": "Chips",
         "Bob": "Licorice",
         "Eve": "Pretzels",
     ]
  -> func buyFavoriteSnack(person: String, vendingMachine: VendingMachine) throws {
         let snackName = favoriteSnacks[person] ?? "Candy Bar"
         try vendingMachine.vend(itemNamed: snackName)
     }
  >> var v = VendingMachine()
  >> v.coinsDeposited = 100
  >> try buyFavoriteSnack(person: "Alice", vendingMachine: v)
  << Dispensing Chips
  ```
-->

Neste exemplo, a função `buyFavoriteSnack(person: vendingMachine:)` procura o lanche favorito de uma pessoa
e tenta comprá-lo para ela chamando o método `vend(itemNamed:)`.
Como o método `vend(itemNamed:)` pode lançar um erro, ele é chamado com a palavra-chave `try` na frente.

Inicializadores que lançam podem propagar erros da mesma forma que funções que lançam.
Por exemplo, o inicializador da struct `PurchasedSnack`, na listagem abaixo,
chama uma função que lança como parte do processo de inicialização
e trata os erros que encontra propagando-os para quem o chamou.

```swift
struct PurchasedSnack {
    let name: String
    init(name: String, vendingMachine: VendingMachine) throws {
        try vendingMachine.vend(itemNamed: name)
        self.name = name
    }
}
```

<!--
  - test: `errorHandling`

  ```swifttest
  -> struct PurchasedSnack {
         let name: String
         init(name: String, vendingMachine: VendingMachine) throws {
             try vendingMachine.vend(itemNamed: name)
             self.name = name
         }
     }
  >> do {
  >>     let succeeds = try PurchasedSnack(name: "Candy Bar", vendingMachine: v)
  >>     print(succeeds)
  >> } catch {
  >>     print("Threw unexpected error.")
  >> }
  << Dispensing Candy Bar
  << PurchasedSnack(name: "Candy Bar")
  >> do {
  >>     let throwsError = try PurchasedSnack(name: "Jelly Baby", vendingMachine: v)
  >>     print(throwsError)
  >> } catch {
  >>     print("Threw EXPECTED error.")
  >> }
  << Threw EXPECTED error.
  ```
-->

### Tratando erros com do-catch

Você usa uma instrução `do`-`catch` para tratar erros executando um bloco de código.
Se um erro for lançado pelo código na cláusula `do`, ele é comparado com as cláusulas `catch`
para determinar qual delas pode tratá-lo.

Esta é a forma geral de uma instrução `do`-`catch`:

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

Você escreve um padrão depois de `catch` para indicar quais erros aquela cláusula pode tratar.
Se uma cláusula `catch` não tiver padrão, ela corresponde a qualquer erro
e vincula o erro a uma constante local chamada `error`.
Para mais informações sobre correspondência de padrões,
veja <doc:Patterns>.

<!--
  TODO: Call out the reasoning why we don't let you
  consider a catch clause exhaustive by just matching
  the errors in an given enum without a general catch/default.
-->

Por exemplo, o código a seguir corresponde aos três casos da enumeração `VendingMachineError`.

```swift
var vendingMachine = VendingMachine()
vendingMachine.coinsDeposited = 8
do {
    try buyFavoriteSnack(person: "Alice", vendingMachine: vendingMachine)
    print("Success! Yum.")
} catch VendingMachineError.invalidSelection {
    print("Invalid Selection.")
} catch VendingMachineError.outOfStock {
    print("Out of Stock.")
} catch VendingMachineError.insufficientFunds(let coinsNeeded) {
    print("Insufficient funds. Please insert an additional \(coinsNeeded) coins.")
} catch {
    print("Unexpected error: \(error).")
}
// Prints "Insufficient funds. Please insert an additional 2 coins."
```

<!--
  - test: `errorHandling`

  ```swifttest
  -> var vendingMachine = VendingMachine()
  -> vendingMachine.coinsDeposited = 8
  -> do {
         try buyFavoriteSnack(person: "Alice", vendingMachine: vendingMachine)
         print("Success! Yum.")
     } catch VendingMachineError.invalidSelection {
         print("Invalid Selection.")
     } catch VendingMachineError.outOfStock {
         print("Out of Stock.")
     } catch VendingMachineError.insufficientFunds(let coinsNeeded) {
         print("Insufficient funds. Please insert an additional \(coinsNeeded) coins.")
     } catch {
         print("Unexpected error: \(error).")
     }
  <- Insufficient funds. Please insert an additional 2 coins.
  ```
-->

No exemplo acima, a função `buyFavoriteSnack(person:vendingMachine:)` é chamada em uma expressão `try`,
porque pode lançar um erro.
Se um erro for lançado, a execução passa imediatamente para as cláusulas `catch`,
que decidem se a propagação deve continuar.
Se nenhum padrão corresponder, o erro é capturado pela última cláusula `catch`
e vinculado a uma constante local `error`.
Se nenhum erro for lançado, as demais instruções do bloco `do` são executadas.

As cláusulas `catch` não precisam tratar todos os erros possíveis que o código da cláusula `do` pode lançar.
Se nenhuma das cláusulas `catch` tratar o erro, ele se propaga para o escopo ao redor.
No entanto, o erro propagado precisa ser tratado por *algum* escopo ao redor.
Em uma função que não lança, uma instrução `do`-`catch` que a envolve precisa tratar o erro.
Em uma função que lança, precisa tratar o erro uma instrução `do`-`catch` que a envolve ou quem a chamou.
Se o erro chegar ao escopo de nível superior sem ser tratado, você terá um erro de tempo de execução.

Por exemplo, o exemplo acima pode ser escrito de modo que qualquer erro que não seja um `VendingMachineError`
seja capturado pela função que a chamou:

```swift
func nourish(with item: String) throws {
    do {
        try vendingMachine.vend(itemNamed: item)
    } catch is VendingMachineError {
        print("Couldn't buy that from the vending machine.")
    }
}

do {
    try nourish(with: "Beet-Flavored Chips")
} catch {
    print("Unexpected non-vending-machine-related error: \(error)")
}
// Prints "Couldn't buy that from the vending machine."
```

<!--
  - test: `errorHandling`

  ```swifttest
  -> func nourish(with item: String) throws {
         do {
             try vendingMachine.vend(itemNamed: item)
         } catch is VendingMachineError {
             print("Couldn't buy that from the vending machine.")
         }
     }

  -> do {
         try nourish(with: "Beet-Flavored Chips")
     } catch {
         print("Unexpected non-vending-machine-related error: \(error)")
     }
  <- Couldn't buy that from the vending machine.
  ```
-->

Na função `nourish(with:)`, se `vend(itemNamed:)` lançar um erro que seja um dos casos da enumeração `VendingMachineError`,
`nourish(with:)` trata o erro imprimindo uma mensagem.
Caso contrário, `nourish(with:)` propaga o erro para o ponto em que foi chamada.
Então, o erro é capturado pela cláusula `catch` geral.

Outra forma de capturar vários erros relacionados é listá-los depois de `catch`, separados por vírgulas.
Por exemplo:

```swift
func eat(item: String) throws {
    do {
        try vendingMachine.vend(itemNamed: item)
    } catch VendingMachineError.invalidSelection, VendingMachineError.insufficientFunds, VendingMachineError.outOfStock {
        print("Invalid selection, out of stock, or not enough money.")
    }
}
```

<!--
  - test: `errorHandling`

  ```swifttest
  -> func eat(item: String) throws {
         do {
             try vendingMachine.vend(itemNamed: item)
         } catch VendingMachineError.invalidSelection, VendingMachineError.insufficientFunds, VendingMachineError.outOfStock {
             print("Invalid selection, out of stock, or not enough money.")
         }
     }
  >> do {
  >>     try eat(item: "Beet-Flavored Chips")
  >> } catch {
  >>     print("Unexpected error: \(error)")
  >> }
  << Invalid selection, out of stock, or not enough money.
  ```
-->

<!--
  FIXME the catch clause is getting indented oddly in HTML output if I hard wrap it
-->

A função `eat(item:)` lista os erros da máquina de venda que devem ser capturados,
e o texto dela corresponde aos itens dessa lista.
Se qualquer um dos três erros listados for lançado, esta cláusula `catch` os trata imprimindo uma mensagem.
Quaisquer outros erros são propagados para o escopo ao redor,
incluindo erros da máquina de venda que possam ser adicionados no futuro.

### Convertendo erros em valores optional

Você usa `try?` para tratar um erro convertendo-o em um valor optional.
Se um erro for lançado durante a avaliação da expressão `try?`, o valor da expressão é `nil`.
Por exemplo, no código a seguir `x` e `y` têm o mesmo valor e o mesmo comportamento:

```swift
func someThrowingFunction() throws -> Int {
    // ...
}

let x = try? someThrowingFunction()

let y: Int?
do {
    y = try someThrowingFunction()
} catch {
    y = nil
}
```

<!--
  - test: `optional-try`

  ```swifttest
  -> func someThrowingFunction() throws -> Int {
        // ...
  >>    return 40
  -> }

  -> let x = try? someThrowingFunction()
  >> print(x as Any)
  << Optional(40)

  -> let y: Int?
     do {
         y = try someThrowingFunction()
     } catch {
         y = nil
     }
  >> print(y as Any)
  << Optional(40)
  ```
-->

Se `someThrowingFunction()` lançar um erro, o valor de `x` e de `y` é `nil`.
Caso contrário, o valor de `x` e de `y` é o valor que a função retornou.
Observe que `x` e `y` são optionals do tipo que `someThrowingFunction()` retorna.
Aqui a função retorna um inteiro, então `x` e `y` são optionals de inteiros.

Usar `try?` permite escrever código de tratamento de erros conciso quando você quer tratar todos os erros da mesma forma.
Por exemplo, o código a seguir usa várias abordagens para buscar dados
ou retorna `nil` se todas elas falharem.

```swift
func fetchData() -> Data? {
    if let data = try? fetchDataFromDisk() { return data }
    if let data = try? fetchDataFromServer() { return data }
    return nil
}
```

<!--
  - test: `optional-try-cached-data`

  ```swifttest
  >> struct Data {}
  >> func fetchDataFromDisk() throws -> Data { return Data() }
  >> func fetchDataFromServer() throws -> Data { return Data() }
  -> func fetchData() -> Data? {
         if let data = try? fetchDataFromDisk() { return data }
         if let data = try? fetchDataFromServer() { return data }
         return nil
     }
  ```
-->

### Desativando a propagação de erros

Às vezes você sabe que uma função ou um método que lança não vai, na prática, lançar um erro em tempo de execução.
Nessas ocasiões, você pode escrever `try!` antes da expressão para desativar a propagação de erros,
envolvendo a chamada em uma verificação de tempo de execução de que nenhum erro será lançado.
Se um erro for de fato lançado, você terá um erro de tempo de execução.

Por exemplo, o código a seguir usa uma função `loadImage(atPath:)`,
que carrega o recurso de imagem em um caminho dado
ou lança um erro se a imagem não puder ser carregada.
Neste caso, como a imagem é distribuída com o aplicativo,
nenhum erro será lançado em tempo de execução,
então é apropriado desativar a propagação de erros.

```swift
let photo = try! loadImage(atPath: "./Resources/John Appleseed.jpg")
```

<!--
  - test: `forceTryStatement`

  ```swifttest
  >> struct Image {}
  >> func loadImage(atPath path: String) throws -> Image {
  >>     return Image()
  >> }
  -> let photo = try! loadImage(atPath: "./Resources/John Appleseed.jpg")
  ```
-->

## Especificando o tipo de erro

Todos os exemplos acima usam o tipo mais comum de tratamento de erros,
em que os erros que o seu código lança podem ser valores de qualquer tipo que esteja em conformidade com o protocolo `Error`.
Essa abordagem reflete a realidade de que você não sabe antecipadamente todos os erros que podem acontecer
enquanto o código roda, especialmente ao propagar erros lançados em outro lugar.
Ela também reflete o fato de que os erros mudam com o tempo.
Novas versões de uma biblioteca, incluindo bibliotecas usadas pelas suas dependências,
podem lançar erros novos, e a complexidade das configurações reais dos usuários
pode expor falhas que não apareceram durante o desenvolvimento ou os testes.
O código de tratamento de erros dos exemplos acima sempre inclui um caso padrão
para tratar erros que não têm uma cláusula `catch` específica.

A maioria do código Swift não especifica o tipo dos erros que lança.
No entanto, você pode limitar o código a lançar erros de apenas um tipo específico nos seguintes casos especiais:

- Ao executar código em um sistema embarcado que não aceita alocação dinâmica de memória.
  Lançar uma instância de `any Error` ou de outro tipo de protocolo empacotado exige alocar memória em tempo de execução
  para armazenar o erro.
  Já lançar um erro de um tipo específico permite ao Swift evitar a alocação na heap para os erros.

- Quando os erros são um detalhe de implementação de alguma unidade de código, como uma biblioteca,
  e não fazem parte da interface desse código.
  Como os erros vêm somente da biblioteca, e não de outras dependências ou dos clientes dela,
  você pode fazer uma lista exaustiva de todas as falhas possíveis.
  E, como esses erros são um detalhe de implementação da biblioteca, eles são sempre tratados dentro dela.

- Em código que apenas propaga erros descritos por parâmetros genéricos,
  como uma função que recebe um argumento closure e propaga quaisquer erros desse closure.
  Para uma comparação entre propagar um tipo de erro específico e usar `rethrows`,
  veja <doc:Declarations#Rethrowing-Functions-and-Methods>.

Por exemplo, considere um código que resume avaliações e usa o seguinte tipo de erro:

```swift
enum StatisticsError: Error {
    case noRatings
    case invalidRating(Int)
}
```

Para especificar que uma função lança apenas valores de `StatisticsError` como erros,
você escreve `throws(StatisticsError)` em vez de só `throws` ao declarar a função.
Essa sintaxe também é chamada de *typed throws*,
porque você escreve o tipo do erro depois de `throws` na declaração.
Por exemplo, a função abaixo lança valores de `StatisticsError` como erros.

```swift
func summarize(_ ratings: [Int]) throws(StatisticsError) {
    guard !ratings.isEmpty else { throw .noRatings }

    var counts = [1: 0, 2: 0, 3: 0]
    for rating in ratings {
        guard rating > 0 && rating <= 3 else { throw .invalidRating(rating) }
        counts[rating]! += 1
    }

    print("*", counts[1]!, "-- **", counts[2]!, "-- ***", counts[3]!)
}
```

No código acima, a função `summarize(_:)` resume uma lista de avaliações em uma escala de 1 a 3.
Essa função lança uma instância de `StatisticsError` se a entrada não for válida.
Os dois lugares do código acima que lançam um erro omitem o tipo do erro,
porque o tipo de erro da função já está definido.
Você pode usar a forma abreviada `throw .noRatings`,
em vez de escrever `throw StatisticsError.noRatings`,
ao lançar um erro em uma função assim.

Quando você escreve um tipo de erro específico no início da função, o Swift verifica se você não lança nenhum outro erro.
Por exemplo, se você tentasse usar `VendingMachineError`, dos exemplos anteriores deste capítulo,
na função `summarize(_:)` acima, esse código produziria um erro em tempo de compilação.

Você pode chamar uma função que usa typed throws dentro de uma função que lança comum:

```swift
func someThrowingFunction() throws {
    let ratings = [1, 2, 3, 2, 2, 1]
    try summarize(ratings)
}
```

O código acima não especifica um tipo de erro para `someThrowingFunction()`,
então ela lança `any Error`.
Você também poderia escrever o tipo de erro explicitamente como `throws(any Error)`;
o código abaixo é equivalente ao código acima:

```swift
func someThrowingFunction() throws(any Error) {
    let ratings = [1, 2, 3, 2, 2, 1]
    try summarize(ratings)
}
```

Neste código, `someThrowingFunction()` propaga quaisquer erros que `summarize(_:)` lança.
Os erros de `summarize(_:)` são sempre valores de `StatisticsError`,
que também é um erro válido para `someThrowingFunction()` lançar.

Assim como você pode escrever uma função que nunca retorna, com tipo de retorno `Never`,
você pode escrever uma função que nunca lança, com `throws(Never)`:

```swift
func nonThrowingFunction() throws(Never) {
  // ...
}
```
Essa função não pode lançar erros, porque é impossível criar um valor do tipo `Never` para lançar.

Além de especificar o tipo de erro de uma função,
você também pode escrever um tipo de erro específico para uma instrução `do`-`catch`.
Por exemplo:

```swift
let ratings = []
do throws(StatisticsError) {
    try summarize(ratings)
} catch {
    switch error {
    case .noRatings:
        print("No ratings available")
    case .invalidRating(let rating):
        print("Invalid rating: \(rating)")
    }
}
// Prints "No ratings available".
```

Neste código, escrever `do throws(StatisticsError)` indica que a instrução `do`-`catch`
lança valores de `StatisticsError` como erros.
Como em outras instruções `do`-`catch`, a cláusula `catch` pode tratar todos os erros possíveis
ou propagar os erros não tratados para algum escopo ao redor tratar.
Este código trata todos os erros, usando uma instrução `switch` com um caso para cada valor da enumeração.
Como outras cláusulas `catch` sem padrão, esta corresponde a qualquer erro
e vincula o erro a uma constante local chamada `error`.
Como a instrução `do`-`catch` lança valores de `StatisticsError`,
`error` é um valor do tipo `StatisticsError`.

A cláusula `catch` acima usa uma instrução `switch` para corresponder e tratar cada erro possível.
Se você tentasse adicionar um novo caso a `StatisticsError` sem atualizar o código de tratamento de erros,
o Swift daria um erro, porque a instrução `switch` deixaria de ser exaustiva.
Para uma biblioteca que captura todos os próprios erros, você poderia usar essa abordagem
para garantir que qualquer erro novo ganhe código correspondente para tratá-lo.

Se uma função ou um bloco `do` lançar erros de apenas um tipo, o Swift infere que esse código está usando typed throws.
Com essa sintaxe mais curta, você poderia escrever o exemplo de `do`-`catch` acima da seguinte forma:

```swift
let ratings = []
do {
    try summarize(ratings)
} catch {
    switch error {
    case .noRatings:
        print("No ratings available")
    case .invalidRating(let rating):
        print("Invalid rating: \(rating)")
    }
}
// Prints "No ratings available".
```

Mesmo que o bloco `do`-`catch` acima não especifique o tipo de erro que lança,
o Swift infere que ele lança `StatisticsError`.
Você pode escrever explicitamente `throws(any Error)` para impedir que o Swift infira typed throws.

## Especificando ações de limpeza

Você usa uma instrução `defer` para executar um conjunto de instruções logo antes de a execução deixar o bloco de código atual.
Essa instrução permite fazer qualquer limpeza necessária, que deve acontecer independentemente de *como* a execução deixa o bloco atual:
seja porque um erro foi lançado, seja por causa de uma instrução como `return` ou `break`.
Por exemplo, você pode usar `defer` para garantir que descritores de arquivo sejam fechados
e que memória alocada manualmente seja liberada.

Uma instrução `defer` adia a execução até que o escopo atual seja encerrado.
Essa instrução é formada pela palavra-chave `defer` e pelas instruções que devem ser executadas depois.
As instruções adiadas não podem conter código que transfira o controle para fora delas,
como uma instrução `break` ou `return`, nem lançar um erro.
As ações adiadas são executadas na ordem inversa da que foram escritas no código-fonte.
Ou seja, o código da primeira instrução `defer` é executado por último,
o da segunda é executado penúltimo, e assim por diante.
A última instrução `defer` na ordem do código-fonte é executada primeiro.

```swift
func processFile(filename: String) throws {
    if exists(filename) {
        let file = open(filename)
        defer {
            close(file)
        }
        while let line = try file.readline() {
            // Work with the file.
        }
        // close(file) is called here, at the end of the scope.
    }
}
```

<!--
  - test: `defer`

  ```swifttest
  >> func exists(_ file: String) -> Bool { return true }
  >> struct File {
  >>    func readline() throws -> String? { return nil }
  >> }
  >> func open(_ file: String) -> File { return File() }
  >> func close(_ fileHandle: File) {}
  -> func processFile(filename: String) throws {
        if exists(filename) {
           let file = open(filename)
           defer {
              close(file)
           }
           while let line = try file.readline() {
              // Work with the file.
  >>          print(line)
           }
           // close(file) is called here, at the end of the scope.
        }
     }
  ```
-->

O exemplo acima usa uma instrução `defer` para garantir que a função `open(_:)`
tenha uma chamada correspondente a `close(_:)`.

Você pode usar `defer` mesmo quando não há código de tratamento de erros envolvido.
Para mais informações, veja <doc:ControlFlow#Deferred-Actions>.

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->

<!-- ia-translate: true -->
