# Concorrência

Execute operações assíncronas.

O Swift tem suporte nativo para escrever código assíncrono e paralelo
de forma estruturada.
*Código assíncrono* pode ser suspenso e retomado depois,
embora apenas um trecho do programa seja executado por vez.
Suspender e retomar código no seu programa
permite que ele continue avançando
em operações de curta duração, como atualizar a interface,
enquanto continua trabalhando em operações demoradas,
como buscar dados pela rede ou processar arquivos.
*Código paralelo* significa que vários trechos de código são executados ao mesmo tempo.
Por exemplo, um computador com um processador de quatro núcleos
pode executar quatro trechos de código ao mesmo tempo,
com cada núcleo realizando uma das tarefas.
Um programa que usa código paralelo e assíncrono
executa várias operações ao mesmo tempo
e suspende as operações que estão esperando por um sistema externo.
O restante deste capítulo usa o termo *concorrência*
para se referir a essa combinação comum de código assíncrono e paralelo.

A flexibilidade extra de agendamento que vem do código paralelo ou assíncrono
também traz o custo de maior complexidade.
Ao escrever código concorrente,
você não sabe com antecedência quais trechos de código vão rodar ao mesmo tempo,
e nem sempre sabe a ordem em que eles vão rodar.
Um problema comum em código concorrente acontece
quando vários trechos de código tentam acessar
um mesmo estado mutável compartilhado.
Isso é conhecido como *data race*.
Quando você usa o suporte à concorrência no nível da linguagem,
o Swift detecta e previne data races,
e a maioria delas gera um erro em tempo de compilação.
Algumas data races só podem ser detectadas quando o código está rodando;
essas data races encerram a execução do código.
Você usa actors e isolamento para se proteger contra data races,
como descrito neste capítulo.

> Nota: Se você já escreveu código concorrente antes,
> pode estar acostumado a trabalhar com threads.
> O modelo de concorrência do Swift é construído sobre threads,
> mas você não interage com elas diretamente.
> Uma função assíncrona em Swift
> pode liberar a thread em que está rodando,
> o que permite que outra função assíncrona rode nessa thread
> enquanto a primeira função está bloqueada.
> Quando uma função assíncrona é retomada,
> o Swift não garante em qual thread
> essa função vai rodar.

Embora seja possível escrever código concorrente
sem usar o suporte da linguagem do Swift,
esse código tende a ser mais difícil de ler.
Por exemplo, o código a seguir baixa uma lista de nomes de fotos,
baixa a primeira foto dessa lista
e mostra essa foto para o usuário:

```swift
listPhotos(inGallery: "Summer Vacation") { photoNames in
    let sortedNames = photoNames.sorted()
    let name = sortedNames[0]
    downloadPhoto(named: name) { photo in
        show(photo)
    }
}
```

<!--
  - test: `async-via-nested-completion-handlers`

  ```swifttest
  >> struct Data {}  // Instead of actually importing Foundation
  >> func listPhotos(inGallery name: String, completionHandler: ([String]) -> Void ) {
  >>   completionHandler(["IMG001", "IMG99", "IMG0404"])
  >> }
  >> func downloadPhoto(named name: String, completionHandler: (Data) -> Void) {
  >>     completionHandler(Data())
  >> }
  >> func show(_ image: Data) { }
  -> listPhotos(inGallery: "Summer Vacation") { photoNames in
         let sortedNames = photoNames.sorted()
         let name = sortedNames[0]
         downloadPhoto(named: name) { photo in
             show(photo)
         }
     }
  ```
-->

Mesmo nesse caso simples,
como o código precisa ser escrito como uma série de completion handlers,
você acaba escrevendo closures aninhadas.
Nesse estilo,
códigos mais complexos com muita aninhação rapidamente se tornam difíceis de manejar.

## Definindo e chamando funções assíncronas

Uma *função assíncrona* ou *método assíncrono*
é um tipo especial de função ou método
que pode ser suspenso enquanto está no meio da execução.
Isso contrasta com funções e métodos síncronos comuns,
que ou executam até o fim, ou lançam um erro, ou nunca retornam.
Uma função ou método assíncrono ainda faz uma dessas três coisas,
mas também pode pausar no meio do caminho quando está esperando por algo.
No corpo de uma função ou método assíncrono,
você marca cada um dos pontos em que a execução pode ser suspensa.

Para indicar que uma função ou método é assíncrono,
você escreve a palavra-chave `async` na declaração, depois dos parâmetros,
de forma parecida com o uso de `throws` para marcar uma função que lança erros.
Se a função ou método retorna um valor,
você escreve `async` antes da seta de retorno (`->`).
Por exemplo,
veja como você poderia buscar os nomes das fotos de uma galeria:

```swift
func listPhotos(inGallery name: String) async -> [String] {
    let result = // ... some asynchronous networking code ...
    return result
}
```

<!--
  - test: `async-function-shape`

  ```swifttest
  -> func listPhotos(inGallery name: String) async -> [String] {
         let result = // ... some asynchronous networking code ...
  >>     ["IMG001", "IMG99", "IMG0404"]
         return result
     }
  ```
-->

Para uma função ou método que é ao mesmo tempo assíncrono e lança erros,
você escreve `async` antes de `throws`.

<!--
  - test: `async-comes-before-throws`

  ```swifttest
  >> func right() async throws -> Int { return 12 }
  >> func wrong() throws async -> Int { return 12 }
  !$ error: 'async' must precede 'throws'
  !! func wrong() throws async -> Int { return 12 }
  !! ^~~~~~
  !! async
  ```
-->

Ao chamar um método assíncrono,
a execução é suspensa até que o método retorne.
Você escreve `await` antes da chamada
para marcar o possível ponto de suspensão.
Isso é parecido com escrever `try` ao chamar uma função que lança erros,
para marcar a possível mudança no fluxo do programa caso ocorra um erro.
Dentro de um método assíncrono,
o fluxo de execução só pode ser suspenso
*apenas* quando você chama outro método assíncrono ---
a suspensão nunca é implícita ou preemptiva ---
o que significa que todo possível ponto de suspensão é marcado com `await`.
Marcar todos os possíveis pontos de suspensão no seu código
ajuda a deixar o código concorrente mais fácil de ler e entender.

Por exemplo,
o código abaixo busca os nomes de todas as fotos de uma galeria
e depois mostra a primeira foto:

```swift
let photoNames = await listPhotos(inGallery: "Summer Vacation")
let sortedNames = photoNames.sorted()
let name = sortedNames[0]
let photo = await downloadPhoto(named: name)
show(photo)
```

<!--
  - test: `defining-async-function`

  ```swifttest
  >> struct Data {}  // Instead of actually importing Foundation
  >> func downloadPhoto(named name: String) async -> Data { return Data() }
  >> func show(_ image: Data) { }
  >> func listPhotos(inGallery name: String) async -> [String] {
  >>     return ["IMG001", "IMG99", "IMG0404"]
  >> }
  >> func f() async {
  -> let photoNames = await listPhotos(inGallery: "Summer Vacation")
  -> let sortedNames = photoNames.sorted()
  -> let name = sortedNames[0]
  -> let photo = await downloadPhoto(named: name)
  -> show(photo)
  >> }
  ```
