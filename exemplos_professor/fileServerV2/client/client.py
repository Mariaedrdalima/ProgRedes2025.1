import socket

SERVIDOR = "localhost"
PORTA    = 2121

def conectaAoServidor():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVIDOR, PORTA))
    
def mostraOpcoes():
    print ("1 - Lista arquivos no servidor")
    print ("2 - Donwload de um arquivo")
    print ("3 - Fim")
    return int (input("Escolha uma opção: "))

def adicionaTamanho(dados):
    tamanho = len(dados)
    return tamanho.to_bytes(4, byteorder='big')+dados

def listaArquivos():
    comando = b"DIR"
    sock.send(adicionaTamanho(comando))
    tamanhoListagem = int.from_bytes(sock.recv(4), byteorder='big')
    while tamanhoListagem > 0:
        resposta = sock.recv(tamanhoListagem)
        tamanhoListagem -= len(resposta)
        print (resposta.decode())
    return

def downloadArquivo():
    return

def main():
    conectaAoServidor()
    while True:
        opcao = mostraOpcoes()
        if opcao == 1:
            listaArquivos()
        elif opcao == 2:
            downloadArquivo()
        elif opcao == 3:
            sock.close()
            return
        else:
            print ("Opcao invalida!")
            
main()