# Closures

Agrupe código que é executado em conjunto, sem criar uma função nomeada.

*Closures* são blocos de funcionalidade autocontidos
que podem ser passados e usados no seu código.
Closures em Swift são semelhantes
a closures, funções anônimas, lambdas e blocos
de outras linguagens de programação.

Closures podem capturar e armazenar referências a quaisquer constantes e variáveis
do contexto em que são definidas.
Isso é conhecido como *fechar sobre* essas constantes e variáveis.
O Swift cuida de todo o gerenciamento de memória dessa captura para você.

> Nota: Não se preocupe se você não estiver familiarizado com o conceito de captura.
> Ele é explicado em detalhes abaixo, em <doc:Closures#Capturando-valores>.

Funções globais e aninhadas, como apresentadas em <doc:Functions>,
são, na verdade, casos especiais de closures.
Closures assumem uma de três formas:

- Funções globais são closures que têm nome
  e não capturam nenhum valor.
- Funções aninhadas são closures que têm nome
  e podem capturar valores da função que as envolve.
- Expressões de closure são closures sem nome, escritas em uma sintaxe leve
  e que podem capturar valores do contexto ao redor.

As expressões de closure do Swift têm um estilo limpo e claro,
com otimizações que incentivam uma sintaxe breve e sem excesso de ruído em cenários comuns.
Essas otimizações incluem:

- Inferência dos tipos dos parâmetros e do valor de retorno pelo contexto
- Retorno implícito de closures de expressão única
- Nomes abreviados de argumento
- Sintaxe de *trailing closure*

## Expressões de closure

Funções aninhadas, como apresentadas em <doc:Functions#Funções-aninhadas>,
são uma forma prática de nomear e definir blocos de código autocontidos
como parte de uma função maior.
No entanto, às vezes é útil escrever versões mais curtas de construções semelhantes a funções
sem uma declaração completa e sem nome.
Isso é especialmente verdadeiro quando você trabalha com funções ou métodos que recebem funções
como um ou mais de seus argumentos.

*Expressões de closure* são uma forma de escrever closures inline com uma sintaxe breve e objetiva.
Elas oferecem várias otimizações de sintaxe
para escrever closures de forma reduzida, sem perda de clareza ou de intenção.
Os exemplos de expressões de closure abaixo ilustram essas otimizações
refinando um único exemplo do método `sorted(by:)` em várias iterações,
cada uma expressando a mesma funcionalidade de forma mais sucinta.

### O método `sorted(by:)`

A biblioteca padrão do Swift fornece um método chamado `sorted(by:)`,
que ordena um array de valores de um tipo conhecido,
com base na saída de uma closure de ordenação que você fornece.
Ao concluir o processo de ordenação,
o método `sorted(by:)` retorna um novo array do mesmo tipo e tamanho do anterior,
com os elementos na ordem correta.
O array original não é modificado pelo método `sorted(by:)`.

Os exemplos de expressão de closure abaixo usam o método `sorted(by:)`
para ordenar um array de valores `String` em ordem alfabética inversa.
Aqui está o array inicial a ser ordenado:

```swift
let names = ["Chris", "Alex", "Ewa", "Barry", "Daniella"]
```

<!--
  - test: `closureSyntax`

  ```swifttest
  -> let names = ["Chris", "Alex", "Ewa", "Barry", "Daniella"]
  ```
-->

O método `sorted(by:)` aceita uma closure que recebe dois argumentos
do mesmo tipo do conteúdo do array,
e retorna um valor `Bool` que indica se o primeiro valor deve aparecer
antes ou depois do segundo valor depois de ordenados.
A closure de ordenação precisa retornar `true`
se o primeiro valor deve aparecer *antes* do segundo valor,
e `false` caso contrário.

Este exemplo ordena um array de valores `String`,
então a closure de ordenação precisa ser uma função do tipo `(String, String) -> Bool`.

Uma forma de fornecer a closure de ordenação é escrever uma função normal do tipo correto
e passá-la como argumento para o método `sorted(by:)`:

```swift
func backward(_ s1: String, _ s2: String) -> Bool {
    return s1 > s2
}
var reversedNames = names.sorted(by: backward)
// reversedNames is equal to ["Ewa", "Daniella", "Chris", "Barry", "Alex"]
```

<!--
  - test: `closureSyntax`

  ```swifttest
  -> func backward(_ s1: String, _ s2: String) -> Bool {
        return s1 > s2
     }
  -> var reversedNames = names.sorted(by: backward)
  /> reversedNames is equal to \(reversedNames)
  </ reversedNames is equal to ["Ewa", "Daniella", "Chris", "Barry", "Alex"]
  ```
-->

Se a primeira string (`s1`) for maior que a segunda string (`s2`),
a função `backward(_:_:)` retornará `true`,
indicando que `s1` deve aparecer antes de `s2` no array ordenado.
Para caracteres em strings,
“maior que” significa “aparece depois no alfabeto que”.
Isso quer dizer que a letra `"B"` é “maior que” a letra `"A"`,
e a string `"Tom"` é maior que a string `"Tim"`.
Isso resulta em uma ordenação alfabética inversa,
com `"Barry"` posicionado antes de `"Alex"`, e assim por diante.

No entanto, essa é uma forma bem prolixa de escrever
o que é essencialmente uma função de expressão única (`a > b`).
Neste exemplo, seria preferível escrever a closure de ordenação inline,
usando a sintaxe de expressão de closure.

### Sintaxe de expressão de closure

A sintaxe de expressão de closure tem a seguinte forma geral:

```swift
{ (<#parameters#>) -> <#return type#> in
   <#statements#>
}
```

