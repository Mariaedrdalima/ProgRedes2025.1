#!/usr/bin/env python3

def conversor(x):
    resultado = [] #criando a lista que receberá o resultado da conversão

    while x > 0:
        r = x%6
        x = x//6
        resultado.insert(0, r) #com o insert eu consigo dizer a posição onde quero inserir o elemento, assim não preciso inverter a lista no final
    return ''.join(str(s) for s in resultado) #Aqui eu retorno somente a junção dos caracteres da lista

print("******************* BEM VINDO AO CONVERSOR *******************\n")

while True:
    try:
        base10 = int(input("Digite o número de base 10: ").replace(" ","")) #removendo todos os espaços que possam ter sido digitados pelo usuário e definindo como int
        print(f'O número {base10} convertido para base 6 é: {conversor(base10)}')
        break #encerrando

    #Tratando o erro de tipo caso o user digite caractere invalido    
    except ValueError:
        print(f'''
              ERRO: CARACTERE INVALIDO!
              Informe um número de base 10 \n''')
        