# Introdução 

Este tutorial ensina os usuários do FIWARE sobre dados de contexto e provedores de contexto. O tutorial baseia-se na entidade **Store** criada nos últimos [[Entidades e relacionamentos no FIWARE|tutoriais do FIWARE]] e permite ao usuário recuperar dados sobre uma loja que não são mantidos diretamente no **Orion Context Broker**.

# # Requisitos 

**Antes de prosseguir é recomendado que os usuários sigam os [[Requisitos para acompanhar os tutoriais]].** 

> **Você pode obter todos os arquivos necessários para este tutorial no seguinte link: [Tutoriais no GitHub](https://github.com/rafaelalvesitm/my_fiware_tutorials) e indo para a pasta `tutorial4`. Existe um arquivo `docker-compose.yml` usado para criar o tutorial usando o Docker um arquivo `tutorial4.postman_collection.json` usado para importar as solicitações deste tutorial para o Postman**.**

# Vídeo do tutorial

# Player

<iframe width="100%" height=100% style="aspect-ratio: 16/9" src="https://www.youtube.com/embed/Ttb5xMKwQBI" allowfullscreen></iframe>


Caso o player não funcione utilize o link: [Provedores de contexto - Tutoriais do FIWARE #5 - YouTube](https://www.youtube.com/watch?v=Ttb5xMKwQBI)

# Dados  de contexto e provedores de contexto

Dentro da plataforma FIWARE, uma entidade representa o estado de um objeto físico ou conceitual que existe no mundo real. Por exemplo, uma **Loja** é um edifício de tijolos e argamassa do mundo real.

Os dados de contexto dessa entidade definem o estado desse objeto do mundo real em um determinado momento. Em todos os tutoriais até agora, estamos mantendo todos os dados de contexto para nossas entidades `Store` diretamente no **Orion Context Broker**, por exemplo, as lojas teriam atributos como:

- Um identificador exclusivo para a loja, por exemplo `urn:ngsi-ld:Store:001`.
- O nome da loja, por exemplo "Carrefour".
- O endereço "Avenida Maria Servidei Demarchi, 398".
- Um local físico, por exemplo -46.552, -23.726.

Como você pode ver, a maioria desses atributos é completamente estática (como o local) e os outros provavelmente não serão alterados regularmente - embora uma rua possa ser renomeada ou o nome da loja possa ser renomeado.

No entanto, há outra classe de dados de contexto sobre a entidade **Store** que é muito mais dinâmica, informações como:
- A temperatura atual no local da loja
- A umidade relativa atual no local da loja

Essas informações estão sempre mudando e, se fossem mantidas estaticamente em um banco de dados, os dados estariam sempre desatualizados. Para manter os dados de contexto atualizados e poder recuperar o estado atual do sistema sob demanda, novos valores para esses atributos de dados dinâmicos precisarão ser recuperados sempre que o contexto da entidade for solicitado.

As soluções inteligentes são projetadas para reagir ao estado atual do mundo real. Eles estão "conscientes", pois dependem de leituras dinâmicas de dados de fontes externas (como mídias sociais, sensores de IoT, entradas do usuário). A plataforma FIWARE torna transparente a coleta e apresentação de dados de contexto em tempo real, pois sempre que uma solicitação do [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2) é feita ao **Orion Context Broker**, sempre retornará o contexto mais recente combinando os dados mantidos em seu banco de dados com as leituras de dados em tempo real de qualquer provedor de contexto externo registrado.

Para poder atender a essas solicitações, o **Orion Context Broker** deve primeiro ser fornecido com dois tipos de informações:

- Os dados de contexto estáticos mantidos dentro do próprio Orion (_Entidades que Orion "conhece" sobre_)
- Provedores de contexto externos registrados e  associados a entidades existentes (_Entidades que Orion pode "encontrar informações" sobre_)

Em nosso sistema simples de gerenciamento de estoque, nossa entidade **Store** atualmente retorna os atributos `id`, `name`, `address` e `location`. Aumentaremos isso com dados de contexto em tempo real adicionais de um gerador de contexto aleatório.

## Arquitetura

Este aplicativo fará uso de apenas um componente FIWARE - o [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/). O uso do **Orion Context Broker** (com dados de contexto adequados fluindo por ele) é suficiente para que um aplicativo seja qualificado como _“Powered by FIWARE”_.

Atualmente, o **Orion Context Broker** conta com a tecnologia de código aberto [MongoDB](https://www.mongodb.com/) para manter a persistência dos dados de contexto que ele contém. Para solicitar dados de contexto de fontes externas, agora precisaremos adicionar um provedor de contexto simples.

Portanto, a arquitetura será composta por três elementos:
- O [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) que receberá solicitações usando [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ ngsiv2).
- O banco de dados [MongoDB](https://www.mongodb.com/):
	- Usado pelo **Orion Context Broker** para armazenar informações de dados de contexto, como entidades de dados, assinaturas e registros.
- O **Fornecedor de contexto** que irá:
	- Receber solicitações usando [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2).
	- Fazer solicitações para fontes de dados disponíveis publicamente usando suas próprias APIs em um formato proprietário.
	- Retornar dados de contexto de volta ao **Orion Context Broker** no formato [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2).

Como todas as interações entre os serviços são iniciadas por solicitações HTTP, os serviços podem ser disponibilizados em contêineres e executados a partir de portas expostas.

![[Fiware context provider tutorial architecture.png]]

# Iniciando os containers

Baixe o arquivo zip ou clone o repositório disponível em [neste link](https://github.com/rafaelalvesitm/my_fiware_tutorials). Abra um terminal e se mova para a pasta `tutorial2`. Depois disso, todos os serviços podem ser inicializados a partir da linha de comando usando o comando `docker compose` conforme indicado abaixo:

```bash
docker compose up -d
```

> **Observação:** Se você deseja limpar e começar de novo, pode fazê-lo com o seguinte comando:
> `docker compose down` e depois utilizar o comando anterior.

O sinalizador `-d` indica que o Docker deve executar os contêineres no modo `detached`, o que significa que os contêineres serão executados em segundo plano.

> **Observação:** você pode verificar cada contêiner no aplicativo Docker ou no plug-in do Docker dentro do Visual Studio Code. Além disso pode usar o comando `docker compose ps -a` ou `docker ps -a` para listar todos os contêineres e avaliar a situação deles.

> [!info] Caso não tenha feito o tutorial anterior, envie a solicitação `Preparando o tutorial 4
> Este solicitação cria as duas entidades que representam as lojas a serem utilizadas nestes tutorial. Essas entidades foram criadas no tutorial anterior. 

# Verificação do provedor de contexto

Você pode ver qual é o comportamento do provedor de contexto no arquivo `app.py`. Este aplicativo Flask tem 2 rotas:
- `health` - Usado para verificar se o provedor de contexto está funcionando
- `op/query` - Usado para retornar informações de contexto. Ele espera uma mensagem específica do **Orion Context Broker**.

São duas solicitações usadas para verificar se o **Orovedor de contexto** está funcionando corretamente
- `Verificação de integridade` - Envia uma requisição GET simples para a rota `health` para verificar se o provedor de contexto está funcionando e responder no endereço IP correto (deve ser localhost:5000).
- ``Verificar consulta` - Envia uma solicitação POST com a consulta que deve ser criada pelo Orion Context Broker ao solicitar informações de contexto.

>[!info] **Envie a solicitação de `Verificação de integridade`**.
>Esta requisição verifica se o **Provedor de contexto** está disponível para ser utilizado. 

Essa solicitação retorna a seguinte resposta:

```json
{
    "relative humidity": 50,
    "temperature": 39
}
```

Essa solicitação obtém uma umidade relativa aleatória (intervalo de 0 a 100) e temperatura (intervalo de 10 a 40) toda vez que é chamada.

>[!info] **Envie a solicitação `Verificar consulta`**.
>Esta solicitação verifica se o **Provedor de contexto** está funcionando adequadamente quanto recebe uma notificação parecida com a que o **Orion Context Broker** enviará ao provedor de contexto. 

Esta solicitação espera uma mensagem com o seguinte corpo JSON:

```json
{
    "entities": [
        {
            "type": "Store",
            "isPattern": "false",
            "id": "urn:ngsi-ld:Store:001"
        }
    ],
    "attrs": [
        "temperature",
        "relativeHumidity"
    ]
}
```

Nesta mensagem, `entities` são as entidades que o provedor de contexto deve fornecer informações e `attrs` são os atributos para as determinadas entidades. O resultado desta solicitação é o seguinte:

```json
[
    {
        "id": "urn:ngsi-ld:Store:001",
        "relativeHumidity": {
            "type": "Number",
            "value": 41
        },
        "temperature": {
            "type": "Number",
            "value": 18
        },
        "type": "Store"
    }
]
```

O resultado é uma lista de entidades com informações de contexto aleatórias para umidade relativa e temperatura. Você pode solicitar apenas um atributo especificando apenas um atributo no corpo da solicitação.

> É importante notar que a consulta é feita na rota `/op/query`. A especificação NGSI-V2 indica que todos os provedores de contexto devem especificar isso como a rota para essa determinada entidade.

# Ações de registro do provedor de contexto

Todas as ações de registro do provedor de contexto ocorrem no endpoint `v2/registrations`. Os mapeamentos CRUD padrão se aplicam:

- A criação é mapeada para o HTTP POST.
- Leitura/Listagem de registros para o verbo HTTP GET.
- A exclusão é mapeada para HTTP DELETE.

>[!info] **Envie a solicitação `Criar loja 1`**.
> Esta solicitação cria uma loja semelhante à do tutorial [[Introdução ao FIWARE]].

### Registrando um novo provedor de contexto

Este exemplo registra o **Provedor de contexto** junto ao **Orion Context Broker**. O corpo da solicitação afirma que: _"A URL `http://context-provider:5000` é capaz de fornecer dados de `relativeHumidity` e `temperature` para a entidade `id=urn:ngsi-ld:Store: 001`"_.

Os valores **nunca** são mantidos no **Orion Context Broker**, mas sempre são solicitados sob demanda do provedor de contexto registrado. O **Orion Context Broker** apenas mantém as informações de registro sobre quais provedores de contexto podem oferecer dados de contexto.

>[!info] **Envie a solicitação `Registre o contexto para a Loja 1`**. 
>Essa solicitação cria um registro no **Orion Context Broker**. 

O seguinte corpo JSON é fornecido:

```JSON
{
    "description": "Random Conditions",
    "dataProvided": {
        "entities": [
            {
                "id": "urn:ngsi-ld:Store:001",
                "type": "Store"
            }
        ],
        "attrs": [
            "relativeHumidity",
            "temperature"
        ]
    },
    "provider": {
        "http": {
            "url": "http://context-provider:5000"
        }
    }
}
```

Esta solicitação retornará com um código de resposta **201 - Criado**. O cabeçalho `Location` da resposta contém um caminho para o registro de registro mantido no Orion

## Lendo informações de contexto

Depois que um provedor de contexto for registrado, os novos dados de contexto serão incluídos se o contexto da entidade **Store** `urn:ngsi-ld:Store:001` for solicitado usando o `/entities/<entity-id> ` ponto final:

>[!info] **Envie múltiplas solicitações `Recupere a loja 1`**. 
>Essa solicitação obtém a entidade `Store` 1. 

Observe que toda vez que essa solicitação é feita, um valor aleatório para temperatura e umidade relativa é fornecido pelo provedor de contexto. A resposta a seguir é um exemplo:

```json
{
    "id": "urn:ngsi-ld:Store:001",
    "type": "Store",
    "relativeHumidity": {
        "type": "Number",
        "value": 91,
        "metadata": {}
    },
    "temperature": {
        "type": "Number",
        "value": 12,
        "metadata": {}
    }
}
```

Observe a seguinte ordem de comunicação.

![[Fiware context provider tutorial - context.png]]

O número representa o seguinte:

1. O usuário solicita uma informação de contexto para uma determinada entidade.
2. O usuário solicita uma informação de contexto para uma determinada entidade. Em seguida, ele envia as solicitações para esse determinado atributo e/ou entidade para o provedor de contexto apropriado
3. O provedor de contexto responde ao Orion Context Broker com as informações de contexto apropriadas.
4. O Orion Context Broker responde ao usuário com a entidade e seus atributos preenchidos com informações do provedor de contexto.

### Leitura de um provedor de contexto registrado

É possível ler os registros no **Orion Context Broker**. 

>[!info] **Envie a solicitação `Recupere todos os registros`**. 
>Essa solicitação lista todos os registros no **Orion Context Broker**. 

A seguir, uma resposta para essa solicitação:

```json
[
    {
        "id": "633dbe07d4210825b72e22db",
        "description": "Random Conditions",
        "dataProvided": {
            "entities": [
                {
                    "id": "urn:ngsi-ld:Store:001",
                    "type": "Store"
                }
            ],
            "attrs": [
                "relativeHumidity",
                "temperature"
            ]
        },
        "provider": {
            "http": {
                "url": "http://context-provider:5000"
            },
            "supportedForwardingMode": "all",
            "legacyForwarding": false
        },
        "status": "active"
    }
]
```

### Remover um provedor de contexto registrado
Os registros podem ser excluídos fazendo uma solicitação DELETE para o ponto de extremidade `/v2/registrations/<entity>`.

>[!info] **Envie a solicitação `Excluir registro`**. 
>Esta solicitação delete um registro feito no **Orion Context Broker**. Observe que a rota deve corresponder ao id de registro acima. 

O resultado, se válido, é uma mensagem com o código `204 - Sem conteúdo`.

# Conclusão

Este tutorial apresenta a capacidade do **Orion Context Broker** de receber informações de contexto de fontes externas. É importante destacar que este tutorial introduz um **Provedor de contexto** simples que gera dados aleatórios mas é possível aumentar a capacidade do **Provedor de contexto** criando um proxy NGSI que consuma APIs externas. 

:: **Referência** :: [Context Providers - Step-by-Step for NGSI-v2](https://fiware-tutorials.readthedocs.io/en/latest/context-providers.html)