# Introdução

Este tutorial é uma introdução ao FIWARE [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/) - um ativador genérico que é usado para persistir dados de contexto em bancos de dados de terceiros usando [Apache Flume]( https://flume.apache.org/) criando uma visão histórica do contexto. Também utiliza o componente **Grafana** (não fornecido pela FIWARE) para visualizar dados no banco de dados externo. O tutorial ativa o dispositivo fictício de IoT criado nos tutoriais anteriores e persiste as medições do sensor em um banco de dados para análise posterior.

# Requisitos 

>[!info] Antes de começar os tutoriais faça o seguinte:
> - Instale o [Docker, Docker compose](https://www.docker.com/)  e o [Postman](https://www.postman.com/downloads/). 
>- Baixe ou clone o [Repositório do GitHub](https://github.com/rafaelalvesitm/tutoriais-do-fiware).
>- Importe o arquivo `Tutoriais do Fiware.postman_collection.json` para o Postman.
>- Abra o Docker no computador.
>- Abra o Postman Agent no computador. 


# Persistência de dados usando Apache Flume

Os tutoriais anteriores introduziram um sensor IoT fictício (fornecendo medições do estado do mundo real) e dois componentes FIWARE - o **Orion Context Broker** e um **Agente IoT JSON**. Este tutorial apresentará um novo componente de persistência de dados - FIWARE **Cygnus**.

O sistema até agora foi construído para lidar com o contexto atual, ou seja, ele contém as entidades de dados que definem o estado dos objetos do mundo real em um determinado momento.

A partir desta definição você pode ver - o contexto está interessado apenas no estado **atual** do sistema - Não é responsabilidade dos componentes existentes relatar o estado histórico do sistema, o contexto é baseado na última medição cada sensor enviou ao agente de contexto.

Para fazer isso, precisaremos estender a arquitetura existente para persistir as mudanças de estado em um banco de dados sempre que o contexto for atualizado.

Dados de contexto histórico persistentes são úteis para análise de big data - eles podem ser usados para descobrir tendências ou dados podem ser amostrados e agregados para remover a influência de medições de dados distantes. No entanto, dentro de cada solução inteligente, o significado de cada tipo de entidade será diferente e entidades e atributos podem precisar ser amostrados em taxas diferentes.

Como os requisitos de negócios para usar dados de contexto diferem de aplicativo para aplicativo, não há um caso de uso padrão para persistência de dados históricos - cada situação é única - não é o caso de um tamanho único. Portanto, em vez de sobrecarregar o agente de contexto com o trabalho de persistência de dados de contexto histórico, essa função foi separada em um componente separado e altamente configurável - **Cygnus**.

Como seria de esperar, **Cygnus**, como parte de uma plataforma Open Source, é independente de tecnologia em relação ao banco de dados a ser usado para persistência de dados. O banco de dados que você escolher usar dependerá de suas próprias necessidades de negócios.

No entanto, há um custo para oferecer essa flexibilidade - cada parte do sistema deve ser configurada separadamente e as notificações devem ser configuradas para transmitir apenas os dados mínimos necessários, conforme necessário.

# Arquitetura

Este aplicativo se baseia nos componentes e no dispositivo IoT fictício criado em tutoriais anteriores. Ele fará uso de três componentes FIWARE - o **Orion Context Broker**, o **Agente IoT** para e introduzirá o [Cygnus Generic Enabler](https://fiware-cygnus.readthedocs.io/en/latest/) para dados de contexto persistentes para um base de dados. Bancos de dados adicionais estão agora envolvidos - tanto o **Orion Context Broker** quanto o **Agente IoT** contam com a tecnologia [MongoDB](https://www.mongodb.com/) para manter a persistência das informações que eles possuem, e nós persistiremos em nosso contexto histórico data outro banco de dados - neste caso o **[MySQL](https://www.mysql.com/)**. Também usará o componente **Grafana** para visualizar dados no banco de dados SQL.

Portanto, a arquitetura geral consistirá nos seguintes elementos:

- Três **Ativadores genéricos de FIWARE**:
    - O FIWARE **Orion Context Broker** que receberá solicitações usando NGSI-v2
    - O FIWARE **Agente IoT para JSON**, que receberá as medições de sentido norte dos dispositivos IoT fictícios no formato JSON e as converterá em solicitações NGSI-v2 para que o agente de contexto altere o estado das entidades de contexto
    - FIWARE [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/) que assinará as alterações de contexto e as manterá em um banco de dados (**MySQL**)
- Dois **Bancos de dados**:
    - O banco de dados **MongoDB**:
        - Usado pelo **Orion Context Broker** para armazenar informações de dados de contexto, como entidades de dados, assinaturas e registros
        - Usado pelo **Agente IoT** para armazenar informações do dispositivo, como URLs e chaves do dispositivo
    - O banco de dados **MySQL**:
        - Potencialmente usado como um coletor de dados para armazenar dados de contexto histórico.
- Um **dispositivo fictício**:
    - Um servidor da Web atuando como um dispositivo IoT usando o protocolo JSON executado em HTTP.
- **Grafana**
	- Usado para visualizar dados no banco de dados SQL.

Como todas as interações entre os serviços são iniciadas por solicitações HTTP, os serviços podem ser disponibilizados em contêineres e executados a partir de portas expostas.

Para persistir dados de contexto histórico em **[MySQL](https://www.mysql.com/)**, precisaremos de um contêiner adicional que hospede o servidor **MySQL**, mais uma vez a imagem padrão do Docker para esses dados pode ser usada . A instância do **MySQL** está escutando na porta padrão `3306` e a arquitetura geral pode ser vista abaixo:

![[FIWARE Tutorial - Persisting data Architecture.png]]

Mais uma vez temos um sistema com dois bancos de dados, pois o container **MongoDB** ainda é necessário para conter os dados relacionados ao **Orion Context Broker** e ao **Agente IoT**.

## MySQL - Configuração do servidor de banco de dados

```yml
mysql-db:
    restart: always
    image: mysql:5.7
    hostname: mysql-db
    container_name: db-mysql
    expose:
        - "3306"
    ports:
        - "3306:3306"
    networks:
        - default
    environment:
        - "MYSQL_ROOT_PASSWORD=123"
        - "MYSQL_ROOT_HOST=%"
```

O contêiner `mysql-db` está escutando em uma única porta:

- A porta `3306` é a porta padrão para um servidor **MySQL**. Ele foi exposto para que você também possa executar outras ferramentas de banco de dados para exibir dados, se desejar.

O contêiner `mysql-db` é controlado por variáveis de ambiente como mostrado:

| Chave | Valor. | Descrição |
| --- | --- | --- |
| MYSQL\_ROOT\_PASSWORD | `123`. | especifica uma senha definida para a conta `root` do MySQL. |
| MYSQL\_ROOT\_HOST | `%` | Por padrão, o MySQL cria a conta `root'@'localhost`. Esta conta só pode ser conectada de dentro do contêiner. Definir essa variável de ambiente permite conexões root de outros hosts |

> **Observação:** Usar o usuário `root` padrão e exibir a senha em variáveis de ambiente como esta é um risco de segurança. Embora essa seja uma prática aceitável em um tutorial, para um ambiente de produção, você pode evitar esse risco configurando outro usuário e aplicando [Docker Secrets](https://blog.docker.com/2017/02/docker-secrets-management /)

## Configuração Cygnus para trabalhar com MySQL

```yml
cygnus:
    image: fiware/cygnus-ngsi:latest
    hostname: cygnus
    container_name: fiware-cygnus
    networks:
        - default
    depends_on:
        - mysql-db
    expose:
        - "5080"
    ports:
        - "5050:5050"
        - "5080:5080"
    environment:
        - "CYGNUS_MYSQL_HOST=mysql-db"
        - "CYGNUS_MYSQL_PORT=3306"
        - "CYGNUS_MYSQL_USER=root"
        - "CYGNUS_MYSQL_PASS=123"
        - "CYGNUS_MYSQL_SERVICE_PORT=5050"
        - "CYGNUS_LOG_LEVEL=DEBUG"
        - "CYGNUS_API_PORT=5080"
        - "CYGNUS_SERVICE_PORT=5050"
```

> **Observação:** Passar o nome de usuário e a senha em variáveis de ambiente de texto simples como esta é um risco de segurança. Considerando que esta é uma prática aceitável em um tutorial, para um ambiente de produção, `CYGNUS_MYSQL_USER` e `CYGNUS_MYSQL_PASS` devem ser injetados usando [Docker Secrets](https://blog.docker.com/2017/02/docker-secrets-management/ )

O contêiner `cygnus` está escutando em duas portas:

- A Porta de Assinatura para Cygnus - `5050` é onde o serviço estará escutando notificações do corretor de contexto Orion.
- A porta de gerenciamento para Cygnus - `5080` é exposta puramente para acesso tutorial - para que cUrl ou Postman possam fazer comandos de provisionamento sem fazer parte da mesma rede.

O contêiner `cygnus` é controlado por variáveis de ambiente, conforme mostrado:

| Chave | Valor | Descrição |
| --- | --- | --- |
| CYGNUS\_MYSQL\_HOST | `mysql-db` | Nome de host do servidor MySQL usado para persistir dados de contexto históricos |
| CYGNUS\_MYSQL\_PORT | `3306` | Porta que o servidor MySQL usa para escutar comandos |
| CYGNUS\_MYSQL\_USER | `root` | Nome de usuário para o usuário do banco de dados MySQL |
| CYGNUS\_MYSQL\_PASS | `123` | Senha para o usuário do banco de dados MySQL |
| CYGNUS\_LOG\_LEVEL | `DEBUG` | O nível de log para Cygnus |
| CYGNUS\_SERVICE\_PORT | `5050` | Notification Port que Cygnus escuta ao assinar alterações de dados de contexto |
| CYGNUS\_API\_PORT | `5080` | Porta que Cygnus escuta por razões operacionais |

# Dados persistentes

## Verificando a integridade do serviço Cygnus

Quando o Cygnus estiver em execução, você pode verificar o status fazendo uma solicitação HTTP para a porta `CYGNUS_API_PORT` exposta. Se a resposta estiver em branco, isso geralmente ocorre porque o Cygnus não está em execução ou está escutando em outra porta.

>[!info] **Envie a solicitação de `saúde do Cygnus`**. 
>Esta solicitação verifica se o Cygnus está funcionando corretamente.

Se for, uma resposta semelhante à abaixo é recebida.

```json
{
    "success": "true",
    "version": "1.18.0_SNAPSHOT.etc"
}
```

> **Solução de problemas:** e se a resposta estiver em branco ?
>
> - Para verificar se um contêiner docker está em execução, tente `docker ps`
>
> Você deverá ver vários contêineres em execução. Se o `cygnus` não estiver rodando, você pode reiniciar os containers conforme necessário.

## Gerando dados de contexto

Para gerar dados de contexto, um dispositivo fictício é criado usando uma aplicação web  com base no framework Flask. Este dispositivo fictício é melhor descrito em tutoriais anteriores. Para criar dados de contexto, envie as seguintes solicitações:

>[!info] **Envie a solicitação `Criar um grupo de serviços`**.
> Essa solicitação cria um serviço para entidades do tipo Device. E

Ele especifica a chave de API que deve ser usada pelos dispositivos para enviar medições por meio do **IoT Agent JSON**.

>[!info] **Envie a solicitação `Provision a device`**. Essa solicitação fornece a entidade do dispositivo capaz de receber comandos e enviar medições. 

O dispositivo pode enviar medições de temperatura e umidade relativa e receber comandos como interruptor e intervalo.

>[!info] **Envie a solicitação `Comece a enviar dados`**. Essa solicitação envia uma solicitação ao **Orion Context Broker** para indicar que o dispositivo deve começar a enviar medições. 

Essa solicitação é encaminhada do **Orion Context Broker** para o **Agente IoT JSON** e, em seguida, para o servidor web do **Dummy device**.

## Assinando Mudanças de Contexto

Assim que um sistema de contexto dinâmico estiver funcionando, precisamos informar ao **Cygnus** sobre as mudanças no contexto. Isso é feito fazendo uma solicitação POST para o endpoint `/v2/subscription` do **Orion Context Broker**.

- Os cabeçalhos `fiware-service` e `fiware-servicepath` são usados para filtrar a assinatura para ouvir apenas as medições dos sensores IoT anexados, uma vez que foram provisionados usando essas configurações.
- O `idPattern` no corpo da solicitação garante que o Cygnus seja informado de todas as alterações de dados de contexto.
- O `url` da notificação deve corresponder ao `CYGNUS_MYSQL_SERVICE_PORT` configurado.
- O valor `throttling` define a taxa em que as alterações são amostradas.

>[!info] **Envie o `Inscrever-se nas Mudanças de Contexto`**. 
>Essa solicitação cria uma assinatura no **Orion Context Broker** para enviar uma notificação sempre que uma entidade nas informações de contexto for alterada. 

Como você pode ver, o banco de dados usado para manter os dados de contexto não afeta os detalhes da assinatura. É o mesmo para cada banco de dados. A resposta será **201 - Criado**.

## MySQL - Lendo dados de um banco de dados

Para ler dados [MySQL](https://www.mysql.com/) da linha de comando, precisaremos acessar o cliente `mysql`, para fazer isso, execute uma instância interativa da imagem `mysql` fornecendo a string de conexão conforme mostrado para obter um prompt de linha de comando:

```bash
docker exec -it  db-mysql mysql -h mysql-db -P 3306  -u root -p123
```

### Mostrar bancos de dados disponíveis no servidor MySQL

Para mostrar a lista de bancos de dados disponíveis, execute a instrução conforme mostrado:

```SQL
SHOW DATABASES;
```

O resultado é o seguinte:

```SQL
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| openiot            |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

Para mostrar a lista de esquemas disponíveis, execute a instrução conforme mostrado:

```SQL
SHOW SCHEMAS;
```

O resultado é o seguinte:

```SQL
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| openiot            |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

Como resultado da assinatura do **Cygnus** para o **Orion Context Broker**, um novo esquema foi criado chamado `openiot`. O nome do esquema corresponde ao cabeçalho `fiware-service` - portanto, `openiot` contém o contexto histórico dos dispositivos IoT.

### Leia o contexto histórico do servidor MySQL

Uma vez executado um container docker dentro da rede, é possível obter informações sobre o banco de dados em execução.

```SQL
SHOW tables FROM openiot;
```

O resultado é o seguinte:

```SQL
+-------------------------------+
| Tables_in_openiot             |
+-------------------------------+
| urn_ngsi-ld_Device_001_Device |
+-------------------------------+
1 row in set (0.00 sec)
```

O `table_schema` corresponde ao cabeçalho `fiware-service` fornecido com os dados de contexto:

Para ler os dados é necessário primeiro selecionar uma tabela. Use o seguinte comando

```sql
use openiot;
```

O resultado é o seguinte:

```
Lendo as informações da tabela para completar os nomes das tabelas e colunas
Você pode desativar esse recurso para obter uma inicialização mais rápida com -A

Banco de dados alterado
```

Dentro de uma tabela, execute uma instrução `select` conforme mostrado:

```sql
SELECT recvtime, attrvalue from `urn_ngsi-ld_Device_001_Device` LIMIT 10;
```

O resultado é o seguinte:

```sql
+---------------+-------------------------+-------------------+------------------------+------------+------------------+---------------+--------------------------+-------------------------------------------------------------------------------+
| recvTimeTs    | recvTime                | fiwareServicePath | entityId               | entityType | attrName         | attrType      | attrValue                | attrMd                                                                        |
+---------------+-------------------------+-------------------+------------------------+------------+------------------+---------------+--------------------------+-------------------------------------------------------------------------------+
| 1665768733799 | 2022-10-14 17:32:13.799 | /                 | urn:ngsi-ld:Device:001 | Device     | relativeHumidity | Number        | 16                       | [{"name":"TimeInstant","type":"DateTime","value":"2022-10-14T17:32:13.645Z"}] |
| 1665768733799 | 2022-10-14 17:32:13.799 | /                 | urn:ngsi-ld:Device:001 | Device     | temperature      | Number        | 12                       | [{"name":"TimeInstant","type":"DateTime","value":"2022-10-14T17:32:13.645Z"}] |
| 1665768733799 | 2022-10-14 17:32:13.799 | /                 | urn:ngsi-ld:Device:001 | Device     | TimeInstant      | DateTime      | 2022-10-14T17:32:13.645Z | []                                                                            |
| 1665768733799 | 2022-10-14 17:32:13.799 | /                 | urn:ngsi-ld:Device:001 | Device     | switch_status    | commandStatus | OK                       | [{"name":"TimeInstant","type":"DateTime","value":"2022-10-14T17:32:03.599Z"}] |
| 1665768733799 | 2022-10-14 17:32:13.799 | /                 | urn:ngsi-ld:Device:001 | Device     | refStore         | Relationship  | urn:ngsi-ld:Store:001    | [{"name":"TimeInstant","type":"DateTime","value":"2022-10-14T17:32:13.645Z"}] |
| 1665768733799 | 2022-10-14 17:32:13.799 | /                 | urn:ngsi-ld:Device:001 | Device     | switch_info      | commandResult | Started sending data     | [{"name":"TimeInstant","type":"DateTime","value":"2022-10-14T17:32:03.599Z"}] |
| 1665768738793 | 2022-10-14 17:32:18.793 | /                 | urn:ngsi-ld:Device:001 | Device     | relativeHumidity | Number        | 31                       | [{"name":"TimeInstant","type":"DateTime","value":"2022-10-14T17:32:18.724Z"}] |
| 1665768738793 | 2022-10-14 17:32:18.793 | /                 | urn:ngsi-ld:Device:001 | Device     | temperature      | Number        | 11                       | [{"name":"TimeInstant","type":"DateTime","value":"2022-10-14T17:32:18.724Z"}] |
| 1665768738793 | 2022-10-14 17:32:18.793 | /                 | urn:ngsi-ld:Device:001 | Device     | TimeInstant      | DateTime      | 2022-10-14T17:32:18.724Z | []                                                                            |
| 1665768738793 | 2022-10-14 17:32:18.793 | /                 | urn:ngsi-ld:Device:001 | Device     | switch_status    | commandStatus | OK                       | [{"name":"TimeInstant","type":"DateTime","value":"2022-10-14T17:32:03.599Z"}] |
+---------------+-------------------------+-------------------+------------------------+------------+------------------+---------------+--------------------------+-------------------------------------------------------------------------------+
```

A sintaxe de consulta usual do **MySQL** pode ser usada para filtrar campos e valores apropriados. Por exemplo, para ler a taxa na qual o Dispositivo com o `id=urn_ngsi-ld_Device_001_Device` está acumulando, você faria uma consulta da seguinte forma:

```SQL
SELECT recvtime, attrvalue from `urn_ngsi-ld_Device_001_Device` LIMIT 10;
```

O resultado é o seguinte:

```sql
+-------------------------+--------------------------+
| recvtime                | attrvalue                |
+-------------------------+--------------------------+
| 2022-10-14 17:32:13.799 | 16                       |
| 2022-10-14 17:32:13.799 | 12                       |
| 2022-10-14 17:32:13.799 | 2022-10-14T17:32:13.645Z |
| 2022-10-14 17:32:13.799 | OK                       |
| 2022-10-14 17:32:13.799 | urn:ngsi-ld:Store:001    |
| 2022-10-14 17:32:13.799 | Started sending data     |
| 2022-10-14 17:32:18.793 | 31                       |
| 2022-10-14 17:32:18.793 | 11                       |
| 2022-10-14 17:32:18.793 | 2022-10-14T17:32:18.724Z |
| 2022-10-14 17:32:18.793 | OK                       |
+-------------------------+--------------------------+
```

Observe que a consulta a seguir retornou valores de vários atributos. Você pode filtrar por temperatura, por exemplo, usando a seguinte consulta:

```sql
SELECT recvtime, attrvalue from `urn_ngsi-ld_Device_001_Device` WHERE attrName="temperature" LIMIT 10;
```

O resultado é o seguinte:

```sql
+-------------------------+-----------+
| recvtime                | attrvalue |
+-------------------------+-----------+
| 2022-10-14 17:32:13.799 | 12        |
| 2022-10-14 17:32:18.793 | 11        |
| 2022-10-14 17:32:23.821 | 22        |
| 2022-10-14 17:32:28.881 | 38        |
| 2022-10-14 17:32:33.960 | 22        |
| 2022-10-14 17:32:38.979 | 22        |
| 2022-10-14 17:32:44.45  | 16        |
| 2022-10-14 17:32:49.110 | 30        |
| 2022-10-14 17:32:54.132 | 24        |
| 2022-10-14 17:32:59.190 | 20        |
+-------------------------+-----------+
10 rows in set (0.00 sec)
```

Para sair do cliente MySQL e sair do modo interativo, execute o seguinte:

```sql
\q
```

Em seguida, você retornará à linha de comando.

# Visualizando dados

Para visualizar os dados é usado o **Grafana**. O **Grafana** não é um componente FIWARE, mas é amplamente usado como construtor de painéis para interagir com bancos de dados externos, como **MySQL**.

A configuração para este componente é a seguinte

```yml
grafana:
    image: grafana/grafana
    depends_on:
        - mysql-db
    ports:
        - "3003:3000"
    environment:
        - GF_INSTALL_PLUGINS=https://github.com/orchestracities/grafana-map-plugin/archive/master.zip;grafana-map-plugin,grafana-clock-panel,grafana-worldmap-panel

```

Para acessar o **Grafana** abra um navegador e vá para a URL `http://localhost:3000/`. Isso abre uma página de login que você pode acessar com o seguinte: `username=admin` `password=admin`. Uma nova senha é solicitada e você pode fornecer uma como achar melhor. Após criar uma nova senha, a tela principal é apresentada.

Para visualizar os dados, o primeiro passo é conectar um banco de dados a ele. Para fazer isso, clique em `Add uour first data source`.

![[FIWARE tutorial - Add data source.png]]

Na barra de pesquisa, selecione **MySQL** como fonte de dados. Preencha as seguintes informações:
- `Host` = mysql-db:3306
- `banco de dados` = openiot
- `usuário` = raiz
- `senha` = 123

Clique em `save and test`. Se tudo correu bem um pop-up com a informação `Datasource updated` e uma bandeira verde. No final da página deve ser apresentada a mensagem `Database Connection OK`.

> Observe que o usuário e a senha estão configurados no arquivo de composição do docker para os bancos de dados MySQL. Esta é uma violação de segurança e deve ser usada apenas para fins de teste e não para implantação.

Volte para a tela principal e clique em `Create your first dashboard`

![[FIWARE Tutorial - Add dashboard.png]]

Clique em adicionar um novo painel e uma tela será carregada com um formulário para preencher e criar um painel. Altere a opção de consulta de `Builder` para `code` no botão de alternância a seguir

![[FIWARE Tutorial - Select code option.png]]

Crie uma consulta semelhante à seguinte:

```SQL
SELECT 
  UNIX_TIMESTAMP(recvTime) as "time",
  CAST(attrValue as decimal) as "value" 
FROM `urn_ngsi-ld_Device_001_Device` 
WHERE attrName = "temperature"
ORDER BY "time"
```

> É importante observar que as colunas no banco de dados **MySQL** salvas usando **Cygnus** são todas strings e, como tal, devem ser convertidas para o valor apropriado.

Isso deve selecionar a representação da série temporal clicando em um dos seguintes

![[FIWARE Tutorial - Select timeseries.png]]

Eles clicam no botão azul `run query` e um gráfico semelhante ao acima deve ser apresentado.
 
# Conclusão

Este tutorial apresenta aos usuários uma maneira de manter as informações de contexto do **Orion Context Broker** em bancos de dados externos. Este método utiliza o componente FIWARE **Cygnus** e o mecanismo de assinatura fornecido pelo **Orion Context Broker**. Ao usar esse componente e mecanismo, os usuários podem criar informações de contexto histórico e ler o banco de dados SQL conforme necessário.

:: **Referência** :: [Persisting Context (Apache Flume)](https://fiware-tutorials.readthedocs.io/en/latest/historic-context-flume.html)