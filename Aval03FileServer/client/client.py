#!/usr/bin/env python3

##########################################>>> IMPORTANDO BIBLIOTECAS E ARQUIVOS ADICIONAIs <<<##########################################
import socket, threading, os, hashlib, glob, sys

#######################################################>>> SESSÃO DE REDE/SOCKET <<<#######################################################
PORT = 20000
SERVER = 'localhost'

diretorio = os.path.dirname(os.path.abspath(__file__))
PASTA_CLIENTE = os.path.join(diretorio,'downloads')


########################################>>> DEFININDO FUNÇÕES DO CLIENTE/COMUNICAÇÃO COM O SERVER <<<########################################
#função para exibir o menu com um input para o cliente selecionar o número da opção
def exibe_menu():
    print("""
        Escolha uma opção:
        1 - Listar arquivos do servidor
        2 - Download de 1 arquivo      
        3 - Continuar Download interrompido
        4 - Download de vários arquivos (com máscara)
        5 - Obter hash MD5 de arquivo
        6 - Sair
          
        Digite o número da opção desejada: """, end="")
    
    try:
        escolha = int(input())
        return escolha 
    
    except ValueError:
        print("\nEntrada inválida! Digite um número.")
        return 0

def enviar_comando(comando):
    try:
        sockServer.send(comando.encode("utf-8")) #envia o comando para o servidor
        resposta = sockServer.recv(4096).decode("utf-8") #recebe a resposta do servidor
        return resposta
    
    except Exception as e:
        print(f"\nErro na comunicação: {e}")
        return "ERRO"



#função para listar arquivos do servidor
def listar_arquivos():
    resposta = enviar_comando("LIST")

    if resposta.startswith("SUCESS"):

        arquivos = resposta.split("&")[1].split("\n")
        print("\n=== Arquivos no servidor ===")
        
        for arq in arquivos:
            if arq:  # Ignorar linhas vazias
                nome, tamanho = arq.split(";") #separa o nome do arquivo e o tamanho
                print(f"{nome} - {tamanho} bytes") #exibe o nome e o tamanho do arquivo

        print("============================")
    else:
        print("\nErro ao listar arquivos:", resposta)



#função para download de arquivo
def download_arquivo():
    nome_arquivo = input("\nDigite o nome do arquivo para download: ").strip()
    resposta = enviar_comando(f"DOWN&{nome_arquivo}")
    
    if resposta.startswith("SUCESS"):
        tamanho = int(resposta.split("&")[1])
        caminho_local = os.path.join(PASTA_CLIENTE, nome_arquivo)
        
        # Verificar se arquivo já existe
        if os.path.exists(caminho_local): #verifica se o arquivo já existe na pasta de downloads
            sobrescrever = input(f"Arquivo {nome_arquivo} já existe. Sobrescrever? (S/N): ").upper()
            if sobrescrever != 'S':
                print("Download cancelado.")
                return
        
        # Receber o arquivo
        with open(caminho_local, 'wb') as f: #abre o arquivo no modo escrita binária
            recebido = 0
            while recebido < tamanho: #enquanto o total recebido for menor que o tamanho do arquivo
                dados = sockServer.recv(4096)
                if not dados: 
                    break
                f.write(dados)
                recebido += len(dados) #atualiza o total recebido
        
        print(f"\nDownload concluído: {nome_arquivo} ({recebido} bytes)")
    else:
       
        print("\nErro no download:", resposta.split("&")[1])




#função para continuar download interrompido
def continuar_download():
    nome_arquivo = input("\nDigite o nome do arquivo para continuar download: ").strip()
    caminho_local = os.path.join(PASTA_CLIENTE, nome_arquivo)
    
    if not os.path.exists(caminho_local):
        print("Arquivo não encontrado localmente. Faça um download normal primeiro.")
        return
    
    tamanho_atual = os.path.getsize(caminho_local)
    
    # Calcular hash da parte existente
    md5 = hashlib.md5()
    with open(caminho_local, 'rb') as f:
        md5.update(f.read())
    hash_atual = md5.hexdigest()
    
    resposta = enviar_comando(f"CONT&{nome_arquivo}&{tamanho_atual}&{hash_atual}")
    
    if resposta.startswith("SUCESS"):
        tamanho_total = int(resposta.split("&")[1])
        with open(caminho_local, 'ab') as f:
            recebido = tamanho_atual
            while recebido < tamanho_total:
                dados = sockServer.recv(4096)
                if not dados:
                    break
                f.write(dados)
                recebido += len(dados)
        
        print(f"\nDownload continuado: {nome_arquivo} ({recebido} bytes no total)")
    else:
        print("\nErro ao continuar download:", resposta.split("&")[1])



