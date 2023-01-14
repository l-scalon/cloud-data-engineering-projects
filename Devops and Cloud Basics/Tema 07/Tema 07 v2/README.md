Essa é uma nova versão do script com o mesmo intuito do principal e que obtém os mesmos resultados, mas que exige menos recursos para ser processado. As instruções para sua utilização continuam as mesmas.

**O QUE MUDA?**
-----

 - O pandas agora é importado apenas com os módulos necessários para o script rodar.
 - Além de utilizar apenas as colunas necessárias, agora o tipo de dado em cada coluna também é definido na leitura do arquivo. Isso também resolve o DtypeWarning para uma das colunas que tem tipos mistos de dados.
 - Ao invés de ler todas as linhas de uma vez, agora a base de dados é dividida e processada em chunks, o que diminui a quantidade de recursos exigida. Testei o número de linhas na t2.micro da AWS e o tamanho dos chunks que ela processa sem problemas fica entre 10^4 e 10^6 linhas.
 - Coloquei print() para marcar etapas. 
 - Com essas modificações, o script, que antes exigia por volta de 8gb para ser processado, passa a poder ser executado em máquinas de pelo menos 1gb.