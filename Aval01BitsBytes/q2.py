#!/usr/bin/env python3

import sys, struct, hashlib, time

# Os argumentos passados na execução do código
args = sys.argv

def findNonce(dataToHash: bytes, bitsToBeZero: int):
    inicio = time.time()
    nonce = 0

    while True:
        nonce = nonce.to_bytes(4,byteorder='big')
        data = nonce+dataToHash
        hash = hashlib.sha256(data).digest()
        break

    tempo = time.time() - inicio
    return nonce, hash, tempo






#--------------------------------------Acessar argumentos passados------------------------------------------------
# Garamtir que pelo menos dois argumentos foram passados
if len(args) >= 3:  
    bitsToBeZero = 32 - int(args[1])
    dataToHash = args[2].encode()


    #Chamando a função FindNonce
    nonce, hash_encontrado, tempo = findNonce(dataToHash, bitsToBeZero)

    print(f"""
        nonce {nonce}
        tempo {tempo:.6f} segundos
        hash {hash_encontrado}
    """)