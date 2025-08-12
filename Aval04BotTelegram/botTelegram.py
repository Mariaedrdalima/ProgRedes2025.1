################################################ BIBLIOTECAS UTILIZADAS ################################################
import socket, ssl, json, time, subprocess
import subprocess #importa a biblioteca subprocess para executar comandos de rede no terminal

#Nome do bot: madunetbot
TOKEN = "7664947436:AAF0k-DAtlFJ9eAz38GbkabGqaLej4RaTpw" #token do bot

HOST  = "api.telegram.org"
PORT  = 443

################################################ FUNÇÕES DO SERVIDOR - Disponibilizadas pelo professor ##############################################################
def conn_to():
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.connect((HOST, PORT))
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose)
    return context.wrap_socket(sock_tcp, server_hostname=HOST)

def send_get (sock_tcp, cmd):
    resource = "/bot"+TOKEN+"/"+cmd
    sock_tcp.send (("GET "+resource+" HTTP/1.1\r\n"+
                    "Host: "+HOST+"\r\n"+
                    "\r\n").encode("utf-8"))
        
def get_response(sock_tcp):
    answer = sock_tcp.recv(4096)
    header_body = answer.split(b"\r\n\r\n")
    headers, body = header_body[0].decode().split("\r\n"), header_body[1]

    status_line = headers[0]
    if status_line.split()[1] == "200":
        for header in headers[1:]:
            field_value = header.split(":")
            if field_value[0] == "Content-Length":
                to_read = int (field_value[1])
                break
    
        to_read -= len(body)
        while to_read > 0:
            segment = sock_tcp.recv(4096)
            body += segment
            to_read -= len(segment)
    
        return (status_line, headers[1:], json.loads(body.decode()))    
    return (None, None, None)

def get_updates(sock_tcp, offset = 0):
    send_get(sock_tcp, f"getUpdates?offset={offset}")
    status_line, headers, body = get_response(sock_tcp)    
    return body["result"]

def show_update(update):
    print (update["message"]["chat"]["first_name"], "->", update["message"]["text"])




################################################ FUNÇÕES IMPLEMENTADAS ##############################################################

#Só editei a função do professor para: receber a "resposta" da função solicitada pelo cliente -> formatar e devolver pro cliente no telegram. Sem mais input.
# def answer_update(update,resposta):
#     sock_tcp = conn_to()

#     chat_id  = update["message"]["chat"]["id"]

#     answer = resposta #input ("Sua resposta: ") - editei essa linha

#     response = json.dumps({
#         "chat_id":chat_id,
#         "text":answer
#         }, ensure_ascii=False)

#     print(response)

#     resource = "/bot"+TOKEN+"/sendMessage"

#     if len(response) > 4096:
#         MAX_LEN = 4000
#         for i in range(0, len(answer), MAX_LEN):
            
#             part = answer[i:i+MAX_LEN]

#             response = json.dumps({"chat_id": chat_id, "text": part}, ensure_ascii=False)
#             # envia cada parte separadamente
    
#     else: sock_tcp.send (("POST "+resource+" HTTP/1.1\r\n"+
#                     "Host: "+HOST+"\r\n"+
#                     "Content-Length: "+str(len(response))+"\r\n"
#                     "Content-Type: application/json\r\n"
#                     "\r\n").encode("utf-8"))
    
#     sock_tcp.send (response.encode("utf-8")) 
#     get_response(sock_tcp)
#     sock_tcp.close()
#     return update["update_id"]

