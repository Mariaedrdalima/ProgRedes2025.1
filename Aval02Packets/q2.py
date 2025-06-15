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
        
        # Procurar pelos metadados
        largura = 0
        altura = 0
        GPSLatitudeRef = ''
        GPSLongitude = ''



        #(3.b) "A partir da posição 18 de app1Data há efetivamente os metadados."
        pos = 18 
        
        for _ in range(num_metadados):

            #tags:
            tag = app1Data[pos:pos+2].hex() #Qual o metadado 
            tipo = int.from_bytes(app1Data[pos+2:pos+4], byteorder='big') #O tipo de metadado
            count = int.from_bytes(app1Data[pos+4:pos+8], byteorder='big') #número de repeticoes (tamanho)
            valor = app1Data[pos+8:pos+12] #Valor do metadado

#-----------------------------------------SESSÃO PARA TRATAR OS DADOS DE GPS-----------------------------------
            if tag == '8825':
                #88 25 00 04 00 00 00 01 00 00 1F 68
                #00 09 00 01 00 02 00 00 00 02 53 00 00 00 

                start_datagps = int.from_bytes(app1Data[pos+8:pos+12], byteorder='big') + 12
                total_datagps = int.from_bytes(app1Data[start_datagps-4:start_datagps-2], byteorder='big') * 12
                data_gps = app1Data[start_datagps:(start_datagps+total_datagps)]
                
                gps = 0

                for _ in range(total_datagps):

                    #tags:
                    tag_gps = data_gps[gps:gps+2].hex() #Qual o metadado 
                    tipo_gps = int.from_bytes(data_gps[gps+2:gps+4], byteorder='big') #O tipo de metadado
                    count_gps = int.from_bytes(data_gps[gps+4:gps+8], byteorder='big') #número de repeticoes (tamanho)
                    valor_gps = data_gps[gps+8:gps+12] #Valor do metadado

                    if tag == '0001':  #Referencia de Latitue
                        if tipo == 2:  #tipo "string"
                            GPSLatitudeRef = valor[:2]
                    elif tag == '0003': #Referencia de Longitude
                        if tipo == 2: #tipoe "string"
                            GPSLongitude = valor[:2]
                    #print(f'Data atual iniciando em: {data_gps[gps]} - tag {tag_gps} - valor {valor_gps}')

                    gps += 12
                print(f'Metadados GPS: {data_gps}')
                # print(f'''
                #     *******************************************
                #     Dados de GPS
                    
                #     Iniciando na Posição {pos}
                    
                #     Inicio dos Metatados no Bloco GPS {start_datagps}
                #     Número de metadados GPS: {total_datagps}
                #     Data GPS: {data_gps}
                    
                # ''')
               
           
#--------------------------------------------------------------------------------------------------------------           
            pos += 12  #Cada metadado ocupa 12 bytes, avanço de 12 em 12
        
        print(f'''
                    *******************************************
                    Tamanho dos metadados APP1: {app1DataSize}
                    Numero de metadados: {num_metadados}
                    Largura da imagem: {largura}
                    Altura da imagem: {altura}
                    ''')

except PermissionError:
    print('Erro: Verifique as permissões de leitura do arquivo.')

except FileNotFoundError:
    print('Erro: Imagem não foi localizada.')

except ValueError as e:
    print(f'Erro: {e}')

# except IndexError:
#     print(f'O indice referenciado para a lista de metadados é superior ao range de metadados. Execução interrompida.')
#     print(f'Metadados GPS: {data_gps}')