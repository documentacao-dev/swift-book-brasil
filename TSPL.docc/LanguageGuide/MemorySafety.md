# Segurança de memória

Estruture seu código para evitar conflitos ao acessar a memória.

Por padrão, o Swift impede que comportamentos inseguros aconteçam no seu código.
Por exemplo,
o Swift garante que variáveis sejam inicializadas antes de serem usadas,
que a memória não seja acessada depois de liberada,
e que os índices de array sejam verificados contra erros de limites.

O Swift também garante que vários acessos
à mesma área da memória não entrem em conflito,
exigindo que o código que modifica um local da memória
tenha acesso exclusivo a essa memória.
Como o Swift gerencia a memória automaticamente,
na maior parte do tempo você não precisa pensar em acessar memória.
No entanto,
é importante entender onde podem ocorrer conflitos,
para que você evite escrever código com acesso conflitante à memória.
Se o seu código contiver conflitos,
você receberá um erro em tempo de compilação ou em tempo de execução.

<!--
  TODO: maybe re-introduce this text...

  Memory safety refers to...
  The term *safety* usually refers to :newTerm:`memory safety`...
  Unsafe access to memory is available, if you ask for it explicitly...
-->

## Entendendo o acesso conflitante à memória

Acessos à memória acontecem no seu código
quando você faz coisas como definir o valor de uma variável
ou passar um argumento para uma função.
Por exemplo,
o código a seguir contém um acesso de leitura e um acesso de escrita:

```swift
// A write access to the memory where one is stored.
var one = 1

// A read access from the memory where one is stored.
print("We're number \(one)!")
```

<!--
  - test: `memory-read-write`

  ```swifttest
  // A write access to the memory where one is stored.
  -> var one = 1

  // A read access from the memory where one is stored.
  -> print("We're number \(one)!")
  << We're number 1!
  ```
-->

<!--
  Might be worth a different example,
  or else I'm going to keep getting "We are Number One" stuck in my head.
-->

Um acesso conflitante à memória pode acontecer
quando partes diferentes do código tentam
acessar o mesmo local da memória ao mesmo tempo.
Vários acessos ao mesmo local da memória ao mesmo tempo
podem produzir um comportamento imprevisível ou inconsistente.
No Swift, há maneiras de modificar um valor
que se estendem por várias linhas de código,
o que torna possível tentar acessar um valor
no meio da própria modificação.

Você pode ver um problema parecido
pensando em como atualizar um orçamento
escrito em uma folha de papel.
Atualizar o orçamento é um processo de duas etapas:
primeiro você acrescenta os nomes e os preços dos itens,
e depois altera o valor total
para refletir os itens que estão na lista no momento.
Antes e depois da atualização,
você pode ler qualquer informação do orçamento
e obter uma resposta correta,
como mostra a figura abaixo.

![](memory_shopping)

Enquanto você acrescenta itens ao orçamento,
ele está em um estado temporário e inválido,
porque o valor total ainda não foi atualizado
para refletir os itens recém-acrescentados.
Ler o valor total
durante o processo de acrescentar um item
fornece uma informação incorreta.

Este exemplo também mostra um desafio
que você pode encontrar ao corrigir acessos conflitantes à memória:
às vezes há mais de uma forma de corrigir o conflito,
e cada uma produz uma resposta diferente,
e nem sempre é óbvio qual resposta está correta.
Neste exemplo,
dependendo de você querer o valor total original
ou o valor total atualizado,
tanto $5 quanto $320 podem ser a resposta correta.
Antes de corrigir o acesso conflitante,
você precisa determinar o que ele deveria fazer.

