# Conceitos básicos

Trabalhe com tipos de dados comuns e escreva a sintaxe básica.

O Swift oferece muitos tipos de dados fundamentais,
incluindo `Int` para inteiros,
`Double` para valores de ponto flutuante,
`Bool` para valores booleanos
e `String` para texto.
O Swift também oferece versões poderosas dos três tipos de coleção principais,
`Array`, `Set` e `Dictionary`,
como descrito em <doc:CollectionTypes>.

O Swift usa variáveis para armazenar valores e referenciá-los por um nome de identificação.
O Swift também usa muito as constantes, cujo valor não pode ser alterado depois de definido.
Elas tornam o código mais seguro e deixam mais clara a intenção
quando você trabalha com valores que não precisam mudar.

Além dos tipos conhecidos, o Swift traz tipos avançados, como as tuplas.
Tuplas permitem criar e passar agrupamentos de valores.
Você pode usar uma tupla para retornar vários valores de uma função como um único valor composto.

O Swift trata a ausência de um valor
usando tipos optional.
Optionals dizem “há *um* valor, que é *x*”
ou “não há valor algum”.
Optionals garantem que o código sempre verifique se um valor está ausente antes de usá-lo,
e valores não optional têm a garantia de nunca estar ausentes.

O Swift é uma linguagem segura,
o que significa que facilita encontrar e corrigir várias categorias de bugs
o quanto antes durante o processo de desenvolvimento,
e permite garantir que certos tipos de bugs não podem acontecer.
A segurança de tipos permite que você seja claro sobre
os tipos de valores com que seu código trabalha.
Se uma parte do código exige uma `String`,
a segurança de tipos impede que você passe um `Int` por engano.
A segurança de memória garante que você trabalhe apenas com dados válidos,
não com memória não inicializada ou objetos desinicializados,
e garante que você trabalhe com esses dados de forma segura,
mesmo em programas que executam vários trechos de código ao mesmo tempo.
O Swift faz a maior parte das verificações de segurança durante a compilação do código,
e, em alguns casos, faz verificações adicionais enquanto o código está em execução.

## Constantes e variáveis

Constantes e variáveis associam um nome
(como `maximumNumberOfLoginAttempts` ou `welcomeMessage`)
a um valor de um tipo específico
(como o número `10` ou a string `"Hello"`).
O valor de uma *constante* não pode ser alterado depois de definido,
enquanto uma *variável* pode receber outro valor no futuro.

### Declarando constantes e variáveis

Constantes e variáveis precisam ser declaradas antes de serem usadas.
Você declara constantes com a palavra-chave `let`
e variáveis com a palavra-chave `var`.
Veja um exemplo de como constantes e variáveis podem ser usadas
para contar as tentativas de login que um usuário fez:

```swift
let maximumNumberOfLoginAttempts = 10
var currentLoginAttempt = 0
```

<!--
  - test: `constantsAndVariables`

  ```swifttest
  -> let maximumNumberOfLoginAttempts = 10
  -> var currentLoginAttempt = 0
  ```
-->

Esse código pode ser lido assim:

“Declare uma nova constante chamada `maximumNumberOfLoginAttempts`
e atribua a ela o valor `10`.
Depois, declare uma nova variável chamada `currentLoginAttempt`
e dê a ela o valor inicial `0`.”

Neste exemplo,
o número máximo de tentativas de login permitidas é declarado como constante,
porque esse valor máximo nunca muda.
O contador de tentativas de login atual é declarado como variável,
porque esse valor precisa ser incrementado após cada tentativa de login malsucedida.

Se um valor armazenado no seu código não vai mudar,
sempre declare-o como constante com a palavra-chave `let`.
Use variáveis apenas para armazenar valores que mudam.

Ao declarar uma constante ou uma variável,
você pode dar a ela um valor como parte dessa declaração,
como nos exemplos acima.
Como alternativa,
você pode atribuir o valor inicial mais adiante no programa,
desde que ele seja garantido antes da primeira vez que você o ler.

```swift
var environment = "development"
let maximumNumberOfLoginAttempts: Int
// maximumNumberOfLoginAttempts has no value yet.

if environment == "development" {
    maximumNumberOfLoginAttempts = 100
} else {
    maximumNumberOfLoginAttempts = 10
}
// Now maximumNumberOfLoginAttempts has a value, and can be read.
```

<!--
  - test: `constantsWithDeferredInitialization`

  ```swifttest
  -> var environment = "development"
  -> let maximumNumberOfLoginAttempts: Int
  -> if environment == "development" {
         maximumNumberOfLoginAttempts = 100
     } else {
         maximumNumberOfLoginAttempts = 10
     }
  >> print(maxNumberOfLoginAttempts)
  << 100
  ```
-->

Neste exemplo,
o número máximo de tentativas de login é constante,
e seu valor depende do ambiente.
No ambiente de desenvolvimento, ele vale 100;
em qualquer outro ambiente, vale 10.
Os dois ramos da instrução `if` inicializam `maximumNumberOfLoginAttempts` com algum valor,
garantindo que a constante sempre receba um valor.
Para saber como o Swift verifica seu código
quando você define um valor inicial dessa forma,
veja <doc:Declarations#Constant-Declaration>.

Você pode declarar várias constantes ou várias variáveis em uma única linha,
separadas por vírgulas:

```swift
var x = 0.0, y = 0.0, z = 0.0
```

<!--
  - test: `multipleDeclarations`

  ```swifttest
  -> var x = 0.0, y = 0.0, z = 0.0
  >> print(x, y, z)
  << 0.0 0.0 0.0
  ```
-->

### Anotações de tipo

Você pode fornecer uma *anotação de tipo* ao declarar uma constante ou variável,
para deixar claro o tipo de valores que ela pode armazenar.
Escreva uma anotação de tipo colocando dois-pontos depois do nome da constante ou variável,
seguidos de um espaço e do nome do tipo a usar.

Este exemplo fornece uma anotação de tipo para uma variável chamada `welcomeMessage`,
para indicar que ela pode armazenar valores `String`:

```swift
var welcomeMessage: String
```

<!--
  - test: `typeAnnotations`

  ```swifttest
  -> var welcomeMessage: String
  ```
-->

Os dois-pontos na declaração significam “…do tipo…”,
então o código acima pode ser lido assim:

“Declare uma variável chamada `welcomeMessage` que é do tipo `String`.”

A expressão “do tipo `String`” significa “pode armazenar qualquer valor `String`”.
Pense nisso como “o tipo de coisa” (ou “a espécie de coisa”) que pode ser armazenada.

A variável `welcomeMessage` agora pode receber qualquer valor de string sem erro:

```swift
welcomeMessage = "Hello"
```

<!--
  - test: `typeAnnotations`

  ```swifttest
  -> welcomeMessage = "Hello"
  >> print(welcomeMessage)
  << Hello
  ```
-->

Você pode definir várias variáveis relacionadas do mesmo tipo em uma única linha,
separadas por vírgulas, com uma única anotação de tipo depois do nome da última variável:

```swift
var red, green, blue: Double
```

<!--
  - test: `typeAnnotations`

  ```swifttest
  -> var red, green, blue: Double
  ```
-->

> Nota: Raramente é preciso escrever anotações de tipo na prática.
> Se você fornecer um valor inicial para uma constante ou variável no momento em que ela é definida,
> o Swift quase sempre consegue inferir o tipo a ser usado para essa constante ou variável,
> como descrito em <doc:TheBasics#Type-Safety-and-Type-Inference>.
> No exemplo `welcomeMessage` acima, nenhum valor inicial é fornecido,
> então o tipo da variável `welcomeMessage` é especificado com uma anotação de tipo
> em vez de ser inferido a partir de um valor inicial.

### Nomeando constantes e variáveis

Nomes de constantes e variáveis podem conter quase qualquer caractere,
incluindo caracteres Unicode:

```swift
let π = 3.14159
let 你好 = "你好世界"
let 🐶🐮 = "dogcow"
```

<!--
  - test: `constantsAndVariables`

  ```swifttest
  -> let π = 3.14159
  -> let 你好 = "你好世界"
  -> let 🐶🐮 = "dogcow"
  ```
-->

Nomes de constantes e variáveis não podem conter caracteres de espaço em branco,
símbolos matemáticos, setas, escalares Unicode de uso privado
nem caracteres de desenho de linhas e de caixas.
Também não podem começar com um número,
embora números possam aparecer em outras posições do nome.

Depois de declarar uma constante ou variável de determinado tipo,
você não pode declará-la de novo com o mesmo nome
nem alterá-la para armazenar valores de outro tipo.
Também não é possível transformar uma constante em variável
nem uma variável em constante.