Os *parâmetros* na sintaxe de expressão de closure
podem ser parâmetros in-out,
mas não podem ter valor padrão.
Parâmetros variádicos podem ser usados se você nomear o parâmetro variádico.
Tuplas também podem ser usadas como tipos de parâmetro e de retorno.

O exemplo abaixo mostra uma versão em expressão de closure da função `backward(_:_:)` acima:

```swift
reversedNames = names.sorted(by: { (s1: String, s2: String) -> Bool in
    return s1 > s2
})
```

<!--
  - test: `closureSyntax`

  ```swifttest
  -> reversedNames = names.sorted(by: { (s1: String, s2: String) -> Bool in
        return s1 > s2
     })
  >> assert(reversedNames == ["Ewa", "Daniella", "Chris", "Barry", "Alex"])
  ```
-->

Observe que a declaração de parâmetros e do tipo de retorno desta closure inline
é idêntica à declaração da função `backward(_:_:)`.
Nos dois casos, é escrita como `(s1: String, s2: String) -> Bool`.
No entanto, na expressão de closure inline,
os parâmetros e o tipo de retorno são escritos *dentro* das chaves,
e não fora delas.

O início do corpo da closure é indicado pela palavra-chave `in`.
Ela sinaliza que
a definição dos parâmetros e do tipo de retorno da closure terminou,
e que o corpo da closure está prestes a começar.

Como o corpo da closure é tão curto,
ele pode até ser escrito em uma única linha:

```swift
reversedNames = names.sorted(by: { (s1: String, s2: String) -> Bool in return s1 > s2 } )
```

<!--
  - test: `closureSyntax`

  ```swifttest
  -> reversedNames = names.sorted(by: { (s1: String, s2: String) -> Bool in return s1 > s2 } )
  >> assert(reversedNames == ["Ewa", "Daniella", "Chris", "Barry", "Alex"])
  ```
-->

Isso mostra que a chamada geral ao método `sorted(by:)` continua a mesma.
Um par de parênteses ainda envolve todo o argumento do método.
Só que esse argumento agora é uma closure inline.

### Inferência de tipo pelo contexto

Como a closure de ordenação é passada como argumento de um método,
o Swift consegue inferir os tipos de seus parâmetros
e o tipo do valor que ela retorna.
O método `sorted(by:)` é chamado em um array de strings,
então seu argumento precisa ser uma função do tipo `(String, String) -> Bool`.
Isso significa que os tipos `(String, String)` e `Bool` não precisam ser escritos
como parte da definição da expressão de closure.
Como todos os tipos podem ser inferidos,
a seta de retorno (`->`) e os parênteses em volta dos nomes dos parâmetros
também podem ser omitidos:

```swift
reversedNames = names.sorted(by: { s1, s2 in return s1 > s2 } )
```

<!--
  - test: `closureSyntax`

  ```swifttest
  -> reversedNames = names.sorted(by: { s1, s2 in return s1 > s2 } )
  >> assert(reversedNames == ["Ewa", "Daniella", "Chris", "Barry", "Alex"])
  ```
-->

É sempre possível inferir os tipos dos parâmetros e o tipo de retorno
ao passar uma closure para uma função ou método como expressão de closure inline.
Por isso, você nunca precisa escrever uma closure inline na sua forma mais completa
quando ela é usada como argumento de função ou método.

Mesmo assim, você ainda pode deixar os tipos explícitos se quiser,
e isso é recomendado quando evita ambiguidade para quem lê seu código.
No caso do método `sorted(by:)`,
a finalidade da closure fica clara pelo fato de que a ordenação está acontecendo,
e é seguro que o leitor presuma que
a closure provavelmente trabalha com valores `String`,
já que ela ajuda na ordenação de um array de strings.

### Retorno implícito de closures de expressão única

Closures de expressão única podem retornar implicitamente o resultado da sua única expressão,
omitindo a palavra-chave `return` da declaração,
como nesta versão do exemplo anterior:

```swift
reversedNames = names.sorted(by: { s1, s2 in s1 > s2 } )
```

<!--
  - test: `closureSyntax`

  ```swifttest
  -> reversedNames = names.sorted(by: { s1, s2 in s1 > s2 } )
  >> assert(reversedNames == ["Ewa", "Daniella", "Chris", "Barry", "Alex"])
  ```
-->

Aqui, o tipo de função do argumento do método `sorted(by:)`
deixa claro que a closure precisa retornar um valor `Bool`.
Como o corpo da closure contém uma única expressão (`s1 > s2`)
que retorna um valor `Bool`,
não há ambiguidade, e a palavra-chave `return` pode ser omitida.

### Nomes abreviados de argumento

O Swift fornece automaticamente nomes abreviados de argumento para closures inline,
que podem ser usados para se referir aos valores dos argumentos da closure
pelos nomes `$0`, `$1`, `$2` e assim por diante.

Se você usar esses nomes abreviados de argumento dentro da sua expressão de closure,
pode omitir a lista de argumentos da definição da closure.
O tipo dos nomes abreviados de argumento
é inferido do tipo de função esperado,
e o maior número de argumento abreviado que você usar
determina quantos argumentos a closure recebe.
A palavra-chave `in` também pode ser omitida,
porque a expressão de closure é formada inteiramente pelo seu corpo:

```swift
reversedNames = names.sorted(by: { $0 > $1 } )
```

<!--
  - test: `closureSyntax`

  ```swifttest
  -> reversedNames = names.sorted(by: { $0 > $1 } )
  >> assert(reversedNames == ["Ewa", "Daniella", "Chris", "Barry", "Alex"])
  ```
