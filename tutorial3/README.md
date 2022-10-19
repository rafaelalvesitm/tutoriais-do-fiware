# Introdução

Este tutorial ensina os usuários do FIWARE sobre as [[Operações CRUD]]. O tutorial baseia-se nos dados criados no tutorial anterior, permitindo que os usuários manipulem os dados mantidos dentro do contexto. Este tutorial foi criado com base no fornecido pela FIWARE em [CRUD Operations - Step-by-Step for NGSI-v2](https://fiware-tutorials.readthedocs.io/en/latest/crud-operations.html)

# Requisitos 

**Antes de prosseguir é recomendado que os usuários sigam os [[Requisitos para acompanhar os tutoriais]].** 

> **Você pode obter todos os arquivos necessários para este tutorial no seguinte link: [Tutoriais no GitHub](https://github.com/rafaelalvesitm/my_fiware_tutorials) e indo para a pasta `tutorial3`. Existe um arquivo `docker-compose.yml` usado para criar o tutorial usando o Docker um arquivo `tutorial3.postman_collection.json` usado para importar as solicitações deste tutorial para o Postman**.

# Entidades

Este tutorial utiliza o mesmo modelo de entidades apresentado no tutorial anterior e exemplificado abaixo. 

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

Baixe o arquivo zip ou clone o repositório disponível em [neste link](https://github.com/rafaelalvesitm/my_fiware_tutorials). Abra um terminal e se mova para a pasta `tutorial3`. Depois disso, todos os serviços podem ser inicializados a partir da linha de comando usando o comando `docker compose` conforme indicado abaixo:

```bash
docker compose up -d
```

> **Observação:** Se você deseja limpar e começar de novo, pode fazê-lo com o seguinte comando:
> `docker compose down` e depois utilizar o comando anterior.

O sinalizador `-d` indica que o Docker deve executar os contêineres no modo `detached`, o que significa que os contêineres serão executados em segundo plano.

> **Observação:** você pode verificar cada contêiner no aplicativo Docker ou no plug-in do Docker dentro do Visual Studio Code. Além disso pode usar o comando `docker compose ps -a` ou `docker ps -a` para listar todos os contêineres e avaliar a situação deles.

> [!info] Caso não tenha feito o tutorial anterior, envie a solicitação `Preparando o tutorial 3`
> Este solicitação cria as entidades criadas no tutorial anterior. 

# O que é CRUD?

**Criar**, **Ler**, **Atualizar** e **Excluir** são as quatro funções básicas do armazenamento persistente. Essas operações geralmente são referidas pelo acrônimo **CRUD**. Dentro de um banco de dados, cada uma dessas operações é mapeada diretamente para uma série de comandos, porém seu relacionamento com uma API RESTful é um pouco mais complexo.

O [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) usa [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2) para manipular o dados de contexto. Como uma API RESTful, as solicitações para manipular os dados contidos no contexto seguem as convenções padrão encontradas ao mapear verbos HTTP para operações CRUD.

## Operações CRUD da Entidade

Para operações em que o `<id da entidade>` ainda não é conhecido no contexto ou não foi especificado, o endpoint `/v2/entities` é usado. Uma vez que um `<id da entidade>` é conhecido dentro do contexto, as entidades de dados individuais podem ser manipuladas usando o ponto de extremidade `/v2/entities/<id da entidade>`.

Recomenda-se que os identificadores de entidade sejam URNs seguindo a [especificação NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.04.01_60/gs_cim009v010401p.pdf), portanto, cada `id` é um URN que segue um formato padrão: `urn:ngsi-ld:<tipo da entidade>:<id da entidade>`. Isso ajuda a tornar cada `id` nos dados de contexto únicos.

| HTTP Verb | `/v2/entities` | `/v2/entities/<ID da entidade>` |
| --- | --- | --- |
| **POST** | CRIE uma nova entidade e adicione ao contexto. |  CRIA ou ATUALIZA um atributo específico da entidade. |
| **GET** | LÊ os dados de contexto de uma entidade. Retorna os dados de múltiplas entidades. Dados podem ser filtrados. | LÊ os dados de uma entidade específica. Retorna os dados de uma única entidade. Os dados podem ser filtrados. |
| **PUT** | :x: | :x: |
| **PATCH** | :x: | :x: |
| **DELETE** | :x: | DELETA a entidade do contexto |

Uma lista completa de endpoints de entidade pode ser encontrada na [NGSI v2 Swagger Specification](https://fiware.github.io/specifications/OpenAPI/ngsiv2#/Entities).

## Operações CRUD de atributo

Para realizar operações CRUD em atributos, o `<ID da entidade>` deve ser conhecido. Cada atributo é efetivamente um par chave-valor.

Existem três rotas:

- `/v2/entities/<ID da entidade>/attrs` é usado apenas para uma operação de PATCH para atualizar um ou mais atributos existentes.
- `/v2/entities/<ID da entidade>/attrs/<atributo>` é usado para manipular um atributo como um todo.
- `/v2/entities/<ID da entidade>/attrs/<atributo>/value` é usado para ler ou atualizar o `value` de um atributo, deixando o `type` intocado.

| HTTP Verb | `.../attrs` | `.../attrs/<atributo>` | `.../attrs/<atributo>/value` |
| --- | --- | --- | --- |
| **POST** | :x: | :x: | :x: |
| **GET** | :x: | :x: | READ the value of an atributo from a specified entity. This will return a single field. |
| **PUT** | :x: | :x: | UPDATE the value of single atributo from a specified entity. |
| **PATCH** | UPDATE one or more existing atributos from an existing entity. | :x: | :x: |
| **DELETE**. | :x: | DELETE an existing atributo from an existing entity. | :x: |

Uma lista completa de endpoints de atributos pode ser encontrada na [NGSI v2 Swagger Specification](https://fiware.github.io/specifications/OpenAPI/ngsiv2#/atributos)

Além disso, o **Orion Context Broker** possui um endpoint de operação em lote conveniente `/v2/op/update` para manipular várias entidades em uma única operação.

As operações em lote são sempre acionadas por uma solicitação POST em que a carga útil é um objeto com duas propriedades:

- `actionType` especifica o tipo de ação a ser invocada (por exemplo, `delete`)
- `entities` é uma matriz de objetos que contém a lista de entidades a serem atualizadas, juntamente com os dados relevantes da entidade usados para realizar a operação.

# Exemplo de operações CRUD usando FIWARE

## Criar operações

Para criar entidades é necessário utilizar uma requisição POST. Note que:
- O endpoint `/v2/entities` é usado para criar novas entidades
- O ponto de extremidade `/v2/entities/<entity>` é usado para adicionar novos atributos

Qualquer entidade recém-criada deve ter atributos `id` e `type`, outros atributos são opcionais e dependerão do sistema que está sendo modelado. Se atributos adicionais estiverem presentes, cada um deve especificar um `type` e um `value`.

A resposta será **204 - Sem conteúdo** se a operação for bem-sucedida ou **422 - Entidade não processável** se a operação falhar.

### Criar uma nova entidade de dados

>[!info] **Envie a solicitação `Criar um produto`**.
>Este exemplo adiciona uma nova entidade do tipo **Product** ("Limonada" a 99 centavos) ao contexto. 

Novas entidades podem ser adicionadas fazendo uma solicitação POST para o endpoint `/v2/entities`. A solicitação falhará se algum dos atributos já existir no contexto.

>[!info] **Envie a solicitação `Recupere o produto`**. Esta solicitação obtém os dados do produto de criado acima. 

A resposta é vista abaixo:

```json
{
    "id": "urn:ngsi-ld:Product:010",
    "type": "Product",
    "name": {
        "type": "Text",
        "value": "Lemonade",
        "metadata": {}
    },
    "price": {
        "type": "Integer",
        "value": 99,
        "metadata": {}
    },
    "size": {
        "type": "Text",
        "value": "S",
        "metadata": {}
    }
}
```

### Create a New atributo
This example adds a new `specialOffer` atributo to the existing **Product** entity with `id=urn:ngsi-ld:Product:001`.

**Send the `Add a Special offer` request**. This request adds a new atributo to the previous entity.  

New atributos can be added by making a POST request to the `/v2/entities/<entity>/attrs` endpoint.The payload should consist of a JSON object holding the atributo names and values as shown. If no `type` is specified a default type (`Boolean`, `Text` , `Number` or `StructuredValue`) will be assigned. Subsequent requests using the same `id` will update the value of the atributo in the context.

**Send the previous `Get the Product` request**. As you can see there is now a boolean `specialOffer` flag attached to the "Beer" **Product** entity.

### Criar um novo atributo

Este exemplo adiciona um novo atributo `specialOffer` à entidade **Product** existente com `id=urn:ngsi-ld:Product:001`.

>[!info] **Envie a solicitação `Adicionar uma oferta especial`**. 
>Essa solicitação adiciona um novo atributo à entidade anterior.

Novos atributos podem ser adicionados fazendo uma solicitação POST para o ponto de extremidade `/v2/entities/<Id da entidade>/attrs`. A carga útil deve consistir em um objeto JSON que contém os nomes e valores dos atributos, conforme mostrado. Se nenhum `type` for especificado, um tipo padrão (`Boolean`, `Text` , `Number` ou `StructuredValue`) será atribuído. As solicitações subsequentes usando o mesmo `id` atualizarão o valor do atributo no contexto.

>[!info] **Envie a solicitação anterior de `Obter o produto novamente`**. 
>Esta solicitação recupera os dados de contexto do produto 1 com os atributos atualizados. 

Como você pode ver, agora há um sinalizador booleano `specialOffer` anexado à entidade "Cerveja" **Produto**.

### Batch Create New Data Entities or atributos
This example uses the convenience batch processing endpoint to add two new **Product** entities and one new atributo (`offerPrice`) to the context.

**Send the `Create 2 Products with offer price` request**. The request will fail if any of the atributos already exist in the context.

Batch processing uses the `/v2/op/update` endpoint with a payload with two atributos
- `actionType=append_strict` means that the request only succeeds if all entities / atributos are new.
- The `entities` atributo holds an array of entities we wish to create.

Subsequent requests using the same data with the `actionType=append_strict` batch operation will result in an error response.

### Batch Create/Overwrite New Data Entities
This example uses the convenience batch processing endpoint to add or amend two **Product** entities and one atributo (`offerPrice`) to the context.
- if an entity already exists, the request will update that entity's atributos.
- if an entity does not exist, a new entity will be created.

**Send the `Append 2 products` request**. Batch processing uses the `/v2/op/update` endpoint with a payload with two atributos:
- `actionType=append` means we will overwrite existing entities if they exist
- The entities atributo holds an array of entities we wish to create/overwrite.

A subsequent request containing the same data (i.e. same entities and `actionType=append`) won't change the context state.

## Read Operations
- The `/v2/entities` endpoint is used for listing entities
- The `/v2/entities/<entity>` endpoint is used for retrieving the details of a single entity

### Filtering
- The options parameter (combined with the attrs parameter) can be used to filter the returned fields
- The q parameter can be used to filter the returned entities

### Read a Data Entity (verbose)
This example reads the full context from an existing **Product** entity with a known `id`.

**Send the `Get the Product 10` request**. This request gets the entity for the Product 10. The response can be seen below.

### Criar, em lote, novas entidades de dados ou atributos

Este exemplo usa o endpoint de processamento em lote de conveniência para adicionar duas novas entidades **Product** e um novo atributo (`offerPrice`) ao contexto.

>[!info] **Envie a solicitação `Criar 2 produtos com preço de oferta`**. 
>Esta solicitação cria dois produtos já com o preço de oferta atualizado. 

A solicitação falhará se algum dos atributos já existir no contexto.

O processamento em lote usa o endpoint `/v2/op/update` com uma carga útil com dois atributos
- `actionType=append_strict` significa que a solicitação só será bem-sucedida se todas as entidades/atributos forem novos.
- O atributo `entities` contém um array de entidades que desejamos criar.

Solicitações subsequentes usando os mesmos dados com a operação em lote `actionType=append_strict` resultarão em uma resposta de erro.

### Criação/substituição, em lote, de novas entidades de dados

Este exemplo usa o endpoint de processamento em lote de conveniência para adicionar ou alterar duas entidades **Product** e um atributo (`offerPrice`) ao contexto.
- se uma entidade já existir, a solicitação atualizará os atributos dessa entidade.
- se uma entidade não existir, uma nova entidade será criada.

>[!info] **Envie a solicitação `Anexar 2 produtos`**. 
>Esta solicitação atualiza os dois produtos criados anteriormente, adicionando atributos se necessário e mantendo os já existentes. 

O processamento em lote usa o endpoint `/v2/op/update` com um payload com dois atributos:
- `actionType=append` significa que substituiremos as entidades existentes se elas existirem
- O atributo de entidades contém um array de entidades que desejamos criar/substituir.

Uma solicitação subsequente contendo os mesmos dados (ou seja, mesmas entidades e `actionType=append`) não alterará o estado do contexto.

## Operações de leitura
- O endpoint `/v2/entities` é usado para listar entidades
- O endpoint `/v2/entities/<ID da entidade>` é usado para recuperar os detalhes de uma única entidade

### Filtragem
- O parâmetro `options` (combinado com o parâmetro `attrs`) pode ser usado para filtrar os campos retornados
- O parâmetro q pode ser usado para filtrar as entidades retornadas

### Ler uma entidade de dados (verboso)

Este exemplo lê o contexto completo de uma entidade **Product** existente com um `id` conhecido.

>[!info] **Envie a solicitação `Recupere o produto 10`**. 
>Esta solicitação recupera os dados de contexto do produto 10. 

A resposta pode ser vista abaixo:

```json
{
    "id": "urn:ngsi-ld:Product:010",
    "type": "Product",
    "name": {
        "type": "Text",
        "value": "Lemonade",
        "metadata": {}
    },
    "price": {
        "type": "Integer",
        "value": 99,
        "metadata": {}
    },
    "size": {
        "type": "Text",
        "value": "S",
        "metadata": {}
    },
    "specialOffer": {
        "type": "Boolean",
        "value": true,
        "metadata": {}
    }
}
```

Os dados de contexto podem ser recuperados fazendo uma solicitação GET para o endpoint `/v2/entities/<ID da entidade>`.

### Read an atributo from a Data Entity

This example reads the value of a single atributo (`name`) from an existing **Product** entity with a known `id`.

**Sent the `Get the Product name` request**. This request gets the value of a atribbute called name for a given `product entity`. The response is shown below:

### Ler um atributo de uma entidade de dados

Este exemplo lê o valor de um único atributo (`name`) de uma entidade **Product** existente com um `id` conhecido.

>[!info] **Envie a solicitação `Obter o nome do produto`**. 
>Essa solicitação obtém o valor de um atributo chamado `name` para uma determinada `entidade do produto`. 

A resposta é mostrada abaixo:

```json
"Lemonade"
```

Os dados de contexto podem ser recuperados fazendo uma solicitação GET para o endpoint `/v2/entities/<ID da entidade>/attrs/<nome do atributo>/value`.

### Read a Data Entity (key-value pairs)

This example reads the key-value pairs of two atributos (`name` and `price`) from the context of existing **Product** entities with a known `id`.

**Send the `Get product summary` request**. This request has the following parameters:
- `type=Product` - Returns a Product type entity
- `options=keyValues` - Returns only the name and value of a property (without metadata). 
- `attrs=name,price` - Returns only the name and price atributos for a given entity. 

The response is shown below:

### Ler uma entidade de dados (pares chave-valor)

Este exemplo lê os pares chave-valor de dois atributos (`name` e `price`) do contexto de entidades **Product** existentes com um `id` conhecido.

>[!info] **Envie a solicitação "Obter resumo do produto"**. 
>Esta solicitação obtém o nome e preço do produto

Esta solicitação tem os seguintes parâmetros:
- `type=Product` - Retorna uma entidade do tipo `Product`
- `options=keyValues` - Retorna apenas o nome e o valor de uma propriedade (sem metadados).
- `attrs=name,price` - Retorna apenas os atributos de nome e preço para uma determinada entidade.

A resposta é mostrada abaixo:

```json
{
    "id": "urn:ngsi-ld:Product:010",
    "type": "Product",
    "name": "Lemonade",
    "price": 99
}
```

Combine o parâmetro `options=keyValues` com o parâmetro `attrs` para recuperar pares de valores-chave.

### Ler vários valores de atributos de uma entidade de dados

Este exemplo lê o valor de dois atributos (`name` e `price`) do contexto de entidades **Product** existentes com um ID conhecido.

>![info] **Envie a solicitação `Obter os valores de resumo do produto`**. 
>Esta solicitação obtém os valores dos atributos `name` e `price` de uma entidade do tipo `product`.

Esta solicitação tem os seguintes parâmetros:
- `type=Product` - Retorna uma entidade do tipo Product.
- `options=values` - Retorna apenas o valor dos atributos selecionados.
- `attrs=name,price` - Retorna apenas os atributos de nome e preço para uma determinada entidade.

A resposta é mostrada abaixo:

```json
[
    "Lemonade",
    99
]
```

Combine o parâmetro `options=values` e o parâmetro `attrs` para retornar uma lista de valores em uma matriz.

### Listar todas as entidades de dados (verboso)

Este exemplo lista o contexto completo de todas as entidades **Product**.

>[!info] **Envie a solicitação `Obter todos os produtos`**. 
>Esta solicitação retorna todas as entidades do tipo `Product`.

A resposta pode ser vista abaixo.

```json
[
    {
        "id": "urn:ngsi-ld:Product:010",
        "type": "Product",
        "name": {
            "type": "Text",
            "value": "Lemonade",
            "metadata": {}
        },
        "price": {
            "type": "Integer",
            "value": 99,
            "metadata": {}
        },
        "size": {
            "type": "Text",
            "value": "S",
            "metadata": {}
        },
        "specialOffer": {
            "type": "Boolean",
            "value": true,
            "metadata": {}
        }
    },
    {
        "id": "urn:ngsi-ld:Product:011",
        "type": "Product",
        "name": {
            "type": "Text",
            "value": "Brandy",
            "metadata": {}
        },
        "price": {
            "type": "Integer",
            "value": 1199,
            "metadata": {}
        },
        "size": {
            "type": "Text",
            "value": "M",
            "metadata": {}
        }
    },
    {
        "id": "urn:ngsi-ld:Product:012",
        "type": "Product",
        "name": {
            "type": "Text",
            "value": "Port",
            "metadata": {}
        },
        "price": {
            "type": "Integer",
            "value": 1099,
            "metadata": {}
        },
        "size": {
            "type": "Text",
            "value": "M",
            "metadata": {}
        }
    },
    {
        "id": "urn:ngsi-ld:Product:001",
        "type": "Product",
        "offerPrice": {
            "type": "Integer",
            "value": 89,
            "metadata": {}
        }
    }
]
```

>[!info] **Envie a solicitação "Obter nome e preço de todos os produtos"**. 
>Essa solicitação obtém o nome e o preço de todas as entidades do produto. 

A resposta pode ser vista abaixo:

```json
[
    {
        "id": "urn:ngsi-ld:Product:010",
        "type": "Product",
        "name": "Lemonade"
    },
    {
        "id": "urn:ngsi-ld:Product:011",
        "type": "Product",
        "name": "Brandy"
    },
    {
        "id": "urn:ngsi-ld:Product:012",
        "type": "Product",
        "name": "Port"
    },
    {
        "id": "urn:ngsi-ld:Product:001",
        "type": "Product"
    }
]
```

Dados de contexto completos para um tipo de entidade especificado podem ser recuperados fazendo uma solicitação GET para o endpoint `/v2/entities` e fornecendo o parâmetro `type`, combine isso com o parâmetro `options=keyValues` e o parâmetro `attrs` para recuperar valores-chave.

### Listar entidade de dados por tipo

Este exemplo lista o `id` e o `type` de todas as entidades **Product**.

**Envie a solicitação `Get all Products ID`**. Esta solicitação tem os seguintes parâmetros:
- `type=Product` - Obtém entidades do tipo Product.
- `options=count` - Obtém toda a descrição da entidade.
- `attrs=__NONE` - Não retorna nenhum atributo, exceto para type e id.

```json
[
    {
        "id": "urn:ngsi-ld:Product:010",
        "type": "Product"
    },
    {
        "id": "urn:ngsi-ld:Product:011",
        "type": "Product"
    },
    {
        "id": "urn:ngsi-ld:Product:012",
        "type": "Product"
    },
    {
        "id": "urn:ngsi-ld:Product:001",
        "type": "Product"
    }
]
```

Os dados de contexto para um tipo de entidade especificado podem ser recuperados fazendo uma solicitação GET para o endpoint `/v2/entities` e fornecendo o parâmetro `type`. Combine isso com `options=count` e `attrs=__NONE` para retornar o atributo `id` do `type` fornecido.

> **Observação:** a especificação NGSIv2 especifica que `attrs=` deve ser uma "lista separada por vírgulas de nomes de atributos cujos dados devem ser incluídos na resposta". `id` e `type` não podem ser usados como nomes de atributos. Se você especificar um nome que não existe em atributos, como `__NONE` para o parâmetro `attrs=`, Nenhum atributo corresponderá e você sempre recuperará apenas o `id` e o `type` da entidade.

## Operações de atualização

As operações de substituição são mapeadas para HTTP PUT. HTTP PATCH pode ser usado para atualizar vários atributos de uma só vez.

- O ponto de extremidade `/v2/entities/<ID da entidade>/attrs/<nome do atributo>/value` é usado para atualizar um atributo
- O ponto de extremidade `/v2/entities/<ID da entidade>/attrs` é usado para atualizar vários atributos

### Substituir o valor de um valor de atributo

>[!info] **Envie a solicitação `Atualizar preço do produto 10`**.
> Esta solicitação atualiza o preço do produto de 10 a 89.

Os valores de atributo existentes podem ser alterados fazendo uma solicitação PUT para o ponto de extremidade `/v2/entities/<entity>/attrs/<atributo>/value`.

### Substituir vários atributos de uma entidade de dados

>[!info] **Envie a solicitação `Update multiple atributos`**. 
>Esta solicitação atualiza o preço e o nome ao mesmo tempo.

### Atributos de substituição de lote de várias entidades de dados

>[!info] **Envie a solicitação "Atualizar vários produtos"**. Essa solicitação atualiza várias entidades e atributos de produtos usando o ponto de extremidade `update`. 

O processamento em lote usa o ponto de extremidade `/v2/op/update` com um payload com dois atributos - `actionType=append` significa que substituiremos as entidades existentes se elas existirem, enquanto o atributo `entities` contém uma matriz de entidades que desejamos atualizar.

### Atributos de criação/substituição em lote de várias entidades de dados

>[!info] **Envie a solicitação `Update and create attribute`**. 
>Essa solicitação atualiza os atributos para várias entidades e também cria atributos se estiverem ausentes. 

O processamento em lote usa o ponto de extremidade `/v2/op/update` com um payload com dois atributos - `actionType=append` significa que substituiremos as entidades existentes se elas existirem, enquanto o atributo `entities` contém uma matriz de entidades que desejamos atualizar.

### Dados de entidade de substituição em lote

>[!info] **Envie a solicitação "Substituir produto"**. 
>Essa solicitação **substitui** as informações de contexto de uma determinada entidade. 

Observe que ele substituirá todas as informações de contexto, portanto, use com cuidado. O processamento em lote usa o endpoint `/v2/op/update` com um payload com dois atributos - `actionType=replace` significa que substituiremos as entidades existentes se elas existirem, enquanto o atributo `entities` contém uma matriz de entidades cujos dados desejamos substituir.

## Excluir operações

Para excluir uma entidade ou atributo utiliza-se uma requisição HTTP do tipo DELETE, para as rotas a seguir:
- O endpoint `/v2/entities/<entity>` pode ser usado para excluir uma entidade
- O ponto de extremidade `/v2/entities/<entity>/attrs/<atributo>` pode ser usado para excluir um atributo

A resposta será **204 - Sem conteúdo** se a operação for bem-sucedida ou **404 - Não encontrado** se a operação falhar.

### Relacionamentos de dados

> **Se houver entidades dentro do contexto que se relacionam umas com as outras, você deve ter cuidado ao excluir uma entidade. Você precisará verificar se não há referências deixadas pendentes depois que a entidade for excluída.**

Organizar uma cascata de exclusões está além do escopo deste tutorial, mas seria possível usando uma solicitação de exclusão em lote.

### Excluir uma entidade

>[!info]  **Envie a solicitação "Excluir um produto"**. 
>Essa solicitação excluirá a entidade do Produto 10. 

As entidades podem ser excluídas fazendo uma solicitação DELETE para o endpoint `/v2/entities/<ID da entidade>`. Solicitações subsequentes usando o mesmo `id` resultarão em uma resposta de erro, pois a entidade não existe mais no contexto.

### Excluir um atributo de uma entidade

>[!info] **Envie a solicitação "Excluir um atributo"**. 
>Esta solicitação excluirá apenas o atributo `specialOffer`. 

Atributos podem ser excluídos fazendo uma solicitação DELETE para o ponto de extremidade `/v2/entities/<ID da entidade>/attrs/<nome do atributo>`. Se o atributo não existir no contexto, o resultado será uma resposta de erro.

### Excluir várias entidades em lote

>[!info] **Envie a solicitação `Excluir várias entidades`**. 
>Esta solicitação excluirá as entidades do produto 11 e 12. 

O processamento em lote usa o endpoint `/v2/op/update` com um payload com dois atributos - `actionType=delete` significa que excluiremos algo do contexto e o atributo `entities` contém o `id` das entidades que desejamos excluir. Se uma entidade não existir no contexto, o resultado será uma resposta de erro.

### Excluir vários atributos de uma entidade em lote

>[!info] **Envie a solicitação `Delete multiple atributos`**.
>Essa solicitação exclui vários atributos de várias entidades.

Essa solicitação excluirá atributos da última entidade. O processamento em lote usa o ponto de extremidade `/v2/op/update` com uma carga com dois atributos - `actionType=delete` significa que excluiremos algo do contexto e o atributo `entities` contém uma matriz de atributos que desejamos excluir. Se algum atributo não existir no contexto, o resultado será uma resposta de erro.

# Conclusão

Este tutorial apresenta como utilizar as operações CRUD para criar, ler, atualizar e deletar entidades de contexto no **Orion Context Broker**.

:: **Referência** :: [CRUD Operations - Step-by-Step for NGSI-v2](https://fiware-tutorials.readthedocs.io/en/latest/crud-operations.html)