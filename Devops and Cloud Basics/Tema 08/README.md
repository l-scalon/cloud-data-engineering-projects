
**1. O que é?**
Um script que levanta, utilizando bases de dados do IMDB, os 10 atores que mais fizeram filmes nos últimos dez anos. Depois faz uma busca no Twitter, levantando os 10 tweets mais recentes que mencionam cada um desses atores, nos últimos 7 dias. No final, uma página HTML é gerada com esses tweets, que é inserida em uma pasta com data e horário que o script foi rodado. Foi desenvolvido utilizando Python 3.10 e funciona corretamente à partir do Python 3.6.x.

**2. Como utilizar?**
Primeiro, insira suas chaves de acesso no arquivo para isso (mais instruções abaixo). Em um *virtual environment* do Python, execute o seguinte comando:

    pip install -r requirements.txt
Então:

    cd path/to/Scripts/
E depois:

    python main.py
Então aguarde. A página HTML com os tweets estará em path/to/Scripts/tweets/data_e_horario/

**3. Como inserir as chaves de acesso?**
Abra o seguinte arquivo em um editor de texto:

> auth.py

Dentro dele, substitua cada um dos placeholders por sua chave de acesso de desenvolvedor da API do Twitter. Exemplo, se sua API Key for **1234**, no arquivo, onde está:

    API_Key = '<API KEY>'

Deve ficar:

    API_Key = '1234'
Repita isso para todas as chaves requisitadas.

**4. É possível utilizar o script sem as chaves de acesso?**
Não. As chaves de acesso são necessárias para acesso à API do Twitter.

**5. É preciso fazer download da base de dados?**
Não. O script faz isso sozinho.

**6. Qual a base da dados utilizada?**
A base utilizada é a fornecida pelo próprio IMDB, e pode ser acessada em: https://www.imdb.com/interfaces/

**7. Para que serve o arquivo /taskscheduler/run.bat?**
Este é um arquivo batch que pode ser utilizado para automatização da tarefa (ou seja, rodar o script) automaticamente e sincronizar com um S3 bucket da AWS.
Para tanto, é preciso já ter instalado um ambiente virtual do Python e as bibliotecas presentes no arquivo requirements.txt. Então é necessário substituir os paths e salvar. Depois, é só criar uma tarefa com o Task Scheduler.

**8. Como agendar uma tarefa no Task Scheduler?**
Na barra de tarefas do Windows, pesquise por Task Scheduler. No menu   direito, acesse a opção Create Basic Task. Em sequência, dê um nome para a tarefa e selecione a frequência em que ela será executada. Em Action, selecione Start a program e procure pelo arquivo /taskscheduler/run.bat. Depois de concluir a criação da tarefa, é possível editar a frequência em que ela é repetida.
 
 **9. A tarefa está sendo executada, mas para antes de baixar os arquivos, como posso resolver?**
Como o script cria arquivos temporários e faz o download da base de dados, é preciso que a tarefa tenha privilégios para isso. Na lista de tarefas ativas, selecione a tarefa criada e vá em Properties. Na aba General, ative a caixa "Run with highest privileges" e clique em OK.

**O QUE HÁ DE NOVO:**
-----

 - O código é o mesmo utilizado no commit [Add Tema 07 v2](https://github.com/ilegra/data-engineering-team/pull/25/commits/d238fa77dd7990653aca2174063323796a9bbb5e) no PR #25, mas sem o arquivo run.sh.
 - Criei o arquivo bash run.bat que, ao ser acionado por uma tarefa agendada do Windows na periodicidade definida pelo usuário, executa o script automaticamente, e faz o sync com um S3 bucket da AWS.