Questões da avaliação 'Aval01BitsBytes'

1) Faça um programa que recebe um string com um número IPv4 (ex:
“200.17.143.131”) e uma máscara em bits (ex: 18) e responda:
a) Qual o endereço da rede?
b) Qual o endereço de broadcast?
c) Qual o endereço do gateway (suponha que será usado o último número IP
válido o para gateway)?
d) Quantos hosts podem existir nessa subrede?
Não use strings ou bibliotecas prontas do Python. Apenas operações com bits.


2) A dificuldade em minerar bitcoins ocorre porque é necessário executar o que se
chama de prova de trabalho. Em outras palavras, vários mineradores competem para
realizar uma tarefa; aquele que primeiro realizá-la é o minerador campeão da
atividade e recebe uma boa recompensa.
Na prática, a atividade a realizar é: receber um conjunto de transações (um conjunto
de bytes) e calcular o hash SHA-256 deles, mas tem um detalhe: um número inteiro
de quatro bytes (big-endian) deve ser concatenado no início dos bytes recebidos
(chame este número de nonce). O resultado do hash (256 bits de resultado) deve ter
uma quantidade inicial de bits zero. O minerador que descobrir o nonce certo é o
vencedor.

Portanto, minerar é: a) escolher um nonce (começando de zero, por exemplo); b)
juntar com os bytes da entrada; c) calcular o hash desse conjunto; d) verificar se o
hash resultante inicia com uma certa quantidade de bits em zero; e) se o hash
calculado não atende ao requisito, repetir o processo.
Faça uma função em Python de nome findNonce que recebe dois argumentos:
dataToHash – um conjunto de bytes
bitsToBeZero – o número de bits iniciais que deve ser zero no hash
e devolve:
o nonce que satisfaz às condições
o hash encontrado
tempo (em segundos) que demorou para encontrar o nonce
Ao final, faça um programa que usa a função e exibe a seguinte tabela:
Texto a validar (converta para bytes antes de chamar) - Bits em zero - Nonce Tempo (em s)
“Esse um texto elementar” - 8 
“Esse um texto elementar” - 10
“Esse um texto elementar” - 15
“Textinho” - 8
“Textinho” - 18
“Textinho” - 22
“Meu texto médio” - 18
“Meu texto médio” - 19
“Meu texto médio” - 20