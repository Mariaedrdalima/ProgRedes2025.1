#!/usr/bin/env python3

import socket, os

HOST= "10.25.2.19"
PORT = 12345

while True:
    
    try:
        print("Tentando conexão...")
        sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockTCP.connect((HOST, PORT))           
        
        # Convertendo a mensagem digitada de string para bytes
        message = input("Digite a mensagem a ser enviada no teste: ")
        message = message.encode('utf-8')
        sockTCP.send(message)
        messageback = sockTCP.recv(1024)
        print(f'Message back: {messageback}')
        break

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        break