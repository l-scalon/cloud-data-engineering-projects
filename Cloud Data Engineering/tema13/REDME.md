# 03. Arquiteturas AWS (Tema 13)

Objetivo: migrar os dados que não sejam do ano corrente para o Athena em formato parquet, consumindo esses dados com os dados do ano corrente, que ainda estarão no Redshift, através do Redshift Spectrum.

## PASSO A PASSO

### 1. PREPARAÇÃO

É necessário ter o Python 3.7 ou superior instalado. Instale o conteúdo do arquivo `/config/requirements.txt` utilizando `pip install -r requirements.txt`. 

Os passos descritos assumem que os dados necessários já estão no Redshift. Para obter os dados no Redshift, caso ainda não estejam, siga o passo a passo do [Tema 12](https://github.com/ilegra/data-engineering-team/tree/main/Cloud%20Data%20Engineering%20Training/2-cloud-data-engineering/lucas-scalon/tema12#readme).

É necessário que já tenha sido criada uma DSN, com o nome "Redshift", no drive ODBC local.

É necessário que o role padrão (**Role type:** Default na opção **Associated IAM Roles**) tenha permissão para criar objetos no Glue.


### 2. S3

Crie um bucket na S3 ou utilize um já existente. Nos arquivos `unload.sql` e `athena.sql`, substitua o termo `<BUCKET>` pelo nome do bucket criado ou já existente.

Crie um diretório (ex. de nome: `tema13`) e, nos arquivos `unload.sql` e `athena.sql`, substitua as ocorrências do termo `<KEY>` pelo seu nome.

No diretório criado, crie um subdiretório chamado `contabyx-parquet` e, dentro dele, três outros diretórios: `transactions`, `transfers` e `tax`.

### 3. REDSHIFT

Faça o `UNLOAD` dos dados que não sejam do ano corrente executando o método `unload()` da classe `Redshift` do módulo `database.redshift`:

    from  database.connect  import  Redshift  as  rs
    from  database.redshift  import  Redshift
    
    def  main():
    	redshift = rs().connect()
    	Redshift().unload(connection = redshift)
    	
    if  __name__ == '__main__':
    	main()
A execução do método `unload()` também fará a exclusão dos dados que não pertencem ao ano corrente. 

Para criar uma rotina que faça o unload e a exclusão no primeiro dia de cada ano, crie uma query agendada (**Amazon Redshift** -> **Query editor** -> **Scheduled queries**) com a seguinte expressão cron:

    00 00 1 JAN ? *

Crie um esquema externo no catálogo de dados do Glue executando o método `create_external_schema()` e views que façam a união dos dados, internos e externos, executando o método `create_views()`, ambos da classe `Redshift` do módulo `database.redshift`:

    from  database.connect  import  Redshift  as  rs
    from  database.redshift  import  Redshift
    
    def  main():
    	redshift = rs().connect()
    	Redshift().create_external_schema(connection = redshift)
    	Redshift().create_views(connection = redshift)
    
    if  __name__ == '__main__':
    	main()
 A criação das views utiliza o termo `WITH  NO  SCHEMA  BINDING`, o que significa que, ainda que as tabelas que elas referenciam não existam, as views serão criadas normalmente, já que esse termo faz com que a query cheque a existência dos objetos apenas quando for chamada.

### 4. ATHENA

No console do Athena, execute **separadamente** as três queries presentes no arquivo `athena.sql`. Isso criará as tabelas as quais as views criadas no passo anterior estão fazendo referência.

A partir daí, já é possível fazer as queries normalmente no Redshift, referenciando as views criadas, que fará a seleção no local apropriado.

> Written with [StackEdit](https://stackedit.io/).