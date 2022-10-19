# Introdução 

Este tutorial ensina os usuários de FIWARE sobre como conectar dispositivos IoT baseados em JSON usando o [Agente IoT para JSON](https://fiware-iotagent-json.readthedocs.io/en/latest/usermanual/index.html#user- programmers-manual) para que as medições possam ser lidas e os comandos possam ser enviados usando solicitações [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2) enviadas ao [Orion Context Broker](https ://fiware-orion.readthedocs.io/en/latest/).

# Requisitos 

**Antes de prosseguir é recomendado que os usuários sigam os [[Requisitos para acompanhar os tutoriais]].** 

> **Você pode obter todos os arquivos necessários para este tutorial no seguinte link: [Tutoriais no GitHub](https://github.com/rafaelalvesitm/my_fiware_tutorials) e indo para a pasta `tutorial7`. Existe um arquivo `docker-compose.yml` usado para criar o tutorial usando o Docker um arquivo `tutorial7.postman_collection.json` usado para importar as solicitações deste tutorial para o Postman**.

## Por que são necessários vários agentes de IoT?

Um Agente IoT é um componente que permite que um grupo de dispositivos envie seus dados e sejam gerenciados a partir de um gestor de contexto usando seus próprios protocolos nativos. Cada agente de IoT é definido para um único formato de carga útil, embora possam usar vários transportes diferentes para essa carga. De longe, a carga útil de mensagens mais comum usada na Internet é a chamada [[Notação de Objeto JavaScript]] ou JSON, que será familiar a qualquer desenvolvedor de software.

Um [IoT Agent for JSON](https://fiware-iotagent-json.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual) separado foi criado especificamente para lidar com mensagens enviadas neste formato, uma vez que um grande número de dispositivos comuns podem ser programados para enviar mensagens em JSON e existem muitas bibliotecas de software para analisar os dados.

Não há diferença prática entre a comunicação usando uma carga JSON e a comunicação usando a carga útil de texto simples Ultralight - desde que a base dessa comunicação - em outras palavras, o protocolo fundamental que define como as mensagens são passadas entre os componentes permaneça o mesmo. Obviamente, a análise de cargas JSON dentro do IoT Agent - a conversão de mensagens de JSON para NGSI e vice-versa será exclusiva do **Agente IoT JSON**.

## Trânsito Sul (Comandos)

As solicitações HTTP geradas pelo **Orion Context Broker** e transmitidas para um dispositivo IoT (por meio de um **Agente IoT**) são conhecidas como tráfego de sentido sul. O tráfego no sentido sul consiste em **comandos** feitos para dispositivos atuadores que alteram o estado do mundo real por meio de suas ações.

Por exemplo, para ativar uma **Lâmpada inteligente** da vida real com um comando `on`, as seguintes interações ocorreriam:

1. Uma solicitação NGSI PATCH é enviada ao **Gestor de contexto** para atualizar o contexto atual do **Smart Lamp**.
2. Esta é efetivamente uma solicitação indireta, invocando o comando `on` da **Smart Lamp**.
3. O **Context Broker** encontra a entidade dentro do contexto e observa que a provisão de contexto para este atributo foi delegada ao IoT Agent
4. O **Gestor de contexto** envia uma solicitação NGSI à porta norte do **Agente IoT** para invocar o comando.
5. O **Agente IoT** recebe essa solicitação de transito sul e a converte em sintaxe JSON e a transmite para a **Lâmpada inteligente**
6. A **Lâmpada inteligente** liga a lâmpada e retorna o resultado do comando para o **Agente IoT** na sintaxe JSON.
7. O **Agente IoT** recebe essa solicitação de transito norte, a interpreta e passa o resultado da interação para o contexto fazendo uma solicitação NGSI ao **Orion Context Broker**.
8. O **Orion Context Broker** recebe essa solicitação de trânsito sul e atualiza o contexto com o resultado do comando.

![[FIWARE Southbound traffic - commands.png]]

-   Requests between **User** and **Context Broker** use NGSI
-   Requests between **Context Broker** and **IoT Agent** use NGSI
-   Requests between **IoT Agent** and **IoT Device** use native protocols
-   Requests between **IoT Device** and **IoT Agent** use native protocols
-   Requests between **IoT Agent** and **Context Broker** use NGSI

- Solicitações entre **Usuário** e o **Orion Context Broker** usam o protocolo NGSI
- Solicitações entre **Orion Context Broke** e **Agente IoT** usam o protocolo NGSI
- As solicitações entre o **Agente IoT** e o **Dispositivo IoT** usam protocolos nativos.
- As solicitações entre o **Dispositivo IoT** e o **Agente IoT** usam protocolos nativos
- Solicitações entre o **Agente IoT** e o **Orion Context Broker*** usam o protocolo NGSI.

## Tráfego no sentido norte (medições)

As solicitações geradas de um dispositivo IoT e passadas de volta para o **Orion Context Broker** (por meio de um agente IoT) são conhecidas como tráfego no sentido norte. O tráfego no sentido norte consiste em **medidas** feitas por dispositivos sensores e retransmite o estado do mundo real para os dados de contexto do sistema.

Por exemplo, para um **Sensor de movimento** da vida real para enviar uma medição de contagem, as seguintes interações ocorreriam:

1. Um **Sensor de movimento** faz uma medição e passa o resultado para o **Agente IoT**
2. O **IoT Agent** recebe essa solicitação de tráfico norte, converte o resultado da sintaxe JSON e passa o resultado da interação para o contexto fazendo uma solicitação NGSI ao **Context Broker**.
3. O **Orion Context Broker** recebe essa solicitação de tráfico norte e atualiza o contexto com o resultado da medição.

![[FIWARE northbound traffic - measurements.png]]

- Solicitações entre **Dipositivo IoT** e **Agente IoT** usam protocolos nativos.
- Solicitações entre **Agente IoT** e o **Orion Context Broker** usam NGSI.

> **Observação** Outras interações mais complexas também são possíveis, mas esta visão geral é suficiente para entender os princípios básicos de um Agente IoT.

## Funcionalidade comum

Como pode ser visto nas seções anteriores, embora cada **Agente IoT** seja único, pois interpreta protocolos diferentes, haverá um grande grau de semelhança entre os **Agentes IoT**. Algumas funções comuns são:
- Oferecer um local padrão para ouvir as atualizações do dispositivo.
- Oferecer um local padrão para ouvir atualizações de dados de contexto.
- Manter uma lista de dispositivos e mapear atributos de dados de contexto para a sintaxe do dispositivo.
- Autorizar e garantir a segurança das informações. 

Essa funcionalidade básica foi abstraída em uma [biblioteca de estrutura do IoT Agent comum](https://iotagent-node-lib.readthedocs.io/)

# Arquitetura

Este aplicativo se baseia nos componentes criados em tutoriais anteriores. Ele fará uso de dois componentes FIWARE - o [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) e o [IoT Agent for JSON](https://fiware-iotagent- json.readthedocs.io/en/latest/). O uso do **Orion Context Broker** é suficiente para que um aplicativo seja qualificado como _“Powered by FIWARE”_. Tanto o **Orion Context Broker** quanto o **Agente IoT** contam com a tecnologia de código aberto [MongoDB](https://www.mongodb.com/) para manter a persistência das informações que possuem.

Portanto, a arquitetura geral consistirá nos seguintes elementos:

- O FIWARE [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) que receberá solicitações usando [NGSI-v2](https://fiware.github.io/specifications/OpenAPI /ngsiv2).
- O FIWARE [IoT Agent for JSON](https://fiware-iotagent-json.readthedocs.io/en/latest/) que receberá solicitações no sentido sul usando [NGSI-v2](https://fiware.github.io /specifications/OpenAPI/ngsiv2) e convertê-los em comandos [JSON](https://fiware-iotagent-json.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual) para os dispositivos.
- O banco de dados subjacente [MongoDB](https://www.mongodb.com/):
    - Usado pelo **Orion Context Broker** para armazenar informações de dados de contexto, como entidades de dados, assinaturas e registros.
    - Usado pelo **IoT Agent** para armazenar informações do dispositivo, como URLs e chaves do dispositivo.
- O **Fornecedor de contexto**. Ele faz o seguinte:
    - receber solicitações usando [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2).
    - retorna dados de contexto de volta ao **Orion Context Broker** no formato [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2).
    - receber notificações do **Orion Context Broker**.
- O **dispositivo dummy**:
	- Envia medições aleatórias para o **Agente IoT JSON**.
	- Receba comandos do **Agente IoT JSON**.

Como todas as interações entre os elementos são iniciadas por solicitações HTTP, os componentes podem ser disponibilizadas em contêineres e executadas a partir de portas expostas. A arquitetura a seguir é usada neste tutorial.

![[FIWARE IoT Agent JSON tutorial.png]]

## Configuração do agente IoT para JSON 

O [Agente IoT para JSON](https://fiware-iotagent-json.readthedocs.io/en/latest/) pode ser instanciado em um contêiner do Docker. Uma imagem oficial do Docker está disponível no [Docker Hub](https://hub.docker.com/r/fiware/iotagent-json/) com a tag `fiware/iotagent-json`. A configuração necessária pode ser vista abaixo:

```yml
iot-agent:
    image: fiware/iotagent-json:latest
    hostname: iot-agent
    container_name: fiware-iot-agent
    depends_on:
        - mongo-db
    networks:
        - default
    expose:
        - "4041"
        - "7896"
    ports:
        - "4041:4041"
        - "7896:7896"
    environment:
        - IOTA_CB_HOST=orion
        - IOTA_CB_PORT=1026
        - IOTA_NORTH_PORT=4041
        - IOTA_REGISTRY_TYPE=mongodb
        - IOTA_LOG_LEVEL=DEBUG
        - IOTA_TIMESTAMP=true
        - IOTA_CB_NGSI_VERSION=v2
        - IOTA_AUTOCAST=true
        - IOTA_MONGO_HOST=mongo-db
        - IOTA_MONGO_PORT=27017
        - IOTA_MONGO_DB=iotagentjson
        - IOTA_HTTP_PORT=7896
        - IOTA_PROVIDER_URL=http://iot-agent:4041
        - IOTA_DEFAULT_RESOURCE=/iot/json
```

O contêiner `iot-agent` depende da presença do **Orion Context Broker** e usa um banco de dados **MongoDB** para armazenar informações do dispositivo, como URLs e chaves do dispositivo. O contêiner está escutando em duas portas:
- A porta `7896` é exposta para receber medições JSON sobre HTTP dos dispositivos IoT dummy.
- A porta `4041` é exposta puramente para acesso ao tutorial - para que cUrl ou Postman possam fazer comandos de provisionamento sem fazer parte da mesma rede.

O contêiner `iot-agent` é controlado por variáveis de ambiente, conforme mostrado:

| Chave | Valor | Descrição |
| --- | --- | --- |
| IOTA\_CB\_HOST | `órion` | Nome do host do agente de contexto para atualizar o contexto |
| IOTA\_CB\_PORT | `1026` | Porta em que o context broker atende para atualizar o contexto |
| IOTA\_NORTH\_PORT | `4041` | Porta usada para configurar o agente IoT e receber atualizações de contexto do agente de contexto |
| IOTA\_REGISTRY\_TYPE | `mongodb` | Se as informações do dispositivo IoT devem ser mantidas na memória ou em um banco de dados |
| IOTA\_LOG\_LEVEL | `DEBUG` | O nível de log do Agente IoT |
| IOTA\_TIMESTAMP | `true` | Se deve fornecer informações de carimbo de data/hora com cada medição recebida de dispositivos conectados |
| IOTA\_CB\_NGSI\_VERSION | `v2` | Se deve usar NGSI v2 ao enviar atualizações para atributos ativos |
| IOTA\_AUTOCAST | `true` | Certifique-se de que os valores numéricos JSON sejam lidos como números e não como strings |
| IOTA\_MONGO\_HOST | `context-db` | O nome do host do mongoDB - usado para armazenar informações do dispositivo |
| IOTA\_MONGO\_PORT | `27017` | A porta mongoDB está escutando |
| IOTA\_MONGO\_DB | `iotagentjson` | O nome do banco de dados usado no mongoDB |
| IOTA\_HTTP\_PORT | `7896` | A porta em que o IoT Agent escuta o tráfego do dispositivo IoT por HTTP |
| IOTA\_PROVIDER\_URL | `http://iot-agent:4041` | URL passado para o Context Broker quando os comandos são registrados, usado como um local de URL de encaminhamento quando o Context Broker emite um comando para um dispositivo |
| IOTA\_PROVIDER\_URL | `/iot/json` | O caminho padrão que o IoT Agent usa para ouvir medidas JSON. |

# Start Up

Para iniciar os contêineres, abra o código do visual studio e abra a pasta `tutorial6`. Na pasta há um arquivo `docker-compose`, uma pasta chamada `context-provider` e uma pasta chamada `dummy-devices`.

A pasta **context-provider** contém:
- `Dockerfile` - Usado para criar e configurar o contêiner para o provedor de contexto.
- `requeriments.txt` - Usado para carregar o Flask no contêiner
- `app.py` - Usado para servir o aplicativo Flask.

A pasta **Dummy-device** contém o seguinte:
- `Dockerfile` - Usado para criar e configurar o contêiner para o provedor de contexto.
- `requeriments.txt` - Usado para carregar bibliotecas python no contêiner
- `app.py` - Usado para servir o aplicativo Flask para criar um dispositivo fictício capaz de enviar medições aleatórias e receber comandos

Na pasta `tutorial6` use os seguintes comandos

```bash
docker compose build # Builds all containers and specially the context provider container and dummy-devices container. 

docker compose up -d # Creates all containers. 
```

# Conectando dispositivos IoT

O **Agente IoT** atua como um middleware entre os **dispositivos IoT** e o **agente de contexto**. Portanto, ele precisa ser capaz de criar entidades de dados de contexto com IDs exclusivos. Depois que um serviço é provisionado e um dispositivo desconhecido faz uma medição, o **Agente IoT** adiciona isso ao contexto usando o `<ID do dispositivo>` fornecido (a menos que o dispositivo seja reconhecido e possa ser mapeado para um ID conhecido).

Não há garantia de que cada dispositivo IoT fornecido `<ID do dispositivo>` será sempre exclusivo, portanto, todas as solicitações de provisionamento para o Agente IoT requerem dois cabeçalhos obrigatórios:
- O cabeçalho `fiware-service` é definido para que as entidades de um determinado serviço possam ser mantidas em um banco de dados **mongoDB** separado.
- `fiware-servicepath` pode ser usado para diferenciar entre arrays de dispositivos.

Por exemplo, em um aplicativo de cidade inteligente, você esperaria diferentes cabeçalhos `fiware-service` para diferentes departamentos (por exemplo, parques, transporte, coleta de lixo etc.) e cada `fiware-servicepath` se referiria a um parque específico e assim por diante. Isso significaria que os dados e dispositivos para cada serviço podem ser identificados e separados conforme necessário, mas os dados não seriam isolados - por exemplo, dados de um **lixeira inteligente** dentro de um parque podem ser combinados com a **Unidade GPS** de um caminhão de lixo para alterar a rota do caminhão de maneira eficiente.

A **lixeira inteligente** e o **Unidade GPS** provavelmente vêm de fabricantes diferentes e não pode ser garantido que não haja sobreposição dentro dos `<ID do dispositivo>`s usados. O uso dos cabeçalhos `fiware-service` e `fiware-servicepath` pode garantir que este seja sempre o caso, e permite que o agente de contexto identifique a fonte original dos dados de contexto.

## Provisionando um grupo de serviços

Invocar a provisão de grupo é sempre a primeira etapa na conexão de dispositivos, pois é sempre necessário fornecer uma chave de autenticação com cada medição e o **Agente IoT** não saberá inicialmente em qual URL o agente de contexto está respondendo.

Também é possível configurar comandos e atributos padrão para todos os dispositivos anônimos, mas isso não é feito neste tutorial, pois forneceremos cada dispositivo separadamente.

Este exemplo provisiona um grupo anônimo de dispositivos. Ele informa ao IoT Agent que uma série de dispositivos enviará mensagens para o `IOTA_HTTP_PORT` (onde o IoT Agent está ouvindo comunicações **Northbound**)

>[!info] **Envie a solicitação `Criar serviço`**. 
>Essa solicitação cria um serviço para que dispositivos possam ser adicionados. 

O serviço indicado tem as seguintes características:

```json
{
    "services": [
        {
            "apikey": "4jggokgpepnvsb2uv4s40d59ov",
            "cbroker": "http://orion:1026",
            "entity_type": "Device",
            "resource": "/iot/json"
        }
    ]
}
```

No exemplo, o **Agente IoT** é informado que o endpoint `/iot/json` será usado e que os dispositivos se autenticarão incluindo o token `4jggokgpepnvsb2uv4s40d59ov`. Para um **Agente IoT JSON**, isso significa que os dispositivos enviarão solicitações GET ou POST para:

```
http://iot-agent:7896/iot/json?i=<device_id>&k=4jggokgpepnvsb2uv4s40d59ov
```

Quando uma medição de um dispositivo IoT é recebida na URL do recurso, ela precisa ser interpretada e passada para o **Orion Context Broker**. O atributo `entity_type` fornece um `type` padrão para cada dispositivo que fez uma solicitação (neste caso, os dispositivos anônimos serão conhecidos como entidades `Device`. Além disso, a localização do agente de contexto (`cbroker`) é necessária, para que o **Agente IoT** possa transmitir quaisquer medidas recebidas para o local correto. `cbroker` é um atributo opcional - se não for fornecido, o **Agente IoT** usa a URL do agente de contexto conforme definido no arquivo de configuração, porém foi incluído aqui para completar.

## Provisioning a device
Three types of measurement attributes can be provisioned:

- `attributes` are active readings from the device, meaning that the device will send data periodically to the IoT Agent. 
- `lazy` attributes are only sent on request - The IoT Agent will inform the device to return the measurement. (This is not implemented at the moment or I did not figure out how to work with it)
- `static_attributes` are as the name suggests static data about the device (such as relationships) passed on to the context broker.

> **Note**: in the case where individual `id`s are not required, or aggregated data is sufficient the `attributes` can be defined within the provisioning service rather than individually.

**Send the `Provision a device` request**. This request provision a device with the following characteristics:

## Provisionando um dispositivo

Três tipos de atributos de medição podem ser provisionados:

- `attributes` são leituras ativas do dispositivo, o que significa que o dispositivo enviará dados periodicamente ao **Agente IoT**.
- Atributos `lazy` são enviados somente mediante solicitação - O **Agente IoT** informará o dispositivo para retornar a medição. (Isso não está implementado no momento ou eu não descobri como trabalhar com isso)
- `static_attributes` são, como o nome sugere, dados estáticos sobre o dispositivo (como relacionamentos) passados para o agente de contexto.

> **Observação**: no caso em que os `id`s individuais não são necessários, ou os dados agregados são suficientes, os `attributes` podem ser definidos dentro do serviço de provisionamento ao invés de individualmente.

>[!info] **Envie a solicitação `Provisione um dispositivo`**. 
>Esta solicitação provisiona um dispositivo no **Agente IoT**.

O dispositivo contém as seguintes careacterísticas:

```json
{
    "devices": [
        {
            "device_id": "device001",
            "entity_name": "urn:ngsi-ld:Device:001",
            "entity_type": "Device",
            "transport": "HTTP",
            "endpoint": "http://dummy-device:80/device1",
            "attributes": [
                {
                    "object_id": "t",
                    "name": "temperature",
                    "type": "Number"
                },
                {
                    "object_id": "rh",
                    "name": "relativeHumidity",
                    "type": "Number"
                }
            ],
            "commands": [
                {
                    "name": "switch",
                    "type": "command"
                }
            ],
            "static_attributes": [
                {
                    "name": "refStore",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:Store:001"
                }
            ]
        }
    ]
}
```

Observe que o dispositivo tem 2 atributos (`t` no **Agente IoT** e `temperature` no **Orion Context Broker**; e `rh` no **Agente IoT** e `relativeHumidity` no **Orion Context Broker**) e um comando (**switch**). Um `refStore` é definido como um `static_attribute`, colocando o dispositivo dentro de **Store** `urn:ngsi-ld:Store:001`. Além disso, indica o mecanismo de transporte (HTTP) e o endpoint (URL para o contêiner do **dispositivo dummy**) para enviar comandos aos dispositivos. Espera-se que o endpoint indicado possa manipular a mensagem do **Agente IoT** e retornar uma mensagem para ele.

> Atributos estáticos são úteis como dados adicionais em uma entidade para permitir a consulta usando o parâmetro `q`. Por exemplo, o modelo Smart Data Models [Device](https://github.com/smart-data-models/dataModel.Device/blob/master/Device/doc/spec.md) define atributos como `category` ou ` controladoProperty` que permitem que consultas sejam feitas como:
>
> - _Quais **Atuadores** têm atualmente um nível de bateria baixo?_
>
> `/v2/entities?q=category=="atuador";BatteryLevel<0.1`
>
> - _Quais **dispositivos** que medem o `fillingLevel` foram instalados antes de janeiro de 2020?_
>
> `/v2/entities?q=controledProperty=="fillingLevel";dateInstalled<"2020-01-25T00:00:00.000Z"`
>
> Obviamente, os dados estáticos podem ser estendidos conforme necessário e também podem incluir dados adicionais, como um 'nome' ou 'número de série' exclusivo para cada dispositivo, caso o ID da entidade seja muito inflexível para consultas.
>
> `/v2/entities?q=serialNumber=="XS403001-002"`
>
> Além disso, dispositivos com um atributo estático `location` fixo também podem ser consultados usando os parâmetros Geofencing.
>
> `/v2/entities?georel=near;maxDistance:1500&geometry=point&coords=52.5162,13.3777`

Você pode simular uma medição de dispositivo dummy proveniente do **Dispositivo**. 

>[!info] **Envie a solicitação `Envie dados através do Agente IoT`**. 
>Essa solicitação simula uma medição de temperatura vinda do dispositivo para o **Agent IoT**.

Agora que o **Agent IoT** está conectado, o grupo de serviço definiu o recurso no qual o **Agente IoT** está escutando (`iot/json`) e a chave de API usada para autenticar a solicitação (`4jggokgpepnvsb2uv4s40d59ov`). Uma vez que ambos são reconhecidos, a medição é válida.

Como provisionamos especificamente o dispositivo (`device001`) - o **Agente IoT** pode mapear atributos antes de gerar uma solicitação com o **Orion Context Broker**.

Você pode ver que uma medição foi registrada, recuperando os dados da entidade do agente de contexto. Não se esqueça de adicionar os cabeçalhos `fiware-service` e `fiware-service-path`.

>[!info] **Envie a solicitação `Recupere dispositivo 1`**. 
>Essa solicitação obtém as informações do Dispositivo 1 registrado no **Orion Context Broker**. 

Ao fazer este pedido não esqueça de atribuir corretamente `fiware-service` e `fiware-servicepath`. A resposta é apresentada a seguir.

```json
{
    "id": "urn:ngsi-ld:Device:001",
    "type": "Device",
    "TimeInstant": "2022-10-07T17:22:03.183Z",
    "refStore": "urn:ngsi-ld:Store:001",
    "relativeHumidity": 50,
    "switch_info": " ",
    "switch_status": "UNKNOWN",
    "temperature": 10,
    "switch": ""
}
```

A resposta mostra que o dispositivo **device** com `id=device001` foi identificado com sucesso pelo IoT Agent e mapeado para a entidade `id=urn:ngsi-ld:Device:001`. Essa nova entidade foi criada dentro dos dados de contexto no **Orion Context broker**. O atributo `t` da solicitação de medição do dispositivo fictício foi mapeado para o atributo `temperature` mais significativo dentro do contexto. Como você notará, um atributo `TimeInstant` foi adicionado à entidade e aos metadados do atributo - isso representa a última vez que a entidade e o atributo foram atualizados e é adicionado automaticamente a cada nova entidade porque o `IOTA_TIMESTAMP` A variável de ambiente foi definida quando o **Agente IoT** foi iniciado. O atributo `refStore` vem do conjunto `static_attributes` quando o dispositivo foi provisionado.

# Ativando a comunicação do agente de contexto

Após conectar o IoT Agent aos dispositivos IoT, o Orion Context Broker foi informado de que os comandos já estão disponíveis. Em outras palavras, o Agente IoT se registrou como um [Provedor de Contexto](https://github.com/FIWARE/tutorials.Context-Providers/) para os atributos de comando.

Uma vez cadastrados os comandos será possível ativá-los enviando requisições ao **Orion Context Broker**, ao invés de enviar requisições JSON diretamente aos dispositivos IoT como fizemos anteriormente.

Todas as comunicações que saem e chegam ao porto norte do **Agente IoT** usam a sintaxe NGSI padrão. O protocolo de transporte usado entre os dispositivos IoT e o **IoT Agent** é irrelevante para essa camada de comunicação. Efetivamente, o **Agente IoT** está oferecendo um padrão de fachada simplificado de endpoints conhecidos para acionar qualquer dispositivo.

## Comunicação entre dispositivos, IoT Agent e Orion Context Broker.

Antes de conectar os 3 componentes, é importante entender as mensagens entre cada um deles. Existem dois tipos principais de comunicação: Mensagem Norte (medições) e Mensagem sul (Comandos).

### Mensagem Norte - Para medições

O esquema abaixo apresenta a comunicação para medições no sentido norte.

![[FIWARE Northbound measurement - Messages.png]]

#### Mensagem 1

O dispositivo envia uma medição para o **Agente IoT JSON** com os parâmetros `k` (chave secreta) e `i` (ID do dispositivo no **Agente IoT**) na URL. O corpo da mensagem é o valor das medidas com o nome no **Orion Context Broker** ou no **Agente IoT JSON**.

#### Mensagem 2

O **Agente IoT JSON** encaminha as medições para o **Orion Context Broker**. Essa mensagem é semelhante a uma solicitação PUT para atualizar o valor de atributos específicos no **Orion Context Broker**.

### Mensagem Sul - Para comandos
O esquema abaixo apresenta a comunicação para os comandos Southbound:

![[FIWARE southbount command - messages.png]]

#### Mensagem 1

A primeira mensagem é uma solicitação PATCH para o **Orion Context Broker**. Esta solicitação deve ter a URL `http://localhost:1026/v2/entities/<device-id>/attrs?type=<entity type>` e deve ter o `fiware-service` e o `fiware-servicepath` corretos . O corpo da mensagem deve ser algo semelhante a:

```json
{
    "<command name>": {
        "type": "command",
        "value": "<command value>"     
    }
}
```

#### Mensagem 2

Quando o **Orion Context Broker** recebe a `mensagem 1`, ele encaminha esta mensagem para o **Agente IoT JSON** como uma solicitação POST.

Quando o **Agente IoT JSON** recebe esta mensagem, ele envia uma resposta ao **Orion Context Broker** indicando que o comando está PENDENTE porque o**Agente IoT JSON** ainda não enviou uma mensagem ao dispositivo ou não encontrou um erro como, por exemplo, um dispositivo não está registrado.

#### Mensagem 3

O **Agente IoT JSON** envia uma solicitação POST para o dispositivo. Essa URL é registrada ao criar a entidade `device` no **Agente IoT JSON**. A solicitação POST tem o seguinte corpo de mensagem:

```json
{
    "<command name>": "<command value>"
}
```

Essa solicitação deve ser tratada adequadamente pelo dispositivo.

#### Mensagem 4

Quando o dispositivo recebe `mensagem 3`, ele deve manipular o comando. Esta lógica deve ser implementada no dispositivo. Quando o comando for concluído, o dispositivo deverá responder ao **Agente IoT JSON** com o código de status apropriado (200 se estiver ok, por exemplo) e um corpo de mensagem com o seguinte:

```json
{
    "<command name>": "<command status/message>"
}
```

Essa mensagem pode ser sempre que o usuário achar interessante apresentar.

#### Mensagem 5

Quando o **Agente IoT JSON** recebe a mensagem 4, ele envia de volta ao **Orion Context Broker** para atualizar o atributo `command_status` com as informações `<command status/message>`.

## Conectando os serviços

O tutorial fornece um contêiner **dummy-device** que cria um servidor web simples utilizando o framework Flask. O arquivo `app.py` na pasta `dummy-device` indica como o servidor web foi programado. Este arquivo tem dois propósitos principais:
- Envie medições aleatórias de temperatura e umidade relativa a cada 5 segundos.
- Receber um comando para iniciar ou parar o envio de medições.

>[!info] **Envie a solicitação `Enviar comando "swicth" pelo Orion`**. 
>Essa solicitação envia um comando ao Orion Context Broker 

O corpo da mensagem é o seguinte:

```json
{
    "switch": {
        "type": "command",
        "value": ""     
    }
}
```

O **Orion Context Broker** sabe que o `device001` está registrado no **Agente IoT** e encaminha esta mensagem para ele. O **Agente IoT** sabe que a URL `http://dummy-device:80/device1` é capaz de lidar com esta mensagem, então ele envia uma solicitação POST com o seguinte corpo de mensagem:

```json
{
    "switch": ""     
}
```

> Se um `value` for fornecido ao comando no **Orion Context Broker**, ele será apresentado na mensagem acima. É importante destacar que para que isso seja verdade a requisição ao **Orion Context Broker** ***deve*** conter o tipo da entidade em seus parâmetros. Veja a solicitação `Enviar comando "swicth" pelo Orion` para detalhes.

Assim que o contêiner **dummy-device** recebe essa mensagem, ele começa a enviar medições aleatórias de temperatura a cada 5 segundos para o **Agente IoT JSON**, conforme indicado na função `sendData` no arquivo `app.py`. Observe que o comando `switch` alterna o envio de dados entre os estados ligado e desligado.

>[!info] **Envie várias solicitações de "Obter dispositivo 1"** de tempos em tempos.
> Esta solicitação recupera as informações de contexto para o dispositivo 1.

Observe que a cada 5 segundos os valores de temperatura e umidade relativa no Orion Context Broker mudam aleatoriamente. O corpo da mensagem abaixo é um exemplo do dispositivo com valores aleatórios:

```json
{
    "id": "urn:ngsi-ld:Device:001",
    "type": "Device",
    "TimeInstant": "2022-10-07T17:22:48.169Z",
    "refStore": "urn:ngsi-ld:Store:001",
    "relativeHumidity": 15,
    "switch_info": "Started sending data",
    "switch_status": "OK",
    "temperature": 17,
    "switch": ""
}
```

# # Conclusão

O **Agente IoT** é um componente importante para permitir que o **Orion Context Broker** se comunique com diferentes dispositivos com diferentes protocolos de comunicação. Existem **Agentes IoT** para protocolos como JSON, Ultralight, LoRaWan, OPC UA e outros.

:: **Referência** :: [IoT Agent (JSON) - Step-by-Step for NGSI-v2](https://fiware-tutorials.readthedocs.io/en/latest/iot-agent-json.html)