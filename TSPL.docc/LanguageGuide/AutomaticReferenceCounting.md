# Contagem automática de referências (ARC)

Modele o tempo de vida dos objetos e os relacionamentos entre eles.

O Swift usa a *contagem automática de referências* (ARC)
para rastrear e gerenciar o uso de memória do seu app.
Na maioria dos casos, isso significa que o gerenciamento de memória “simplesmente funciona” no Swift,
e você não precisa pensar nele.
O ARC libera automaticamente a memória usada pelas instâncias de classe
quando essas instâncias não são mais necessárias.

No entanto, em alguns casos, o ARC precisa de mais informações
sobre a relação entre partes do seu código
para gerenciar a memória por você.
Este capítulo descreve essas situações
e mostra como fazer o ARC gerenciar toda a memória do seu app.
Usar o ARC no Swift é muito parecido com a abordagem descrita em
[Transitioning to ARC Release Notes](https://developer.apple.com/library/content/releasenotes/ObjectiveC/RN-TransitioningToARC/Introduction/Introduction.html)
para usar o ARC com Objective-C.

A contagem de referências se aplica apenas a instâncias de classes.
Structs e enums são tipos de valor, não tipos de referência,
e não são armazenados nem passados por referência.

## Como o ARC funciona

Toda vez que você cria uma nova instância de classe,
o ARC aloca um bloco de memória para armazenar informações sobre essa instância.
Essa memória guarda informações sobre o tipo da instância,
junto com os valores de quaisquer propriedades armazenadas associadas a essa instância.

Além disso, quando uma instância não é mais necessária,
o ARC libera a memória usada por essa instância
para que ela possa ser usada para outras finalidades.
Isso garante que instâncias de classe não ocupem espaço na memória
quando não são mais necessárias.

No entanto, se o ARC desalocasse uma instância que ainda estivesse em uso,
deixaria de ser possível acessar as propriedades dessa instância
ou chamar os métodos dela.
De fato, se você tentasse acessar a instância, seu app provavelmente travaria.

Para garantir que as instâncias não desapareçam enquanto ainda são necessárias,
o ARC rastreia quantas propriedades, constantes e variáveis
estão referenciando cada instância de classe no momento.
O ARC não desaloca uma instância
enquanto existir pelo menos uma referência ativa a ela.

Para que isso seja possível,
sempre que você atribui uma instância de classe a uma propriedade, constante ou variável,
essa propriedade, constante ou variável faz uma *strong reference* à instância.
A referência é chamada de “strong” porque mantém um vínculo firme com a instância,
e não permite que ela seja desalocada enquanto essa strong reference existir.

## ARC em ação

Aqui está um exemplo de como a contagem automática de referências funciona.
O exemplo começa com uma classe simples chamada `Person`,
que define uma constante de propriedade armazenada chamada `name`:

```swift
class Person {
    let name: String
    init(name: String) {
        self.name = name
        print("\(name) is being initialized")
    }
    deinit {
        print("\(name) is being deinitialized")
    }
}
```

<!--
  - test: `howARCWorks`

  ```swifttest
  -> class Person {
        let name: String
        init(name: String) {
           self.name = name
           print("\(name) is being initialized")
        }
        deinit {
           print("\(name) is being deinitialized")
        }
     }
  ```
-->

A classe `Person` tem um inicializador que define a propriedade `name` da instância
e imprime uma mensagem para indicar que a inicialização está em andamento.
A classe `Person` também tem um desinicializador
que imprime uma mensagem quando uma instância da classe é desalocada.

O próximo trecho de código define três variáveis do tipo `Person?`,
que serão usadas para criar várias referências a uma nova instância de `Person`
nos trechos seguintes.
Como essas variáveis são de um tipo optional (`Person?`, e não `Person`),
elas são automaticamente inicializadas com o valor `nil`
e, por enquanto, não referenciam nenhuma instância de `Person`.

```swift
var reference1: Person?
var reference2: Person?
var reference3: Person?
```

<!--
  - test: `howARCWorks`

  ```swifttest
  -> var reference1: Person?
  -> var reference2: Person?
  -> var reference3: Person?
  ```
-->

Agora você pode criar uma nova instância de `Person`
e atribuí-la a uma dessas três variáveis:

```swift
reference1 = Person(name: "John Appleseed")
// Prints "John Appleseed is being initialized".
```

<!--
  - test: `howARCWorks`

  ```swifttest
  -> reference1 = Person(name: "John Appleseed")
  <- John Appleseed is being initialized
  ```
-->

Observe que a mensagem `"John Appleseed is being initialized"` é impressa
no momento em que você chama o inicializador de `Person`.
Isso confirma que a inicialização ocorreu.

Como a nova instância de `Person` foi atribuída à variável `reference1`,
agora existe uma strong reference de `reference1` para a nova instância de `Person`.
Como existe pelo menos uma strong reference,
o ARC garante que esse `Person` seja mantido na memória e não seja desalocado.

Se você atribuir a mesma instância de `Person` a mais duas variáveis,
outras duas strong references a essa instância são estabelecidas:

```swift
reference2 = reference1
reference3 = reference1
```

<!--
  - test: `howARCWorks`

  ```swifttest
  -> reference2 = reference1
  -> reference3 = reference1
  ```
-->

Agora há *três* strong references para essa única instância de `Person`.

Se você quebrar duas dessas strong references (incluindo a original)
atribuindo `nil` a duas das variáveis,
resta uma única strong reference,
e a instância de `Person` não é desalocada:

```swift
reference1 = nil
reference2 = nil
```

<!--
  - test: `howARCWorks`

  ```swifttest
  -> reference1 = nil
  -> reference2 = nil
  ```
-->

O ARC não desaloca a instância de `Person` até que a terceira e última strong reference
seja quebrada, momento em que fica claro que você não está mais usando a instância de `Person`:

```swift
reference3 = nil
// Prints "John Appleseed is being deinitialized".
```

<!--
  - test: `howARCWorks`

  ```swifttest
  -> reference3 = nil
  <- John Appleseed is being deinitialized
  ```
-->

## Ciclos de strong reference entre instâncias de classe

Nos exemplos acima,
o ARC consegue rastrear o número de referências à nova instância de `Person` que você criou
e desalocar essa instância de `Person` quando ela não for mais necessária.

No entanto, é possível escrever código em que uma instância de uma classe
*nunca* chega a ter zero strong references.
Isso pode acontecer se duas instâncias de classe mantiverem uma strong reference uma para a outra,
de modo que cada instância mantenha a outra viva.
Isso é chamado de *ciclo de strong reference*.

Você resolve ciclos de strong reference
definindo algumas das relações entre classes
como referências weak ou unowned, em vez de strong references.
Esse processo é descrito em
<doc:AutomaticReferenceCounting#Resolving-Strong-Reference-Cycles-Between-Class-Instances>.
Porém, antes de aprender a resolver um ciclo de strong reference,
é útil entender como esse ciclo é causado.

Veja a seguir um exemplo de como um ciclo de strong reference pode ser criado sem querer.
Este exemplo define duas classes, `Person` e `Apartment`,
que modelam um prédio de apartamentos e seus moradores:

```swift
class Person {
    let name: String
    init(name: String) { self.name = name }
    var apartment: Apartment?
    deinit { print("\(name) is being deinitialized") }
}

class Apartment {
    let unit: String
    init(unit: String) { self.unit = unit }
    var tenant: Person?
    deinit { print("Apartment \(unit) is being deinitialized") }
}
```

<!--
  - test: `referenceCycles`

  ```swifttest
  -> class Person {
        let name: String
        init(name: String) { self.name = name }
        var apartment: Apartment?
        deinit { print("\(name) is being deinitialized") }
     }

  -> class Apartment {
        let unit: String
        init(unit: String) { self.unit = unit }
        var tenant: Person?
        deinit { print("Apartment \(unit) is being deinitialized") }
     }
  ```
-->

Toda instância de `Person` tem uma propriedade `name` do tipo `String`
e uma propriedade `apartment` optional, que começa como `nil`.
A propriedade `apartment` é optional porque uma pessoa nem sempre tem um apartamento.

De forma semelhante, toda instância de `Apartment` tem uma propriedade `unit` do tipo `String`
e uma propriedade `tenant` optional, que começa como `nil`.
A propriedade `tenant` é optional porque um apartamento nem sempre tem um inquilino.

As duas classes também definem um desinicializador,
que imprime uma mensagem informando que uma instância da classe está sendo desinicializada.
Isso permite verificar se as instâncias de `Person` e `Apartment`
estão sendo desalocadas como esperado.

Este próximo trecho de código define duas variáveis de tipo optional
chamadas `john` e `unit4A`,
que serão definidas com uma instância específica de `Apartment` e de `Person` mais adiante.
As duas variáveis têm valor inicial `nil`, por serem optionals:

```swift
var john: Person?
var unit4A: Apartment?
```

<!--
  - test: `referenceCycles`

  ```swifttest
  -> var john: Person?
  -> var unit4A: Apartment?
  ```
-->

Agora você pode criar uma instância específica de `Person` e uma de `Apartment`
e atribuir essas novas instâncias às variáveis `john` e `unit4A`:

```swift
john = Person(name: "John Appleseed")
unit4A = Apartment(unit: "4A")
```

<!--
  - test: `referenceCycles`

  ```swifttest
  -> john = Person(name: "John Appleseed")
  -> unit4A = Apartment(unit: "4A")
  ```
-->

Veja como ficam as strong references depois de criar e atribuir essas duas instâncias.
A variável `john` agora tem uma strong reference para a nova instância de `Person`,
e a variável `unit4A` tem uma strong reference para a nova instância de `Apartment`:

![](referenceCycle01)

Agora você pode conectar as duas instâncias,
para que a pessoa tenha um apartamento e o apartamento tenha um inquilino.
Observe que um ponto de exclamação (`!`) é usado para fazer unwrap
e acessar as instâncias armazenadas dentro das variáveis optional `john` e `unit4A`,
para que as propriedades dessas instâncias possam ser definidas:

```swift
john!.apartment = unit4A
unit4A!.tenant = john
```

<!--
  - test: `referenceCycles`

  ```swifttest
  -> john!.apartment = unit4A
  -> unit4A!.tenant = john
  ```
-->

Veja como ficam as strong references depois que você conecta as duas instâncias:

![](referenceCycle02)

Infelizmente, conectar essas duas instâncias cria
um ciclo de strong reference entre elas.
A instância de `Person` agora tem uma strong reference para a instância de `Apartment`,
e a instância de `Apartment` tem uma strong reference para a instância de `Person`.
Por isso, quando você quebra as strong references mantidas pelas variáveis `john` e `unit4A`,
as contagens de referência não chegam a zero,
e o ARC não desaloca as instâncias:

```swift
john = nil
unit4A = nil
```

<!--
  - test: `referenceCycles`

  ```swifttest
  -> john = nil
  -> unit4A = nil
  ```
-->

Observe que nenhum dos desinicializadores foi chamado
quando você definiu essas duas variáveis como `nil`.
O ciclo de strong reference impede que as instâncias de `Person` e `Apartment`
nunca sejam desalocadas, o que causa um vazamento de memória no seu app.

Veja como ficam as strong references depois que você define
as variáveis `john` e `unit4A` como `nil`:

![](referenceCycle03)

As strong references entre a instância de `Person` e a instância de `Apartment`
permanecem e não podem ser quebradas.

## Resolvendo ciclos de strong reference entre instâncias de classe

O Swift oferece duas formas de resolver ciclos de strong reference
quando você trabalha com propriedades de tipo classe:
referências weak e referências unowned.

Referências weak e unowned permitem que uma instância em um ciclo de strong reference
se refira à outra instância *sem* manter um vínculo forte com ela.
As instâncias podem então se referir uma à outra
sem criar um ciclo de strong reference.

Use uma referência weak quando a outra instância tiver um tempo de vida mais curto,
ou seja, quando a outra instância puder ser desalocada primeiro.
No exemplo de `Apartment` acima,
é apropriado que um apartamento possa ficar sem inquilino em algum momento do seu tempo de vida,
então uma referência weak é uma forma adequada de quebrar o ciclo nesse caso.
Já uma referência unowned é indicada quando a outra instância
tem o mesmo tempo de vida ou um tempo de vida maior.

<!--
  QUESTION: how do I answer the question
  "which of the two properties in the reference cycle
  should be marked as weak or unowned?"
-->

### Referências weak

Uma *referência weak* é uma referência que não mantém uma strong reference
sobre a instância a que se refere,
e por isso não impede o ARC de desalocar a instância referenciada.
Esse comportamento impede que a referência faça parte de um ciclo de strong reference.
Você indica uma referência weak colocando a palavra-chave `weak`
antes da declaração de uma propriedade ou variável.

Como uma referência weak não mantém uma strong reference sobre a instância a que se refere,
é possível que essa instância seja desalocada
enquanto a referência weak ainda aponta para ela.
Por isso, o ARC define automaticamente uma referência weak como `nil`
quando a instância a que ela se refere é desalocada.
E, como as referências weak precisam permitir que o valor seja alterado para `nil` em tempo de execução,
elas são sempre declaradas como variáveis, e não como constantes, de um tipo optional.

Você pode verificar a existência de um valor na referência weak,
como faria com qualquer outro valor optional,
e nunca terá uma referência a uma instância inválida que não existe mais.

> Nota: Observadores de propriedade não são chamados
> quando o ARC define uma referência weak como `nil`.

<!--
  - test: `weak-reference-doesnt-trigger-didset`

  ```swifttest
  -> class C {
         weak var w: C? { didSet { print("did set") } }
     }
  -> var c1 = C()
  -> do {
  ->     let c2 = C()
  ->     assert(c1.w == nil)
  ->     c1.w = c2
  << did set
  ->     assert(c1.w != nil)
  -> } // ARC deallocates c2; didSet doesn't fire.
  -> assert(c1.w == nil)
  ```
-->

O exemplo a seguir é idêntico ao exemplo de `Person` e `Apartment` acima,
com uma diferença importante.
Desta vez, a propriedade `tenant` do tipo `Apartment`
é declarada como uma referência weak:

```swift
class Person {
    let name: String
    init(name: String) { self.name = name }
    var apartment: Apartment?
    deinit { print("\(name) is being deinitialized") }
}

class Apartment {
    let unit: String
    init(unit: String) { self.unit = unit }
    weak var tenant: Person?
    deinit { print("Apartment \(unit) is being deinitialized") }
}
```

<!--
  - test: `weakReferences`

  ```swifttest
  -> class Person {
        let name: String
        init(name: String) { self.name = name }
        var apartment: Apartment?
        deinit { print("\(name) is being deinitialized") }
     }

  -> class Apartment {
        let unit: String
        init(unit: String) { self.unit = unit }
        weak var tenant: Person?
        deinit { print("Apartment \(unit) is being deinitialized") }
     }
  ```
-->

As strong references das duas variáveis (`john` e `unit4A`)
e as conexões entre as duas instâncias são criadas como antes:

```swift
var john: Person?
var unit4A: Apartment?

john = Person(name: "John Appleseed")
unit4A = Apartment(unit: "4A")

john!.apartment = unit4A
unit4A!.tenant = john
```

<!--
  - test: `weakReferences`

  ```swifttest
  -> var john: Person?
  -> var unit4A: Apartment?

  -> john = Person(name: "John Appleseed")
  -> unit4A = Apartment(unit: "4A")

  -> john!.apartment = unit4A
  -> unit4A!.tenant = john
  ```
-->

Veja como ficam as referências agora que você conectou as duas instâncias:

![](weakReference01)

A instância de `Person` ainda tem uma strong reference para a instância de `Apartment`,
mas a instância de `Apartment` agora tem uma referência *weak* para a instância de `Person`.
Isso significa que, quando você quebra a strong reference mantida pela variável `john`
ao defini-la como `nil`, não há mais strong references para a instância de `Person`:

```swift
john = nil
// Prints "John Appleseed is being deinitialized".
```

<!--
  - test: `weakReferences`

  ```swifttest
  -> john = nil
  <- John Appleseed is being deinitialized
  ```
-->

Como não há mais strong references para a instância de `Person`,
ela é desalocada e a propriedade `tenant` é definida como `nil`:

![](weakReference02)

A única strong reference restante para a instância de `Apartment`
vem da variável `unit4A`.
Se você quebrar *essa* strong reference,
não há mais strong references para a instância de `Apartment`:

```swift
unit4A = nil
// Prints "Apartment 4A is being deinitialized".
```

<!--
  - test: `weakReferences`

  ```swifttest
  -> unit4A = nil
  <- Apartment 4A is being deinitialized
  ```
-->

Como não há mais strong references para a instância de `Apartment`,
ela também é desalocada:

![](weakReference03)

> Nota: Em sistemas que usam coleta de lixo,
> ponteiros weak às vezes são usados para implementar um mecanismo de cache simples,
> porque objetos sem strong references só são desalocados
> quando a pressão de memória dispara a coleta de lixo.
> No entanto, com o ARC, os valores são desalocados
> assim que a última strong reference é removida,
> o que torna as referências weak inadequadas para essa finalidade.

### Referências unowned

Assim como uma referência weak, uma *referência unowned*
não mantém uma strong reference sobre a instância a que se refere.
Diferente da referência weak, porém,
uma referência unowned é usada quando a outra instância
tem o mesmo tempo de vida ou um tempo de vida maior.
Você indica uma referência unowned colocando a palavra-chave `unowned`
antes da declaração de uma propriedade ou variável.

Diferente de uma referência weak,
uma referência unowned deve sempre ter um valor.
Por isso, marcar um valor como unowned não o torna optional,
e o ARC nunca define o valor de uma referência unowned como `nil`.

<!--
  Everything that unowned can do, weak can do slower and more awkwardly
  (but still correctly).
  Unowned is interesting because it's faster and easier (no optionals) ---
  in the cases where it's actually correct for your data.
-->

> Importante: Use uma referência unowned apenas quando tiver certeza de que
> a referência *sempre* se refere a uma instância que não foi desalocada.
>
> Se você tentar acessar o valor de uma referência unowned
> depois que essa instância foi desalocada,
> você vai receber um erro de tempo de execução.

<!--
  One way to satisfy that requirement is to
  always access objects that have unmanaged properties through their owner
  instead of keeping a reference to them directly,
  because those direct references could outlive the owner.
  However... this strategy really only works when the unowned reference
  is a backpointer from an object up to its owner.
-->

O exemplo a seguir define duas classes, `Customer` e `CreditCard`,
que modelam um cliente de banco e um possível cartão de crédito desse cliente.
Essas duas classes armazenam uma instância da outra como propriedade.
Essa relação tem potencial para criar um ciclo de strong reference.

A relação entre `Customer` e `CreditCard` é um pouco diferente
da relação entre `Apartment` e `Person`
vista no exemplo de referência weak acima.
Nesse modelo de dados, um cliente pode ter ou não um cartão de crédito,
mas um cartão de crédito sempre estará associado a um cliente.
Uma instância de `CreditCard` nunca sobrevive ao `Customer` a que se refere.
Para representar isso, a classe `Customer` tem uma propriedade `card` optional,
mas a classe `CreditCard` tem uma propriedade `customer` unowned e não optional.

Além disso, uma nova instância de `CreditCard` só pode ser criada
passando um valor `number` e uma instância de `customer`
para um inicializador personalizado de `CreditCard`.
Isso garante que uma instância de `CreditCard` sempre tenha
uma instância de `customer` associada no momento da criação.

Como um cartão de crédito sempre terá um cliente,
você define a propriedade `customer` como uma referência unowned,
para evitar um ciclo de strong reference:

```swift
class Customer {
    let name: String
    var card: CreditCard?
    init(name: String) {
        self.name = name
    }
    deinit { print("\(name) is being deinitialized") }
}

class CreditCard {
    let number: UInt64
    unowned let customer: Customer
    init(number: UInt64, customer: Customer) {
        self.number = number
        self.customer = customer
    }
    deinit { print("Card #\(number) is being deinitialized") }
}
```

<!--
  - test: `unownedReferences`

  ```swifttest
  -> class Customer {
        let name: String
        var card: CreditCard?
        init(name: String) {
           self.name = name
        }
        deinit { print("\(name) is being deinitialized") }
     }

  -> class CreditCard {
        let number: UInt64
        unowned let customer: Customer
        init(number: UInt64, customer: Customer) {
           self.number = number
           self.customer = customer
        }
        deinit { print("Card #\(number) is being deinitialized") }
     }
  ```
-->

> Nota: A propriedade `number` da classe `CreditCard` é definida
> com o tipo `UInt64` em vez de `Int`,
> para garantir que a capacidade da propriedade `number` seja grande o bastante
> para armazenar um número de cartão de 16 dígitos
> tanto em sistemas de 32 bits quanto de 64 bits.

Este próximo trecho de código define uma variável `Customer` optional chamada `john`,
que será usada para armazenar uma referência a um cliente específico.
Essa variável tem valor inicial `nil`, por ser optional:

```swift
var john: Customer?
```

<!--
  - test: `unownedReferences`

  ```swifttest
  -> var john: Customer?
  ```
-->

Agora você pode criar uma instância de `Customer`
e usá-la para inicializar e atribuir uma nova instância de `CreditCard`
como a propriedade `card` desse cliente:

```swift
john = Customer(name: "John Appleseed")
john!.card = CreditCard(number: 1234_5678_9012_3456, customer: john!)
```

<!--
  - test: `unownedReferences`

  ```swifttest
  -> john = Customer(name: "John Appleseed")
  -> john!.card = CreditCard(number: 1234_5678_9012_3456, customer: john!)
  ```
-->

Veja como ficam as referências agora que você conectou as duas instâncias:

![](unownedReference01)

A instância de `Customer` agora tem uma strong reference para a instância de `CreditCard`,
e a instância de `CreditCard` tem uma referência unowned para a instância de `Customer`.

Por causa da referência unowned `customer`,
quando você quebra a strong reference mantida pela variável `john`,
não há mais strong references para a instância de `Customer`:

![](unownedReference02)

Como não há mais strong references para a instância de `Customer`, ela é desalocada.
Depois disso, não há mais strong references para a instância de `CreditCard`,
que também é desalocada:

```swift
john = nil
// Prints "John Appleseed is being deinitialized".
// Prints "Card #1234567890123456 is being deinitialized".
```

<!--
  - test: `unownedReferences`

  ```swifttest
  -> john = nil
  <- John Appleseed is being deinitialized
  <- Card #1234567890123456 is being deinitialized
  ```
-->

O último trecho de código acima mostra que
os desinicializadores da instância de `Customer` e da instância de `CreditCard`
imprimem suas mensagens de “deinitialized” depois que a variável `john` é definida como `nil`.

> Nota: Os exemplos acima mostram como usar unowned references *seguras*.
> O Swift também oferece unowned references *inseguras* para casos em que
> você precisa desativar as verificações de segurança em tempo de execução,
> por exemplo, por motivos de desempenho.
> Como em todas as operações inseguras, você assume a responsabilidade
> de verificar a segurança desse código.
>
> Você indica uma unowned reference insegura escrevendo `unowned(unsafe)`.
> Se você tentar acessar uma unowned reference insegura
> depois que a instância a que ela se refere foi desalocada,
> seu programa vai tentar acessar a posição de memória
> onde a instância estava, o que é uma operação insegura.

<!--
  <rdar://problem/28805121> TSPL: ARC - Add discussion of "unowned" with different lifetimes
  Try expanding the example above so each customer has an array of credit cards.
-->

### Referências unowned optional

Você pode marcar uma referência optional a uma classe como unowned.
No modelo de posse do ARC, uma referência unowned optional e uma referência weak
podem ser usadas nos mesmos contextos.
A diferença é que, ao usar uma referência unowned optional,
você é responsável por garantir que ela sempre se refira a um objeto válido
ou seja definida como `nil`.

Aqui está um exemplo que acompanha os cursos oferecidos
por um departamento de uma escola:

```swift
class Department {
    var name: String
    var courses: [Course]
    init(name: String) {
        self.name = name
        self.courses = []
    }
}

class Course {
    var name: String
    unowned var department: Department
    unowned var nextCourse: Course?
    init(name: String, in department: Department) {
        self.name = name
        self.department = department
        self.nextCourse = nil
    }
}
```

<!--
  - test: `unowned-optional-references`

  ```swifttest
  -> class Department {
         var name: String
         var courses: [Course]
         init(name: String) {
             self.name = name
             self.courses = []
         }
     }

  -> class Course {
         var name: String
         unowned var department: Department
         unowned var nextCourse: Course?
         init(name: String, in department: Department) {
             self.name = name
             self.department = department
             self.nextCourse = nil
         }
     }
  ```
-->

`Department` mantém uma strong reference para cada curso que o departamento oferece.
No modelo de posse do ARC, um departamento é dono dos seus cursos.
`Course` tem duas referências unowned,
uma para o departamento e outra para o próximo curso que um aluno deve fazer;
um curso não é dono de nenhum desses objetos.
Todo curso faz parte de algum departamento,
então a propriedade `department` não é optional.
No entanto, como alguns cursos não têm um curso seguinte recomendado,
a propriedade `nextCourse` é optional.

Veja um exemplo de uso dessas classes:

```swift
let department = Department(name: "Horticulture")

let intro = Course(name: "Survey of Plants", in: department)
let intermediate = Course(name: "Growing Common Herbs", in: department)
let advanced = Course(name: "Caring for Tropical Plants", in: department)

intro.nextCourse = intermediate
intermediate.nextCourse = advanced
department.courses = [intro, intermediate, advanced]
```

<!--
  - test: `unowned-optional-references`

  ```swifttest
  -> let department = Department(name: "Horticulture")

  -> let intro = Course(name: "Survey of Plants", in: department)
  -> let intermediate = Course(name: "Growing Common Herbs", in: department)
  -> let advanced = Course(name: "Caring for Tropical Plants", in: department)

  -> intro.nextCourse = intermediate
  -> intermediate.nextCourse = advanced
  -> department.courses = [intro, intermediate, advanced]
  ```
-->

O código acima cria um departamento e seus três cursos.
Os cursos introdutório e intermediário têm um próximo curso sugerido
armazenado na propriedade `nextCourse`,
que mantém uma referência unowned optional ao curso
que o aluno deve fazer depois de concluir aquele.

![](unownedOptionalReference)

Uma referência unowned optional não mantém uma strong reference
sobre a instância da classe que ela envolve,
e por isso não impede o ARC de desalocar a instância.
Ela se comporta da mesma forma que uma referência unowned se comporta sob o ARC,
com a diferença de que uma referência unowned optional pode ser `nil`.

Assim como nas referências unowned não optional,
você é responsável por garantir que `nextCourse`
sempre se refira a um curso que ainda não foi desalocado.
Neste caso, por exemplo, quando você remove um curso de `department.courses`,
também precisa remover quaisquer referências a ele
que outros cursos possam ter.

> Nota: O tipo subjacente de um valor optional é `Optional`,
> que é um enum da biblioteca padrão do Swift.
> No entanto, optionals são uma exceção à regra de que
> tipos de valor não podem ser marcados com `unowned`.
>
> O optional que envolve a classe
> não usa contagem de referências,
> então você não precisa manter uma strong reference para o optional.

<!--
  - test: `unowned-can-be-optional`

  ```swifttest
  >> class C { var x = 100 }
  >> class D {
  >>     unowned var a: C
  >>     unowned var b: C?
  >>     init(value: C) {
  >>         self.a = value
  >>         self.b = value
  >>     }
  >> }
  >> var c = C() as C?
  >> let d = D(value: c! )
  >> print(d.a.x, d.b?.x as Any)
  << 100 Optional(100)

  >> c = nil
  // Now that the C instance is deallocated, access to d.a is an error.
  // We manually nil out d.b, which is safe because d.b is an Optional and the
  // enum stays in memory regardless of ARC deallocating the C instance.
  >> d.b = nil
  >> print(d.b?.x as Any)
  << nil
  ```
-->

### Referências unowned e propriedades optional com unwrap implícito

Os exemplos de referências weak e unowned acima
cobrem dois dos cenários mais comuns
em que é necessário quebrar um ciclo de strong reference.

O exemplo de `Person` e `Apartment` mostra uma situação
em que duas propriedades, ambas com permissão de ser `nil`,
têm potencial para causar um ciclo de strong reference.
Esse cenário é mais bem resolvido com uma referência weak.

O exemplo de `Customer` e `CreditCard` mostra uma situação
em que uma propriedade que pode ser `nil`
e outra que não pode ser `nil`
têm potencial para causar um ciclo de strong reference.
Esse cenário é mais bem resolvido com uma referência unowned.

Existe, porém, um terceiro cenário,
em que *as duas* propriedades devem sempre ter um valor,
e nenhuma delas deve ser `nil` depois que a inicialização termina.
Nesse cenário, é útil combinar uma propriedade unowned em uma classe
com uma propriedade optional com unwrap implícito na outra classe.

Isso permite que as duas propriedades sejam acessadas diretamente
(sem fazer unwrap do optional) depois que a inicialização termina,
ao mesmo tempo em que evita um ciclo de strong reference.
Esta seção mostra como configurar esse relacionamento.

O exemplo a seguir define duas classes, `Country` e `City`,
cada uma armazenando uma instância da outra como propriedade.
Nesse modelo de dados, todo país precisa ter sempre uma capital,
e toda cidade precisa sempre pertencer a um país.
Para representar isso, a classe `Country` tem uma propriedade `capitalCity`,
e a classe `City` tem uma propriedade `country`:

```swift
class Country {
    let name: String
    var capitalCity: City!
    init(name: String, capitalName: String) {
        self.name = name
        self.capitalCity = City(name: capitalName, country: self)
    }
}

class City {
    let name: String
    unowned let country: Country
    init(name: String, country: Country) {
        self.name = name
        self.country = country
    }
}
```

<!--
  - test: `implicitlyUnwrappedOptionals`

  ```swifttest
  -> class Country {
        let name: String
        var capitalCity: City!
        init(name: String, capitalName: String) {
           self.name = name
           self.capitalCity = City(name: capitalName, country: self)
        }
     }

  -> class City {
        let name: String
        unowned let country: Country
        init(name: String, country: Country) {
           self.name = name
           self.country = country
        }
     }
  ```
-->

Para configurar a interdependência entre as duas classes,
o inicializador de `City` recebe uma instância de `Country`
e armazena essa instância na propriedade `country`.

O inicializador de `City` é chamado de dentro do inicializador de `Country`.
No entanto, o inicializador de `Country` não pode passar `self` para o inicializador de `City`
até que uma nova instância de `Country` esteja totalmente inicializada,
como descrito em <doc:Initialization#Two-Phase-Initialization>.

Para lidar com esse requisito, você declara a propriedade `capitalCity` de `Country`
como uma propriedade optional com unwrap implícito,
indicada pelo ponto de exclamação no fim da anotação de tipo (`City!`).
Isso significa que a propriedade `capitalCity` tem valor padrão `nil`,
como qualquer outro optional,
mas pode ser acessada sem a necessidade de fazer unwrap do valor,
como descrito em <doc:TheBasics#Implicitly-Unwrapped-Optionals>.

Como `capitalCity` tem valor padrão `nil`,
uma nova instância de `Country` é considerada totalmente inicializada
assim que define sua propriedade `name` dentro do inicializador.
Isso significa que o inicializador de `Country` pode começar a referenciar
e passar a propriedade `self` implícita assim que `name` é definida.
Por isso, o inicializador de `Country` pode passar `self`
como um dos parâmetros do inicializador de `City`
enquanto define a própria propriedade `capitalCity`.

Assim, é possível criar as instâncias de `Country` e `City` em uma única instrução,
sem criar um ciclo de strong reference,
e a propriedade `capitalCity` pode ser acessada diretamente,
sem precisar usar um ponto de exclamação para fazer unwrap do seu valor optional:

```swift
var country = Country(name: "Canada", capitalName: "Ottawa")
print("\(country.name)'s capital city is called \(country.capitalCity.name)")
// Prints "Canada's capital city is called Ottawa".
```

<!--
  - test: `implicitlyUnwrappedOptionals`

  ```swifttest
  -> var country = Country(name: "Canada", capitalName: "Ottawa")
  -> print("\(country.name)'s capital city is called \(country.capitalCity.name)")
  <- Canada's capital city is called Ottawa
  ```
-->

No exemplo acima, o uso de um optional com unwrap implícito
faz com que todos os requisitos do inicializador de classe em duas fases sejam atendidos.
A propriedade `capitalCity` pode ser usada e acessada como um valor não optional
depois que a inicialização termina,
ao mesmo tempo em que evita um ciclo de strong reference.

## Ciclos de strong reference para closures

Você viu acima como um ciclo de strong reference pode ser criado
quando duas propriedades de instâncias de classe mantêm uma strong reference uma para a outra.
Você também viu como usar referências weak e unowned para quebrar esses ciclos.

Um ciclo de strong reference também pode ocorrer
se você atribuir uma closure a uma propriedade de uma instância de classe,
e o corpo dessa closure capturar a instância.
Essa captura pode acontecer porque o corpo da closure acessa uma propriedade da instância,
como `self.someProperty`,
ou porque a closure chama um método da instância,
como `self.someMethod()`.
Em qualquer um dos casos, esses acessos fazem a closure “capturar” `self`,
criando um ciclo de strong reference.

Esse ciclo de strong reference ocorre porque closures, assim como classes,
são *tipos de referência*.
Quando você atribui uma closure a uma propriedade,
está atribuindo uma *referência* a essa closure.
Na essência, é o mesmo problema de antes:
duas strong references que mantêm uma à outra vivas.
No entanto, em vez de duas instâncias de classe,
desta vez são uma instância de classe e uma closure que se mantêm vivas mutuamente.

O Swift oferece uma solução elegante para esse problema,
conhecida como *lista de captura de closure*.
No entanto, antes de aprender a quebrar um ciclo de strong reference com uma lista de captura,
é útil entender como esse ciclo pode ser causado.

O exemplo a seguir mostra como criar um ciclo de strong reference
ao usar uma closure que se refere a `self`.
Este exemplo define uma classe chamada `HTMLElement`,
que fornece um modelo simples para um elemento individual dentro de um documento HTML:

```swift
class HTMLElement {
    let name: String
    let text: String?

    lazy var asHTML: () -> String = {
        if let text = self.text {
            return "<\(self.name)>\(text)</\(self.name)>"
        } else {
            return "<\(self.name) />"
        }
    }

    init(name: String, text: String? = nil) {
        self.name = name
        self.text = text
    }

    deinit {
        print("\(name) is being deinitialized")
    }
}
```

<!--
  - test: `strongReferenceCyclesForClosures`

  ```swifttest
  -> class HTMLElement {
        let name: String
        let text: String?

        lazy var asHTML: () -> String = {
           if let text = self.text {
              return "<\(self.name)>\(text)</\(self.name)>"
           } else {
              return "<\(self.name) />"
           }
        }

        init(name: String, text: String? = nil) {
           self.name = name
           self.text = text
        }

        deinit {
           print("\(name) is being deinitialized")
        }
     }
  ```
-->

A classe `HTMLElement` define uma propriedade `name`,
que indica o nome do elemento,
como `"h1"` para um elemento de título,
`"p"` para um elemento de parágrafo
ou `"br"` para um elemento de quebra de linha.
`HTMLElement` também define uma propriedade `text` optional,
que você pode definir como uma string que representa
o texto a ser renderizado dentro desse elemento HTML.

Além dessas duas propriedades simples,
a classe `HTMLElement` define uma propriedade lazy chamada `asHTML`.
Essa propriedade referencia uma closure que combina `name` e `text`
em um fragmento de string HTML.
A propriedade `asHTML` é do tipo `() -> String`,
ou seja, “uma função que não recebe parâmetros e retorna um valor `String`”.

Por padrão, a propriedade `asHTML` recebe uma closure
que retorna uma representação em string de uma tag HTML.
Essa tag contém o valor optional de `text`, se ele existir,
ou nenhum conteúdo de texto, se `text` não existir.
Para um elemento de parágrafo, a closure retornaria `"<p>some text</p>"` ou `"<p />"`,
dependendo de a propriedade `text` ser igual a `"some text"` ou a `nil`.

A propriedade `asHTML` é nomeada e usada de forma parecida com um método de instância.
No entanto, como `asHTML` é uma propriedade de closure e não um método de instância,
você pode substituir o valor padrão da propriedade `asHTML`
por uma closure personalizada,
se quiser mudar a renderização HTML de um elemento específico.

Por exemplo, a propriedade `asHTML` poderia ser definida com uma closure
que usa algum texto padrão se a propriedade `text` for `nil`,
para evitar que a representação retorne uma tag HTML vazia:

```swift
let heading = HTMLElement(name: "h1")
let defaultText = "some default text"
heading.asHTML = {
    return "<\(heading.name)>\(heading.text ?? defaultText)</\(heading.name)>"
}
print(heading.asHTML())
// Prints "<h1>some default text</h1>".
```

<!--
  - test: `strongReferenceCyclesForClosures`

  ```swifttest
  -> let heading = HTMLElement(name: "h1")
  -> let defaultText = "some default text"
  -> heading.asHTML = {
        return "<\(heading.name)>\(heading.text ?? defaultText)</\(heading.name)>"
     }
  -> print(heading.asHTML())
  <- <h1>some default text</h1>
  ```
-->

> Nota: A propriedade `asHTML` é declarada como lazy
> porque só é necessária se e quando o elemento precisar ser renderizado
> como um valor de string para algum destino de saída HTML.
> Como `asHTML` é uma propriedade lazy,
> você pode se referir a `self` dentro da closure padrão,
> porque a propriedade lazy não é acessada
> até que a inicialização esteja completa e `self` exista.

A classe `HTMLElement` oferece um único inicializador,
que recebe um argumento `name` e, se desejado, um argumento `text`
para inicializar um novo elemento.
A classe também define um desinicializador,
que imprime uma mensagem para mostrar quando uma instância de `HTMLElement` é desalocada.

Veja como usar a classe `HTMLElement` para criar e imprimir uma nova instância:

```swift
var paragraph: HTMLElement? = HTMLElement(name: "p", text: "hello, world")
print(paragraph!.asHTML())
// Prints "<p>hello, world</p>".
```

<!--
  - test: `strongReferenceCyclesForClosures`

  ```swifttest
  -> var paragraph: HTMLElement? = HTMLElement(name: "p", text: "hello, world")
  -> print(paragraph!.asHTML())
  <- <p>hello, world</p>
  ```
-->

> Nota: A variável `paragraph` acima é definida como um `HTMLElement` *optional*,
> para que possa ser definida como `nil` mais adiante
> e demonstrar a presença de um ciclo de strong reference.

Infelizmente, a classe `HTMLElement`, como escrita acima,
cria um ciclo de strong reference entre
uma instância de `HTMLElement` e a closure usada para o valor padrão de `asHTML`.
Veja como fica o ciclo:

![](closureReferenceCycle01)

A propriedade `asHTML` da instância tem uma strong reference para a closure.
No entanto, como a closure se refere a `self` no seu corpo
(para acessar `self.name` e `self.text`),
a closure *captura* `self`,
o que significa que ela mantém uma strong reference de volta para a instância de `HTMLElement`.
Um ciclo de strong reference é criado entre as duas.
(Para mais informações sobre a captura de valores em uma closure,
consulte <doc:Closures#Capturing-Values>.)

> Nota: Mesmo que a closure se refira a `self` várias vezes,
> ela captura apenas uma strong reference para a instância de `HTMLElement`.

Se você definir a variável `paragraph` como `nil`
e quebrar a strong reference para a instância de `HTMLElement`,
o ciclo de strong reference impede a desalocação
tanto da instância de `HTMLElement` quanto da sua closure:

```swift
paragraph = nil
```

<!--
  - test: `strongReferenceCyclesForClosures`

  ```swifttest
  -> paragraph = nil
  ```
-->

Observe que a mensagem do desinicializador de `HTMLElement` não é impressa,
o que mostra que a instância de `HTMLElement` não é desalocada.

## Resolvendo ciclos de strong reference para closures

Você resolve um ciclo de strong reference entre uma closure e uma instância de classe
definindo uma *lista de captura* como parte da definição da closure.
Uma lista de captura define as regras a serem usadas ao capturar
uma ou mais referências a tipos de referência dentro do corpo da closure.
Assim como nos ciclos de strong reference entre duas instâncias de classe,
você declara cada referência capturada como uma referência weak ou unowned,
em vez de uma strong reference.
A escolha entre weak e unowned depende
do relacionamento entre as diferentes partes do seu código.

> Nota: O Swift exige que você escreva `self.someProperty` ou `self.someMethod()`
> (em vez de apenas `someProperty` ou `someMethod()`)
> sempre que se referir a um membro de `self` dentro de uma closure.
> Isso ajuda a lembrar que é possível capturar `self` sem querer.

### Definindo uma lista de captura

Cada item de uma lista de captura é um par formado pela palavra-chave `weak` ou `unowned`
e uma referência a uma instância de classe (como `self`)
ou a uma variável inicializada com algum valor (como `delegate = self.delegate`).
Esses pares são escritos entre colchetes, separados por vírgulas.

Coloque a lista de captura antes da lista de parâmetros e do tipo de retorno da closure,
se eles forem informados:

```swift
lazy var someClosure = {
        [unowned self, weak delegate = self.delegate]
        (index: Int, stringToProcess: String) -> String in
    // closure body goes here
}
```

<!--
  - test: `strongReferenceCyclesForClosures`

  ```swifttest
  >> class SomeClass {
  >> var delegate: AnyObject?
     lazy var someClosure = {
           [unowned self, weak delegate = self.delegate]
           (index: Int, stringToProcess: String) -> String in
        // closure body goes here
  >>    return "foo"
     }
  >> }
  ```
-->

Se uma closure não especificar uma lista de parâmetros nem um tipo de retorno,
porque eles podem ser inferidos pelo contexto,
coloque a lista de captura no início da closure,
seguida da palavra-chave `in`:

```swift
lazy var someClosure = {
        [unowned self, weak delegate = self.delegate] in
    // closure body goes here
}
```

<!--
  - test: `strongReferenceCyclesForClosures`

  ```swifttest
  >> class AnotherClass {
  >> var delegate: AnyObject?
     lazy var someClosure = {
           [unowned self, weak delegate = self.delegate] in
        // closure body goes here
  >>    return "foo"
     }
  >> }
  ```
-->

### Referências weak e unowned

Defina uma captura em uma closure como uma referência unowned
quando a closure e a instância que ela captura sempre se referirem uma à outra,
e sempre forem desalocadas ao mesmo tempo.

Por outro lado, defina uma captura como referência weak
quando a referência capturada puder se tornar `nil` em algum momento no futuro.
Referências weak são sempre de um tipo optional
e se tornam `nil` automaticamente quando a instância a que se referem é desalocada.
Isso permite verificar a existência delas dentro do corpo da closure.

<!--
  <rdar://problem/28812110> Reframe discussion of weak/unowned closure capture in terms of object graph
-->

> Nota: Se a referência capturada nunca vai se tornar `nil`,
> ela deve sempre ser capturada como unowned,
> e não como weak.

Uma unowned reference é a forma de captura apropriada para resolver
o ciclo de strong reference do exemplo `HTMLElement`
de <doc:AutomaticReferenceCounting#Strong-Reference-Cycles-for-Closures> acima.
Veja como escrever a classe `HTMLElement` para evitar o ciclo:

```swift
class HTMLElement {
    let name: String
    let text: String?

    lazy var asHTML: () -> String = {
            [unowned self] in
        if let text = self.text {
            return "<\(self.name)>\(text)</\(self.name)>"
        } else {
            return "<\(self.name) />"
        }
    }

    init(name: String, text: String? = nil) {
        self.name = name
        self.text = text
    }

    deinit {
        print("\(name) is being deinitialized")
    }
}
```

<!--
  - test: `unownedReferencesForClosures`

  ```swifttest
  -> class HTMLElement {
        let name: String
        let text: String?

        lazy var asHTML: () -> String = {
              [unowned self] in
           if let text = self.text {
              return "<\(self.name)>\(text)</\(self.name)>"
           } else {
              return "<\(self.name) />"
           }
        }

        init(name: String, text: String? = nil) {
           self.name = name
           self.text = text
        }

        deinit {
           print("\(name) is being deinitialized")
        }
     }
  ```
-->

Esta implementação de `HTMLElement` é idêntica à anterior,
exceto pela adição de uma lista de captura na closure de `asHTML`.
Nesse caso, a lista de captura é `[unowned self]`,
o que significa “capturar `self` como uma unowned reference
em vez de uma strong reference”.

Você pode criar e imprimir uma instância de `HTMLElement` como antes:

```swift
var paragraph: HTMLElement? = HTMLElement(name: "p", text: "hello, world")
print(paragraph!.asHTML())
// Prints "<p>hello, world</p>".
```

<!--
  - test: `unownedReferencesForClosures`

  ```swifttest
  -> var paragraph: HTMLElement? = HTMLElement(name: "p", text: "hello, world")
  -> print(paragraph!.asHTML())
  <- <p>hello, world</p>
  ```
-->

Veja como ficam as referências com a lista de captura no lugar:

![](closureReferenceCycle02)

Desta vez, a captura de `self` pela closure é uma unowned reference,
e não mantém uma strong reference sobre a instância de `HTMLElement` que ela capturou.
Se você definir a strong reference da variável `paragraph` como `nil`,
a instância de `HTMLElement` é desalocada,
como se vê pela impressão da mensagem do seu desinicializador no exemplo abaixo:

```swift
paragraph = nil
// Prints "p is being deinitialized".
```

<!--
  - test: `unownedReferencesForClosures`

  ```swifttest
  -> paragraph = nil
  <- p is being deinitialized
  ```
-->

Para mais informações sobre listas de captura,
consulte <doc:Expressions#Capture-Lists>.

<!--
This source file is part of the Swift.org open source project

Copyright (c) 2014 - 2022 Apple Inc. and the Swift project authors
Licensed under Apache License v2.0 with Runtime Library Exception

See https://swift.org/LICENSE.txt for license information
See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
-->
<!-- ia-translate: true -->