-->

Aqui, `$0` e `$1` se referem ao primeiro e ao segundo argumentos `String` da closure.
Como `$1` é o argumento abreviado de maior número,
entende-se que a closure recebe dois argumentos.
Como a função `sorted(by:)` aqui espera uma closure
cujos argumentos são ambos strings,
os argumentos abreviados `$0` e `$1` são ambos do tipo `String`.

<!--
  - test: `closure-syntax-arity-inference`

  ```swifttest
  >> let a: [String: String] = [:]
  >> var b: [String: String] = [:]
  >> b.merge(a, uniquingKeysWith: { $1 })
  >> b.merge(a, uniquingKeysWith: { $0 })
  !$ error: contextual closure type '(String, String) throws -> String' expects 2 arguments, but 1 was used in closure body
  !! b.merge(a, uniquingKeysWith: { $0 })
  !! ^
  ```
-->

### Métodos de operador

Existe, na verdade, uma forma ainda *mais* curta de escrever a expressão de closure acima.
O tipo `String` do Swift define sua implementação específica para strings
do operador de maior que (`>`)
como um método que tem dois parâmetros do tipo `String`
e retorna um valor do tipo `Bool`.
Isso corresponde exatamente ao tipo de método exigido pelo método `sorted(by:)`.
Por isso, você pode simplesmente passar o operador de maior que,
e o Swift vai inferir que você quer usar a implementação específica para strings:

```swift
reversedNames = names.sorted(by: >)
```

<!--
  - test: `closureSyntax`

  ```swifttest
  -> reversedNames = names.sorted(by: >)
  >> assert(reversedNames == ["Ewa", "Daniella", "Chris", "Barry", "Alex"])
  ```
-->

Para saber mais sobre métodos de operador, veja <doc:AdvancedOperators#Operator-Methods>.

## Trailing closures

Se você precisar passar uma expressão de closure para uma função como último argumento dela
e a expressão de closure for longa,
pode ser útil escrevê-la como uma *trailing closure*.
Você escreve a trailing closure depois dos parênteses da chamada da função,
mesmo que ela continue sendo um argumento da função.
Ao usar a sintaxe de trailing closure,
você não escreve o rótulo do argumento da primeira closure
como parte da chamada da função.
Uma chamada de função pode incluir várias trailing closures;
no entanto, os primeiros exemplos abaixo usam uma única trailing closure.

```swift
func someFunctionThatTakesAClosure(closure: () -> Void) {
    // function body goes here
}

// Here's how you call this function without using a trailing closure:

someFunctionThatTakesAClosure(closure: {
    // closure's body goes here
})

// Here's how you call this function with a trailing closure instead:

someFunctionThatTakesAClosure() {
    // trailing closure's body goes here
}
```

<!--
  - test: `closureSyntax`

  ```swifttest
  -> func someFunctionThatTakesAClosure(closure: () -> Void) {
        // function body goes here
     }

  -> // Here's how you call this function without using a trailing closure:

  -> someFunctionThatTakesAClosure(closure: {
        // closure's body goes here
     })

  -> // Here's how you call this function with a trailing closure instead:

  -> someFunctionThatTakesAClosure() {
        // trailing closure's body goes here
     }
  ```
-->

A closure de ordenação de strings da seção <doc:Closures#Sintaxe-de-expressão-de-closure> acima
pode ser escrita fora dos parênteses do método `sorted(by:)` como uma trailing closure:

```swift
reversedNames = names.sorted() { $0 > $1 }
```

<!--
  - test: `closureSyntax`

  ```swifttest
  -> reversedNames = names.sorted() { $0 > $1 }
  >> assert(reversedNames == ["Ewa", "Daniella", "Chris", "Barry", "Alex"])
  ```
-->

Se uma expressão de closure for o único argumento de uma função ou método
e você fornecer essa expressão como trailing closure,
não precisa escrever um par de parênteses `()`
depois do nome da função ou método ao chamá-la:

```swift
reversedNames = names.sorted { $0 > $1 }
```

<!--
  - test: `closureSyntax`

  ```swifttest
  -> reversedNames = names.sorted { $0 > $1 }
  >> assert(reversedNames == ["Ewa", "Daniella", "Chris", "Barry", "Alex"])
  ```
-->

Trailing closures são mais úteis quando a closure é longa o suficiente
para que não seja possível escrevê-la inline em uma única linha.
Por exemplo, o tipo `Array` do Swift tem um método `map(_:)`,
que recebe uma expressão de closure como seu único argumento.
A closure é chamada uma vez para cada item do array,
e retorna um valor mapeado alternativo (possivelmente de outro tipo) para esse item.
Você especifica
a natureza do mapeamento e o tipo do valor retornado
escrevendo o código na closure que passa para `map(_:)`.

Depois de aplicar a closure fornecida a cada elemento do array,
o método `map(_:)` retorna um novo array com todos os novos valores mapeados,
na mesma ordem dos valores correspondentes no array original.

Veja como usar o método `map(_:)` com uma trailing closure
para converter um array de valores `Int` em um array de valores `String`.
O array `[16, 58, 510]` é usado para criar o novo array
`["OneSix", "FiveEight", "FiveOneZero"]`:

```swift
let digitNames = [
    0: "Zero", 1: "One", 2: "Two",   3: "Three", 4: "Four",
    5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"
]
let numbers = [16, 58, 510]
```

<!--
  - test: `arrayMap`

  ```swifttest
  -> let digitNames = [
        0: "Zero", 1: "One", 2: "Two",   3: "Three", 4: "Four",
        5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"
     ]
  -> let numbers = [16, 58, 510]
  ```
