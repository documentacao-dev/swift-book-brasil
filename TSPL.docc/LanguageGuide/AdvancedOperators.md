# Operadores avançados

Defina operadores personalizados, execute operações bit a bit e use a sintaxe de result builders.

Além dos operadores descritos em <doc:BasicOperators>,
a Swift oferece vários operadores avançados que realizam manipulações de valores mais complexas.
Entre eles estão todos os operadores bit a bit e de deslocamento de bits que você já conhece
do C e do Objective-C.

Diferentemente dos operadores aritméticos do C,
os operadores aritméticos da Swift não fazem overflow por padrão.
O comportamento de overflow é interceptado e reportado como erro.
Para optar pelo comportamento de overflow,
use o segundo conjunto de operadores aritméticos da Swift, que fazem overflow por padrão,
como o operador de adição com overflow (`&+`).
Todos esses operadores de overflow começam com um e comercial (`&`).

Ao definir suas próprias structs, classes e enums,
pode ser útil fornecer suas próprias implementações
dos operadores padrão da Swift para esses tipos personalizados.
A Swift facilita fornecer implementações sob medida desses operadores
e definir exatamente qual deve ser o comportamento de cada um para cada tipo que você criar.

Você não está limitado aos operadores predefinidos.
A Swift permite definir seus próprios operadores infixos, prefixos, pós-fixos e de atribuição,
com valores personalizados de precedência e associatividade.
Esses operadores podem ser usados e adotados no código como qualquer um dos operadores predefinidos,
e você pode até estender tipos existentes para que eles aceitem os operadores personalizados que você definir.

## Operadores bit a bit

*Operadores bit a bit* permitem manipular
os bits individuais dos dados brutos dentro de uma estrutura de dados.
Eles costumam ser usados em programação de baixo nível,
como programação gráfica e criação de drivers de dispositivo.
Operadores bit a bit também podem ser úteis ao trabalhar com dados brutos de fontes externas,
como na codificação e decodificação de dados para comunicação por um protocolo personalizado.

A Swift oferece todos os operadores bit a bit encontrados em C, descritos a seguir.

### Operador NOT bit a bit

O *operador NOT bit a bit* (`~`) inverte todos os bits de um número:

![](bitwiseNOT)

O operador NOT bit a bit é um operador prefixo
e aparece imediatamente antes do valor sobre o qual opera,
sem espaço em branco:

```swift
let initialBits: UInt8 = 0b00001111
let invertedBits = ~initialBits  // equals 11110000
```

<!--
  - test: `bitwiseOperators`

  ```swifttest
  -> let initialBits: UInt8 = 0b00001111
  >> assert(initialBits == 15)
  -> let invertedBits = ~initialBits  // equals 11110000
  >> assert(invertedBits == 240)
  ```
-->

Inteiros `UInt8` têm oito bits
e podem armazenar qualquer valor entre `0` e `255`.
Este exemplo inicializa um inteiro `UInt8` com o valor binário `00001111`,
cujos quatro primeiros bits estão em `0`,
e cujos quatro últimos bits estão em `1`.
Isso equivale ao valor decimal `15`.

<!-- Apple Books screenshot begins here. -->

O operador NOT bit a bit é então usado para criar uma nova constante chamada `invertedBits`,
que é igual a `initialBits`,
mas com todos os bits invertidos.
Zeros viram uns, e uns viram zeros.
O valor de `invertedBits` é `11110000`,
que equivale ao decimal sem sinal `240`.

### Operador AND bit a bit

O *operador AND bit a bit* (`&`) combina os bits de dois números.
Ele retorna um novo número cujos bits são definidos como `1`
somente se os bits correspondentes valerem `1` em *ambos* os números de entrada:

![](bitwiseAND)

No exemplo abaixo,
os valores de `firstSixBits` e `lastSixBits`
têm, ambos, os quatro bits do meio iguais a `1`.
O operador AND bit a bit os combina e produz o número `00111100`,
que equivale ao decimal sem sinal `60`:

```swift
let firstSixBits: UInt8 = 0b11111100
let lastSixBits: UInt8  = 0b00111111
let middleFourBits = firstSixBits & lastSixBits  // equals 00111100
```

<!--
  - test: `bitwiseOperators`

  ```swifttest
  -> let firstSixBits: UInt8 = 0b11111100
  -> let lastSixBits: UInt8  = 0b00111111
  -> let middleFourBits = firstSixBits & lastSixBits  // equals 00111100
  >> assert(middleFourBits == 0b00111100)
  ```
-->

### Operador OR bit a bit

O *operador OR bit a bit* (`|`) compara os bits de dois números.
O operador retorna um novo número cujos bits são definidos como `1`
se os bits valerem `1` em *um ou outro* dos números de entrada:

![](bitwiseOR)

<!-- Apple Books screenshot ends here. -->

No exemplo abaixo,
os valores de `someBits` e `moreBits` têm bits diferentes definidos como `1`.
O operador OR bit a bit os combina e produz o número `11111110`,
que equivale ao decimal sem sinal `254`:

```swift
let someBits: UInt8 = 0b10110010
let moreBits: UInt8 = 0b01011110
let combinedbits = someBits | moreBits  // equals 11111110
```

<!--
  - test: `bitwiseOperators`

  ```swifttest
  -> let someBits: UInt8 = 0b10110010
  -> let moreBits: UInt8 = 0b01011110
  -> let combinedbits = someBits | moreBits  // equals 11111110
  >> assert(combinedbits == 0b11111110)
  ```
-->

### Operador XOR bit a bit

O *operador XOR bit a bit*, ou “operador OU exclusivo” (`^`),
compara os bits de dois números.
O operador retorna um novo número cujos bits são definidos como `1`
onde os bits de entrada são diferentes,
e como `0` onde os bits de entrada são iguais:

![](bitwiseXOR)

No exemplo abaixo,
os valores de `firstBits` e `otherBits` têm, cada um, um bit definido como `1`
em uma posição em que o outro não tem.
O operador XOR bit a bit define esses dois bits como `1` no valor de saída.
Todos os outros bits de `firstBits` e `otherBits` coincidem
e são definidos como `0` no valor de saída:

```swift
let firstBits: UInt8 = 0b00010100
let otherBits: UInt8 = 0b00000101
let outputBits = firstBits ^ otherBits  // equals 00010001
```

<!--
  - test: `bitwiseOperators`

  ```swifttest
  -> let firstBits: UInt8 = 0b00010100
  -> let otherBits: UInt8 = 0b00000101
  -> let outputBits = firstBits ^ otherBits  // equals 00010001
  >> assert(outputBits == 0b00010001)
  ```
