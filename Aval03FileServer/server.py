import socket, threading

SERVER = ''
PORT = 50000
allClients = []

def trataCliente(sockCon, origem):
    print (f"Tratando conexão com {origem}")

    while True:
        msg = sockCon.recv(4096)
        print (f"Recebi de {origem} -> {msg.decode()}")
        sockCon.send(msg)

sockServer = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sockServer.bind((SERVER, PORT))
sockServer.listen(5)

while True:
    print ("Aguardando conexão ...")
    sockCon, origem = sockServer.accept()
    threading.Thread(target=trataCliente, args=(sockCon, origem)).start()