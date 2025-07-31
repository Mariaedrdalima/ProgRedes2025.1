#!/usr/bin/env python3

import socket, threading, os

#Definindo porta e ip para o socket do servidor
PORT = 50000
SERVER = ''


########################################>>> DEFININDO FUNÇÕES DO CLIENTE <<<########################################
# Exibindo menu ao cliente
def showMenu():
    escolha=int(input(print("""
        **** Confirme qual opção deseja ****
        1 - Listar arquivos do servidor
        2 - Download de 1 arquivo      
        3 - Continuar Download
        4 - Download de vários arquivos
        5 - Sair
    """)))

    return escolha

def sendMessage():
    msg = 1
    while True:
        msg = input (f"Digite msg ({nMsg}): +")
        sockClient.send((f"msg {nMsg} -> "+msg).encode())
        nMsg += 1

def serverJob():
    while True:
        msg = sockClient.recv(4096)
        print (msg.decode())




########################################>>> INICIANDO CLIENTE <<<########################################

# #iniciando o socket do servidor
sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sockServer.connect((SERVER, PORT)) #Conectando ao servidor

try:
    while True:
        escolha = showMenu()

        if escolha == 1:
            print("LISTAR")

        elif escolha == 2:
            print("DOWNLOAD DE 1 ARQUIVO")

        elif escolha == 3:
            print("CONTINUAR DOWNLOAD")

        elif escolha == 4:
            print("DOWNLOAD DE VÁRIOS ARQUIVOS")

        elif escolha == 5:
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

except KeyboardInterrupt:
    print("\nSaindo do cliente. Crtl+C pressionado.")
        








# tUsuario  = threading.Thread(target=trataUsuario)
# tServidor = threading.Thread(target=trataServidor)

# tServidor.start()
# tUsuario.start()

# tServidor.join()
# tUsuario.join()

# sockClient.close()