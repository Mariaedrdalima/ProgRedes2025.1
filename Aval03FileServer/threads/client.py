import socket, threading

PORT = 50000
SERVER = 'localhost'

def trataUsuario():
    nMsg = 1
    while True:
        msg = input (f"Digite msg ({nMsg}): +")
        sockClient.send((f"msg {nMsg} -> "+msg).encode())
        nMsg += 1

def trataServidor():
    while True:
        msg = sockClient.recv(4096)
        print (msg.decode())

    
sockClient = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sockClient.connect((SERVER, PORT))

tUsuario  = threading.Thread(target=trataUsuario)
tServidor = threading.Thread(target=trataServidor)

tServidor.start()
tUsuario.start()

tServidor.join()
tUsuario.join()

sockClient.close()