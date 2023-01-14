# 03. Arquiteturas AWS (Tema 14)

Objetivo: migrar dados do Redshift para o DynamoDB, e criar uma API para acessar esses dados.

## PASSO A PASSO

### 1. PREPARAÇÃO

É necessário ter o Python 3.7 ou superior instalado. Instale o conteúdo do arquivo `/config/requirements.txt` utilizando `pip install -r requirements.txt`. 

Os passos descritos assumem que os dados necessários já estão no Redshift e no Glue Data Catalog. Para acessar os dados com o Redshift Spectrum siga o passo a passo do [Tema 13](https://github.com/ilegra/data-engineering-team/blob/fd83ad4a8259c7962ba83c07b5fa6eec7dd198be/Cloud%20Data%20Engineering%20Training/2-cloud-data-engineering/lucas-scalon/tema13/REDME.md).

Edite o arquivo `/config/.env` substituindo o campo `<DATABASE>` pelo banco de dados do Redshift (o pradrão é "dev"), `<CLUSTER>` pelo nome do cluster no Redshift e o `<DBUSER>` para o nome do usuário que acessará o banco de dados (o padrão é "awsuser).


### 2. REDSHIFT

Crie as views necessárias dentro do Redshift, executando o conteúdo do arquivo `/sql/create_views.sql`.

### 3. DYNAMODB

Acesse o DynamoDB e crie duas tabelas: `clients_info`e `clients_info_by_year`. Ambas devem ter como **Partition key** o atributo `clientid` do tipo **Number**.

### 4. INSERINDO DADOS NO DYNAMODB

Primeiro, configure corretamente as credenciais de acesso da AWS localmente, pois a biblioteca que se conecta ao banco de dados as utilizará.

Para inserir os dados na tabela `clients_info` e `clients_info_by_year` do DynamoDB, é necessário executar as funções `clients_info()` e `clients_info_by_month()`, respectivamente, da classe `Insert` do módulo `dynamo.query`. É **altamente recomendável** que, para testar o código, seja passado um número baixo como o parâmetro `entries`. Isso para evitar que o DynamoDB tenha que escalar seus limites de escrita muitas vezes em seguida. Exemplo de código:

    from  dynamo.query  import  Insert
    
    def  main():
    	Insert().clients_info(entries = 10)
    	Insert().clients_info_by_month(entries = 10)
    
    if  __name__ == '__main__':
    	main()

Com um número limitado, no entanto, é preciso ter certeza quais foram os `clientid` inseridos, já que a leitura correta, utilizando a API, dependerá disso. Para isso, é possível pegar os dados logados pela execuação do código.

### 5. CRIANDO UMA ROTINA DE INSERÇÕES

Para criar uma rotina de inserções, que faça a leitura dos dados do Redshift e escrita deles no DynamoDB, é possível passar o conteúdo dos diretórios `/scripts/` e `/config/` para uma EC2. É importante notar que tanto o arquivo `.env` quanto as credenciais AWS na EC2 têm que estar configurados corretamente.

Depois disso, é apenas necessário inserir o script bash `/scripts/insert.sh` em uma rotina do crontab. Para fazer essa inserção diária, por exemplo, a sintaxe é `0 0 * * *`.

### 6. CONTABYXAPI

`ContabyxAPI` é uma classe utilizada para obter os dados das tabelas criadas no DynamoDB.

Para utilizá-la, primeiro deve-se criar um cliente, passando como parâmetro as chaves `aws_access_key_id` e `aws_secret_access_key`. É altamente recomendável, por questões de segurança, que essas chaves estejam em um arquivo `.env` e sejam chamadas como parâmetro. Exemplo de código:

    from  contabyx  import  contabyxAPI  as  contabyx
    
    def  main():
    	client = contabyx(aws_access_key_id = '<ACCESS_KEY_ID>', aws_secret_access_key = '<SECRET_ACCESS_KEY>')
    
    if  __name__ == '__main__':
    	main()

Depois disso, é possível obter os dados chamando as funções com `client.<NOME_DA_FUNÇÃO>(id = <ID_DO_CLIENT>, [argumentos])`. As funções são:

 - **balance()**: retorna o balanço da conta do respectivo cliente em formato float.
 - **income()**: sem parâmetros, retorna o total de receitas do cliente. Com o parâmetro `year` retorna o total de receitas naquele ano, e com os parâmetros `year`e `month`, retorna o total de receitas naquele ano e mês.
 -  **expense()**: sem parâmetros, retorna o total de despesas do cliente. Com o parâmetro `year` retorna o total de despesas naquele ano, e com os parâmetros `year`e `month`, retorn o total de despesas naquele ano e mês.
 - **client()**: além do parêmetros `id`, é necessário passar o parâmetro `return_type`, que pode ser:
	 - **total**: retorna um dicionário com o balanço, as receitas e as despesas totais do cliente.
	 - **by_year**: retorna um dicionário com as informações do cliente separadas por ano.
	 - **by_month**: retorna um dicionário com as informações do cliente separadas por ano e mês. 

> Written with [StackEdit](https://stackedit.io/).