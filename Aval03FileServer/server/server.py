#!/usr/bin/env python3

##########################################>>> IMPORTANDO BIBLIOTECAS E ARQUIVOS ADICIONAIs <<<##########################################
import socket, threading, os, hashlib, glob

#######################################################>>> SESSÃO DE REDE/SOCKET <<<#######################################################
PORT = 20000
SERVER = 'localhost'

diretorio = os.path.dirname(os.path.abspath(__file__))
PASTA_SERVIDOR = os.path.join(diretorio,'arquivos')
MAX_CONNECTIONS = 5

# Criar pasta do servidor se não existir
if not os.path.exists(PASTA_SERVIDOR):
    os.makedirs(PASTA_SERVIDOR)

    diretorio = os.path.dirname(os.path.abspath(__file__))
    arq_list = os.listdir(os.path.join(diretorio, 'arquivos'))
    arq_list = ("\n".join(arq_list))


########################################>>> DEFININDO FUNÇÕES DO SERVIDOR/TRATAMENTO DE CLIENTES <<<########################################
def verificar_caminho_seguro(caminho):
    # Verifica se o caminho está dentro da pasta permitida
    caminho_real = os.path.realpath(caminho)
    pasta_real = os.path.realpath(PASTA_SERVIDOR)
    return os.path.commonpath([caminho_real, pasta_real]) == pasta_real

def listar_arquivos():
    try:
        arquivos = []
        for arq in os.listdir(PASTA_SERVIDOR):
            caminho = os.path.join(PASTA_SERVIDOR, arq)
            if os.path.isfile(caminho):
                tamanho = os.path.getsize(caminho)
                arquivos.append(f"{arq};{tamanho}")
        return "SUCESS|" + "\n".join(arquivos)
    except Exception as e:
        return f"ERRO|{str(e)}"

def enviar_arquivo(nome_arquivo, sock, posicao=0):
    caminho = os.path.join(PASTA_SERVIDOR, nome_arquivo)
    
    if not verificar_caminho_seguro(caminho) or not os.path.isfile(caminho):
        sock.send("ERRO|Arquivo não encontrado ou acesso negado".encode("utf-8"))
        return
    
    tamanho = os.path.getsize(caminho)
    sock.send(f"SUCESS|{tamanho}".encode("utf-8"))
    
    with open(caminho, 'rb') as f:
        if posicao > 0:
            f.seek(posicao)
        while True:
            dados = f.read(4096)
            if not dados:
                break
            sock.send(dados)

def calcular_hash(nome_arquivo, posicao):
    caminho = os.path.join(PASTA_SERVIDOR, nome_arquivo)
    
    if not verificar_caminho_seguro(caminho) or not os.path.isfile(caminho):
        return "ERRO|Arquivo não encontrado ou acesso negado"
    
    md5 = hashlib.md5()
    with open(caminho, 'rb') as f:
        if posicao > 0:
            dados = f.read(posicao)
        else:
            dados = f.read()
        md5.update(dados)
    
    return f"SUCESS|{md5.hexdigest()}"

def continuar_download(nome_arquivo, posicao, hash_cliente):
    caminho = os.path.join(PASTA_SERVIDOR, nome_arquivo)
    
    if not verificar_caminho_seguro(caminho) or not os.path.isfile(caminho):
        return "ERRO|Arquivo não encontrado ou acesso negado"
    
    # Verificar hash da parte existente
    md5 = hashlib.md5()
    with open(caminho, 'rb') as f:
        dados = f.read(posicao)
        md5.update(dados)
    
    if md5.hexdigest() != hash_cliente:
        return "ERRO|Hash não confere - arquivo corrompido ou modificado"
    
    tamanho_total = os.path.getsize(caminho)
    return f"SUCESS|{tamanho_total}"

def listar_arquivos_mascara(mascara):
    try:
        arquivos = []
        caminho_mascara = os.path.join(PASTA_SERVIDOR, mascara)
        
        for caminho in glob.glob(caminho_mascara):
            if os.path.isfile(caminho) and verificar_caminho_seguro(caminho):
                nome = os.path.basename(caminho)
                tamanho = os.path.getsize(caminho)
                arquivos.append(f"{nome};{tamanho}")
        
        return "SUCESS|" + "\n".join(arquivos)
    except Exception as e:
        return f"ERRO|{str(e)}"

def tratar_cliente(sock, endereco):
    print(f"Conexão estabelecida com {endereco}")
    
    try:
        while True:
            dados = sock.recv(4096).decode("utf-8").strip()
            if not dados:
                break
                
            partes = dados.split()
            comando = partes[0].upper()
            
            if comando == "LIST":
                resposta = listar_arquivos()
                sock.send(resposta.encode("utf-8"))
                
            elif comando == "DOWN" and len(partes) > 1:
                nome_arquivo = partes[1]
                enviar_arquivo(nome_arquivo, sock)
                
            elif comando == "CONT" and len(partes) > 3:
                nome_arquivo = partes[1]
                posicao = int(partes[2])
                hash_cliente = partes[3]
                resposta = continuar_download(nome_arquivo, posicao, hash_cliente)
                sock.send(resposta.encode("utf-8"))
                
                # Se o hash conferir, enviar o restante do arquivo
                if resposta.startswith("SUCESS"):
                    enviar_arquivo(nome_arquivo, sock, posicao)
                    
            elif comando == "MULTI" and len(partes) > 1:
                mascara = partes[1]
                resposta = listar_arquivos_mascara(mascara)
                sock.send(resposta.encode("utf-8"))
                
                # Esperar confirmação para cada arquivo
                while True:
                    confirmacao = sock.recv(4096).decode("utf-8").strip()
                    if confirmacao == "CONFIRM":
                        nome_arquivo = sock.recv(4096).decode("utf-8").strip()
                        enviar_arquivo(nome_arquivo, sock)
                    else:
                        break
                        
            elif comando == "HASH" and len(partes) > 2:
                nome_arquivo = partes[1]
                posicao = int(partes[2])
                resposta = calcular_hash(nome_arquivo, posicao)
                sock.send(resposta.encode("utf-8"))
                
            elif comando == "EXIT":
                print(f"Cliente {endereco} solicitou encerramento.")
                break
                
            else:
                sock.send("ERRO|Comando inválido".encode("utf-8"))
                
    except Exception as e:
        print(f"Erro com cliente {endereco}: {str(e)}")
    finally:
        sock.close()
        print(f"Conexão com {endereco} encerrada.")

#########################################################>>> INICIANDO SERVIDOR <<<#########################################################
sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_servidor.bind((SERVER, PORT))
sock_servidor.listen(MAX_CONNECTIONS)

print(f"Servidor iniciado em {SERVER}:{PORT}. Aguardando conexões...")

try:
    while True:
        sock_cliente, endereco = sock_servidor.accept()
        threading.Thread(target=tratar_cliente, args=(sock_cliente, endereco)).start()
except KeyboardInterrupt:
    print("\nServidor encerrado.")
finally:
    sock_servidor.close()