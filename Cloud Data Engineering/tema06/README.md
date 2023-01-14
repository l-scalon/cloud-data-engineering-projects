# 02. Arquiteturas On Premises (Tema 06)

Objetivo: apresentar um projeto de banco de dados em MySQL com o contexto descrito no exercício.

## PREPARAÇÃO

### DOCKER

Instale o Docker Engine seguindo as [instruções da documentação](https://docs.docker.com/engine/install/). 

Instale a imagem do MySQL e crie um container com o seguinte comando:

    docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=<PASSWORD> -d mysql:latest

É importante garantir que nenhum outro processo esteja rodando na mesma porta.

Então execute:

    docker exec -it mysql mysql -uroot -p
Digite a senha definida no passo anterior.
No cliente do MySQL, insira:

    update mysql.user set host = '%' where user='root';
Saia do cliente MySQL e execute:

    docker restart mysql
Depois disso é possível executar o script python parar criar e inserir no banco de dados, assim como se conectar através do MySQL Workbench.

### PYTHON
É preciso ter o Python 3.4 ou superior instalado para rodar os scripts de inserção.
Crie um `venv`, ative-o e vá até o diretório `/tema06/config/`. Então execute o comando:

    pip install -r requirements.txt
No script `/tema06/scripts/database/server.py`, substitua o campo `<PASSWORD>`  pela senha inserida na criação do container MySQL.

##  BANCO DE DADOS
### SCHEMA
Contém o script de criação do banco de dados. Ao executá-lo, será criado um esquema de nome `contabyx`, com 5 tabelas:

    Clients
    +----------+-------------------------+------+-----+---------+----------------+
    | Field    | Type                    | Null | Key | Default | Extra          |
    +----------+-------------------------+------+-----+---------+----------------+
    | clientID | int                     | NO   | PRI | NULL    | auto_increment |
    | type     | enum('natural','legal') | NO   |     | NULL    |                |
    | name     | varchar(255)            | NO   |     | NULL    |                |
    +----------+-------------------------+------+-----+---------+----------------+
    Documents
    +----------+-----------------+------+-----+---------+-------+
    | Field    | Type            | Null | Key | Default | Extra |
    +----------+-----------------+------+-----+---------+-------+
    | clientID | int             | NO   | PRI | NULL    |       |
    | type     | varchar(45)     | NO   | PRI | NULL    |       |
    | number   | bigint unsigned | NO   |     | NULL    |       |
    +----------+-----------------+------+-----+---------+-------+
    Transactions
    +---------------+--------------------------+------+-----+-------------------+-------------------+
    | Field         | Type                     | Null | Key | Default           | Extra             |
    +---------------+--------------------------+------+-----+-------------------+-------------------+
    | transactionID | int                      | NO   | PRI | NULL              | auto_increment    |
    | clientID      | int                      | NO   | MUL | NULL              |                   |
    | nature        | enum('income','expense') | NO   |     | NULL              |                   |
    | time          | datetime                 | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
    | amount        | float                    | NO   |     | NULL              |                   |
    +---------------+--------------------------+------+-----+-------------------+-------------------+
    Transfers
    +-----------------------+------+------+-----+---------+----------------+
    | Field                 | Type | Null | Key | Default | Extra          |
    +-----------------------+------+------+-----+---------+----------------+
    | transferID            | int  | NO   | PRI | NULL    | auto_increment |
    | expense_transactionID | int  | YES  | MUL | NULL    |                |
    | income_transactionID  | int  | YES  | MUL | NULL    |                |
    +-----------------------+------+------+-----+---------+----------------+
    Tax
    +---------------+-------+------+-----+---------+-------+
    | Field         | Type  | Null | Key | Default | Extra |
    +---------------+-------+------+-----+---------+-------+
    | transactionID | int   | NO   | PRI | NULL    |       |
    | rate          | float | NO   |     | NULL    |       |
    | fee           | float | NO   |     | NULL    |       |
    +---------------+-------+------+-----+---------+-------+
### PROCEDURES
Dos procedures criados, 6 são para novas inserções, e podem ser chamados diretamente ou por outros procedures, dependendo de cada caso.

Para criar inserir um novo cliente pessoa física ou pessoa jurídica na tabela `Clients`, são chamados os scripts `new_client_natural`ou `new_client_legal`, respectivamente. Ambos fazem a chamada do script `new_document`, ou seja, é obrigatório haver um documento associado ao cliente na sua inserção. Também é possível inserir um documento de um cliente que já tenha sido inserido através do script `new_document`. Lembrando que a chave primária da tabela `Documents` é a associação entre `clientID` e `type`, que descreve o tipo de documento. Ou seja: um cliente pode ter vários documentos, mas apenas um de cada tipo.

Para inserir novas transações na tabela `Transactions`, utiliza-se os script `new_transaction_expense` ou `new_transaction_income`, para uma despesa ou receita, respectivamente. Ambos fazem, também, uma inserção na tabela `Tax`, guardando a taxa aplicada à transação e o montante pago em imposto.

Para um nova transferência, deve-se utilizar o script `new_transfer`. Ele criará uma entrada de despesa e uma de receita na tabela `Transactions`, e guardará a associação entre as duas movimentações com um ID único.

O script `get_history` deve ser utilizado para chamar a view `Transaction_History` que, com o `clientID` passado como parâmetro, retornará o histórico de transações do respectivo cliente.

### FUNCTIONS

As funções `tax_fee` e `tax_rate` estão associadas ao cálculo de imposto de cada transação e são chamados pelos procedures de inserção delas. Já a função `get_client` é chamada para auxiliar na visualização do histórico de transações de cada cliente.

### VIEWS
A view `Transaction_History` só funciona corretamente quando chamada pelo procedure `get_history`, e serve para visualizar o histórico de transações de determinado cliente.

A view `Balance` mostra o balanço atual na conta de cada cliente.

A view `Transfer_History` mostra o histórico de transferências, com os clientes associados a elas e o movimento que foi feito de uma conta a outra. As views `Transfer_Aux_Expense` e `Transfer_Aux_Income` são auxiliares nesse processo e, apesar de poderem ser utilizadas separadamente, trazem menos informações importantes sozinhas que a view principal.

## EXECUÇÃO
Os scripts de criação do banco de dados podem ser executados tanto dentro do Workbench quanto através do `main.py`. Note que, através do script `main.py`, além da criação serão feitas inserções no banco.

Com o venv anteriormente criado ativado, vá até o diretório `/tema06/scripts/` e execute:

    python main.py
   As inserções criadas podem ser visualizadas executando os comandos SQL apropriados tanto no Workbench quando no cliente MySQL.
   
#### IMPORTANTE
 A cada nova execução do script `main.py`,  o banco de dados será criado novamente, havendo exclusão do antigo. 

A criação de inserts é cumulativa, ou seja, se o diretório `/tema06/SQL/INSERTS/` não for excluído entre as execuções, as inserções de cada vez que o script for rodado continuaram sendo executadas.

> Written with [StackEdit](https://stackedit.io/).