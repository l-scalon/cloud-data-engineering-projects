# Tema 12 - Terraform and Ansible

Nesse tema, utilizei as ferramentas estudadas até aqui para executar um pipeline que cria uma instância EC2, executa o código em container na instância criada e faz o sync do resultado com a S3. Ainda é possível fazer a análise dos dados gerados pelo app.

## PREPARAÇÃO

### PATHS

Os paths em `Jenkinsfile` devem apontar corretamente o caminho para o diretório `/cmd/local/` dentro do workspace.

No diretório `/cmd/local/`, os scripts `.sh` devem apontar corretamente para o diretório `terraform` dentro do workspace, e para os diretórios corretos na instância criada.

Em `/cmd/remote/run.sh`, insira o caminho do bucket para o qual o output será enviado.

Minha recomendação, para testar, é que o job criado no Jenkins tenha o nome `tema12` e que aponte para o um repositório de mesmo nome, cujo arquivo Jenkinsfile esteja no diretório raiz. Assim, não é preciso fazer nenhuma modificação nos paths.

### CHAVES

Em três arquivos, as chaves devem ser inseridas manualmente. 

Em `/app/scripts/twitterapi/auth.py`, insira as chaves da API do Twitter. 

Em `/cmd/local/preapre.sh` é preciso inserir o endereço do repositório com o token do Github, no formato `https://token@github.com/usuario/repositorio.git`

Em `/cmd/remote/run.sh`, insira as chaves da AWS, para que o script faça o sync corretamente. Ainda que não obrigatório, esse passo é importante para salvar o output, já que a máquina é destruída no fim do pipeline. Com o output salvo na S3 também será possível fazer a análise dos dados.

É importante, também, que as credenciais da AWS estejam definidas na máquina que vai executar o pipeline, já que elas serão utilizadas para a criação da instância remota.

### JENKINS

