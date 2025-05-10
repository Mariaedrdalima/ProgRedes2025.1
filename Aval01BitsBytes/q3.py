# #!/usr/bin/env python3

# import os, sys, struct

# dir_atual= os.getcwd()

# print(dir_atual)
import os

dir_atual = os.path.dirname(__file__)
dir_image = os.path.join(dir_atual, 'IMG_20250509_184205.jpg')

try:
    


    with open(dir_image, 'rb') as f:
        app1DataSize = 0
        app1Data = 0

        #Pega os primeiros 6 bytes
        header = f.read(6)

        # Posições 4 e 5 = Tamanho dos metadados APP1
        app1DataSize = int.from_bytes(header[4:6], byteorder='big')

        f.close()

    print(f'app1DataSize: {app1DataSize}')

except PermissionError:
    print('Erro: Verifique as permissões de leitura do arquivo.')

except FileNotFoundError:
    print('Erro: Imagem não foi localizada.')