-->

O código acima cria um dicionário de correspondências entre
os dígitos inteiros e as versões em inglês dos seus nomes.
Ele também define um array de inteiros, pronto para ser convertido em strings.

Agora você pode usar o array `numbers` para criar um array de valores `String`,
passando uma expressão de closure para o método `map(_:)` do array como trailing closure:

```swift
let strings = numbers.map { (number) -> String in
    var number = number
    var output = ""
    repeat {
        output = digitNames[number % 10]! + output
        number /= 10
    } while number > 0
    return output
}
// strings is inferred to be of type [String]
// its value is ["OneSix", "FiveEight", "FiveOneZero"]
```

<!--
  - test: `arrayMap`

  ```swifttest
  -> let strings = numbers.map { (number) -> String in
        var number = number
        var output = ""
        repeat {
           output = digitNames[number % 10]! + output
           number /= 10
        } while number > 0
        return output
     }
  // strings is inferred to be of type [String]
  /> its value is [\"\(strings[0])\", \"\(strings[1])\", \"\(strings[2])\"]
  </ its value is ["OneSix", "FiveEight", "FiveOneZero"]
  ```
-->

O método `map(_:)` chama a expressão de closure uma vez para cada item do array.
Você não precisa especificar o tipo do parâmetro de entrada da closure, `number`,
porque o tipo pode ser inferido dos valores do array a ser mapeado.

Neste exemplo,
a variável `number` é inicializada com o valor do parâmetro `number` da closure,
para que o valor possa ser modificado dentro do corpo da closure.
(Os parâmetros de funções e closures são sempre constantes.)
A expressão de closure também especifica um tipo de retorno `String`,
para indicar o tipo que será armazenado no array de saída mapeado.

A expressão de closure monta uma string chamada `output` a cada vez que é chamada.
Ela calcula o último dígito de `number` usando o operador de resto (`number % 10`),
e usa esse dígito para buscar uma string apropriada no dicionário `digitNames`.
A closure pode ser usada para criar uma representação em string de qualquer inteiro maior que zero.

> Nota: A chamada à subscript do dicionário `digitNames`
> é seguida de um ponto de exclamação (`!`),
> porque subscripts de dicionário retornam um valor opcional
> para indicar que a busca pode falhar se a chave não existir.
> No exemplo acima, é garantido que `number % 10`
> sempre será uma chave válida para o dicionário `digitNames`,
> por isso um ponto de exclamação é usado para forçar o unwrap do valor `String`
> armazenado no retorno opcional da subscript.

A string obtida do dicionário `digitNames`
é adicionada no *início* de `output`,
construindo efetivamente uma versão em string do número de trás para frente.
(A expressão `number % 10` resulta em
`6` para `16`, `8` para `58` e `0` para `510`.)

Em seguida, a variável `number` é dividida por `10`.
Como é um inteiro, o resultado é arredondado para baixo na divisão,
então `16` vira `1`, `58` vira `5` e `510` vira `51`.

O processo se repete até que `number` seja igual a `0`,
momento em que a closure retorna a string `output`,
e o método `map(_:)` a adiciona ao array de saída.

O uso da sintaxe de trailing closure no exemplo acima
encapsula de forma organizada a funcionalidade da closure
logo depois da função que ela auxilia,
sem precisar envolver toda a closure entre os parênteses externos
do método `map(_:)`.

Se uma função recebe várias closures,
você omite o rótulo do argumento da primeira trailing closure
e rotula as trailing closures restantes.
Por exemplo,
a função abaixo carrega uma foto para uma galeria:

```swift
func loadPicture(from server: Server, completion: (Picture) -> Void, onFailure: () -> Void) {
    if let picture = download("photo.jpg", from: server) {
        completion(picture)
    } else {
        onFailure()
    }
}
```

<!--
  - test: `multiple-trailing-closures`

  ```swifttest
  >> struct Server { }
  >> struct Picture { }
  >> func download(_ path: String, from server: Server) -> Picture? {
  >>     return Picture()
  >> }
  -> func loadPicture(from server: Server, completion: (Picture) -> Void, onFailure: () -> Void) {
         if let picture = download("photo.jpg", from: server) {
             completion(picture)
         } else {
             onFailure()
         }
     }
  ```
-->

Ao chamar essa função para carregar uma foto,
você fornece duas closures.
A primeira closure é um completion handler
que exibe a foto depois de um download bem-sucedido.
A segunda closure é um handler de erro
que exibe um erro para o usuário.

```swift
loadPicture(from: someServer) { picture in
    someView.currentPicture = picture
} onFailure: {
    print("Couldn't download the next picture.")
}
```

<!--
  - test: `multiple-trailing-closures`

  ```swifttest
  >> struct View {
  >>    var currentPicture = Picture() { didSet { print("Changed picture") } }
  >> }
  >> var someView = View()
  >> let someServer = Server()
  -> loadPicture(from: someServer) { picture in
         someView.currentPicture = picture
     } onFailure: {
         print("Couldn't download the next picture.")
     }
  << Changed picture
  ```
-->

Neste exemplo,
a função `loadPicture(from:completion:onFailure:)` envia sua tarefa de rede para o segundo plano
e chama um dos dois completion handlers quando a tarefa de rede termina.
Escrever a função dessa forma permite separar com clareza o código
responsável por tratar uma falha de rede
do código que atualiza a interface depois de um download bem-sucedido,
em vez de usar apenas uma closure que trata as duas situações.

