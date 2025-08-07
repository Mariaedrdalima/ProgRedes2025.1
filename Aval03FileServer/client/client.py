#!/usr/bin/env python3

##########################################>>> IMPORTANDO BIBLIOTECAS E ARQUIVOS ADICIONAIs <<<##########################################
import socket, threading, os, struct
#from secret import BOT_TOKEN   # Importando o token do bot de um arquivo secreto



#######################################################>>> SESSÃO DE REDE/SOCKET <<<#######################################################
#Definindo porta e ip para o socket do servidor
PORT = 20000
SERVER = 'localhost'  # Pode ser alterado para o IP do servidor se necessário



########################################>>> DEFININDO FUNÇÕES DO CLIENTE/COMUNICAÇÃO COM O SERVER <<<########################################
# Exibindo menu ao cliente
def showMenu():
    print("""
        Escolha uma opção:
        1 - Listar arquivos do servidor
        2 - Download de 1 arquivo      
        3 - Continuar Download
        4 - Download de vários arquivos
        5 - Sair
          
        Digite o número da opção desejada: """, end="")
    
    escolha=int(input())

    return escolha


#Função para enviar pedido de listagem de arquivos

def get_arq_list():
    sockServer.send(('LIST').encode("utf-8"))
    arq_list = sockServer.recv(4096).decode()
    data = arq_list.split("&")

    # Verificando se a resposta do servidor é de sucesso para entender a lista de arquivos
    if data[0] == "SUCESS":
        arq_list = data[1].split("\n")

        if arq_list:
            print("""\nLista de arquivos disponíveis no servidor:""")

            for i, arq in enumerate(arq_list, start=1):
                print(f"""{i} - {arq}""")
            print(40* """*""")

            sockServer.close()

        else:
            print("O servidor não possui arquivos para compartilhar.")
    else:
        print(f"ERRO: {data[0]}")






#Função para enviar pedido de download de arquivo
def get_down(arq_down):

    sockServer.send(('DOWN'+"&"+arq_down).encode("utf-8"))
    arq_down = sockServer.recv(8192)  # Recebendo confirmação de download

    # if arq_down:
    #     print(f"Download do arquivo '{arq_down.decode()}' iniciado.")

    #     # Abrindo o arquivo para escrita
    #     with open(arq_down.decode(), 'wb') as f:

    #         while True:
    #             data = sockServer.recv(4096)
    #             if not data:
    #                 break
    #             f.write(data)

    #     print(f"Download do arquivo '{arq_down.decode()}' concluído.")

    #     showMenu()






#########################################################>>> INICIANDO CLIENTE <<<#########################################################
while True:
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