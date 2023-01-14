
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

**7. Para que serve o arquivo crontab/run.sh?**
Este é um arquivo bash que pode ser utilizado para automatização da tarefa (ou seja, rodar o script) automaticamente e sincronizar com um S3 bucket da AWS.
Para tanto, é preciso já ter instalado um ambiente virtual do Python e as bibliotecas presentes no arquivo requirements.txt. Então é necessário substituir os paths e salvar. Depois, é só incluir o arquivo na rotina do crontab.

**8. Como agendar uma tarefa no crontab?**
Execute os seguintes comandos:

    $ sudo crontab -e
  Se o arquivo crontab para o usuário root não existir, ele será criado. Então tecle i, [digite o comando](https://medium.com/totvsdevelopers/entendendo-o-crontab-607bc9f00ed3), tecle ESC, depois digite :wq e tecle ENTER. Isso irá salvar e executar a tarefa conforme a frequência agendada. Exemplo, para fazer com o que este script execute a cada 5 minutos, deve ser inserido no crontab:
  

    */5 * * * * /path/to/Scripts/crontab/run.sh
   Importante: o path para o arquivo deve ser absoluto.
 
 **9. O script não está sendo executado, como posso resolver?**
Se depois de seguir os passos, o script não estiver sendo executado, tente as possíveis soluções:
a. Cheque se os paths no arquivo run.sh estão corretos.
b. Cheque se o path absoluto para o arquivo run.sh, no crontab, está correto. Você pode fazer isso utilizando o comando pwd no diretório do arquivo run.sh.
c. Cheque se o arquivo run.sh está rodando. Para isso, vá até o diretório do arquivo, e então execute:

    $ chmod +x run.sh
    $ ./run.sh
 Isso deve executar o script main.py e fazer o sync com o bucket.
 
 **10. Segui os passos anteriores e obtive o seguinte erro: "/bin/bash^M: bad interpreter: No such file or directory"**
 Execute o comando:
 
	$ sed -i -e 's/\r$//' run.sh
	$ ./run.sh
Isso deve executar o script main.py e fazer o sync com o bucket.

**O QUE HÁ DE NOVO:**
-----

 - Os tweets coletados agora são colocados em pastas com o dia e o horário em que o script foi executado.
 - A página HTML não mais abre sozinha e os arquivos de dados são excluídos depois de utilizados.
 - Corrigi o problema que dava erro nos paths. Agora os paths são independentes do SO utilizado. Há também um novo script para coletar o caminho absoluto da pasta.
 - O script agora exige uma versão anterior do *pandas*, para que funciona corretamente com Python 3.6 em diante.
 - Modifiquei a abertura dos arquivos de dados, para que sejam carregadas apenas as colunas necessárias para o script. Pretendo fazer ainda mais mudanças para que o *pandas* exija menos recursos.
 - Criei o arquivo bash run.sh que, ao ser adicionado à rotina do crontab, executa o script automaticamente na periodicidade definida pelo usuário, e faz o sync com um S3 bucket da AWS.