-->

Como `listPhotos(inGallery:)` e `downloadPhoto(named:)`
precisam fazer requisições de rede,
elas podem levar um tempo relativamente longo para terminar.
Torná-las assíncronas, escrevendo `async` antes da seta de retorno,
permite que o restante do código do app continue rodando
enquanto este código espera a foto ficar pronta.

Para entender a natureza concorrente do exemplo acima,
veja uma das ordens de execução possíveis:

1. O código começa a rodar pela primeira linha
   e executa até o primeiro `await`.
   Ele chama a função `listPhotos(inGallery:)`
   e suspende a execução enquanto espera que essa função retorne.

2. Enquanto a execução deste código está suspensa,
   algum outro código concorrente do mesmo programa roda.
   Por exemplo, talvez uma tarefa de longa duração em segundo plano
   continue atualizando uma lista de novas galerias de fotos.
   Esse código também roda até o próximo ponto de suspensão, marcado com `await`,
   ou até terminar.

3. Depois que `listPhotos(inGallery:)` retorna,
   este código continua a execução a partir desse ponto.
   Ele atribui o valor retornado a `photoNames`.

4. As linhas que definem `sortedNames` e `name`
   são código comum e síncrono.
   Como nada nessas linhas está marcado com `await`,
   não há possíveis pontos de suspensão ali.

5. O próximo `await` marca a chamada à função `downloadPhoto(named:)`.
   Este código pausa a execução novamente até que essa função retorne,
   dando a outro código concorrente a oportunidade de rodar.

6. Depois que `downloadPhoto(named:)` retorna,
   o valor retornado é atribuído a `photo`
   e depois passado como argumento na chamada a `show(_:)`.

Os possíveis pontos de suspensão no seu código marcados com `await`
indicam que o trecho atual de código pode pausar a execução
enquanto espera que a função ou método assíncrono retorne.
Isso também é chamado de *ceder a thread*,
porque, nos bastidores,
o Swift suspende a execução do seu código na thread atual
e roda outro código nessa thread.
Como código com `await` precisa poder suspender a execução,
apenas alguns lugares do seu programa podem chamar funções ou métodos assíncronos:

- Código no corpo de uma função, método ou propriedade assíncrona.

- Código no método estático `main()` de
  uma struct, classe ou enum marcado com `@main`.

- Código em uma task filha não estruturada,
  como mostrado em <doc:Concurrency#Unstructured-Concurrency> abaixo.

<!--
  SE-0296 specifically calls out that top-level code is *not* an async context,
  contrary to what you might expect.
  If that gets changed, add this bullet to the list above:

  - Code at the top level that forms an implicit main function.
-->

O método [`Task.sleep(for:tolerance:clock:)`][]
é útil ao escrever código simples
para entender como a concorrência funciona.
Esse método suspende a task atual por pelo menos o tempo informado.
Aqui está uma versão da função `listPhotos(inGallery:)`
que usa `sleep(for:tolerance:clock:)` para simular a espera por uma operação de rede:

[`Task.sleep(for:tolerance:clock:)`]: https://developer.apple.com/documentation/swift/task/sleep(for:tolerance:clock:)

```swift
func listPhotos(inGallery name: String) async throws -> [String] {
    try await Task.sleep(for: .seconds(2))
    return ["IMG001", "IMG99", "IMG0404"]
}
```

<!--
  - test: `sleep-in-toy-code`

  ```swifttest
  >> struct Data {}  // Instead of actually importing Foundation
  -> func listPhotos(inGallery name: String) async throws -> [String] {
         try await Task.sleep(for: .seconds(2))
         return ["IMG001", "IMG99", "IMG0404"]
  }
  ```
-->

A versão de `listPhotos(inGallery:)` no código acima
é ao mesmo tempo assíncrona e capaz de lançar erros,
porque a chamada a `Task.sleep(until:tolerance:clock:)` pode lançar um erro.
Ao chamar essa versão de `listPhotos(inGallery:)`,
você escreve `try` e `await` juntos:

```swift
let photos = try await listPhotos(inGallery: "A Rainy Weekend")
```

Funções assíncronas têm algumas semelhanças com funções que lançam erros:
ao definir uma função assíncrona ou que lança erros,
você a marca com `async` ou `throws`,
e marca as chamadas a essa função com `await` ou `try`.
Uma função assíncrona pode chamar outra função assíncrona,
assim como uma função que lança erros pode chamar outra função que lança erros.

No entanto, existe uma diferença muito importante.
Você pode envolver código que lança erros em um bloco `do`-`catch` para tratar os erros,
ou usar `Result` para armazenar o erro e deixar que outro código o trate.
Essas abordagens permitem chamar funções que lançam erros
a partir de código não lançador.
Por exemplo:

```swift
func availableRainyWeekendPhotos() -> Result<[String], Error> {
    return Result {
        try listDownloadedPhotos(inGallery: "A Rainy Weekend")
    }
}
```

Em contraste,
não existe uma forma segura de envolver código assíncrono
para que você possa chamá-lo a partir de código síncrono e esperar pelo resultado.
A biblioteca padrão do Swift intencionalmente omite essa funcionalidade insegura ---
tentar implementá-la por conta própria pode levar a
problemas como races sutis, problemas de thread e deadlocks.
Ao adicionar código concorrente a um projeto existente,
trabalhe de cima para baixo.
Ou seja,
comece convertendo a camada mais alta do código para usar concorrência,
e depois passe a converter as funções e métodos que ela chama,
percorrendo a arquitetura do projeto uma camada por vez.
Não existe forma de seguir uma abordagem de baixo para cima,
porque código síncrono nunca pode chamar código assíncrono.

<!--
  OUTLINE

  ## Asynchronous Closures

  like how you can have an async function, a closure con be async
  if a closure contains 'await' that implicitly makes it async
  you can mark it explicitly with "async -> in"

  (discussion of @MainActor closures can probably go here too)
-->

## Sequências assíncronas

A função `listPhotos(inGallery:)` na seção anterior
retorna de forma assíncrona o array inteiro de uma vez,
depois que todos os elementos do array estão prontos.
Outra abordagem
é esperar por um elemento da coleção de cada vez,
usando uma *sequência assíncrona*.
Veja como é iterar sobre uma sequência assíncrona:

```swift
import Foundation

let handle = FileHandle.standardInput
for try await line in handle.bytes.lines {
    print(line)
}
```

<!--
  - test: `async-sequence`

  ```swifttest
  -> import Foundation

  >> func f() async throws {
  -> let handle = FileHandle.standardInput
  -> for try await line in handle.bytes.lines {
         print(line)
     }
  >> }
  ```
-->

Em vez de usar um loop `for`-`in` comum,
o exemplo acima escreve `for` seguido de `await`.
Assim como ao chamar uma função ou método assíncrono,
escrever `await` indica um possível ponto de suspensão.
Um loop `for`-`await`-`in` pode suspender a execução
no início de cada iteração,
enquanto espera que o próximo elemento esteja disponível.

