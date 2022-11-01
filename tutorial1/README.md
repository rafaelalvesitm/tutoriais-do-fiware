# Introdução

Este tutorial fornece ao usuário informações sobre como usar os conceitos básicos do **[Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/)** com o protocolo [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ ngsiv2). Começaremos com os dados de vários edifícios e criaremos um aplicativo _“Powered by FIWARE”_ muito simples, passando o endereço e a localização de cada loja como dados de contexto para o agente de contexto FIWARE.

# Requisitos 

>[!info] Antes de começar os tutoriais faça o seguinte:
> - Instale o [Docker, Docker compose](https://www.docker.com/)  e o [Postman](https://www.postman.com/downloads/). 
>- Baixe ou clone o [Repositório do GitHub](https://github.com/rafaelalvesitm/tutoriais-do-fiware).
>- Importe o arquivo `Tutoriais do Fiware.postman_collection.json` para o Postman.
>- Abra o Docker no computador.
>- Abra o Postman Agent no computador. 

# Vídeo do tutorial

# Player

<iframe width="100%" height=100% style="aspect-ratio: 16/9" src="https://www.youtube.com/embed/PSGLu1eodr4" allowfullscreen></iframe>



# Arquitetura

Nosso aplicativo de demonstração usará apenas um componente do FIWARE: o [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/). Atualmente, o **Orion Context Broker** conta com a tecnologia de código aberto [MongoDB](https://www.mongodb.com/) para manter a persistência dos dados de contexto que ele contém. Portanto, a arquitetura consistirá em dois elementos:

- O [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) que receberá solicitações usando o protocolo [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ ngsiv2).
- O banco de dados [MongoDB](https://www.mongodb.com/): Usado pelo Orion Context Broker para armazenar informações de dados de contexto, como entidades de dados, assinaturas e registros.

Como todas as interações entre os dois serviços são iniciadas por solicitações HTTP, os serviços podem ser incluídos em contêineres e executados a partir de portas expostas. Isso significa que ao implantar cada componente é importante definir corretamente a rede na qual a solução irá operar (Isso tudo é definido do arquivo **docker-compose.yml** diponibilizado).

![[Introduction to FIWARE - Architecture.png]]


# Iniciando os containers

Baixe o arquivo zip ou clone o repositório disponível em [neste link](https://github.com/rafaelalvesitm/my_fiware_tutorials). Abra um terminal e se mova para a pasta `tutorial1`. Depois disso, todos os serviços podem ser inicializados a partir da linha de comando usando o comando `docker compose` conforme indicado abaixo:

```bash
docker compose up -d
```

> **Observação:** Se você deseja limpar e começar de novo, pode fazê-lo com o seguinte comando:
> `docker compose down` e depois utilizar o comando anterior.

O sinalizador `-d` indica que o Docker deve executar os contêineres no modo `detached`, o que significa que os contêineres serão executados em segundo plano.

> **Observação:** você pode verificar cada contêiner no aplicativo Docker ou no plug-in do Docker dentro do Visual Studio Code. Além disso pode usar o comando `docker compose ps -a` ou `docker ps -a` para listar todos os contêineres e avaliar a situação deles.

# Criando seu primeiro aplicativo "Powered by FIWARE"

Após este ponto, utilizaremos o Postman para enviar solicitações HTTP. Para acompanhar este tutorial importe a coleção `tutorial1.postman_collection.json` disponibilizado para a sua área de trabalho do Postman. 

## Verificando a integridade do serviço

Você pode verificar se o **Orion Context Broker** está em execução fazendo uma solicitação GET para a seguinte URL: `http://localhost:1026/version`. 

>[!Info] **Envie a solicitação `Verifique a saúde do Orion`**.
>Esta solicitação recupera as informações do **Orion Context Broker**  caso este esteja funcionando adequadamente.

A resposta será semelhante à seguinte:

```json
{
    "orion": {
        "version": "3.7.0",
        "uptime": "0 d, 0 h, 0 m, 21 s",
        "git_hash": "8b19705a8ec645ba1452cb97847a5615f0b2d3ca",
        "compile_time": "Thu May 26 11:45:49 UTC 2022",
        "compiled_by": "root",
        "compiled_in": "025d96e1419a",
        "release_date": "Thu May 26 11:45:49 UTC 2022",
        "machine": "x86_64",
        "doc": "https://fiware-orion.rtfd.io/en/3.7.0/",
        "libversions": {
            "boost": "1_74",
            "libcurl": "libcurl/7.74.0 OpenSSL/1.1.1n zlib/1.2.11 brotli/1.0.9 libidn2/2.3.0 libpsl/0.21.0 (+libidn2/2.3.0) libssh2/1.9.0 nghttp2/1.43.0 librtmp/2.3",
            "libmosquitto": "2.0.12",
            "libmicrohttpd": "0.9.70",
            "openssl": "1.1",
            "rapidjson": "1.1.0",
            "mongoc": "1.17.4",
            "bson": "1.17.4"
        }
    }
}
```

> **Observação:** **Localhost** refere-se ao dispositivo atual usado para acessá-lo, ou seja, o mesmo dispositivo que está enviando a solicitação. **Os contêineres Postman e Docker devem estar sendo executados na mesma máquina.** Se não estiverem, você precisará alterar **Localhost** para corresponder ao endereço IP onde os contêineres Docker estão localizados.

> **Nota:** Se estiver usando **Windows Subsystem for Linux**, pode ser necessário executar `docker compose up -d` com privilégios de administrador, então use `sudo docker compose up -d`

## Criando dados de contexto

Em sua essência, FIWARE é um sistema para gerenciar informações de contexto, então vamos adicionar alguns dados de contexto ao sistema criando duas novas entidades (lojas no Brasil). Qualquer entidade deve ter atributos `id` e `type`. Atributos adicionais são opcionais e dependerão do sistema que está sendo descrito. Cada atributo adicional também deve ter um atributo `type` e um atributo `value` definidos.

>[!Info] **Envie a solicitação `Criar Loja 1`**
>Esta é uma solicitação `POST` com um corpo JSON descrevendo uma entidade de uma loja.

> Cada entidade deve ter um único `id` para um determinado `type`.

>[!Info] **Envie a solicitação `Criar Loja 2`**. 
>Esta é uma solicitação `POST` com um corpo JSON descrevendo uma entidade de uma loja. 

### Diretrizes do modelo de dados

Embora a entidade de dados em seu contexto varie de acordo com seu caso de uso, a estrutura comum dentro de cada entidade de dados deve ser padronizada para promover a reutilização e interoperabilidade entre sistemas. As diretrizes completas do modelo de dados FIWARE podem ser encontradas [aqui](https://smartdatamodels.org/). Este tutorial demonstra o uso das seguintes recomendações:

- Todos os termos são definidos em inglês americano
	- Embora os campos `value` dos dados de contexto possam estar em qualquer idioma, todos os atributos e tipos são escritos usando o idioma inglês.
- Os nomes de tipo de entidade devem começar com uma letra maiúscula
	- Neste caso temos apenas um tipo de entidade - **Store**
- Os IDs de entidade devem ser um URN seguindo as diretrizes NGSI-LD
	- O NGSI-LD foi publicado recentemente como uma [especificação completa do ETSI](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.04.01_60/gs_cim009v010401p.pdf), a proposta é que cada `id` é um URN que segue um formato padrão: `urn:ngsi-ld:<entity-type>:<entity-id>`. Isso significa que cada `id` no sistema será único.
- Os nomes dos tipos de dados devem reutilizar os tipos de dados do schema.org sempre que possível
	- [Schema.org](http://schema.org/) é uma iniciativa para criar esquemas de dados estruturados comuns. Para promover a reutilização, usamos deliberadamente os nomes de tipo [`Text`](http://schema.org/PostalAddress) e [`PostalAddress`](http://schema.org/PostalAddress) em nossa entidade **Store**. Outros padrões existentes, como [Open311](http://www.open311.org/) (para rastreamento de questões cívicas) ou [Datex II](https://datex2.eu/) (para sistemas de transporte) também podem ser usados , mas o objetivo é verificar a existência do mesmo atributo em modelos de dados existentes e reutilizá-lo.
- Use a sintaxe **camelCase** para nomes de atributos
	- O `streetAddress`, `addressRegion`, `addressLocality` e `postalCode` são todos exemplos de atributos usando camel casing
- As informações de localização devem ser definidas usando os atributos `address` e `location`
	- Usamos um atributo `address` para locais cívicos conforme [schema.org](http://schema.org/)
	- Usamos um atributo `location` para coordenadas geográficas.
- Use GeoJSON para codificar propriedades geoespaciais
	- [GeoJSON](http://geojson.org/) é um formato padrão aberto projetado para representar características geográficas simples. O atributo `location` foi codificado como um local geoJSON `Point`.

### Metadados de atributo

Metadados são _"dados sobre dados"_. São dados adicionais para descrever propriedades do próprio valor do atributo, como precisão, provedor ou um carimbo de data/hora. Já existem vários atributos de metadados integrados e esses nomes são reservados, são eles:

- `dateCreated` (tipo: DateTime): data de criação do atributo como uma string ISO 8601.
- `dateModified` (tipo: DateTime): data de modificação do atributo como uma string ISO 8601.
- `previousValue` (tipo: qualquer): Indica o valor anterior de um attributo (Somente em notificações).
- `actionType` (tipo: Texto): Indica qual o tipo de ação ocorreu no atributo (Somente em notificações).

Um elemento de metadados pode ser encontrado no atributo `address`, no qual um sinalizador `verified` indica se o endereço foi confirmado.

## Consultando dados de contexto

Um aplicativo consumidor agora pode solicitar dados de contexto fazendo solicitações HTTP para o **Orion Context Broker**. A interface NGSI existente nos permite fazer consultas complexas e filtrar resultados.

No momento, para a demonstração das lojas, todos os dados de contexto estão sendo adicionados diretamente por meio de solicitações HTTP, porém em uma solução inteligente mais complexa, o **Orion Context Broker** também recuperará o contexto diretamente dos sensores associados a cada entidade.

Abaixo estão alguns exemplos de solicitações, em cada caso o parâmetro de consulta `options=keyValues` foi usado para encurtar as respostas removendo os elementos de tipo de cada atributo

### Obter dados da entidade por ID

>[!Info] **Envie a solicitação `Resgate loja 1`**. 
>Este solicitação resgata as informações da loja com o ID `urn:ngsi-ld:Store:001`

Devido ao uso de `options=keyValues`, a resposta consiste apenas em JSON sem os elementos de atributo `type` e `metadata`.

```json
{
    "id": "urn:ngsi-ld:Store:001",
    "type": "Store",
    "address": {
        "streetAddress": "Avenida Maria Servidei Demarchi, 398",
        "addressRegion": "São Paulo",
        "addressLocality": "São Bernardo do Campo",
        "postalCode": "09820-000"
    },
    "location": {
        "type": "Point",
        "coordinates": [
            -46.552501261,
            -23.726831523
        ]
    },
    "name": "Carrefour"
}
```

> Se você deseja os metadados de uma determinada entidade, basta desmarcar as opções de parâmetros na aba `params` no Postman

### Obter dados da entidade por tipo

Este exemplo retorna os dados de todas as entidades do tipo `store` dentro dos dados de contexto. O parâmetro `type` limita a resposta apenas para armazenar entidades.

>[!Info] **Envie a solicitação `Recupere as lojas`**. 
>Esta solicitação recupera todas as entidades definidas com o tipo `store`

A resposta é uma lista de todas as entidades que correspondem à consulta por `type`, neste caso o tipo `Building`. A resposta será algo semelhante a:

```json
[
    {
        "id": "urn:ngsi-ld:Store:001",
        "type": "Store",
        "address": {
            "streetAddress": "Avenida Maria Servidei Demarchi, 398",
            "addressRegion": "São Paulo",
            "addressLocality": "São Bernardo do Campo",
            "postalCode": "09820-000"
        },
        "location": {
            "type": "Point",
            "coordinates": [
                -46.552501261,
                -23.726831523
            ]
        },
        "name": "Carrefour"
    },
    {
        "id": "urn:ngsi-ld:Store:002",
        "type": "Store",
        "address": {
            "streetAddress": "Avenida Humberto de Alencar Castelo Branco, 3100",
            "addressRegion": "São Paulo",
            "addressLocality": "São Bernardo do Campo",
            "postalCode": "09851-070"
        },
        "location": {
            "type": "Point",
            "coordinates": [
                -46.584579033,
                -23.716240476
            ]
        },
        "name": "Bem Barato"
    }
]
```

### Filtre dados de contexto comparando os valores de um atributo

Este exemplo retorna todos as lojas com o atributo `name` igual a `Carrefour`. A filtragem pode ser feita usando o parâmetro `q`. 

>[!Info] **Envie a solicitação `Recupere o Carrefour`**. 
>Essa solicitação resgata a entidade que contém um atributo `name` que é igual a `Carrefour`.

Observe que o parâmetro `q` é igual a `name==Carrefour`. A resposta será uma lista de entidades que correspondem à consulta fornecida, neste caso, apenas uma entidade. Abaixo segue a resposta:

```json
[
    {
        "id": "urn:ngsi-ld:Store:001",
        "type": "Store",
        "address": {
            "streetAddress": "Avenida Maria Servidei Demarchi, 398",
            "addressRegion": "São Paulo",
            "addressLocality": "São Bernardo do Campo",
            "postalCode": "09820-000"
        },
        "location": {
            "type": "Point",
            "coordinates": [
                -46.552501261,
                -23.726831523
            ]
        },
        "name": "Carrefour"
    }
]
```

### Filtre dados de contexto comparando os valores de um subatributo

Este exemplo retorna todas as entidades `Store` localizadas em São Bernardo do Campo. A filtragem pode ser feita usando o parâmetro `q`. Os subatributos são anotados usando a sintaxe de ponto, por exemplo `address.addressLocality` 

>[!Info] **Envie a solicitação `Recupere lojas em São Bernardo`**. 
>Esta solicitação recupera as entidades que contém um atributo chamado `adress` e que este tenha um subatributos chamado `adressLocality`. Este subatributo deve ser igual a `São Bernardo do Campo`

>Caso uma string contenha algum caractere não permitido, como `á` ou `-`, ela deve ser codificada em URL (use esta ferramenta [URL Encode and Decode](https://www.urlencoder.org/)) e mantida entre aspas simples `'` = `%27`

A resposta é uma lista de entidades que correspondem a essa consulta. Neste caso, ambos as lojas estão localizados em São Bernardo e como tal são retornados na requisição. Abaixo segue a resposta:

```json
[
    {
        "id": "urn:ngsi-ld:Store:001",
        "type": "Store",
        "address": {
            "streetAddress": "Avenida Maria Servidei Demarchi, 398",
            "addressRegion": "São Paulo",
            "addressLocality": "São Bernardo do Campo",
            "postalCode": "09820-000"
        },
        "location": {
            "type": "Point",
            "coordinates": [
                -46.552501261,
                -23.726831523
            ]
        },
        "name": "Carrefour"
    },
    {
        "id": "urn:ngsi-ld:Store:002",
        "type": "Store",
        "address": {
            "streetAddress": "Avenida Humberto de Alencar Castelo Branco, 3100",
            "addressRegion": "São Paulo",
            "addressLocality": "São Bernardo do Campo",
            "postalCode": "09851-070"
        },
        "location": {
            "type": "Point",
            "coordinates": [
                -46.584579033,
                -23.716240476
            ]
        },
        "name": "Bem Barato"
    }
]
```


### Filtre dados de contexto consultando metadados

Este exemplo retorna os dados de todas as entidades `Store` com um endereço verificado. As consultas de metadados podem ser feitas usando o parâmetro `mq`.

>[!Info] **Envie a solicitação `Recupere lojas verificadas`**. 
>Esta solicitação recupera as lojas que contém um metadado de um atributo com o nome `verified`.

A resposta é uma lista de entidades que correspondem a essa consulta de metadados fornecida. Nesse caso, ambos as `stores` são verificadas, portanto ambas são retornadas na resposta. Abaixo segue a resposta:

```json
[
    {
        "id": "urn:ngsi-ld:Store:001",
        "type": "Store",
        "address": {
            "streetAddress": "Avenida Maria Servidei Demarchi, 398",
            "addressRegion": "São Paulo",
            "addressLocality": "São Bernardo do Campo",
            "postalCode": "09820-000"
        },
        "location": {
            "type": "Point",
            "coordinates": [
                -46.552501261,
                -23.726831523
            ]
        },
        "name": "Carrefour"
    },
    {
        "id": "urn:ngsi-ld:Store:002",
        "type": "Store",
        "address": {
            "streetAddress": "Avenida Humberto de Alencar Castelo Branco, 3100",
            "addressRegion": "São Paulo",
            "addressLocality": "São Bernardo do Campo",
            "postalCode": "09851-070"
        },
        "location": {
            "type": "Point",
            "coordinates": [
                -46.584579033,
                -23.716240476
            ]
        },
        "name": "Bem Barato"
    }
]
```

### Filtre dados de contexto comparando os valores de um atributo `geo:json`

Este exemplo retorna a loja que está a uma distância máxima de 1500 metros de um ponto representado por um objeto `geo:json`. A consulta deve conter os seguintes parâmetros:
- `georel` - Que tipo de consulta será usada. Pode ser `near`, `coveredBy`, `intersects`, `equals` e `disjoint`.
- `geometria` - Pode ser um `point`, `line`, `box`, `polygon`.
- `coords` - coordenadas para essa geometria dada.

>[!Info] **Envie a requisição `Recupere loja mais próxima`**. 
>Esta requisição resgata as lojas que estão a 1500 de um ponto definido como um objeto `geo:json`.

A resposta é uma lista de entidades correspondentes a essa consulta, no nosso caso mostra uma lista de `stores` que estão a uma distância máxima de 1500 metros do ponto localizado nas coordenadas -23.7272 -46.5792 (referente ao Centro universitário FEI). Abaixo segue a resposta:

```json
[
    {
        "id": "urn:ngsi-ld:Building:002",
        "type": "Building",
        "address": {
            "streetAddress": "Avenida Humberto de Alencar Castelo Branco, 3100",
            "addressRegion": "São Paulo",
            "addressLocality": "São Bernardo do Campo",
            "postalCode": "09851-070"
        },
        "location": {
            "type": "Point",
            "coordinates": [
                -46.584579033,
                -23.716240476
            ]
        },
        "name": "Bem Barato"
    }
]
```


:: **Referência** :: [Getting Started with NGSI-v2 - Step-by-Step for NGSI-v2 (fiware-tutorials.readthedocs.io)](https://fiware-tutorials.readthedocs.io/en/latest/getting-started.html)