#função para download de múltiplos arquivos a partir da extensão (máscara)
def download_multiplo():
    mascara = input("\nDigite a máscara para download (ex: *.txt): ").strip()
    resposta = enviar_comando(f"MULTI&{mascara}")
    
    if resposta.startswith("SUCESS"): 
        arquivos = resposta.split("&")[1].split("\n") #pega a lista de arquivos retornada pelo servidor

        for arq_info in arquivos: #para cada arquivo na lista ele vai ver se já existe, perguntar se quer baixar novamente, baixar e salvar, dizer que está pronto para o próximo

            if not arq_info: #Em alguns testes, a lista tinha espaços vazios, então ignora esses casos (não cosnegui descobrir o motivo ainda)
                continue
                
            nome_arquivo, tamanho = arq_info.split(";") #separa o nome do arquivo e o tamanho
            tamanho = int(tamanho)
            caminho_local = os.path.join(PASTA_CLIENTE, nome_arquivo)
            
            # Verificar se arquivo já existe
            if os.path.exists(caminho_local):
                sobrescrever = input(f"Arquivo {nome_arquivo} já existe. Sobrescrever? (S/N): ").upper()
                
                if sobrescrever != 'S':
                    print(f"Pulando {nome_arquivo}...")
                    continue
            
            # Confirmar download
            confirmar = input(f"Baixar {nome_arquivo} ({tamanho} bytes)? (S/N): ").upper()
            if confirmar != 'S':
                continue
            
            # Enviar confirmação para o servidor
            sockServer.send(f"DOWNLOADMULTI&{nome_arquivo}".encode("utf-8"))
            
            # Receber o arquivo
            with open(caminho_local, 'wb') as f:
                recebido = 0
                while recebido < tamanho:
                    dados = sockServer.recv(4096)
                    if not dados:
                        print(f"\nErro ao receber {nome_arquivo}. Download interrompido.")
                        break
                    f.write(dados)
                    recebido += len(dados)
            
            print(f"Download concluído: {nome_arquivo}")
            
            # Esperar confirmação do servidor para próximo arquivo
            sockServer.send("PRONTO".encode("utf-8"))
    else:
        print("\nErro no download múltiplo:", resposta.split("&")[1])




def obter_hash():
    nome_arquivo = input("\nDigite o nome do arquivo: ").strip()
    posicao = input("Digite a posição final para cálculo do hash (deixe vazio para arquivo inteiro): ").strip()
    
    if not posicao:
        posicao = "0"
    elif not posicao.isdigit():
        print("Posição inválida!")
        return
    
    resposta = enviar_comando(f"HASH&{nome_arquivo}&{posicao}")
    
    if resposta.startswith("SUCESS"):
        hash_value = resposta.split("&")[1]
        print(f"\nHash MD5 do arquivo {nome_arquivo} (até posição {posicao}): {hash_value}")
    else:
        print("\nErro ao obter hash:", resposta.split("&")[1])

while True:
    try:
        sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockServer.connect((SERVER, PORT))
        print("\nConexão com o servidor estabelecida.")

        #A conexão fica ativada até o cliente escolher a opção 6 de 'sair'
        while True:
            escolha = exibe_menu()

            if escolha == 1:
                listar_arquivos()
            elif escolha == 2:
                download_arquivo()
            elif escolha == 3:
                continuar_download()
            elif escolha == 4:
                download_multiplo()
            elif escolha == 5:
                obter_hash()
            elif escolha == 6:
                enviar_comando("EXIT")
                print("\nSaindo...")
                sockServer.close()
                sys.exit(0)
                break
            else:
                print("\nOpção inválida!")

    #Tratamento de erros de conexão
    except ConnectionRefusedError:
        print("\nNão foi possível conectar ao servidor. Verifique se o servidor está rodando.")
        break
    except KeyboardInterrupt:
        print("\nSaindo...")
        sockServer.close()
        break

    except Exception as e:
        print(f"\nErro inesperado: {e}")
        sockServer.close()
        break