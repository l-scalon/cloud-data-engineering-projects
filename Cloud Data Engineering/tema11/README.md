# 03. Arquiteturas AWS (Tema 11)

Objetivo: migrar a arquitetura atual do SQL Server local para a AWS.

## PREPAÇÃO

O documentação do tema descreve como migar o banco de dados do SQL Server para o MySQL, rodando em um container Docker dentro de uma instância EC2.

### AWS
Primeiro, crie uma instância EC2 t2.micro. Em seguida, configure os acessos da AWS na instância, através do comando `aws configure`. Atualize o que for necessário com o comando: `sudo yum update -y`.

Permita que o usuário `ec2-user` faça modificações no diretório `/home/ec2-user/` com: `sudo chown -R ec2-user /home/ec2-user/`.

Crie uma pasta chamada `tema11` em `/home/ec2-user/` e faça o download do conteúdo do diretório `/backup/` nela (seja por `s3 sync` ou `git pull`).

No arquivo `backup/.env` substitua o campo `<PASSWORD>` pela senha de acesso ao servidor MySQL.

No arquivo `/backup/backup.sh`, insira o caminho correto para o bucket S3 em que o arquivo de backup `.sql` será upado. Depois execute: `sudo chmod u+x backup.sh` e `sudo chmod u+x recover.sh`

*TODO:* usar o Jenkins para criar um job para automatizar esses processos.

#### DOCKER

Instale o Docker com:  `sudo amazon-linux-extras install docker`

Para que o Docker inicie-se com o sistema, execute:  `sudo systemctl enable docker`

Então ative e verifique se está ativado com os comandos:  `sudo systemctl start docker` e `sudo systemctl status docker`

Por fim, permita que o Docker execute comandos sem utilizar  `sudo`:  `sudo usermod -a -G docker ec2-user`

Agora inicie um container MySQL com:

`docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=<PASSWORD> -d mysql:latest`

Note que o campo `<PASSWORD>` aqui tem de ser o mesmo do campo `<PASSWORD>` no `.env` editado anteriormente.

É importante garantir que nenhum outro processo esteja rodando na mesma porta. Então execute: `docker exec -it mysql mysql -uroot -p`. Digite a senha definida no passo anterior. No cliente do MySQL, insira: `update mysql.user set host = '%' where user='root';`. Saia do cliente MySQL e execute: `docker restart mysql`.

Execute o seguinte comando para garantir que o container MySQL inicie sempre junto com o Docker: `docker update --restart always mysql`.

### LOCAL

Essa documentação assume que os passos dos temas anteriores foram seguidos, ou seja, que na arquitetura atual já existem um banco de dados em SQL Server rodando em um container Docker.

#### INSTALAÇÕES

