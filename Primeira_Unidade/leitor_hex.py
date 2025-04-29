#!/usr/bin/env python3

import os

dirfile = os.getcwd()
arqname = 'packipv4.txt'
arqdir = os.path.join(dirfile,arqname)

with open(arqdir, 'wb') as arq:
    arq.write(b'\x45\x00\x00\x38\x04\x88\x40\x00\x80\x11\x69\x34\xc0\xa8\x01\x69\xac\xd9\x1e\x0e')

while True:
    try:
        with open(arqdir, 'rb') as file:
            d = file.read()
        
        #escrevendo o IP e as demais informações:
        print(f'ip source:{d[8]}.{d[9]}.{d[10]}.{d[11]}')
        print(f'flag:{d[6] >> 5}')
        print(f'offset:{(d[6] & ((1<<5)-1) | d[7])}')

        break

    except ValueError:
        print("Erro")
