# Introdução 

Este tutorial ensina os usuários do FIWARE sobre comandos em lote e relacionamentos entre entidades. O tutorial se baseia nos dados criados no tutorial anterior e cria e associa uma série de entidades de dados relacionadas para criar um sistema simples de gerenciamento de lojas. 

# Requisitos 

>[!info] Antes de começar os tutoriais faça o seguinte:
> - Instale o [Docker, Docker compose](https://www.docker.com/)  e o [Postman](https://www.postman.com/downloads/). 
>- Baixe ou clone o [Repositório do GitHub](https://github.com/rafaelalvesitm/tutoriais-do-fiware).
>- Importe o arquivo `Tutoriais do Fiware.postman_collection.json` para o Postman.
>- Abra o Docker no computador.
>- Abra o Postman Agent no computador. 

# Vídeo do tutorial

# Player

<iframe width="100%" height=100% style="aspect-ratio: 16/9" src="https://www.youtube.com/embed/PnP2NldZPHY" allowfullscreen></iframe>

Caso o player não funcione utilize o link: [Entidades e relacionamentos - Tutoriais do FIWARE #3 - YouTube](https://www.youtube.com/watch?v=PnP2NldZPHY)

# Entendendo Entidades e Relacionamentos

Dentro da plataforma FIWARE, o contexto de uma entidade representa o estado de um objeto físico ou conceitual que existe no mundo real. Para um sistema simples de gerenciamento de lojas, precisaremos apenas de quatro tipos de entidade. O relacionamento entre nossas entidades é definido como mostrado:

![[Fiware tutorials - entity relationship.png]]

- Uma loja é um edifício de tijolos e argamassa do mundo real. As entidades `Store` teriam propriedades como: nome, endereço e local.
- Uma prateleira é um dispositivo do mundo real para guardar objetos que desejamos vender. Cada entidade `shelf` teria propriedades como: nome, capacidade máxima e a loja que possui a estante.
- Um produto é definido como algo que vendemos - é um objeto conceitual. As entidades `product` teriam propriedades como: nome, preço e tamanho.
- Um item de estoque é outra entidade conceitual, utilizada para associar produtos, lojas, prateleiras e objetos físicos. As entidades `inventory Item` teriam propriedades como: 
	- Uma relação com o produto que está sendo vendido 
	- Uma relação com a loja na qual o produto está sendo vendido 
	- Uma relação com a prateleira onde o produto está sendo exibido 
	- Uma contagem de estoque de a quantidade do produto disponível no armazém 
	- Uma contagem de estoque da quantidade do produto disponível na prateleira

Como você pode ver, cada uma das entidades definidas acima contém algumas propriedades que podem ser alteradas. Um produto pode alterar seu preço, o estoque pode ser vendido e a contagem de estoque pode ser reduzida e assim por diante.

# Arquitetura

Nosso aplicativo de demonstração usará apenas um componente do FIWARE: o [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/). Atualmente, o **Orion Context Broker** conta com a tecnologia de código aberto [MongoDB](https://www.mongodb.com/) para manter a persistência dos dados de contexto que ele contém. Portanto, a arquitetura consistirá em dois elementos:

- O [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) que receberá solicitações usando o protocolo [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ ngsiv2).
- O banco de dados [MongoDB](https://www.mongodb.com/): Usado pelo Orion Context Broker para armazenar informações de dados de contexto, como entidades de dados, assinaturas e registros.

Como todas as interações entre os dois serviços são iniciadas por solicitações HTTP, os serviços podem ser incluídos em contêineres e executados a partir de portas expostas. Isso significa que ao implantar cada componente é importante definir corretamente a rede na qual a solução irá operar (Isso tudo é definido do arquivo **docker-compose.yml** diponibilizado).

![[Introduction to FIWARE - Architecture.png]]

# Iniciando os containers

Baixe o arquivo zip ou clone o repositório disponível em [neste link](https://github.com/rafaelalvesitm/my_fiware_tutorials). Abra um terminal e se mova para a pasta `tutorial2`. Depois disso, todos os serviços podem ser inicializados a partir da linha de comando usando o comando `docker compose` conforme indicado abaixo:

```bash
docker compose up -d
```

> **Observação:** Se você deseja limpar e começar de novo, pode fazê-lo com o seguinte comando:
> `docker compose down` e depois utilizar o comando anterior.

O sinalizador `-d` indica que o Docker deve executar os contêineres no modo `detached`, o que significa que os contêineres serão executados em segundo plano.

> **Observação:** você pode verificar cada contêiner no aplicativo Docker ou no plug-in do Docker dentro do Visual Studio Code. Além disso pode usar o comando `docker compose ps -a` ou `docker ps -a` para listar todos os contêineres e avaliar a situação deles.

> [!info] Caso não tenha feito o tutorial anterior, envie a solicitação `Preparando o tutorial 2`
> Este solicitação cria as duas entidades que representam as lojas a serem utilizadas nestes tutorial. Essas entidades foram criadas no tutorial anterior. 

# Criando e associando entidades de dados

## Criando várias entidades ao mesmo tempo

No tutorial anterior, criamos cada entidade **Store** individualmente. Vamos criar cinco unidades de prateleira ao mesmo tempo. Essa solicitação usa o endpoint de processamento em lote de conveniência para criar cinco entidades de prateleira. O processamento em lote usa o endpoint `/v2/op/update` com uma carga útil com dois atributos - `actionType=APPEND` significa que substituiremos entidades existentes se elas existirem, enquanto o atributo `entities` contém uma matriz de entidades que desejamos atualizar.

Para diferenciar Entidades **shelf** de Entidades **store**, cada prateleira foi atribuída a `type=Shelf`. Propriedades do mundo real, como `name` e `location`, foram adicionadas como propriedades a cada estante.

> [!info] **Envie a solicitação `Criar Prateleiras`**. 
> Essa solicitação cria 5 prateleiras com nomes e capacidades diferentes, mas no mesmo local que `Loja 1` do tutorial anterior. 

Da mesma forma, podemos criar uma série de entidades **product** usando o `type=Product`.

> [!info] **Envie a solicitação `Criar Produtos`.** 
> Esta solicitação cria 5 produtos com nomes, tamanhos e preços diferentes.

Em ambos os casos, codificamos cada entidade `id` de acordo com a [especificação NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.04.01_60/gs_cim009v010401p.pdf) - a proposta é que cada `id` seja um URN siga um formato padrão: `urn:ngsi-ld:<entity-type>:<entity-id>`. Isso significa que cada `id` no sistema será único.

As informações de prateleira podem ser solicitadas fazendo uma solicitação GET no endpoint `/v2/entities`. Por exemplo, para retornar os dados de contexto da entidade **Shelf** com o `id=urn:ngsi-ld:Shelf:unit001`.

> [!info] **Enviar solicitação `Recupere a prateleira 1`**. 
> Esta solicitação recupera as informações da prateleira 1. 

A resposta apresenta as propriedades para essa determinada entidade, conforme apresentado abaixo.

```json
{
    "id": "urn:ngsi-ld:Shelf:unit001",
    "type": "Shelf",
    "location": {
        "type": "Point",
        "coordinates": [
            -46.552501261,
            -23.726831523
        ]
    },
    "maxCapacity": 50,
    "name": "Corner Unit"
}
```

Como você pode ver, existem atualmente três atributos de propriedade adicionais presentes `location`, `maxCapacity` e `name`.

## Criando um relacionamento de um para muitos

Em bancos de dados, as chaves estrangeiras são frequentemente usadas para designar um relacionamento um-para-muitos. Como exemplo, cada prateleira é encontrada em uma única loja e uma única loja pode conter muitas unidades de prateleiras. Para lembrar essas informações, precisamos adicionar um relacionamento de associação semelhante a uma chave estrangeira. O processamento em lote pode ser usado novamente para alterar as entidades **Shelf** existentes para adicionar um atributo `refStore` mantendo o relacionamento com cada loja. De acordo com as Diretrizes de modelos de dados inteligentes sobre [dados vinculados](https://smartdatamodels.org/), quando um atributo de entidade é usado como um link para outras entidades, ele deve ser nomeado com o prefixo `ref` mais o nome do tipo de entidade de destino (vinculado).

O valor do atributo `refStore` corresponde a um URN associado à própria entidade **Store**.

O URN segue um formato padrão: `urn:ngsi-ld:<entity-type>:<entity-id>`

>[!info] **Envie a solicitação "Criar relacionamentos"**. 
>Essa solicitação associa três prateleiras a `urn:ngsi-ld:Store:001` e duas prateleiras a `urn:ngsi-ld:Store:002`.

Agora, quando as informações da prateleira são solicitadas novamente, a resposta foi alterada e inclui uma nova propriedade `refStore`, que foi adicionada na etapa anterior.

>[!info] **Envie a solicitação `Recupere a prateleira 1 novamente`**. 
>Essa solicitação recupera as informações da prateleira 1 armazenadas no **Orion Context Broker**.

Desta vez a resposta tem a propriedade de relacionamento como pode ser visto na resposta abaixo.

```json
{
    "id": "urn:ngsi-ld:Shelf:unit001",
    "type": "Shelf",
    "location": {
        "type": "Point",
        "coordinates": [
            -46.552501261,
            -23.726831523
        ]
    },
    "maxCapacity": 50,
    "name": "Corner Unit",
    "refStore": "urn:ngsi-ld:Store:001"
}
```

## Lendo um relacionamento de chave estrangeira

### Leitura da entidade filha para a entidade pai

Também podemos fazer uma solicitação para recuperar as informações de relacionamento do atributo `refStore` de uma entidade **Shelf** conhecida usando a configuração `options=values`

>[!info] **Envie a solicitação `Obter loja de uma prateleira`**. 
>Esta solicitação avalia qual loja está relacionada a prateleira 1. Para isso, é necessário saber qual é  o `ID` da entidade `shelf` e o nome do parâmetro de relação que por padrão é no formato `ref<entity type>`.

Desta vez a requisição tem os seguintes parâmetros:
- `options=values` - Resulta apenas o valor do atributo dado que queremos encontrar.
- `type=Shelf` - garante que estamos obtendo uma entidade com o tipo `Shelf`.
- `attrs=refStore` - obtém o atributo com o nome `refStore`.

A resposta é dada abaixo.

```json
[
    "urn:ngsi-ld:Store:001"
]
```

A requisição pode ser interpretada como "Qual é a loja que está relacionada a prateleira que tem ID `urn:ngsi-ld:Shelf:unit001`". A resposta pode ser interpretada como "esta prateleira está relacionada a loja com o `id=urn:ngsi-ld:Store:001`".

### Leitura da entidade pai para a entidade filha

A leitura de um pai para um filho pode ser feita usando a configuração `options=count`.

>[!info] **Envie a solicitação "Obter prateleiras de uma loja"**. 
>Esta solicitação está solicitando o `id` de todas as entidades **Shelf** associadas ao URN `urn:ngsi-ld:Store:001`. 

Desta vez a requisição tem os seguintes parâmetros:
- `options=count` - resulta em toda a entidade que corresponde à consulta.
- `type=Shelf` - Garante que estamos obtendo entidades com o tipo `Shelf`.
- `attrs=type` - Retorna apenas o atributo `type` (o id é retornado como padrão). Pode incluir outros atributos como `name` e `maxCapacity`.
- `q=refStore==urn:ngsi-ld:Store:001` - Consulta todas as entidades para ver qual tem um atributo com o nome `refStore` e que o valor é `urn:ngsi-ld:Store:001`

A resposta é uma lista de todas as prateleiras relacionadas à Loja 1 como apresentado a seguir:

```json
[
    {
        "id": "urn:ngsi-ld:Shelf:unit001",
        "type": "Shelf"
    },
    {
        "id": "urn:ngsi-ld:Shelf:unit002",
        "type": "Shelf"
    },
    {
        "id": "urn:ngsi-ld:Shelf:unit003",
        "type": "Shelf"
    }
]
```

Essa resposta pode ser interpretada como "Existem três prateleiras em `urn:ngsi-ld:Store:001`". A solicitação pode ser alterada usando os parâmetros `options=values` e `attrs` para retornar propriedades específicas das entidades associadas relevantes. Por exemplo o pedido:

>[!info] **Envie a solicitação `Obter nomes de prateleiras da loja`**.

Desta vez a requisição tem os seguintes parâmetros:
- `options=values` - Retorna os valores das propriedades.
- `type=Shelf` - Garante que estamos obtendo entidades com o tipo `Shelf`.
- `attrs=name` - Retorna apenas o atributo `name`.
- `q=refStore==urn:ngsi-ld:Store:001` - Consulta todas as entidades para ver qual tem um atributo com o nome `refStore` e que o valor é `urn:ngsi-ld:Store:001`

Esta solicitação pode ser interpretada como: _Dê-me os nomes de todas as prateleiras em `urn:ngsi-ld:Store:001`_.

```json
[
    [
        "Corner Unit"
    ],
    [
        "Wall Unit 1"
    ],
    [
        "Wall Unit 2"
    ]
]
```

## Criando relacionamentos muitos-para-muitos

As tabelas de ponte são frequentemente usadas para relacionar relacionamentos muitos-para-muitos. Por exemplo, cada loja venderá uma gama diferente de produtos e cada produto é vendido em muitas lojas.

Para manter as informações de contexto para "colocar um produto em uma prateleira em uma determinada loja", precisaremos criar uma nova entidade de dados `InventoryItem` que existe para associar dados de outras entidades. Ele tem um relacionamento de chave estrangeira com as entidades `Store`, `Shelf` e `Product` e, portanto, requer atributos de relacionamento chamados `refStore`, `refShelf` e `refProduct`.

A atribuição de um produto a uma prateleira é feita simplesmente criando uma entidade que contém as informações de relacionamento e quaisquer outras propriedades adicionais (como `stockCount` e `shelfCount`)

>[!info] **Envie a solicitação `Criar item de inventário`**. 
>Essa solicitação cria um Item de Estoque com relacionamentos com o Sore 1, a Prateleira 1 e o Produto 1. Também indica que a contagem de estoque é 1000 e a contagem da prateleira é 50.

## Lendo de uma tabela de ponte

Ao ler de uma entidade de tabela de ponte, o `tipo` da entidade deve ser conhecido.

>[!info] **Envie a solicitação `Obter produtos vendidos em uma loja`**. 
>Esta solicitação lê  as entidades de item de inventário que estão relacionadas a loja 1, retornando quais produtos pertencem a este item de inventário. 

Esta solicitação tem os seguintes parâmetros:
- `options=values` - Retorna os valores das propriedades.
- `type=InventoryItem` - Garante que estamos obtendo entidades com o tipo `InventoryItem`.
- `attrs=refProduct` - Retorna apenas o atributo `refProduct`.
- `q=refStore==urn:ngsi-ld:Store:001` - Consulta todas as entidades para ver qual tem um atributo com o nome `refStore` e que o valor é `urn:ngsi-ld:Store:001`

Esta solicitação representa a seguinte consulta: _Quais produtos são vendidos em `urn:ngsi-ld:Store:001`?_ . A resposta está indicada abaixo

```json
[
    [
        "urn:ngsi-ld:Product:001"
    ]
]
```

Da mesma forma, podemos solicitar "Quais lojas estão vendendo o produto `urn:ngsi-ld:Produto:001`?" alterando a solicitação.

>[!info] **Envie a solicitação `Obter lojas vendendo um produto`**. 
>Esta solicitação lê  as entidades de item de inventário que estão relacionadas ao produto 1, retornando quais lojas pertencem a este item de inventário. 

Os seguintes parâmetros são usados nesta solicitação:
- `options=values` - Retorna os valores das propriedades.
- `type=InventoryItem` - Garante que estamos obtendo entidades com o tipo `InventoryItem`.
- `attrs=refStore` - Retorna apenas o atributo `refStore`.
- `q=refProduct==urn:ngsi-ld:Product:001` - Consulta todas as entidades para ver qual tem um atributo com o nome `refProduct` e que o valor é `urn:ngsi-ld:Product:001`

```json
[
    [
        "urn:ngsi-ld:Store:001"
    ]
]
```

## Integridade de dados

Os relacionamentos de dados de contexto só devem ser configurados e mantidos entre entidades existentes - em outras palavras, o URN `urn:ngsi-ld:<entity-type>:<entity-id>` deve ser vinculado a outra entidade existente dentro do contexto. Portanto, devemos tomar cuidado ao excluir uma entidade para que nenhuma referência pendente permaneça. Imagine que `urn:ngsi-ld:Store:001` seja excluído - o que deve acontecer com as entidades **Shelf** associadas?

>[!info] **Envie a solicitação `Obter entidades restantes`**. 
>Esta solicitação verifica quais as entidades estão relacionadas a determinada loja. 

Os seguintes parâmetros são usados:
- `options=counts` - Retorna o nome das propriedades.
- `attrs=type` - Retorna apenas o atributo `type`.
- `q=refStore==urn:ngsi-ld:Store:001` - Consulta todas as entidades para ver qual tem um atributo com o nome `refStore` e que o valor é `urn:ngsi-ld:Store:001`

A resposta lista uma série de entidades `Shelf` e `InventoryItem` - não há entidades `Product`, pois não há relação direta entre o produto e a loja. A resposta está presente abaixo

```json
[
    {
        "id": "urn:ngsi-ld:Shelf:unit001",
        "type": "Shelf"
    },
    {
        "id": "urn:ngsi-ld:Shelf:unit002",
        "type": "Shelf"
    },
    {
        "id": "urn:ngsi-ld:Shelf:unit003",
        "type": "Shelf"
    },
    {
        "id": "urn:ngsi-ld:InventoryItem:001",
        "type": "InventoryItem"
    }
]
```

> Se esta solicitação retornar uma lista vazia, a entidade não possui associados. Ou seja, pode ser deletado. Se não retornar vazio é necessário remover o relacionamento de todas as entidades da lista antes de deletar esta entidade.

# Conclusão

Este tutorial apresenta a capacidade de gerar relações de entre entidades de context armazenadas no **Orion Context Broker**. Com essas relações é possível realizar buscas mais complexas no gestor de contexto e assim aproximar a modelagem da solução inteligente ao mundo real. 

:: **Referência** :: [Entity Relationships - Step-by-Step for NGSI-v2](https://fiware-tutorials.readthedocs.io/en/latest/entity-relationships.html)