> Nota: Completion handlers podem ficar difíceis de ler,
> especialmente quando é preciso aninhar vários handlers.
> Uma abordagem alternativa é usar código assíncrono,
> como descrito em <doc:Concurrency>.

## Capturando valores

Uma closure pode *capturar* constantes e variáveis
do contexto ao redor em que é definida.
A closure pode então se referir e modificar
os valores dessas constantes e variáveis dentro do seu corpo,
mesmo que o escopo original que definiu as constantes e variáveis não exista mais.

No Swift, a forma mais simples de closure que pode capturar valores é uma função aninhada,
escrita dentro do corpo de outra função.
Uma função aninhada pode capturar qualquer um dos argumentos da função externa
e também qualquer constante ou variável definida dentro da função externa.

Aqui está um exemplo de uma função chamada `makeIncrementer`,
que contém uma função aninhada chamada `incrementer`.
A função aninhada `incrementer()` captura dois valores,
`runningTotal` e `amount`,
do contexto ao redor.
Depois de capturar esses valores,
`incrementer` é retornada por `makeIncrementer` como uma closure
que incrementa `runningTotal` em `amount` cada vez que é chamada.

```swift
func makeIncrementer(forIncrement amount: Int) -> () -> Int {
    var runningTotal = 0
    func incrementer() -> Int {
        runningTotal += amount
        return runningTotal
    }
    return incrementer
}
```

<!--
  - test: `closures`

  ```swifttest
  -> func makeIncrementer(forIncrement amount: Int) -> () -> Int {
        var runningTotal = 0
        func incrementer() -> Int {
           runningTotal += amount
           return runningTotal
        }
        return incrementer
     }
  ```
-->

O tipo de retorno de `makeIncrementer` é `() -> Int`.
Isso significa que ela retorna uma *função*, e não um valor simples.
A função que ela retorna não tem parâmetros
e retorna um valor `Int` cada vez que é chamada.
Para saber como funções podem retornar outras funções,
veja <doc:Functions#Tipos-de-função-como-tipos-de-retorno>.

A função `makeIncrementer(forIncrement:)` define uma variável inteira chamada `runningTotal`,
para armazenar o total acumulado atual do incrementador que será retornado.
Essa variável é inicializada com o valor `0`.

A função `makeIncrementer(forIncrement:)` tem um único parâmetro `Int`
com o rótulo de argumento `forIncrement` e o nome de parâmetro `amount`.
O valor do argumento passado a esse parâmetro especifica
de quanto `runningTotal` deve ser incrementado
cada vez que a função incrementadora retornada é chamada.
A função `makeIncrementer` define uma função aninhada chamada `incrementer`,
que faz o incremento de fato.
Essa função simplesmente soma `amount` a `runningTotal` e retorna o resultado.

Considerada isoladamente,
a função aninhada `incrementer()` pode parecer incomum:

```swift
func incrementer() -> Int {
    runningTotal += amount
    return runningTotal
}
```

<!--
  - test: `closuresPullout`

  ```swifttest
  -> func incrementer() -> Int {
  >>    var runningTotal = 0
  >>    let amount = 1
        runningTotal += amount
        return runningTotal
     }
  ```
-->

A função `incrementer()` não tem parâmetros,
mas se refere a `runningTotal` e `amount` dentro do corpo da função.
Ela faz isso capturando uma *referência* a `runningTotal` e `amount`
da função externa e usando essas referências dentro do seu próprio corpo.
Capturar por referência garante que `runningTotal` e `amount` não desapareçam
quando a chamada a `makeIncrementer` terminar,
e também garante que `runningTotal` esteja disponível
na próxima vez que a função `incrementer` for chamada.

> Nota: Como otimização,
> o Swift pode, em vez disso, capturar e armazenar uma *cópia* de um valor
> se esse valor não for modificado por uma closure,
> e se o valor não for modificado depois que a closure é criada.
>
> O Swift também cuida de todo o gerenciamento de memória envolvido no descarte de
> variáveis quando elas não são mais necessárias.

Veja um exemplo de `makeIncrementer` em funcionamento:

```swift
let incrementByTen = makeIncrementer(forIncrement: 10)
```

<!--
  - test: `closures`

  ```swifttest
  -> let incrementByTen = makeIncrementer(forIncrement: 10)
  ```
-->

Este exemplo define uma constante chamada `incrementByTen`
para se referir a uma função incrementadora que soma `10` à
sua variável `runningTotal` cada vez que é chamada.
Chamar a função várias vezes mostra esse comportamento em ação:

```swift
incrementByTen()
// returns a value of 10
incrementByTen()
// returns a value of 20
incrementByTen()
// returns a value of 30
```

<!--
  - test: `closures`

  ```swifttest
  >> let r0 =
  -> incrementByTen()
  /> returns a value of \(r0)
  </ returns a value of 10
  >> let r1 =
  -> incrementByTen()
  /> returns a value of \(r1)
  </ returns a value of 20
  >> let r2 =
  -> incrementByTen()
  /> returns a value of \(r2)
  </ returns a value of 30
  ```
-->

<!--
  Rewrite the above to avoid discarding the function's return value.
  Tracking bug is <rdar://problem/35301593>
-->

Se você criar um segundo incrementador,
ele terá sua própria referência armazenada para uma nova variável `runningTotal`, separada:

```swift
let incrementBySeven = makeIncrementer(forIncrement: 7)
incrementBySeven()
// returns a value of 7
```

<!--
  - test: `closures`

  ```swifttest
  -> let incrementBySeven = makeIncrementer(forIncrement: 7)
  >> let r3 =
  -> incrementBySeven()
  /> returns a value of \(r3)
  </ returns a value of 7
  ```
