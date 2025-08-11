################################################ BIBLIOTECAS UTILIZADAS ################################################
import socket, ssl, json, time, subprocess
import subprocess #importa a biblioteca subprocess para executar comandos de rede no terminal

#Nome do bot: madunetbot
TOKEN = "" #token do bot

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
    print(update)
    print (update["message"]["chat"]["first_name"], "->", update["message"]["text"])
    
def answer_update(update):
    sock_tcp = conn_to()

    chat_id  = update["message"]["chat"]["id"]

    answer = input ("Sua resposta: ")

    response = '{"chat_id":'+str(chat_id)+', "text":"'+answer+'"}'

    resource = "/bot"+TOKEN+"/sendMessage"

    sock_tcp.send (("POST "+resource+" HTTP/1.1\r\n"+
                    "Host: "+HOST+"\r\n"+
                    "Content-Length: "+str(len(response))+"\r\n"
                    "Content-Type: application/json\r\n"
                    "\r\n").encode("utf-8"))
    
    sock_tcp.send (response.encode("utf-8")) 
    get_response(sock_tcp)
    sock_tcp.close()
    return update["update_id"]

################################################ FUNÇÕES IMPLEMENTADAS ##############################################################

def exec_comando(comando):

def exec_ping():
    # if comando == "/ping":
    # # Comando completo como string, shell=True para interpretar pipe e findstr
    # comando = 'ipconfig | findstr "IPv4 Gateway"'

    # resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)

    # print(resultado.stdout.splitlines()[1])

    # gateway = resultado.stdout.splitlines()[1].split(":")[1].strip()
    # ip_server = resultado.stdout.splitlines()[0].split(":")[1].strip()

def exec_route_print():
def exec_nslookup()
def download_image()
def scan_ports_open():




################################################ FUNÇÃO PRINCIPAL ##############################################################
#A função main() inicia a conexão com o servidor do Telegram, aceita atualizações e responde às mensagens recebidas.
def main():
    sock_tcp = conn_to()
    print ("Aceitando updates ....")

    last_update = 0

    while True:
        updates = get_updates(sock_tcp, last_update+1)
        print()
        for update in updates:
            #show_update(update)
            get_comando(update(update["message"]["text"]))
            last_update = answer_update(update)
        print ("-------------")

        time.sleep(2)
        
    sock_tcp.close()
    
main()