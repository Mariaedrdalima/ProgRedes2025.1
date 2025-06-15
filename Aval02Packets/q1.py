 #------------------------------------------------Bibliotecas necessárias-----------------------------------------------------
#!/usr/bin/env python3
import sys, struct, datetime


#---------------------------------------Funções auxiliares para formatar endereços---------------------------------------------
def mac_addr(bytes_mac): 
    """Converte bytes de endereço MAC para formato string (xx:xx:xx:xx:xx:xx)"""
    return ':'.join('%02x' % b for b in bytes_mac)

def ip_addr(bytes_ip):
    """Converte bytes de endereço IP para formato string (x.x.x.x)"""
    return '.'.join(str(b) for b in bytes_ip)

def parse_ethernet(quadro):
    """Analisa cabeçalho Ethernet e retorna tipo do protocolo e payload"""
    mac_destino = mac_addr(quadro[0:6])
    mac_origem = mac_addr(quadro[6:12])
    print(f"MAC Origem: {mac_origem} -> MAC Destino: {mac_destino}")
    
    # Extrai tipo do protocolo (2 bytes) e retorna com payload
    tipo_protocolo = struct.unpack('!H', quadro[12:14])[0]
    return tipo_protocolo, quadro[14:]

def parse_arp(pacote):
    """Analisa pacotes ARP"""
    # Extrai campos do cabeçalho ARP
    opcode = struct.unpack('!HHBBH', pacote[:8])[4]  # Código de operação
    mac_origem = mac_addr(pacote[8:14])
    ip_origem = ip_addr(pacote[14:18])
    mac_destino = mac_addr(pacote[18:24])
    ip_destino = ip_addr(pacote[24:28])
    
    print(f"ARP Op: {opcode} | MAC Origem: {mac_origem} -> MAC Destino: {mac_destino} | IP Origem: {ip_origem} -> IP Destino: {ip_destino}")

def parse_ipv4(pacote):
    """Analisa cabeçalho IPv4"""
    version_ihl = pacote[0]
    versao = version_ihl >> 4
    ihl = (version_ihl & 0x0F) * 4  # Tamanho do cabeçalho em bytes
    
    # Extrai campos do cabeçalho IP
    comprimento_total = struct.unpack('!H', pacote[2:4])[0]
    identificacao = struct.unpack('!H', pacote[4:6])[0]
    ttl = pacote[8]
    protocolo = pacote[9]
    ip_origem = ip_addr(pacote[12:16])
    ip_destino = ip_addr(pacote[16:20])
    
    print(f"IP Origem: {ip_origem} -> IP Destino: {ip_destino}")
    print(f"  Versão: {versao} | IHL: {ihl} | Tamanho Total: {comprimento_total} | ID: {identificacao} | TTL: {ttl} | Protocolo: {protocolo}")
    
    return protocolo, pacote[ihl:], ip_origem, ip_destino

def parse_icmp(pacote):
    """Analisa pacotes ICMP"""
    tipo_icmp, codigo_icmp = pacote[0], pacote[1]
    print(f"  ICMP Tipo: {tipo_icmp} | Código: {codigo_icmp}")
    
    # Se for mensagem Echo Request/Reply
    if tipo_icmp in (8, 0):
        identificador, sequencia = struct.unpack('!HH', pacote[4:8])
        print(f"  Echo ID: {identificador} | Seq: {sequencia}")

def parse_udp(pacote):
    """Analisa cabeçalho UDP"""
    porta_origem, porta_destino, comprimento = struct.unpack('!HHH', pacote[:6])
    print(f"  UDP Porta Origem: {porta_origem} -> Porta Destino: {porta_destino} | Comprimento: {comprimento}")

#-------------------------------------------Dicionário para rastrear conexões TCP----------------------------------------------
fluxos_tcp = {}

def parse_tcp(pacote, ip_origem, ip_destino):
    """Analisa cabeçalho TCP com controle de handshake"""
    porta_origem, porta_destino, seq, ack, offset_flags = struct.unpack('!HHLLH', pacote[:14])
    offset = (offset_flags >> 12) * 4  # Tamanho do cabeçalho TCP
    flags = offset_flags & 0x01FF       # Flags TCP
    janela = struct.unpack('!H', pacote[14:16])[0]
    
    print(f"  TCP Porta Origem: {porta_origem} -> Porta Destino: {porta_destino}")
    print(f"    Seq: {seq} | Ack: {ack} | Flags: {bin(flags)} | Janela: {janela}")

    # Chave para identificar a conexão
    chave = (ip_origem, ip_destino, porta_origem, porta_destino)
    chave_reversa = (ip_destino, ip_origem, porta_destino, porta_origem)
    dados_aplicacao = pacote[offset:]

    # Extrai flags importantes
    syn = flags & 0x02    # Flag SYN
    ack_flag = flags & 0x10  # Flag ACK

    # Máquina de estados para handshake TCP
    if syn and not ack_flag:  # Primeiro SYN
        fluxos_tcp[chave] = {"estado": "SYN", "exibido": False}
    elif syn and ack_flag and chave in fluxos_tcp and fluxos_tcp[chave]["estado"] == "SYN":  # SYN-ACK
        fluxos_tcp[chave]["estado"] = "SYN-ACK"
    elif ack_flag and not syn and chave_reversa in fluxos_tcp:  # ACK final
        fluxo = fluxos_tcp[chave_reversa]
        if fluxo["estado"] == "SYN-ACK" and not fluxo["exibido"]:
            if len(dados_aplicacao) > 0:
                print(f"    Dados de aplicação (até 200 bytes): {dados_aplicacao[:200]}")
            fluxo["exibido"] = True

    return offset, dados_aplicacao

# --------------------------------------------------Leitura dos Dados----------------------------------------------------------

if len(sys.argv) != 2:
    print(f"Uso: {sys.argv[0]} arquivo.pcap")
    sys.exit(1)

with open(sys.argv[1], "rb") as arquivo:
    # Verifica cabeçalho do arquivo PCAP
    cabecalho = arquivo.read(24)
    if len(cabecalho) < 24 or struct.unpack('I', cabecalho[:4])[0] != 0xa1b2c3d4:
        print("Formato de pcap inválido.")
        sys.exit(1)

    # Processa cada pacote no arquivo
    while (cabecalho_pacote := arquivo.read(16)) and len(cabecalho_pacote) == 16:
        # Extrai timestamp do pacote
        ts_segundos, ts_microsegundos, tam_incluido = struct.unpack("<III", cabecalho_pacote[:12])
        timestamp = datetime.datetime.fromtimestamp(ts_segundos) + datetime.timedelta(microseconds=ts_microsegundos)
        print(f"\n=== Pacote @ {timestamp} ===")

        # Lê dados do pacote
        dados_pacote = arquivo.read(tam_incluido)
        if not dados_pacote or len(dados_pacote) < 14:
            continue

        # Processa pacote Ethernet
        tipo_ether, payload = parse_ethernet(dados_pacote)

        # Encaminha para o parser específico
        if tipo_ether == 0x0806:  # ARP
            parse_arp(payload)
        elif tipo_ether == 0x0800:  # IPv4
            protocolo, payload_ip, ip_origem, ip_destino = parse_ipv4(payload)
            if protocolo == 1:    # ICMP
                parse_icmp(payload_ip)
            elif protocolo == 6:  # TCP
                parse_tcp(payload_ip, ip_origem, ip_destino)
            elif protocolo == 17: # UDP
                parse_udp(payload_ip)