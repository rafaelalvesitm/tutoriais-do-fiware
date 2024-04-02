# Tutoriais FIWARE

Este repositório contém vários tutoriais para usar [FIWARE](https://www.fiware.org/). Todos os tutoriais aqui apresentados são baseados nos [tutoriais fornecidos pelo FIWARE aqui](https://fiware-tutorials.readthedocs.io/en/latest/). Os tutorias aqui desenvolvidos foram criados com objetivo de apresentar a plataforma e suas funcionalidades através de vídeos e treinamentos. 

# Descrição geral

Cada tutorial é dividido em uma determinada pasta aqui dentro deste repositório. Os detalhes de cada tutorial podem ser vistos no [meu site pessoal](https://www.rafaelalvesitm.com/). Estes tutoriais visam demonstrar a utilização dos seguintes componentes:

- FIWARE Orion Context Broker - Gerencidor de contexto e principal elemento da plataforma. 
- FIWARE IoT Agent JSON. - Gerenciador de dispositivos com comunicação HTTP/MQTT e protocolo JSON com a plataforma. 
- FIWARE IoT Agent Ultralight. - Gerenciador de dispositivos com comunicação HTTP/MQTT e protocolo Ultralight com a plataforma. 
- FIWARE Cygnus - Conector entre o Orion Context Broker e bancos de dados relacionais como o MySQL e PostgreSQL. 
- MongoDB database - Banco de dados para armazenamento de informações de configuração e operação dos componentes do FIWARE. 
- MySQL database - Banco de dados para armazenamento de dados históricos dos componentes do FIWARE. 
- Grafana - Aplicação para visualização de gráficos de forma iterativa. 
- Mosquitto MQTT Broker - Broker MQTT para gestão de mensageria entre dispositivos e a plataforma. 
- Context provider - Elemento genérico para disponibilização de informações de contexto, escrito utilizando o framework Flask.
- Dummy-device - Elemento genérico para simulação de um dispositivo, escrito utilizando o framework Flask.

## Tutorial 1 - Introdução ao FIWARE

Este tutorial fornece ao usuário informações sobre como usar os conceitos básicos do Orion Context Broker com o protocolo NGSI-V2. Começaremos com os dados do localizador de lojas de uma rede de supermercados e criaremos um aplicativo __“Powered by FIWARE”__ muito simples, passando o endereço e a localização de cada loja como dados de contexto para o agente de contexto FIWARE.

## Tutorial 2 - Entendendo entidades e relacionamentos em FIWARE

Este tutorial ensina os usuários do FIWARE sobre comandos em lote e relacionamentos entre entidades. O tutorial se baseia nos dados criados no tutorial anterior e cria e associa uma série de entidades de dados relacionadas para criar um sistema simples de gerenciamento de lojas. 

## Tutorial 3 - Operações CRUD no Orion Context Broker

Este tutorial ensina os usuários do FIWARE sobre as [[Operações CRUD]]. O tutorial baseia-se nos dados criados no tutorial anterior, permitindo que os usuários manipulem os dados mantidos dentro do contexto. Este tutorial foi criado com base no fornecido pela FIWARE em [CRUD Operations - Step-by-Step for NGSI-v2](https://fiware-tutorials.readthedocs.io/en/latest/crud-operations.html)

## Tutorial 4 - Provedores de contexto no Orion Context Broker

Este tutorial ensina os usuários do FIWARE sobre dados de contexto e provedores de contexto. O tutorial baseia-se na entidade **Store** criada nos últimos tutoriais do FIWARE e permite ao usuário recuperar dados sobre uma loja que não são mantidos diretamente no **Orion Context Broker**.

## Tuoorial 5 - Assinaturas no Orion Context Broker

Este tutorial ensina os usuários do FIWARE sobre como criar e gerenciar assinaturas de dados de contexto. O tutorial baseia-se na entidade **Store** criada nos últimos tutoriais do FIWARE e permite ao usuário enviar notificações para sistemas externos caso uma regra seja atingida. 

## Tutorial 6 - Agente IoT JSON no FIWARE

Este tutorial ensina os usuários de FIWARE sobre como conectar dispositivos IoT baseados em JSON usando o [Agente IoT para JSON](https://fiware-iotagent-json.readthedocs.io/en/latest/usermanual/index.html#user- programmers-manual) para que as medições possam ser lidas e os comandos possam ser enviados usando solicitações [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2) enviadas ao [Orion Context Broker](https ://fiware-orion.readthedocs.io/en/latest/).

## Tutorial 7 - Agente IoT sobre MQTT em FIWARE

Este tutorial apresenta o uso do protocolo MQTT em dispositivos IoT que se conectam ao FIWARE. O [Agente IoT UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual) é usado para se comunicar com um conjunto de dispositivos IoT fictícios usando MQTT por meio de um agente de mensagens [Mosquitto](https://mosquitto.org/).

## Tutorial 8 - Persistindo dados com o Cygnus e visualizando com o Grafana

Este tutorial é uma introdução ao FIWARE [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/) - um ativador genérico que é usado para persistir dados de contexto em bancos de dados de terceiros usando [Apache Flume]( https://flume.apache.org/) criando uma visão histórica do contexto. Também utiliza o componente **Grafana** (não fornecido pela FIWARE) para visualizar dados no banco de dados externo. O tutorial ativa o dispositivo fictício de IoT criado nos tutoriais anteriores e persiste as medições do sensor em um banco de dados para análise posterior.


## Tutorial 9 - Caso de uso - FIWARE e Raspberry Pi para medir temperatura e umidade relativa

Este tutorial fornece ao usuário um cenário de caso de uso e demonstra como conectar a plataforma FIWARE e um Raspberry Pi enviando dados para a plataforma.