-->

### Operadores de deslocamento à esquerda e à direita bit a bit

O *operador de deslocamento à esquerda bit a bit* (`<<`)
e o *operador de deslocamento à direita bit a bit* (`>>`)
movem todos os bits de um número para a esquerda ou para a direita por um certo número de posições,
de acordo com as regras definidas abaixo.

Deslocamentos bit a bit para a esquerda e para a direita têm o efeito de
multiplicar ou dividir um inteiro por um fator de dois.
Deslocar os bits de um inteiro uma posição para a esquerda dobra seu valor,
enquanto deslocá-lo uma posição para a direita reduz seu valor à metade.

<!--
  TODO: mention the caveats to this claim.
-->

#### Comportamento de deslocamento para inteiros sem sinal

O comportamento de deslocamento de bits para inteiros sem sinal é o seguinte:

1. Os bits existentes são movidos para a esquerda ou para a direita pelo número de posições solicitado.
2. Os bits que são movidos para além dos limites do armazenamento do inteiro são descartados.
3. Zeros são inseridos nos espaços deixados para trás
   depois que os bits originais são movidos para a esquerda ou para a direita.

Essa abordagem é conhecida como *deslocamento lógico*.

A ilustração abaixo mostra os resultados de `11111111 << 1`
(que é `11111111` deslocado uma posição para a esquerda),
e `11111111 >> 1`
(que é `11111111` deslocado uma posição para a direita).
Os números verdes são deslocados,
os cinza são descartados,
e os zeros rosa são inseridos:

![](bitshiftUnsigned)

Veja como o deslocamento de bits fica em código Swift:

```swift
let shiftBits: UInt8 = 4   // 00000100 in binary
shiftBits << 1             // 00001000
shiftBits << 2             // 00010000
shiftBits << 5             // 10000000
shiftBits << 6             // 00000000
shiftBits >> 2             // 00000001
```

<!--
  - test: `bitwiseShiftOperators`

  ```swifttest
  -> let shiftBits: UInt8 = 4   // 00000100 in binary
  >> let r0 =
  -> shiftBits << 1             // 00001000
  >> assert(r0 == 8)
  >> let r1 =
  -> shiftBits << 2             // 00010000
  >> assert(r1 == 16)
  >> let r2 =
  -> shiftBits << 5             // 10000000
  >> assert(r2 == 128)
  >> let r3 =
  -> shiftBits << 6             // 00000000
  >> assert(r3 == 0)
  >> let r4 =
  -> shiftBits >> 2             // 00000001
  >> assert(r4 == 1)
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

Você pode usar o deslocamento de bits para codificar e decodificar valores dentro de outros tipos de dados:

```swift
let pink: UInt32 = 0xCC6699
let redComponent = (pink & 0xFF0000) >> 16    // redComponent is 0xCC, or 204
let greenComponent = (pink & 0x00FF00) >> 8   // greenComponent is 0x66, or 102
let blueComponent = pink & 0x0000FF           // blueComponent is 0x99, or 153
```

<!--
  - test: `bitwiseShiftOperators`

  ```swifttest
  -> let pink: UInt32 = 0xCC6699
  -> let redComponent = (pink & 0xFF0000) >> 16    // redComponent is 0xCC, or 204
  -> let greenComponent = (pink & 0x00FF00) >> 8   // greenComponent is 0x66, or 102
  -> let blueComponent = pink & 0x0000FF           // blueComponent is 0x99, or 153
  >> assert(redComponent == 204)
  >> assert(greenComponent == 102)
  >> assert(blueComponent == 153)
  ```
-->

Este exemplo usa uma constante `UInt32` chamada `pink` para armazenar
um valor de cor de Cascading Style Sheets para a cor rosa.
O valor de cor CSS `#CC6699` é escrito como
`0xCC6699` na representação hexadecimal de números da Swift.
Essa cor é então decomposta em suas
componentes vermelha (`CC`), verde (`66`) e azul (`99`)
pelo operador AND bit a bit (`&`) e pelo operador de deslocamento à direita bit a bit (`>>`).

A componente vermelha é obtida realizando um AND bit a bit
entre os números `0xCC6699` e `0xFF0000`.
Os zeros em `0xFF0000` funcionam como uma “máscara” sobre o segundo e o terceiro bytes de `0xCC6699`,
fazendo com que `6699` seja ignorado e deixando `0xCC0000` como resultado.

Esse número é então deslocado 16 posições para a direita (`>> 16`).
Cada par de caracteres de um número hexadecimal usa 8 bits,
então um deslocamento de 16 posições para a direita converte `0xCC0000` em `0x0000CC`.
Isso é o mesmo que `0xCC`, que tem valor decimal `204`.

De modo semelhante, a componente verde é obtida realizando um AND bit a bit
entre os números `0xCC6699` e `0x00FF00`,
o que gera o valor de saída `0x006600`.
Esse valor é então deslocado oito posições para a direita,
resultando em `0x66`, que tem valor decimal `102`.

Por fim, a componente azul é obtida realizando um AND bit a bit
entre os números `0xCC6699` e `0x0000FF`,
o que gera o valor de saída `0x000099`.
Como `0x000099` já é igual a `0x99`,
que tem valor decimal `153`,
esse valor é usado sem ser deslocado para a direita,

#### Comportamento de deslocamento para inteiros com sinal

O comportamento de deslocamento é mais complexo para inteiros com sinal do que para inteiros sem sinal,
por causa da forma como inteiros com sinal são representados em binário.
(Os exemplos abaixo são baseados em inteiros com sinal de 8 bits, por simplicidade,
mas os mesmos princípios valem para inteiros com sinal de qualquer tamanho.)

Inteiros com sinal usam o primeiro bit (conhecido como *bit de sinal*)
para indicar se o inteiro é positivo ou negativo.
Um bit de sinal `0` significa positivo, e um bit de sinal `1` significa negativo.

Os demais bits (conhecidos como *bits de valor*) armazenam o valor em si.
Números positivos são armazenados exatamente da mesma forma que inteiros sem sinal,
contando a partir de `0`.
Veja como os bits de um `Int8` ficam para o número `4`:

![](bitshiftSignedFour)

O bit de sinal é `0` (significando “positivo”),
e os sete bits de valor são o próprio número `4`,
escrito em notação binária.

Números negativos, porém, são armazenados de outra forma.
Eles são armazenados subtraindo seu valor absoluto de `2` elevado à potência de `n`,
em que `n` é o número de bits de valor.
Um número de oito bits tem sete bits de valor,
então isso significa `2` elevado à potência de `7`, ou `128`.

