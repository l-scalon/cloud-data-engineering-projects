# 02. Arquiteturas On Premises (Tema 10)

Objetivo: Gravar os dados do SQL Server no MongoDB via Python, e consumi-los também através do Python.

## PREPARAÇÃO

### DOCKER

Instale o Docker Engine seguindo as [instruções da documentação](https://docs.docker.com/engine/install/). 

Instale a imagem do MongoDB e crie um container com o seguinte comando:

    docker run -d --name mongodb -p 27017:27017 mongo

É importante garantir que nenhum outro processo esteja rodando na mesma porta.

### PYTHON
É preciso ter o Python 3.4 ou superior instalado para rodar os scripts de inserção.

Crie um `venv`, ative-o e vá até o diretório `/tema10/config/`. Então execute o comando:

    pip install -r requirements.txt
Também é necessário instalar o driver [Microsoft ODBC Driver 17 for SQL Server](https://www.microsoft.com/pt-br/download/details.aspx?id=56567), caso ainda não esteja instalado.

No script `/tema10/config/.env`, substitua o campo `<PASSWORD>`  pela senha inserida na criação do container SQL Server.

##  MIGRAÇÃO

Para realizar a migração do banco de dados do SQL Server para o MongoDB, deve-se executar o método `main()` do módulo `migration.migrate`. O banco de dados receberá o mesmo nome do banco de dados em `<DATABASE>` do arquivo `/tema10/config/.env`.

### COLLECTIONS

Serão criadas duas collections: `Clients` e `Transactions`. A collection `Clients` traz as características das tabelas `Clients` e `Documents`. Já a collection `Transactions` traz as características das tabelas `Transactions`, `Tax`, `Transfers` e `TransactionTypes`. 

### DOCUMENTS

Os documentos criados têm características ou de clientes ou de transações. Para ambas, o documento é indexado através do campo `_id`, que recebe uma variável do tipo `ObjectID` da biblioteca `bson`. 

Enquanto os campos vindos de `Transactions` e `TransactionTypes` continuam obrigatórios, `tax` é inserido apenas se houve taxação, e o novo campo `transaction_counterpart` é inserido apenas se aquela transação é proveniente de um transação.


## MONGODB

Tantos os dados migrados quanto os novos dados são operados através do Python. Apesar do `Pymongo` ter métodos que realizam as operações no MongoDB, foram criados métodos novos para facilitar sua execução. 

### SELECT
Todas as operações de seleção retornam uma lista de dicionários com os resultados, assim como os resultados podem ser visualizados passando a variável `dataframed = True`. Também é possível passar as colunas que se quer receber daquela pesquisa. O módulo é dividido nas seguintes classe:

 - **Collection:** permite a visualizar as coleções inteiras. O método `filter()` é utilizado para filtrar as colunas e é utilizado também pelas outras classes do módulo.
 - **Document:** seleciona documentos por apenas uma chave ou várias chaves (passando uma lista de chaves e valores). Em ambos os casos a chave padrão é o `_id`, caso nenhuma outra chave seja passada.
 - **Views:** classe utilizada para facilitar a visualização de dados específicos. Tem métodos para receber o balanço de determinado cliente  e para receber o histórico de transações.

### INSERT

A classe `Document` faz a inserção de um ou mais documentos na coleção passada. Cada tipo de documento é criado por sua respectiva classe, construído pela classe do objeto passado. A ideia dessa separação é diminuir a chance que um documento de um tipo seja inserido na coleção errada.

Através do módulo `generate.inserts` é possível fazer inserções aleatórias em batches.

### DELETE

A classe `Client` permite que a entrada de um cliente seja excluída da base. A exclusão faz uma cascata para excluir também as transações às quais aquele cliente está ligado, assim como o `_id` das transações excluídas no campo `transfer_counterpart` caso aquela transação provenha de uma transferência.

### BACKUP, RECOVERY E STATS

Os backups são feitos salvando os dumps do MongoDB no host. Sua execução tanto pode ser feita manualmente através do script `backup\backup.py` tanto criando uma tarefa agendada para fazê-lo periodicamente.

A recuperação é feita executando o script `backup\recovery.py`, que copia o último dump do host para o container e realiza a recuperação, tanto do banco quanto das coleções e documentos.

Para obter a projeção de crescimento do banco de dados, basta utilizar a classe `Growth` do módulo `database.stats`, passando o banco de dados, o número de inserções diárias e o tamanho da memória reservada para o banco de dados (em GB).

> Written with [StackEdit](https://stackedit.io/).