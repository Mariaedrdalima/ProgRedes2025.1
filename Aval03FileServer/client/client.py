#!/usr/bin/env python3

##########################################>>> IMPORTANDO BIBLIOTECAS E ARQUIVOS ADICIONAIs <<<##########################################
import socket, threading, os, hashlib, glob

#######################################################>>> SESSÃO DE REDE/SOCKET <<<#######################################################
PORT = 20000
SERVER = 'localhost'
PASTA_CLIENTE = 'arquivos_cliente'

# Criar pasta do cliente se não existir
if not os.path.exists(PASTA_CLIENTE):
    os.makedirs(PASTA_CLIENTE)

########################################>>> DEFININDO FUNÇÕES DO CLIENTE/COMUNICAÇÃO COM O SERVER <<<########################################
def showMenu():
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
        arquivos = resposta.split("|")[1].split("\n")
        print("\n=== Arquivos no servidor ===")
        for arq in arquivos:
            if arq:  # Ignorar linhas vazias
                nome, tamanho = arq.split(";")
                print(f"{nome} - {tamanho} bytes")
        print("============================")
    else:
        print("\nErro ao listar arquivos:", resposta)
 


#########################################################>>> INICIANDO CLIENTE <<<#########################################################


global sockServer
    
while True:
    try:
        sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sockServer.connect((SERVER, PORT))
            
        while True:
            escolha = showMenu()
                
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


while True:
    global sockServer
    #iniciando o socket do servidor
    sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sockServer.connect((SERVER, PORT)) #Conectando ao servidor

    try:    
        escolha = showMenu()

        if escolha == 1:
            get_arq_list()

        elif escolha == 2:
            arq_down = input("Digite o nome do arquivo que deseja baixar: ")
            get_down(arq_down)

        elif escolha == 3:
            print("CONTINUAR DOWNLOAD")

        elif escolha == 4:
            print("DOWNLOAD DE VÁRIOS ARQUIVOS")

        elif escolha == 5:
            print("\n Saindo...")
            break



################################################>>> Sessão de erro para opções inválidas <<<###############################################
    except TypeError:
        print("Opção inválida. Por favor, escolha uma opção válida.")

    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")

    except KeyboardInterrupt:
        print("\n Saindo do cliente. Crtl+C pressionado.")






# tUsuario  = threading.Thread(target=trataUsuario)
# tServidor = threading.Thread(target=trataServidor)

# tServidor.start()
# tUsuario.start()

# tServidor.join()
# tUsuario.join()

# sockClient.close()