Veja como os bits de um `Int8` ficam para o número `-4`:

![](bitshiftSignedMinusFour)

Desta vez, o bit de sinal é `1` (significando “negativo”),
e os sete bits de valor têm valor binário `124` (que é `128 - 4`):

![](bitshiftSignedMinusFourValue)

Essa codificação para números negativos é conhecida como representação em *complemento de dois*.
Ela pode parecer uma forma incomum de representar números negativos,
mas tem várias vantagens.

Primeiro, você pode somar `-1` a `-4`
simplesmente realizando uma soma binária padrão dos oito bits
(incluindo o bit de sinal),
descartando o que não couber nos oito bits ao final:

![](bitshiftSignedAddition)

Segundo, a representação em complemento de dois também permite
deslocar os bits de números negativos para a esquerda e para a direita, como nos positivos,
e ainda assim dobrar o valor a cada deslocamento para a esquerda,
ou reduzi-lo à metade a cada deslocamento para a direita.
Para isso, uma regra extra é aplicada quando inteiros com sinal são deslocados para a direita:
Ao deslocar inteiros com sinal para a direita,
aplique as mesmas regras dos inteiros sem sinal,
mas preencha os bits vazios à esquerda com o *bit de sinal*,
em vez de com zero.

![](bitshiftSigned)

Isso garante que inteiros com sinal mantenham o mesmo sinal depois de deslocados para a direita,
e é conhecido como *deslocamento aritmético*.

Por causa da forma especial como números positivos e negativos são armazenados,
deslocar qualquer um deles para a direita os aproxima do zero.
Manter o bit de sinal igual durante esse deslocamento faz com que
inteiros negativos continuem negativos à medida que seu valor se aproxima do zero.

## Operadores de overflow

Se você tentar inserir um número em uma constante ou variável inteira
que não consegue armazenar esse valor,
por padrão a Swift reporta um erro em vez de permitir que um valor inválido seja criado.
Esse comportamento oferece segurança extra quando você trabalha com números grandes ou pequenos demais.

Por exemplo, o tipo inteiro `Int16` pode armazenar
qualquer inteiro com sinal entre `-32768` e `32767`.
Tentar atribuir a uma constante ou variável `Int16` um número fora desse intervalo
causa um erro:

```swift
var potentialOverflow = Int16.max
// potentialOverflow equals 32767, which is the maximum value an Int16 can hold
potentialOverflow += 1
// this causes an error
```

<!--
  - test: `overflowOperatorsWillFailToOverflow`

  ```swifttest
  -> var potentialOverflow = Int16.max
  /> potentialOverflow equals \(potentialOverflow), which is the maximum value an Int16 can hold
  </ potentialOverflow equals 32767, which is the maximum value an Int16 can hold
  -> potentialOverflow += 1
  xx overflow
  // this causes an error
  ```
-->

Tratar valores que ficam grandes ou pequenos demais com erros
oferece muito mais flexibilidade ao programar para condições de valores-limite.

No entanto, quando você quer especificamente que uma condição de overflow
trunque o número de bits disponíveis,
pode optar por esse comportamento em vez de disparar um erro.
A Swift oferece três *operadores de overflow* aritméticos que optam pelo comportamento de overflow
em cálculos com inteiros.
Todos esses operadores começam com um e comercial (`&`):

- Adição com overflow (`&+`)
- Subtração com overflow (`&-`)
- Multiplicação com overflow (`&*`)

### Overflow de valor

Números podem sofrer overflow tanto no sentido positivo quanto no negativo.

Veja um exemplo do que acontece quando
um inteiro sem sinal sofre overflow no sentido positivo,
usando o operador de adição com overflow (`&+`):

```swift
var unsignedOverflow = UInt8.max
// unsignedOverflow equals 255, which is the maximum value a UInt8 can hold
unsignedOverflow = unsignedOverflow &+ 1
// unsignedOverflow is now equal to 0
```

<!--
  - test: `overflowOperatorsWillOverflowInPositiveDirection`

  ```swifttest
  -> var unsignedOverflow = UInt8.max
  /> unsignedOverflow equals \(unsignedOverflow), which is the maximum value a UInt8 can hold
  </ unsignedOverflow equals 255, which is the maximum value a UInt8 can hold
  -> unsignedOverflow = unsignedOverflow &+ 1
  /> unsignedOverflow is now equal to \(unsignedOverflow)
  </ unsignedOverflow is now equal to 0
  ```
-->

A variável `unsignedOverflow` é inicializada com o valor máximo que um `UInt8` pode armazenar
(`255`, ou `11111111` em binário).
Em seguida, ela é incrementada em `1` com o operador de adição com overflow (`&+`).
Isso empurra sua representação binária um pouco além do tamanho que um `UInt8` consegue armazenar,
fazendo com que ela sofra overflow além dos seus limites,
como mostra o diagrama abaixo.
O valor que permanece dentro dos limites do `UInt8`
após a adição com overflow é `00000000`, ou zero.

![](overflowAddition)

Algo semelhante acontece quando
um inteiro sem sinal sofre overflow no sentido negativo.
Veja um exemplo usando o operador de subtração com overflow (`&-`):

```swift
var unsignedOverflow = UInt8.min
// unsignedOverflow equals 0, which is the minimum value a UInt8 can hold
unsignedOverflow = unsignedOverflow &- 1
// unsignedOverflow is now equal to 255
```

<!--
  - test: `overflowOperatorsWillOverflowInNegativeDirection`

  ```swifttest
  -> var unsignedOverflow = UInt8.min
  /> unsignedOverflow equals \(unsignedOverflow), which is the minimum value a UInt8 can hold
  </ unsignedOverflow equals 0, which is the minimum value a UInt8 can hold
  -> unsignedOverflow = unsignedOverflow &- 1
  /> unsignedOverflow is now equal to \(unsignedOverflow)
  </ unsignedOverflow is now equal to 255
  ```
-->

O valor mínimo que um `UInt8` pode armazenar é zero,
ou `00000000` em binário.
Se você subtrair `1` de `00000000` usando o operador de subtração com overflow (`&-`),
o número sofrerá overflow e dará a volta até `11111111`,
ou `255` em decimal.

![](overflowUnsignedSubtraction)

O overflow também ocorre com inteiros com sinal.
Todas as somas e subtrações de inteiros com sinal são realizadas bit a bit,
com o bit de sinal incluído como parte dos números que estão sendo somados ou subtraídos,
como descrito em <doc:AdvancedOperators#Bitwise-Left-and-Right-Shift-Operators>.