-->

Chamar o incrementador original (`incrementByTen`) de novo
continua incrementando a sua própria variável `runningTotal`,
e não afeta a variável capturada por `incrementBySeven`:

```swift
incrementByTen()
// returns a value of 40
```

<!--
  - test: `closures`

  ```swifttest
  >> let r4 =
  -> incrementByTen()
  /> returns a value of \(r4)
  </ returns a value of 40
  ```
-->

> Nota: Se você atribuir uma closure a uma propriedade de uma instância de classe,
> e a closure capturar essa instância ao se referir a ela ou aos seus membros,
> você criará um ciclo de referência forte entre a closure e a instância.
> O Swift usa *listas de captura* para quebrar esses ciclos de referência forte.
> Para mais informações, veja <doc:AutomaticReferenceCounting#Strong-Reference-Cycles-for-Closures>.

## Closures são tipos de referência

No exemplo acima,
`incrementBySeven` e `incrementByTen` são constantes,
mas as closures a que essas constantes se referem ainda conseguem incrementar
as variáveis `runningTotal` que capturaram.
Isso acontece porque funções e closures são *tipos de referência*.

Sempre que você atribui uma função ou uma closure a uma constante ou variável,
você está, na verdade, fazendo essa constante ou variável
ser uma *referência* à função ou closure.
No exemplo acima,
é a escolha da closure *à qual* `incrementByTen` se refere que é constante,
e não o conteúdo da própria closure.

Isso também significa que, se você atribuir uma closure a duas constantes ou variáveis diferentes,
ambas as constantes ou variáveis se referem à mesma closure.

```swift
let alsoIncrementByTen = incrementByTen
alsoIncrementByTen()
// returns a value of 50

incrementByTen()
// returns a value of 60
```

<!--
  - test: `closures`

  ```swifttest
  -> let alsoIncrementByTen = incrementByTen
  >> let r5 =
  -> alsoIncrementByTen()
  /> returns a value of \(r5)
  </ returns a value of 50

  >> let r6 =
  -> incrementByTen()
  /> returns a value of \(r6)
  </ returns a value of 60
  ```
-->

O exemplo acima mostra que chamar `alsoIncrementByTen`
é o mesmo que chamar `incrementByTen`.
Como ambas se referem à mesma closure,
as duas incrementam e retornam o mesmo total acumulado.

## Escaping closures

Diz-se que uma closure *escapa* de uma função
quando a closure é passada como argumento para a função,
mas é chamada depois que a função retorna.
Ao declarar uma função que recebe uma closure como um de seus parâmetros,
você pode escrever `@escaping` antes do tipo do parâmetro
para indicar que a closure tem permissão para escapar.

Uma forma de a closure escapar
é ser armazenada em uma variável definida fora da função.
Por exemplo,
muitas funções que iniciam uma operação assíncrona
recebem um argumento de closure como completion handler.
A função retorna depois de iniciar a operação,
mas a closure só é chamada quando a operação termina:
a closure precisa escapar para ser chamada depois. Por exemplo:

```swift
var completionHandlers: [() -> Void] = []
func someFunctionWithEscapingClosure(completionHandler: @escaping () -> Void) {
    completionHandlers.append(completionHandler)
}
```

<!--
  - test: `noescape-closure-as-argument, implicit-self-struct`

  ```swifttest
  -> var completionHandlers: [() -> Void] = []
  -> func someFunctionWithEscapingClosure(completionHandler: @escaping () -> Void) {
         completionHandlers.append(completionHandler)
     }
  ```
-->

A função `someFunctionWithEscapingClosure(_:)` recebe uma closure como argumento
e a adiciona a um array declarado fora da função.
Se você não marcasse o parâmetro dessa função com `@escaping`,
receberia um erro de compilação.

Uma escaping closure que se refere a `self`
precisa de atenção especial se `self` for uma instância de classe.
Capturar `self` em uma escaping closure
facilita a criação acidental de um ciclo de referência forte.
Para informações sobre ciclos de referência, veja <doc:AutomaticReferenceCounting>.

Normalmente, uma closure captura variáveis implicitamente
ao usá-las no corpo da closure,
mas nesse caso você precisa ser explícito.
Se você quiser capturar `self`,
escreva `self` explicitamente ao usá-lo,
ou inclua `self` na lista de captura da closure.
Escrever `self` explicitamente deixa clara a sua intenção
e lembra você de confirmar que não há um ciclo de referência.
Por exemplo, no código abaixo,
a closure passada para `someFunctionWithEscapingClosure(_:)`
se refere a `self` explicitamente.
Já a closure passada para `someFunctionWithNonescapingClosure(_:)`
é uma nonescaping closure, o que significa que ela pode se referir a `self` implicitamente.

```swift
func someFunctionWithNonescapingClosure(closure: () -> Void) {
    closure()
}

class SomeClass {
    var x = 10
    func doSomething() {
        someFunctionWithEscapingClosure { self.x = 100 }
        someFunctionWithNonescapingClosure { x = 200 }
    }
}

let instance = SomeClass()
instance.doSomething()
print(instance.x)
// Prints "200".

completionHandlers.first?()
print(instance.x)
// Prints "100".
```

<!--
  - test: `noescape-closure-as-argument`

  ```swifttest
  -> func someFunctionWithNonescapingClosure(closure: () -> Void) {
         closure()
     }

  -> class SomeClass {
         var x = 10
         func doSomething() {
             someFunctionWithEscapingClosure { self.x = 100 }
             someFunctionWithNonescapingClosure { x = 200 }
         }
     }

  -> let instance = SomeClass()
  -> instance.doSomething()
  -> print(instance.x)
  <- 200

  -> completionHandlers.first?()
  -> print(instance.x)
  <- 100
  ```
