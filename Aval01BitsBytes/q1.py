#!/usr/bin/env python3

import os, sys, struct

# Os argumentos passados na execução do código
args = sys.argv

#--------------------------------------Acessar argumentos passados------------------------------------------------
# Garamtir que pelo menos dois argumentos foram passados - 
if len(args) >= 3:  
    host = args[1] #IP
    mask = int(args[2]) #Bits em zero
    ipblocos = host.split(".") #Aqui eu tenho uma lista somente com os blocos de ip separados pelo ponto


    while True:
        try:
            #----------------------------------Tratando o IP--------------------------------------------------------------
            #Concatendo os blocos em um unico inteiro cujos 4 blocos de 8 bits equivalem aos blocos ips
            ip = 0
            for bloco in ipblocos:
                ip = (ip << 8) | int(bloco)
            
            hosts = (2**mask)-2

            #----------------------------------Rede-----------------------------------------------------------------------
            #Bits zeros para a direita e depois à esquerda, em seguida obtenho essa informação em 4 blocos de 8 bits
            redebytes = struct.pack(">I",((ip >> mask) << mask))
            rede = struct.unpack(">BBBB",redebytes)
            

            #----------------------------------Broadcast------------------------------------------------------------------
            #Mesma lógica acima, mas deixei a quantidade de bits zeros todos em 1
            broadcastbytes = struct.pack(">I", (ip >> mask) << mask | (1<<mask)-1)
            broadcast = struct.unpack(">BBBB",broadcastbytes)
            

            #----------------------------------Gateway--------------------------------------------------------------------
            gatewaybytes = struct.pack(">I", ((ip >> mask) << mask | (1<<mask)-2)) #menos 2 para chegar ao ultimo endereõ valido
            gateway = struct.unpack(">BBBB",gatewaybytes)



            print(f"""
                IP: {host}, Bits zero: {mask}
                Rede: {rede[0]}.{rede[1]}.{rede[2]}.{rede[3]}
                Broadcast: {broadcast[0]}.{broadcast[1]}.{broadcast[2]}.{broadcast[3]}
                Gateway: {gateway[0]}.{gateway[1]}.{gateway[2]}.{gateway[3]}
                Quantidade de hosts para essa rede: {hosts}
            """)

            break

        except ValueError as e:
            print(f'Erro: {e}')
            break

        except struct.error as e:
            print(f'Erro: Revisar o formato dos argumentos passados. Cada bloco do ip pode variar de 0 a 255 e bits zeros de 2 a 32.')
            break


else:
    print("Uso correto: ./leitor_hex <IP> <QUANTIDADE DE BITS ZERO - informar um número inteiro de 0 a 32>")