#!/usr/bin/env python3

import sys, struct, hashlib, time

# # Os argumentos passados na execução do código
args = sys.argv

def findNonce(dataToHash: bytes, bitsToBeZero: int):
    inicio = time.time()
    nonce = 0

    while True:
        nonce_bytes = nonce.to_bytes(4,byteorder='big')
        data = nonce_bytes+dataToHash
        hash_bytes= hashlib.sha256(data).digest()
        hash_int = int.from_bytes(hash_bytes, byteorder='big')

        if (hash_int >> (256-bitsToBeZero)) == 0:
            tempo = time.time() - inicio
            break

        nonce +=1

    return nonce, hash_bytes, tempo



#--------------------------------------Acessar argumentos passados------------------------------------------------
# Garamtir que pelo menos dois argumentos foram passados
if len(args) >= 3:  
    bitsToBeZero = int(args[1]) #garantindo que será um valor inteiro de bits em zero
    dataToHash = args[2].encode() #convertendo pra cadeia de bytes


    #Chamando a função FindNonce
    nonce, hash_encontrado, tempo = findNonce(dataToHash, bitsToBeZero)

    print(f"""
        nonce {nonce}
        tempo {tempo:.6f} segundos
        hash {hash_encontrado}
    """)

else: 
    #--------------------------------------Gerando a Tabela------------------------------------------------
    #Casos da tabela
    tabela_casos = [
        ("Esse um texto elementar", 8),
        ("Esse um texto elementar", 10),
        ("Esse um texto elementar", 15),
        ("Textinho", 8),
        ("Textinho", 18),
        ("Textinho", 22),
        ("Meu texto médio", 18),
        ("Meu texto médio", 19),
        ("Meu texto médio", 20)
    ]

    # Cabeçalho da tabela
    print("+" + "-"*168 + "+")
    print(f"  {'Texto':<25}   {'Bits':>5}   {'Nonce':>8}   {'Tempo (s)':>2}   {'Hash':>10}")
    print("+" + "-"*168 + "+")
        
    for texto, bitsZero in tabela_casos:
        data = texto.encode()
        nonce, hash_bytes, tempo = findNonce(data, bitsZero)
            
        #Formatando a linha da tabela
        print(f"| {texto[:25]:<25} | {bitsZero:>5} | {nonce:>8} | {tempo:>10.6f} | {hash_bytes}")

    # Rodapé da tabela
    print("+" + "-"*168 + "+")
