#!/usr/bin/env python3

import socket
import os

HOST= "10.25.2.39"
PORT = 12345

sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockTCP.connect((HOST, PORT))
print("Tentando conexão...")



while True:
    
    try:
        # Convertendo a mensagem digitada de string para bytes
        message = input("Digite a mensagem a ser enviada no teste: ")
        message = message.encode('utf-8')
        sockTCP.send(message)
        sockTCP.recv()

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        break