> Nota: Se você já escreveu código concorrente ou multithread,
> o acesso conflitante à memória pode ser um problema familiar.
> No entanto,
> o acesso conflitante discutido aqui pode acontecer
> em uma única thread e
> *não* envolve código concorrente nem multithread.
>
> Se houver acesso conflitante à memória
> dentro de uma única thread,
> o Swift garante que você receberá um erro
> em tempo de compilação ou em tempo de execução.
> Para código multithread,
> use o [Thread Sanitizer](https://developer.apple.com/documentation/xcode/diagnosing_memory_thread_and_crash_issues_early)
> para ajudar a detectar acessos conflitantes entre threads.

<!--
  TODO: The xref above doesn't seem to give enough information.
  What should I be looking for when I get to the linked page?
-->

### Características do acesso à memória

Há três características do acesso à memória
a considerar no contexto de acesso conflitante:
se o acesso é de leitura ou de escrita,
a duração do acesso
e o local da memória acessado.
Especificamente,
existe um conflito quando há dois acessos
que atendem a todas as condições a seguir:

- Os acessos não são ambos de leitura, e não são ambos atômicos.
- Eles acessam o mesmo local da memória.
- As durações deles se sobrepõem.

A diferença entre acesso de leitura e de escrita
geralmente é óbvia:
um acesso de escrita altera o local da memória,
mas um acesso de leitura não altera.
O local da memória
se refere ao que está sendo acessado ---
por exemplo, uma variável, constante ou propriedade.
A duração de um acesso à memória
é instantânea ou de longo prazo.

Um acesso é *atômico* se
for uma chamada a uma operação atômica em [`Atomic`] ou [`AtomicLazyReference`],
ou se usar apenas operações atômicas do C;
caso contrário, ele é não atômico.
Para uma lista de funções atômicas do C, veja a página de manual `stdatomic(3)`.

[`Atomic`]: https://developer.apple.com/documentation/synchronization/atomic
[`AtomicLazyReference`]: https://developer.apple.com/documentation/synchronization/atomiclazyreference

<!--
  Using the C atomic functions from Swift
  requires some shimming that's out of scope for TSPL - for example:
  https://github.com/apple/swift-atomics/tree/main/Sources/_AtomicsShims
-->

Um acesso é *instantâneo*
se não for possível que outro código seja executado
depois que esse acesso começa, mas antes de ele terminar.
Por natureza, dois acessos instantâneos não podem acontecer ao mesmo tempo.
A maior parte dos acessos à memória é instantânea.
Por exemplo,
todos os acessos de leitura e de escrita no código abaixo são instantâneos:

```swift
func oneMore(than number: Int) -> Int {
    return number + 1
}

var myNumber = 1
myNumber = oneMore(than: myNumber)
print(myNumber)
// Prints "2".
```

<!--
  - test: `memory-instantaneous`

  ```swifttest
  -> func oneMore(than number: Int) -> Int {
         return number + 1
     }

  -> var myNumber = 1
  -> myNumber = oneMore(than: myNumber)
  -> print(myNumber)
  <- 2
  ```
-->

No entanto,
há várias formas de acessar a memória,
chamadas acessos de *longo prazo*,
que se estendem pela execução de outro código.
A diferença entre acesso instantâneo e acesso de longo prazo
é que pode ser que outro código seja executado
depois que um acesso de longo prazo começa, mas antes de ele terminar,
o que se chama *sobreposição*.
Um acesso de longo prazo pode se sobrepor
a outros acessos de longo prazo e a acessos instantâneos.

Sobreposições aparecem principalmente em código que usa
parâmetros in-out em funções e métodos,
ou métodos mutating de uma struct.
Os tipos específicos de código Swift que usam acessos de longo prazo
são discutidos nas seções a seguir.

## Acesso conflitante a parâmetros in-out

Uma função tem acesso de escrita de longo prazo
a todos os seus parâmetros in-out.
O acesso de escrita de um parâmetro in-out começa
depois que todos os parâmetros que não são in-out foram avaliados
e dura por toda a chamada da função.
Se houver vários parâmetros in-out,
os acessos de escrita começam na mesma ordem em que os parâmetros aparecem.

Uma consequência desse acesso de escrita de longo prazo
é que você não pode acessar a variável original
que foi passada como in-out,
mesmo que as regras de escopo e de controle de acesso permitissem ---
qualquer acesso à original cria um conflito.
Por exemplo:

```swift
var stepSize = 1

func increment(_ number: inout Int) {
    number += stepSize
}

increment(&stepSize)
// Error: Conflicting accesses to stepSize.
```

<!--
  - test: `memory-increment`

  ```swifttest
  -> var stepSize = 1

  -> func increment(_ number: inout Int) {
         number += stepSize
     }

  -> increment(&stepSize)
  // Error: Conflicting accesses to stepSize.
  xx Simultaneous accesses to 0x10e8667d8, but modification requires exclusive access.
  xx Previous access (a modification) started at  (0x10e86b032).
  xx Current access (a read) started at:
  ```
-->

No código acima,
`stepSize` é uma variável global,
e normalmente ela é acessível de dentro de `increment(_:)`.
No entanto,
o acesso de leitura a `stepSize` se sobrepõe
ao acesso de escrita a `number`.
Como mostra a figura abaixo,
tanto `number` quanto `stepSize` se referem ao mesmo local da memória.
Os acessos de leitura e de escrita
se referem à mesma memória e se sobrepõem,
o que produz um conflito.

![](memory_increment)

Uma forma de resolver esse conflito
é fazer uma cópia explícita de `stepSize`:

```swift
// Make an explicit copy.
var copyOfStepSize = stepSize
increment(&copyOfStepSize)

// Update the original.
stepSize = copyOfStepSize
// stepSize is now 2
```

<!--
  - test: `memory-increment-copy`

  ```swifttest
  >> var stepSize = 1
  >> func increment(_ number: inout Int) {
  >>     number += stepSize
  >> }
  // Make an explicit copy.
  -> var copyOfStepSize = stepSize
  -> increment(&copyOfStepSize)

  // Update the original.
  -> stepSize = copyOfStepSize
  /> stepSize is now \(stepSize)
  </ stepSize is now 2
  ```
-->

Quando você faz uma cópia de `stepSize` antes de chamar `increment(_:)`,
fica claro que o valor de `copyOfStepSize` é incrementado
pelo tamanho do passo atual.
O acesso de leitura termina antes de o acesso de escrita começar,
então não há conflito.

Outra consequência do acesso de escrita de longo prazo
aos parâmetros in-out é que
passar uma mesma variável como argumento de vários parâmetros in-out
da mesma função
produz um conflito.
Por exemplo:

```swift
func balance(_ x: inout Int, _ y: inout Int) {
    let sum = x + y
    x = sum / 2
    y = sum - x
}
var playerOneScore = 42
var playerTwoScore = 30
balance(&playerOneScore, &playerTwoScore)  // OK
balance(&playerOneScore, &playerOneScore)
// Error: Conflicting accesses to playerOneScore.
```

<!--
  - test: `memory-balance`

  ```swifttest
  -> func balance(_ x: inout Int, _ y: inout Int) {
         let sum = x + y
         x = sum / 2
         y = sum - x
     }
  -> var playerOneScore = 42
  -> var playerTwoScore = 30
  -> balance(&playerOneScore, &playerTwoScore)  // OK
  -> balance(&playerOneScore, &playerOneScore)
  // Error: Conflicting accesses to playerOneScore.
  !$ error: inout arguments are not allowed to alias each other
  !! balance(&playerOneScore, &playerOneScore)
  !!                          ^~~~~~~~~~~~~~~
  !$ note: previous aliasing argument
  !! balance(&playerOneScore, &playerOneScore)
  !!         ^~~~~~~~~~~~~~~
  !$ error: overlapping accesses to 'playerOneScore', but modification requires exclusive access; consider copying to a local variable
  !! balance(&playerOneScore, &playerOneScore)
  !!                          ^~~~~~~~~~~~~~~
  !$ note: conflicting access is here
  !! balance(&playerOneScore, &playerOneScore)
  !!         ^~~~~~~~~~~~~~~
  ```
-->

A função `balance(_:_:)` acima
modifica seus dois parâmetros
para dividir o valor total igualmente entre eles.
Chamá-la com `playerOneScore` e `playerTwoScore` como argumentos
não produz conflito ---
há dois acessos de escrita que se sobrepõem no tempo,
mas eles acessam locais diferentes da memória.
Em contraste,
passar `playerOneScore` como valor para os dois parâmetros
produz um conflito,
porque tenta fazer dois acessos de escrita
ao mesmo local da memória ao mesmo tempo.

> Nota: Como operadores são funções,
> eles também podem ter acessos de longo prazo aos seus parâmetros in-out.
> Por exemplo, se `balance(_:_:)` fosse uma função operadora chamada `<^>`,
> escrever `playerOneScore <^> playerOneScore`
> resultaria no mesmo conflito
> que `balance(&playerOneScore, &playerOneScore)`.

## Acesso conflitante a self em métodos

<!--
  This (probably?) applies to all value types,
  but structures are the only place you can observe it.
  Enumerations can have mutating methods
  but you can't mutate their associated values in place,
  and tuples can't have methods.
-->

<!--
  Methods behave like self is passed to the method as inout
  because, under the hood, that's exactly what happens.
-->

Um método mutating de uma struct tem acesso de escrita a `self`
durante toda a chamada do método.
Por exemplo, considere um jogo em que cada jogador
tem uma quantidade de vida, que diminui ao receber dano,
e uma quantidade de energia, que diminui ao usar habilidades especiais.

```swift
struct Player {
    var name: String
    var health: Int
    var energy: Int

    static let maxHealth = 10
    mutating func restoreHealth() {
        health = Player.maxHealth
    }
}
```

<!--
  - test: `memory-player-share-with-self`

  ```swifttest
  >> func balance(_ x: inout Int, _ y: inout Int) {
  >>     let sum = x + y
  >>     x = sum / 2
  >>     y = sum - x
  >> }
  -> struct Player {
         var name: String
         var health: Int
         var energy: Int

         static let maxHealth = 10
         mutating func restoreHealth() {
             health = Player.maxHealth
         }
     }
  ```
-->

No método `restoreHealth()` acima,
um acesso de escrita a `self` começa no início do método
e dura até o método retornar.
Nesse caso, não há outro código
dentro de `restoreHealth()`
que possa ter um acesso sobreposto às propriedades de uma instância de `Player`.
O método `shareHealth(with:)` abaixo
recebe outra instância de `Player` como parâmetro in-out,
criando a possibilidade de acessos sobrepostos.

```swift
extension Player {
    mutating func shareHealth(with teammate: inout Player) {
        balance(&teammate.health, &health)
    }
}

var oscar = Player(name: "Oscar", health: 10, energy: 10)
var maria = Player(name: "Maria", health: 5, energy: 10)
oscar.shareHealth(with: &maria)  // OK
```

<!--
  - test: `memory-player-share-with-self`

  ```swifttest
  -> extension Player {
         mutating func shareHealth(with teammate: inout Player) {
             balance(&teammate.health, &health)
         }
     }

  -> var oscar = Player(name: "Oscar", health: 10, energy: 10)
  -> var maria = Player(name: "Maria", health: 5, energy: 10)
  -> oscar.shareHealth(with: &maria)  // OK
  ```
-->

No exemplo acima,
chamar o método `shareHealth(with:)`
para que o jogador da Oscar compartilhe vida com o jogador da Maria
não causa conflito.
Há um acesso de escrita a `oscar` durante a chamada do método
porque `oscar` é o valor de `self` em um método mutating,
e há um acesso de escrita a `maria`
pela mesma duração
porque `maria` foi passada como parâmetro in-out.
Como mostra a figura abaixo,
eles acessam locais diferentes da memória.
Mesmo que os dois acessos de escrita se sobreponham no tempo,
eles não entram em conflito.

![](memory_share_health_maria)

No entanto,
se você passar `oscar` como argumento para `shareHealth(with:)`,
há um conflito:

```swift
oscar.shareHealth(with: &oscar)
// Error: Conflicting accesses to oscar.
```

<!--
  - test: `memory-player-share-with-self`

  ```swifttest
  -> oscar.shareHealth(with: &oscar)
  // Error: Conflicting accesses to oscar.
  !$ error: inout arguments are not allowed to alias each other
  !! oscar.shareHealth(with: &oscar)
  !!                         ^~~~~~
  !$ note: previous aliasing argument
  !! oscar.shareHealth(with: &oscar)
  !! ^~~~~
  !$ error: overlapping accesses to 'oscar', but modification requires exclusive access; consider copying to a local variable
  !! oscar.shareHealth(with: &oscar)
  !!                          ^~~~~
  !$ note: conflicting access is here
  !! oscar.shareHealth(with: &oscar)
  !! ^~~~~~
  ```
-->

O método mutating precisa de acesso de escrita a `self`
durante toda a duração do método,
e o parâmetro in-out precisa de acesso de escrita a `teammate`
pela mesma duração.
Dentro do método,
tanto `self` quanto `teammate` se referem ao
mesmo local da memória ---
como mostra a figura abaixo.
Os dois acessos de escrita
se referem à mesma memória e se sobrepõem,
o que produz um conflito.

![](memory_share_health_oscar)

## Acesso conflitante a propriedades

Tipos como structs, tuplas e enums
são formados por valores constituintes individuais,
como as propriedades de uma struct ou os elementos de uma tupla.
Como são tipos por valor, modificar qualquer parte do valor
modifica o valor inteiro,
o que significa que o acesso de leitura ou de escrita a uma das propriedades
exige acesso de leitura ou de escrita ao valor inteiro.
Por exemplo,
acessos de escrita sobrepostos aos elementos de uma tupla
produzem um conflito:

```swift
var playerInformation = (health: 10, energy: 20)
balance(&playerInformation.health, &playerInformation.energy)
// Error: Conflicting access to properties of playerInformation.
```

<!--
  - test: `memory-tuple`

  ```swifttest
  >> func balance(_ x: inout Int, _ y: inout Int) {
  >>     let sum = x + y
  >>     x = sum / 2
  >>     y = sum - x
  >> }
  -> var playerInformation = (health: 10, energy: 20)
  -> balance(&playerInformation.health, &playerInformation.energy)
  // Error: Conflicting access to properties of playerInformation.
  xx Simultaneous accesses to 0x10794d848, but modification requires exclusive access.
  xx Previous access (a modification) started at  (0x107952037).
  xx Current access (a modification) started at:
  ```
-->

No exemplo acima,
chamar `balance(_:_:)` nos elementos de uma tupla
produz um conflito
porque há acessos de escrita sobrepostos a `playerInformation`.
Tanto `playerInformation.health` quanto `playerInformation.energy`
são passados como parâmetros in-out,
o que significa que `balance(_:_:)` precisa de acesso de escrita a eles
durante toda a chamada da função.
Nos dois casos, um acesso de escrita a um elemento da tupla
exige um acesso de escrita à tupla inteira.
Isso significa que há dois acessos de escrita a `playerInformation`
com durações sobrepostas,
o que causa um conflito.

O código abaixo mostra que o mesmo erro aparece
em acessos de escrita sobrepostos
às propriedades de uma struct
armazenada em uma variável global.

```swift
var holly = Player(name: "Holly", health: 10, energy: 10)
balance(&holly.health, &holly.energy)  // Error
```

<!--
  - test: `memory-share-health-global`

  ```swifttest
  >> struct Player {
  >>     var name: String
  >>     var health: Int
  >>     var energy: Int
  >> }
  >> func balance(_ x: inout Int, _ y: inout Int) {
  >>     let sum = x + y
  >>     x = sum / 2
  >>     y = sum - x
  >> }
  -> var holly = Player(name: "Holly", health: 10, energy: 10)
  -> balance(&holly.health, &holly.energy)  // Error
  xx Simultaneous accesses to 0x10794d848, but modification requires exclusive access.
  xx Previous access (a modification) started at  (0x107952037).
  xx Current access (a modification) started at:
  ```
-->

Na prática,
a maioria dos acessos às propriedades de uma struct
pode se sobrepor com segurança.
Por exemplo,
se a variável `holly` no exemplo acima
for trocada por uma variável local em vez de uma variável global,
o compilador consegue provar que o acesso sobreposto
às propriedades armazenadas da struct é seguro:

```swift
func someFunction() {
    var oscar = Player(name: "Oscar", health: 10, energy: 10)
    balance(&oscar.health, &oscar.energy)  // OK
}
```

<!--
  - test: `memory-share-health-local`

  ```swifttest
  >> struct Player {
  >>     var name: String
  >>     var health: Int
  >>     var energy: Int
  >> }
  >> func balance(_ x: inout Int, _ y: inout Int) {
  >>     let sum = x + y
  >>     x = sum / 2
  >>     y = sum - x
  >> }
  -> func someFunction() {
         var oscar = Player(name: "Oscar", health: 10, energy: 10)
         balance(&oscar.health, &oscar.energy)  // OK
     }
  >> someFunction()
  ```
-->

No exemplo acima,
a vida e a energia do Oscar são passadas
como os dois parâmetros in-out de `balance(_:_:)`.
O compilador consegue provar que a segurança de memória é preservada
porque as duas propriedades armazenadas não interagem de nenhuma forma.

A restrição contra
o acesso sobreposto às propriedades de uma struct
nem sempre é necessária para preservar a segurança de memória.
A segurança de memória é a garantia desejada,
mas o acesso exclusivo é um requisito mais rígido do que a segurança de memória ---
o que significa que algum código preserva a segurança de memória,
mesmo violando o acesso exclusivo à memória.
O Swift permite esse código seguro para a memória se o compilador conseguir provar
que o acesso não exclusivo à memória ainda é seguro.
Especificamente, ele consegue provar
que o acesso sobreposto às propriedades de uma struct é seguro
se as condições a seguir forem atendidas:

- Você está acessando apenas propriedades armazenadas de uma instância,
  não propriedades computadas nem propriedades de classe.
- A struct é o valor de uma variável local,
  não de uma variável global.
- A struct não é capturada por nenhuma closure,
  ou é capturada apenas por closures *nonescaping*.

Se o compilador não conseguir provar que o acesso é seguro,
ele não permite o acesso.

<!--
  Because there's no syntax
  to mutate an enum's associated value in place,
  we can't show that overlapping mutations
  to two different associated values on the same enum
  would violate exclusivity.
  Otherwise, we'd want an example of that
  in this section too --
  it's the moral equivalent of property access.
-->

<!--
  .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
-->

<!--
  In Swift 4, the only way to create a long-term read
  is to use implicit pointer conversion
  when passing a value as a nonmutating unsafe pointer parameter,
  as in the example below.
  There's discussion in <rdar://problem/33115142>
  about changing the semantics of nonmutating method calls
  to be long-term reads,
  but it's not clear if/when that change will land.

  ::

      var global = 4

      func foo(_ x: UnsafePointer<Int>){
          global = 7
      }

      foo(&global)
      print(global)

      // Simultaneous accesses to 0x106761618, but modification requires exclusive access.
      // Previous access (a read) started at temp2`main + 87 (0x10675e417).
      // Current access (a modification) started at:
      // 0    libswiftCore.dylib                 0x0000000106ac7b90 swift_beginAccess + 605
      // 1    temp2                              0x000000010675e500 foo(_:) + 39
      // 2    temp2                              0x000000010675e3c0 main + 102
      // 3    libdyld.dylib                      0x00007fff69c75144 start + 1
      // Fatal access conflict detected.
-->

<!--
  TEXT FOR THE FUTURE

  Versions of Swift before Swift 5 ensure memory safety
  by aggressively making a copy of the shared mutable state
  when a conflicting access is possible.
  The copy is no longer shared, preventing the possibility of conflicts.
  However, the copying approach has a negative impact
  on performance and memory usage.
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
