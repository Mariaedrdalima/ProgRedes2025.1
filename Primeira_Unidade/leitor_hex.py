#!/usr/bin/env python3

import os

dirfile = os.getcwd()
arqname = 'packipv4.txt'
arqdir = os.path.join(dirfile,arqname)

while True:
    try:
        print(f'Diretorio atual {dirfile}')
        print(f'Diretorio arq {arqdir}')

        with open(arqdir, 'rb') as file:
            header = file.read(10)
            d = file.read()
        print(d[0:6])

        break

    except ValueError:
        print("teste")