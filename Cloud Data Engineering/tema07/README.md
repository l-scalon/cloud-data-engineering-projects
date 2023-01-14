# 02. Arquiteturas On Premises (Tema 07)

Objetivo: tarefas para o banco de dados criado anteriormente.

## PREPARAÇÃO

### DOCKER

Siga as instruções do [Tema 06](https://github.com/ilegra/data-engineering-team/tree/main/Cloud%20Data%20Engineering%20Training/2-cloud-data-engineering/lucas-scalon/tema06#docker).

### PYTHON
É preciso ter o Python 3.4 ou superior instalado para rodar os scripts.

Crie um `venv`, ative-o e vá até o diretório `/tema07/config/`. Então execute o comando:

    pip install -r requirements.txt
No arquivo`/tema07/config/.env`, substitua o campo `<PASSWORD>`  pela senha inserida na criação do container MySQL.

##  BANCO DE DADOS
### PROCEDURES
Em relação ao banco de dados criado anteriormente, foi criado um novo procedure.

O procedure `delete_null_from_transfers.sql` exclui as entradas da tabela `Transfers` em que ambos `expense_transactionID` e `income_transactionID` são `Null`.

## BACKUP

O backup do banco de dados é feito executando o script `backup.py`. Por questão de segurança, é o script do Python que diz ao script batch qual senha utilizar, e que deverá estar inserida no arquivo .env.

O script batch `backup.bat` então é chamado. Ele cria um arquivo de backup `.sql`, no seguinte formato:

> contabyxYYYYMMDDHsMsSs.sql

O script então faz a contagem da quantidade de arquivos de backup e, caso hajam mais de 3 na pasta, faz exclusão do mais antigo.

### SCHEDULED TASK
Para criar uma tarefa agendada do Windows que faz backup diariamente do banco de dados, apenas é necessário executar o script `create_schedule.bat`.

### RECOVER
Existam duas maneiras de fazer a recuperação do banco de dados: `simple` e `full`.

#### SIMPLE
Esta estratégia deve ser utilizada quando o banco de dados  e as tabelas continuam existindo, mas quer-se recuperar entradas perdidas. Para isso, na pasta `/tema07/backup/recover/` execute `python recover.py simple`.

O script, então, fara a recuperação das entradas utilizando o arquivo de backup mais recente. Caso seja necessária fazer a recuperação à partir de um backup mais antigo, deve-se deixá-lo como o único da pasta - e depois retornar os outros. 

Essa estratégia utiliza o comando `INSERT IGNORE`: ele tenta fazer a inserção de todas as entradas do backup mas, caso aquela entrada já exista, será ignorada, partindo para a próxima.

#### FULL
Esta estratégia deve ser utilizado quando deseja-se recriar o banco de dados, assim como inserir as entradas presentes no backup. Para isso, na pasta `/tema07/backup/recover/` execute `python recover.py full`.

O script, então, recriará o banco de dados, com procedures, functions e views, assim como fará as inserções das entradas presentes no último backup. Caso seja necessária fazer a recuperação à partir de um backup mais antigo, deve-se deixá-lo como o único da pasta - e depois retornar os outros.

## REINDEX AND STATISTICS

A atualização de indexação e estatísticas são feitas utilizando os comandos `--auto-repair` e `--optimize` do `mysqlcheck`. 

Para realizá-los, execute o script `update.py`, que chamará o script batch `update.bat`. 

### SCHEDULED TASK
Para criar uma tarefa agendada do Windows que faz atualização semanal da indexação e estatísticas do banco de dados, apenas é necessário executar o script `update_schedule.bat`.

> Written with [StackEdit](https://stackedit.io/).