Da mesma forma que você pode usar seus próprios tipos em um loop `for`-`in`
ao adotar o protocolo [`Sequence`][],
você pode usar seus próprios tipos em um loop `for`-`await`-`in`
ao adotar o protocolo [`AsyncSequence`].

[`Sequence`]: https://developer.apple.com/documentation/swift/sequence
[`AsyncSequence`]: https://developer.apple.com/documentation/swift/asyncsequence

<!--
  TODO what happened to ``Series`` which was supposed to be a currency type?
  Is that coming from Combine instead of the stdlib maybe?

  Also... need a real API that produces a async sequence.
  I'd prefer not to go through the whole process of making one here,
  since the protocol reference has enough detail to show you how to do that.
  There's nothing in the stdlib except for the AsyncFooSequence types.
  Maybe one of the other conforming types from an Apple framework --
  how about FileHandle.AsyncBytes (myFilehandle.bytes.lines) from Foundation?
  https://developer.apple.com/documentation/swift/asyncsequence
  https://developer.apple.com/documentation/foundation/filehandle

  if we get a stdlib-provided async sequence type at some point,
  rewrite the above to fit the same narrative flow
  using something like the following

  let names = await listPhotos(inGallery: "Winter Vacation")
  for await photo in Photos(names: names) {
      show(photo)
  }
-->

## Chamando funções assíncronas em paralelo

Chamar uma função assíncrona com `await`
executa apenas um trecho de código por vez.
Enquanto o código assíncrono está rodando,
quem chamou espera que esse código termine
antes de passar para a próxima linha.
Por exemplo,
para buscar as três primeiras fotos de uma galeria,
você poderia esperar três chamadas à função `downloadPhoto(named:)`
da seguinte forma:

```swift
let firstPhoto = await downloadPhoto(named: photoNames[0])
let secondPhoto = await downloadPhoto(named: photoNames[1])
let thirdPhoto = await downloadPhoto(named: photoNames[2])

let photos = [firstPhoto, secondPhoto, thirdPhoto]
show(photos)
```

<!--
  - test: `defining-async-function`

  ```swifttest
  >> func show(_ images: [Data]) { }
  >> func ff() async {
  >> let photoNames = ["IMG001", "IMG99", "IMG0404"]
  -> let firstPhoto = await downloadPhoto(named: photoNames[0])
  -> let secondPhoto = await downloadPhoto(named: photoNames[1])
  -> let thirdPhoto = await downloadPhoto(named: photoNames[2])

  -> let photos = [firstPhoto, secondPhoto, thirdPhoto]
  -> show(photos)
  >> }
  ```
-->

Essa abordagem tem uma desvantagem importante:
embora o download seja assíncrono
e permita que outro trabalho aconteça enquanto ele avança,
apenas uma chamada a `downloadPhoto(named:)` roda por vez.
Cada foto é baixada por completo antes de o download da próxima começar.
No entanto, não há necessidade de essas operações esperarem ---
cada foto pode ser baixada de forma independente, ou até ao mesmo tempo.

Para chamar uma função assíncrona
e deixá-la rodar em paralelo com o código ao redor,
escreva `async` antes de `let` ao definir uma constante,
e depois escreva `await` toda vez que usar a constante.

```swift
async let firstPhoto = downloadPhoto(named: photoNames[0])
async let secondPhoto = downloadPhoto(named: photoNames[1])
async let thirdPhoto = downloadPhoto(named: photoNames[2])

let photos = await [firstPhoto, secondPhoto, thirdPhoto]
show(photos)
```

<!--
  - test: `calling-with-async-let`

  ```swifttest
  >> struct Data {}  // Instead of actually importing Foundation
  >> func show(_ images: [Data]) { }
  >> func downloadPhoto(named name: String) async -> Data { return Data() }
  >> let photoNames = ["IMG001", "IMG99", "IMG0404"]
  >> func f() async {
  -> async let firstPhoto = downloadPhoto(named: photoNames[0])
  -> async let secondPhoto = downloadPhoto(named: photoNames[1])
  -> async let thirdPhoto = downloadPhoto(named: photoNames[2])

  -> let photos = await [firstPhoto, secondPhoto, thirdPhoto]
  -> show(photos)
  >> }
  ```
-->

Neste exemplo,
as três chamadas a `downloadPhoto(named:)` começam
sem esperar que a anterior termine.
Se houver recursos suficientes disponíveis, elas podem rodar ao mesmo tempo.
Nenhuma dessas chamadas de função é marcada com `await`
porque o código não suspende para esperar o resultado da função.
Em vez disso, a execução continua
até a linha em que `photos` é definido ---
nesse ponto, o programa precisa dos resultados dessas chamadas assíncronas,
então você escreve `await` para pausar a execução
até que as três fotos terminem de baixar.

Veja como você pode pensar nas diferenças entre essas duas abordagens:

- Chame funções assíncronas com `await`
  quando o código das linhas seguintes depende do resultado dessa função.
  Isso cria trabalho que é executado de forma sequencial.
- Chame funções assíncronas com `async`-`let`
  quando você não precisa do resultado até mais adiante no código.
  Isso cria trabalho que pode ser executado em paralelo.
- Tanto `await` quanto `async`-`let`
  permitem que outro código rode enquanto estão suspensos.
- Nos dois casos, você marca o possível ponto de suspensão com `await`
  para indicar que a execução vai pausar, se necessário,
  até que a função assíncrona retorne.

Você também pode combinar as duas abordagens no mesmo código.

## Tasks e task groups

Uma *task* é uma unidade de trabalho
que pode ser executada de forma assíncrona como parte do seu programa.
Todo código assíncrono roda como parte de alguma task.
Uma task, por si só, faz apenas uma coisa por vez,
mas, quando você cria várias tasks,
o Swift pode agendá-las para rodar simultaneamente.

A sintaxe `async`-`let` descrita na seção anterior
cria implicitamente uma task filha ---
essa sintaxe funciona bem quando você já sabe
quais tasks o programa precisa executar.
Você também pode criar um task group
(uma instância de [`TaskGroup`][])
e adicionar tasks filhas a esse grupo explicitamente,
o que oferece mais controle sobre prioridade e cancelamento,
e permite criar um número dinâmico de tasks.

[`TaskGroup`]: https://developer.apple.com/documentation/swift/taskgroup

As tasks são organizadas em uma hierarquia.
Cada task de um determinado task group tem a mesma task pai,
e cada task pode ter tasks filhas.
Por causa da relação explícita entre tasks e task groups,
essa abordagem é chamada de *concorrência estruturada*.
A relação explícita pai-filho entre as tasks traz várias vantagens:

- Em uma task pai,
  você não pode se esquecer de esperar que as tasks filhas terminem.

- Ao definir uma prioridade mais alta para uma task filha,
  a prioridade da task pai é elevada automaticamente.

- Quando uma task pai é cancelada,
  cada uma de suas tasks filhas também é cancelada automaticamente.