```swift
var signedOverflow = Int8.min
// signedOverflow equals -128, which is the minimum value an Int8 can hold
signedOverflow = signedOverflow &- 1
// signedOverflow is now equal to 127
```

<!--
  - test: `overflowOperatorsWillOverflowSigned`

  ```swifttest
  -> var signedOverflow = Int8.min
  /> signedOverflow equals \(signedOverflow), which is the minimum value an Int8 can hold
  </ signedOverflow equals -128, which is the minimum value an Int8 can hold
  -> signedOverflow = signedOverflow &- 1
  /> signedOverflow is now equal to \(signedOverflow)
  </ signedOverflow is now equal to 127
  ```
-->

O valor mínimo que um `Int8` pode armazenar é `-128`,
ou `10000000` em binário.
Subtrair `1` desse número binário com o operador de overflow
resulta no valor binário `01111111`,
que inverte o bit de sinal e produz `127` positivo,
o maior valor positivo que um `Int8` pode armazenar.

![](overflowSignedSubtraction)

Tanto para inteiros com sinal quanto sem sinal,
o overflow no sentido positivo
dá a volta a partir do maior valor inteiro válido até o menor,
e o overflow no sentido negativo
dá a volta a partir do menor valor até o maior.

## Precedência e associatividade

A *precedência* de operadores dá a alguns operadores prioridade maior que a de outros;
esses operadores são aplicados primeiro.

A *associatividade* de operadores define como operadores de mesma precedência
são agrupados:
pela esquerda ou pela direita.
Pense nisso como “eles se associam à expressão à sua esquerda”
ou “eles se associam à expressão à sua direita”.

É importante considerar
a precedência e a associatividade de cada operador
ao determinar a ordem em que uma expressão composta será calculada.
Por exemplo, a precedência de operadores explica por que a expressão a seguir resulta em `17`.

```swift
2 + 3 % 4 * 5
// this equals 17
```

<!--
  - test: `evaluationOrder`

  ```swifttest
  >> let r0 =
  -> 2 + 3 % 4 * 5
  >> assert(r0 == 17)
  /> this equals \(2 + 3 % 4 * 5)
  </ this equals 17
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

Se você lesse estritamente da esquerda para a direita,
poderia esperar que a expressão fosse calculada assim:

- `2` mais `3` é igual a `5`
- `5` resto `4` é igual a `1`
- `1` vezes `5` é igual a `5`

No entanto, a resposta real é `17`, não `5`.
Operadores de maior precedência são avaliados antes dos de menor precedência.
Na Swift, assim como no C,
o operador de resto (`%`) e o operador de multiplicação (`*`)
têm precedência maior que o operador de adição (`+`).
Por isso, ambos são avaliados antes de a adição ser considerada.

Porém, o resto e a multiplicação têm a *mesma* precedência entre si.
Para determinar a ordem exata de avaliação,
você também precisa considerar a associatividade.
O resto e a multiplicação se associam à expressão à sua esquerda.
Pense nisso como adicionar parênteses implícitos em torno dessas partes da expressão,
começando pela esquerda:

```swift
2 + ((3 % 4) * 5)
```

<!--
  - test: `evaluationOrder`

  ```swifttest
  >> let r1 =
  -> 2 + ((3 % 4) * 5)
  >> assert(r1 == 17)
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

`(3 % 4)` é `3`, então isso equivale a:

```swift
2 + (3 * 5)
```

<!--
  - test: `evaluationOrder`

  ```swifttest
  >> let r2 =
  -> 2 + (3 * 5)
  >> assert(r2 == 17)
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

`(3 * 5)` é `15`, então isso equivale a:

```swift
2 + 15
```

<!--
  - test: `evaluationOrder`

  ```swifttest
  >> let r3 =
  -> 2 + 15
  >> assert(r3 == 17)
  ```
-->

<!--
  Rewrite the above to avoid bare expressions.
  Tracking bug is <rdar://problem/35301593>
-->

Esse cálculo resulta na resposta final `17`.

Para informações sobre os operadores fornecidos pela biblioteca padrão da Swift,
incluindo uma lista completa dos grupos de precedência e das configurações de associatividade,
consulte [Declarações de operadores](https://developer.apple.com/documentation/swift/operator_declarations).

> Nota: As regras de precedência e associatividade de operadores da Swift são mais simples e previsíveis
> do que as encontradas no C e no Objective-C.
> No entanto, isso significa que elas não são exatamente iguais às das linguagens baseadas em C.
> Tenha cuidado para garantir que as interações entre operadores continuem se comportando como você pretende
> ao portar código existente para a Swift.

## Métodos de operador

Classes e structs podem fornecer suas próprias implementações de operadores existentes.
Isso é conhecido como *sobrecarga* dos operadores existentes.

O exemplo abaixo mostra como implementar
o operador de adição aritmética (`+`) para uma struct personalizada.
O operador de adição aritmética é um operador binário
porque opera sobre dois alvos,
e é um operador infixo porque aparece entre esses dois alvos.

O exemplo define uma struct `Vector2D` para
um vetor de posição bidimensional `(x, y)`,
seguido da definição de um *método de operador*
para somar instâncias da struct `Vector2D`:

```swift
struct Vector2D {
    var x = 0.0, y = 0.0
}

