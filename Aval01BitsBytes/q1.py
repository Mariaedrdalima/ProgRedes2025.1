#!/usr/bin/env python3
#Acima vou inserir a 

import os
import sys

# Os argumentos passados na execução do código (exceto o nome do script)
args = sys.argv

# Acessar argumentos específicos
if len(args) >= 3:  # Garantir que pelo menos dois argumentos foram passados
    ip = args[1]
    mask = args[2]

    while True:
        try:

            print(f"IP: {ip}, Bits zero: {mask}")

            #escrevendo o IP e as demais informações:
            # print(f'ip source:{arq[8]}.{arq[9]}.{arq[10]}.{arq[11]}')
            # print(f'flag:{arq[6] >> 5}')
            # print(f'offset:{(arq[6] & ((1<<5)-1) | arq[7])}')



            break

        except ValueError:
            print("Erro")

else:
    print("Uso correto: ./leitor_hex <IP> <QUANTIDADE DE BITS ZERO - informar um número inteiro de 0 a 32>")