-->

Aqui está uma versão de `doSomething()` que captura `self`
incluindo-o na lista de captura da closure,
e depois se refere a `self` implicitamente:

```swift
class SomeOtherClass {
    var x = 10
    func doSomething() {
        someFunctionWithEscapingClosure { [self] in x = 100 }
        someFunctionWithNonescapingClosure { x = 200 }
    }
}
```

<!--
  - test: `noescape-closure-as-argument`

  ```swifttest
  -> class SomeOtherClass {
         var x = 10
         func doSomething() {
             someFunctionWithEscapingClosure { [self] in x = 100 }
             someFunctionWithNonescapingClosure { x = 200 }
         }
     }
  >> completionHandlers = []
  >> let instance2 = SomeOtherClass()
  >> instance2.doSomething()
  >> print(instance2.x)
  << 200
  >> completionHandlers.first?()
  >> print(instance2.x)
  << 100
  ```
-->

Se `self` for uma instância de uma struct ou de um enum,
você sempre pode se referir a `self` implicitamente.
No entanto,
uma escaping closure não pode capturar uma referência mutável a `self`
quando `self` é uma instância de uma struct ou de um enum.
Structs e enums não permitem mutabilidade compartilhada,
como discutido em <doc:ClassesAndStructures#Structures-and-Enumerations-Are-Value-Types>.

```swift
struct SomeStruct {
    var x = 10
    mutating func doSomething() {
        someFunctionWithNonescapingClosure { x = 200 }  // OK
        someFunctionWithEscapingClosure { x = 100 }     // Error
    }
}
```

<!--
  - test: `struct-capture-mutable-self`

  ```swifttest
  >> var completionHandlers: [() -> Void] = []
  >> func someFunctionWithEscapingClosure(completionHandler: @escaping () -> Void) {
  >>     completionHandlers.append(completionHandler)
  >> }
  >> func someFunctionWithNonescapingClosure(closure: () -> Void) {
  >>     closure()
  >> }
  -> struct SomeStruct {
         var x = 10
         mutating func doSomething() {
             someFunctionWithNonescapingClosure { x = 200 }  // OK
             someFunctionWithEscapingClosure { x = 100 }     // Error
         }
     }
  !$ error: escaping closure captures mutating 'self' parameter
  !! someFunctionWithEscapingClosure { x = 100 }     // Error
  !! ^
  !$ note: captured here
  !! someFunctionWithEscapingClosure { x = 100 }     // Error
  !! ^
  ```
-->

A chamada à função `someFunctionWithEscapingClosure` no exemplo acima
é um erro porque está dentro de um método `mutating`,
então `self` é mutável.
Isso viola a regra de que escaping closures não podem capturar
uma referência mutável a `self` em structs.

<!--
  - test: `noescape-closure-as-argument`

  ```swifttest
  // Test the non-error portion of struct-capture-mutable-self
  >> struct SomeStruct {
  >>     var x = 10
  >>     mutating func doSomething() {
  >>         someFunctionWithNonescapingClosure { x = 200 }
  >>     }
  >> }

  >> completionHandlers = []
  >> var instance3 = SomeStruct()
  >> instance3.doSomething()
  >> print(instance3.x)
  << 200
  ```
-->

<!--
  - test: `noescape-closure-as-argument`

  ```swifttest
  >> struct S {
  >>     var x = 10
  >>     func doSomething() {
  >>         someFunctionWithEscapingClosure { print(x) }  // OK
  >>     }
  >> }

  >> completionHandlers = []
  >> var s = S()
  >> s.doSomething()
  >> s.x = 99  // No effect on self.x already captured -- S is a value type
  >> completionHandlers.first?()
  << 10
  ```
-->

## Autoclosures

Uma *autoclosure* é uma closure criada automaticamente
para envolver uma expressão que está sendo passada como argumento para uma função.
Ela não recebe nenhum argumento,
e, quando é chamada, retorna o valor
da expressão que está envolvida dentro dela.
Essa conveniência sintática permite omitir as chaves em volta do parâmetro de uma função
ao escrever uma expressão normal em vez de uma closure explícita.

É comum *chamar* funções que recebem autoclosures,
mas não é comum *implementar* esse tipo de função.
Por exemplo,
a função `assert(condition:message:file:line:)` recebe uma autoclosure
nos parâmetros `condition` e `message`;
o parâmetro `condition` só é avaliado em builds de depuração,
e o parâmetro `message` só é avaliado se `condition` for `false`.

Uma autoclosure permite adiar a avaliação,
porque o código dentro dela não é executado até que você chame a closure.
Adiar a avaliação é útil para código
que tem efeitos colaterais ou que é computacionalmente caro,
porque permite controlar quando esse código é avaliado.
O código abaixo mostra como uma closure adia a avaliação.

```swift
var customersInLine = ["Chris", "Alex", "Ewa", "Barry", "Daniella"]
print(customersInLine.count)
// Prints "5".

let customerProvider = { customersInLine.remove(at: 0) }
print(customersInLine.count)
// Prints "5".

print("Now serving \(customerProvider())!")
// Prints "Now serving Chris!"
print(customersInLine.count)
// Prints "4".
```

<!--
  - test: `autoclosures`

  ```swifttest
  -> var customersInLine = ["Chris", "Alex", "Ewa", "Barry", "Daniella"]
  -> print(customersInLine.count)
  <- 5

  -> let customerProvider = { customersInLine.remove(at: 0) }
  -> print(customersInLine.count)
  <- 5

  -> print("Now serving \(customerProvider())!")
  <- Now serving Chris!
  -> print(customersInLine.count)
  <- 4
  ```