- Valores locais da task se propagam para as tasks filhas de forma eficiente e automática.

Aqui está outra versão do código para baixar fotos
que lida com qualquer quantidade de fotos:

```swift
await withTaskGroup(of: Data.self) { group in
    let photoNames = await listPhotos(inGallery: "Summer Vacation")
    for name in photoNames {
        group.addTask {
            return await downloadPhoto(named: name)
        }
    }

    for await photo in group {
        show(photo)
    }
}
```

O código acima cria um novo task group
e depois cria tasks filhas
para baixar cada foto da galeria.
O Swift executa o máximo possível dessas tasks de forma concorrente, conforme as condições permitirem.
Assim que uma task filha termina de baixar uma foto,
essa foto é exibida.
Não há garantia sobre a ordem em que as tasks filhas terminam,
então as fotos dessa galeria podem ser mostradas em qualquer ordem.

> Nota:
> Se o código para baixar uma foto puder lançar um erro,
> você deve chamar `withThrowingTaskGroup(of:returning:body:)` no lugar.

No trecho de código acima,
cada foto é baixada e depois exibida,
então o task group não retorna nenhum resultado.
Para um task group que retorna um resultado,
você adiciona código que acumula esse resultado
dentro da closure que você passa para `withTaskGroup(of:returning:body:)`.

```swift
let photos = await withTaskGroup(of: Data.self) { group in
    let photoNames = await listPhotos(inGallery: "Summer Vacation")
    for name in photoNames {
        group.addTask {
            return await downloadPhoto(named: name)
        }
    }

    var results: [Data] = []
    for await photo in group {
        results.append(photo)
    }

    return results
}
```

Assim como no exemplo anterior,
este exemplo cria uma task filha para cada foto, para baixá-la.
Diferente do exemplo anterior,
o loop `for`-`await`-`in` espera a próxima task filha terminar,
adiciona o resultado dessa task ao array de resultados,
e continua esperando até que todas as tasks filhas tenham terminado.
Por fim,
o task group retorna o array de fotos baixadas
como seu resultado geral.

<!--
TODO:
In the future,
we could extend the example above
to show how you can limit the number of concurrent tasks
that get spun up by a task group.
There isn't a specific guideline we can give
in terms of how many concurrent tasks to run --
it's more "profile your code, and then adjust".

See also:
https://developer.apple.com/videos/play/wwdc2023/10170?time=688

We could also show withDiscardingTaskGroup(...)
since that's optimized for child tasks
whose values aren't collected.
-->

### Cancelamento de task

A concorrência do Swift usa um modelo de cancelamento cooperativo.
Cada task verifica se foi cancelada
nos pontos apropriados da sua execução,
e responde ao cancelamento de forma adequada.
Dependendo do trabalho que a task está fazendo,
responder ao cancelamento normalmente significa uma das seguintes ações:

- Lançar um erro como `CancellationError`
- Retornar `nil` ou uma coleção vazia
- Retornar o trabalho parcialmente concluído

Baixar imagens pode levar muito tempo
se as imagens forem grandes ou a rede for lenta.
Para permitir que o usuário interrompa esse trabalho,
sem precisar esperar que todas as tasks terminem,
as tasks precisam verificar o cancelamento e parar de rodar se forem canceladas.
Há duas formas de uma task fazer isso:
chamando o método de tipo [`Task.checkCancellation()`][],
ou lendo a propriedade de tipo [`Task.isCancelled`][`Task.isCancelled` type].
Chamar `checkCancellation()` lança um erro se a task foi cancelada;
uma task que lança erros pode propagar esse erro para fora da task,
interrompendo todo o trabalho dela.
Isso tem a vantagem de ser simples de implementar e entender.
Para mais flexibilidade, use a propriedade `isCancelled`,
que permite fazer trabalho de limpeza como parte da interrupção da task,
como fechar conexões de rede e apagar arquivos temporários.

[`Task.checkCancellation()`]: https://developer.apple.com/documentation/swift/task/checkcancellation()
[`Task.isCancelled` type]: https://developer.apple.com/documentation/swift/task/iscancelled-swift.type.property

```swift
let photos = await withTaskGroup { group in
    let photoNames = await listPhotos(inGallery: "Summer Vacation")
    for name in photoNames {
        let added = group.addTaskUnlessCancelled {
            Task.isCancelled ? nil : await downloadPhoto(named: name)
        }
        guard added else { break }
    }

    var results: [Data] = []
    for await photo in group {
        if let photo { results.append(photo) }
    }
    return results
}
```

O código acima faz várias mudanças em relação à versão anterior:

- Cada task é adicionada usando o método
  [`TaskGroup.addTaskUnlessCancelled(priority:operation:)`][],
  para evitar começar trabalho novo depois do cancelamento.

- Depois de cada chamada a `addTaskUnlessCancelled(priority:operation:)`,
  o código confirma que a nova task filha foi adicionada.
  Se o grupo for cancelado, o valor de `added` é `false` ---
  nesse caso, o código para de tentar baixar fotos adicionais.

- Cada task verifica o cancelamento
  antes de começar a baixar a foto.
  Se tiver sido cancelada, a task retorna `nil`.

- No final,
  o task group ignora os valores `nil` ao coletar os resultados.
  Tratar o cancelamento retornando `nil`
  permite que o task group devolva um resultado parcial ---
  as fotos que já tinham sido baixadas no momento do cancelamento ---
  em vez de descartar o trabalho já concluído.

[`TaskGroup.addTaskUnlessCancelled(priority:operation:)`]: https://developer.apple.com/documentation/swift/taskgroup/addtaskunlesscancelled(priority:operation:)

> Nota:
> Para verificar se uma task foi cancelada a partir de fora dessa task,
> use a propriedade de instância [`Task.isCancelled`][`Task.isCancelled` instance]
> em vez da propriedade de tipo.

[`Task.isCancelled` instance]: https://developer.apple.com/documentation/swift/task/iscancelled-swift.property

Para trabalho que precisa de notificação imediata do cancelamento,
use a função [`withTaskCancellationHandler(operation:onCancel:isolation:)`][].
Por exemplo:

[`withTaskCancellationHandler(operation:onCancel:isolation:)`]: https://developer.apple.com/documentation/swift/withtaskcancellationhandler(operation:oncancel:isolation:)

```swift
let task = Task {
    await withTaskCancellationHandler {
        // ...
    } onCancel: {
        print("Canceled!")
    }
}

// ... some time later...
task.cancel()  // Prints "Canceled!"
```

Ao usar um cancellation handler,
o cancelamento da task continua sendo cooperativo:
a task ou roda até o fim
ou verifica o cancelamento e para mais cedo.
Como a task ainda está rodando quando o cancellation handler começa,
evite compartilhar estado entre a task e o cancellation handler,
porque isso pode criar uma race condition.

