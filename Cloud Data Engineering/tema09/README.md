# 02. Arquiteturas On Premises (Tema 09)

Objetivo: Conectar o Power BI no SQL Server e criar um painel que traga informações do banco de dados.

## PREPARAÇÃO

O banco de dados utilizado é o mesmo do exercício anterior, que foi migrado do MySQL para o SQL Server. Se for necessário recriá-lo, siga as instruções dos exercícios anteriores.

### PYTHON
É preciso ter o Python 3.4 ou superior instalado para rodar os scripts.

Crie um `venv`, ative-o e vá até o diretório `/tema09/config/`. Então execute o comando:

    pip install -r requirements.txt
Também é necessário instalar o driver [Microsoft ODBC Driver 17 for SQL Server](https://www.microsoft.com/pt-br/download/details.aspx?id=56567), caso ainda não esteja instalado.

No arquivo`/tema09/config/.env`, substitua o campo `<PASSWORD>` para a senha inserida na criação do container SQL Server.

##  SQL SERVER
### NOVA TABELA: TRANSACTIONTYPES
A tabela TransactionTypes guarda a categoria em que a respectiva transação se encaixa. Agora, quando os procedures de inserção de transações são chamados, é necessário também passar o tipo de transação como parâmetro. Os procedures fazem a inserção na nova tabela.

## PYTHON

### INSERÇÕES E UPDATE
Foi criado um script para fazer as inserções na tabela TransactionTypes das transações já existentes. 

As inserções aleatórias agora passam como parâmetro a categoria da transação. Ambas utilizam o função `get_type` para obter a categoria, escolhida aleatoriamente a partir de uma lista, de acordo com a natureza da transação e o tipo de cliente.

Para fazer a análise dos dados agrupados por mês, foi necessário fazer um update das transações já existentes com novas datas. Isso porque o campo `time` da tabela Transaction tem como parâmetro default a data real da inserção. Agora a coluna pode ter datas aleatórias de 01-JAN-2029 a 30-JUN-2022. 

Também é possível passar uma data como parâmetro nos procedures de inserção da tabela Transaction.
> Written with [StackEdit](https://stackedit.io/).