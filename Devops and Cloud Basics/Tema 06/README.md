**1. O que é?**
Um script que levanta, utilizando bases de dados do IMDB, os 10 atores que mais fizeram filmes nos últimos dez anos. Depois faz uma busca no Twitter, levantando os 10 tweets mais recentes que mencionam cada um desses atores, nos últimos 7 dias. No final, uma página HTML é gerada com esses tweets. Foi desenvolvido utilizando Python 3.10 e funciona corretamente à partir do Python 3.6.x.

**2. Como utilizar?**
Primeiro, insira suas chaves de acesso no arquivo para isso (mais instruções abaixo). Em um *virtual environment* do Python, execute o seguinte comando:

    pip install -r requirements.txt
Então:

    cd path/to/Scripts/
E depois:

    python main.py
Então aguarde. A página HTML com os tweets será aberta sozinha no seu aplicativo padrão para esse tipo de arquivo.

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