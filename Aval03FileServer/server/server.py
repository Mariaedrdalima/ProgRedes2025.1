#! /usr/bin/env python3

import socket, threading, struct, os, sys

SERVER = 'localhost'
PORT = 20000
allClients = []


# ###################################################>>> TRATANDO SOLICITAÇÕES DO CLIENTE <<<#############################################
def send_arq_list():
    # Obtendo a lista de arquivos do servidor
    print("Cliente pediu lista de arquivos")
    diretorio = os.path.dirname(os.path.abspath(__file__))
    arq_list = os.listdir(os.path.join(diretorio, 'arquivos'))
    arq_list = ("\n".join(arq_list))

    print(arq_list)

    
    # Enviando a lista de arquivos para o cliente
    sockCon.send(("SUCESS"+"&" + arq_list).encode("utf-8"))
    print("Lista de arquivos enviada ao cliente.")
    print()
    sockCon.close()
    return 'break'


def trataCliente(sockCon, origem):
    print(f"Tratando conexão com {origem}")
    print()

    while True:
        req = sockCon.recv(4096)
        req = req.split(b"&")

        req_cliente = req[0].decode("utf-8")

        if req_cliente == 'LIST':
            send_arq_list()
            break
        
        elif req_cliente == 'DOWN':
            arq_down = req[1].decode("utf-8")
            print(f"Cliente pediu download do arquivo: {arq_down}")
            sockCon.close()
            allClients.remove(sockCon)
            break

        elif req_cliente == 'MULTI':
            print(f"Cliente pediu download de vários arquivos: {arq_down}")
            sockCon.close()
            allClients.remove(sockCon)
            break 

        elif req_cliente == 'EXIT':
            print("Cliente pediu para sair")
            sockCon.close()
            allClients.remove(sockCon)
            break

        else:
            print(f"Requisição desconhecida: {req_cliente}")
            sockCon.send(("ERRO: Requisição "+req_cliente+" nvalida").encode("utf-8"))
            sockCon.close()
            break

        break


sockServer = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sockServer.bind((SERVER, PORT))
sockServer.listen(5)

while True:
    print ("Aguardando conexão ...")
    sockCon, origem = sockServer.accept()
    trataCliente(sockCon, origem)
    break

#     #threading.Thread(target=trataCliente, args=(sockCon, origem)).start()