-->

<!--
  Using remove(at:) instead of popFirst() because the latter only works
  with ArraySlice, not with Array:
      customersInLine[0..<3].popLast()     // fine
      customersInLine[0..<3].popFirst()    // fine
      customersInLine.popLast()            // fine
      customersInLine.popFirst()           // FAIL
  It also returns an optional, which complicates the listing.
-->

<!--
  TODO: It may be worth describing the differences between ``lazy`` and autoclousures.
-->

Mesmo que o primeiro elemento do array `customersInLine` seja removido
pelo código dentro da closure,
o elemento do array não é removido até que a closure seja de fato chamada.
Se a closure nunca for chamada,
a expressão dentro dela nunca é avaliada,
o que significa que o elemento do array nunca é removido.
Observe que o tipo de `customerProvider` não é `String`,
mas `() -> String`:
uma função sem parâmetros que retorna uma string.

Você obtém o mesmo comportamento de avaliação adiada
quando passa uma closure como argumento para uma função.

```swift
// customersInLine is ["Alex", "Ewa", "Barry", "Daniella"]
func serve(customer customerProvider: () -> String) {
    print("Now serving \(customerProvider())!")
}
serve(customer: { customersInLine.remove(at: 0) } )
// Prints "Now serving Alex!"
```

<!--
  - test: `autoclosures-function`

  ```swifttest
  >> var customersInLine = ["Alex", "Ewa", "Barry", "Daniella"]
  /> customersInLine is \(customersInLine)
  </ customersInLine is ["Alex", "Ewa", "Barry", "Daniella"]
  -> func serve(customer customerProvider: () -> String) {
         print("Now serving \(customerProvider())!")
     }
  -> serve(customer: { customersInLine.remove(at: 0) } )
  <- Now serving Alex!
  ```
-->

A função `serve(customer:)` no código acima
recebe uma closure explícita que retorna o nome de um cliente.
A versão de `serve(customer:)` abaixo
faz a mesma operação, mas, em vez de receber uma closure explícita,
recebe uma autoclosure
ao marcar o tipo do seu parâmetro com o atributo `@autoclosure`.
Agora você pode chamar a função
como se ela recebesse um argumento `String` em vez de uma closure.
O argumento é convertido automaticamente em uma closure,
porque o tipo do parâmetro `customerProvider` é marcado
com o atributo `@autoclosure`.

```swift
// customersInLine is ["Ewa", "Barry", "Daniella"]
func serve(customer customerProvider: @autoclosure () -> String) {
    print("Now serving \(customerProvider())!")
}
serve(customer: customersInLine.remove(at: 0))
// Prints "Now serving Ewa!"
```

<!--
  - test: `autoclosures-function-with-autoclosure`

  ```swifttest
  >> var customersInLine = ["Ewa", "Barry", "Daniella"]
  /> customersInLine is \(customersInLine)
  </ customersInLine is ["Ewa", "Barry", "Daniella"]
  -> func serve(customer customerProvider: @autoclosure () -> String) {
         print("Now serving \(customerProvider())!")
     }
  -> serve(customer: customersInLine.remove(at: 0))
  <- Now serving Ewa!
  ```
-->

> Nota: Usar autoclosures em excesso pode tornar seu código difícil de entender.
> O contexto e o nome da função devem deixar claro
> que a avaliação está sendo adiada.

Se você quiser uma autoclosure que possa escapar,
use os atributos `@autoclosure` e `@escaping` juntos.
O atributo `@escaping` é descrito acima, em <doc:Closures#Escaping-closures>.

```swift
// customersInLine is ["Barry", "Daniella"]
var customerProviders: [() -> String] = []
func collectCustomerProviders(_ customerProvider: @autoclosure @escaping () -> String) {
    customerProviders.append(customerProvider)
}
collectCustomerProviders(customersInLine.remove(at: 0))
collectCustomerProviders(customersInLine.remove(at: 0))

print("Collected \(customerProviders.count) closures.")
// Prints "Collected 2 closures."
for customerProvider in customerProviders {
    print("Now serving \(customerProvider())!")
}
// Prints "Now serving Barry!"
// Prints "Now serving Daniella!"
```

<!--
  - test: `autoclosures-function-with-escape`

  ```swifttest
  >> var customersInLine = ["Barry", "Daniella"]
  /> customersInLine is \(customersInLine)
  </ customersInLine is ["Barry", "Daniella"]
  -> var customerProviders: [() -> String] = []
  -> func collectCustomerProviders(_ customerProvider: @autoclosure @escaping () -> String) {
         customerProviders.append(customerProvider)
     }
  -> collectCustomerProviders(customersInLine.remove(at: 0))
  -> collectCustomerProviders(customersInLine.remove(at: 0))

  -> print("Collected \(customerProviders.count) closures.")
  <- Collected 2 closures.
  -> for customerProvider in customerProviders {
         print("Now serving \(customerProvider())!")
     }
  <- Now serving Barry!
  <- Now serving Daniella!
  ```
-->

No código acima,
em vez de chamar a closure passada para ele
como seu argumento `customerProvider`,
a função `collectCustomerProviders(_:)`
adiciona a closure ao array `customerProviders`.
O array é declarado fora do escopo da função,
o que significa que as closures do array podem ser executadas depois que a função retorna.
Como resultado,
o valor do argumento `customerProvider`
precisa poder escapar do escopo da função.

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
