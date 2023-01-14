# Tema 09 - Jenkins

### O que é e como utilizar?
Esse script tem o mesmo objetivo do utilizado no [Tema 07 v2](https://github.com/ilegra/data-engineering-team/tree/main/Cloud%20Data%20Engineering%20Training/1-devops-and-cloud-basics/lucas-scalon/Tema%2007/Tema%2007%20v2) e as instruções para sua utilização continuam as mesmas. Na estrutura principal foram feitas pequenas modificações para melhoria o código.
### O que há de novo?
Foram adicionados os arquivos `/jenkinsfile/tema09`, `/Scripts/test.py`, `/Scripts/cleanup.py` e `/Scripts/prepare.sh`.
> `tema09`

É um arquivo para ser utilizado pelo pipeline do Jenkins (mais sobre ele abaixo).
> `test.py`

Percebi durante a utilização do Jenkins que se eu fizesse o deploy antes de testar o script, poderia estar copiando um código falho. Criei um estrutura de teste bem básica que, ainda que não seja a ideal, garante que o código está funcionando antes de fazer deploy. Para ficar melhor, seria necessário mockar tudo que é independente do código (arquivos para download, API do Twitter etc.), porque qualquer falha de alguma dessas dependências interromperá o pipeline. Por ter que fazer o download e a análise, o teste acaba sendo demorado.
> `cleanup.py`

Fiz esse script para limpar tudo que foi criado pelo teste. No caso do Jenkins talvez não faça muito sentido porque o próprio pipeline exclui os diretórios do teste, mas ele pode ser utilizado em outras situações. Poderia criar uma tarefa que rodasse um .sh executando o cleanup, assim a pasta /tweets/ seria limpa de tempos em tempos, por exemplo.
> `prepare.sh`

Esse arquivo serve para o Jenkins preparar o ambiente em que o script será executado, no caso de haver um nova dependência.

## JENKINS
#### PREPARANDO EC2
Para ter acesso corretamente à GUI do Jenkins, é necessário que o security group da máquina EC2 tenha a seguinte regra de entrada:
> IP version: IPv4
> Type: Custom TCP
> Protocol: TCP
> Port range: 8080
#### INSTALANDO JENKINS
Já tendo se conectado à EC2, execute:

    $ sudo yum update -y
Depois siga as instruções de instalação para sistemas baseados em [CentOS](https://pkg.jenkins.io/redhat/). Para que o Jenkins inicie quando a instância for ativada, execute:

    $ sudo systemctl enable jenkins
Então ative e verifique se está ativado com os comandos:

    $ sudo systemctl start jenkins
    $ sudo systemctl status jenkins
 #### CONFIGURANDO GITHUB
 Essa configuração é necessária para que o Jenkins execute o pipeline toda vez que houver um `push` no repositório utilizado. Para realizar esse tema eu utilizei um repositório pessoal. No repositório, vá em **Settings**, no menu à esquerda vá em **Webhooks** e em **Add Webhook**. Em **Payload URL**, insira:
 

> `http://public-ipv4-dns:8080/github-webhook/`

Substituindo `public-ipv4-dns` pelo endereço da máquina EC2. Garanta que "Just the `push` event." esteja selecionado e crie o webhook.

Se você não tem um token do Github, no seu perfil do Github vá em **Settings**, no menu à esquerda vá em **Developer settings**, e então em **Personal access tokens**. Gere um token e salve em um local seguro. Ele será utilizado pelo Jenkins.

#### CONFIGURANDO JENKINS
Acesse o Jenkins através de um navegador, com o endereço:
> `http://public-ipv4-dns:8080/`

Substituindo `public-ipv4-dns` pelo endereço da máquina EC2. A senha solicitada pode ser encontrada na EC2 através do comando:

    sudo cat /var/lib/jenkins/secrets/initialAdminPassword
É possível criar um perfil e uma senha, mas essas etapas de configuração inicial podem ser puladas. Se não for criado um perfil, o acesso através do endereço é feito com o usuário `admin` e a senha encontrada com o comando acima.

No Dashboard do Jenkins, vá em **Manage Jenkins**, depois em **Manage Plugins**, em **Available** e pesquise por **Amazon EC2 plugin**. Selecione e clique em **Install without restart**.

Espere instalar, volte ao Dashboard e selecione **Configure a cloud**, **Add a new cloud** e selecione **Amazon EC2**. Dê um nome a ela, insira suas credenciais, selecione a região e salve.

Na EC2, acesse o arquivo `/etc/sudoers` utilizando um editor de texto e, na última linha, insira:

    jenkins ALL=(ALL) NOPASSWD: ALL
 E salve. Isso fará com que o Jenkins tenha privilégios do usuário root sem necessitar de uma senha.

#### CRIANDO PIPELINE
No Dashboard, vá em **New item**. Dê um nome e selecione **Pipeline**. Configure da seguinte forma:
#### 1. General

> GitHub project
	> Project url: `https://github.com/usuario/repositorio`

#### 2. Build Triggers

> GitHub hook trigger for GITScm polling

Também é possível criar um build periodicamente, com a sintaxe parecida com a utilizada no crontab. Marque a opção:

> Build periodically

E insira a periodicidade em que uma build será criada. Ao inserir `H 12 * * *`, por exemplo, haverá uma build todos os dias ao 12h, que executará a pipeline.

#### 3. Pipeline

> Definition: Pipeline script from SCM
	> SCM: Git
	> Repository URL: `https://token@github.com/usuario/repositorio.git`
	> Credentials: none
	> Branch Specifier: **
	> Script Path: path/to/jenkinsfile
	> Desative Lightweight checkout

O espaço `token` deve ser substituído pelo token gerado anteriormente. O caminho para o `jenkinsfile` tem como base a raiz do repositório e é nele que estará o script a ser executado pelo Jenkins.

Se tudo foi configurado corretamente, o Jenkins executará o pipeline toda vez que houver um `push` no repositório.

#### JENKINSFILE
A pipeline é executava com os seguintes passos:

**1. Checkout SCM**
Esse passo é feito configurado seguindo os passos anteriores. Ele faz um pull do repositório para a EC2.

**2. Prepare**
Prepara o ambiente executando o arquivo `prepare.sh`, que instala novas dependências. Também cria a pasta para executar testes.

**3. Test**
Testa o script e garante que não seja feito o deploy de um código defeituoso. Se houver qualquer erro nessa etapa o código não é copiado.

**4. Deploy**
O código é copiado da pasta do Jenkins para onde deverá ser executado na EC2. À partir daí o arquivo `run.sh`já pode ser rodado.