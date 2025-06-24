#!/usr/bin/env python3

import socket
HOST = '10.25.2.39'
PORT = 12345 #Definindo a porta


# Criando o socket TCP
sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockTCP.bind((HOST, PORT)) # Ligando o socket a porta
sockTCP.listen(1) # Máximo de conexões enfileiradas


while True:
    con, cliente = sockTCP.accept() # Aceita a conexão com o cliente

    print('Conectado por: ', cliente)
    
    try:
        #Recebendo
        message = con.recv(1024) #buffer de 1024 bytes
        print(f"mensagem recebida: {message.decode('utf-8')}")

        if not message: break
        
        #Enviando para encerrar
        print("Enviando mensagem ao cliente...")
        con.send(message)
        print('Finalizando Conexão do Cliente ', cliente)
        con.close()
        break

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
