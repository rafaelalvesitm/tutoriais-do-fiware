# Introdução

Este tutorial fornece ao usuário um cenário de caso de uso e demonstra como conectar a plataforma FIWARE e um Raspberry Pi enviando dados para a plataforma.

# Requisitos 

>[!info] Antes de começar os tutoriais faça o seguinte:
> - Instale o [Docker, Docker compose](https://www.docker.com/)  e o [Postman](https://www.postman.com/downloads/). 
>- Baixe ou clone o [Repositório do GitHub](https://github.com/rafaelalvesitm/tutoriais-do-fiware).
>- Importe o arquivo `Tutoriais do Fiware.postman_collection.json` para o Postman.
>- Abra o Docker no computador.
>- Abra o Postman Agent no computador. 

Também é necessário que se utilize o seguinte hardware:
- Raspberry Pi que possua o capacidade de utilizar o wi-fi (**Pi 3 A+, 3 B, 3 B+, 4 B e Zero W**)
- DHT22 ou DHT11 - Sensor de temperatura e umidade.
- Jumpers - Cabos.
- Protoboard - Útil para gerar protótipos de circuitos elétricos. 

# Arquitetura

Este aplicativo se baseia nos componentes criados em tutoriais anteriores. Ele fará uso de dois componentes FIWARE - o [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) e o [IoT Agent for JSON](https://fiware-iotagent- json.readthedocs.io/en/latest/). O uso do **Orion Context Broker** é suficiente para que um aplicativo se qualifique como _“Powered by FIWARE”_. Tanto o **Orion Context Broker** quanto o **Agente IoT** contam com a tecnologia de código aberto [MongoDB](https://www.mongodb.com/) para manter a persistência das informações que possuem.

Portanto, a arquitetura geral consistirá nos seguintes elementos:
- O FIWARE [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) que receberá solicitações usando [NGSI-v2](https://fiware.github.io/specifications/OpenAPI /ngsiv2).
- O FIWARE [IoT Agent for JSON](https://fiware-iotagent-json.readthedocs.io/en/latest/) que receberá solicitações no sentido sul usando [NGSI-v2](https://fiware.github.io /specifications/OpenAPI/ngsiv2) e convertê-los em comandos [JSON](https://fiware-iotagent-json.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual) para os dispositivos.
- O banco de dados subjacente [MongoDB](https://www.mongodb.com/):
    - Usado pelo **Orion Context Broker** para armazenar informações de dados de contexto, como entidades de dados, assinaturas e registros.
    - Usado pelo **Agente IoT** para armazenar informações do dispositivo, como URLs e chaves do dispositivo.
- O **Raspberry Pi**:
	- Usado para enviar dados coletados do DHT22 para o **Orion Context Broker**.
	- Receber comandos para iniciar e parar o envio de dados; e alterar o intervalo de coleta de dados.
- **Cygnus**: Persiste dados do **Orion Context Broker** para bancos de dados externos.
- **MySQL**: Banco de dados de relacionamento usado para armazenar dados.
- **Grafana**: cria um dashboard para visualizar os dados coletados pela IoT Platform.

Como todas as interações entre os elementos são iniciadas por solicitações HTTP, as entidades podem ser disponibilizados em contêineres e executadas a partir de portas expostas. A arquitetura a seguir é usada neste tutorial.

![[FIWARE tutorial - Raspberry Pi example.png]]

# Start Up

Para iniciar os contêineres, abra o código no Visual Studio e abra a pasta `tutorial7`. Na pasta está um arquivo `docker-compose`, uma pasta chamada `raspberry`.

A pasta **raspberry** contém:
- `app.py` - Arquivo usado para criar um aplicativo de frasco usado para receber comandos e enviar dados para o **Agente IoT JSON**.

Na pasta `tutorial7` use os seguintes comandos

```bash
docker compose build # Builds all containers and specially the context provider container and dummy-devices container. 

docker compose up -d # Creates all containers. 

```

# Usando o Raspberry Pi

Os primeiros passos para usar um Raspberry Pi estão fora do escopo deste tutorial. Os usuários são incentivados a seguir este link [Documentação do Raspberry Pi - Introdução](https://www.raspberrypi.com/documentation/computers/getting-started.html) para entender como começar a usar o Raspberry Pi.

É importante que os usuários conectem o Raspberry Pi e o computador local (usado para criar os contêineres) na mesma rede. Também é importante saber o endereço IP do Raspberry Pi e do computador local. isso pode ser feito usando os comandos `ifconfig` ou `ipconfig` dependendo do sistema operacional utilizado nos dispositivos.

Os usuários podem acessar o Raspberry Pi de duas maneiras:
- ATRAVÉS de um monitor externo e um cabo HDMI;
- Via SSH sabendo o endereço IP do raspberry Pi.

Uma vez no Raspberry Pi, os usuários devem abrir uma janela de terminal e copiar o arquivo `app.py` localizado na pasta `tutorial7/raspberry` fornecida no repositório GitHub para uma pasta no Raspberry Pi. Antes de usar este arquivo os usuários devem instalar o flask usando o comando `pip install flask`

Depois disso, os usuários podem iniciar o servidor no Raspberry Pi usando o seguinte comando:

```bash
flask run --host=0.0.0.0
```

O sinalizador `--host=0.0.0.0` permite que o servidor Web Flask fique visível na rede e, como tal, visível para o **Agente IoT JSON**.

# Configurando o sistema

Para poder conectar o Raspberry Pi ao **Orion Context Broker**, os usuários devem usar o **IoT Agent JSON** como um serviço intermediário. Isso não é exatamente necessário, mas é recomendado, pois os IoT Agents são usados como uma ponte de comunicação entre os dispositivos e o **Orion Context Broker** que são capazes de traduzir diferentes protocolos de dispositivos para o protocolo NGSI-V2 usado no **Orion Context Broker**.

>[!info] **Envie a solicitação `Criar serviço`**. 
>Essa solicitação cria um serviço no **Agente IoT** para poder criar dispositivos. 

Observe o seguinte corpo JSON usado na solicitação:

```json
{
 "services": [
   {
     "apikey":      "4jggokgpepnvsb2uv4s40d59ov1",
     "cbroker":     "http://orion:1026",
     "entity_type": "Device",
     "resource":    "/iot/json"
   }
 ]
}
```

Este corpo indica que entidades do tipo `DHT22` devem usar uma `api-key` com o valor `4jggokgpepnvsb2uv4s40d59ov1`. Essa chave de API é usada para autenticar dispositivos que enviam dados para a plataforma. Observe que o valor `cbroker` representa o endereço IP do **Orion Context Broker**.

Para registrar um dispositivo, deve-se enviar uma solicitação POST para o **IoT Agent JSON**. 

>[!info] **Envie a solicitação `Criar dispositivo`**. 
>Essa solicitação cria um novo dispositivo no **Orion Context Broker**. 

Observe o seguinte corpo da mensagem:

```json
{
    "devices": [
        {
            "device_id": "device_001",
            "entity_name": "urn:ngsi-ld:DHT22:001",
            "entity_type": "Device",
            "timezone": "America/Sao_Paulo",
            "transport": "HTTP",
            "endpoint": "http://10.42.0.94:5000/dht22",
            "protocolo": "PDI-IoTA-JSON",
            "attributes": [
                {
                    "object_id": "t",
                    "name": "temperature",
                    "type": "Number"
                },
                {
                    "object_id": "h",
                    "name": "humidity",
                    "type": "Number"
                }
            ],
            "commands": [
                {
                    "name": "start",
                    "type": "command",
                    "value": ""
                },
                {
                    "name": "stop",
                    "type": "command",
                     "value": ""
                },
                {
                    "name": "interval",
                    "type": "command",
                    "value": ""
                }
            ]
        }
    ]
}
```

Observe os seguintes parâmetros:
- `"device_id": "device_001"` - Registra este ID de dispositivo no **IoT Agent JSON**.
- `"entity_name": "urn:ngsi-ld:Device:001"` - Registra uma entidade com este ID no **Orion Context Broker**. Também cria uma assinatura no **Orion Context Broker** para corresponder essa entidade à do **IoT Agent JSON**.
- `"entity_type": "Device"` - Indica o tipo da entidade.
- `"timezone": "America/Sao_Paulo"` - Indica que o timestamp usado no **Orion Context Broker** deve corresponder a este fuso horário.
- `"transport": "HTTP"` - Indica que o protocolo de transporte HTTP será utilizado. Pode ser um protocolo MQTT, conforme usado nos tutoriais anteriores.
- `"endpoint": "http://10.42.0.94:5000/device/001"` - Indica que o dispositivo está localizado no endereço IP `10.42.0.94` e na porta `5000`. O endereço IP é o endereço IP do Raspberry Pi e a porta é a porta padrão para o servidor web Flask. A rota `device/001` é usada pois estamos especificando apenas um dispositivo dht22
- `"protocolo": "PDI-IoTA-JSON"` - Indica que o dispositivo vai se comunicar usando o protocolo JSON. Pode ser Ultralight conforme indicado nos tutoriais anteriores.
- `lista de "atributos"` - Indica os atributos que este dispositivo é capaz de enviar.
- `lista de comandos` - Indica os comandos que este dispositivo é capaz de receber.

É importante observar que os usuários podem criar entidades para receber dados e entidades para enviar comandos no **Agente IoT JSON**. Não é necessário criar entidades com atributos e comandos na mesma entidade. Quando essa entidade é criada no **Agente IoT JSON**, uma entidade também é criada no **Orion Context Broker**.

**Envie a solicitação "Obter entidades"**. Essa solicitação obtém todas as entidades registradas no **Orion Context Broker**. Observe que uma entidade foi criada.

**Envie a solicitação `Get registrations`**. Essa solicitação obtém todos os registros registrados no **Orion Context Broker**. Observe que há um create para que o Orion saiba que os dados dos atributos da entidade cadastrada em si devem ser fornecidos pelo **Agente IoT JSON**.

**Envie a solicitação `Criar registro`**. Essa solicitação cria um registro para indicar que os dados de temperatura e umidade relativa enviados pelo Raspberry e Recebidos no **Orion Context Broker** devem ser enviados ao banco de dados **MySQL** para criar um dado histórico.

## Enviando comandos para o dispositivo

>[!info] **Envie a solicitação `Alterar estado`**. 
>Essa solicitação notifica o Raspberry Pi que ele deve começar ou parar de enviar dados para o **Orion Context Broker**. Esse comando altera entre os dois estados. 

>[!info] **Envie a solicitação `Alterar intervalo`**. 
>Essa solicitação notifica o Raspberry Pi que ele deve alterar o intervalo para enviar dados para o padrão de 5 segundos a 2 segundos.

Para verificar que a Raspberry está funcionando faça o seguinte:

>[!info] Envie multiplas solicitações `Obter dispositivo`
>Essas solicitações recuperam as informações do dispositivo no **Orion Context Broker**. Várias mensagens são necessárias para avaliar se os valores estão sendo alterados. 

# Entendendo o que está acontecendo entre o Orion Context Broker e o dispositivo

O diagrama abaixo indica a comunicação entre o **Orion Context Broker** e o **Raspberry Pi**.

![[FIWARE Tutorial - Communication between Orion and Devices.png]]

A comunicação entre cada componente é a seguinte:

## Comunicação 1

Uma solicitação PATCH é enviada do **Postman** (representando um aplicativo de usuário) para o **Orion Context Broker** com a seguinte mensagem:

```bash
curl --location --request PATCH 'http://localhost:1026/v2/entities/urn:ngsi-ld:Device:001/attrs?type=Device' \
--header 'fiware-service: verticalfarm' \
--header 'fiware-servicepath: /prototype' \
--header 'Content-Type: application/json' \
--data-raw '{
  "start": {
      "type" : "command",
      "value" : ""
  }
}'
```

Essa solicitação indica que a seguinte URL `http://localhost:1026/v2/entities/urn:ngsi-ld:Device:001/attrs?type=Device` será usada. Essa URL representa a entidade DHT22 no **Orion Context Broker**. Os cabeçalhos são parâmetros usados para criar multilocação no **Orion Context Broker** e para indicar que o corpo da mensagem está em JSON. O `data-raw` indica a mensagem do corpo da solicitação. Esta mensagem de corpo apresenta um comando `start` com um valor vazio.

Ao receber esta mensagem o **Orion Context Broker** valida se a entidade atual possui o comando indicado. Em caso afirmativo, ele examinará seus registros para ver para onde encaminhar o comando. No nosso caso, deve ser o **IoT Agent JSON**.

## Comunicação 2

O **Orion Context Broker** cria a seguinte mensagem

```jSON
POST http://iot-agent-json:4041/op/update, request payload (137 bytes): 
{
	"entities":[
		{
			"id":"urn:ngsi-ld:Device:001",
			"type":"Device",
			"switch":{
				"type":"command",
				"value":"",
				"metadata":{}
			}
		}
	],
	"actionType":"update"
}
```

Esta mensagem é enviada para o **Agente IoT JSON**. Quando o **Agente IoT JSON** recebe esta mensagem, ele responde ao **Orion Context Broker** indicando que a mensagem foi recebida. Em seguida, o **Orion Context Broker** altera a propriedade `<command>_status_` para `PENDING`. Em seguida, o **Agente IoT JSON** verifica se um dispositivo está registrado para encaminhar o comando.

## Comunicação 3

O **Agente IoT JSON** envia a solicitação ao dispositivo. O corpo da mensagem é o seguinte:

```json
{
	"<command name>":"<command value>"
}
```

No nosso caso, pode ser um comando com um dos seguintes:

```json
{
	"switch":""
}
{
	"interval":"2"
}
```

O dispositivo recebe esta mensagem na rota `/Device/001` e deve agir com base no corpo da mensagem recebida. Isso deve ser escrito anteriormente no arquivo `app.py` escrito no **Raspberry Pi**.

## Comunicação 4

Após concluir o processamento do comando, o **Raspberry Pi** deve responder à solicitação POST **Agente IoT JSON** com o código de status apropriado (200 se tudo estiver bem) e um corpo de mensagem semelhante ao seguinte:

```json
{
	"<command name>":"<command info>"
}
```

Observe que essa comunicação também pode ser usada para enviar leituras de temperatura e umidade relativa do Raspberry Pi para o **Agente IoT JSON**. Se este for o caso, a seguinte mensagem é usada:

```bash
curl --location --request POST 'http://fiware-iot-agent-json:7896/iot/json?k=4jggokgpepnvsb2uv4s40d59ov&i=device001' \
--header 'Content-Type: application/json' \
--data-raw '{
	"t": f"{temperature}",
	"rh": f"{humidity}"
}'
```

Observe que os parâmetros `temperature` e `humidity` são coletados do **Raspberry Pi** que reúne essas informações de um sensor DHT22.

## Comunicação 5

O **Agente IoT JSON** recebe a mensagem de resposta do dispositivo e encaminha os resultados para o **Orion Context Broker**. Se tudo correu bem, a seguinte mensagem é criada no **Agente IoT JSON** e enviada para o **Orion Context Broker**

```bash
curl --location --request PATCH 'http://orion:1026/v2/entities/urn:ngsi-ld:Device:001/attrs?type=Device' \
--header 'Content-Type: application/json' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /'
--data-raw '{
	"<command_name>_status": "<status>",
	"<command_name>_info": "<info>"
}'
```

Se uma leitura for recebida pelo **Agente IoT JSON**, a seguinte mensagem será criada:

```bash
curl --location --request PATCH 'http://orion:1026/v2/entities/urn:ngsi-ld:Device:001/attrs?type=Device' \
--header 'Content-Type: application/json' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /'
--data-raw '{
	"<temperature": 21,
	"relativeHumidity": 15
}'
```

Depois que o **Orion Context Broker** recebe a mensagem do **Agente IoT JSON**, ele atualiza as informações de Contexto atuais para a entidade que representa o DHT22. O seguinte JSON representa esta entidade com as informações de atualização

```json
{
	"temperature": {
		"type": "Number",
		"value": 21,
		"metadata": {
			"TimeInstant": {
				"type": "DateTime",
				"value": "2022-10-14T19:22:34.346Z"
			}
		}
	},
	"relativeHumidity": {
		"type": "Number",
		"value": 15,
		"metadata": {
			"TimeInstant": {
				"type": "DateTime",
				"value": "2022-10-14T19:22:34.346Z"
			}
		}
	},
	"refStore": {
		"type": "Relationship",
		"value": "urn:ngsi-ld:Store:001",
		"metadata": {
			"TimeInstant": {
				"type": "DateTime",
				"value": "2022-10-14T19:22:34.346Z"
			}
		}
	},
	"TimeInstant": {
		"type": "DateTime",
		"value": "2022-10-14T19:22:34.346Z"
	}
}
```


# Persistindo e visualizando dados

## Dados persistentes no banco de dados

Para persistir os dados, o componente **Cygnus** é usado. Este componente recebe uma notificação do **Orion Context Broker** e a salva no banco de dados indicado no arquivo `docker-compose.yml`. Neste caso, o banco de dados **MySQL** é usado. Para utilizar este mecanismo é necessário criar uma assinatura/registro no **Orion Context Broker**. Isso já foi feito neste tutorial, então nada de novo é necessário.

>[!info] Envie a solicitação `Assinar a mudanças no contexto`
>Esta soliticação gera uma assinatura do **Cygnus** no **Orion Context Broker**. Essa assinatura fará com que o **Cygnus** seja notificado sempre que o valor da temperatura seja alterado. 

Para entender melhor o que está acontecendo, o corpo da mensagem JSON a seguir é enviado do **Orion Context Broker** para o **Cygnus** sempre que a leitura de temperatura ou umidade relativa muda no **Orion Context Broker**.

```json
{
  "data": [
    {
      "id": "urn:ngsi-ld:Device:001",
      "temperature": {
        "metadata": {},
        "type": "Integer",
        "value": 70
      },
      "relativeHumidity": {
        "metadata": {},
        "type": "Integer",
        "value": 70
      }
      "type": "Device"
    }
  ],
  "subscriptionId": "633ebd2c1007af0e6472062b"
}
```

## Visualizando dados

Para visualizar os dados é utilizado o componente **Grafana**. Este componente é melhor descrito no tutorial anterior. Como conectar e criar um painel não é fornecido neste tutorial. Os usuários são incentivados a criar um painel com dois gráficos: um para temperatura e outro para umidade relativa. Para consultar o banco de dados com essas informações, use as seguintes consultas

Para a temperatura

```SQL
SELECT 
  UNIX_TIMESTAMP(recvTime) as "time",
  CAST(attrValue as decimal(5,2)) as "value" 
FROM `urn_ngsi-ld_Device_001_Device` 
WHERE attrName = "temperature"
ORDER BY "time"
```

Para a umidade relativa:

```SQL
SELECT 
  UNIX_TIMESTAMP(recvTime) as "time",
  CAST(attrValue as decimal(5,2)) as "value" 
FROM `urn_ngsi-ld_Device_001_Device` 
WHERE attrName = "relatveHumidity"
ORDER BY "time"
```

Um dashboard semelhante ao abaixo deve ser criado.

![[Tutorial FIWARE - dashboard de caso de uso.png]]

Neste caso eu deixei a Raspberry Pi funcionando por alguns minutos e coloquei os meus dedos em volta do sensor de umidade e temperatura relativa DHT22. Como os meus dedos são mais quentes do que a temperatura ambiente o sensor de temperatura responde lentamente ao aumento da temperatura e depois lentamente quando eu retiro os dedos do sensor. Já o sensor de umidade tem uma resposta mais rápida pois depende apenas do ar presente em volta do sensor. 

# Conclusão 

Este tutorial fornece aos usuários uma compreensão básica sobre como conectar dispositivos com a FIWARE IoT Platform. Os usuários são incentivados a continuar desenvolvendo soluções inteligentes usando a plataforma e outros dispositivos.