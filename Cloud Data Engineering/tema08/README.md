# 02. Arquiteturas On Premises (Tema 08)

Objetivo: migrar a estrutura MySQL para SQL Server.

## PREPARAÇÃO

### DOCKER

Instale o Docker Engine seguindo as  [instruções da documentação](https://docs.docker.com/engine/install/).

Instale a imagem do SQL Server e crie um container com o seguinte comando:

    docker run --name sqlserver -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=<PASSWORD>" -p 1433:1433 -d mcr.microsoft.com/mssql/server:2019-latest

Substituindo o campo `<PASSWORD>` pela senha desejada. É importante que ela esteja de acordo com as [diretrizes de criação de senha](https://docs.microsoft.com/en-us/sql/relational-databases/security/password-policy?view=sql-server-ver16) do SQL Server.

É necessário também que nenhum outro serviço esteja utilizando a porta `1433`.

### PYTHON
É preciso ter o Python 3.4 ou superior instalado para rodar os scripts.

Crie um `venv`, ative-o e vá até o diretório `/tema08/config/`. Então execute o comando:

    pip install -r requirements.txt
Também é necessário instalar o driver [Microsoft ODBC Driver 17 for SQL Server](https://www.microsoft.com/pt-br/download/details.aspx?id=56567).

No arquivo`/tema08/config/.env`, substitua os campos `<PASSWORD>`  , em `PASSWORD=` para a senha inserida na criação do container SQL Server, e em `OLD_PASSWORD=` pela senha inserida na criação do container MySQL.

##  MIGRAÇÃO
### PREPARAÇÃO E TESTES
A preparepação para a migração foi feita executando os seguintes passos:

 1. Baixar e instalar do Microsoft SQL Server Migration Assistant for MySQL.
 2. No software, criar um novo projeto.
 3. Conectar-se ao MySQL e ao SQL Server com o botão **Connect to...** respectivo.
 4. Criar um relatório com o botão **Create Report**.
 5. Recriar o banco do dados no SQL Server, sem migrar os dados, utilizando o botão **Convert Schema**.
 6. À partir do relatório criado no passo 4, editar os scrips DML para que as procedures, funtions e views estejam de acordo com a sintaxe do SQL Server.
 7. Testar o funcionamento das procedures, funtions e views, e criar um script para sua recriação.

### MIGRAÇÃO
A  migração foi feita executando os seguintes passos:

1. Selecionar os itens que serão migrados. No caso, apenas as tabelas, porque as procedures, functions e views serão recriadas à partir do script DML.
2. Interrompa novas inserções no banco de dados de origem.
3. Clicar no botão **Migrate Data** e aguardar a migração. Se tudo ocorrer corretamente, a migração das tabelas deve ser de 100%.

### VALIDAÇÃO
Para garantir a integridade dos dados, o script `/scripts/migration/compare.py` se conecta aos bancos de dados no MySQL e no SQL Server, e compara os dados dos dois.  O script compara tabela por tabela e retorn `True`, se os dados foram iguais, ou `False`, se encontrar alguma incosistência.

### RECRIANDO PROCEDURES, FUNCTIONS E VIEWS
Conecte-se ao banco de dados utilizando uma ferramente apropriada (no meu caso, utilizei o DBeaver 22.1.0). Execute os scripts do diretório `SQL` na ferramenta, recriando assim as procedures, functions e views. É possível que haja um aviso para algumas funções que elas chamam funções que não existem, mas essa serão criadas na mesma execução do script.

## SQL SERVER

### INSERÇÕES
À partir daqui, se todos os passos foram seguidos corretamente, já é possível realizar inserções através das procedures, assim como realizar outras operações no banco de dados migrado. É possível simular inserções recorrentes através da classe `Recurrent` do script `inserts`.

### BACKUP
O backup do banco de dados é feito executando o script `backup.py`. Ele cria um full backup dentro do container e então copia para o host. Depois faz uma varredura no diretório de backups, deixando apenas os três backups mais recentes.

É possível criar uma tarefa agendada que faz backup do banco de dados todos os dias, às 12h, executando o script `create_schedule.bat`.

### RECOVER
É possível recuperar as mudanças feitas desde a última inserções executando o script `recover.py`. Ele insere o último backup no container e executa a recuperação no servidor.

### REINDEX, STATISTICS E CRESCIMENTO
A reindexação pode ser feita executando a classe `Reindex` do script `scripts\stats\reindex.py`. Ela analisa a porcentagem de fragmentação de cada índice do banco e pode executar duas atividades: `REORGANIZE`, caso a fragmentação esteja entre 15 e 30%, ou `REBUILD`, caso a fragmentação seja maior que 30%.

As estatísticas podem ser atualizadas executando o script `scripts\stats\update.py`.

Já a projeção de crescimento pode ser obtida através do script `scripts\stats\growth.py`, passando os parêmetros **taxa de crescimento por 1000 inserções**, **média de inserções diárias** e **armazenamento total disponível**.

> Written with [StackEdit](https://stackedit.io/).