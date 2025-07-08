#!/usr/bin/env python3

import socket
HOST = "10.25.2.19"
PORT = 12345 #Definindo a porta





while True:
    
    try:
        # Criando o socket TCP
        print("Escutando...")
        sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockTCP.bind((HOST, PORT)) # Ligando o socket a porta
        sockTCP.listen(3) # Máximo de conexões enfileiradas

        while True:
            con, cliente = sockTCP.accept() # Aceita a conexão com o cliente
            print('Conectado por: ', cliente)

            #Recebendo
            message = con.recv(1024) #buffer de 1024 bytes

            #Se não receber mensagem -> Encerra
            if not message: break
            elif message == 'FIM': break

            print(f"mensagem recebida: {message.decode('utf-8')}")

            #Enviando mensagem de volta >>> Encerrando conexão
            print("Enviando mensagem ao cliente...")
            con.send(message)
            print('Finalizando Conexão do Cliente ', cliente)
            con.close()
        break
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")