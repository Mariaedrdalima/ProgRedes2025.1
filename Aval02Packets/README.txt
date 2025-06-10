1) Faça um programa que recebe na linha de comando o nome de um arquivo
correspondente a uma captura de tráfego (arquivo .pcap) e apresenta, para cada
pacote:

a) Os MAC addresses de origem e destino do frame;

b) Se o protocolo transportado no enlace for ARP ou RARP e o tipo do protocolo
for IPv4, apresente:
	• O código da operação (ARP ou RARP)
	• Os MAC adresses do remetente e do destinatário;
	• Os endereços IPv4 do remetente e do destinatário;

c) Se o protocolo transportado no enlace for IPv4:
	• Mostre os endereço IPv4 de origem e destino;
	• Escolha mais quatro campos para também exibir;

d) Se o protocolo transportado no IPv4 for ICMP:
	▪ Mostre o nome do tipo do pacote (basta cinco, ignore outros)
	▪ Exiba também, se o tipo for echo request ou echo reply,:
		• O número do identificador;
		• O número de sequência.

e) Se o protocolo transportado no IPv4 for UDP:
	• Mostre as portas de origem e destino do datagrama;

f) Se o protocolo transportado no IPv4 for TCP:
	• Mostre as portas de origem e destino do datagrama;
	• Exiba mais quatro campos a sua escolha;

g) Para os protocolos de aplicação carreados no TCP, exiba até 200 bytes em
cada sentido no primeiro pacote depois dos SYN, SYN/ACK.

*******************************************************************************************************
2) Faça um programa que receba na linha de comando um arquivo com o nome de uma
foto, em formato jpeg, e abra um navegador com um mapa contendo o ponto de
localização em que a foto foi tirada (Se não existe georeferenciamento na foto,
indique o erro). Use o OpenStreet Map. A única biblioteca permitida é subprocess.