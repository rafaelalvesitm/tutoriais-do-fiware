# Introdução 

Este tutorial ensina os usuários do FIWARE sobre como criar e gerenciar assinaturas de dados de contexto. O tutorial baseia-se na entidade **Store** criada nos últimos [[Entendendo entidades e relacionamentos em FIWARE|tutoriais do FIWARE]] e permite ao usuário enviar notificações para sistemas externos caso uma regra seja atingida. 

# Requirements

# Requisitos 

**Antes de prosseguir é recomendado que os usuários sigam os [[Requisitos para acompanhar os tutoriais]].** 

> **Você pode obter todos os arquivos necessários para este tutorial no seguinte link: [Tutoriais no GitHub](https://github.com/rafaelalvesitm/my_fiware_tutorials) e indo para a pasta `tutorial5`. Existe um arquivo `docker-compose.yml` usado para criar o tutorial usando o Docker um arquivo `tutorial5.postman_collection.json` usado para importar as solicitações deste tutorial para o Postman**.

# Assinando Mudanças de Estado

Dentro da plataforma FIWARE, uma entidade representa o estado de um objeto físico ou conceitual que existe no mundo real. Toda solução inteligente precisa conhecer o estado atual desses objetos em um determinado momento.

O contexto de cada uma dessas entidades está em constante mudança. Por exemplo, no exemplo de gerenciamento de lojas, o contexto mudará à medida que novas lojas forem abertas, os produtos forem vendidos, os preços mudarem e assim por diante. Para uma solução inteligente baseada em dados de sensores de IoT, esse problema é ainda mais premente, pois o sistema reage constantemente às mudanças no mundo real.

Até agora todas as operações que usamos para alterar o estado do sistema foram **síncronas** - as alterações foram feitas diretamente por um usuário ou aplicativo, e eles foram informados do resultado. O **Orion Context Broker** também oferece um mecanismo de notificação **assíncrono** - os aplicativos podem se inscrever em alterações de informações de contexto para que possam ser informados quando algo acontecer. Isso significa que o aplicativo não precisa sondar ou repetir solicitações de consulta continuamente.

O uso do mecanismo de assinatura reduzirá, portanto, o volume de solicitações e a quantidade de dados transmitidos entre os componentes do sistema. Essa redução no tráfego de rede melhorará a capacidade de resposta geral.

# Arquitetura

Este aplicativo fará uso de apenas um componente FIWARE - o [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/). O uso do **Orion Context Broker** (com dados de contexto adequados fluindo por ele) é suficiente para que um aplicativo seja qualificado como _“Powered by FIWARE”_.

Atualmente, o **Orion Context Broker** conta com a tecnologia de código aberto [MongoDB](https://www.mongodb.com/) para manter a persistência dos dados de contexto que ele contém. Para solicitar dados de contexto de fontes externas, um simples **proxy NGSI do provedor de contexto** também foi adicionado. Para visualizar e interagir com o **Provedor de contexto**,

Portanto, a arquitetura será composta por quatro elementos:

- O [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) que receberá solicitações usando [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ ngsiv2)
- O banco de dados subjacente [MongoDB](https://www.mongodb.com/):
	- Usado pelo **Orion Context Broker** para armazenar informações de dados de contexto, como entidades de dados, assinaturas e registros
- O **Fornecedor de contexto** que irá:
	- Receber solicitações usando [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2)
	- Retorna dados de contexto de volta ao **Orion Context Broker** no formato [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2).
	- Mostrar a última notificação recebida pelo **Orion Context Broker**.

Como todas as interações entre os serviços são iniciadas por solicitações HTTP, os serviços podem ser disponibilizados em containers e executados a partir de portas expostas.



# Iniciando os containers

Baixe o arquivo zip ou clone o repositório disponível em [neste link](https://github.com/rafaelalvesitm/my_fiware_tutorials). Abra um terminal e se mova para a pasta `tutorial5`. Depois disso, todos os serviços podem ser inicializados a partir da linha de comando usando o comando `docker compose` conforme indicado abaixo:

```bash
docker compose up -d
```

> **Observação:** Se você deseja limpar e começar de novo, pode fazê-lo com o seguinte comando:
> `docker compose down` e depois utilizar o comando anterior.

O sinalizador `-d` indica que o Docker deve executar os contêineres no modo `detached`, o que significa que os contêineres serão executados em segundo plano.

> **Observação:** você pode verificar cada contêiner no aplicativo Docker ou no plug-in do Docker dentro do Visual Studio Code. Além disso pode usar o comando `docker compose ps -a` ou `docker ps -a` para listar todos os contêineres e avaliar a situação deles.

> [!info] Caso não tenha feito o tutorial anterior, envie a solicitação `Preparando o tutorial 5`
> Este solicitação cria as duas entidades que representam as lojas a serem utilizadas nestes tutorial. Essas entidades foram criadas no tutorial anterior. 

# Ações CRUD de assinatura

As operações **CRUD** para assinaturas são mapeadas para os verbos HTTP esperados no endpoint `/v2/subscriptions/`.

- **Criar** - HTTP POST
- **Ler** - HTTP GET
- **Atualização** - PATCH HTTP
- **Excluir** - HTTP DELETE

O `<id de assinatura>` é gerado automaticamente quando a assinatura é criada e retornada no cabeçalho da resposta POST para ser usada pela outra operação posterior.

## Criando uma assinatura

Este exemplo cria uma nova assinatura. A assinatura acionará uma notificação assíncrona para uma URL sempre que o contexto for alterado e as condições da assinatura - Quaisquer alterações nos preços do produto - forem atendidas.

Novas assinaturas podem ser adicionadas fazendo uma solicitação POST para o endpoint `/v2/subscriptions/`. A seção de assunto da solicitação informa que a assinatura será acionada sempre que o atributo de preço de qualquer entidade do Produto for alterado.

A seção de notificação do corpo informa que uma solicitação POST contendo todas as entidades afetadas será enviada para o endpoint `http://tutorial:3000/subscription/price-change`.

>[!info] **Envie a solicitação `Criar assinatura para alteração de preço`**. 
>Essa solicitação cria uma assinatura para todas as entidades do Produto e é acionada sempre que o atributo de preço muda. 

A notificação é enviada para a URL `http://context-provider:5000/priceChange`. Abra o arquivo `app.py` e veja que esta URL apenas atualiza a variável `lastPriceChange` que pode ser vista na URL `http://localhost:5000/monitor`.

>[!info] **Envie a solicitação "Alterar preço"**. 
>Esta solicitação altera o preço de um Produto. 

Ao receber essa solicitação, o **Orion Context Broker** altera o preço do Produto. Como existe uma assinatura, ele também envia uma notificação para a URL especificada. A notificação é semelhante à abaixo:

```json
{
  "data": [
    {
      "id": "urn:ngsi-ld:Product:010",
      "price": {
        "metadata": {},
        "type": "Integer",
        "value": 70
      },
      "type": "Product"
    }
  ],
  "subscriptionId": "633ebd2c1007af0e6472062b"
}
```

## Listar todas as assinaturas

Este exemplo lista todas as assinaturas fazendo uma solicitação GET para o endpoint `/v2/subscriptions/`.

A seção de notificação de cada assinatura também incluirá a última vez que as condições da assinatura foram atendidas e se a ação POST associada foi bem-sucedida.

>[!info] **Envie a solicitação "Obter assinaturas"**. 
>Esta solicitação gesta todas as assinaturas no **Orion Context Broker**. 

A resposta a seguir é um exemplo:

```json
[
    {
        "id": "633ebd2c1007af0e6472062b",
        "description": "Notify me of all product price changes",
        "status": "active",
        "subject": {
            "entities": [
                {
                    "idPattern": ".*",
                    "type": "Product"
                }
            ],
            "condition": {
                "attrs": [
                    "price"
                ]
            }
        },
        "notification": {
            "timesSent": 2,
            "lastNotification": "2022-10-06T11:35:04.000Z",
            "attrs": [],
            "onlyChangedAttrs": false,
            "attrsFormat": "normalized",
            "http": {
                "url": "http://context-provider:5000/priceChange"
            },
            "lastSuccess": "2022-10-06T11:35:04.000Z",
            "lastSuccessCode": 200,
            "covered": false
        }
    }
]
```

## Leia os detalhes de uma assinatura

Este exemplo obtém os detalhes completos de uma assinatura com um determinado ID. A resposta inclui detalhes adicionais na seção de notificação mostrando a última vez que as condições da assinatura foram atendidas e se a ação POST associada foi bem-sucedida.

>[!info] **Envie a solicitação `Obter assinatura específica`**. 
>Esta solicitação resgata as informações de uma assinatura específica registrada no **Orion Context Broker**.

Observe que você deve saber o ID da assinatura antecipadamente. A resposta para esta solicitação é apresentada abaixo:

```json
{
    "id": "633ebd2c1007af0e6472062b",
    "description": "Notify me of all product price changes",
    "status": "active",
    "subject": {
        "entities": [
            {
                "idPattern": ".*",
                "type": "Product"
            }
        ],
        "condition": {
            "attrs": [
                "price"
            ]
        }
    },
    "notification": {
        "timesSent": 2,
        "lastNotification": "2022-10-06T11:35:04.000Z",
        "attrs": [],
        "onlyChangedAttrs": false,
        "attrsFormat": "normalized",
        "http": {
            "url": "http://context-provider:5000/priceChange"
        },
        "lastSuccess": "2022-10-06T11:35:04.000Z",
        "lastSuccessCode": 200,
        "covered": false
    }
}
```

## Atualizar uma assinatura existente
Este exemplo altera uma assinatura existente com o ID `5ae07c7e6e4f353c5163c93e` e atualiza o URL de notificação.

As assinaturas podem ser atualizadas fazendo uma solicitação PATCH para o endpoint `/v2/subscriptions/<subscription-id>`.

**Envie a solicitação `Atualizar assinatura`**. Esta solicitação atualiza a assinatura anterior para desativá-la enviando as informações `"status": "inactive"`. Você pode tentar alterar o preço do produto e ver que o Orion Context Broker não notificará o Context Provider com a alteração.

## Excluir uma assinatura

As assinaturas podem ser excluídas fazendo uma solicitação DELETE para o ponto de extremidade `/v2/subscriptions/<ID da assinatura>`. Observe que você deve saber o ID da assinatura com antecedência.

>[!info] **Envie a solicitação `Excluir assinatura`**.
>Essa solicitação exclui uma assinatura registrada no **Orion Context Broker**. Note que é necessário saber previamenete qual o ID da assinatura. 

## Reduzindo a carga útil com `attrs`, `attrsFormat` ou expressões. 

No exemplo anterior, os dados detalhados completos de cada entidade **product** afetada foram enviados com a notificação POST. Isso não é muito eficiente.

A quantidade de dados transmitidos pode ser reduzida adicionando um atributo `attrs` que especificará uma lista de atributos a serem incluídos nas mensagens de notificação - outros atributos são ignorados

> **Dica** um atributo `exceptAttrs` também existe para retornar todos os atributos, exceto os da lista de exclusão. `attrs` e `exceptAttrs` não podem ser usados simultaneamente na mesma assinatura.

O atributo `attrsFormat` especifica como as entidades são representadas nas notificações. Uma resposta detalhada é retornada por padrão. `keyValues` e `values` funcionam da mesma maneira que uma solicitação GET `v2/entities`.

Também é possível passar uma expressão para ser avaliada como, por exemplo, notificando apenas quando um preço fica abaixo de 50. Este exemplo é expresso como `"expression": {"q": "price<50;"}`.

>[!info] **Envie a solicitação `Criar assinatura mais simples`**. 
>Essa solicitação simplifica a assinatura criada anteriormente para mostrar apenas valores-chave e notificar apenas quando o preço ficar abaixo de 50. 

>[!info] **Envie a solicitação `Alterar preço para 40`**. 
>Essa solicitação altera o preço do produto associado a assinatura criada. 

Observe na URL `http://localhost:5000/monitor` a nova notificação. Essa notificação aparece pois o **Orion Context Broker** notifica a aplicação quando o preço do produto fica menor do que 50. 

# Conclusão

A assinatura é um mecanismo para enviar mensagens de forma assíncrona do **Orion Context Broker** para aplicativos externos. Esse mecanismo é importante para não criar muito tráfego de dados enviando mensagens de tempos em tempos, mas apenas quando algo acontece, como alterar um valor de atributo.

:: **Referência** :: [Subscriptions - Step-by-Step for NGSI-v2](https://fiware-tutorials.readthedocs.io/en/latest/subscriptions.html)