Instale o [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)  e o [AWS PowerShell](https://www.powershellgallery.com/packages/AWSPowerShell/4.1.120).

É preciso ter o Python 3.4 ou superior instalado para rodar os scripts. Instale as dependências utilizando o comando `pip install -r requirements.txt`, na pasta `/config/`.

Para a migração, instale o [MySQL Workbench 8.0 CE](https://dev.mysql.com/downloads/workbench/).

#### ACESSOS

Substitua os campos do arquivo `/config/.env` por suas respectivas variáveis:

`<INSTANCE>`: id da instância EC2 criada na AWS.
`<KEYPAIR>`: nome do arquivo keypair `.pem` utilizado para a criação da instância EC2. Exemplo 'mykeypair.pem'.
`<PASSWORD>`: senha de acesso ao servidor MySQL (a mesma do arquivo `/backup/.env` e da criação do container na EC2).
`<SSPASSWORD>`: senha utilizada para acessar o SQL Server local.

Os outros campos podem ser deixados como estão, ou mudados conforme a necessidade.

Coloque um cópia do arquivo keypair `.pem` utilizado para a criação da instância EC2 no diretório `/config/`. Este arquivo deve ser o mesmo que foi inserido no campo `<KEYPAIR>` anteriormente.

Configure os acessos da conta AWS localmente utilizando o comando `aws configure`.

## MIGRAÇÃO

### CONEXÃO

Na tela inicial do Workbench, em MySQL Connections clique no **+**.  Preencha os campos da seguinte forma:

> **Connection Name:** MySQL EC2
> **Connection Method:** Standard TCP/IP over SSH
> **SSH Hostname:** `<Public IPv4 DNS>` 
> **SSH Username:** ec2-user
> **SSH Key File:** `<path/to/keypair.pem>`

Em que `<Public IPv4 DNS>` é o endereço público de acesso à instância EC2 e o `<path/to/keypair.pem>` é o caminho local para o keypair utilizado para sua criação. Os outros campos podem ser deixados como estão ou modificados conforme necessidade.

Clique em **Test Connection** e digite a senha quando for pedido. Se tudo ocorrer normalmente, cliqem em **Ok**.

### MIGRAÇÃO

Acesse a conexão criada. Na aba **Database**, cliquem em **Migration Wizard...**.

Na nova tela, clique em **Start Migration**. No fim de cada etapa, clique em **Next**. Em *Source Selection* , preencha os campos da seguinte forma:

> **Database System:** Microsoft SQL Server
> **Connection Method:** ODBC Data Source
> **DSN:** ODBC For SQL Server
> **Username:** sa

Em *Target Selection*, preencha os campos da seguinte forma:

> **Stored Connection:** MySQL EC2
> **Connection Method:** Standard TCP/IP over SSH

Digite a senha de cada servidor quando for perguntado. Em *Schemas Selection* selecione **contabyx**.

Em *Source Objects* selecione **Migrate Table objects**.

Em *Create Target Results*, selecione **contabyx.Transactions**, na *linha 6*, edite o campo `'amount' FLOAT(24,0) NOT NULL,` para `'amount' FLOAT(24,2) NOT NULL,` e dê **Apply**. Já em em **contabyx.Tax**, nas *linhas 3 e 4*, também substitua os 0 por 2 em cada `FLOAT(24,0)` e dê **Apply**.

Em **contabyx.Clients**, **contabyx.Transactions** e em **contabyx.Transfers**, adicione os termos `UNIQUE AUTO_INCREMENT` logo após `NOT NULL` de cada respectivo id. Dê **Apply** em cada um depois clique em **Recreate Objects**.

Continue clicando em **Next** e aguarde a migração dos dados. No fim, clique em **Finish**. Se tudo ocorrer corretamente, os dados estarão migrados no fim dessa etapa.

### COMPARANDO DADOS

Para comparar os dados da fonte e do destino, execute o método `is_equal()`. Exemplo de código: 

    from  database.connect  import  MySQL, SQLServer
    from  database.consistency  import  Compare
    
    def  main():
    	mysql = MySQL().connect(database = 'contabyx')
    	sqlserver = SQLServer().connect(database = 'contabyx')
    	Compare().is_equal(source = mysql.cursor(), target = sqlserver.cursor(), database = 'contabyx', tables = ['Clients', 'Documents', 'Transactions', 'Tax', 'Transfers', 'TransactionTypes'])
    
    if  __name__ == '__main__':
	    main()

Exemplo de resultado positivo:

    Clients: True
    Documents: True
    Transactions: True
    Tax: True
    Transfers: True
    TransactionTypes: True

### RECRIANDO OBJETOS

Para recriar os objetos (functions, procedures e views), execute a função `default()` da classe `Create`. Exemplo de código:

    from  database.connect  import  MySQL, SQLServer
    from  database.create  import  Create
    
    def  main():
    	mysql = MySQL().connect(database = 'contabyx')
    	Create().default(connection = mysql)
    
    if  __name__ == '__main__':
    	main()

O método `default()` segue uma rotina especificada, mas também é possível chamar os métodos da classe `Create` separadamente.

## BANCO DE DADOS

### INSERÇÕES

À partir daqui, já é possível fazer inserções normalmente no banco de dados migrado. Para testar as inserções, é possível chamar o método `inserts()`, que faz inserções aleatórias em bloco. Exemplo de código:

    from  database.generate.inserts  import  Batch
    
        def  main():
        	Batch().insert([5, 1], 10)
        	
    if  __name__ == '__main__':
    	main()
 Que fará a inserção de 5 clientes físicos, 1 jurídico e 10 transações.

### BACKUP E RECUPERAÇÃO

O backup pode ser feito tanto manualmente, executando `bash backup.sh`, quanto automaticamente, inserindo o  script `backup.sh` em um cronjob.

A recuperação pode ser feita tanto executando `bash recover.sh`.

Em ambos os casos, os scripts devem ser executados na instância EC2.

### REINDEXAÇÃO E ESTATÍSTICAS

Localmente, execute o método `default()` da classe `Maintenance` que executa uma rotina padrão de manutenção. Exemplo de código:

    from  database.connect  import  MySQL, SQLServer
    from  database.maintenance  import  Maintenance
    
    def  main():
    	mysql = MySQL().connect(database = 'contabyx')
    	Maintenance().default(connection = mysql)
    
    if  __name__ == '__main__':
    	main()

Para obter a projeção de crescimento, deve-se chamar o método `projection()`. Exemplo de código:

    from  database.connect  import  MySQL, SQLServer
    from  database.maintenance  import  Growth
    
    def  main():
    	mysql = MySQL().connect(database = 'contabyx')
    	Growth().projection(connection = mysql, per_day = 1000, disk_size = 10)
    
    if  __name__ == '__main__':
    	main()

Exemplo de resposta:

    ***GROWTH PROJECTION***
    
    Database size: 3.45 MB
    Average object size: 410.00 bytes
    Average growth per day: 400.39 KB
    Average growth per month: 11.73 MB
    Months until full: 873
    Years until full: 73

## SERVIDOR

É possível criar rotinas de manutenção utilizando uma instância EC2 como servidor para o banco de dados.

### AMAZON CLOUDWATCH

#### ALARMES

Para criar um alarme que desligue a instância EC2 quando ela estiver ociosa, primeiro vá até o painel do CloudWatch.

No menu lateral, clique em **All alarms** na guia **Alarms**. Clique no botão **Create alarm** e então em **Select metric** > **EC2** > **Per-Instance Metrics** e selecione a métrica *CPUUtilization* da instância para a qual o alarme está sendo criado. Então clique no botão **Select metric**. Preencha os campos da seguinte forma:

> **Statistic:** Average
> **Period:** 15 minutes
> **Threshold type:** Static
> **Whenever CPUUtilization is...:** Lower
> **than..:** 1

E clique em **Next**. Então clique em **Add EC2 action** e preencha:

> **Alarm state trigger:** In alarm **Stop this instance**

Clique em **Next** e então dê uma nome e uma descrição para o alarme. Clique em **Next** novamente, revise as informações e clique em **Create alarm**. Isso fará com que a instância seja desliga caso sua utilização seja muito baixa (< 1% do CPU) por 15 minutos.

#### EVENTOS

No menu lateral, vá em **Rules**, na aba **Events**, e então clique em **Create rule**. 

Para criar uma regra que desligue a instância todos os dias úteis às 21:00 GMT (18:00 BRT), preencha os campos da seguinte forma:

>  **Event Source:** Schedule  
>  **Cron expression**: 0 21 ? * 2-6 * 
> **Targets:** EC2 StopInstances API call  
> **Instance ID:** `<INSTANCE>`  
> **Create a new role for this specific resource**

Em que `<INSTANCE>` é o ID da instância que se deseja desligar.

Clique no botão **Configure details**, insira um nome e uma descrição, e então clique no botão **Create rule**.

Já para criar uma regra que ligue a instância, é preciso recorrer a uma função Lambda. Para criar uma função Lambda, veja o subtítulo abaixo. 

Para ligar a instância todos os dias úteis às 11:00 GMT (8:00 BRT), preencha os campos da seguinte forma:

>  **Event Source:** Schedule  
>  **Cron expression**: 0 11 ? * 2-6 * 
> **Targets:** Lambda function
> **Funtion:** `<FUNCTION>`

Em que `<FUNCTION> ` é o nome da função Lambda criada.

Clique no botão **Configure details**, insira um nome e uma descrição, e então clique no botão **Create rule**.

### AWS LAMBDA

Para criar uma função Lambda que desligue uma instância EC2, vá ao painel do Lambda e clique no botão **Create Function**.  Preencha os campos da seguinte forma:

>  **Create Function:** Author from scratch
>  **Function name**: EC2Start
> **Runtime:** Python 3.9
> **Architeture:** x86_64
>  **Use an existing role**

O IAM role selecionado tem que dar ao Lambda acesso a execução de atividades em instâncias EC2.

Clique em **Create function**. Em `lambda_funtion.py`, cole o conteúdo do arquivo `/config/lambda_function.py`, substituindo o campo `<INSTANCE>` pelo id da instância que se deseja ligar. Então clique no botão **Deploy** e então no botão **Test**. Se tudo ocorrer normalmente, a instância se ligada.


Written with [StackEdit](https://stackedit.io/).