def answer_update(update, resposta):
    sock_tcp = conn_to()
    chat_id = update["message"]["chat"]["id"]
    resource = "/bot"+TOKEN+"/sendMessage"

    if len(resposta) > 4096:
        MAX_LEN = 4000
        for i in range(0, len(resposta), MAX_LEN):
            part = resposta[i:i+MAX_LEN]
            response = json.dumps({
                "chat_id": chat_id,
                "text": part
            }, ensure_ascii=True)
            
            sock_tcp.send(("POST "+resource+" HTTP/1.1\r\n"+
                          "Host: "+HOST+"\r\n"+
                          "Content-Length: "+str(len(response))+"\r\n"
                          "Content-Type: application/json\r\n"
                          "\r\n").encode("utf-8"))
            sock_tcp.send(response.encode("utf-8"))
            get_response(sock_tcp)
    else:
        response = json.dumps({
            "chat_id": chat_id,
            "text": resposta
        }, ensure_ascii=True)
        
        sock_tcp.send(("POST "+resource+" HTTP/1.1\r\n"+
                      "Host: "+HOST+"\r\n"+
                      "Content-Length: "+str(len(response))+"\r\n"
                      "Content-Type: application/json\r\n"
                      "\r\n").encode("utf-8"))
        sock_tcp.send(response.encode("utf-8"))
        get_response(sock_tcp)
    
    sock_tcp.close()
    return update["update_id"]


#separei a execução do comando em uma função isolada pra tirar a repetição
def exec_comando(comando):
    resultado = subprocess.run(comando, capture_output=True, text=True, shell=True, encoding='cp850')
    return resultado.stdout

def exec_ping():
    #o primeiro resultado deve trazer o IP e o Gateway do servidor
    resultado1 = exec_comando('ipconfig | findstr \"IPv4 Gateway\"')
    gateway = resultado1.splitlines()[1].split(":")[1].strip()
    ip_server = resultado1.splitlines()[0].split(":")[1].strip()

    #o segundo resultado vai usar o gateway para fazer o ping
    resultado = exec_comando(f"ping {gateway} -n 4")
    mensagem = resultado.splitlines()[11].split("=")[3]

    resposta = f"O ping entre {ip_server} e {gateway} tem uma média de resultado completo: {mensagem}"

    return resposta

def exec_route_print():
    resultado = exec_comando("route print")
    linhas = resultado.splitlines()
    
    resposta = "Tabela de Roteamento:\n"

    for linha in linhas[1:]:
        if linha.strip():  #Ignora linhas vazias
            resposta += linha + "\n"
    
    resposta = resposta.strip()  #Remove espaços em branco no início e no final

    return resposta


# def exec_nslookup()
# def download_image()
# def exec_scan_ports():

# def answer_update(update):
#     sock_tcp = conn_to()

#     chat_id  = update["message"]["chat"]["id"]

#     answer = input ("Sua resposta: ")

#     response = '{"chat_id":'+str(chat_id)+', "text":"'+answer+'"}'

#     resource = "/bot"+TOKEN+"/sendMessage"

#     sock_tcp.send (("POST "+resource+" HTTP/1.1\r\n"+
#                     "Host: "+HOST+"\r\n"+
#                     "Content-Length: "+str(len(response))+"\r\n"
#                     "Content-Type: application/json\r\n"
#                     "\r\n").encode("utf-8"))
    
#     sock_tcp.send (response.encode("utf-8")) 
#     get_response(sock_tcp)
#     sock_tcp.close()
#     return update["update_id"]




################################################ FUNÇÃO PRINCIPAL ##############################################################
#A função main() inicia a conexão com o servidor do Telegram, aceita atualizações e responde às mensagens recebidas.
def main():
    sock_tcp = conn_to()
    print ("Aceitando updates ....")

    last_update = 0

    while True:
        updates = get_updates(sock_tcp, last_update+1)     
        

        for update in updates:
            solicitacao = update["message"]["text"]

            if solicitacao == "/ping":
                resposta = exec_ping()
                last_update = answer_update(update, resposta)
                show_update(update)

            elif solicitacao == "/route_print":
                resposta = exec_route_print()
                print(resposta)
                last_update = answer_update(update, resposta)
                show_update(update)

            # elif solicitacao == "/nslookup":
            #     exec_ping()

            # elif solicitacao == "/Baixar_imagem".upper():
            #     exec_ping()

            # elif solicitacao.startswit("/escanear portas"):
            #     scan_ports()

            # else:
            #     envio_resposta()

        # for update in updates:
        #     #show_update(update)
        #     last_update = answer_update(update)
        print ("-------------")

        time.sleep(2)
        
    sock_tcp.close()
    
main()