import socket, sys

'''
Esse programa le os dados de um servidor HTTP que responde
Esse programa le os dados de um servidor HTTP que responde
o tamanho dos dados baseado em Content-Length ...

Atividade:
    Use sys.argv para fazer com que o programa possa 
    ser chamado passando o HOST e o RESOURCE na linha 
    de comando e salvando os dados no arquivo especificado 
    (arqDestino). 
    Exemplos:
    
        python getByContenyLen viacep.com.br /ws/59064250/json/ dadosCEP.txt
            - Acessa viacep.com.br/ws/59064250/json/ e salva os 
              dados no arquivo dadosCEP.txt
        python getByContenyLen httpbin.org /image/png  img.png
            - Acessa httpbin.org /image/png e salva os dados no 
              arquivo img.png
        python getByContenyLen httpbin.org /image/jpg  img.jpeg
            - Acessa httpbin.org /image/jpg e salva os dados no 
              arquivo img.jpeg
'''

PORT = 80
NL = b"\r\n"
MARKER2NL = NL*2

def conectHost(host, port):
    sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockTCP.connect((host, port))
    return sockTCP

def requestResource (sockTCP, host, resource):
    sockTCP.send (("GET "+resource+" HTTP/1.1\r\n"+
               "Host:"+host+"\r\n"+
               "\r\n").encode("utf-8"))
    answer = sockTCP.recv(4096)
    while MARKER2NL not in answer:
        answer += sockTCP.recv(4096) 
    return answer

def  getStatusAndHeaders(answer):
    endFirstLine = answer.find(NL)
    markerPos = answer.find(MARKER2NL)
    statusCode = answer[:endFirstLine].split()[1].decode()
    
    headersDict = {}
    headers = answer[endFirstLine+2:markerPos]
    for header in headers.split(NL):
        header = header.decode()
        pos2point = header.find(":")
        headersDict[header[:pos2point]] = header[pos2point+1:]
    return statusCode, headersDict, answer[markerPos+4:]

def requestByContentLen(sockTCP, toRead, data):
    toRead -= len(data)
    while toRead > 0:
        segment = sockTCP.recv(4096)
        data += segment
        toRead -= len(segment)
    return data
    
def requestByChunks(sockTCP, toRead, data):
    return data

if len(sys.argv) != 4:
    print (f"Uso: {sys.argv[0]} host resource fileToSave")
    sys.exit(2)

HOST = sys.argv[1]
resource = sys.argv[2]
fileName = sys.argv[3]

sockTCP = conectHost(HOST, PORT)
answer  = requestResource(sockTCP, HOST, resource)
input (answer)
statusCode, headers, data = getStatusAndHeaders(answer)
input (statusCode)
print (headers.items())
input()
print (data)
input()

if statusCode == "200":
    toRead = int(headers.get("Content-Length", 0))
    if toRead > 0:
        data  = requestByContentLen(sockTCP, toRead, data)
    elif " chunked" in headers.get("Transfer-Encoding", ""): 
        data  = requestByChunks(sockTCP, toRead, data)

    fdOut = open (fileName, "wb")
    fdOut.write(data)
    fdOut.close()

sockTCP.close()