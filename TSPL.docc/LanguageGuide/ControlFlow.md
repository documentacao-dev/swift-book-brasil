# Controle de fluxo

Estruture o código com ramos, laços e saídas antecipadas.

O Swift oferece uma variedade de instruções de controle de fluxo.
Entre elas estão os laços `while`, para executar uma tarefa várias vezes;
as instruções `if`, `guard` e `switch`, para executar ramos diferentes de código
de acordo com certas condições;
e instruções como `break` e `continue`, para transferir o fluxo de execução
para outro ponto do seu código.
O Swift oferece um laço `for`-`in` que facilita percorrer
arrays, dicionários, intervalos, strings e outras sequências.
O Swift também oferece instruções `defer`,
que envolvem código a ser executado ao sair do escopo atual.

A instrução `switch` do Swift é bem mais poderosa
do que a equivalente em muitas linguagens da família C.
Os casos podem corresponder a muitos padrões diferentes,
incluindo correspondências em intervalos, tuplas e conversões para um tipo específico.
Os valores correspondidos em um caso do `switch` podem ser vinculados a constantes
ou variáveis temporárias para uso no corpo do caso,
e condições de correspondência complexas podem ser expressas
com uma cláusula `where` em cada caso.

## Laços for-in

Use o laço `for`-`in` para percorrer uma sequência,
como os itens de um array, intervalos de números ou caracteres de uma string.

Este exemplo usa um laço `for`-`in` para percorrer os itens de um array:

```swift
let names = ["Anna", "Alex", "Brian", "Jack"]
for name in names {
    print("Hello, \(name)!")
}
// Hello, Anna!
// Hello, Alex!
// Hello, Brian!
// Hello, Jack!
```

<!--
  - test: `forLoops`

  ```swifttest
  -> let names = ["Anna", "Alex", "Brian", "Jack"]
  -> for name in names {
        print("Hello, \(name)!")
     }
  </ Hello, Anna!
  </ Hello, Alex!
  </ Hello, Brian!
  </ Hello, Jack!
  ```
-->

Você também pode percorrer um dicionário para acessar seus pares chave-valor.
Cada item do dicionário é retornado como uma tupla `(key, value)` durante a iteração,
e você pode decompor os membros da tupla `(key, value)` em constantes
com nomes explícitos para uso no corpo do laço `for`-`in`.
No exemplo de código abaixo, as chaves do dicionário são decompostas
em uma constante chamada `animalName`,
e os valores do dicionário são decompostos em uma constante chamada `legCount`.

```swift
let numberOfLegs = ["spider": 8, "ant": 6, "cat": 4]
for (animalName, legCount) in numberOfLegs {
    print("\(animalName)s have \(legCount) legs")
}
// cats have 4 legs
// ants have 6 legs
// spiders have 8 legs
```

<!--
  - test: `forLoops`

  ```swifttest
  -> let numberOfLegs = ["spider": 8, "ant": 6, "cat": 4]
  -> for (animalName, legCount) in numberOfLegs {
        print("\(animalName)s have \(legCount) legs")
     }
  </ cats have 4 legs
  </ ants have 6 legs
  </ spiders have 8 legs
  ```
-->

O conteúdo de um `Dictionary` é, por natureza, desordenado,
e percorrê-lo não garante a ordem em que os itens serão recuperados.
Em especial, a ordem em que você insere itens em um `Dictionary`
não define a ordem em que eles são percorridos.
Para saber mais sobre arrays e dicionários, veja <doc:CollectionTypes>.

<!--
  TODO: provide some advice on how to iterate over a Dictionary in order
  (perhaps sorted by key), using a predicate or array sort or some kind.
-->

Você também pode usar laços `for`-`in` com intervalos numéricos.
Este exemplo imprime as primeiras entradas da tabuada do cinco:

```swift
for index in 1...5 {
    print("\(index) times 5 is \(index * 5)")
}
// 1 times 5 is 5
// 2 times 5 is 10
// 3 times 5 is 15
// 4 times 5 is 20
// 5 times 5 is 25
```

<!--
  - test: `forLoops`

  ```swifttest
  -> for index in 1...5 {
        print("\(index) times 5 is \(index * 5)")
     }
  </ 1 times 5 is 5
  </ 2 times 5 is 10
  </ 3 times 5 is 15
  </ 4 times 5 is 20
  </ 5 times 5 is 25
  ```
-->

A sequência percorrida é um intervalo de números de `1` a `5`, inclusive,
como indica o uso do operador de intervalo fechado (`...`).
O valor de `index` é definido como o primeiro número do intervalo (`1`),
e as instruções dentro do laço são executadas.
Neste caso, o laço contém apenas uma instrução,
que imprime uma entrada da tabuada do cinco para o valor atual de `index`.
Depois que a instrução é executada, o valor de `index` é atualizado
para o segundo valor do intervalo (`2`),
e a função `print(_:separator:terminator:)` é chamada novamente.
Esse processo continua até chegar ao fim do intervalo.

No exemplo acima, `index` é uma constante cujo valor é definido automaticamente
no início de cada iteração do laço.
Por isso, `index` não precisa ser declarado antes de ser usado.
Ele é declarado implicitamente apenas por aparecer na declaração do laço,
sem a necessidade da palavra-chave `let`.

Se você não precisar de cada valor de uma sequência,
pode ignorar esses valores usando um sublinhado no lugar do nome de uma variável.

```swift
let base = 3
let power = 10
var answer = 1
for _ in 1...power {
    answer *= base
}
print("\(base) to the power of \(power) is \(answer)")
// Prints "3 to the power of 10 is 59049".
```

<!--
  - test: `forLoops`

  ```swifttest
  -> let base = 3
  -> let power = 10
  -> var answer = 1
  -> for _ in 1...power {
        answer *= base
     }
  -> print("\(base) to the power of \(power) is \(answer)")
  <- 3 to the power of 10 is 59049
  ```
-->

O exemplo acima calcula o valor de um número elevado a outro
(neste caso, `3` elevado a `10`).
Ele multiplica um valor inicial de `1`
(ou seja, `3` elevado a `0`) por `3`, dez vezes,
usando um intervalo fechado que começa em `1` e termina em `10`.
Para esse cálculo, os valores individuais do contador a cada passagem pelo laço
são desnecessários: o código simplesmente executa o laço o número certo de vezes.
O caractere sublinhado (`_`) usado no lugar de uma variável do laço
faz com que os valores individuais sejam ignorados
e não dá acesso ao valor atual em cada iteração do laço.

Em algumas situações, você pode não querer usar intervalos fechados,
que incluem os dois extremos.
Pense em desenhar as marcas de cada minuto em um mostrador de relógio.
Você quer desenhar `60` marcas, começando pelo minuto `0`.
Use o operador de intervalo semiaberto (`..<`) para incluir o limite inferior,
mas não o superior.
Para saber mais sobre intervalos, veja <doc:BasicOperators#Range-Operators>.

```swift
let minutes = 60
for tickMark in 0..<minutes {
    // render the tick mark each minute (60 times)
}
```

<!--
  - test: `forLoops`

  ```swifttest
  -> let minutes = 60
  >> var result: [Int] = []
  -> for tickMark in 0..<minutes {
        // render the tick mark each minute (60 times)
  >>    result.append(tickMark)
     }
  >> print(result.first!, result.last!, result.count)
  << 0 59 60
  ```
-->

Alguns usuários podem preferir menos marcas na interface.
Eles podem preferir uma marca a cada `5` minutos.
Use a função `stride(from:to:by:)` para pular as marcas indesejadas.

```swift
let minuteInterval = 5
for tickMark in stride(from: 0, to: minutes, by: minuteInterval) {
    // render the tick mark every 5 minutes (0, 5, 10, 15 ... 45, 50, 55)
}
```

<!--
  - test: `forLoops`

  ```swifttest
  -> let minuteInterval = 5
  >> result = []
  -> for tickMark in stride(from: 0, to: minutes, by: minuteInterval) {
        // render the tick mark every 5 minutes (0, 5, 10, 15 ... 45, 50, 55)
  >>      result.append(tickMark)
     }
  >> print(result.first!, result.last!, result.count)
  << 0 55 12
  ```
-->

Intervalos fechados também estão disponíveis, usando `stride(from:through:by:)` no lugar:

```swift
let hours = 12
let hourInterval = 3
for tickMark in stride(from: 3, through: hours, by: hourInterval) {
    // render the tick mark every 3 hours (3, 6, 9, 12)
}
```

<!--
  - test: `forLoops`

  ```swifttest
  -> let hours = 12
  -> let hourInterval = 3
  -> for tickMark in stride(from: 3, through: hours, by: hourInterval) {
        // render the tick mark every 3 hours (3, 6, 9, 12)
  >>    print(tickMark)
     }
  << 3
  << 6
  << 9
  << 12
  ```
-->