extension Vector2D {
    static func + (left: Vector2D, right: Vector2D) -> Vector2D {
       return Vector2D(x: left.x + right.x, y: left.y + right.y)
    }
}
```

<!--
  - test: `customOperators`

  ```swifttest
  -> struct Vector2D {
        var x = 0.0, y = 0.0
     }

  -> extension Vector2D {
         static func + (left: Vector2D, right: Vector2D) -> Vector2D {
            return Vector2D(x: left.x + right.x, y: left.y + right.y)
         }
     }
  ```
-->

O método de operador é definido como um método de tipo em `Vector2D`,
com um nome de método que corresponde ao operador a ser sobrecarregado (`+`).
Como a adição não faz parte do comportamento essencial de um vetor,
o método de tipo é definido em uma extension de `Vector2D`
em vez de na declaração principal da struct `Vector2D`.
Como o operador de adição aritmética é um operador binário,
esse método de operador recebe dois parâmetros de entrada do tipo `Vector2D`
e retorna um único valor de saída, também do tipo `Vector2D`.

Nessa implementação, os parâmetros de entrada se chamam `left` e `right`
para representar as instâncias de `Vector2D` que estarão do lado esquerdo e do lado direito do operador `+`.
O método retorna uma nova instância de `Vector2D`,
cujas propriedades `x` e `y` são
inicializadas com a soma das propriedades `x` e `y` das
duas instâncias de `Vector2D` que estão sendo somadas.

O método de tipo
pode ser usado como operador infixo entre instâncias existentes de `Vector2D`:

```swift
let vector = Vector2D(x: 3.0, y: 1.0)
let anotherVector = Vector2D(x: 2.0, y: 4.0)
let combinedVector = vector + anotherVector
// combinedVector is a Vector2D instance with values of (5.0, 5.0)
```

<!--
  - test: `customOperators`

  ```swifttest
  -> let vector = Vector2D(x: 3.0, y: 1.0)
  -> let anotherVector = Vector2D(x: 2.0, y: 4.0)
  -> let combinedVector = vector + anotherVector
  /> combinedVector is a Vector2D instance with values of (\(combinedVector.x), \(combinedVector.y))
  </ combinedVector is a Vector2D instance with values of (5.0, 5.0)
  ```
-->

Este exemplo soma os vetores `(3.0, 1.0)` e `(2.0, 4.0)`
para formar o vetor `(5.0, 5.0)`, como ilustrado abaixo.

![](vectorAddition)

### Operadores prefixos e pós-fixos

O exemplo acima demonstra uma implementação personalizada de um operador binário infixo.
Classes e structs também podem fornecer implementações
dos *operadores unários* padrão.
Operadores unários operam sobre um único alvo.
Eles são *prefixos* quando precedem o alvo (como em `-a`)
e *pós-fixos* quando seguem o alvo (como em `b!`).

Você implementa um operador unário prefixo ou pós-fixo escrevendo
o modificador `prefix` ou `postfix`
antes da palavra-chave `func` ao declarar o método de operador:

```swift
extension Vector2D {
    static prefix func - (vector: Vector2D) -> Vector2D {
        return Vector2D(x: -vector.x, y: -vector.y)
    }
}
```

<!--
  - test: `customOperators`

  ```swifttest
  -> extension Vector2D {
         static prefix func - (vector: Vector2D) -> Vector2D {
             return Vector2D(x: -vector.x, y: -vector.y)
         }
     }
  ```
-->

O exemplo acima implementa o operador de menos unário
(`-a`) para instâncias de `Vector2D`.
O operador de menos unário é um operador prefixo,
por isso esse método precisa ser qualificado com o modificador `prefix`.

Para valores numéricos simples, o operador de menos unário converte
números positivos em seus equivalentes negativos, e vice-versa.
A implementação correspondente para instâncias de `Vector2D`
executa essa operação sobre as propriedades `x` e `y`:

```swift
let positive = Vector2D(x: 3.0, y: 4.0)
let negative = -positive
// negative is a Vector2D instance with values of (-3.0, -4.0)
let alsoPositive = -negative
// alsoPositive is a Vector2D instance with values of (3.0, 4.0)
```

<!--
  - test: `customOperators`

  ```swifttest
  -> let positive = Vector2D(x: 3.0, y: 4.0)
  -> let negative = -positive
  /> negative is a Vector2D instance with values of (\(negative.x), \(negative.y))
  </ negative is a Vector2D instance with values of (-3.0, -4.0)
  -> let alsoPositive = -negative
  /> alsoPositive is a Vector2D instance with values of (\(alsoPositive.x), \(alsoPositive.y))
  </ alsoPositive is a Vector2D instance with values of (3.0, 4.0)
  ```
-->

### Operadores de atribuição composta

*Operadores de atribuição composta* combinam a atribuição (`=`) com outra operação.
Por exemplo, o operador de atribuição por adição (`+=`)
combina adição e atribuição em uma única operação.
Você marca o tipo do parâmetro de entrada à esquerda de um operador de atribuição composta como `inout`,
porque o valor do parâmetro será modificado diretamente dentro do método de operador.

O exemplo abaixo implementa
um método de operador de atribuição por adição para instâncias de `Vector2D`:

```swift
extension Vector2D {
    static func += (left: inout Vector2D, right: Vector2D) {
        left = left + right
    }
}
```

<!--
  - test: `customOperators`

  ```swifttest
  -> extension Vector2D {
         static func += (left: inout Vector2D, right: Vector2D) {
             left = left + right
         }
     }
  ```
-->

Como um operador de adição já foi definido antes,
você não precisa reimplementar o processo de adição aqui.
Em vez disso, o método de operador de atribuição por adição
aproveita o método de operador de adição existente
e o usa para definir o valor à esquerda como o valor à esquerda mais o valor à direita:

```swift
var original = Vector2D(x: 1.0, y: 2.0)
let vectorToAdd = Vector2D(x: 3.0, y: 4.0)
original += vectorToAdd
// original now has values of (4.0, 6.0)
```

<!--
  - test: `customOperators`

  ```swifttest
  -> var original = Vector2D(x: 1.0, y: 2.0)
  -> let vectorToAdd = Vector2D(x: 3.0, y: 4.0)
  -> original += vectorToAdd
  /> original now has values of (\(original.x), \(original.y))
  </ original now has values of (4.0, 6.0)
  ```
-->

> Nota: Não é possível sobrecarregar o operador de atribuição padrão
> (`=`).
> Apenas os operadores de atribuição composta podem ser sobrecarregados.
> Da mesma forma, o operador condicional ternário
> (`a ? b : c`) não pode ser sobrecarregado.

<!--
  - test: `cant-overload-assignment`

  ```swifttest
  >> struct Vector2D {
  >>    var x = 0.0, y = 0.0
  >> }
  >> extension Vector2D {
  >>     static func = (left: inout Vector2D, right: Vector2D) {
  >>         left = right
  >>     }
  >> }
  !$ error: expected identifier in function declaration
  !! static func = (left: inout Vector2D, right: Vector2D) {
  !!             ^
  ```
-->

### Operadores de equivalência

Por padrão, classes e structs personalizados não têm implementação dos
*operadores de equivalência*,
conhecidos como operador de *igual a* (`==`) e operador de *diferente de* (`!=`).
Normalmente você implementa o operador `==`,
e usa a implementação padrão da biblioteca padrão da Swift para o operador `!=`,
que nega o resultado do operador `==`.
Há duas formas de implementar o operador `==`:
você pode implementá-lo você mesmo,
ou, para muitos tipos, pode pedir à Swift que sintetize
uma implementação para você.
Nos dois casos,
você adiciona a conformidade com o protocolo `Equatable` da biblioteca padrão da Swift.

Você fornece uma implementação do operador `==`
da mesma forma que implementa outros operadores infixos:

```swift
extension Vector2D: Equatable {
    static func == (left: Vector2D, right: Vector2D) -> Bool {
       return (left.x == right.x) && (left.y == right.y)
    }
}
```

<!--
  - test: `customOperators`

  ```swifttest
  -> extension Vector2D: Equatable {
         static func == (left: Vector2D, right: Vector2D) -> Bool {
            return (left.x == right.x) && (left.y == right.y)
         }
     }
  ```
-->

O exemplo acima implementa um operador `==`
para verificar se duas instâncias de `Vector2D` têm valores equivalentes.
No contexto de `Vector2D`,
faz sentido considerar “igual” como significando
“ambas as instâncias têm os mesmos valores de `x` e os mesmos valores de `y`”,
e por isso essa é a lógica usada na implementação do operador.

Agora você pode usar esse operador para verificar se duas instâncias de `Vector2D` são equivalentes:

```swift
let twoThree = Vector2D(x: 2.0, y: 3.0)
let anotherTwoThree = Vector2D(x: 2.0, y: 3.0)
if twoThree == anotherTwoThree {
    print("These two vectors are equivalent.")
}
// Prints "These two vectors are equivalent."
```

<!--
  - test: `customOperators`

  ```swifttest
  -> let twoThree = Vector2D(x: 2.0, y: 3.0)
  -> let anotherTwoThree = Vector2D(x: 2.0, y: 3.0)
  -> if twoThree == anotherTwoThree {
        print("These two vectors are equivalent.")
     }
  <- These two vectors are equivalent.
  ```
-->

Em muitos casos simples, você pode pedir à Swift
que forneça implementações sintetizadas dos operadores de equivalência para você,
como descrito em <doc:Protocols#Adopting-a-Protocol-Using-a-Synthesized-Implementation>.

## Operadores personalizados

Você pode declarar e implementar seus próprios *operadores personalizados*, além dos
operadores padrão fornecidos pela Swift.
Para uma lista de caracteres que podem ser usados para definir operadores personalizados,
consulte <doc:LexicalStructure#Operators>.

Novos operadores são declarados em nível global usando a palavra-chave `operator`,
e são marcados com os modificadores `prefix`, `infix` ou `postfix`:

```swift
prefix operator +++
```

<!--
  - test: `customOperators`

  ```swifttest
  -> prefix operator +++
  ```
-->

O exemplo acima define um novo operador prefixo chamado `+++`.
Esse operador não tem um significado existente na Swift,
por isso recebe seu próprio significado personalizado abaixo, no contexto específico de
trabalhar com instâncias de `Vector2D`. Para fins deste exemplo,
`+++` é tratado como um novo operador prefixo de “duplicação”.
Ele dobra os valores de `x` e `y` de uma instância de `Vector2D`,
somando o vetor a si mesmo com o operador de atribuição por adição definido anteriormente.
Para implementar o operador `+++`,
você adiciona um método de tipo chamado `+++` a `Vector2D` da seguinte forma:

```swift
extension Vector2D {
    static prefix func +++ (vector: inout Vector2D) -> Vector2D {
        vector += vector
        return vector
    }
}

var toBeDoubled = Vector2D(x: 1.0, y: 4.0)
let afterDoubling = +++toBeDoubled
// toBeDoubled now has values of (2.0, 8.0)
// afterDoubling also has values of (2.0, 8.0)
```

<!--
  - test: `customOperators`

  ```swifttest
  -> extension Vector2D {
        static prefix func +++ (vector: inout Vector2D) -> Vector2D {
           vector += vector
           return vector
        }
     }

  -> var toBeDoubled = Vector2D(x: 1.0, y: 4.0)
  -> let afterDoubling = +++toBeDoubled
  /> toBeDoubled now has values of (\(toBeDoubled.x), \(toBeDoubled.y))
  </ toBeDoubled now has values of (2.0, 8.0)
  /> afterDoubling also has values of (\(afterDoubling.x), \(afterDoubling.y))
  </ afterDoubling also has values of (2.0, 8.0)
  ```
-->

### Precedência para operadores infixos personalizados

Operadores infixos personalizados pertencem cada um a um grupo de precedência.
Um grupo de precedência especifica a precedência de um operador em relação
a outros operadores infixos, além da associatividade do operador.
Veja <doc:AdvancedOperators#Precedence-and-Associativity> para uma explicação de
como essas características afetam a interação de um operador infixo
com outros operadores infixos.

Um operador infixo personalizado que não é explicitamente colocado em um grupo de precedência
recebe um grupo de precedência padrão, com precedência imediatamente superior
à do operador condicional ternário.

O exemplo a seguir define um novo operador infixo personalizado chamado `+-`,
que pertence ao grupo de precedência `AdditionPrecedence`:

```swift
infix operator +-: AdditionPrecedence
extension Vector2D {
    static func +- (left: Vector2D, right: Vector2D) -> Vector2D {
        return Vector2D(x: left.x + right.x, y: left.y - right.y)
    }
}
let firstVector = Vector2D(x: 1.0, y: 2.0)
let secondVector = Vector2D(x: 3.0, y: 4.0)
let plusMinusVector = firstVector +- secondVector
// plusMinusVector is a Vector2D instance with values of (4.0, -2.0)
```

<!--
  - test: `customOperators`

  ```swifttest
  -> infix operator +-: AdditionPrecedence
  -> extension Vector2D {
        static func +- (left: Vector2D, right: Vector2D) -> Vector2D {
           return Vector2D(x: left.x + right.x, y: left.y - right.y)
        }
     }
  -> let firstVector = Vector2D(x: 1.0, y: 2.0)
  -> let secondVector = Vector2D(x: 3.0, y: 4.0)
  -> let plusMinusVector = firstVector +- secondVector
  /> plusMinusVector is a Vector2D instance with values of (\(plusMinusVector.x), \(plusMinusVector.y))
  </ plusMinusVector is a Vector2D instance with values of (4.0, -2.0)
  ```
-->

Esse operador soma os valores `x` de dois vetores
e subtrai o valor `y` do segundo vetor do primeiro.
Como ele é, na essência, um operador “aditivo”,
recebeu o mesmo grupo de precedência
dos operadores infixos aditivos, como `+` e `-`.
Para informações sobre os operadores fornecidos pela biblioteca padrão da Swift,
incluindo uma lista completa dos grupos de precedência e das configurações de associatividade,
consulte [Declarações de operadores](https://developer.apple.com/documentation/swift/operator_declarations).
Para mais informações sobre grupos de precedência e para ver a sintaxe
para definir seus próprios operadores e grupos de precedência,
consulte <doc:Declarations#Operator-Declaration>.

> Nota: Você não especifica precedência ao definir um operador prefixo ou pós-fixo.
> No entanto, se você aplicar um operador prefixo e um pós-fixo ao mesmo operando,
> o operador pós-fixo é aplicado primeiro.

<!--
  - test: `postfixOperatorsAreAppliedBeforePrefixOperators`

  ```swifttest
  -> prefix operator +++
  -> postfix operator ---
  -> extension Int {
         static prefix func +++ (x: Int) -> Int {
             return x * 2
         }
     }
  -> extension Int {
         static postfix func --- (x: Int) -> Int {
             return x - 1
         }
     }
  -> let x = +++1---
  -> let y = +++(1---)
  -> let z = (+++1)---
  -> print(x, y, z)
  <- 0 0 1
  // Note that x==y
  ```
-->

## Result builders

Um *result builder* é um tipo que você define
e que adiciona sintaxe para criar dados aninhados,
como uma lista ou uma árvore, de forma natural e declarativa.
O código que usa o result builder
pode incluir sintaxe comum da Swift, como `if` e `for`,
para lidar com partes condicionais ou repetidas dos dados.

O código abaixo define alguns tipos para desenhar em uma única linha
usando estrelas e texto.

```swift
protocol Drawable {
    func draw() -> String
}
struct Line: Drawable {
    var elements: [Drawable]
    func draw() -> String {
        return elements.map { $0.draw() }.joined(separator: "")
    }
}
struct Text: Drawable {
    var content: String
    init(_ content: String) { self.content = content }
    func draw() -> String { return content }
}
struct Space: Drawable {
    func draw() -> String { return " " }
}
struct Stars: Drawable {
    var length: Int
    func draw() -> String { return String(repeating: "*", count: length) }
}
struct AllCaps: Drawable {
    var content: Drawable
    func draw() -> String { return content.draw().uppercased() }
}
```

<!--
  - test: `result-builder`

  ```swifttest
  -> protocol Drawable {
         func draw() -> String
     }
  -> struct Line: Drawable {
         var elements: [Drawable]
         func draw() -> String {
             return elements.map { $0.draw() }.joined(separator: "")
         }
     }
  -> struct Text: Drawable {
         var content: String
         init(_ content: String) { self.content = content }
         func draw() -> String { return content }
     }
  -> struct Space: Drawable {
         func draw() -> String { return " " }
     }
  -> struct Stars: Drawable {
         var length: Int
         func draw() -> String { return String(repeating: "*", count: length) }
     }
  -> struct AllCaps: Drawable {
         var content: Drawable
         func draw() -> String { return content.draw().uppercased() }
     }
  ```
-->

O protocolo `Drawable` define o requisito
para algo que pode ser desenhado, como uma linha ou uma forma:
o tipo precisa implementar um método `draw()`.
A struct `Line` representa um desenho de uma única linha,
e serve como contêiner de nível superior para a maioria dos desenhos.
Para desenhar uma `Line`,
a struct chama `draw()` em cada um dos componentes da linha,
e depois concatena as strings resultantes em uma única string.
A struct `Text` envolve uma string para torná-la parte de um desenho.
A struct `AllCaps` envolve e modifica outro desenho,
convertendo qualquer texto do desenho para maiúsculas.

É possível montar um desenho com esses tipos
chamando seus inicializadores:

```swift
let name: String? = "Ravi Patel"
let manualDrawing = Line(elements: [
     Stars(length: 3),
     Text("Hello"),
     Space(),
     AllCaps(content: Text((name ?? "World") + "!")),
     Stars(length: 2),
])
print(manualDrawing.draw())
// Prints "***Hello RAVI PATEL!**".
```

<!--
  - test: `result-builder`

  ```swifttest
  -> let name: String? = "Ravi Patel"
  -> let manualDrawing = Line(elements: [
          Stars(length: 3),
          Text("Hello"),
          Space(),
          AllCaps(content: Text((name ?? "World") + "!")),
          Stars(length: 2),
     ])
  -> print(manualDrawing.draw())
  <- ***Hello RAVI PATEL!**
  ```
-->

Esse código funciona, mas é um pouco desajeitado.
Os parênteses aninhados depois de `AllCaps` são difíceis de ler.
A lógica de valor padrão para usar "World" quando `name` é `nil`
precisa ser feita inline com o operador `??`,
o que seria difícil com algo mais complexo.
Se você precisasse incluir instruções switch ou laços `for`
para montar parte do desenho, não haveria como fazer isso.
Um result builder permite reescrever código assim
para que ele pareça código Swift comum.

Para definir um result builder,
você escreve o atributo `@resultBuilder` na declaração do tipo.
Por exemplo, este código define um result builder chamado `DrawingBuilder`,
que permite usar uma sintaxe declarativa para descrever um desenho:

```swift
@resultBuilder
struct DrawingBuilder {
    static func buildBlock(_ components: Drawable...) -> Drawable {
        return Line(elements: components)
    }
    static func buildEither(first: Drawable) -> Drawable {
        return first
    }
    static func buildEither(second: Drawable) -> Drawable {
        return second
    }
}
```

<!--
  - test: `result-builder`

  ```swifttest
  -> @resultBuilder
  -> struct DrawingBuilder {
         static func buildBlock(_ components: Drawable...) -> Drawable {
             return Line(elements: components)
         }
         static func buildEither(first: Drawable) -> Drawable {
             return first
         }
         static func buildEither(second: Drawable) -> Drawable {
             return second
         }
     }
  ```
-->

A struct `DrawingBuilder` define três métodos
que implementam partes da sintaxe de result builder.
O método `buildBlock(_:)` permite escrever uma série de linhas em um bloco de código.
Ele combina os componentes desse bloco em uma `Line`.
Os métodos `buildEither(first:)` e `buildEither(second:)`
permitem usar `if`-`else`.

Você pode aplicar o atributo `@DrawingBuilder` ao parâmetro de uma função,
o que transforma um closure passado para a função
no valor que o result builder cria a partir desse closure.
Por exemplo:

```swift
func draw(@DrawingBuilder content: () -> Drawable) -> Drawable {
    return content()
}
func caps(@DrawingBuilder content: () -> Drawable) -> Drawable {
    return AllCaps(content: content())
}

func makeGreeting(for name: String? = nil) -> Drawable {
    let greeting = draw {
        Stars(length: 3)
        Text("Hello")
        Space()
        caps {
            if let name = name {
                Text(name + "!")
            } else {
                Text("World!")
            }
        }
        Stars(length: 2)
    }
    return greeting
}
let genericGreeting = makeGreeting()
print(genericGreeting.draw())
// Prints "***Hello WORLD!**".

let personalGreeting = makeGreeting(for: "Ravi Patel")
print(personalGreeting.draw())
// Prints "***Hello RAVI PATEL!**".
```

<!--
  - test: `result-builder`

  ```swifttest
  -> func draw(@DrawingBuilder content: () -> Drawable) -> Drawable {
         return content()
     }
  -> func caps(@DrawingBuilder content: () -> Drawable) -> Drawable {
         return AllCaps(content: content())
     }

  -> func makeGreeting(for name: String? = nil) -> Drawable {
         let greeting = draw {
             Stars(length: 3)
             Text("Hello")
             Space()
             caps {
                 if let name = name {
                     Text(name + "!")
                 } else {
                     Text("World!")
                 }
             }
             Stars(length: 2)
         }
         return greeting
     }
  -> let genericGreeting = makeGreeting()
  -> print(genericGreeting.draw())
  <- ***Hello WORLD!**

  -> let personalGreeting = makeGreeting(for: "Ravi Patel")
  -> print(personalGreeting.draw())
  <- ***Hello RAVI PATEL!**
  ```
-->

A função `makeGreeting(for:)` recebe um parâmetro `name`
e o usa para desenhar uma saudação personalizada.
As funções `draw(_:)` e `caps(_:)`
recebem, cada uma, um único closure como argumento,
marcado com o atributo `@DrawingBuilder`.
Quando você chama essas funções,
usa a sintaxe especial que `DrawingBuilder` define.
A Swift transforma essa descrição declarativa de um desenho
em uma série de chamadas aos métodos de `DrawingBuilder`,
para montar o valor que é passado como argumento da função.
Por exemplo,
a Swift transforma a chamada a `caps(_:)` naquele exemplo
em um código como o seguinte:

```swift
let capsDrawing = caps {
    let partialDrawing: Drawable
    if let name = name {
        let text = Text(name + "!")
        partialDrawing = DrawingBuilder.buildEither(first: text)
    } else {
        let text = Text("World!")
        partialDrawing = DrawingBuilder.buildEither(second: text)
    }
    return partialDrawing
}
```

<!--
  - test: `result-builder`

  ```swifttest
  -> let capsDrawing = caps {
         let partialDrawing: Drawable
         if let name = name {
             let text = Text(name + "!")
             partialDrawing = DrawingBuilder.buildEither(first: text)
         } else {
             let text = Text("World!")
             partialDrawing = DrawingBuilder.buildEither(second: text)
         }
         return partialDrawing
  -> }
  >> print(capsDrawing.draw())
  << RAVI PATEL!
  ```
-->

A Swift transforma o bloco `if`-`else` em
chamadas aos métodos `buildEither(first:)` e `buildEither(second:)`.
Embora você não chame esses métodos no seu próprio código,
mostrar o resultado da transformação
facilita ver como a Swift transforma seu código
quando você usa a sintaxe de `DrawingBuilder`.

Para permitir escrever laços `for` na sintaxe especial de desenho,
adicione um método `buildArray(_:)`.

```swift
extension DrawingBuilder {
    static func buildArray(_ components: [Drawable]) -> Drawable {
        return Line(elements: components)
    }
}
let manyStars = draw {
    Text("Stars:")
    for length in 1...3 {
        Space()
        Stars(length: length)
    }
}
```

<!--
  - test: `result-builder`

  ```swifttest
  -> extension DrawingBuilder {
         static func buildArray(_ components: [Drawable]) -> Drawable {
             return Line(elements: components)
         }
     }
  -> let manyStars = draw {
         Text("Stars:")
         for length in 1...3 {
             Space()
             Stars(length: length)
         }
  -> }
  >> print(manyStars.draw())
  << Stars: * ** ***
  ```
-->

No código acima, o laço `for` cria um array de desenhos,
e o método `buildArray(_:)` transforma esse array em uma `Line`.

Para uma lista completa de como a Swift transforma a sintaxe de builder
em chamadas aos métodos do tipo builder,
consulte <doc:Attributes#resultBuilder>.

<!--
  The following needs more work...

   Protocol Operator Requirements
   ------------------------------

   You can include operators in the requirements of a protocol.
   A type conforms to the protocol
   only if there's an implementation of the operator for that type.
   You use ``Self`` to refer to the type that will conform to the protocol,
   just like you do in other protocol requirements.
   For example, the Swift standard library defines the ``Equatable`` protocol
   which requires the ``==`` operator:

   .. testcode:: protocolOperator

      -> protocol Equatable {
             static func == (lhs: Self, rhs: Self) -> Bool
         }

   To make a type conform to the protocol,
   you need to implement the ``==`` operator for that type.
   For example:

   .. testcode:: protocolOperator

  -> struct Vector3D {
        var x = 0.0, y = 0.0, z = 0.0
     }
  -> extension Vector3D: Equatable {
         static func == (left: Vector3D, right: Vector3D) -> Bool {
             return (left.x == right.x) && (left.y == right.y) && (left.z == right.z)
         }
     }
  >> let r0 =
  >> Vector3D(x: 1.1, y: 2.3, z: 12) == Vector3D(x: 1.1, y: 2.3, z: 12)
  >> assert(r0)
-->

<!--
  FIXME: This doesn't work
  <rdar://problem/27536066> SE-0091 -- can't have protocol conformance & operator implementation in different types

   For operators that take values of two different types,
   the operator's implementation doesn't have to be
   a member of the type that conforms to the protocol ---
   the implementation can also be a member of the other type.
   For example,
   the code below defines the ``*`` operator
   to scale a vector by a given amount.
   The ``Vector2D`` structure conforms to this protocol
   because there's an implementation of the operator
   that takes a ``Vector2D`` as its second argument,
   even though that implementation is a member of ``Double``.

   .. testcode:: customOperators

  -> infix operator *** {}
  -> protocol AnotherProtocol {
         // static func * (scale: Double, vector: Self) -> Self
         static func *** (scale: Double, vector: Vector2D) -> Vector2D
     }

  -> extension Double {
         static func *** (scale: Double, vector: Vector2D) -> Vector2D {
             return Vector2D(x: scale * vector.x, y: scale * vector.y)
         }
     }
  -> extension Vector2D: AnotherProtocol {}
  -> let unitVector = Vector2D(x: 1.0, y: 1.0)
  -> print(2.5 *** unitVector)
  <- Vector2D(x: 2.5, y: 2.5)
-->

<!--
  TODO: However, Doug thought that this might be better covered by Generics,
  where you know that two things are definitely of the same type.
  Perhaps mention it here, but don't actually show an example?
-->

<!--
  TODO: generic operators
-->

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->

<!-- ia-translate: true -->