<!--
  OUTLINE

  - cancellation propagates (Konrad's example below)

  ::

      let handle = Task.detached {
      await withTaskGroup(of: Bool.self) { group in
          var done = false
          while done {
          await group.addTask { Task.isCancelled } // is this child task canceled?
          done = try await group.next() ?? false
          }
      print("done!") // <1>
      }

      handle.cancel()
      // done!           <1>
-->

<!--
  Not for WWDC, but keep for future:

  task have deadlines, not timeouts --- like "now + 20 ms" ---
  a deadline is usually what you want anyhow when you think of a timeout

  - this chapter introduces the core ways you use tasks;
  for the full list what you can do,
  including the unsafe escape hatches
  and ``Task.current()`` for advanced use cases,
  see the Task API reference [link to stdlib]

  - task cancellation isn't part of the state diagram below;
  it's an independent property that can happen in any state

  [PLACEHOLDER ART]

  Task state diagram

     |
     v
  Suspended <-+
     |        |
     v        |
  Running ----+
     |
     v
  Completed

  [PLACEHOLDER ART]

  Task state diagram, including "substates"

     |
     v
  Suspended <-----+
  (Waiting) <---+ |
     |          | |
     v          | |
  Suspended     | |
  (Schedulable) / |
     |            |
     v            |
  Running --------+
     |
     v
  Completed

  .. _Concurrency_ChildTasks:

  Adding Child Tasks to a Task Group

  - awaiting ``withGroup`` means waiting for all child tasks to complete

  - a child task can't outlive its parent,
  like how ``async``-``let`` can't outlive the (implicit) parent
  which is the function scope

  - awaiting ``addTask(priority:operation:)``
  means waiting for that child task to be added,
  not waiting for that child task to finish

  - ?? maybe cover ``TaskGroup.next``
  probably nicer to use the ``for await result in someGroup`` syntax

  quote from the SE proposal --- I want to include this fact here too

  > There's no way for reference to the child task to
  > escape the scope in which the child task is created.
  > This ensures that the structure of structured concurrency is maintained.
  > It makes it easier to reason about
  > the concurrent tasks that are executing within a given scope,
  > and also enables various optimizations.
-->

<!--
  OUTLINE

  .. _Concurrency_TaskPriority:

  Setting Task Priority

  - priority values defined by ``Task.Priority`` enum

  - type property ``Task.currentPriority``

  - The exact result of setting a task's priority depends on the executor

  - TR: What's the built-in stdlib executor do?

  - Child tasks inherit the priority of their parents

  - If a high-priority task is waiting for a low-priority one,
  the low-priority one gets scheduled at high priority
  (this is known as :newTerm:`priority escalation`)

  - In addition, or instead of, setting a low priority,
  you can use ``Task.yield()`` to explicitly pass execution to the next scheduled task.
  This is a sort of cooperative multitasking for long-running work.
-->

Você pode inserir explicitamente um ponto de suspensão
chamando o método [`Task.yield()`][].

[`Task.yield()`]: https://developer.apple.com/documentation/swift/task/yield()

```swift
func generateSlideshow(forGallery gallery: String) async {
    let photos = await listPhotos(inGallery: gallery)
    for photo in photos {
        // ... render a few seconds of video for this photo ...
        await Task.yield()
    }
}
```

Supondo que o código que renderiza o vídeo seja síncrono,
ele não contém nenhum ponto de suspensão.
O trabalho de renderizar vídeo também pode levar muito tempo.
No entanto,
você pode chamar `Task.yield()` periodicamente
para adicionar pontos de suspensão explícitos.
Estruturar código de longa duração dessa forma
permite que o Swift equilibre o progresso desta task
com o progresso do trabalho de outras tasks do seu programa.

### Concorrência não estruturada

Além das abordagens estruturadas de concorrência
descritas nas seções anteriores,
o Swift também oferece suporte a concorrência não estruturada.
Diferente das tasks que fazem parte de um task group,
uma *task não estruturada* não tem uma task pai.
Você tem total liberdade para gerenciar tasks não estruturadas
da forma que o seu programa precisar,
mas também é totalmente responsável pela corretude delas.

Para criar uma task não estruturada
que roda de forma semelhante ao código ao redor,
chame o inicializador [`Task.init(name:priority:operation:)`][].
A nova task, por padrão, roda com
o mesmo isolamento de actor, prioridade e estado local de task da task atual.
Para criar uma task não estruturada
que é mais independente do código ao redor,
conhecida mais especificamente como *task destacada*,
chame o método estático [`Task.detached(name:priority:operation:)`][].
A nova task, por padrão, roda sem nenhum isolamento de actor
e não herda a prioridade nem o estado local da task atual.
As duas operações retornam uma task com a qual você pode interagir ---
por exemplo, para esperar pelo resultado dela ou cancelá-la.

```swift
let newPhoto = // ... some photo data ...
let handle = Task {
    return await add(newPhoto, toGalleryNamed: "Spring Adventures")
}
let result = await handle.value
```

Para mais informações sobre como gerenciar tasks destacadas,
veja [`Task`](https://developer.apple.com/documentation/swift/task).

[`Task.init(name:priority:operation:)`]: https://developer.apple.com/documentation/swift/task/init(name:priority:operation:)-43wmk
[`Task.detached(name:priority:operation:)`]: https://developer.apple.com/documentation/swift/task/detached(name:priority:operation:)-795w1

<!--
  TODO Add some conceptual guidance about
  when to make a method do its work in a detached task
  versus making the method itself async?
  (Pull from my 2021-04-21 notes from Ben's talk rehearsal.)
-->

## Isolamento

As seções anteriores discutem abordagens para dividir trabalho concorrente.
Esse trabalho pode envolver a alteração de dados compartilhados, como a interface de um app.
Se partes diferentes do código puderem modificar os mesmos dados ao mesmo tempo,
isso cria o risco de uma data race.
O Swift protege você de data races no seu código:
sempre que você lê ou modifica um dado,
o Swift garante que nenhum outro código esteja modificando esse dado ao mesmo tempo.
Essa garantia é chamada de *isolamento de dados*.
Existem três formas principais de isolar dados:

1. Dados imutáveis são sempre isolados.
   Como você não pode modificar uma constante,
   não há risco de outro código modificar uma constante
   no mesmo momento em que você a lê.

2. Dados referenciados apenas pela task atual são sempre isolados.
   Uma variável local é segura para ler e escrever
   porque nenhum código fora da task tem uma referência para essa memória,
   então nenhum outro código pode modificar esses dados.
   Além disso,
   se você capturar a variável em uma closure,
   o Swift garante que a closure não seja usada de forma concorrente.

3. Dados protegidos por um actor são isolados
   se o código que acessa esses dados também estiver isolado ao actor.
   Se a função atual está isolada a um actor,
   é seguro ler e escrever os dados protegidos por esse actor,
   porque qualquer outro código isolado a esse mesmo actor
   precisa esperar a sua vez para rodar.

## O main actor

Um actor é um objeto que protege o acesso a dados mutáveis,
forçando o código a se revezar no acesso a esses dados.
O actor mais importante na maioria dos programas é o *main actor*.
Em um app,
o main actor protege todos os dados usados para mostrar a interface.
O main actor alterna o acesso entre a renderização da interface,
o tratamento de eventos da interface
e a execução do código que você escreve e que precisa consultar ou atualizar a interface.

Antes de começar a usar concorrência no seu código,
tudo roda no main actor.
Conforme você identifica código de longa duração ou que consome muitos recursos,
pode tirar esse trabalho do main actor
de uma forma que continua segura e correta.

> Nota:
> O main actor está intimamente relacionado à main thread,
> mas eles não são a mesma coisa.
> O main actor tem estado mutável privado,
> e a main thread serializa o acesso a esse estado.
> Quando você roda código no main actor,
> o Swift executa esse código na main thread.
> Por causa dessa conexão,
> você pode ver esses dois termos usados como sinônimos.
> Seu código interage com o main actor;
> a main thread é um detalhe de implementação de nível mais baixo.

<!--
TODO: Discuss the SE-0478 syntax for 'using @MainActor'

When you're writing UI code,
you often want all of it to be isolated to the main actor.
To do this, you can write `using @MainActor`
at the top of a Swift file to apply that attribute by default
to all the code in the file.
If there's a specific function or property
that you want to exclude from `using @MainActor`,
you can use the `nonisolated` modifier on that declaration
to override the default.
Modules can be configured to be built using `using @MainActor` by default.
This can be overridden on a per-file basis
by writing `using nonisolated` at the top of a file.
-->

Há várias formas de executar trabalho no main actor.
Para garantir que uma função sempre rode no main actor,
marque-a com o atributo `@MainActor`:

```swift
@MainActor
func show(_: Data) {
    // ... UI code to display the photo ...
}
```

No código acima,
o atributo `@MainActor` na função `show(_:)`
exige que essa função rode somente no main actor.
Dentro de outro código que está rodando no main actor,
você pode chamar `show(_:)` como uma função síncrona.
No entanto,
para chamar `show(_:)` a partir de código que não está rodando no main actor,
você precisa incluir `await` e chamá-la como uma função assíncrona,
porque mudar para o main actor introduz um possível ponto de suspensão.
Por exemplo:

```swift
func downloadAndShowPhoto(named name: String) async {
    let photo = await downloadPhoto(named: name)
    await show(photo)
}
```

No código acima,
tanto `downloadPhoto(named:)` quanto `show(_:)`
podem suspender quando você as chama.
Este código também mostra um padrão comum:
execute o trabalho de longa duração e intensivo em CPU em segundo plano,
e depois mude para o main actor para atualizar a interface.
Como a função `downloadAndShowPhoto(named:)` não está no main actor,
o trabalho em `downloadPhoto(named:)` também não roda no main actor.
Apenas o trabalho em `show(_:)` para atualizar a interface roda no main actor,
porque essa função é marcada com o atributo `@MainActor`.
<!-- TODO
When updating for SE-0461,
this is a good place to note
that downloadPhoto(named:) runs
on whatever actor you were on when you called it.
-->

Para garantir que uma closure rode no main actor,
você escreve `@MainActor` antes da lista de captura e antes de `in`,
no início da closure.

```swift
let photo = await downloadPhoto(named: "Trees at Sunrise")
Task { @MainActor in
    show(photo)
}
```

O código acima é parecido com
`downloadAndShowPhoto(named:)` da listagem anterior,
mas o código deste exemplo não espera a atualização da interface.
Você também pode escrever `@MainActor` em uma struct, classe ou enum
para garantir que todos os seus métodos e todo acesso às suas propriedades
rodem no main actor:

```swift
@MainActor
struct PhotoGallery {
    var photoNames: [String]
    func drawUI() { /* ... other UI code ... */ }
}
```

A struct `PhotoGallery` no código acima
desenha as fotos na tela,
usando os nomes da propriedade `photoNames`
para determinar quais fotos exibir.
Como `photoNames` afeta a interface,
o código que a altera precisa rodar no main actor
para serializar esse acesso.

Quando você está construindo sobre um framework,
os protocolos e classes base desse framework
normalmente já são marcados com `@MainActor`,
então você não costuma escrever `@MainActor` nos seus próprios tipos nesse caso.
Aqui está um exemplo simplificado:

```swift
@MainActor
protocol View { /* ... */ }

// Implicitly @MainActor
struct PhotoGalleryView: View { /* ... */ }
```

No código acima,
um framework como o SwiftUI define o protocolo `View`.
Ao escrever `@MainActor` na declaração do protocolo,
tipos como `PhotoGalleryView` que adotam o protocolo
também são marcados implicitamente com `@MainActor`.
O mesmo comportamento aconteceria se `View` fosse uma classe base
e `PhotoGalleryView` fosse uma subclasse ---
a subclasse seria marcada implicitamente com `@MainActor`.

Nos exemplos acima,
`PhotoGallery` protege a struct inteira no main actor.
Para um controle mais refinado,
você pode escrever `@MainActor` apenas nas propriedades ou métodos
que precisam ser acessados ou executados na main thread:

```swift
struct PhotoGallery {
    @MainActor var photoNames: [String]
    var hasCachedPhotos = false

    @MainActor func drawUI() { /* ... UI code ... */ }
    func cachePhotos() { /* ... networking code ... */ }
}
```

Na versão de `PhotoGallery` acima,
o método `drawUI()` desenha as imagens da galeria na tela,
então precisa ser isolado ao main actor.
A propriedade `photoNames` não cria a interface diretamente,
mas armazena o estado que a função `drawUI()` usa para desenhar a interface,
então essa propriedade também precisa ser acessada somente no main actor.
Em contraste,
mudanças na propriedade `hasCachedPhotos`
não interagem com a interface,
e o método `cachePhotos()` não acessa nenhum estado
que exija rodar no main actor.
Por isso, eles não são marcados com `@MainActor`.

Assim como nos exemplos anteriores,
se você estiver usando um framework para construir sua interface,
os property wrappers desse framework
provavelmente já marcam as propriedades de estado da interface como `@MainActor`.
Ao definir um property wrapper,
se a propriedade `wrappedValue` dele for marcada com `@MainActor`,
qualquer propriedade à qual você aplicar esse property wrapper
também fica implicitamente marcada com `@MainActor`.

## Actors

O Swift fornece o main actor para você ---
você também pode definir os seus próprios actors.
Actors permitem compartilhar informações com segurança entre código concorrente.

Assim como classes, actors são tipos por referência,
então a comparação entre tipos por valor e tipos por referência
em <doc:ClassesAndStructures#Classes-Are-Reference-Types>
vale para actors tanto quanto para classes.
Diferente de classes,
actors permitem que apenas uma task acesse o estado mutável deles por vez,
o que torna seguro que código de várias tasks
interaja com a mesma instância de um actor.
Por exemplo, aqui está um actor que registra temperaturas:

```swift
actor TemperatureLogger {
    let label: String
    var measurements: [Int]
    private(set) var max: Int

    init(label: String, measurement: Int) {
        self.label = label
        self.measurements = [measurement]
        self.max = measurement
    }
}
```

<!--
  - test: `actors, actors-implicitly-sendable`

  ```swifttest
  -> actor TemperatureLogger {
         let label: String
         var measurements: [Int]
         private(set) var max: Int

         init(label: String, measurement: Int) {
             self.label = label
             self.measurements = [measurement]
             self.max = measurement
         }
     }
  ```
-->

Você declara um actor com a palavra-chave `actor`,
seguida da definição entre um par de chaves.
O actor `TemperatureLogger` tem propriedades
que outro código fora do actor pode acessar,
e restringe a propriedade `max` para que somente código dentro do actor
possa atualizar o valor máximo.

Você cria uma instância de um actor
usando a mesma sintaxe de inicializador de structs e classes.
Ao acessar uma propriedade ou método de um actor,
você usa `await` para marcar o possível ponto de suspensão.
Por exemplo:

```swift
let logger = TemperatureLogger(label: "Outdoors", measurement: 25)
print(await logger.max)
// Prints "25".
```

Neste exemplo,
acessar `logger.max` é um possível ponto de suspensão.
Como o actor permite que apenas uma task por vez acesse o estado mutável,
se código de outra task já estiver interagindo com o logger,
este código fica suspenso enquanto espera para acessar a propriedade.

Em contraste,
código que faz parte do actor não escreve `await`
ao acessar as propriedades do actor.
Por exemplo,
aqui está um método que atualiza um `TemperatureLogger` com uma nova temperatura:

```swift
extension TemperatureLogger {
    func update(with measurement: Int) {
        measurements.append(measurement)
        if measurement > max {
            max = measurement
        }
    }
}
```

O método `update(with:)` já está rodando no actor,
então ele não marca o acesso às propriedades como `max` com `await`.
Este método também mostra um dos motivos
pelos quais os actors permitem que apenas uma task por vez interaja com o estado mutável:
algumas atualizações do estado de um actor quebram temporariamente invariantes.
O actor `TemperatureLogger` mantém uma lista de temperaturas
e uma temperatura máxima,
e atualiza a temperatura máxima quando você registra uma nova medição.
No meio da atualização,
depois de acrescentar a nova medição, mas antes de atualizar `max`,
o logger de temperatura está em um estado temporário inconsistente.
Impedir que várias tasks interajam com a mesma instância ao mesmo tempo
evita problemas como a seguinte sequência de eventos:

1. O seu código chama o método `update(with:)`.
   Ele atualiza primeiro o array `measurements`.
2. Antes que o seu código consiga atualizar `max`,
   outro código lê o valor máximo e o array de temperaturas.
3. O seu código termina a atualização alterando `max`.

Nesse caso, o código que roda em outro lugar leria informações incorretas,
porque o acesso dele ao actor foi intercalado
no meio da chamada a `update(with:)`,
enquanto os dados estavam temporariamente inválidos.
Você pode evitar esse problema ao usar actors do Swift,
porque eles permitem apenas uma operação sobre o estado por vez,
e porque esse código só pode ser interrompido
nos lugares em que `await` marca um ponto de suspensão.
Como `update(with:)` não contém nenhum ponto de suspensão,
nenhum outro código pode acessar os dados no meio de uma atualização.

Se código fora do actor tentar acessar essas propriedades diretamente,
como acessar as propriedades de uma struct ou classe,
você receberá um erro em tempo de compilação.
Por exemplo:

```swift
print(logger.max)  // Error
```

Acessar `logger.max` sem escrever `await` falha porque
as propriedades de um actor fazem parte do estado local isolado desse actor.
O código para acessar essa propriedade precisa rodar como parte do actor,
o que é uma operação assíncrona e exige escrever `await`.
O Swift garante que
somente código rodando em um actor pode acessar o estado local desse actor.
Essa garantia é conhecida como *isolamento de actor*.

Os seguintes aspectos do modelo de concorrência do Swift
trabalham juntos para facilitar o raciocínio sobre estado mutável compartilhado:

- O código entre os possíveis pontos de suspensão roda de forma sequencial,
  sem a possibilidade de ser interrompido por outro código concorrente.
  No entanto,
  vários trechos de código concorrente podem rodar ao mesmo tempo,
  então outro código pode estar rodando simultaneamente.

- O código que interage com o estado local de um actor
  roda somente nesse actor.

- Um actor executa apenas um trecho de código por vez.

Por causa dessas garantias,
código que não inclui `await` e que está dentro de um actor
pode fazer as atualizações sem o risco de outros pontos do programa
observarem o estado temporariamente inválido.
Por exemplo,
o código abaixo converte temperaturas medidas de Fahrenheit para Celsius:

```swift
extension TemperatureLogger {
    func convertFahrenheitToCelsius() {
        for i in measurements.indices {
            measurements[i] = (measurements[i] - 32) * 5 / 9
        }
    }
}
```

O código acima converte o array de medições, uma por vez.
Enquanto a operação de conversão está em andamento,
algumas temperaturas estão em Fahrenheit e outras em Celsius.
No entanto, como nenhum dos códigos contém `await`,
não há pontos de suspensão possíveis nesse método.
O estado que esse método modifica pertence ao actor,
que o protege contra código que o leia ou modifique,
exceto quando esse código roda no actor.
Isso significa que não há como outro código
ler uma lista de temperaturas parcialmente convertidas
enquanto a conversão de unidades está em andamento.

Além de escrever código em um actor
que protege estados temporariamente inválidos ao omitir pontos de suspensão possíveis,
você pode mover esse código para um método síncrono.
O método `convertFahrenheitToCelsius()` acima é um método síncrono,
então é garantido que ele *nunca* contenha pontos de suspensão possíveis.
Essa função encapsula o código
que torna temporariamente o modelo de dados inconsistente,
e facilita para quem lê o código reconhecer
que nenhum outro código pode rodar
antes de a consistência dos dados ser restaurada com a conclusão do trabalho.
É importante que o Swift não troque de execução deste código
para rodar código de outra parte do programa
durante esse período.
No futuro,
se você tentar adicionar código concorrente a essa função,
introduzindo um possível ponto de suspensão,
você receberá um erro em tempo de compilação em vez de introduzir um bug.


## Global actors

O main actor é uma instância global única do tipo [`MainActor`][].
Um actor normalmente pode ter várias instâncias,
cada uma fornecendo um isolamento independente.
É por isso que você declara todos os dados isolados de um actor
como propriedades de instância desse actor.
No entanto, como `MainActor` é um singleton ---
existe somente uma instância desse tipo ---
o tipo sozinho basta para identificar o actor,
permitindo marcar o isolamento no main actor usando apenas um atributo.
Essa abordagem dá mais flexibilidade para organizar o seu código
da forma que funciona melhor para você.

[`MainActor`]: https://developer.apple.com/documentation/swift/mainactor

Você pode definir os seus próprios global actors singleton
usando o atributo `@globalActor`,
como descrito em <doc:Attributes#globalActor>.


<!--
  OUTLINE

  Add this post-WWDC when we have a more solid story to tell around Sendable

   .. _Concurrency_ActorIsolation:

   Actor Isolation

   TODO outline impact from SE-0313 Control Over Actor Isolation
   about the 'isolated' and 'nonisolated' keywords

   - actors protect their mutable state using :newTerm:`actor isolation`
   to prevent data races
   (one actor reading data that's in an inconsistent state
   while another actor is updating/writing to that data)

   - within an actor's implementation,
   you can read and write to properties of ``self`` synchronously,
   likewise for calling methods of ``self`` or ``super``

   - method calls from outside the actor are always async,
   as is reading the value of an actor's property

   - you can't write to a property directly from outside the actor

   - The same actor method can be called multiple times, overlapping itself.
   This is sometimes referred to as *reentrant code*.
   The behavior is defined and safe... but might have unexpected results.
   However, the actor model doesn't require or guarantee
   that these overlapping calls behave correctly (that they're *idempotent*).
   Encapsulate state changes in a synchronous function
   or write them so they don't contain an ``await`` in the middle.

   - If a closure is ``@Sendable`` or ``@escaping``
   then it behaves like code outside of the actor
   because it could execute concurrently with other code that's part of the actor

   exercise the log actor, using its client API to mutate state

   ::

       let logger = TemperatureSensor(lines: [
           "Outdoor air temperature",
           "25 C",
           "24 C",
       ])
       print(await logger.getMax())

       await logger.update(with: "27 C")
       print(await logger.getMax())
-->

## Tipos Sendable

Tasks e actors permitem dividir um programa
em partes que podem rodar de forma concorrente com segurança.
Dentro de uma task ou de uma instância de um actor,
a parte do programa que contém estado mutável,
como variáveis e propriedades,
é chamada de *domínio de concorrência*.
Alguns tipos de dados não podem ser compartilhados entre domínios de concorrência,
porque esses dados contêm estado mutável,
mas não protegem contra acesso sobreposto.

Um tipo que pode ser compartilhado de um domínio de concorrência para outro
é conhecido como tipo *sendable*.
Por exemplo, ele pode ser passado como argumento ao chamar um método de actor
ou ser retornado como resultado de uma task.
Os exemplos anteriores neste capítulo não discutiram sendability
porque usam tipos por valor simples,
que são sempre seguros para compartilhar
pelos dados passados entre domínios de concorrência.
Em contraste,
alguns tipos não são seguros para passar entre domínios de concorrência.
Por exemplo, uma classe que contém propriedades mutáveis
e não serializa o acesso a essas propriedades
pode produzir resultados imprevisíveis e incorretos
quando você passa instâncias dessa classe entre tasks diferentes.

Você marca um tipo como sendable
declarando conformidade com o protocolo `Sendable`.
Esse protocolo não tem nenhum requisito de código,
mas tem requisitos semânticos que o Swift verifica.
Em geral, há três formas de um tipo ser sendable:

- O tipo é um tipo por valor,
  e o seu estado mutável é formado por outros dados sendable ---
  por exemplo, uma struct com propriedades armazenadas que são sendable
  ou um enum com valores associados que são sendable.
- O tipo não tem nenhum estado mutável,
  e o seu estado imutável é formado por outros dados sendable ---
  por exemplo, uma struct ou classe que tem apenas propriedades somente leitura.
- O tipo tem código que garante a segurança do seu estado mutável,
  como uma classe marcada com `@MainActor`
  ou uma classe que serializa o acesso às suas propriedades
  em uma thread ou fila específica.

<!--
  There's no example of the third case,
  where you serialize access to the class's members,
  because the stdlib doesn't include the locking primitives you'd need.
  Implementing it in terms of NSLock or some Darwin API
  isn't a good fit for TSPL.
  Implementing it in terms of isKnownUniquelyReferenced(_:)
  and copy-on-write is also probably too involved for TSPL.
-->

Para uma lista detalhada dos requisitos semânticos,
veja a referência do protocolo [`Sendable`](https://developer.apple.com/documentation/swift/sendable).

Alguns tipos são sempre sendable,
como structs que têm apenas propriedades sendable
e enums que têm apenas valores associados sendable.
Por exemplo:

```swift
struct TemperatureReading: Sendable {
    var measurement: Int
}

extension TemperatureLogger {
    func addReading(from reading: TemperatureReading) {
        measurements.append(reading.measurement)
    }
}

let logger = TemperatureLogger(label: "Tea kettle", measurement: 85)
let reading = TemperatureReading(measurement: 45)
await logger.addReading(from: reading)
```

<!--
  - test: `actors`

  ```swifttest
  -> struct TemperatureReading: Sendable {
         var measurement: Int
     }

  -> extension TemperatureLogger {
         func addReading(from reading: TemperatureReading) {
             measurements.append(reading.measurement)
         }
     }

  -> let logger = TemperatureLogger(label: "Tea kettle", measurement: 85)
  -> let reading = TemperatureReading(measurement: 45)
  -> await logger.addReading(from: reading)
  ```
-->

Como `TemperatureReading` é uma struct que tem apenas propriedades sendable,
e a struct não é marcada como `public` nem como `@usableFromInline`,
ela é implicitamente sendable.
Aqui está uma versão da struct
em que a conformidade com o protocolo `Sendable` é implícita:

```swift
struct TemperatureReading {
    var measurement: Int
}
```

<!--
  - test: `actors-implicitly-sendable`

  ```swifttest
  -> struct TemperatureReading {
         var measurement: Int
     }
  ```
-->

Para marcar explicitamente um tipo como não sendable,
escreva uma conformidade indisponível com `Sendable`:

```swift
struct FileDescriptor {
    let rawValue: Int
}

@available(*, unavailable)
extension FileDescriptor: Sendable {}
```

<!--
The example above is based on a Swift System API.
https://github.com/apple/swift-system/blob/main/Sources/System/FileDescriptor.swift

See also this PR that adds Sendable conformance to FileDescriptor:
https://github.com/apple/swift-system/pull/112
-->

Você também pode usar uma conformidade indisponível
para suprimir a conformidade implícita a um protocolo,
como discutido em <doc:Protocols#Implicit-Conformance-to-a-Protocol>.

<!--
  LEFTOVER OUTLINE BITS

  - like classes, actors can inherit from other actors

  - actors can also inherit from ``NSObject``,
  which lets you mark them ``@objc`` and do interop stuff with them

  - every actor implicitly conforms to the ``Actor`` protocol,
  which has no requirements

  - you can use the ``Actor`` protocol to write code that's generic across actors

  - In the future, when we get distributed actors,
    the TemperatureSensor example
    might be a good example to expand when explaining them.

  ::

      while let result = try await group.next() { }
      for try await result in group { }

  how much should you have to understand threads to understand this?
  Ideally you don't have to know anything about them.

  How do you meld async-await-Task-Actor with an event driven model?
  Can you feed your user events through an async sequence or Combine
  and then use for-await-in to spin an event loop?
  I think so --- but how do you get the events *into* the async sequence?

  Probably don't cover unsafe continuations (SE-0300) in TSPL,
  but maybe link to them?
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
