
# 03. Arquiteturas AWS (Tema 12)

Objetivo: criar um DW utilizando Amazon Redshift.

## PASSO A PASSO

A documentação do tema descreve como importar os dados de uma fonte local (ex: um banco de dados) para o Redshift.

### 1. PREPARAÇÃO

É necessário ter o Python 3.7 ou superior instalado. Instale o conteúdo do arquivo `/config/requirements.txt` utilizando `pip install -r requirements.txt`. 

Os dados a serem importados serão gerados e obtidos a partir de um banco de dados MySQL, então é necessário ter a instalação de um servidor hospedado localmente na porta 3306. É possível obter instruções de como rodá-lo como um container Docker na documentação dos temas anteriores.

A senha para o banco de dados deve ser inserida no arquivo `/config/.env`, no campo `<PASSWORD>`.

Instale o [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)  e configure as permissões corretamente.


### 2. GERANDO OS DADOS
Crie o banco de dados no MySQL rodando o arquivo `/sql/mysql.sql`. 

Por padrão, quando as inserções em batch forem executadas, o início se dará em `2015-07-01 00:00:00.000`. Para modificar essa data, é preciso modificar o datetime em

    class  Batch:
    
	    def  __init__(self) -> None:
			self.fake_time = datetime(2015, 7, 1, 0, 0, 0, 0)
do módulo `database.generate.inserts` para a data em que se deseja iniciar.
Para iniciar deve-se chamar o método `insert()` da classe `Batch`, passando como parâmetro o número de dias que se deseja fazer inserções. Para 7 anos, por exemplo, deve-se utilizar 2555 dias:

    from  database.generate.inserts  import  Batch
    
    def  main():
	    Batch().insert(2555)
    
    if  __name__ == '__main__':
		main()

Isso criará 400 inserções por dia (100 entradas, 100 saídas e 100 transferências internas, que geram 1 entrada e 1 saída cada).

Depois de feitas as inserções, é possível extrair os dados utilizando o método `extract()` da classe `Data`:

	from  database.generate.files  import  Data
    
    def  main():
	    Data().extract()
    
    if  __name__ == '__main__':
		main()

### 3. S3
Crie um bucket S3 e insira seu nome no campo `<BUCKET>` do arquivo `/config/.env/`. Também cria uma pasta para o tema e coloque seu nome (ex: `tema12`) no campo `<KEY>` do mesmo arquivo. Esses passos são necessários para guardar os arquivos originais, os processados e os que derem erro ao fazer a importação dos dados para o Redshift. Na pasta do campo `<KEY>`, crie 3 pastas: `data`, `processed` e `error`.

Faça upload dos dados extraídos executando o método `data()` da classe `Upload`, que utiliza um caminho padrão tanto de origem como de destino, caso nenhum seja passado:

	from  aws.s3  import  Upload
    
    def  main():
	    Upload().data()
    
    if  __name__ == '__main__':
		main()

### 4. REDSHIFT
Crie um cluster na Redshift seguindo as configurações padrões. Apenas um node `dc2.large` é o suficiente para o tema.

Adicione um security group já existente ao cluster ou crie um novo. É importante que esse grupo tenha, tanto como regra de ingresso quanto de saída, a exposição da porta 5439 por TCP. Por segurança, é recomendado que essa conexão possa ser feita apenas o seu IP.

Faça o [download](https://docs.aws.amazon.com/redshift/latest/mgmt/configure-odbc-connection.html) e a instalação do driver ODBC para o Redshift. Crie um DSN chamado "Redshift" e insira os parâmetros solicitados. O endpoint correto pode ser copiado através do painel do cluster, inserido no DSN **sem** a parte final `:5439/dev`.

Conectando-se externamente ao Redshift ou utilizando seu próprio painel de query, crie um esquema chamado `contabyx` no banco de dados `dev`. Então execute o arquivo `/sql/redshift.sql`, que criará as tabelas na ferramenta.

### 5. IMPORTANDO OS DADOS

Os dados serão importados do S3 utilizando o comando `COPY`. Para a importação dados desse tema, deve-se utilizar o método `default()` da classe `Copy`, passando a conexão com o Redshift como parâmetro:

	from  database.connect  import  Redshift
	from  aws.redshift  import  Copy
    
    def  main():
	    redshift = Redshift().connect()
	    Copy().default(connection = redshift)
    
    if  __name__ == '__main__':
		main()

O método se comportará da seguinte maneira:

 1. Cria os diretórios de logs e o arquivo `redshift.log` caso ainda não exista.
 2. Para cada tabela, chama o método `from_s3_to_redshift()`, da mesma classe, que faz a importação dos dados que estão na S3 para o Redshift.
 3. Caso a importação do arquivo ocorra sem erros, ele será replicado para o diretório `processed` dentro do mesmo bucket.
 4. Caso haja erro na importação do arquivo, ele não será processado e será replicado para o diretório `error` do mesmo bucket.
 5. Por fim, o arquivo `redshift.log`, que guarda o log dos erros durante a execução, será subido também para a pasta `error`.

Com esses passos seguidos corretamente, os arquivos estarão importados dentro do Redshift.

Written with [StackEdit](https://stackedit.io/).