Para criar e executar o pipeline, é preciso ter o Jenkins instalado na máquina que irá fazê-lo. Siga as [instruções](https://github.com/ilegra/data-engineering-team/tree/main/Cloud%20Data%20Engineering%20Training/1-devops-and-cloud-basics/lucas-scalon/Tema%2009#jenkins) do Tema 09 para instalar e configurar o Jenkins, configurar o Github e criar o pipeline.

### TERRAFORM

Para criar uma instância remota, é preciso instalar o Terraform na instância em que o pipeline será executado. Já tendo acessado a instância, execute os seguintes comandos, um seguido do outro:

    sudo yum install -y yum-utils
    sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
    sudo yum -y install terraform

## APP

Assim como nos temas passados, o app criado faz download de três bases de dados do IMDB, procura pelos filmes feitos nos últimos 10 anos e então faz uma lista dos 10 atores que mais participaram desses filmes. Depois, faz uma busca no Twitter dos tweets que fazem menção a eles. Pela limitação da API, a pesquisa retorna os tweets dos últimos 7 dias.

O script, então, cria duas saídas: um arquivo `.csv` com os 10 nomes pesquisados e quantidade de resultados retornados (limitados a 100 para cada nome). E também um arquivo `html`, onde é possível visualizar os 10 tweets mais recentes obtidos como resposta da pesquisa, para cada nome pesquisado.

##  FERRAMENTAS

### JENKINS

Se configurado conforme as instruções acima, o Jenkins executará o pipeline do `Jenkinsfile`.  À partir daqui, a instância em que o Jenkins está executando será chamada de `local`, e a criada pelo Terraform será chamada de `remota`.

#### PIPELINE

1. **Declarative: Checkout SCM:** executado pelo Jenkins para buscar os arquivos no repositório, seguindo as configurações do pipeline.
2. **Prepare Scripts:** torna os scripts na instância `local` executáveis e garante que sejam legíveis pelo Linux. Como os scripts foram criados em Windows, podem haver erros de leitura, corrigidos pelo comando `sed`.
3. **Create Remote Instance:** executa o script `create.sh` na instância `local`, responsável por criar uma instância utilizando o Terraform.
4. **Prepare Remote Instance:** primeiro, aguarda 120 segundos para garantir que a instância `remota` foi iniciada com sucesso, e então executa o script `prepare.sh` na instância `local`. O script cria o diretório `tema12`, copia a chave criada pelo Terraform e envia instruções para a instância `remota`, através de conexão SSH utilizando seu DNS público. As instruções enviadas executam os seguintes passos na instância `remota`:
	* Update dos pacotes.
	* Instalação do Git.
	* Clone do repositório.
	* Preparação dos scripts.
	* Execução dos script `prepare.sh`.
O script executa os seguintes passos na instância `remota`:
		* Instalação do Docker.
		* Construção da imagem chamada `tema12` utilizando as instruções do Dockerfile.
		* Criação de um container chamado `tema12c`, baseado na imagem `tema12`.
5. **Run App:** na instância local, executa o script `run.sh`, que manda a instrução para a instância `remota` executar o script `run.sh`. O script executa o container `tema12c`, espera pela sua execução e copia o conteúdo da pasta output para a host. Então declara as credenciais da AWS e faz o sync da pasta de output da host com o bucket.
6. **Destroy Remote Instance:** na instância local, executa o script `destroy.sh`, que põe termo à instância `remota` criada pelo Terraform.

### TERRAFORM

Os comandos para iniciar, criar e destruir a instância serão feitos executando os scripts no pipeline. Caso deseje executá-los manualmente, acesse o diretório `terraform` e execute os comandos, respectivamente:

    sudo terraform init
    sudo terraform apply
    sudo terraform destroy

Nos dois últimos, a ferramenta perguntará se o usuário está seguro das alterações que o Terraform iria fazer, situação em que apenas a entrada `yes` será aceita para continuar. No entanto, é possível aplicar as alterações automaticamente usando o comando `-auto-approve` na frente de `apply` ou `destroy`.

#### MAIN(.)TF

Os arquivos .tf são os responsáveis por gerar os comandos que o Terraform irá executar. Não existe hierarquia de pastas ou nomes padrão para os arquivos, ou seja, o Terraform executará todos os arquivos .tf que estiverem no diretório, assim como nos subdiretórios.

##### PONTOS IMPORTANTES:

1. O arquivo utiliza as credenciais definidas no ambiente em que o Terraform está sendo executado, então é necessário que elas já tenham sido configuradas.
2. Um Key Pair chamado `terraformkp` é criado e utilizado para acessar a instância `remota`. Esse nome não deve ser modificado. No fim da pipeline, o par é destruído: a ideia é mesmo que ele seja utilizado apenas em uma sessão e descartado.
3. O ID do Security Group pode ser modificado ou deixado como está. Se modificado, é importante que seja um que aceite conexão SSH pela porta 22.
4. As tags `Name` e `Owner` podem ser modificados ou deixadas como está. As outras tags não devem ser modificadas.

### DOCKER

O Docker será instalado na instância `remota`, seguindo as instruções dos scripts, criará uma imagem com o app, utilizando as instruções do `Dockerfile` e criará um container que será rodado. Esses passos serão controlados pelo pipeline, não é necessária nenhuma configuração manual.

### STACK ELK

Se configurado corretamente, o script `run.sh`, da instância `remota`, fará o sync do output com o bucket S3. À partir daí, é possível fazer a análise dos dados gerados pelo app nos arquivos `.csv` utilizando o Kibana.

#### PREPARANDO

Os passos descritos são executados utilizado Windows como sistema operacional. Instale o Docker Desktop utilizando as [instruções](https://docs.docker.com/desktop/windows/install/) da sua documentação.

#### EXECUTANDO

Execute o arquivo `docker-compose-up.bat`, que criará o diretório `output`, caso ainda não exista, fará a cópia dos arquivos no bucket para o ambiente local e iniciará os containers da stack ELK.

### VISUALIZANDO

#### KIBANA

Acesse a GUI do Kibana através de um browser, pelo endereço: 
> http://localhost:5601/

No menu à esquerda, vá até **Stack Management**. Depois vá até **Index Patterns** e clique em **Create index pattern**. Em **Index patter name** digite `tweets`, e clique em **Next step**. Em **Time field**, selecione **@timestamp**. Finalmente, clique em **Create index pattern**.

Agora, no menu esquerdo, vá em **Dashboard**, e clique em **Create new dashboard**. Para, por exemplo, visualizar um gráfico de barras com os nomes pesquisados e a quantidade de resultados para cada um, clique em **Create visualization**. No menu dropdown, selecione o index pattern **tweets**. Em **Chart type**, selecione **Bar vertical**. Então arraste  o campo `name.keyword` para **Horizontal axis**, e o campo `results` para **Vertical axis**. Em **Vertical axis configuration**, selecione **Sum**.