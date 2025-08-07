#!/usr/bin/env python3

##########################################>>> IMPORTANDO BIBLIOTECAS E ARQUIVOS ADICIONAIs <<<##########################################
import socket, threading, os, hashlib, glob

#######################################################>>> SESSÃO DE REDE/SOCKET <<<#######################################################
PORT = 20000
SERVER = 'localhost'

diretorio = os.path.dirname(os.path.abspath(__file__))
PASTA_CLIENTE = os.path.join(diretorio,'downloads')


########################################>>> DEFININDO FUNÇÕES DO CLIENTE/COMUNICAÇÃO COM O SERVER <<<########################################
def exibe_menu():
    print("""
        Escolha uma opção:
        1 - Listar arquivos do servidor
        2 - Download de 1 arquivo      
        3 - Continuar Download interrompido
        4 - Download de vários arquivos (com máscara)
        5 - Obter hash MD5 de arquivo
        6 - Sair
          
        Digite o número da opção desejada: """, end="")
    
    try:
        escolha = int(input())
        return escolha
    except ValueError:
        print("\nEntrada inválida! Digite um número.")
        return 0

def enviar_comando(comando):
    try:
        sockServer.send(comando.encode("utf-8"))
        resposta = sockServer.recv(4096).decode("utf-8")
        return resposta
    except Exception as e:
        print(f"\nErro na comunicação: {e}")
        return "ERRO"

def listar_arquivos():
    resposta = enviar_comando("LIST")

    if resposta.startswith("SUCESS"):

        arquivos = resposta.split("&")[1].split("\n")
        print("\n=== Arquivos no servidor ===")
        
        for arq in arquivos:
            if arq:  # Ignorar linhas vazias
                nome, tamanho = arq.split(";")
                print(f"{nome} - {tamanho} bytes")

        print("============================")
    else:
        print("\nErro ao listar arquivos:", resposta)


def download_arquivo():
    nome_arquivo = input("\nDigite o nome do arquivo para download: ").strip()
    resposta = enviar_comando(f"DOWN&{nome_arquivo}")
    
    if resposta.startswith("SUCESS"):
        tamanho = int(resposta.split("&")[1])
        caminho_local = os.path.join(PASTA_CLIENTE, nome_arquivo)
        
        # Verificar se arquivo já existe
        if os.path.exists(caminho_local):
            sobrescrever = input(f"Arquivo {nome_arquivo} já existe. Sobrescrever? (S/N): ").upper()
            if sobrescrever != 'S':
                print("Download cancelado.")
                return
        
        # Receber o arquivo
        with open(caminho_local, 'wb') as f:
            recebido = 0
            while recebido < tamanho:
                dados = sockServer.recv(4096)
                if not dados:
                    break
                f.write(dados)
                recebido += len(dados)
        
        print(f"\nDownload concluído: {nome_arquivo} ({recebido} bytes)")
    else:
       
        print("\nErro no download:", resposta.split("&")[1])

def continuar_download():
    nome_arquivo = input("\nDigite o nome do arquivo para continuar download: ").strip()
    caminho_local = os.path.join(PASTA_CLIENTE, nome_arquivo)
    
    if not os.path.exists(caminho_local):
        print("Arquivo não encontrado localmente. Faça um download normal primeiro.")
        return
    
    tamanho_atual = os.path.getsize(caminho_local)
    
    # Calcular hash da parte existente
    md5 = hashlib.md5()
    with open(caminho_local, 'rb') as f:
        md5.update(f.read())
    hash_atual = md5.hexdigest()
    
    resposta = enviar_comando(f"CONT&{nome_arquivo}&{tamanho_atual}&{hash_atual}")
    
    if resposta.startswith("SUCESS"):
        tamanho_total = int(resposta.split("&")[1])
        with open(caminho_local, 'ab') as f:
            recebido = tamanho_atual
            while recebido < tamanho_total:
                dados = sockServer.recv(4096)
                if not dados:
                    break
                f.write(dados)
                recebido += len(dados)
        
        print(f"\nDownload continuado: {nome_arquivo} ({recebido} bytes no total)")
    else:
        print("\nErro ao continuar download:", resposta.split("&")[1])





def download_multiplo():
    mascara = input("\nDigite a máscara para download (ex: *.txt): ").strip()
    resposta = enviar_comando(f"MULTI&{mascara}")
    
    if resposta.startswith("SUCESS"):
        arquivos = resposta.split("&")[1].split("\n")

        for arq_info in arquivos:
            if not arq_info:
                continue
                
            nome_arquivo, tamanho = arq_info.split(";")
            tamanho = int(tamanho)
            caminho_local = os.path.join(PASTA_CLIENTE, nome_arquivo)
            
            # Verificar se arquivo já existe
            if os.path.exists(caminho_local):
                sobrescrever = input(f"Arquivo {nome_arquivo} já existe. Sobrescrever? (S/N): ").upper()
                if sobrescrever != 'S':
                    print(f"Pulando {nome_arquivo}...")
                    continue
            
            # Confirmar download
            confirmar = input(f"Baixar&{nome_arquivo}&({tamanho} bytes)? (S/N): ").upper()
            if confirmar != 'S':
                continue
            
            # Enviar confirmação
            sockServer.send("CONFIRM&".encode("utf-8"))
            
            # Receber o arquivo
            with open(caminho_local, 'wb') as f:
                recebido = 0
                while recebido < tamanho:
                    dados = sockServer.recv(4096)
                    if not dados:
                        print(f"\nErro ao receber {nome_arquivo}. Download interrompido.")
                        break
                    f.write(dados)
                    recebido += len(dados)
            
            print(f"Download concluído: {nome_arquivo}")
    else:
        print("\nErro no download múltiplo:", resposta.split("&")[1])





def obter_hash():
    nome_arquivo = input("\nDigite o nome do arquivo: ").strip()
    posicao = input("Digite a posição final para cálculo do hash (deixe vazio para arquivo inteiro): ").strip()
    
    if not posicao:
        posicao = "0"
    elif not posicao.isdigit():
        print("Posição inválida!")
        return
    
    resposta = enviar_comando(f"HASH&{nome_arquivo} {posicao}")
    
    if resposta.startswith("SUCESS"):
        hash_value = resposta.split("&")[1]
        print(f"\nHash MD5 do arquivo {nome_arquivo} (até posição {posicao}): {hash_value}")
    else:
        print("\nErro ao obter hash:", resposta.split("&")[1])

#########################################################>>> INICIANDO CLIENTE <<<#########################################################
global sockServer
    
while True:
    try:
        sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sockServer.connect((SERVER, PORT))
     
        while True:
            escolha = exibe_menu()
                
            if escolha == 1:
                listar_arquivos()
            elif escolha == 2:
                download_arquivo()
            elif escolha == 3:
                continuar_download()
            elif escolha == 4:
                download_multiplo()
            elif escolha == 5:
                obter_hash()
            elif escolha == 6:
                enviar_comando("EXIT")
                print("\nSaindo...")
                break

            else:
                print("\nOpção inválida!")
             
                # Reconectar para próxima operação
            sockServer.close()
            break
                
    except ConnectionRefusedError:
        print("\nNão foi possível conectar ao servidor. Verifique se o servidor está rodando.")
        break
    except KeyboardInterrupt:
        print("\nSaindo...")
        if 'sockServer' in globals():
            sockServer.close()
        break
    except Exception as e:
        print(f"\nErro: {e}")
        if 'sockServer' in globals():
            sockServer.close()
        break