#ATIVIDADE AVAL04BOTTELEGRAM - Disciplina de Programação para Redes - Semestre 2025.1

##Desenvolvido por Eduarda Lima e Kalyne Rodrigues - Para a disciplina de de Programação de 

Acessando o bot:
@madunetbot -> /start (me sinalizar antes para que eu possa "ligar" o servidor)



#Comandos implementados
/ping -> O server vai utilizar o comando "ipconfig" para capturar o IP e GATEWAY, depois vai utilizar essas informações para capturar o tempo médio do ping entre o IP server e o GATEWAY da rede do server


/dns -> O server vai utilizar  o comando "nslookup /" (usei a barra no final pra ele encerrar o comando e devolver o dns server para onde ele requisitou a resolução de nome do "/")
devolve o ip e nome do server dns

/route_print -> Vai enviar a tabela de roteamento para o cliente no telegram

/imagem url_imagem -> aqui eu não vou chamar a função de executar comando, eu vou chamar direto a função que envia os dados pro cliente no telegram, ajusto o endpoint para /sendPhoto e o formato do envio para "photo", passo como paramentro a url.

/systeminfo -> O server vai utilizar o comando "systeminfo" para pegar as informações de sistema da máquina onde está rodando o server, vai formatar e enviar para o cliente no telegram
