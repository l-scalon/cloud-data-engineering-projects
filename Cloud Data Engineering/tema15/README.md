# 03. Arquiteturas AWS - Tema 15

**Objetivo:** criar uma arquitetura de dados full AWS, para uma rede de cinemas, utilizando os serviços Redshift, Athena, Glue, S3 e QuickSight.

## PREPARAÇÃO

É necessário ter o Python 3.6.x instalado, assim como um servidor MySQL rodando - localmente ou em um servidor remoto. Instale os módulos necessários utilizando `pip install -r requirements.txt`. Substitua os campos do arquivo `tema15/config/.env` com as seguintes informações:

> BUCKET = nome do bucket em que os arquivos extraídos do banco de dados, em formato .csv, seram upados.
> KEY = diretório intermediário dentro do bucket, que será usado pelo crawler do Glue para buscar os arquivos .csv.
> KEY_NEW_ENTRIES = diretório intermediário dentro do bucket em que serão inseridas as novas entradas, que então serão inseridas no Redshift.
> ATHENA = diretório intermediário dentro do bucket em que os resultados das queries no Athena serão armazenados.
> HOST = nome dos host do servidor MySQL (padrão: 'LOCALHOST')
> SQLUSER = nome do user do servidor MySQL (padrão: 'root')
> PASSWORD = senha do servidor MySQL.
> DATABASE = banco de dados do cluster do Redshift (padrão: 'dev')
> CLUSTER = nome do cluster do Redshift.
> DBUSER = nome do usuário para acessar o cluster do Redshift.

É necessário que as permissões da AWS estejam configuradas corretamente no local em que os scripts serão rodados. Substitua com os nomes apropriados os campos dos arquivos do diretório `sql`.

## DADOS

Os dados foram gerados utilizando um script em Python e, para manter a ideia de *full AWS*, inseridos em servidor MySQL rodando em uma EC2. Para fazer o teste da arquitetura completa, crie o esquema e as tabelas do banco de dados `cinemyx` executando o conteúdo do arquivo `tema15/sql/cinemyx_mysql_create.sql`. Depois, crie um diretório chamado `original` no caminho `tema15/cinemyx/data/` e faça download do conteúdo da seguinte URI nele: s3://jt-dataeng-lucasscalon/cinemyx-test-data/ (é preciso ter acesso à conta poc-ilegra). Depois, execute a função `insert()` da classe `data.insert.Data`, passando a conexão com o servido MySQL e o nome do esquema como parâmetros. Exemplo de código:

    from database.connect import MySQL
    from data.insert import Data

    def main():
	    mysql = MySQL().connect(database = 'cinemyx')
	    Data().insert(connection = mysql, schema = 'cinemyx')

	if __name__ == '__main__':
		main()

O código precisa ser rodado localmente onde o servidor MySQL estiver.

## ARQUITETURA AWS

Crie e configure corretamente, seguindo as variáveis de ambiente inseridas no arquivo `.env` anteriormente, o cluster no Redshift e o bucket (com os subdiretórios) no S3. Conecte-se ao banco de dados `dev` e execute o conteúdo do arquivo `sql/cinemyx_redshift_create.sql`. Isso criará tanto o `cinemyx` no Redshift, quanto o banco de dados `cinemyx` no Data Catalog.

Primeiro, execute o script `cinemyx/first.py`, que seguirá os seguintes passos:

 1. Conexão com o servidor MySQL.
 2. Extração das tabelas em formato .csv.
 3. Upload dos dados em formato .csv para o S3.
 4. Cópia dos dados do S3 para o Redshift.

Ainda conectado ao banco de dados `dev` no Redshift, execute o conteúdo do arquivo `sql/cinemyx_redshift_unload_and_delete.sql`. Isso fará o unload dos dados anteriores ao ano corrente para o Data Catalog, assim como irá detetá-los do Redshift.

Acesse o Glue e crie um crawler, apontando com origem da pesquisa o bucket com o subdiretório em que o unload do passo anterior foi feito, e o banco de dados `cinemyx` do **Data Catalog** como alvo

Ainda no Glue, crie um banco de dados no Data Catalog chamado `cinemyx-csv`. Então crie um crawler, apontando como origem da pesquisa o bucket com o subdiretório em que foi feito o upload dos arquivos .csv, e o banco de dados `cinemyx-csv` como alvo. 

À partir daí, cria-se uma camada de abstração em que os dados podem ser acessados através do Athena, tantos para os dados em parquet quanto para em csv.

Então, diariamente, execute o script `cinemyx/daily.py` - colocando-o em uma tarefa agendada, por exemplo. O script seguirá os seguintes passos:

 1. Conexão com o servidor MySQL.
 2. Extração das novas entradas desde a última execução. Para isso, o script, para cada tabela, executa uma query no Athena para verificar a última entrada no Data Catalog, e uma query no MySQL para verificar a última entrada no servidor. Se a última entrada no MySQL for diferente da que está no Data Catalog, os dados novos são extraídos para um .csv.
 3. Upload dos dados novos para o S3, tanto para atualizar o Data Catalog quanto para serem inseridos no Redshift. Para isso, os dados novos são colocados em diretórios separados, os únicos que serão checados para fazer a inserção no Redshift como tarefa diária. Se houverem dados novos da extração feita no dia anterior no S3, esses são excluídos. Assim, garante-se que não há repetição dos dados inseridos no Redshift.
 4. Inserção dos dados novos no Redshift.

Por último, ainda conectado ao banco de dados `dev` do Redshift, execute o conteúdo do arquivo `cinemyx_redshift_create_views.sql`. As views utilizam tanto o dados no Redshift quanto no Data Catalog para fazer queries utilizando o Redshift Spectrum, e que serão utilizados para compôr os painéis do QuickSight.

## DOCUMENTAÇÃO

Para além desse README, há uma documentação na pasta `docs`, que tem o seguinte conteúdo:

> billing.pdf: informações detalhadas dos custos da arquitetura para a empresa.
> database.pdf: modelo de relacionamento do banco de dados original.
> architecture.pdf: resumo visual da arquitetura criada.
> analysis/current_year.pdf: paineis de análises para o ano corrente feitos no QuickSight.
> analysis/overall.pdf: paineis de análises gerais feitos no QuickSight