> Nota: Se você precisar dar a uma constante ou variável o mesmo nome de uma palavra-chave reservada do Swift,
> envolva a palavra-chave com crases (`` ` ``) ao usá-la como nome.
> No entanto, evite usar palavras-chave como nomes, a menos que você não tenha nenhuma outra escolha.

Você pode alterar o valor de uma variável existente para outro valor de tipo compatível.
Neste exemplo, o valor de `friendlyWelcome` é trocado de
`"Hello!"` para `"Bonjour!"`:

```swift
var friendlyWelcome = "Hello!"
friendlyWelcome = "Bonjour!"
// friendlyWelcome is now "Bonjour!"
```

<!--
  - test: `constantsAndVariables`

  ```swifttest
  -> var friendlyWelcome = "Hello!"
  -> friendlyWelcome = "Bonjour!"
  /> friendlyWelcome is now \"\(friendlyWelcome)\"
  </ friendlyWelcome is now "Bonjour!"
  ```
-->

Diferentemente de uma variável, o valor de uma constante não pode ser alterado depois de definido.
Tentar fazer isso é reportado como erro quando o código é compilado:

```swift
let languageName = "Swift"
languageName = "Swift++"
// This is a compile-time error: languageName cannot be changed.
```

<!--
  - test: `constantsAndVariables_err`

  ```swifttest
  -> let languageName = "Swift"
  -> languageName = "Swift++"
  // This is a compile-time error: languageName cannot be changed.
  !$ error: cannot assign to value: 'languageName' is a 'let' constant
  !! languageName = "Swift++"
  !! ^~~~~~~~~~~~
  !! /tmp/swifttest.swift:1:1: note: change 'let' to 'var' to make it mutable
  !! let languageName = "Swift"
  !! ^~~
  !! var
  ```
-->

### Imprimindo constantes e variáveis

Você pode imprimir o valor atual de uma constante ou variável com a função `print(_:separator:terminator:)`:

```swift
print(friendlyWelcome)
// Prints "Bonjour!"
```

<!--
  - test: `constantsAndVariables`

  ```swifttest
  -> print(friendlyWelcome)
  <- Bonjour!
  ```
-->

A função `print(_:separator:terminator:)` é uma função global
que imprime um ou mais valores em uma saída apropriada.
No Xcode, por exemplo,
a função `print(_:separator:terminator:)` mostra sua saída no painel “console” do Xcode.
Os parâmetros `separator` e `terminator` têm valores padrão,
então você pode omiti-los ao chamar essa função.
Por padrão, a função encerra a linha que imprime adicionando uma quebra de linha.
Para imprimir um valor sem quebra de linha depois dele,
passe uma string vazia como `terminator`,
por exemplo, `print(someValue, terminator: "")`.
Para saber mais sobre parâmetros com valores padrão,
veja <doc:Functions#Default-Parameter-Values>.

<!--
  - test: `printingWithoutNewline`

  ```swifttest
  >> let someValue = 10
  -> print(someValue, terminator: "")
  -> print(someValue)
  << 1010
  ```
-->

<!--
  QUESTION: have I referred to Xcode's console correctly here?
  Should I mention other output streams, such as the REPL / playgrounds?
-->

<!--
  NOTE: this is a deliberately simplistic description of what you can do with print().
  It will be expanded later on.
-->

O Swift usa *interpolação de string* para incluir o nome de uma constante ou variável
como marcador em uma string maior,
fazendo com que o Swift o substitua pelo valor atual dessa constante ou variável.
Coloque o nome entre parênteses e escreva uma barra invertida antes do parêntese de abertura:

```swift
print("The current value of friendlyWelcome is \(friendlyWelcome)")
// Prints "The current value of friendlyWelcome is Bonjour!"
```

<!--
  - test: `constantsAndVariables`

  ```swifttest
  -> print("The current value of friendlyWelcome is \(friendlyWelcome)")
  <- The current value of friendlyWelcome is Bonjour!
  ```
-->

> Nota: Todas as opções que você pode usar com a interpolação de string
> são descritas em <doc:StringsAndCharacters#String-Interpolation>.

## Comentários

Use comentários para incluir texto não executável no seu código,
como uma anotação ou um lembrete para você mesmo.
Os comentários são ignorados pelo compilador do Swift quando o código é compilado.

Os comentários em Swift são muito parecidos com os comentários em C.
Comentários de uma linha começam com duas barras (`//`):

```swift
// This is a comment.
```

<!--
  - test: `comments`

  ```swifttest
  -> // This is a comment.
  ```
-->

Comentários de múltiplas linhas começam com uma barra seguida de um asterisco (`/*`)
e terminam com um asterisco seguido de uma barra (`*/`):

```swift
/* This is also a comment
but is written over multiple lines. */
```

<!--
  - test: `comments`

  ```swifttest
  -> /* This is also a comment
     but is written over multiple lines. */
  ```
-->

Diferentemente dos comentários de múltiplas linhas em C,
os comentários de múltiplas linhas em Swift podem ser aninhados dentro de outros comentários de múltiplas linhas.
Você escreve comentários aninhados abrindo um bloco de comentário de múltiplas linhas
e depois abrindo um segundo comentário de múltiplas linhas dentro do primeiro bloco.
O segundo bloco é então fechado, seguido do primeiro:

```swift
/* This is the start of the first multiline comment.
    /* This is the second, nested multiline comment. */
This is the end of the first multiline comment. */
```

<!--
  - test: `comments`

  ```swifttest
  -> /* This is the start of the first multiline comment.
        /* This is the second, nested multiline comment. */
     This is the end of the first multiline comment. */
  ```
-->

Comentários aninhados de múltiplas linhas permitem comentar blocos grandes de código
de forma rápida e fácil, mesmo que o código já contenha comentários de múltiplas linhas.

## Ponto e vírgula

Diferentemente de muitas outras linguagens,
o Swift não exige que você escreva um ponto e vírgula (`;`) depois de cada instrução do código,
embora você possa fazer isso se quiser.
No entanto, o ponto e vírgula *é* obrigatório
se você quiser escrever várias instruções separadas em uma única linha:

```swift
let cat = "🐱"; print(cat)
// Prints "🐱".
```

<!--
  - test: `semiColons`

  ```swifttest
  -> let cat = "🐱"; print(cat)
  <- 🐱
  ```
-->

## Inteiros

*Inteiros* são números inteiros, sem componente fracionário,
como `42` e `-23`.
Os inteiros são *com sinal* (positivos, zero ou negativos)
ou *sem sinal* (positivos ou zero),
e seus valores máximo e mínimo dependem do seu *tamanho*
(a quantidade de bits usados para armazenar valores).
Os tipos inteiros incluem o tamanho e o sinal no nome:
por exemplo, um inteiro sem sinal de 8 bits é do tipo `UInt8`,
e um inteiro com sinal de 32 bits é do tipo `Int32`.
Como todos os tipos em Swift, esses tipos inteiros têm nomes com inicial maiúscula.
Na maioria dos casos, quando você não precisa especificar o tamanho exato do inteiro,
usa o tipo `Int`, descrito abaixo.

Os tipos inteiros se comportam como a maioria das contas que você faz à mão;
a aritmética com inteiros produz resultados sem aproximação.
Essas características tornam os inteiros adequados para contar
e para outros cálculos que representam quantias exatas,
por exemplo, encontrar a linha mais longa de um arquivo de texto,
aplicar um multiplicador de pontuação em um jogo
ou somar os preços de um recibo.

Embora inteiros não tenham componente fracionário,
você pode usá-los para representar quantidades com frações
contando uma parte fracionária.
Por exemplo,
você pode representar US$ 1,23 armazenando o número `123`
em um inteiro que conta centavos.
Essa abordagem é conhecida como *matemática de ponto fixo*,
porque o separador decimal fica em uma posição fixa do número.
No exemplo acima,
entende-se que o número `123` tem um separador decimal antes dos dois últimos dígitos.

> Nota:
> Para cálculos em áreas reguladas, como finanças ou construção,
> ou em um domínio que espera resultados de alta precisão,
> você pode precisar de um tipo numérico de finalidade específica
> que implemente comportamentos como arredondamento e truncamento,
> de acordo com os requisitos dessa área.

### Limites dos inteiros

Você pode acessar os valores mínimo e máximo de cada tipo inteiro
pelas propriedades `min` e `max`:

```swift
let minValue = UInt8.min  // minValue is equal to 0, and is of type UInt8
let maxValue = UInt8.max  // maxValue is equal to 255, and is of type UInt8
```

<!--
  - test: `integerBounds`

  ```swifttest
  -> let minValue = UInt8.min  // minValue is equal to 0, and is of type UInt8
  -> let maxValue = UInt8.max  // maxValue is equal to 255, and is of type UInt8
  >> print(minValue, maxValue)
  << 0 255
  ```
-->

Os valores dessas propriedades são do tipo numérico de tamanho apropriado
(como `UInt8` no exemplo acima)
e, por isso, podem ser usados em expressões junto com outros valores do mesmo tipo.

Cálculos que produzem resultados fora dos limites,
como um número maior que a propriedade `max`,
interrompem a execução do programa em vez de armazenar um resultado inválido.
Você pode, de forma explícita, fazer a operação estourar (overflow),
como descrito em <doc:AdvancedOperators#Overflow-Operators>.

### Int

Na maioria dos casos, você não precisa escolher um tamanho específico de inteiro para usar no código.
O Swift oferece um tipo inteiro adicional, `Int`,
que tem o mesmo tamanho da palavra nativa da plataforma atual:

- Em uma plataforma de 32 bits, `Int` tem o mesmo tamanho de `Int32`.
- Em uma plataforma de 64 bits, `Int` tem o mesmo tamanho de `Int64`.

A menos que você precise trabalhar com um tamanho específico de inteiro,
use sempre `Int` para valores inteiros no código.
Isso ajuda na consistência e na interoperabilidade do código.
Mesmo em plataformas de 32 bits, `Int` pode armazenar qualquer valor entre `-2,147,483,648` e `2,147,483,647`,
e é grande o bastante para muitos intervalos de inteiros.

### UInt

O Swift também oferece um tipo inteiro sem sinal, `UInt`,
que tem o mesmo tamanho da palavra nativa da plataforma atual:

- Em uma plataforma de 32 bits, `UInt` tem o mesmo tamanho de `UInt32`.
- Em uma plataforma de 64 bits, `UInt` tem o mesmo tamanho de `UInt64`.

> Nota: Use `UInt` somente quando você precisar especificamente
> de um tipo inteiro sem sinal com o mesmo tamanho da palavra nativa da plataforma.
> Se não for o caso, `Int` é preferível,
> mesmo quando os valores a armazenar são conhecidamente não negativos.
> O uso consistente de `Int` para valores inteiros ajuda na interoperabilidade do código,
> evita a necessidade de converter entre diferentes tipos numéricos
> e combina com a inferência de tipo inteiro, como descrito em <doc:TheBasics#Type-Safety-and-Type-Inference>.

## Números de ponto flutuante

*Números de ponto flutuante* têm componente fracionário,
como `3.14159`, `0.1` e `-273.15`.
O Swift oferece vários tipos de ponto flutuante que cobrem diferentes tamanhos de número,
assim como oferece diferentes tamanhos de inteiros.
Se você não precisar especificar um tamanho exato, use `Double`.
Caso contrário, use o tipo que inclui o tamanho necessário no nome,
como `Float16` ou `Float80`.
Seguindo a terminologia comum da matemática de ponto flutuante,
`Float` usa 32 bits e `Double` usa 64 bits.
Você também pode escrever esses tipos como `Float32` ou `Float64`.
Por exemplo,
código de gráficos costuma usar `Float` para combinar com o tipo de dado mais rápido da GPU.
Alguns tipos de ponto flutuante só estão disponíveis em certas plataformas,
mas `Float` e `Double` estão disponíveis em todas as plataformas.

Números de ponto flutuante permitem trabalhar com valores muito pequenos e muito grandes,
mas não conseguem representar todos os valores possíveis nesse intervalo.
Diferentemente dos cálculos com inteiros, que sempre produzem um resultado exato,
a matemática de ponto flutuante arredonda os resultados para o número representável mais próximo.
Por exemplo,
ao armazenar o número 10.000 como `Float`,
o próximo maior número que você consegue representar é 10.000,001:
valores entre esses dois números são arredondados para um ou para o outro.
O espaçamento entre os números também varia;
há espaços maiores entre números grandes do que entre números pequenos.
Por exemplo,
o próximo valor de `Float` depois de 0,001 é 0,0010000002,
que é menor que o espaçamento depois de 10.000.

<!---
var n: Float = 10_000
print(n.nextUp)
n = 0.001
print(n.nextUp)
-->

Números de ponto flutuante têm valores para zero negativo, infinito e infinito negativo,
que representam estouro (overflow) e subfluxo (underflow) nos cálculos.
Eles também têm valores NaN (*not-a-number*, ou não é um número)
para representar um resultado inválido ou indefinido,
como dividir zero por zero.
Esse comportamento é diferente dos inteiros,
que interrompem o programa se não conseguirem representar o resultado.

Se você precisar do mesmo espaçamento entre todos os valores possíveis,
ou se os cálculos que você faz exigem resultados exatos
e não envolvem os valores especiais listados acima,
um número de ponto flutuante talvez não seja o tipo de dado certo.
Considere usar números de ponto fixo, como descrito em <doc:TheBasics#Integers>.

## Segurança de tipos e inferência de tipos

Todo valor em um programa Swift tem um tipo.
Todo lugar onde você armazena um valor,
incluindo constantes, variáveis e propriedades,
também tem um tipo.
Você pode escrever o tipo explicitamente usando uma anotação de tipo,
ou o Swift pode inferir o tipo a partir de um valor inicial.
Em todo lugar do código em que você fornece um valor,
o tipo desse valor precisa corresponder ao lugar em que você o usa.
Por exemplo,
se uma parte do código exige uma `String`,
você não pode passar um `Int` por engano.
Esse tipo de verificação torna o Swift uma linguagem *type-safe*, ou seja, com segurança de tipos.

Uma linguagem com segurança de tipos incentiva você a ser claro
sobre os tipos de valores com que seu código trabalha.
Valores de um tipo nunca são convertidos implicitamente para outro tipo.
No entanto, alguns tipos podem ser convertidos explicitamente.
Ao compilar o código, o Swift verifica a segurança de tipos
e marca qualquer tipo incompatível como erro.

A verificação de tipos ajuda a evitar erros quando você trabalha com diferentes tipos de valores.
No entanto, isso não significa que você precise especificar o tipo de cada constante
e de cada variável que declara.
Se você não especificar o tipo do valor de que precisa,
o Swift usa *inferência de tipos* para descobrir o tipo apropriado.
A inferência de tipos permite que o compilador deduza automaticamente
o tipo de uma expressão específica ao compilar o código,
simplesmente examinando os valores que você fornece.

Por causa da inferência de tipos, o Swift exige bem menos declarações de tipo
do que linguagens como C ou Objective-C.
Constantes e variáveis continuam com um tipo definido,
mas grande parte do trabalho de especificar esse tipo é feito por você.

A inferência de tipos é especialmente útil
quando você declara uma constante ou variável com um valor inicial.
Isso costuma ser feito atribuindo um *valor literal* (ou *literal*)
à constante ou variável no momento em que você a declara.
(Um valor literal é um valor que aparece diretamente no código-fonte,
como `42` e `3.14159` nos exemplos abaixo.)

Por exemplo, se você atribuir um valor literal `42` a uma nova constante
sem dizer qual é o tipo,
o Swift infere que você quer que a constante seja um `Int`,
porque você a inicializou com um número que parece um inteiro:

```swift
let meaningOfLife = 42
// meaningOfLife is inferred to be of type Int
```

<!--
  - test: `typeInference`

  ```swifttest
  -> let meaningOfLife = 42
  // meaningOfLife is inferred to be of type Int
  >> print(type(of: meaningOfLife))
  << Int
  ```
-->

Da mesma forma, se você não especificar o tipo de um literal de ponto flutuante,
o Swift infere que você quer criar um `Double`:

```swift
let pi = 3.14159
// pi is inferred to be of type Double
```

<!--
  - test: `typeInference`

  ```swifttest
  -> let pi = 3.14159
  // pi is inferred to be of type Double
  >> print(type(of: pi))
  << Double
  ```
-->

O Swift sempre escolhe `Double` (em vez de `Float`)
ao inferir o tipo de números de ponto flutuante.

Se você combinar literais inteiros e de ponto flutuante em uma expressão,
o tipo `Double` será inferido a partir do contexto:

```swift
let anotherPi = 3 + 0.14159
// anotherPi is also inferred to be of type Double
```

<!--
  - test: `typeInference`

  ```swifttest
  -> let anotherPi = 3 + 0.14159
  // anotherPi is also inferred to be of type Double
  >> print(type(of: anotherPi))
  << Double
  ```
-->

O valor literal `3` não tem tipo explícito por si só,
por isso o tipo de saída apropriado, `Double`,
é inferido a partir da presença de um literal de ponto flutuante como parte da soma.

## Literais numéricos

Literais inteiros podem ser escritos como:

- Um número *decimal*, sem prefixo
- Um número *binário*, com prefixo `0b`
- Um número *octal*, com prefixo `0o`
- Um número *hexadecimal*, com prefixo `0x`

Todos estes literais inteiros têm o valor decimal `17`:

```swift
let decimalInteger = 17
let binaryInteger = 0b10001       // 17 in binary notation
let octalInteger = 0o21           // 17 in octal notation
let hexadecimalInteger = 0x11     // 17 in hexadecimal notation
```

<!--
  - test: `numberLiterals`

  ```swifttest
  -> let decimalInteger = 17
  -> let binaryInteger = 0b10001       // 17 in binary notation
  -> let octalInteger = 0o21           // 17 in octal notation
  -> let hexadecimalInteger = 0x11     // 17 in hexadecimal notation
  >> print(binaryInteger, octalInteger, hexadecimalInteger)
  << 17 17 17
  ```
-->

Literais de ponto flutuante podem ser decimais (sem prefixo)
ou hexadecimais (com prefixo `0x`).
Eles sempre devem ter um número (ou um número hexadecimal) dos dois lados do separador decimal.
Literais decimais de ponto flutuante também podem ter um *expoente* opcional,
indicado por `e` maiúsculo ou minúsculo;
literais hexadecimais de ponto flutuante devem ter um expoente,
indicado por `p` maiúsculo ou minúsculo.

<!--
  - test: `float-required-vs-optional-exponent-err`

  ```swifttest
  -> let hexWithout = 0x1.5
  !$ error: hexadecimal floating point literal must end with an exponent
  !! let hexWithout = 0x1.5
  !!                       ^
  ```
-->

<!--
  - test: `float-required-vs-optional-exponent`

  ```swifttest
  -> let hexWith = 0x1.5p7
  -> let decimalWithout = 0.5
  -> let decimalWith = 0.5e7
  ```
-->

Para números decimais com expoente `x`,
o número base é multiplicado por 10ˣ:

- `1.25e2` significa 1,25 x 10², ou `125.0`.
- `1.25e-2` significa 1,25 x 10⁻², ou `0.0125`.

Para números hexadecimais com expoente `x`,
o número base é multiplicado por 2ˣ:

- `0xFp2` significa 15 x 2², ou `60.0`.
- `0xFp-2` significa 15 x 2⁻², ou `3.75`.

Todos estes literais de ponto flutuante têm o valor decimal `12.1875`:

```swift
let decimalDouble = 12.1875
let exponentDouble = 1.21875e1
let hexadecimalDouble = 0xC.3p0
```

<!--
  - test: `numberLiterals`

  ```swifttest
  -> let decimalDouble = 12.1875
  -> let exponentDouble = 1.21875e1
  -> let hexadecimalDouble = 0xC.3p0
  ```
-->

Literais numéricos podem conter formatação extra para facilitar a leitura.
Tanto inteiros quanto números de ponto flutuante podem ter zeros extras
e podem conter sublinhados para ajudar na legibilidade.
Nenhum desses tipos de formatação altera o valor subjacente do literal:

```swift
let paddedDouble = 000123.456
let oneMillion = 1_000_000
let justOverOneMillion = 1_000_000.000_000_1
```

<!--
  - test: `numberLiterals`

  ```swifttest
  -> let paddedDouble = 000123.456
  -> let oneMillion = 1_000_000
  -> let justOverOneMillion = 1_000_000.000_000_1
  ```
-->

## Conversão de tipos numéricos

Use o tipo `Int` para todas as constantes e variáveis inteiras de uso geral no código,
mesmo quando se sabe que não são negativas.
Usar o tipo inteiro padrão em situações do dia a dia significa que
constantes e variáveis inteiras são imediatamente interoperáveis no código
e vão combinar com o tipo inferido para valores literais inteiros.

Use outros tipos inteiros somente quando eles forem especificamente necessários para a tarefa,
por causa de dados com tamanho explícito vindos de uma fonte externa,
ou por desempenho, uso de memória ou outra otimização necessária.
Usar tipos com tamanho explícito nessas situações ajuda a detectar estouros acidentais de valor
e documenta implicitamente a natureza dos dados usados.

### Conversão de inteiros

O intervalo de números que podem ser armazenados em uma constante ou variável inteira
é diferente para cada tipo numérico.
Uma constante ou variável `Int8` pode armazenar números entre `-128` e `127`,
enquanto uma constante ou variável `UInt8` pode armazenar números entre `0` e `255`.
Um número que não cabe em uma constante ou variável de um tipo inteiro com tamanho definido
é reportado como erro quando o código é compilado:

```swift
let cannotBeNegative: UInt8 = -1
// UInt8 can't store negative numbers, and so this will report an error
let tooBig: Int8 = Int8.max + 1
// Int8 can't store a number larger than its maximum value,
// and so this will also report an error
```

<!--
  - test: `constantsAndVariablesOverflowError`

  ```swifttest
  -> let cannotBeNegative: UInt8 = -1
  // UInt8 can't store negative numbers, and so this will report an error
  -> let tooBig: Int8 = Int8.max + 1
  // Int8 can't store a number larger than its maximum value,
  // and so this will also report an error
  !! /tmp/swifttest.swift:2:29: error: arithmetic operation '127 + 1' (on type 'Int8') results in an overflow
  !! let tooBig: Int8 = Int8.max + 1
  !!                    ~~~~~~~~ ^ ~
  !! /tmp/swifttest.swift:1:31: error: negative integer '-1' overflows when stored into unsigned type 'UInt8'
  !! let cannotBeNegative: UInt8 = -1
  !!                                ^
  ```
-->

Como cada tipo numérico pode armazenar um intervalo diferente de valores,
você precisa optar pela conversão de tipo numérico caso a caso.
Essa abordagem de optar explicitamente evita erros de conversão ocultos
e ajuda a deixar explícita no código a intenção da conversão de tipo.

Para converter um tipo numérico específico em outro,
você inicializa um novo número do tipo desejado com o valor existente.
No exemplo abaixo,
a constante `twoThousand` é do tipo `UInt16`,
enquanto a constante `one` é do tipo `UInt8`.
Elas não podem ser somadas diretamente,
porque não são do mesmo tipo.
Em vez disso, este exemplo chama `UInt16(one)` para criar um novo `UInt16`
inicializado com o valor de `one`,
e usa esse valor no lugar do original:

```swift
let twoThousand: UInt16 = 2_000
let one: UInt8 = 1
let twoThousandAndOne = twoThousand + UInt16(one)
```

<!--
  - test: `typeConversion`

  ```swifttest
  -> let twoThousand: UInt16 = 2_000
  -> let one: UInt8 = 1
  -> let twoThousandAndOne = twoThousand + UInt16(one)
  >> print(twoThousandAndOne)
  << 2001
  ```
-->

Como os dois lados da soma agora são do tipo `UInt16`,
a soma é permitida.
A constante de saída (`twoThousandAndOne`) é inferida como do tipo `UInt16`,
porque é a soma de dois valores `UInt16`.

`SomeType(ofInitialValue)` é a forma padrão de chamar o inicializador de um tipo Swift
e passar um valor inicial.
Nos bastidores, `UInt16` tem um inicializador que aceita um valor `UInt8`,
e por isso esse inicializador é usado para criar um novo `UInt16` a partir de um `UInt8` existente.
No entanto, você não pode passar *qualquer* tipo aqui:
ele precisa ser um tipo para o qual `UInt16` forneça um inicializador.
Estender tipos existentes para fornecer inicializadores que aceitam novos tipos
(incluindo as suas próprias definições de tipo)
é tratado em <doc:Extensions>.

### Conversão entre inteiros e números de ponto flutuante

Conversões entre tipos numéricos inteiros e de ponto flutuante devem ser explícitas:

```swift
let three = 3
let pointOneFourOneFiveNine = 0.14159
let pi = Double(three) + pointOneFourOneFiveNine
// pi equals 3.14159, and is inferred to be of type Double
```

<!--
  - test: `typeConversion`

  ```swifttest
  -> let three = 3
  -> let pointOneFourOneFiveNine = 0.14159
  -> let pi = Double(three) + pointOneFourOneFiveNine
  /> pi equals \(pi), and is inferred to be of type Double
  </ pi equals 3.14159, and is inferred to be of type Double
  ```
-->

Aqui, o valor da constante `three` é usado para criar um novo valor do tipo `Double`,
de modo que os dois lados da soma sejam do mesmo tipo.
Sem essa conversão, a soma não seria permitida.

A conversão de ponto flutuante para inteiro também deve ser explícita.
Um tipo inteiro pode ser inicializado com um valor `Double` ou `Float`:

```swift
let integerPi = Int(pi)
// integerPi equals 3, and is inferred to be of type Int
```

<!--
  - test: `typeConversion`

  ```swifttest
  -> let integerPi = Int(pi)
  /> integerPi equals \(integerPi), and is inferred to be of type Int
  </ integerPi equals 3, and is inferred to be of type Int
  ```
-->

Valores de ponto flutuante são sempre truncados quando usados para inicializar um novo valor inteiro dessa forma.
Isso significa que `4.75` vira `4`, e `-3.9` vira `-3`.

> Nota: As regras para combinar constantes e variáveis numéricas são diferentes
> das regras para literais numéricos.
> O literal `3` pode ser somado diretamente ao literal `0.14159`,
> porque literais numéricos não têm tipo explícito por si só.
> O tipo deles só é inferido no momento em que o compilador os avalia.

<!--
  NOTE: this section on explicit conversions could be included in the Operators section.
  I think it's more appropriate here, however,
  and helps to reinforce the “just use Int” message.
-->

## Aliases de tipo

*Aliases de tipo* definem um nome alternativo para um tipo existente.
Você define aliases de tipo com a palavra-chave `typealias`.

Aliases de tipo são úteis quando você quer se referir a um tipo existente
por um nome mais adequado ao contexto,
como ao trabalhar com dados de um tamanho específico vindos de uma fonte externa:

```swift
typealias AudioSample = UInt16
```

<!--
  - test: `typeAliases`

  ```swifttest
  -> typealias AudioSample = UInt16
  ```
-->

Depois de definir um alias de tipo,
você pode usar o alias em qualquer lugar onde usaria o nome original:

```swift
var maxAmplitudeFound = AudioSample.min
// maxAmplitudeFound is now 0
```

<!--
  - test: `typeAliases`

  ```swifttest
  -> var maxAmplitudeFound = AudioSample.min
  /> maxAmplitudeFound is now \(maxAmplitudeFound)
  </ maxAmplitudeFound is now 0
  ```
-->

Aqui, `AudioSample` é definido como alias de `UInt16`.
Como é um alias, a chamada a `AudioSample.min` na verdade chama `UInt16.min`,
que fornece o valor inicial `0` para a variável `maxAmplitudeFound`.

## Booleanos

O Swift tem um tipo básico *booleano*, chamado `Bool`.
Valores booleanos são chamados de *lógicos*,
porque só podem ser verdadeiros ou falsos.
O Swift oferece dois valores booleanos constantes,
`true` e `false`:

```swift
let orangesAreOrange = true
let turnipsAreDelicious = false
```

<!--
  - test: `booleans`

  ```swifttest
  -> let orangesAreOrange = true
  -> let turnipsAreDelicious = false
  ```
-->

Os tipos de `orangesAreOrange` e `turnipsAreDelicious`
foram inferidos como `Bool` pelo fato de terem sido inicializados com valores literais booleanos.
Assim como com `Int` e `Double` acima,
você não precisa declarar constantes ou variáveis como `Bool`
se as definir como `true` ou `false` logo ao criá-las.

Valores booleanos são especialmente úteis quando você trabalha com instruções condicionais,
como a instrução `if`:

```swift
if turnipsAreDelicious {
    print("Mmm, tasty turnips!")
} else {
    print("Eww, turnips are horrible.")
}
// Prints "Eww, turnips are horrible."
```

<!--
  - test: `booleans`

  ```swifttest
  -> if turnipsAreDelicious {
        print("Mmm, tasty turnips!")
     } else {
        print("Eww, turnips are horrible.")
     }
  <- Eww, turnips are horrible.
  ```
-->

Instruções condicionais, como a instrução `if`, são tratadas com mais detalhes em <doc:ControlFlow>.

A segurança de tipos do Swift impede que valores não booleanos sejam usados no lugar de `Bool`.
O exemplo a seguir reporta um erro de compilação:

```swift
let i = 1
if i {
    // this example will not compile, and will report an error
}
```

<!--
  - test: `booleansNotBoolean`

  ```swifttest
  -> let i = 1
  -> if i {
        // this example will not compile, and will report an error
     }
  !$ error: type 'Int' cannot be used as a boolean; test for '!= 0' instead
  !! if i {
  !!   ^
  !! ( != 0)
  ```
-->

No entanto, o exemplo alternativo abaixo é válido:

```swift
let i = 1
if i == 1 {
    // this example will compile successfully
}
```

<!--
  - test: `booleansIsBoolean`

  ```swifttest
  -> let i = 1
  -> if i == 1 {
        // this example will compile successfully
     }
  ```
-->

O resultado da comparação `i == 1` é do tipo `Bool`,
então este segundo exemplo passa na verificação de tipos.
Comparações como `i == 1` são discutidas em <doc:BasicOperators>.

Assim como nos outros exemplos de segurança de tipos no Swift,
essa abordagem evita erros acidentais
e garante que a intenção de um trecho específico do código esteja sempre clara.

## Tuplas

*Tuplas* agrupam vários valores em um único valor composto.
Os valores dentro de uma tupla podem ser de qualquer tipo
e não precisam ser do mesmo tipo entre si.

Neste exemplo, `(404, "Not Found")` é uma tupla que descreve um *código de status HTTP*.
Um código de status HTTP é um valor especial retornado por um servidor web sempre que você solicita uma página.
O código de status `404 Not Found` é retornado se você solicitar uma página que não existe.

```swift
let http404Error = (404, "Not Found")
// http404Error is of type (Int, String), and equals (404, "Not Found")
```

<!--
  - test: `tuples`

  ```swifttest
  -> let http404Error = (404, "Not Found")
  /> http404Error is of type (Int, String), and equals (\(http404Error.0), \"\(http404Error.1)\")
  </ http404Error is of type (Int, String), and equals (404, "Not Found")
  ```
-->

A tupla `(404, "Not Found")` agrupa um `Int` e uma `String`
para dar ao código de status HTTP dois valores separados:
um número e uma descrição legível por humanos.
Ela pode ser descrita como “uma tupla do tipo `(Int, String)`”.

Você pode criar tuplas com qualquer combinação de tipos,
e elas podem conter quantos tipos diferentes você quiser.
Nada impede você de ter uma tupla do tipo `(Int, Int, Int)`, ou `(String, Bool)`,
ou qualquer outra combinação que você precise.

Você pode *decompor* o conteúdo de uma tupla em constantes ou variáveis separadas,
que então acessa normalmente:

```swift
let (statusCode, statusMessage) = http404Error
print("The status code is \(statusCode)")
// Prints "The status code is 404".
print("The status message is \(statusMessage)")
// Prints "The status message is Not Found".
```

<!--
  - test: `tuples`

  ```swifttest
  -> let (statusCode, statusMessage) = http404Error
  -> print("The status code is \(statusCode)")
  <- The status code is 404
  -> print("The status message is \(statusMessage)")
  <- The status message is Not Found
  ```
-->

Se você só precisar de alguns dos valores da tupla,
ignore partes dela com um sublinhado (`_`)
ao decompor a tupla:

```swift
let (justTheStatusCode, _) = http404Error
print("The status code is \(justTheStatusCode)")
// Prints "The status code is 404".
```

<!--
  - test: `tuples`

  ```swifttest
  -> let (justTheStatusCode, _) = http404Error
  -> print("The status code is \(justTheStatusCode)")
  <- The status code is 404
  ```
-->

Como alternativa,
acesse os valores individuais dos elementos de uma tupla
usando números de índice começando em zero:

```swift
print("The status code is \(http404Error.0)")
// Prints "The status code is 404".
print("The status message is \(http404Error.1)")
// Prints "The status message is Not Found".
```

<!--
  - test: `tuples`

  ```swifttest
  -> print("The status code is \(http404Error.0)")
  <- The status code is 404
  -> print("The status message is \(http404Error.1)")
  <- The status message is Not Found
  ```
-->

Você pode nomear os elementos individuais de uma tupla quando ela é definida:

```swift
let http200Status = (statusCode: 200, description: "OK")
```

<!--
  - test: `tuples`

  ```swifttest
  -> let http200Status = (statusCode: 200, description: "OK")
  ```
-->

Se você nomear os elementos de uma tupla,
pode usar os nomes deles para acessar os valores desses elementos:

```swift
print("The status code is \(http200Status.statusCode)")
// Prints "The status code is 200".
print("The status message is \(http200Status.description)")
// Prints "The status message is OK".
```

<!--
  - test: `tuples`

  ```swifttest
  -> print("The status code is \(http200Status.statusCode)")
  <- The status code is 200
  -> print("The status message is \(http200Status.description)")
  <- The status message is OK
  ```
-->

Tuplas são especialmente úteis como valores de retorno de funções.
Uma função que tenta buscar uma página web pode retornar o tipo de tupla `(Int, String)`
para descrever o sucesso ou a falha da busca.
Ao retornar uma tupla com dois valores distintos,
cada um de um tipo diferente,
a função fornece informações mais úteis sobre o resultado
do que se pudesse retornar apenas um valor de um único tipo.
Para mais informações, veja <doc:Functions#Functions-with-Multiple-Return-Values>.

> Nota: Tuplas são úteis para grupos simples de valores relacionados.
> Elas não são adequadas para criar estruturas de dados complexas.
> Se a sua estrutura de dados tende a ser mais complexa, modele-a como uma classe ou struct,
> e não como uma tupla.
> Para mais informações, veja <doc:ClassesAndStructures>.

## Optionals

Você usa *optionals* em situações em que um valor pode estar ausente.
Um optional representa duas possibilidades:
ou existe *um* valor de um tipo especificado,
e você pode fazer o unwrap do optional para acessar esse valor,
ou simplesmente *não* existe valor algum.

Como exemplo de valor que pode estar ausente,
o tipo `Int` do Swift tem um inicializador
que tenta converter um valor `String` em um valor `Int`.
No entanto, só algumas strings podem ser convertidas em inteiros.
A string `"123"` pode ser convertida no valor numérico `123`,
mas a string `"hello, world"` não tem um valor numérico correspondente.
O exemplo abaixo usa o inicializador para tentar converter uma `String` em um `Int`:

```swift
let possibleNumber = "123"
let convertedNumber = Int(possibleNumber)
// The type of convertedNumber is "optional Int"
```

<!--
  - test: `optionals`

  ```swifttest
  -> let possibleNumber = "123"
  -> let convertedNumber = Int(possibleNumber)
  // convertedNumber is inferred to be of type "Int?", or "optional Int"
  >> print(type(of: convertedNumber))
  << Optional<Int>
  ```
-->

Como o inicializador do código acima pode falhar,
ele retorna um `Int` *optional*, e não um `Int`.

Para escrever um tipo optional,
você escreve um ponto de interrogação (`?`)
depois do nome do tipo que o optional contém.
Por exemplo, o tipo de um `Int` optional é `Int?`.
Um `Int` optional sempre contém
algum valor `Int` ou nenhum valor.
Ele não pode conter outra coisa, como um valor `Bool` ou `String`.

### nil

Você coloca uma variável optional em um estado sem valor
atribuindo a ela o valor especial `nil`:

```swift
var serverResponseCode: Int? = 404
// serverResponseCode contains an actual Int value of 404
serverResponseCode = nil
// serverResponseCode now contains no value
```

<!--
  - test: `optionals`

  ```swifttest
  -> var serverResponseCode: Int? = 404
  /> serverResponseCode contains an actual Int value of \(serverResponseCode!)
  </ serverResponseCode contains an actual Int value of 404
  -> serverResponseCode = nil
  // serverResponseCode now contains no value
  ```
-->

Se você definir uma variável optional sem fornecer um valor padrão,
a variável é automaticamente definida como `nil`:

```swift
var surveyAnswer: String?
// surveyAnswer is automatically set to nil
```

<!--
  - test: `optionals`

  ```swifttest
  -> var surveyAnswer: String?
  // surveyAnswer is automatically set to nil
  ```
-->

Você pode usar uma instrução `if` para descobrir se um optional contém um valor,
comparando o optional com `nil`.
Essa comparação é feita com o operador “igual a” (`==`)
ou com o operador “diferente de” (`!=`).

Se um optional tiver um valor, ele é considerado “diferente de” `nil`:

```swift
let possibleNumber = "123"
let convertedNumber = Int(possibleNumber)

if convertedNumber != nil {
    print("convertedNumber contains some integer value.")
}
// Prints "convertedNumber contains some integer value."
```

<!--
  - test: `optionals`

  ```swifttest
  -> if convertedNumber != nil {
        print("convertedNumber contains some integer value.")
     }
  <- convertedNumber contains some integer value.
  ```
-->

Você não pode usar `nil` com constantes ou variáveis que não são optional.
Se uma constante ou variável do seu código precisar lidar com a ausência de valor
em certas condições, declare-a como um valor optional do tipo apropriado.
Uma constante ou variável declarada como não optional tem a garantia de nunca conter `nil`.
Se você tentar atribuir `nil` a um valor não optional, receberá um erro de compilação.

Essa separação entre valores optional e não optional permite marcar explicitamente
quais informações podem estar ausentes, e facilita escrever código que trate valores ausentes.
Você não consegue tratar um optional por engano como se fosse não optional,
porque o compilador reporta esse erro.
Depois que você faz o unwrap do valor, nenhum outro código que trabalha com esse valor
precisa verificar `nil`, então não há necessidade de verificar repetidamente
o mesmo valor em diferentes partes do código.

Ao acessar um valor optional, seu código sempre trata os dois casos, o de `nil` e o de não `nil`.
Há várias coisas que você pode fazer quando um valor está ausente,
como descrito nas seções a seguir:

- Pular o código que opera sobre o valor quando ele for `nil`.

- Propagar o valor `nil`,
  retornando `nil`
  ou usando o operador `?.` descrito em <doc:OptionalChaining>.

- Fornecer um valor alternativo, usando o operador `??`.

- Interromper a execução do programa, usando o operador `!`.

> Nota:
> No Objective-C, `nil` é um ponteiro para um objeto inexistente.
> No Swift, `nil` não é um ponteiro: é a ausência de um valor de determinado tipo.
> Optionals de *qualquer* tipo podem ser definidos como `nil`, não apenas tipos de objeto.

### Optional binding

Você usa optional binding para descobrir se um optional contém um valor
e, se contiver, para disponibilizar esse valor como uma constante ou variável temporária.
O optional binding pode ser usado com as instruções `if`, `guard` e `while`
para verificar se há um valor dentro de um optional
e extrair esse valor para uma constante ou variável, em uma única ação.
Para mais informações sobre as instruções `if`, `guard` e `while`,
veja <doc:ControlFlow>.

Escreva um optional binding para uma instrução `if` assim:

```swift
if let <#constantName#> = <#someOptional#> {
   <#statements#>
}
```

Você pode reescrever o exemplo de `possibleNumber` da seção <doc:TheBasics#Optionals>
para usar optional binding em vez de force unwrapping:

```swift
if let actualNumber = Int(possibleNumber) {
    print("The string \"\(possibleNumber)\" has an integer value of \(actualNumber)")
} else {
    print("The string \"\(possibleNumber)\" couldn't be converted to an integer")
}
// Prints "The string "123" has an integer value of 123".
```

<!--
  - test: `optionals`

  ```swifttest
  -> if let actualNumber = Int(possibleNumber) {
        print("The string \"\(possibleNumber)\" has an integer value of \(actualNumber)")
     } else {
        print("The string \"\(possibleNumber)\" couldn't be converted to an integer")
     }
  <- The string "123" has an integer value of 123
  ```
-->

Esse código pode ser lido assim:

“Se o `Int` optional retornado por `Int(possibleNumber)` contiver um valor,
defina uma nova constante chamada `actualNumber` com o valor contido no optional.”

Se a conversão for bem-sucedida,
a constante `actualNumber` fica disponível para uso dentro do primeiro ramo da instrução `if`.
Ela já foi inicializada com o valor contido no optional
e tem o tipo não optional correspondente.
Nesse caso, o tipo de `Int(possibleNumber)` é `Int?`,
então o tipo de `actualNumber` é `Int`.

Se você não precisar se referir à constante ou variável optional original
depois de acessar o valor que ela contém,
pode usar o mesmo nome para a nova constante ou variável:

```swift
let myNumber = Int(possibleNumber)
// Here, myNumber is an optional integer
if let myNumber = myNumber {
    // Here, myNumber is a non-optional integer
    print("My number is \(myNumber)")
}
// Prints "My number is 123".
```

<!--
  - test: `optionals`

  ```swifttest
  -> let myNumber = Int(possibleNumber)
  // Here, myNumber is an optional integer
  -> if let myNumber = myNumber {
         // Here, myNumber is a non-optional integer
         print("My number is \(myNumber)")
     }
  <- My number is 123
  ```
-->

Este código começa verificando se `myNumber` contém um valor,
assim como o código do exemplo anterior.
Se `myNumber` tiver um valor,
o valor de uma nova constante chamada `myNumber` é definido com esse valor.
Dentro do corpo da instrução `if`, escrever `myNumber` se refere a essa nova constante não optional.
Escrever `myNumber` antes ou depois da instrução `if`
se refere à constante original de inteiro optional.

Como esse tipo de código é muito comum,
você pode usar uma forma mais curta para fazer o unwrap de um valor optional:
escreva apenas o nome da constante ou variável que passa por unwrap.
A nova constante ou variável, já sem o optional,
usa implicitamente o mesmo nome do valor optional.

```swift
if let myNumber {
    print("My number is \(myNumber)")
}
// Prints "My number is 123".
```

<!--
  - test: `optionals`

  ```swifttest
  -> if let myNumber {
         print("My number is \(myNumber)")
     }
  <- My number is 123
  ```
-->

Você pode usar constantes e variáveis com optional binding.
Se quiser manipular o valor de `myNumber`
dentro do primeiro ramo da instrução `if`,
pode escrever `if var myNumber`,
e o valor contido no optional ficará disponível como variável, e não como constante.
As alterações que você fizer em `myNumber` dentro do corpo da instrução `if`
se aplicam apenas a essa variável local,
*não* à constante ou variável optional original que você fez o unwrap.

Você pode incluir quantos optional bindings e condições booleanas forem necessários
em uma única instrução `if`, separados por vírgulas.
Se algum dos valores dos optional bindings for `nil`
ou se alguma condição booleana for avaliada como `false`,
a condição inteira da instrução `if` é considerada `false`.
As instruções `if` a seguir são equivalentes:

```swift
if let firstNumber = Int("4"), let secondNumber = Int("42"), firstNumber < secondNumber && secondNumber < 100 {
    print("\(firstNumber) < \(secondNumber) < 100")
}
// Prints "4 < 42 < 100".

if let firstNumber = Int("4") {
    if let secondNumber = Int("42") {
        if firstNumber < secondNumber && secondNumber < 100 {
            print("\(firstNumber) < \(secondNumber) < 100")
        }
    }
}
// Prints "4 < 42 < 100".
```

<!--
  - test: `multipleOptionalBindings`

  ```swifttest
  -> if let firstNumber = Int("4"), let secondNumber = Int("42"), firstNumber < secondNumber && secondNumber < 100 {
        print("\(firstNumber) < \(secondNumber) < 100")
     }
  <- 4 < 42 < 100

  -> if let firstNumber = Int("4") {
         if let secondNumber = Int("42") {
             if firstNumber < secondNumber && secondNumber < 100 {
                 print("\(firstNumber) < \(secondNumber) < 100")
             }
         }
     }
  <- 4 < 42 < 100
  ```
-->

<!--
  The example above uses multiple optional bindings
  to show that you can have more than one
  and to show the short-circuiting behavior.
  It has multiple Boolean conditions
  to show that you should join logically related conditions
  using the && operator instead of a comma.
-->

Constantes e variáveis criadas com optional binding em uma instrução `if`
ficam disponíveis apenas dentro do corpo dessa instrução.
Em contraste, as constantes e variáveis criadas com uma instrução `guard`
ficam disponíveis nas linhas de código que seguem a instrução `guard`,
como descrito em <doc:ControlFlow#Early-Exit>.

### Fornecendo um valor alternativo

Outra forma de lidar com um valor ausente é fornecer um valor padrão
usando o operador de coalescência nula (`??`).
Se o optional à esquerda do `??` não for `nil`,
esse valor passa pelo unwrap e é usado.
Caso contrário, é usado o valor à direita do `??`.
Por exemplo, o código abaixo cumprimenta alguém pelo nome, se um nome for informado,
e usa uma saudação genérica quando o nome for `nil`.

```swift
let name: String? = nil
let greeting = "Hello, " + (name ?? "friend") + "!"
print(greeting)
// Prints "Hello, friend!"
```

<!--
.. testcode:: optionalFallback

   ```swifttest
   -> let name: String? = nil
   -> let greeting = "Hello, " + (name ?? "friend") + "!"
   -> print(greeting)
   <- Hello, friend!
   ```
-->

Para mais informações sobre usar `??` para fornecer um valor alternativo,
veja <doc:BasicOperators#Nil-Coalescing-Operator>.

### Force unwrapping

Quando `nil` representa uma falha irrecuperável,
como um erro de programação ou um estado corrompido,
você pode acessar o valor subjacente do optional
adicionando um ponto de exclamação (`!`) ao final do nome do optional.
Isso é conhecido como *force unwrapping* do valor do optional.
Quando você faz force unwrapping de um valor que não é `nil`,
o resultado é o valor já sem o optional.
Fazer force unwrapping de um valor `nil` dispara um erro em tempo de execução.

Na prática, o `!` é uma forma mais curta de escrever [`fatalError(_:file:line:)`][].
Por exemplo, o código abaixo mostra duas abordagens equivalentes:

[`fatalError(_:file:line:)`]: https://developer.apple.com/documentation/swift/fatalerror(_:file:line:)

```swift
let possibleNumber = "123"
let convertedNumber = Int(possibleNumber)

let number = convertedNumber!

guard let number = convertedNumber else {
    fatalError("The number was invalid")
}
```

As duas versões do código acima dependem de `convertedNumber`
sempre conter um valor.
Escrever essa exigência como parte do código, usando qualquer uma das abordagens acima,
permite que o código verifique em tempo de execução que a exigência é verdadeira.

Para mais informações sobre como impor requisitos de dados
e verificar premissas em tempo de execução,
veja <doc:TheBasics#Assertions-and-Preconditions>.

### Optionals com unwrap implícito

Como descrito acima,
optionals indicam que uma constante ou variável pode ter “nenhum valor”.
Optionals podem ser verificados com uma instrução `if` para ver se um valor existe,
e podem passar por unwrap condicional com optional binding
para acessar o valor do optional, se ele existir.

Às vezes, a estrutura do programa deixa claro que um optional *sempre* terá um valor,
depois que esse valor for definido pela primeira vez.
Nesses casos, é útil eliminar a necessidade de verificar e fazer o unwrap
do valor do optional toda vez que ele for acessado,
porque é seguro presumir que ele terá um valor o tempo todo.

Esses optionals são definidos como *optionals com unwrap implícito*.
Você escreve um optional com unwrap implícito colocando um ponto de exclamação (`String!`)
em vez de um ponto de interrogação (`String?`) depois do tipo que você quer tornar optional.
Em vez de colocar um ponto de exclamação depois do nome do optional ao usá-lo,
você coloca um ponto de exclamação depois do tipo do optional ao declará-lo.

Optionals com unwrap implícito são úteis quando
a existência do valor de um optional é confirmada logo depois que ele é definido pela primeira vez
e pode ser considerada certa em todos os momentos seguintes.
O principal uso de optionals com unwrap implícito no Swift
é durante a inicialização de classes,
como descrito em <doc:AutomaticReferenceCounting#Unowned-References-and-Implicitly-Unwrapped-Optional-Properties>.

Não use um optional com unwrap implícito quando houver a possibilidade de
a variável virar `nil` mais tarde.
Sempre use um tipo optional normal se você precisar verificar um valor `nil`
durante a vida de uma variável.

Nos bastidores, um optional com unwrap implícito é um optional normal,
mas também pode ser usado como um valor não optional,
sem a necessidade de fazer o unwrap do valor toda vez que ele é acessado.
O exemplo a seguir mostra a diferença de comportamento entre uma string optional
e uma string optional com unwrap implícito ao acessar o valor contido no optional como uma `String` explícita:

```swift
let possibleString: String? = "An optional string."
let forcedString: String = possibleString! // Requires explicit unwrapping

let assumedString: String! = "An implicitly unwrapped optional string."
let implicitString: String = assumedString // Unwrapped automatically
```

<!--
  - test: `implicitlyUnwrappedOptionals`

  ```swifttest
  -> let possibleString: String? = "An optional string."
  -> let forcedString: String = possibleString! // requires an exclamation point

  -> let assumedString: String! = "An implicitly unwrapped optional string."
  -> let implicitString: String = assumedString // no need for an exclamation point
  ```
-->

Você pode pensar em um optional com unwrap implícito como uma permissão
para que o optional passe por force unwrapping quando necessário.
Ao usar um valor optional com unwrap implícito, o Swift primeiro tenta usá-lo
como um valor optional comum;
se ele não puder ser usado como optional, o Swift faz force unwrapping do valor.
No código acima,
o valor optional `assumedString` passa por force unwrapping
antes de ter seu valor atribuído a `implicitString`,
porque `implicitString` tem o tipo explícito não optional `String`.
No código abaixo,
`optionalString` não tem tipo explícito,
então é um optional comum.

```swift
let optionalString = assumedString
// The type of optionalString is "String?" and assumedString isn't force-unwrapped.
```

<!--
  - test: `implicitlyUnwrappedOptionals`

  ```swifttest
  -> let optionalString = assumedString
  // The type of optionalString is "String?" and assumedString isn't force-unwrapped.
  >> print(type(of: optionalString))
  << Optional<String>
  ```
-->

Se um optional com unwrap implícito for `nil` e você tentar acessar o valor contido no optional,
você disparará um erro em tempo de execução.
O resultado é exatamente o mesmo de escrever um ponto de exclamação
para fazer force unwrapping de um optional normal que não contém valor.

Você pode verificar se um optional com unwrap implícito é `nil`
da mesma forma que verifica um optional normal:

```swift
if assumedString != nil {
    print(assumedString!)
}
// Prints "An implicitly unwrapped optional string."
```

<!--
  - test: `implicitlyUnwrappedOptionals`

  ```swifttest
  -> if assumedString != nil {
        print(assumedString!)
     }
  <- An implicitly unwrapped optional string.
  ```
-->

Você também pode usar um optional com unwrap implícito com optional binding,
para verificar e fazer o unwrap do valor em uma única instrução:

```swift
if let definiteString = assumedString {
    print(definiteString)
}
// Prints "An implicitly unwrapped optional string."
```

<!--
  - test: `implicitlyUnwrappedOptionals`

  ```swifttest
  -> if let definiteString = assumedString {
        print(definiteString)
     }
  <- An implicitly unwrapped optional string.
  ```
-->

## Segurança de memória

Além das verificações que impedem incompatibilidades de tipo,
descritas acima em <doc:TheBasics#Type-Safety-and-Type-Inference>,
o Swift também protege o código contra o trabalho com memória inválida.
Essa proteção é conhecida como *segurança de memória*
e inclui os seguintes requisitos:

- Valores são definidos antes de serem lidos.
  A proteção contra a interação com regiões de memória não inicializadas
  também é conhecida como *inicialização definitiva*.
- Arrays e buffers são acessados apenas em índices válidos.
  A proteção contra acesso fora dos limites
  também é conhecida como *segurança de limites*.
- A memória é acessada apenas durante o tempo de vida do valor.
  A proteção contra erros de uso após liberação
  também é conhecida como *segurança de tempo de vida*.
- O acesso à memória se sobrepõe apenas de formas comprovadamente seguras.
  A proteção contra corridas de dados (data races) em código concorrente
  também é conhecida como *segurança de threads*.

Se você já trabalhou com linguagens que não oferecem essas garantias,
pode conhecer alguns dos erros e bugs citados na lista acima.
Se você nunca encontrou esses problemas, tudo bem:
código seguro em Swift evita esses problemas.
Para saber como o Swift garante que você defina valores iniciais, veja <doc:Initialization>;
para saber como o Swift verifica a segurança de memória em código concorrente, veja <doc:Concurrency>;
e para saber como o Swift verifica acessos sobrepostos à memória, veja <doc:MemorySafety>.

Às vezes você precisa trabalhar fora dos limites de segurança,
por exemplo, por causa de limitações da linguagem ou da biblioteca padrão,
então o Swift também oferece versões inseguras de algumas APIs.
Quando você usa tipos ou métodos cujo nome inclui palavras como
"unsafe", "unchecked" ou "unmanaged",
você assume a responsabilidade pela segurança.

Código seguro em Swift ainda pode encontrar erros e falhas inesperadas,
que podem interromper a execução do programa.
Segurança não garante que seu código seja executado até o fim.
O Swift oferece várias formas de indicar e se recuperar de erros,
discutidas em <doc:TheBasics#Error-Handling> e <doc:TheBasics#Assertions-and-Preconditions>, mais abaixo.
No entanto, em alguns casos, a *única* forma segura de tratar um erro é interromper a execução.
Se você precisar garantir que um serviço nunca pare inesperadamente,
incorpore tolerância a falhas na arquitetura geral dele,
para que ele consiga se recuperar caso algum de seus componentes pare inesperadamente.

## Tratamento de erros

Você usa *tratamento de erros* para responder a condições de erro
que o programa pode encontrar durante a execução.

Em contraste com os optionals,
que podem usar a presença ou a ausência de um valor
para comunicar sucesso ou falha de uma função,
o tratamento de erros permite descobrir a causa subjacente da falha
e, se necessário, propagar o erro para outra parte do programa.

Quando uma função encontra uma condição de erro, ela *lança* (throws) um erro.
Quem chamou essa função pode então *capturar* (catch) o erro e responder de forma apropriada.

```swift
func canThrowAnError() throws {
    // this function may or may not throw an error
}
```

<!--
  - test: `errorHandling`

  ```swifttest
  >> enum SimpleError: Error {
  >>    case someError
  >> }
  >> let condition = true
  -> func canThrowAnError() throws {
        // this function may or may not throw an error
  >>    if condition {
  >>       throw SimpleError.someError
  >>    }
     }
  ```
-->

Uma função indica que pode lançar um erro incluindo a palavra-chave `throws` na sua declaração.
Quando você chama uma função que pode lançar um erro, coloca a palavra-chave `try` antes da expressão.

O Swift propaga automaticamente os erros para fora do escopo atual
até que sejam tratados por uma cláusula `catch`.

```swift
do {
    try canThrowAnError()
    // no error was thrown
} catch {
    // an error was thrown
}
```

<!--
  - test: `errorHandling`

  ```swifttest
  -> do {
  ->    try canThrowAnError()
  >>    print("No Error")
  ->    // no error was thrown
  -> } catch {
  >>    print("Error")
  ->    // an error was thrown
  -> }
  << Error
  ```
-->

Uma instrução `do` cria um novo escopo,
o que permite que os erros sejam propagados para uma ou mais cláusulas `catch`.

Veja um exemplo de como o tratamento de erros pode ser usado
para responder a diferentes condições de erro:

```swift
func makeASandwich() throws {
    // ...
}

do {
    try makeASandwich()
    eatASandwich()
} catch SandwichError.outOfCleanDishes {
    washDishes()
} catch SandwichError.missingIngredients(let ingredients) {
    buyGroceries(ingredients)
}
```

<!--
  - test: `errorHandlingTwo`

  ```swifttest
  >> enum SandwichError: Error {
  >>     case outOfCleanDishes
  >>     case missingIngredients([String])
  >> }
  >> func washDishes() { print("Wash dishes") }
  >> func buyGroceries(_ shoppingList: [String]) { print("Buy \(shoppingList)") }
  -> func makeASandwich() throws {
         // ...
     }
  >> func eatASandwich() {}

  -> do {
         try makeASandwich()
         eatASandwich()
     } catch SandwichError.outOfCleanDishes {
         washDishes()
     } catch SandwichError.missingIngredients(let ingredients) {
         buyGroceries(ingredients)
     }
  ```
-->

Neste exemplo, a função `makeASandwich()` lança um erro
se não houver pratos limpos disponíveis ou se algum ingrediente estiver faltando.
Como `makeASandwich()` pode lançar um erro, a chamada da função fica envolvida em uma expressão `try`.
Ao envolver a chamada da função em uma instrução `do`,
quaisquer erros lançados serão propagados para as cláusulas `catch` fornecidas.

Se nenhum erro for lançado, a função `eatASandwich()` é chamada.
Se um erro for lançado e corresponder ao caso `SandwichError.outOfCleanDishes`,
a função `washDishes()` é chamada.
Se um erro for lançado e corresponder ao caso `SandwichError.missingIngredients`,
a função `buyGroceries(_:)` é chamada com o valor associado `[String]`
capturado pelo padrão `catch`.

Lançar, capturar e propagar erros é tratado com mais detalhes em
<doc:ErrorHandling>.

## Asserções e pré-condições

*Asserções* e *pré-condições* são verificações feitas em tempo de execução.
Você as usa para garantir que uma condição essencial seja satisfeita
antes de executar qualquer código adicional.
Se a condição booleana na asserção ou na pré-condição for avaliada como `true`,
a execução do código continua normalmente.
Se a condição for avaliada como `false`,
o estado atual do programa é inválido;
a execução do código termina e seu app é encerrado.

Você usa asserções e pré-condições para expressar as premissas que assume
e as expectativas que tem enquanto programa,
para que possa incluí-las como parte do código.
Asserções ajudam a encontrar erros e premissas incorretas durante o desenvolvimento,
e pré-condições ajudam a detectar problemas em produção.

Além de verificar suas expectativas em tempo de execução,
asserções e pré-condições também se tornam uma forma útil de documentação dentro do código.
Diferentemente das condições de erro discutidas acima em <doc:TheBasics#Error-Handling>,
asserções e pré-condições não são usadas para erros recuperáveis ou esperados.
Como uma asserção ou pré-condição que falha indica um estado inválido do programa,
não há como capturar uma asserção que falhou.
Recuperar-se de um estado inválido é impossível.
Quando uma asserção falha, pelo menos uma parte dos dados do programa é inválida,
mas você não sabe por que ela é inválida
nem se algum outro estado também é inválido.

Usar asserções e pré-condições não substitui projetar o código
de modo que condições inválidas sejam pouco prováveis.
No entanto, usá-las para impor dados e estado válidos faz seu app ser encerrado
de forma mais previsível quando ocorre um estado inválido,
e ajuda a tornar o problema mais fácil de depurar.
Quando as premissas não são verificadas,
você pode só notar esse tipo de problema muito mais tarde,
quando o código em outro lugar começa a falhar de forma visível,
e depois que os dados do usuário já foram corrompidos silenciosamente.
Interromper a execução assim que um estado inválido é detectado
também ajuda a limitar o estrago causado por esse estado.

A diferença entre asserções e pré-condições está em quando elas são verificadas:
asserções são verificadas apenas em builds de depuração,
mas pré-condições são verificadas tanto em builds de depuração quanto em builds de produção.
Em builds de produção, a condição dentro de uma asserção não é avaliada.
Isso significa que você pode usar quantas asserções quiser
durante o desenvolvimento, sem afetar o desempenho em produção.

### Depurando com asserções

<!--
  If your code triggers an assertion while running in a debug environment,
  such as when you build and run an app in Xcode,
  you can see exactly where the invalid state occurred
  and query the state of your app at the time that the assertion was triggered.
  An assertion also lets you provide a suitable debug message as to the nature of the assert.
-->

Você escreve uma asserção chamando a função
[`assert(_:_:file:line:)`](https://developer.apple.com/documentation/swift/assert(_:_:file:line:))
da biblioteca padrão do Swift.
Você passa para essa função uma expressão que é avaliada como `true` ou `false`
e uma mensagem a exibir se o resultado da condição for `false`.
Por exemplo:

```swift
let age = -3
assert(age >= 0, "A person's age can't be less than zero.")
// This assertion fails because -3 isn't >= 0.
```

<!--
  - test: `assertions-1`

  ```swifttest
  -> let age = -3
  -> assert(age >= 0, "A person's age can't be less than zero.")
  xx assert
  // This assertion fails because -3 isn't >= 0.
  ```
-->

Neste exemplo, a execução do código continua se `age >= 0` for avaliado como `true`,
ou seja, se o valor de `age` não for negativo.
Se o valor de `age` for negativo, como no código acima,
então `age >= 0` é avaliado como `false`,
a asserção falha e o app é encerrado.

Você pode omitir a mensagem da asserção,
por exemplo, quando ela apenas repetiria a condição em forma de texto.

```swift
assert(age >= 0)
```

<!--
  - test: `assertions-2`

  ```swifttest
  >> let age = -3
  -> assert(age >= 0)
  xx assert
  ```
-->

<!--
  - test: `assertionsCanUseStringInterpolation`

  ```swifttest
  -> let age = -3
  -> assert(age >= 0, "A person's age can't be less than zero, but value is \(age).")
  xx assert
  ```
-->

Se o código já verifica a condição,
use a função [`assertionFailure(_:file:line:)`](https://developer.apple.com/documentation/swift/assertionfailure(_:file:line:))
para indicar que uma asserção falhou.
Por exemplo:

```swift
if age > 10 {
    print("You can ride the roller-coaster or the ferris wheel.")
} else if age >= 0 {
    print("You can ride the ferris wheel.")
} else {
    assertionFailure("A person's age can't be less than zero.")
}
```

<!--
  - test: `assertions-3`

  ```swifttest
  >> let age = -3
  -> if age > 10 {
         print("You can ride the roller-coaster or the ferris wheel.")
     } else if age >= 0 {
         print("You can ride the ferris wheel.")
     } else {
         assertionFailure("A person's age can't be less than zero.")
     }
  xx assert
  ```
-->

### Impondo pré-condições

Use uma pré-condição sempre que uma condição puder ser falsa,
mas *precisar* ser verdadeira para que o código continue a execução.
Por exemplo, use uma pré-condição para verificar se um subscript não está fora dos limites,
ou para verificar se uma função recebeu um valor válido.

Você escreve uma pré-condição chamando a função
[`precondition(_:_:file:line:)`](https://developer.apple.com/documentation/swift/precondition(_:_:file:line:)).
Você passa para essa função uma expressão que é avaliada como `true` ou `false`
e uma mensagem a exibir se o resultado da condição for `false`.
Por exemplo:

```swift
// In the implementation of a subscript...
precondition(index > 0, "Index must be greater than zero.")
```

<!--
  - test: `preconditions`

  ```swifttest
  >> let index = -1
  // In the implementation of a subscript...
  -> precondition(index > 0, "Index must be greater than zero.")
  xx assert
  ```
-->

Você também pode chamar a função
[`preconditionFailure(_:file:line:)`](https://developer.apple.com/documentation/swift/preconditionfailure(_:file:line:))
para indicar que ocorreu uma falha,
por exemplo, se o caso padrão de um switch foi executado,
mas todos os dados de entrada válidos deveriam ter sido tratados
por algum dos outros casos do switch.

> Nota: Se você compilar no modo sem verificações (`-Ounchecked`), as pré-condições não são verificadas.
> O compilador presume que as pré-condições são sempre verdadeiras
> e otimiza o seu código de acordo.
> No entanto, a função `fatalError(_:file:line:)` sempre interrompe a execução,
> independentemente das configurações de otimização.
>
> Você pode usar a função `fatalError(_:file:line:)` durante a prototipagem e o desenvolvimento inicial
> para criar stubs de funcionalidades que ainda não foram implementadas,
> escrevendo `fatalError("Unimplemented")` como implementação do stub.
> Como erros fatais nunca são removidos pela otimização, diferentemente das asserções ou pré-condições,
> você pode ter certeza de que a execução sempre é interrompida
> se encontrar uma implementação stub.

<!--
  "\ " in the first cell below lets it be empty.
  Otherwise RST treats the row as a continuation.

  ============ =====  ==========  ===============================
  \            Debug  Production  Production with ``-Ounchecked``
  ============ =====  ==========  ===============================
  Assertion    Yes    No          No
  ------------ -----  ----------  -------------------------------
  Precondition Yes    Yes         No
  ------------ -----  ----------  -------------------------------
  Fatal Error  Yes    Yes         Yes
  ============ =====  ==========  ===============================
-->

<!--
  TODO: In Xcode, can you set a breakpoint on assertion/precondition failure?
  If so, mention that fact and give a link to a guide that shows you how.
  In LLDB, 'breakpoint set -E swift' catches when errors are thrown,
  but doesn't stop at assertions.
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
