
# Tema 11 - Stack ELK
### O que é e como utilizar?
Esse script tem o mesmo objetivo do utilizado nos temas anteriores, mas fazendo log dos termos pesquisados e da quantidade de resultados e criando um arquivo `.csv` com eles. Neste caso, script é rodado dentro de um container Docker e enviado para a stack ELK, também rodando em um container. Todos os passos foram feitos utilizando Windows 10 como sistema operacional.

### O que há de novo?

* Fiz mudanças estruturais: o nome da pasta em que os resultados são inseridos mudou de `tweets` para `output`mas sua função continua a mesma. A criação das pastas com os resultados agora é feita pelo `folder_structure.py`. Algumas funções sofreram pequenas modificações para acompanhar essa mudança.
* Criei `log.py`, responsável por fazer log da query e da quantidade de resultados.
* Exclui `test.py` e `cleanup.py`, que não serão usadas nesse tema.
* Modifiquei `actor_names.py`, para coletar corretamente o index da referência em chunks. O que acontecia anteriormente é o script procurar pelo index absoluto, que muitas vezes estourava o limite do chunk. Agora, com o index absoluto, é feito um cálculo para encontrar o index relativo dentro do chunk.
* Criei `output.py`, responsável por criar o `.csv` com os termos pesquisados e a quantidade de resultados para cada um. Esse resultado está limitado a 100, nos últimos 7 dias.
* Os shell scripts `build.bat` e `run.bat` continuam tendo funções parecidas às suas versões em `.sh`, com modificações que refletem as necessidades do tema.
* Criei os arquivos necessários para rodar a Stack ELK em um container Docker.

## DOCKER
#### INSTALANDO
Instale o Docker Desktop, para Windows, seguindo as [instruções oficiais](https://docs.docker.com/desktop/windows/install/).  Este passo instalará tanto a Docker Engine quanto o Docker Compose.

 #### BUILD
Construa a imagem executando o script `build.bat`. Ele criará uma imagem chamada `tema11` usando as instruções do `Dockerfile`. Também cria um container chamado `tema11c`.

## ELK
Aqui, iremos utilizar o Docker Compose, que já vem instalado por padrão no Docker Desktop. 

#### BUILD
No Powershell, execute:

    wsl -d docker-desktop
Depois:

    sysctl -w vm.max_map_count=262144
 E então:

     exit
Isso é uma recomendação da documentação do Elasticsearch para que rode corretamente em um container.

Garanta que o Docker Desktop esteja executando, e então execute o script `docker-compose-up.sh` na pasta `docker-elk`.

Aguarde até que os componentes estejam rodando - no Docker Desktop os três devem estar com o símbolo verde e com status `RUNNING`.

## VISUALIZANDO OS RESULTADOS

#### KIBANA
Acessa a GUI do Kibana através de browser, pelo endereço: 
> http://localhost:5601/

No menu à esquerda, vá até **Stack Management**. Depois vá até **Index Patterns** e clique em **Create index pattern**. Em **Index patter name** digite `tweets`, e clique em **Next step**. Em **Time field**, selecione **@timestamp**. Finalmente, clique em **Create index pattern**.

Agora, no menu esquerdo, vá **Dashboard**, e clique em **Create new dashboard**. Parar, por exemplo, visualizar um gráfico de barras com os nomes pesquisados e a quantidade de resultados para um, clique em **Create visualization**. No menu dropdown, selecione o index pattern **tweets**. Em **Chart type**, selecione **Bar vertical**. Então arraste  o campo `name.keyword` para **Horizontal axis**, e o campo `results`para **Vertical axis**. Em **Vertical axis configuration**, selecione **Sum**.

Agora execute o arquivo `run.bat`. Além de rodar o container, o script fará a cópia da pasta `tema11/scripts/output/` para a host e o sync com a S3, caso a host esteja configurado corretamente para isso. 

Na visualização criada, clique em **Refresh** e os novos dados serão carregados.