Os exemplos acima usam um laço `for`-`in` para percorrer
intervalos, arrays, dicionários e strings.
No entanto, você pode usar essa sintaxe para percorrer *qualquer* coleção,
incluindo suas próprias classes e tipos de coleção,
desde que esses tipos estejam em conformidade com o protocolo
[`Sequence`](https://developer.apple.com/documentation/swift/sequence).

<!--
  TODO: for (index, object) in enumerate(collection)
  and also for i in indices(collection) { collection[i] }
-->

## Laços while

Um laço `while` executa um conjunto de instruções até que uma condição se torne `false`.
Esses laços são mais indicados quando o número de iterações não é conhecido
antes da primeira iteração começar.
O Swift oferece dois tipos de laços `while`:

- `while` avalia sua condição no início de cada passagem pelo laço.
- `repeat`-`while` avalia sua condição no fim de cada passagem pelo laço.

### While

Um laço `while` começa avaliando uma única condição.
Se a condição for `true`, um conjunto de instruções é repetido
até que a condição se torne `false`.

Esta é a forma geral de um laço `while`:

```swift
while <#condition#> {
   <#statements#>
}
```

Este exemplo simula uma partida simples de *Cobras e Escadas*
(também conhecido como *Chutes and Ladders*):

<!-- Apple Books screenshot begins here. -->

![](snakesAndLadders)

As regras do jogo são as seguintes:

- O tabuleiro tem 25 casas, e o objetivo é cair na casa 25 ou além dela.
- A casa inicial do jogador é a “casa zero”, logo fora do canto inferior esquerdo do tabuleiro.
- A cada turno, você lança um dado de seis faces e avança esse número de casas,
  seguindo o caminho horizontal indicado pela seta pontilhada acima.
- Se o turno terminar na base de uma escada, você sobe por essa escada.
- Se o turno terminar na cabeça de uma cobra, você desce por essa cobra.

O tabuleiro do jogo é representado por um array de valores `Int`.
Seu tamanho é baseado em uma constante chamada `finalSquare`,
usada para inicializar o array e também para verificar a condição de vitória
mais adiante no exemplo.
Como os jogadores começam fora do tabuleiro, na “casa zero”,
o tabuleiro é inicializado com 26 valores `Int` zero, e não 25.

```swift
let finalSquare = 25
var board = [Int](repeating: 0, count: finalSquare + 1)
```

<!--
  - test: `snakesAndLadders1`

  ```swifttest
  -> let finalSquare = 25
  -> var board = [Int](repeating: 0, count: finalSquare + 1)
  >> assert(board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
  ```
-->

Em seguida, algumas casas recebem valores mais específicos para as cobras e escadas.
As casas com a base de uma escada têm um número positivo, que faz você subir no tabuleiro,
enquanto as casas com a cabeça de uma cobra têm um número negativo,
que faz você descer no tabuleiro.

```swift
board[03] = +08; board[06] = +11; board[09] = +09; board[10] = +02
board[14] = -10; board[19] = -11; board[22] = -02; board[24] = -08
```

<!--
  - test: `snakesAndLadders1`

  ```swifttest
  -> board[03] = +08; board[06] = +11; board[09] = +09; board[10] = +02
  -> board[14] = -10; board[19] = -11; board[22] = -02; board[24] = -08
  ```
-->

<!-- Apple Books screenshot ends here. -->

A casa 3 contém a base de uma escada que leva você até a casa 11.
Para representar isso, `board[03]` é igual a `+08`,
o que equivale ao valor inteiro `8` (a diferença entre `3` e `11`).
Para alinhar os valores e as instruções, o operador de sinal positivo unário (`+i`)
é usado explicitamente junto com o operador de sinal negativo unário (`-i`),
e os números menores que `10` são preenchidos com zeros.
(Nenhuma dessas técnicas de estilo é estritamente necessária,
mas elas deixam o código mais organizado.)

```swift
var square = 0
var diceRoll = 0
while square < finalSquare {
    // roll the dice
    diceRoll += 1
    if diceRoll == 7 { diceRoll = 1 }
    // move by the rolled amount
    square += diceRoll
    if square < board.count {
        // if we're still on the board, move up or down for a snake or a ladder
        square += board[square]
    }
}
print("Game over!")
```

<!--
  - test: `snakesAndLadders1`

  ```swifttest
  -> var square = 0
  -> var diceRoll = 0
  -> while square < finalSquare {
        // roll the dice
        diceRoll += 1
        if diceRoll == 7 { diceRoll = 1 }
  >>    print("diceRoll is \(diceRoll)")
        // move by the rolled amount
        square += diceRoll
  >>    print("after diceRoll, square is \(square)")
        if square < board.count {
           // if we're still on the board, move up or down for a snake or a ladder
           square += board[square]
  >>       print("after snakes or ladders, square is \(square)")
        }
     }
  -> print("Game over!")
  << diceRoll is 1
  << after diceRoll, square is 1
  << after snakes or ladders, square is 1
  << diceRoll is 2
  << after diceRoll, square is 3
  << after snakes or ladders, square is 11
  << diceRoll is 3
  << after diceRoll, square is 14
  << after snakes or ladders, square is 4
  << diceRoll is 4
  << after diceRoll, square is 8
  << after snakes or ladders, square is 8
  << diceRoll is 5
  << after diceRoll, square is 13
  << after snakes or ladders, square is 13
  << diceRoll is 6
  << after diceRoll, square is 19
  << after snakes or ladders, square is 8
  << diceRoll is 1
  << after diceRoll, square is 9
  << after snakes or ladders, square is 18
  << diceRoll is 2
  << after diceRoll, square is 20
  << after snakes or ladders, square is 20
  << diceRoll is 3
  << after diceRoll, square is 23
  << after snakes or ladders, square is 23
  << diceRoll is 4
  << after diceRoll, square is 27
  << Game over!
  ```
-->

O exemplo acima usa uma abordagem bem simples para o lançamento do dado.
Em vez de gerar um número aleatório, ele começa com o valor `diceRoll` igual a `0`.
A cada passagem pelo laço `while`, `diceRoll` é incrementado em um
e depois é verificado para ver se ficou grande demais.
Sempre que esse valor chega a `7`, o lançamento ficou grande demais
e é reiniciado com o valor `1`.
O resultado é uma sequência de valores de `diceRoll` que é sempre
`1`, `2`, `3`, `4`, `5`, `6`, `1`, `2` e assim por diante.

Depois de lançar o dado, o jogador avança `diceRoll` casas.
É possível que o lançamento tenha levado o jogador além da casa 25,
caso em que o jogo termina.
Para lidar com esse cenário, o código verifica se `square`
é menor que a propriedade `count` do array `board`.
Se `square` for válido, o valor armazenado em `board[square]`
é somado ao valor atual de `square`
para fazer o jogador subir ou descer qualquer escada ou cobra.

> Nota: Se essa verificação não for feita,
> `board[square]` pode tentar acessar um valor fora dos limites do array `board`,
> o que dispararia um erro de tempo de execução.

A execução atual do laço `while` então termina,
e a condição do laço é verificada para ver se ele deve ser executado de novo.
Se o jogador tiver chegado à casa `25` ou além,
a condição do laço é avaliada como `false` e o jogo termina.

Um laço `while` é adequado neste caso,
porque a duração do jogo não está clara no início do laço.
Em vez disso, o laço é executado até que determinada condição seja satisfeita.

### Repeat-while

A outra variação do laço `while`, conhecida como laço `repeat`-`while`,
executa primeiro uma única passagem pelo bloco do laço,
*antes* de considerar a condição do laço.
Em seguida, continua repetindo o laço até que a condição seja `false`.

> Nota: O laço `repeat`-`while` do Swift é análogo
> a um laço `do`-`while` de outras linguagens.

Esta é a forma geral de um laço `repeat`-`while`:

```swift
repeat {
   <#statements#>
} while <#condition#>
```

Aqui está o exemplo de *Cobras e Escadas* de novo,
escrito como um laço `repeat`-`while` em vez de um laço `while`.
Os valores de `finalSquare`, `board`, `square` e `diceRoll`
são inicializados exatamente da mesma forma que no laço `while`.

```swift
let finalSquare = 25
var board = [Int](repeating: 0, count: finalSquare + 1)
board[03] = +08; board[06] = +11; board[09] = +09; board[10] = +02
board[14] = -10; board[19] = -11; board[22] = -02; board[24] = -08
var square = 0
var diceRoll = 0
```

<!--
  - test: `snakesAndLadders2`

  ```swifttest
  -> let finalSquare = 25
  -> var board = [Int](repeating: 0, count: finalSquare + 1)
  >> assert(board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
  -> board[03] = +08; board[06] = +11; board[09] = +09; board[10] = +02
  -> board[14] = -10; board[19] = -11; board[22] = -02; board[24] = -08
  -> var square = 0
  -> var diceRoll = 0
  ```
-->

Nesta versão do jogo, a *primeira* ação do laço é verificar se há uma escada ou uma cobra.
Nenhuma escada do tabuleiro leva o jogador direto até a casa 25,
e por isso não é possível vencer o jogo subindo por uma escada.
Portanto, é seguro verificar uma cobra ou uma escada como a primeira ação do laço.

No início do jogo, o jogador está na “casa zero”.
`board[0]` é sempre igual a `0` e não tem efeito.

```swift
repeat {
    // move up or down for a snake or ladder
    square += board[square]
    // roll the dice
    diceRoll += 1
    if diceRoll == 7 { diceRoll = 1 }
    // move by the rolled amount
    square += diceRoll
} while square < finalSquare
print("Game over!")
```

<!--
  - test: `snakesAndLadders2`

  ```swifttest
  -> repeat {
        // move up or down for a snake or ladder
        square += board[square]
  >>      print("after snakes or ladders, square is \(square)")
        // roll the dice
        diceRoll += 1
        if diceRoll == 7 { diceRoll = 1 }
  >>    print("diceRoll is \(diceRoll)")
        // move by the rolled amount
        square += diceRoll
  >>    print("after diceRoll, square is \(square)")
  -> } while square < finalSquare
  -> print("Game over!")
  << after snakes or ladders, square is 0
  << diceRoll is 1
  << after diceRoll, square is 1
  << after snakes or ladders, square is 1
  << diceRoll is 2
  << after diceRoll, square is 3
  << after snakes or ladders, square is 11
  << diceRoll is 3
  << after diceRoll, square is 14
  << after snakes or ladders, square is 4
  << diceRoll is 4
  << after diceRoll, square is 8
  << after snakes or ladders, square is 8
  << diceRoll is 5
  << after diceRoll, square is 13
  << after snakes or ladders, square is 13
  << diceRoll is 6
  << after diceRoll, square is 19
  << after snakes or ladders, square is 8
  << diceRoll is 1
  << after diceRoll, square is 9
  << after snakes or ladders, square is 18
  << diceRoll is 2
  << after diceRoll, square is 20
  << after snakes or ladders, square is 20
  << diceRoll is 3
  << after diceRoll, square is 23
  << after snakes or ladders, square is 23
  << diceRoll is 4
  << after diceRoll, square is 27
  << Game over!
  ```
-->

Depois que o código verifica cobras e escadas,
o dado é lançado e o jogador avança `diceRoll` casas.
A execução atual do laço então termina.

A condição do laço (`while square < finalSquare`) é a mesma de antes,
mas desta vez ela só é avaliada no *fim* da primeira passagem pelo laço.
A estrutura do laço `repeat`-`while` se adapta melhor a este jogo
do que o laço `while` do exemplo anterior.
No laço `repeat`-`while` acima,
`square += board[square]` é sempre executado *logo depois*
de a condição `while` confirmar que `square` ainda está no tabuleiro.
Esse comportamento elimina a necessidade da verificação de limites do array
vista na versão com `while` do jogo, descrita antes.

## Instruções condicionais

Muitas vezes é útil executar trechos diferentes de código com base em certas condições.
Você pode querer executar um trecho extra de código quando ocorre um erro,
ou exibir uma mensagem quando um valor fica alto ou baixo demais.
Para isso, você torna partes do seu código *condicionais*.

O Swift oferece duas formas de adicionar ramos condicionais ao seu código:
a instrução `if` e a instrução `switch`.
Normalmente, use a instrução `if` para avaliar condições simples,
com poucos resultados possíveis.
A instrução `switch` é mais indicada para condições mais complexas,
com várias combinações possíveis,
e é útil em situações em que a correspondência de padrões
pode ajudar a escolher o ramo de código adequado a executar.

### If

Em sua forma mais simples, a instrução `if` tem uma única condição `if`.
Ela executa um conjunto de instruções somente se essa condição for `true`.

```swift
var temperatureInFahrenheit = 30
if temperatureInFahrenheit <= 32 {
    print("It's very cold. Consider wearing a scarf.")
}
// Prints "It's very cold. Consider wearing a scarf."
```

<!--
  - test: `ifElse`

  ```swifttest
  -> var temperatureInFahrenheit = 30
  -> if temperatureInFahrenheit <= 32 {
        print("It's very cold. Consider wearing a scarf.")
     }
  <- It's very cold. Consider wearing a scarf.
  ```
-->

O exemplo acima verifica se a temperatura é menor ou igual a 32 graus Fahrenheit
(o ponto de congelamento da água).
Se for, uma mensagem é impressa.
Caso contrário, nenhuma mensagem é impressa,
e a execução do código continua depois da chave de fechamento da instrução `if`.

A instrução `if` pode fornecer um conjunto alternativo de instruções,
conhecido como *cláusula else*, para situações em que a condição `if` é `false`.
Essas instruções são indicadas pela palavra-chave `else`.

```swift
temperatureInFahrenheit = 40
if temperatureInFahrenheit <= 32 {
    print("It's very cold. Consider wearing a scarf.")
} else {
    print("It's not that cold. Wear a T-shirt.")
}
// Prints "It's not that cold. Wear a T-shirt."
```

<!--
  - test: `ifElse`

  ```swifttest
  -> temperatureInFahrenheit = 40
  -> if temperatureInFahrenheit <= 32 {
        print("It's very cold. Consider wearing a scarf.")
     } else {
        print("It's not that cold. Wear a T-shirt.")
     }
  <- It's not that cold. Wear a T-shirt.
  ```
-->

Um desses dois ramos é sempre executado.
Como a temperatura subiu para `40` graus Fahrenheit,
já não está frio o bastante para recomendar um cachecol,
e por isso o ramo `else` é acionado.

Você pode encadear várias instruções `if` para considerar cláusulas adicionais.

```swift
temperatureInFahrenheit = 90
if temperatureInFahrenheit <= 32 {
    print("It's very cold. Consider wearing a scarf.")
} else if temperatureInFahrenheit >= 86 {
    print("It's really warm. Don't forget to wear sunscreen.")
} else {
    print("It's not that cold. Wear a T-shirt.")
}
// Prints "It's really warm. Don't forget to wear sunscreen."
```

<!--
  - test: `ifElse`

  ```swifttest
  -> temperatureInFahrenheit = 90
  -> if temperatureInFahrenheit <= 32 {
        print("It's very cold. Consider wearing a scarf.")
     } else if temperatureInFahrenheit >= 86 {
        print("It's really warm. Don't forget to wear sunscreen.")
     } else {
        print("It's not that cold. Wear a T-shirt.")
     }
  <- It's really warm. Don't forget to wear sunscreen.
  ```
-->

Aqui, foi adicionada uma instrução `if` extra para responder a temperaturas
especialmente altas.
A cláusula `else` final permanece,
e imprime uma resposta para qualquer temperatura
que não seja nem muito alta nem muito baixa.

A cláusula `else` final é opcional, porém,
e pode ser omitida se o conjunto de condições não precisar ser completo.

```swift
temperatureInFahrenheit = 72
if temperatureInFahrenheit <= 32 {
    print("It's very cold. Consider wearing a scarf.")
} else if temperatureInFahrenheit >= 86 {
    print("It's really warm. Don't forget to wear sunscreen.")
}
```

<!--
  - test: `ifElse`

  ```swifttest
  -> temperatureInFahrenheit = 72
  -> if temperatureInFahrenheit <= 32 {
        print("It's very cold. Consider wearing a scarf.")
     } else if temperatureInFahrenheit >= 86 {
        print("It's really warm. Don't forget to wear sunscreen.")
     }
  ```
-->

Como a temperatura não está fria o bastante para acionar a condição `if`
nem quente o bastante para acionar a condição `else if`,
nenhuma mensagem é impressa.

O Swift oferece uma forma abreviada de `if` que você pode usar ao definir valores.
Por exemplo, considere o código a seguir:

```swift
let temperatureInCelsius = 25
let weatherAdvice: String

if temperatureInCelsius <= 0 {
    weatherAdvice = "It's very cold. Consider wearing a scarf."
} else if temperatureInCelsius >= 30 {
    weatherAdvice = "It's really warm. Don't forget to wear sunscreen."
} else {
    weatherAdvice = "It's not that cold. Wear a T-shirt."
}

print(weatherAdvice)
// Prints "It's not that cold. Wear a T-shirt."
```

Aqui, cada um dos ramos define um valor para a constante `weatherAdvice`,
que é impresso depois da instrução `if`.

Usando a sintaxe alternativa, conhecida como expressão `if`,
você pode escrever este código de forma mais concisa:

```swift
let weatherAdvice = if temperatureInCelsius <= 0 {
    "It's very cold. Consider wearing a scarf."
} else if temperatureInCelsius >= 30 {
    "It's really warm. Don't forget to wear sunscreen."
} else {
    "It's not that cold. Wear a T-shirt."
}

print(weatherAdvice)
// Prints "It's not that cold. Wear a T-shirt."
```

Nesta versão com expressão `if`, cada ramo contém um único valor.
Se a condição de um ramo for verdadeira,
o valor desse ramo é usado como valor da expressão `if` inteira
na atribuição de `weatherAdvice`.
Todo ramo `if` tem um ramo `else if` ou `else` correspondente,
o que garante que um dos ramos sempre seja escolhido
e que a expressão `if` sempre produza um valor,
independentemente de quais condições sejam verdadeiras.

Como a sintaxe da atribuição começa fora da expressão `if`,
não é preciso repetir `weatherAdvice =` dentro de cada ramo.
Em vez disso, cada ramo da expressão `if` produz um dos três valores possíveis
para `weatherAdvice`, e a atribuição usa esse valor.

Todos os ramos de uma expressão `if` precisam conter valores do mesmo tipo.
Como o Swift verifica o tipo de cada ramo separadamente,
valores como `nil`, que podem ser usados com mais de um tipo,
impedem que o Swift determine automaticamente o tipo da expressão `if`.
Por isso, é preciso especificar o tipo explicitamente, por exemplo:

```swift
let freezeWarning: String? = if temperatureInCelsius <= 0 {
    "It's below freezing. Watch for ice!"
} else {
    nil
}
```

No código acima, um ramo da expressão `if` tem um valor de string
e o outro ramo tem o valor `nil`.
O valor `nil` poderia ser usado como valor de qualquer tipo opcional,
então você precisa escrever explicitamente que `freezeWarning` é uma string opcional,
como descrito em <doc:TheBasics#Type-Annotations>.

Uma forma alternativa de fornecer essa informação de tipo
é indicar um tipo explícito para `nil`,
em vez de indicar um tipo explícito para `freezeWarning`:

```swift
let freezeWarning = if temperatureInCelsius <= 0 {
    "It's below freezing. Watch for ice!"
} else {
    nil as String?
}
```

Uma expressão `if` pode responder a falhas inesperadas lançando um erro
ou chamando uma função como `fatalError(_:file:line:)`, que nunca retorna.
Por exemplo:

```swift
let weatherAdvice = if temperatureInCelsius > 100 {
    throw TemperatureError.boiling
} else {
    "It's a reasonable temperature."
}
```

Neste exemplo, a expressão `if` verifica se a temperatura prevista
é maior que 100 °C, o ponto de ebulição da água.
Uma temperatura tão alta faz a expressão `if` lançar um erro `.boiling`,
em vez de retornar um resumo em texto.
Mesmo que essa expressão `if` possa lançar um erro,
você não escreve `try` antes dela.
Para informações sobre como trabalhar com erros, veja <doc:ErrorHandling>.

Além de usar expressões `if` do lado direito de uma atribuição,
como nos exemplos acima,
você também pode usá-las como o valor que uma função ou closure retorna.

### Switch

Uma instrução `switch` considera um valor e o compara com vários padrões de correspondência possíveis.
Em seguida, executa o bloco de código adequado, com base no primeiro padrão que corresponder com sucesso.
Uma instrução `switch` é uma alternativa à instrução `if`
para responder a vários estados possíveis.

Em sua forma mais simples, uma instrução `switch` compara um valor
com um ou mais valores do mesmo tipo.

```swift
switch <#some value to consider#> {
case <#value 1#>:
    <#respond to value 1#>
case <#value 2#>,
    <#value 3#>:
    <#respond to value 2 or 3#>
default:
    <#otherwise, do something else#>
}
```

Toda instrução `switch` é composta por vários *casos* possíveis,
cada um começando com a palavra-chave `case`.
Além de comparar com valores específicos,
o Swift oferece várias formas de cada caso especificar
padrões de correspondência mais complexos.
Essas opções são descritas mais adiante neste capítulo.

Assim como o corpo de uma instrução `if`, cada `case` é um ramo separado de execução do código.
A instrução `switch` determina qual ramo deve ser selecionado.
Esse procedimento é conhecido como *fazer o switch* sobre o valor analisado.

Toda instrução `switch` precisa ser *exaustiva*.
Ou seja, cada valor possível do tipo considerado deve ser coberto por um dos casos do `switch`.
Se não for apropriado criar um caso para cada valor possível,
você pode definir um caso `default` para cobrir os valores que não foram tratados explicitamente.
Esse caso é indicado pela palavra-chave `default` e deve sempre aparecer por último.

Este exemplo usa uma instrução `switch` para analisar um único caractere minúsculo chamado `someCharacter`:

```swift
let someCharacter: Character = "z"
switch someCharacter {
case "a":
    print("The first letter of the Latin alphabet")
case "z":
    print("The last letter of the Latin alphabet")
default:
    print("Some other character")
}
// Prints "The last letter of the Latin alphabet".
```

<!--
  - test: `switch`

  ```swifttest
  -> let someCharacter: Character = "z"
  -> switch someCharacter {
        case "a":
           print("The first letter of the Latin alphabet")
        case "z":
           print("The last letter of the Latin alphabet")
        default:
           print("Some other character")
     }
  <- The last letter of the Latin alphabet
  ```
-->

O primeiro caso da instrução `switch` corresponde à primeira letra do alfabeto inglês, `a`,
e o segundo caso corresponde à última letra, `z`.
Como o `switch` precisa ter um caso para cada caractere possível,
e não apenas para cada letra,
esta instrução usa um caso `default` para corresponder a todos os caracteres
diferentes de `a` e `z`.
Esse caso `default` garante que a instrução `switch` seja exaustiva.

Assim como as instruções `if`, as instruções `switch` também têm uma forma de expressão:

```swift
let anotherCharacter: Character = "a"
let message = switch anotherCharacter {
case "a":
    "The first letter of the Latin alphabet"
case "z":
    "The last letter of the Latin alphabet"
default:
    "Some other character"
}

print(message)
// Prints "The first letter of the Latin alphabet".
```

Neste exemplo, cada caso da expressão `switch` contém o valor de `message`
a ser usado quando esse caso corresponder a `anotherCharacter`.
Como o `switch` é sempre exaustivo, sempre há um valor para atribuir.

Assim como nas expressões `if`, você pode lançar um erro
ou chamar uma função como `fatalError(_:file:line:)`, que nunca retorna,
em vez de fornecer um valor para um determinado caso.
Você pode usar expressões `switch` do lado direito de uma atribuição,
como no exemplo acima,
e como o valor que uma função ou closure retorna.

#### Sem fallthrough implícito

Diferentemente das instruções `switch` em C e Objective-C,
as instruções `switch` do Swift não passam, por padrão,
da parte de baixo de cada caso para o seguinte.
Em vez disso, a instrução `switch` inteira termina sua execução
assim que o primeiro caso correspondente é concluído,
sem exigir uma instrução `break` explícita.
Isso torna a instrução `switch` mais segura e mais fácil de usar do que a de C,
e evita executar mais de um caso do `switch` por engano.

> Nota: Embora `break` não seja obrigatório no Swift,
> você pode usar uma instrução `break` para corresponder e ignorar um caso específico
> ou para sair de um caso correspondido antes que esse caso termine sua execução.
> Para detalhes, veja <doc:ControlFlow#Break-in-a-Switch-Statement>.

O corpo de cada caso *deve* conter pelo menos uma instrução executável.
Não é válido escrever o código a seguir, porque o primeiro caso está vazio:

```swift
let anotherCharacter: Character = "a"
switch anotherCharacter {
case "a": // Invalid, the case has an empty body
case "A":
    print("The letter A")
default:
    print("Not the letter A")
}
// This will report a compile-time error.
```

<!--
  - test: `noFallthrough`

  ```swifttest
  -> let anotherCharacter: Character = "a"
  -> switch anotherCharacter {
        case "a": // Invalid, the case has an empty body
        case "A":
           print("The letter A")
        default:
           print("Not the letter A")
     }
  !$ error: 'case' label in a 'switch' must have at least one executable statement
  !!      case "a": // Invalid, the case has an empty body
  !!      ^~~~~~~~~
  !!                break
  // This will report a compile-time error.
  ```
-->

Diferentemente de uma instrução `switch` em C,
este `switch` não corresponde a `"a"` e `"A"` ao mesmo tempo.
Em vez disso, ele reporta um erro de compilação informando que `case "a":`
não contém nenhuma instrução executável.
Essa abordagem evita passagens acidentais de um caso para outro
e torna o código mais seguro e com intenção mais clara.

Para fazer um `switch` com um único caso que corresponda a `"a"` e a `"A"`,
combine os dois valores em um caso composto,
separando os valores com vírgulas.

```swift
let anotherCharacter: Character = "a"
switch anotherCharacter {
case "a", "A":
    print("The letter A")
default:
    print("Not the letter A")
}
// Prints "The letter A".
```

<!--
  - test: `compoundCaseInsteadOfFallthrough`

  ```swifttest
  -> let anotherCharacter: Character = "a"
  -> switch anotherCharacter {
        case "a", "A":
           print("The letter A")
        default:
           print("Not the letter A")
     }
  <- The letter A
  ```
-->

Para facilitar a leitura, um caso composto também pode ser escrito em várias linhas.
Para mais informações sobre casos compostos, veja <doc:ControlFlow#Compound-Cases>.

> Nota: Para passar explicitamente ao caso seguinte no fim de um caso específico do `switch`,
> use a palavra-chave `fallthrough`,
> como descrito em <doc:ControlFlow#Fallthrough>.

#### Correspondência por intervalo

Os valores nos casos do `switch` podem ser verificados quanto à sua inclusão em um intervalo.
Este exemplo usa intervalos numéricos para produzir uma contagem em linguagem natural
para números de qualquer tamanho:

<!--
  REFERENCE
  Saturn has 62 moons with confirmed orbits.
-->

```swift
let approximateCount = 62
let countedThings = "moons orbiting Saturn"
let naturalCount: String
switch approximateCount {
case 0:
    naturalCount = "no"
case 1..<5:
    naturalCount = "a few"
case 5..<12:
    naturalCount = "several"
case 12..<100:
    naturalCount = "dozens of"
case 100..<1000:
    naturalCount = "hundreds of"
default:
    naturalCount = "many"
}
print("There are \(naturalCount) \(countedThings).")
// Prints "There are dozens of moons orbiting Saturn."
```

<!--
  - test: `intervalMatching`

  ```swifttest
  -> let approximateCount = 62
  -> let countedThings = "moons orbiting Saturn"
  -> let naturalCount: String
  -> switch approximateCount {
     case 0:
         naturalCount = "no"
     case 1..<5:
         naturalCount = "a few"
     case 5..<12:
         naturalCount = "several"
     case 12..<100:
         naturalCount = "dozens of"
     case 100..<1000:
         naturalCount = "hundreds of"
     default:
         naturalCount = "many"
     }
  -> print("There are \(naturalCount) \(countedThings).")
  <- There are dozens of moons orbiting Saturn.
  ```
-->

No exemplo acima, `approximateCount` é avaliado em uma instrução `switch`.
Cada `case` compara esse valor com um número ou intervalo.
Como o valor de `approximateCount` está entre 12 e 100,
`naturalCount` recebe o valor `"dozens of"`,
e a execução sai da instrução `switch`.

#### Tuplas

Você pode usar tuplas para testar vários valores na mesma instrução `switch`.
Cada elemento da tupla pode ser testado com um valor ou intervalo de valores diferente.
Como alternativa, use o caractere sublinhado (`_`),
também conhecido como padrão curinga, para corresponder a qualquer valor possível.

O exemplo abaixo recebe um ponto (x, y), expresso como uma tupla simples do tipo `(Int, Int)`,
e o classifica no gráfico que vem após o exemplo.

```swift
let somePoint = (1, 1)
switch somePoint {
case (0, 0):
    print("\(somePoint) is at the origin")
case (_, 0):
    print("\(somePoint) is on the x-axis")
case (0, _):
    print("\(somePoint) is on the y-axis")
case (-2...2, -2...2):
    print("\(somePoint) is inside the box")
default:
    print("\(somePoint) is outside of the box")
}
// Prints "(1, 1) is inside the box".
```

<!--
  - test: `tuples`

  ```swifttest
  -> let somePoint = (1, 1)
  -> switch somePoint {
        case (0, 0):
           print("\(somePoint) is at the origin")
        case (_, 0):
           print("\(somePoint) is on the x-axis")
        case (0, _):
           print("\(somePoint) is on the y-axis")
        case (-2...2, -2...2):
           print("\(somePoint) is inside the box")
        default:
           print("\(somePoint) is outside of the box")
     }
  <- (1, 1) is inside the box
  ```
-->

![](coordinateGraphSimple)

A instrução `switch` determina se o ponto está na origem (0, 0),
no eixo x vermelho, no eixo y verde,
dentro da caixa azul de 4 por 4 centralizada na origem, ou fora da caixa.

Diferentemente de C, o Swift permite que vários casos do `switch`
considerem o mesmo valor ou valores.
Na verdade, o ponto (0, 0) poderia corresponder a *todos os quatro* casos deste exemplo.
No entanto, se houver várias correspondências possíveis,
o primeiro caso correspondente é sempre usado.
O ponto (0, 0) corresponderia primeiro a `case (0, 0)`,
e por isso todos os outros casos correspondentes seriam ignorados.

#### Vinculações de valor

Um caso do `switch` pode associar o valor ou os valores com que ele corresponde
a constantes ou variáveis temporárias, para uso no corpo do caso.
Esse comportamento é conhecido como *vinculação de valor*,
porque os valores ficam vinculados a constantes ou variáveis temporárias
dentro do corpo do caso.

O exemplo abaixo recebe um ponto (x, y), expresso como uma tupla do tipo `(Int, Int)`,
e o classifica no gráfico que segue:

```swift
let anotherPoint = (2, 0)
switch anotherPoint {
case (let x, 0):
    print("on the x-axis with an x value of \(x)")
case (0, let y):
    print("on the y-axis with a y value of \(y)")
case let (x, y):
    print("somewhere else at (\(x), \(y))")
}
// Prints "on the x-axis with an x value of 2".
```

<!--
  - test: `valueBindings`

  ```swifttest
  -> let anotherPoint = (2, 0)
  -> switch anotherPoint {
        case (let x, 0):
           print("on the x-axis with an x value of \(x)")
        case (0, let y):
           print("on the y-axis with a y value of \(y)")
        case let (x, y):
           print("somewhere else at (\(x), \(y))")
     }
  <- on the x-axis with an x value of 2
  ```
-->

![](coordinateGraphMedium)

A instrução `switch` determina se o ponto está no eixo x vermelho,
no eixo y verde, ou em outro lugar (em nenhum dos dois eixos).

Os três casos do `switch` declaram constantes de espaço reservado `x` e `y`,
que assumem temporariamente um ou os dois valores da tupla de `anotherPoint`.
O primeiro caso, `case (let x, 0)`, corresponde a qualquer ponto com valor `y` igual a `0`
e atribui o valor `x` do ponto à constante temporária `x`.
Da mesma forma, o segundo caso, `case (0, let y)`, corresponde a qualquer ponto
com valor `x` igual a `0` e atribui o valor `y` do ponto à constante temporária `y`.

Depois que as constantes temporárias são declaradas, elas podem ser usadas dentro do bloco de código do caso.
Aqui, são usadas para imprimir a classificação do ponto.

Esta instrução `switch` não tem um caso `default`.
O caso final, `case let (x, y)`, declara uma tupla de duas constantes de espaço reservado
que podem corresponder a qualquer valor.
Como `anotherPoint` é sempre uma tupla de dois valores,
este caso corresponde a todos os valores restantes possíveis,
e um caso `default` não é necessário para tornar a instrução `switch` exaustiva.

#### Where

Um caso do `switch` pode usar uma cláusula `where` para verificar condições adicionais.

O exemplo abaixo classifica um ponto (x, y) no gráfico a seguir:

```swift
let yetAnotherPoint = (1, -1)
switch yetAnotherPoint {
case let (x, y) where x == y:
    print("(\(x), \(y)) is on the line x == y")
case let (x, y) where x == -y:
    print("(\(x), \(y)) is on the line x == -y")
case let (x, y):
    print("(\(x), \(y)) is just some arbitrary point")
}
// Prints "(1, -1) is on the line x == -y".
```

<!--
  - test: `where`

  ```swifttest
  -> let yetAnotherPoint = (1, -1)
  -> switch yetAnotherPoint {
        case let (x, y) where x == y:
           print("(\(x), \(y)) is on the line x == y")
        case let (x, y) where x == -y:
           print("(\(x), \(y)) is on the line x == -y")
        case let (x, y):
           print("(\(x), \(y)) is just some arbitrary point")
     }
  <- (1, -1) is on the line x == -y
  ```
-->

![](coordinateGraphComplex)

A instrução `switch` determina se o ponto está na diagonal verde onde `x == y`,
na diagonal roxa onde `x == -y`, ou em nenhuma delas.

Os três casos do `switch` declaram constantes de espaço reservado `x` e `y`,
que assumem temporariamente os dois valores da tupla de `yetAnotherPoint`.
Essas constantes são usadas como parte de uma cláusula `where`, para criar um filtro dinâmico.
O caso do `switch` corresponde ao valor atual de `point` somente
se a condição da cláusula `where` for avaliada como `true` para esse valor.

Como no exemplo anterior, o caso final corresponde a todos os valores restantes possíveis,
e por isso um caso `default` não é necessário para tornar a instrução `switch` exaustiva.

#### Casos compostos

Vários casos do `switch` que compartilham o mesmo corpo podem ser combinados
escrevendo vários padrões depois de `case`, com uma vírgula entre cada padrão.
Se algum dos padrões corresponder, o caso é considerado correspondente.
Os padrões podem ser escritos em várias linhas se a lista for longa.
Por exemplo:

```swift
let someCharacter: Character = "e"
switch someCharacter {
case "a", "e", "i", "o", "u":
    print("\(someCharacter) is a vowel")
case "b", "c", "d", "f", "g", "h", "j", "k", "l", "m",
    "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z":
    print("\(someCharacter) is a consonant")
default:
    print("\(someCharacter) isn't a vowel or a consonant")
}
// Prints "e is a vowel".
```

<!--
  - test: `compound-switch-case`

  ```swifttest
  -> let someCharacter: Character = "e"
  -> switch someCharacter {
         case "a", "e", "i", "o", "u":
             print("\(someCharacter) is a vowel")
         case "b", "c", "d", "f", "g", "h", "j", "k", "l", "m",
             "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z":
             print("\(someCharacter) is a consonant")
         default:
             print("\(someCharacter) isn't a vowel or a consonant")
     }
  <- e is a vowel
  ```
-->

O primeiro caso da instrução `switch` corresponde às cinco vogais minúsculas do idioma inglês.
Da mesma forma, o segundo caso corresponde a todas as consoantes minúsculas do inglês.
Por fim, o caso `default` corresponde a qualquer outro caractere.

Casos compostos também podem incluir vinculações de valor.
Todos os padrões de um caso composto precisam incluir o mesmo conjunto de vinculações de valor,
e cada vinculação precisa receber um valor do mesmo tipo de todos os padrões do caso composto.
Isso garante que, qualquer que seja a parte do caso composto que correspondeu,
o código no corpo do caso sempre possa acessar um valor para as vinculações,
e que esse valor sempre tenha o mesmo tipo.

```swift
let stillAnotherPoint = (9, 0)
switch stillAnotherPoint {
case (let distance, 0), (0, let distance):
    print("On an axis, \(distance) from the origin")
default:
    print("Not on an axis")
}
// Prints "On an axis, 9 from the origin".
```

<!--
  - test: `compound-switch-case`

  ```swifttest
  -> let stillAnotherPoint = (9, 0)
  -> switch stillAnotherPoint {
         case (let distance, 0), (0, let distance):
             print("On an axis, \(distance) from the origin")
         default:
             print("Not on an axis")
     }
  <- On an axis, 9 from the origin
  ```
-->

O `case` acima tem dois padrões:
`(let distance, 0)` corresponde a pontos no eixo x,
e `(0, let distance)` corresponde a pontos no eixo y.
Os dois padrões incluem uma vinculação para `distance`,
e `distance` é um inteiro nos dois,
o que significa que o código no corpo do `case`
sempre pode acessar um valor para `distance`.

## Padrões

Nos exemplos anteriores, cada caso do switch inclui um padrão
que indica quais valores correspondem a esse caso.
Você também pode usar um padrão como condição de uma instrução `if`.
Veja como fica:

```swift
let somePoint = (12, 100)
if case (let x, 100) = somePoint {
    print("Found a point on the y=100 line, at \(x)")
}
// Prints "Found a point on the y=100 line, at 12".
```

Neste código, a condição da instrução `if` começa com `case`,
indicando que a condição é um padrão em vez de um valor booleano.
Se o padrão corresponder, a condição do `if` é considerada verdadeira,
e então o código no corpo da instrução `if` é executado.
Os padrões que você pode escrever depois de `if case`
são os mesmos que você pode escrever em um caso do switch.

Em um laço `for`-`in`, você pode dar nomes a partes do valor
usando um padrão de vinculação de valor, mesmo sem escrever `case` no seu código:

```swift
let points = [(10, 0), (30, -30), (-20, 0)]

for (x, y) in points {
    if y == 0 {
        print("Found a point on the x-axis at \(x)")
    }
}
// Prints "Found a point on the x-axis at 10".
// Prints "Found a point on the x-axis at -20".
```

O laço `for`-`in` acima percorre um array de tuplas,
vinculando o primeiro e o segundo elementos das tuplas às constantes `x` e `y`.
As instruções dentro do laço podem usar essas constantes,
como a instrução `if` que verifica se o ponto está no eixo x.
Uma forma mais concisa de escrever esse código é combinar a vinculação de valores
e a condição usando um laço `for`-`case`-`in`.
O código abaixo tem o mesmo comportamento do laço `for`-`in` acima:

```swift
for case (let x, 0) in points {
    print("Found a point on the x-axis at \(x)")
}
// Prints "Found a point on the x-axis at 10".
// Prints "Found a point on the x-axis at -20".
```

Neste código, a condição está integrada ao laço `for`-`case`-`in` como parte do padrão.
As instruções do laço `for`-`case`-`in` são executadas somente para pontos no eixo x.
Este código produz o mesmo resultado do laço `for`-`in` acima,
mas é uma forma mais compacta de percorrer somente certos elementos de uma coleção.

Um laço `for`-`case`-`in` também pode incluir uma cláusula `where`,
para verificar uma condição adicional.
As instruções dentro do laço são executadas somente quando a cláusula `where`
corresponde ao elemento atual.
Por exemplo:

```swift
for case let (x, y) in points where x == y || x == -y  {
    print("Found (\(x), \(y)) along a line through the origin")
}
// Prints "Found (30, -30) along a line through the origin".
```

Este código vincula o primeiro e o segundo elementos da tupla
a `x` e `y` como constantes, e depois verifica seus valores na cláusula `where`.
Se a cláusula `where` for `true`, o código no corpo do laço `for` é executado;
caso contrário, a iteração continua com o próximo elemento.

Como os padrões podem vincular valores,
as instruções `if`-`case` e os laços `for`-`case`-`in`
são úteis para trabalhar com enums que têm associated values,
como descrito em <doc:Enumerations#Associated-Values>.

## Instruções de transferência de controle

*Instruções de transferência de controle* mudam a ordem em que o seu código é executado,
transferindo o controle de um trecho de código para outro.
O Swift tem cinco instruções de transferência de controle:

- `continue`
- `break`
- `fallthrough`
- `return`
- `throw`

As instruções `continue`, `break` e `fallthrough` são descritas a seguir.
A instrução `return` é descrita em <doc:Functions>,
e a instrução `throw` é descrita em <doc:ErrorHandling#Propagating-Errors-Using-Throwing-Functions>.

### Continue

A instrução `continue` diz a um laço para parar o que está fazendo
e recomeçar no início da próxima iteração.
Ela diz “terminei a iteração atual do laço”
sem sair do laço por completo.

O exemplo a seguir remove todas as vogais e espaços de uma string em letras minúsculas
para criar uma frase enigmática de quebra-cabeça:

```swift
let puzzleInput = "great minds think alike"
var puzzleOutput = ""
let charactersToRemove: [Character] = ["a", "e", "i", "o", "u", " "]
for character in puzzleInput {
    if charactersToRemove.contains(character) {
        continue
    }
    puzzleOutput.append(character)
}
print(puzzleOutput)
// Prints "grtmndsthnklk".
```

<!--
  - test: `continue`

  ```swifttest
  -> let puzzleInput = "great minds think alike"
  -> var puzzleOutput = ""
  -> let charactersToRemove: [Character] = ["a", "e", "i", "o", "u", " "]
  -> for character in puzzleInput {
        if charactersToRemove.contains(character) {
           continue
        }
        puzzleOutput.append(character)
     }
  -> print(puzzleOutput)
  <- grtmndsthnklk
  ```
-->

O código acima chama a palavra-chave `continue` sempre que encontra uma vogal ou um espaço,
fazendo a iteração atual do laço terminar imediatamente
e pular direto para o início da próxima iteração.

### Break

A instrução `break` encerra imediatamente a execução de uma instrução de controle de fluxo inteira.
A instrução `break` pode ser usada dentro de uma instrução `switch` ou de laço
quando você quer encerrar a execução dessa instrução
antes do que aconteceria normalmente.

#### Break em um laço

Quando usada dentro de um laço, `break` encerra a execução do laço imediatamente
e transfere o controle para o código depois da chave de fechamento (`}`) do laço.
Nenhum código restante da iteração atual do laço é executado,
e nenhuma iteração adicional do laço é iniciada.

<!--
  TODO: I need an example here.
-->

#### Break em uma instrução switch

Quando usada dentro de uma instrução `switch`, `break` faz a instrução `switch`
encerrar sua execução imediatamente
e transferir o controle para o código depois da chave de fechamento (`}`) da instrução `switch`.

Esse comportamento pode ser usado para corresponder e ignorar um ou mais casos em uma instrução `switch`.
Como a instrução `switch` do Swift é exaustiva e não permite casos vazios,
às vezes é necessário corresponder e ignorar um caso deliberadamente,
para deixar a sua intenção explícita.
Você faz isso escrevendo a instrução `break` como o corpo inteiro do caso que quer ignorar.
Quando esse caso é correspondido pela instrução `switch`,
a instrução `break` dentro do caso encerra imediatamente a execução da instrução `switch`.

> Nota: Um caso do `switch` que contém apenas um comentário é apontado como erro de compilação.
> Comentários não são instruções e não fazem um caso do `switch` ser ignorado.
> Sempre use uma instrução `break` para ignorar um caso do `switch`.

O exemplo a seguir faz um `switch` sobre um valor `Character`
e determina se ele representa um símbolo numérico em um de quatro idiomas.
Por brevidade, vários valores são cobertos em um único caso do `switch`.

```swift
let numberSymbol: Character = "三"  // Chinese symbol for the number 3
var possibleIntegerValue: Int?
switch numberSymbol {
case "1", "١", "一", "๑":
    possibleIntegerValue = 1
case "2", "٢", "二", "๒":
    possibleIntegerValue = 2
case "3", "٣", "三", "๓":
    possibleIntegerValue = 3
case "4", "٤", "四", "๔":
    possibleIntegerValue = 4
default:
    break
}
if let integerValue = possibleIntegerValue {
    print("The integer value of \(numberSymbol) is \(integerValue).")
} else {
    print("An integer value couldn't be found for \(numberSymbol).")
}
// Prints "The integer value of 三 is 3."
```

<!--
  - test: `breakInASwitchStatement`

  ```swifttest
  -> let numberSymbol: Character = "三"  // Chinese symbol for the number 3
  -> var possibleIntegerValue: Int?
  -> switch numberSymbol {
        case "1", "١", "一", "๑":
           possibleIntegerValue = 1
        case "2", "٢", "二", "๒":
           possibleIntegerValue = 2
        case "3", "٣", "三", "๓":
           possibleIntegerValue = 3
        case "4", "٤", "四", "๔":
           possibleIntegerValue = 4
        default:
           break
     }
  -> if let integerValue = possibleIntegerValue {
        print("The integer value of \(numberSymbol) is \(integerValue).")
     } else {
        print("An integer value couldn't be found for \(numberSymbol).")
     }
  <- The integer value of 三 is 3.
  ```
-->

Este exemplo verifica `numberSymbol` para determinar se ele é
um símbolo latino, árabe, chinês ou tailandês para os números de `1` a `4`.
Se houver correspondência, um dos casos da instrução `switch`
define uma variável optional `Int?` chamada `possibleIntegerValue`
com o valor inteiro adequado.

Depois que a instrução `switch` termina sua execução,
o exemplo usa optional binding para determinar se um valor foi encontrado.
A variável `possibleIntegerValue` tem valor inicial implícito de `nil`,
por ser um tipo optional,
e por isso o optional binding só será bem-sucedido
se `possibleIntegerValue` tiver sido definida com um valor real
por um dos quatro primeiros casos da instrução `switch`.

Como não é prático listar todos os valores `Character` possíveis no exemplo acima,
um caso `default` trata quaisquer caracteres que não foram correspondidos.
Esse caso `default` não precisa executar nenhuma ação,
e por isso é escrito com uma única instrução `break` como corpo.
Assim que o caso `default` é correspondido, a instrução `break` encerra a execução da instrução `switch`,
e a execução do código continua a partir da instrução `if let`.

### Fallthrough

No Swift, as instruções `switch` não passam da parte de baixo de cada caso para o seguinte.
Ou seja, a instrução `switch` inteira termina sua execução
assim que o primeiro caso correspondente é concluído.
Já em C, é preciso inserir uma instrução `break` explícita no fim de cada caso do `switch`
para evitar o `fallthrough`.
Evitar o `fallthrough` padrão faz com que as instruções `switch` do Swift
sejam bem mais concisas e previsíveis do que as equivalentes em C,
e assim evitam executar vários casos do `switch` por engano.

Se você precisar do comportamento de `fallthrough` no estilo C,
pode optar por ele caso a caso com a palavra-chave `fallthrough`.
O exemplo abaixo usa `fallthrough` para criar uma descrição textual de um número.

```swift
let integerToDescribe = 5
var description = "The number \(integerToDescribe) is"
switch integerToDescribe {
case 2, 3, 5, 7, 11, 13, 17, 19:
    description += " a prime number, and also"
    fallthrough
default:
    description += " an integer."
}
print(description)
// Prints "The number 5 is a prime number, and also an integer."
```

<!--
  - test: `fallthrough`

  ```swifttest
  -> let integerToDescribe = 5
  -> var description = "The number \(integerToDescribe) is"
  -> switch integerToDescribe {
        case 2, 3, 5, 7, 11, 13, 17, 19:
           description += " a prime number, and also"
           fallthrough
        default:
           description += " an integer."
     }
  -> print(description)
  <- The number 5 is a prime number, and also an integer.
  ```
-->

Este exemplo declara uma nova variável `String` chamada `description`
e atribui a ela um valor inicial.
Em seguida, a instrução `switch` analisa o valor de `integerToDescribe`.
Se o valor de `integerToDescribe` for um dos números primos da lista,
o exemplo acrescenta texto ao fim de `description`, para indicar que o número é primo.
Depois, usa a palavra-chave `fallthrough` para também “cair” no caso `default`.
O caso `default` acrescenta um texto extra ao fim da descrição,
e a instrução `switch` está concluída.

A menos que o valor de `integerToDescribe` esteja na lista de números primos conhecidos,
ele não é correspondido pelo primeiro caso do `switch`.
Como não há outros casos específicos,
`integerToDescribe` é correspondido pelo caso `default`.

Depois que a instrução `switch` termina de executar,
a descrição do número é impressa usando a função `print(_:separator:terminator:)`.
Neste exemplo, o número `5` é corretamente identificado como primo.

> Nota: A palavra-chave `fallthrough` não verifica as condições do caso
> para o qual ela faz a execução cair.
> A palavra-chave `fallthrough` apenas faz a execução do código passar
> diretamente para as instruções dentro do bloco do próximo caso (ou do caso `default`),
> como no comportamento padrão da instrução `switch` de C.

### Instruções rotuladas

No Swift, você pode aninhar laços e instruções condicionais
dentro de outros laços e instruções condicionais
para criar estruturas de fluxo de controle complexas.
No entanto, tanto laços quanto instruções condicionais podem usar a instrução `break`
para encerrar sua execução antes do previsto.
Por isso, às vezes é útil deixar explícito qual laço ou instrução condicional
você quer que uma instrução `break` encerre.
Da mesma forma, se você tiver vários laços aninhados,
pode ser útil deixar explícito qual laço a instrução `continue` deve afetar.

Para atingir esses objetivos, você pode marcar um laço ou uma instrução condicional
com um *rótulo de instrução*.
Com uma instrução condicional, você pode usar um rótulo de instrução com a instrução `break`
para encerrar a execução da instrução rotulada.
Com um laço, você pode usar um rótulo de instrução com as instruções `break` ou `continue`
para encerrar ou continuar a execução da instrução rotulada.

Uma instrução rotulada é indicada colocando um rótulo na mesma linha da palavra-chave
que introduz a instrução, seguido de dois-pontos.
Aqui está um exemplo dessa sintaxe para um laço `while`,
embora o princípio seja o mesmo para todos os laços e instruções `switch`:

```swift
<#label name#>: while <#condition#> {
   <#statements#>
}
```

O exemplo a seguir usa as instruções `break` e `continue` com um laço `while` rotulado,
para uma versão adaptada do jogo *Cobras e Escadas* que você viu antes neste capítulo.
Desta vez, o jogo tem uma regra extra:

- Para vencer, você deve cair *exatamente* na casa 25.

Se um lançamento de dado específico levar você além da casa 25,
você deve lançar de novo até tirar o número exato necessário para cair na casa 25.

O tabuleiro do jogo é o mesmo de antes.

![](snakesAndLadders)

Os valores de `finalSquare`, `board`, `square` e `diceRoll`
são inicializados da mesma forma que antes:

```swift
let finalSquare = 25
var board = [Int](repeating: 0, count: finalSquare + 1)
board[03] = +08; board[06] = +11; board[09] = +09; board[10] = +02
board[14] = -10; board[19] = -11; board[22] = -02; board[24] = -08
var square = 0
var diceRoll = 0
```

<!--
  - test: `labels`

  ```swifttest
  -> let finalSquare = 25
  -> var board = [Int](repeating: 0, count: finalSquare + 1)
  >> assert(board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
  -> board[03] = +08; board[06] = +11; board[09] = +09; board[10] = +02
  -> board[14] = -10; board[19] = -11; board[22] = -02; board[24] = -08
  -> var square = 0
  -> var diceRoll = 0
  ```
-->

Esta versão do jogo usa um laço `while` e uma instrução `switch` para implementar a lógica do jogo.
O laço `while` tem um rótulo de instrução chamado `gameLoop`,
para indicar que ele é o laço principal do jogo Cobras e Escadas.

A condição do laço `while` é `while square != finalSquare`,
para refletir que você precisa cair exatamente na casa 25.

```swift
gameLoop: while square != finalSquare {
    diceRoll += 1
    if diceRoll == 7 { diceRoll = 1 }
    switch square + diceRoll {
    case finalSquare:
        // diceRoll will move us to the final square, so the game is over
        break gameLoop
    case let newSquare where newSquare > finalSquare:
        // diceRoll will move us beyond the final square, so roll again
        continue gameLoop
    default:
        // this is a valid move, so find out its effect
        square += diceRoll
        square += board[square]
    }
}
print("Game over!")
```

<!--
  - test: `labels`

  ```swifttest
  -> gameLoop: while square != finalSquare {
        diceRoll += 1
        if diceRoll == 7 { diceRoll = 1 }
  >>    print("diceRoll is \(diceRoll)")
        switch square + diceRoll {
           case finalSquare:
              // diceRoll will move us to the final square, so the game is over
  >>          print("finalSquare, game is over")
              break gameLoop
           case let newSquare where newSquare > finalSquare:
              // diceRoll will move us beyond the final square, so roll again
  >>          print("move too far, roll again")
              continue gameLoop
           default:
              // this is a valid move, so find out its effect
              square += diceRoll
  >>          print("after diceRoll, square is \(square)")
              square += board[square]
  >>          print("after snakes or ladders, square is \(square)")
        }
     }
  -> print("Game over!")
  << diceRoll is 1
  << after diceRoll, square is 1
  << after snakes or ladders, square is 1
  << diceRoll is 2
  << after diceRoll, square is 3
  << after snakes or ladders, square is 11
  << diceRoll is 3
  << after diceRoll, square is 14
  << after snakes or ladders, square is 4
  << diceRoll is 4
  << after diceRoll, square is 8
  << after snakes or ladders, square is 8
  << diceRoll is 5
  << after diceRoll, square is 13
  << after snakes or ladders, square is 13
  << diceRoll is 6
  << after diceRoll, square is 19
  << after snakes or ladders, square is 8
  << diceRoll is 1
  << after diceRoll, square is 9
  << after snakes or ladders, square is 18
  << diceRoll is 2
  << after diceRoll, square is 20
  << after snakes or ladders, square is 20
  << diceRoll is 3
  << after diceRoll, square is 23
  << after snakes or ladders, square is 23
  << diceRoll is 4
  << move too far, roll again
  << diceRoll is 5
  << move too far, roll again
  << diceRoll is 6
  << move too far, roll again
  << diceRoll is 1
  << after diceRoll, square is 24
  << after snakes or ladders, square is 16
  << diceRoll is 2
  << after diceRoll, square is 18
  << after snakes or ladders, square is 18
  << diceRoll is 3
  << after diceRoll, square is 21
  << after snakes or ladders, square is 21
  << diceRoll is 4
  << finalSquare, game is over
  << Game over!
  ```
-->

O dado é lançado no início de cada laço.
Em vez de mover o jogador imediatamente,
o laço usa uma instrução `switch` para analisar o resultado do movimento
e determinar se ele é permitido:

- Se o lançamento do dado vai levar o jogador à casa final, o jogo termina.
  A instrução `break gameLoop` transfere o controle para a primeira linha de código
  fora do laço `while`, o que encerra o jogo.
- Se o lançamento do dado vai levar o jogador *além* da casa final,
  o movimento é inválido e o jogador precisa lançar de novo.
  A instrução `continue gameLoop` encerra a iteração atual do laço `while`
  e começa a próxima iteração do laço.
- Em todos os outros casos, o lançamento do dado é um movimento válido.
  O jogador avança `diceRoll` casas, e a lógica do jogo verifica se há cobras e escadas.
  O laço então termina, e o controle volta para a condição do `while`
  para decidir se é preciso outro turno.

> Nota: Se a instrução `break` acima não usasse o rótulo `gameLoop`,
> ela sairia da instrução `switch`, e não da instrução `while`.
> Usar o rótulo `gameLoop` deixa claro qual instrução de controle deve ser encerrada.
>
> Não é estritamente necessário usar o rótulo `gameLoop`
> ao chamar `continue gameLoop` para pular para a próxima iteração do laço.
> Só há um laço no jogo, e portanto não há ambiguidade sobre qual laço a instrução `continue` vai afetar.
> No entanto, não há problema em usar o rótulo `gameLoop` com a instrução `continue`.
> Isso é coerente com o uso do rótulo junto com a instrução `break`
> e ajuda a tornar a lógica do jogo mais clara de ler e entender.

## Saída antecipada

Uma instrução `guard`, assim como uma instrução `if`, executa instruções
dependendo do valor booleano de uma expressão.
Você usa uma instrução `guard` para exigir que uma condição seja verdadeira
para que o código depois da instrução `guard` seja executado.
Diferentemente de uma instrução `if`, uma instrução `guard` sempre tem uma cláusula `else`:
o código dentro da cláusula `else` é executado se a condição não for verdadeira.

```swift
func greet(person: [String: String]) {
    guard let name = person["name"] else {
        return
    }

    print("Hello \(name)!")

    guard let location = person["location"] else {
        print("I hope the weather is nice near you.")
        return
    }

    print("I hope the weather is nice in \(location).")
}

greet(person: ["name": "John"])
// Prints "Hello John!"
// Prints "I hope the weather is nice near you."
greet(person: ["name": "Jane", "location": "Cupertino"])
// Prints "Hello Jane!"
// Prints "I hope the weather is nice in Cupertino."
```

<!--
  - test: `guard`

  ```swifttest
  -> func greet(person: [String: String]) {
         guard let name = person["name"] else {
             return
         }

         print("Hello \(name)!")

         guard let location = person["location"] else {
             print("I hope the weather is nice near you.")
             return
         }

         print("I hope the weather is nice in \(location).")
     }

  -> greet(person: ["name": "John"])
  <- Hello John!
  <- I hope the weather is nice near you.
  -> greet(person: ["name": "Jane", "location": "Cupertino"])
  <- Hello Jane!
  <- I hope the weather is nice in Cupertino.
  ```
-->

Se a condição da instrução `guard` for atendida,
a execução do código continua depois da chave de fechamento da instrução `guard`.
Quaisquer variáveis ou constantes que receberam valores por meio de um optional binding
como parte da condição ficam disponíveis para o restante do bloco de código
em que a instrução `guard` aparece.

Se essa condição não for atendida, o código dentro do ramo `else` é executado.
Esse ramo precisa transferir o controle para sair do bloco de código
em que a instrução `guard` aparece.
Ele pode fazer isso com uma instrução de transferência de controle,
como `return`, `break`, `continue` ou `throw`,
ou pode chamar uma função ou método que não retorna, como `fatalError(_:file:line:)`.

Usar uma instrução `guard` para requisitos melhora a legibilidade do código,
em comparação com fazer a mesma verificação com uma instrução `if`.
Ela permite escrever o código que normalmente é executado sem envolvê-lo em um bloco `else`,
e permite manter o código que trata um requisito não atendido perto do próprio requisito.

## Ações adiadas

Diferentemente de construções de controle de fluxo como `if` e `while`,
que permitem controlar se parte do código é executada
ou quantas vezes ela é executada,
`defer` controla *quando* um trecho de código é executado.
Você usa um bloco `defer` para escrever código que será executado mais tarde,
quando o programa chegar ao fim do escopo atual.
Por exemplo:

```swift
var score = 1
if score < 10 {
    defer {
        print(score)
    }
    score += 5
}
// Prints "6".
```

<!--
  - test: `defer-with-if`

  ```swifttest
  -> var score = 1
  -> if score < 10 {
  ->     defer {
  ->         print(score)
  ->     }
  ->     score += 5
  -> }
  <- 6
  ```
-->

No exemplo acima, o código dentro do bloco `defer` é executado
antes de sair do corpo da instrução `if`.
Primeiro, o código da instrução `if` é executado, o que incrementa `score` em cinco.
Depois, antes de sair do escopo da instrução `if`, o código adiado é executado,
o que imprime `score`.

O código dentro do `defer` sempre é executado, independentemente de como o programa sai desse escopo.
Isso inclui casos como uma saída antecipada de uma função, a saída de um laço `for`
ou o lançamento de um erro.
Esse comportamento torna `defer` útil para operações em que você precisa garantir
que um par de ações aconteça, como alocar e liberar memória manualmente,
abrir e fechar descritores de arquivo de baixo nível
e iniciar e encerrar transações em um banco de dados,
porque você pode escrever as duas ações lado a lado no seu código.
Por exemplo, o código a seguir dá um bônus temporário à pontuação,
somando e subtraindo 100 dentro de um trecho de código:

```swift
var score = 3
if score < 100 {
    score += 100
    defer {
        score -= 100
    }
    // Other code that uses the score with its bonus goes here.
    print(score)
}
// Prints "103".
```

<!--
  - test: `defer-paired-actions`

  ```swift
  -> var score = 3
  -> if score < 100 {
  ->     score += 100
  ->     defer {
  ->         score -= 100
  ->     }
  ->     // Other code that uses the score with its bonus goes here.
  ->     print(score)
  -> }
  <- 103
  ```
-->

Se você escrever mais de um bloco `defer` no mesmo escopo,
o primeiro que você especificar será o último a ser executado.

```swift
if score < 10 {
    defer {
        print(score)
    }
    defer {
        print("The score is:")
    }
    score += 5
}
// Prints "The score is:".
// Prints "6".
```

<!--
  - test: `defer-with-if`

  ```swifttest
  -> if score < 10 {
  ->     defer {
  ->         print(score)
  ->     }
  ->     defer {
  ->         print("The score is:")
  ->     }
  ->     score += 5
  -> }
  <- 6
  ```
-->

Se o seu programa parar de executar, por exemplo por causa de um erro de tempo de execução
ou de uma falha, o código adiado não é executado.
No entanto, o código adiado é executado depois que um erro é lançado;
para informações sobre como usar `defer` com tratamento de erros,
veja <doc:ErrorHandling#Specifying-Cleanup-Actions>.

## Verificando a disponibilidade de APIs

O Swift tem suporte nativo para verificar a disponibilidade de APIs,
o que garante que você não use por engano APIs indisponíveis
em um determinado alvo de implantação.

O compilador usa as informações de disponibilidade do SDK
para verificar se todas as APIs usadas no seu código
estão disponíveis no alvo de implantação especificado pelo seu projeto.
O Swift reporta um erro em tempo de compilação
se você tentar usar uma API que não está disponível.

Você usa uma *condição de disponibilidade* em uma instrução `if` ou `guard`
para executar condicionalmente um bloco de código,
dependendo de as APIs que você quer usar estarem disponíveis em tempo de execução.
O compilador usa as informações da condição de disponibilidade
ao verificar se as APIs naquele bloco de código estão disponíveis.

```swift
if #available(iOS 10, macOS 10.12, *) {
    // Use iOS 10 APIs on iOS, and use macOS 10.12 APIs on macOS
} else {
    // Fall back to earlier iOS and macOS APIs
}
```

<!--
  - test: `availability`

  ```swifttest
  -> if #available(iOS 10, macOS 10.12, *) {
         // Use iOS 10 APIs on iOS, and use macOS 10.12 APIs on macOS
     } else {
         // Fall back to earlier iOS and macOS APIs
     }
  ```
-->

A condição de disponibilidade acima especifica que, no iOS,
o corpo da instrução `if` é executado somente no iOS 10 ou posterior;
no macOS, somente no macOS 10.12 ou posterior.
O último argumento, `*`, é obrigatório e especifica que, em qualquer outra plataforma,
o corpo do `if` é executado no alvo de implantação mínimo especificado pelo seu target.

Em sua forma geral, a condição de disponibilidade recebe uma lista de nomes de plataformas e versões.
Você usa nomes de plataformas como `iOS`, `macOS`, `watchOS`, `tvOS` e `visionOS`.
Para a lista completa, veja <doc:Attributes#Declaration-Attributes>.
Além de especificar números de versão principal, como iOS 8 ou macOS 10.10,
você pode especificar números de versão secundária, como iOS 11.2.6 e macOS 10.13.3.

```swift
if #available(<#platform name#> <#version#>, <#...#>, *) {
    <#statements to execute if the APIs are available#>
} else {
    <#fallback statements to execute if the APIs are unavailable#>
}
```

Quando você usa uma condição de disponibilidade com uma instrução `guard`,
ela refina as informações de disponibilidade usadas no restante do código desse bloco.

```swift
@available(macOS 10.12, *)
struct ColorPreference {
    var bestColor = "blue"
}

func chooseBestColor() -> String {
    guard #available(macOS 10.12, *) else {
       return "gray"
    }
    let colors = ColorPreference()
    return colors.bestColor
}
```

<!--
  - test: `guard-with-pound-available`

  ```swifttest
  -> @available(macOS 10.12, *)
  -> struct ColorPreference {
         var bestColor = "blue"
     }

  -> func chooseBestColor() -> String {
        guard #available(macOS 10.12, *) else {
            return "gray"
        }
        let colors = ColorPreference()
        return colors.bestColor
     }
  >> print(chooseBestColor())
  << blue
  ```
-->

No exemplo acima, a struct `ColorPreference` exige macOS 10.12 ou posterior.
A função `chooseBestColor()` começa com uma instrução `guard` de disponibilidade.
Se a versão da plataforma for antiga demais para usar `ColorPreference`,
ela recorre a um comportamento que está sempre disponível.
Depois da instrução `guard`, você pode usar APIs que exigem macOS 10.12 ou posterior.

Além de `#available`, o Swift também oferece suporte à verificação oposta,
usando uma condição de indisponibilidade.
Por exemplo, as duas verificações a seguir fazem a mesma coisa:

```swift
if #available(iOS 10, *) {
} else {
    // Fallback code
}

if #unavailable(iOS 10) {
    // Fallback code
}
```

<!--
  - test: `availability-and-unavailability`

  ```swifttest
  -> if #available(iOS 10, *) {
     } else {
        // Fallback code
     }

  -> if #unavailable(iOS 10) {
        // Fallback code
     }
  ```
-->

Usar a forma `#unavailable` ajuda a tornar o código mais legível
quando a verificação contém apenas código alternativo.

<!--
  FIXME
  Not a general purpose condition; can't combine with &&, etc.
  You can use it with if-let, and other Boolean conditions, using a comma
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->

<!-- ia-translate: true -->
