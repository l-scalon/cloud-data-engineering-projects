# Tema 10 - Docker and Containers
### O que é e como utilizar?
Esse script tem o mesmo objetivo do utilizado nos temas anteriores, com a diferença que ele pode ser montado e rodado como um container Docker. Ainda é necessário manter uma venv do Python na máquina para o Jenkins realizar os testes, assim como substituir as credenciais no arquivo `auth.py` e, para fazer o sync com a S3, configurar as credenciais da AWS na máquina host. Também assume-se que o usuário já tenha o Jenkins instalado e configurado na máquina, assim como o GitHub. Eu mantive os paths originais para exemplificação do código.

### O que há de novo?
Foram feitas algumas mudanças no código seguindo o que foi conversando com os mentores. Foram elas:
* Antes, toda a estrutura das pastas era incluída no repositório. Agora só as pastas necessárias para o código rodar são incluídas, cabendo ao próprio código criar essa estrutura de pastas localmente.
* Melhorei a função de criação de pastas com data e hora, para não incluir espaços no nome.
* Corrigi o script de limpeza, que é executado após o teste, e que continha um erro de parâmetro na hora de chamar outra função.
* Foram adicionados shell scripts que são executados pelo Jenkins em cada uma de suas etapas.

Ainda pretendo melhorar no futuro o sistema de autenticação da API do Twitter, utilizando variáveis locais ao invés do `auth.py`.

## DOCKER
#### INSTALANDO
Já tendo se conectado à EC2, execute:
`$ sudo yum update -y`

Instale o Docker com:
`$ sudo amazon-linux-extras install docker`

Para que o Docker inicie-se com o sistema, execute:
 `$ sudo systemctl enable docker`
 
Então ative e verifique se está ativado com os comandos:
`$ sudo systemctl start docker`
`$ sudo systemctl status docker`

 Por fim, permita que o Docker execute comandos sem utilizar `sudo`:
 `$ sudo usermod -a -G docker ec2-user`

Com essas passos, já é possível utilizar o Jenkins para montar uma imagem e rodar um container à partir dela.

 #### DOCKERFILE
O `Dockerfile`é o responsável por dar instruções ao Docker de como construir a imagem. Neste caso, ele utiliza como base a imagem do Python 3, disponível no Docker Hub. Depois cria o diretório `/tema10/`, declara-o como diretório raiz e copia o conteúdo de onde o `Dockerfile` está sendo executado para esse diretório criado. Então, instala as dependências do `requirements.txt` e, por fim, declara o ponto de entrada com `CMD`. Isso significa que este é o script que será executado quando o container for iniciado: neste caso, o script `main.py` utilizando Python.

#### JENKINSFILE
O `Jenkinsfile` é o responsável por orquestrar a execução ordenada dos shell scripts.

**Checkout SCM**
Configurado no próprio job do Jenkins. Ele faz um `pull` do repositório para a máquina, e depende da configuração do trigger. É nesse passo que o Jenkinsfile é lido e executado.

**Options**
Adicionei uma configuração que desabilita uma build caso uma nova seja iniciada. Isso garante que o Jenkins não tente rodar duas builds ao mesmo tempo, gerando conflitos de arquivos e gargalos de memória.

**Test**
Executa o script `test.sh`. O script ativa a venv, instala as dependências e testa o código. Só dá continuidade na pipeline se o resultado do teste for positivo, prevenindo que a imagem seja montada com um código defeituoso. Deixei comentado porque sua execução é instável e eu não consegui encontrar exatamente onde está o problema. Quando rodo manualmente o script, ele executa normalmente, mas dentro do Jenkins algumas vezes ele trava e não consegue continuar.

**Prepare**
Executa o script `prepare.sh`. Cria o diretório para onde o arquivo `run.sh` será copiado, copia e o torna executável. Faz parar o container `tema10c`, caso exista e esteja em execução, e o remove, caso exista.

**Build Image**
Executa o script `build.sh`. Constrói uma imagem chamada `tema10` à partir das instruções no `Dockerfile`.

**Create Container**
Executa o script `create.sh`. Cria um container chamado `tema10c` baseado na imagem criada no passo anterior.

**Cleanup**
 Executa o script `cleanup.sh`. Faz uma limpeza das imagens que não estejam sendo utilizadas por nenhum container, caso existam.

**Reboot**
Executa o script `restart.sh`, sem esperar pelo término de sua execução. O script aguarda 30 segundos e então reinicia a máquina host. Isso foi necessário por um problema que eu estava tendo: após a criação de uma imagem, um container baseado nela rodava, mas travava a máquina. Tentei alguns troubleshootings, mas nada resolveu. Ainda que eu não tenha descoberto o exato problema, esse foi um workaround que resolveu.

#### RODANDO O CONTAINER
O container pode ser rodado executando o arquivo `run.sh` que, por default, fica em `/home/ec2-user/cmd/`. Ele executa o container, copia os resultados gerados para o host e faz o sync com a S3, caso as credenciais estejam configuradas e os paths inseridos corretamente.