#Analisador de Pacotes PCAP
##Este script Python analisa arquivos de captura de rede no formato PCAP, exibindo informações detalhadas sobre os pacotes e protocolos de rede.

###Funcionalidades:
Análise de protocolos Ethernet, IPv4, ARP, ICMP, TCP e UDP
Exibição de metadados de pacotes (timestamps, endereços, portas)
Controle de handshake TCP para identificar início de conexões
Exibição dos primeiros 200 bytes de dados de aplicação após handshake TCP
Suporte a arquivos PCAP no formato padrão

###Como Usar
Certifique-se de ter Python 3 instalado
Execute o script passando um arquivo PCAP como argumento:

python3 q1.py arquivo_captura.pcap

Protocolos Suportados: Ethernet, ARP, IPv4, ICMP, TCP e UDP.

Exemplo de Saída:

=== Pacote @ 2023-01-01 12:34:56.789012 ===
MAC Origem: aa:bb:cc:dd:ee:ff -> MAC Destino: ff:ee:dd:cc:bb:aa
IP Origem: 192.168.1.1 -> IP Destino: 192.168.1.2
  Versão: 4 | IHL: 20 | Tamanho Total: 60 | ID: 1234 | TTL: 64 | Protocolo: 6
  TCP Porta Origem: 443 -> Porta Destino: 54321
    Seq: 123456789 | Ack: 987654321 | Flags: 0b10010 | Janela: 64240
    Dados de aplicação (até 200 bytes): b'\x17\x03\x03\x00...'

Observações
O script foi desenvolvido para fins educacionais
Funciona com arquivos PCAP no formato padrão (little-endian)
Exibe apenas os primeiros 200 bytes de dados de aplicação após handshake TCP completo