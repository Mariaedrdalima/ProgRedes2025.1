#!/usr/bin/env python3

import os

dir_atual = os.path.dirname(__file__)
dir_image = os.path.join(dir_atual, 'IMG_20250509_184205.jpg')

try:
    #(03): Ler os primeiros 6 bytes para obter app1DataSize
    with open(dir_image, 'rb') as f:
        header = f.read(6)
        app1DataSize = int.from_bytes(header[4:6], byteorder='big')
    
    #(3.a): Ler os metadados APP1
    with open(dir_image, 'rb') as f:

        f.read(4)  #Descartar os primeiros 4 bytes
        app1Data = f.read(app1DataSize)
        
        #Numero de metadados (posições 16-17)
        num_metadados = int.from_bytes(app1Data[16:18], byteorder='big')
        
        # Procurar pelos metadados de largura (0x0100) e altura (0x0101)
        largura = 0
        altura = 0


        #(3.b) "A partir da posição 18 de app1Data há efetivamente os metadados."
        pos = 18 
        
        for _ in range(num_metadados):

            #tags:
            tag = app1Data[pos:pos+2].hex() #Qual o metadado 
            tipo = int.from_bytes(app1Data[pos+2:pos+4], byteorder='big') #O tipo de metadado
            count = int.from_bytes(app1Data[pos+4:pos+8], byteorder='big') #número de repeticoes (tamanho)
            valor = app1Data[pos+8:pos+12] #Valor do metadado

            if tag == '0100':  #Largura
                if tipo == 3:  #tipo "Unsigned short"
                    largura = int.from_bytes(valor[:2], byteorder='big')
                elif tipo == 4:  #tipo "Unsigned long"
                    largura = int.from_bytes(valor, byteorder='big')
            elif tag == '0101':  #Altura
                if tipo == 3:  #tipo "Unsigned short"
                    altura = int.from_bytes(valor[:2], byteorder='big')
                elif tipo == 4:  #tipo "Unsigned long"
                    altura = int.from_bytes(valor, byteorder='big')

#-----------------------------------------SESSÃO PARA TRATAR OS DADOS DE GPS-----------------------------------
            elif tag == '8825':
                #88 25 00 04 00 00 00 01 00 00 1F 68
                inicio_metadados_gps = int.from_bytes(app1Data[pos+8:pos+12], byteorder='big') + 12
                metadados_gps = pos[inicio_metadados_gps:]

                print(f'''

                    *******************************************
                    Dados de GPS
                    
                    Iniciando na Posição {pos}
                    Numero de Metatados no Bloco GPS {inicio_metadados_gps}
                ''')

                
           
#--------------------------------------------------------------------------------------------------------------           
            pos += 12  #Cada metadado ocupa 12 bytes, avanço de 12 em 12
        
        # print(f'''
        #             *******************************************
        #             Tamanho dos metadados APP1: {app1DataSize}
        #             Numero de metadados: {num_metadados}

        #             Largura da imagem: {largura}
        #             Altura da imagem: {altura}

        #             Referência de Latitude:
        #             Latitude:

        #             Referência de Longitude:
        #             Longitude:

        #             Referência de Altitude:
        #             Altitude:
        #             ''')

except PermissionError:
    print('Erro: Verifique as permissões de leitura do arquivo.')

except FileNotFoundError:
    print('Erro: Imagem não foi localizada.')

except ValueError as e:
    print(f'Erro: {e}')