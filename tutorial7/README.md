# Introdução

Este tutorial apresenta o uso do protocolo MQTT em dispositivos IoT que se conectam ao FIWARE. O [Agente IoT UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual) é usado para se comunicar com um conjunto de dispositivos IoT fictícios usando MQTT por meio de um agente de mensagens [Mosquitto](https://mosquitto.org/).

# Requisitos

>[!info] Antes de começar os tutoriais faça o seguinte:
> - Instale o [Docker, Docker compose](https://www.docker.com/)  e o [Postman](https://www.postman.com/downloads/). 
>- Baixe ou clone o [Repositório do GitHub](https://github.com/rafaelalvesitm/tutoriais-do-fiware).
>- Importe o arquivo `Tutoriais do Fiware.postman_collection.json` para o Postman.
>- Abra o Docker no computador.
>- Abra o Postman Agent no computador. 

# Vídeo do tutorial

<iframe width="100%" height=100% style="aspect-ratio: 16/9" src="https://www.youtube.com/embed/5LAg3Wvvsrk" allowfullscreen></iframe>

Caso o player não funcione utilize o link: [IoT Agent Ultralight sobre MQTT - Tutoriais do FIWARE #8 - YouTube](https://www.youtube.com/watch?v=5LAg3Wvvsrk)

## O que é MQTT?

O MQTT é um protocolo de mensagens baseado em publicação-assinatura usado na Internet das Coisas. Ele funciona em cima do protocolo TCP/IP e é projetado para conexões com locais remotos onde é necessária uma "pequena área de cobertura de código" ou a largura de banda da rede é limitada. O objetivo é fornecer um protocolo que seja eficiente em largura de banda e use pouca energia da bateria.

O tutorial anterior usou HTTP como mecanismo de transporte entre os dispositivos e o **Agente IoT**. O HTTP usa um paradigma de solicitação/resposta em que cada dispositivo se conecta diretamente ao **Agente IoT**. O MQTT é diferente, pois publicar-assinar é orientado a eventos e envia mensagens aos clientes. Requer um ponto de comunicação central adicional (conhecido como **broker MQTT**) que é responsável por despachar todas as mensagens entre os remetentes e os destinatários legítimos. Cada cliente que publica uma mensagem para o broker inclui um **tópico** na mensagem. O **tópico** são as informações de roteamento para o broker. Cada cliente que deseja receber mensagens assina um determinado **tópico** e o corretor entrega todas as mensagens com o **tópico** correspondente ao cliente. Portanto, os clientes não precisam se conhecer, eles apenas se comunicam pelo **tema**. Essa arquitetura permite soluções altamente escaláveis sem dependências entre os produtores de dados e os consumidores de dados.

O **Agente IoT UltraLight 2.0** só enviará ou interpretará mensagens usando a sintaxe [UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual), no entanto, pode ser usado para enviar e receber mensagens através de vários mecanismos de **transporte**. Portanto, podemos usar o mesmo ativador genérico FIWARE para conectar a uma gama mais ampla de dispositivos IoT.

## Broker Mosquitto MQTT

[Mosquitto](https://mosquitto.org/) é um **broker MQTT** de código aberto prontamente disponível que será usado durante este tutorial. Está disponível licenciado sob EPL/EDL. Mais informações podem ser encontradas em https://mosquitto.org/

## Arquitetura

Este aplicativo se baseia nos componentes criados em tutoriais anteriores. Ele fará uso de dois componentes FIWARE - o [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) e o [IoT Agent for UltraLight 2.0](https://fiware-iotagent -ul.readthedocs.io/en/latest/). O uso do **Orion Context Broker** (com dados de contexto adequados fluindo por ele) é suficiente para que um aplicativo seja qualificado como _“Powered by FIWARE”_. Tanto o **Orion Context Broker** quanto o **Agente IoT** contam com a tecnologia de código aberto [MongoDB](https://www.mongodb.com/) para manter a persistência das informações que possuem. Também usaremos os dispositivos IoT fictícios criados no tutorial anterior, mas adaptados para trabalhar com MQTT. Além disso, adicionaremos uma instância do broker [Mosquitto](https://mosquitto.org/) MQTT que é de código aberto e está disponível sob o EPL/EDL.

Portanto, a arquitetura geral consistirá nos seguintes elementos:

- O FIWARE [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) que receberá solicitações usando [NGSI-v2](https://fiware.github.io/specifications/OpenAPI /ngsiv2)
- O FIWARE [IoT Agent for UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/) que irá:
    - Receber solicitações do sul usando [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2) e convertê-las para [UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/ pt/latest/usermanual/index.html#user-programmers-manual) Tópicos MQTT para o MQTT Broker
    - Ouvir o **MQTT Broker** sobre tópicos registrados para enviar medições para o norte
- O [Mosquitto](https://mosquitto.org/) **MQTT Broker** que atua como um ponto de comunicação central, passando tópicos MQTT entre o **Agente IoT** e os dispositivos IoT conforme necessário.
- O banco de dados subjacente [MongoDB](https://www.mongodb.com/):
    - Usado pelo **Orion Context Broker** para armazenar informações de dados de contexto, como entidades de dados, assinaturas e registros
    - Usado pelo **Agente IoT** para armazenar informações do dispositivo, como URLs e chaves do dispositivo
- Um servidor web atuando como um conjunto de dispositivos IoT fictícios usando o protocolo [UltraLight 2.0](https://fiware-iotagent- ul.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual) rodando sobre MQTT.

Como todas as interações entre os elementos são iniciadas por solicitações HTTP ou MQTT sobre TCP, as entidades podem ser disponibilizadas em contêineres e executadas a partir de portas expostas.

As informações de configuração necessárias para conectar o Mosquitto MQTT Broker, os dispositivos IoT e o **Agente IoT** podem ser vistas na seção de serviços do arquivo `docker-compose.yml` disponibilizado. Abaixo destaca-se os elementos principais. 

### Configuração do Mosquitto

```yml
mosquitto:
    image: eclipse-mosquitto
    hostname: mosquitto
    container_name: mosquitto
    networks:
        - default
    expose:
        - "1883"
        - "9001"
    ports:
        - "1883:1883"
        - "9001:9001"
```

O contêiner `mosquitto` está escutando em duas portas:

- A porta `1883` é exposta para que possamos postar tópicos MQTT.
- A porta `9001` é a porta padrão para comunicações HTTP/Websocket.

### Configuração do Agente IoT para UltraLight 2.0

O [Agente IoT para UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/) pode ser instanciado em um contêiner do Docker. Uma imagem oficial do Docker está disponível no [Docker Hub](https://hub.docker.com/r/fiware/iotagent-ul/) com a tag `fiware/iotagent-ul`. A configuração necessária pode ser vista abaixo:

```yml
iot-agent-ul:
    image: fiware/iotagent-ul:latest
    hostname: iot-agent-ul
    container_name: fiware-iot-agent-ul
    depends_on:
        - mongo-db
    networks:
        - default
    expose:
        - "4042"
    ports:
        - "4042:4042"
    environment:
        - IOTA_CB_HOST=orion
        - IOTA_CB_PORT=1026
        - IOTA_NORTH_PORT=4042
        - IOTA_REGISTRY_TYPE=mongodb
        - IOTA_LOG_LEVEL=DEBUG
        - IOTA_TIMESTAMP=true
        - IOTA_CB_NGSI_VERSION=v2
        - IOTA_AUTOCAST=true
        - IOTA_MONGO_HOST=mongo-db
        - IOTA_MONGO_PORT=27017
        - IOTA_MONGO_DB=iotagentul
        - IOTA_PROVIDER_URL=http://iot-agent-ul:4041
        - IOTA_MQTT_HOST=mosquitto
        - IOTA_MQTT_PORT=1883
```

O contêiner `iot-agent` depende da presença do **Orion Context Broker** e usa um banco de dados **MongoDB** para armazenar informações do dispositivo, como URLs e chaves do dispositivo. O contêiner está escutando em uma única porta:

- A porta `4042` é exposta exclusivamente para acesso ao tutorial - para que cUrl ou Postman possam fazer comandos de provisionamento sem fazer parte da mesma rede.

O contêiner `iot-agent` é controlado por variáveis de ambiente, conforme mostrado:

| Chave | Valor | Descrição |
| --- | --- | --- |
| IOTA\_CB\_HOST | `Orion` | Nome do host do agente de contexto para atualizar o contexto |
| IOTA\_CB\_PORT | `1026` | Porta em que o context broker atende para atualizar o contexto |
| IOTA\_NORTH\_PORT | `4042` | Porta usada para configurar o agente IoT e receber atualizações de contexto do agente de contexto |
| IOTA\_REGISTRY\_TYPE | `mongodb` | Se as informações do dispositivo IoT devem ser mantidas na memória ou em um banco de dados |
| IOTA\_LOG\_LEVEL | `DEBUG` | O nível de log do Agente IoT |
| IOTA\_TIMESTAMP | `true` | Se deve fornecer informações de carimbo de data/hora com cada medição recebida de dispositivos conectados |
| IOTA\_CB\_NGSI\_VERSION | `v2` | Se deve usar NGSI v2 ao enviar atualizações para atributos ativos |
| IOTA\_AUTOCAST | `true` | Certifique-se de que os valores numéricos Ultralight sejam lidos como números e não como strings |
| IOTA\_MONGO\_HOST | `context-db` | O nome do host do mongoDB - usado para armazenar informações do dispositivo |
| IOTA\_MONGO\_PORT | `27017` | A porta mongoDB está escutando |
| IOTA\_MONGO\_DB | `iotagentul` | O nome do banco de dados usado no mongoDB |
| IOTA\_PROVIDER\_URL | `http://iot-agent-ul:4041` | URL passado para o Context Broker quando os comandos são registrados, usado como um local de URL de encaminhamento quando o Context Broker emite um comando para um dispositivo |
| IOTA\_MQTT\_HOST | `mosquito` | O nome do host do MQTT Broker |
| IOTA\_MQTT\_PORT | `1883` | A porta que o MQTT Broker está escutando para receber tópicos |

Como você pode ver, o uso do transporte MQTT é orientado por apenas duas variáveis de ambiente `IOTA_MQTT_HOST` e `IOTA_MQTT_PORT`

# Start Up

Para iniciar os contêineres, abra o código do visual studio e abra a pasta `tutorial7`. Na pasta há um arquivo `docker-compose`, uma pasta chamada `context-provider` e uma pasta chamada `dummy-devices`.

A pasta **context-provider** contém:
- `Dockerfile` - Usado para criar e configurar o contêiner para o provedor de contexto.
- `requeriments.txt` - Usado para carregar o Flask no contêiner
- `app.py` - Usado para servir o aplicativo Flask.

A pasta **Dummy-device** contém o seguinte:
- `Dockerfile` - Usado para criar e configurar o contêiner para o provedor de contexto.
- `requeriments.txt` - Usado para carregar bibliotecas python no contêiner
- `app.py` - Usado para atender o cliente MQTT e criar um dispositivo fictício capaz de enviar medições aleatórias e receber comandos

Na pasta `tutoria7` use os seguintes comandos

```bash
docker compose build # Constrói todos os contêineres e especialmente o contêiner do provedor de contexto e o contêiner de dispositivos fictícios.

docker compose up -d # Cria todos os contêineres.
```

## Verificando a saúde do mosquito

Começaremos imitando as funções do **Agente IoT** e de um dispositivo IoT fictício e enviaremos e receberemos algumas mensagens usando o MQTT. Esta seção do tutorial requer vários terminais abertos.

### Iniciar um Assinante MQTT (1º Terminal)

Eventualmente, uma vez que o sistema tenha sido conectado corretamente, o **Agente IoT** se inscreverá em todos os eventos relevantes para ouvir o tráfego no sentido norte na forma de medições de sensores. Portanto, será necessário fazer uma assinatura em todos os tópicos. Da mesma forma, um atuador deve se inscrever em um único tópico para receber eventos que se efetivam quando os comandos são enviados para o sul. Para verificar se as linhas de comunicação estão abertas, podemos nos inscrever em um determinado tópico e ver que podemos receber algo quando uma mensagem é publicada.

Abra um **novo terminal** e crie um novo contêiner do Docker `mqtt-subscriber` em execução da seguinte maneira:

```bash
docker run -it --rm --name mqtt-subscriber \
  --network fiware_default efrecon/mqtt-client sub -h mosquitto -t "/#"
```

O terminal estará então pronto para receber eventos

### Inicie um Publicador MQTT (2º Terminal)

Um sensor que envia medições no sentido norte publicará essas medições no MQTT Broker para serem repassadas a qualquer assinante que as queira. O sensor não precisará fazer uma conexão direta com o assinante.

Abra um **novo terminal** e execute um contêiner do Docker `mqtt-publisher` para enviar uma mensagem da seguinte forma:

```bash
docker run -it --rm --name mqtt-publisher \
  --network fiware_default efrecon/mqtt-client pub -h mosquitto -m "HELLO WORLD" -t "/test"
```

#### 1º terminal - Resultado:

Se o MQTT Broker estiver funcionando corretamente, a mensagem deve ser recebida no outro terminal

```bash
HELLO WORLD
```

### Parar um Assinante MQTT (1º Terminal)

Para encerrar o assinante do MQTT, execute o seguinte comando do Docker:

```bash
docker stop mqtt-subscriber
```

### Mostrar registro do mosquito

Para mostrar que a comunicação ocorreu por meio do **MQTT Broker**, podemos inspecionar o log do contêiner `mosquitto` Docker conforme mostrado:

```bash
docker logs --tail 10 mosquitto
```

O resultado será algo parecido com o seguinte:

```
1529661883: New client connected from 172.18.0.5 as mqttjs_8761e518 (c1, k0).
1529662472: New connection from 172.18.0.7 on port 1883.
1529662472: New client connected from 172.18.0.7 as mosqpub|1-5637527c63c1 (c1, k60).
1529662472: Client mosqpub|1-5637527c63c1 disconnected.
1529662614: New connection from 172.18.0.7 on port 1883.
1529662614: New client connected from 172.18.0.7 as mosqsub|1-64b27d675f58 (c1, k60).
1529662623: New connection from 172.18.0.8 on port 1883.
1529662623: New client connected from 172.18.0.8 as mosqpub|1-ef03e74b0270 (c1, k60).
1529662623: Client mosqpub|1-ef03e74b0270 disconnected.
1529667841: Socket error on client mosqsub|1-64b27d675f58, disconnecting.
```

## Verificando a integridade do serviço do agente IoT

Você pode verificar se o Agente IoT está em execução fazendo uma solicitação HTTP para a porta exposta:

**Envie o ``**

A resposta será semelhante à seguinte:

```json
{
    "libVersion": "2.6.0-next",
    "port": "4042",
    "baseRoot": "/",
    "version": "1.6.0-next"
}
```

> **E se eu receber uma resposta `Falha ao conectar-se à porta localhost 4041: Conexão recusada`?**
>
> Se você receber uma resposta 'Conexão recusada', o **Agente IoT** não poderá ser encontrado onde esperado para este tutorial - você precisará substituir a URL e a porta em cada comando cUrl pelo endereço IP corrigido. Todos os tutoriais de comandos cUrl assumem que o **Agente IoT** está disponível em `localhost:4042`.
>
> Tente os seguintes comandos:
>
> - Para verificar se os contêineres do docker estão em execução, tente o seguinte: `docker ps`
>	Você deve ver quatro contêineres em execução. Se o **Agente IoT** não estiver em execução, você poderá reiniciar os contêineres conforme necessário. Este comando também exibirá informações de porta aberta.
>
> - Se você instalou o [`docker-machine`](https://docs.docker.com/machine/) e o [Virtual Box](https://www.virtualbox.org/), o agente de contexto, IoT Os contêineres docker Agent e Dummy Device podem estar sendo executados a partir de outro endereço IP - você precisará recuperar o IP do host virtual conforme mostrado: `curl -X GET \ 'http://$(docker-machine ip default):4041/version'`
>
> Como alternativa, execute todos os seus comandos curl de dentro da rede de contêineres: `docker run --network default --rm appropriate/curl -s \ -X GET 'http://iot-agent:4042/iot/about'`

## Conectando dispositivos IoT

O **Agente IoT** atua como um middleware entre os dispositivos IoT e o agente de contexto. Portanto, ele precisa ser capaz de criar entidades de dados de contexto com IDs exclusivos. Depois que um serviço é provisionado e um dispositivo desconhecido faz uma medição, o **Agente IoT** adiciona isso ao contexto usando o `<device-id>` fornecido, a menos que o dispositivo seja reconhecido e possa ser mapeado para um ID conhecido.

Não há garantia de que cada dispositivo IoT fornecido `<device-id>` será sempre exclusivo, portanto, todas as solicitações de provisionamento para o Agente IoT requerem dois cabeçalhos obrigatórios:

- O cabeçalho `fiware-service` é definido para que as entidades de um determinado serviço possam ser mantidas em um banco de dados mongoDB separado.
- `fiware-servicepath` pode ser usado para diferenciar entre arrays de dispositivos.

Por exemplo, em um aplicativo de cidade inteligente, você esperaria diferentes cabeçalhos `fiware-service` para diferentes departamentos (por exemplo, parques, transporte, coleta de lixo etc.) e cada `fiware-servicepath` se referiria a um parque específico e assim por diante. Isso significaria que os dados e dispositivos para cada serviço podem ser identificados e separados conforme necessário, mas os dados não seriam isolados - por exemplo, dados de uma **Lixeira inteligente** dentro de um parque podem ser combinados com a **Unidade GPS** de um caminhão de lixo para alterar a rota do caminhão de maneira eficiente.

A **Lixeira inteligente** e a **Unidade GPS** provavelmente vêm de fabricantes diferentes e não é possível garantir que não haja sobreposição nos `<device-id>`s usados. O uso dos cabeçalhos `fiware-service` e `fiware-servicepath` pode garantir que este seja sempre o caso, e permite que o agente de contexto identifique a fonte original dos dados de contexto.

### Provisionando um grupo de serviços para MQTT

Invocar a provisão de grupo é sempre o primeiro passo para conectar dispositivos. Para comunicação MQTT, o provisionamento fornece a chave de autenticação para que o **Agente IoT** saiba em qual **tópico** ele deve se inscrever.

Também é possível configurar comandos e atributos padrão para todos os dispositivos, mas isso não é feito neste tutorial, pois forneceremos cada dispositivo separadamente.

Este exemplo provisiona um grupo anônimo de dispositivos. Ele informa ao Agente IoT que uma série de dispositivos estará se comunicando enviando medidas de dispositivo sobre o `/ul/4jggokgpepnvsb2uv4s40d59ov` **tópico**

> **Observação** Medidas e comandos são enviados em diferentes tópicos MQTT:
>
> - _Medidas_ são enviados no tópico `/<protocol>/<api-key>/<device-id>/attrs`,
> - _Comandos_ são enviados no tópico `/<api-key>/<device-id>/cmd`,
>
> O raciocínio por trás disso é que, ao enviar medidas no sentido norte do dispositivo para o **Agente IoT**, é necessário identificar explicitamente qual **Agente IoT** é necessário para analisar os dados. Isso é feito prefixando o tópico MQTT relevante com um protocolo, caso contrário, não há como definir qual agente está processando a medida. Esse mecanismo permite que sistemas inteligentes conectem diferentes dispositivos a diferentes **Agentes IoT** de acordo com a necessidade.
>
> Para comandos no sentido sul, essa distinção é desnecessária, pois o **Agente IoT** correto já se registrou para o comando durante a etapa de provisionamento do dispositivo e o dispositivo sempre receberá comandos em um formato apropriado.

O atributo `resource` é deixado em branco porque a comunicação HTTP não está sendo usada.

A localização da URL de `cbroker` é um atributo opcional - se não for fornecido, o Agente IoT usa a URL do agente de contexto padrão conforme definido no arquivo de configuração, mas foi adicionado aqui para completar.

>[!info] **Envie a solicitação `Criar serviço no Agente IoT`**. 
>Esta solicitação cria um grupo de serviços para registrar dispositivos com o tipo `Device`.

### Provisionando um dispositivo

É uma boa prática comum usar URNs seguindo a [especificação NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.04.01_60/gs_cim009v010401p.pdf) ao criar entidades. Além disso, é mais fácil entender nomes significativos ao definir atributos de dados. Esses mapeamentos podem ser definidos provisionando um dispositivo individualmente.

Três tipos de atributos de medição podem ser provisionados:

- `attributes` são leituras ativas do dispositivo
- Atributos `lazy` são enviados apenas mediante solicitação - O Agente IoT informará o dispositivo para retornar a medição (Não suportado no momento ou pelo menos não consegui fazer funcionar)
- `static_attributes` são, como o nome sugere, dados estáticos sobre o dispositivo (como relacionamentos) passados para o agente de contexto.

> **Observação**: no caso em que os `id`s individuais não são necessários, ou os dados agregados são suficientes, os `atributos` podem ser definidos dentro do serviço de provisionamento ao invés de individualmente.

>[!info] **Envie a solicitação `Provisionando um dispositivo`.** 
>Essa solicitação cria um dispositivo capaz de enviar dados de temperatura e umidade relativa e receber dois comandos, sendo um para iniciar ou parar o envio de dados e outro para alterar o intervalo de envio dos dados

Na solicitação estamos associando o dispositivo `device001` com o URN `urn:ngsi-ld:Device:001` e mapeando o dispositivo que lê `t` com o atributo de contexto `temperature` (que é definido como um `Integer`) e um `rh` com o atributo de contexto `relativeHumidity`. Um `refStore` é definido como um `static_attribute`, colocando o dispositivo dentro de **Store** `urn:ngsi-ld:Store:001`.

A adição do atributo `transport=MQTT` no corpo da solicitação é suficiente para informar ao **Agente IoT** que ele deve assinar o `/<api-key>/<device-id>` **tópico** para receber Medidas.

Você pode simular uma medição de dispositivo IoT fictícia proveniente do dispositivo `device001`, postando uma mensagem MQTT no seguinte **tópico** `ul/<api-key/<device id>/attrs`.

> **Observação** No tutorial anterior, ao testar a conectividade HTTP entre o sensor de movimento e um agente IoT, um uma solicitação HTTP fictícia semelhante foi enviada para atualizar o valor `temperature`. Desta vez, o Agente IoT está configurado para ouvir tópicos MQTT e precisamos postar uma mensagem fictícia em um tópico MQTT.

Ao executar usando o protocolo de transporte MQTT, o Agente IoT está assinando os **tópicos** do MQTT. Com o Agente IoT conectado via MQTT, o grupo de serviços definiu o **tópico** no qual o agente está inscrito. Como a chave de API corresponde à raiz do **tópico**, a mensagem MQTT do **dispositivo** é passada para o Agente IoT que se inscreveu anteriormente.

Como provisionamos especificamente o dispositivo (`device001`) - o Agente IoT pode mapear atributos antes de gerar uma solicitação com o Orion Context Broker.

## Habilitando comandos do Orion Context Broker

Após conectar o **Agente IoT** aos dispositivos IoT, o **Orion Context Broker** foi informado de que os comandos já estão disponíveis. Em outras palavras, o **Agente IoT** se registrou como um [Provedor de Contexto](https://fiware-tutorials.readthedocs.io/en/latest/context-providers.html) para os atributos de comando. Uma vez registrados os comandos, será possível enviar o comando para o dispositivo.

Todas as comunicações que saem e chegam ao porto norte do **Agente IoT** usam a sintaxe NGSI padrão. O protocolo de transporte usado entre os dispositivos IoT e o Agente IoT é irrelevante para essa camada de comunicação. Efetivamente, o Agente IoT está oferecendo um padrão de fachada simplificado de endpoints conhecidos para acionar qualquer dispositivo.

>[!info] **Envia a solicitação `Envie o comando Switch através do Orion`.** 
>Essa solicitação envia um comando switch para o dispositivo. Esses comandos devem alternar entre o envio e o não envio de dados.

Você pode alterar o comando `switch` para um comando `interval`. 

>[!info] **Envie a solicitação `Alterar intervalo`**. 
>Esta solicitação altera o intervalo dos dados enviados para 2 segundos

# Conclusão

Este tutorial apresenta usos com a possibilidade de comunicar dispositivos com o Orion Context Broker via comunicação MQTT. É semelhante ao tutorial anterior, mas com uma forma diferente de protocolo de comunicação.

:: **Reference** :: [IoT over MQTT - Step-by-Step for NGSI-v2](https://fiware-tutorials.readthedocs.io/en/latest/iot-over-mqtt.html)