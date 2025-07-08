import socket

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
    
        python getByContenyLen viacep.com.br "/ws/59064250/json/ dadosCEP.txt
            - Acessa viacep.com.br/ws/59064250/json/ e salva os 
              dados no arquivo dadosCEP.txt
        python getByContenyLen httpbin.org /image/png  img.png
            - Acessa httpbin.org /image/png e salva os dados no 
              arquivo img.png
        python getByContenyLen httpbin.org /image/jpg  img.jpeg
            - Acessa httpbin.org /image/jpg e salva os dados no 
              arquivo img.jpeg
'''

PORT= 80

#HOST= "viacep.com.br"
#CEP = "59064250"
#resource = "/ws/"+CEP+"/json/"
HOST="httpbin.org"
resource = "/image/png"

sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockTCP.connect((HOST, PORT))

sockTCP.send (("GET "+resource+" HTTP/1.1\r\n"+
               "Host:"+HOST+"\r\n"+
               "\r\n").encode("utf-8"))
answer = sockTCP.recv(4096)
headerData = answer.split(b"\r\n\r\n")
headers, data = headerData[0].decode().split("\r\n"), headerData[1]

statusLine = headers[0]
if statusLine.split()[1] == "200":
    for header in headers[1:]:
        fieldValue = header.split(":")
        if fieldValue[0] == "Content-Length":
            toRead = int (fieldValue[1])
            break
    
    print (f"Content-Lenght = {toRead}")
    toRead -= len(data)
    while toRead > 0:
        segment = sockTCP.recv(4096)
        data += segment
        toRead -= len(segment)

    fdOut = open ("out.img", "wb")
    fdOut.write(data)
    fdOut.close()

sockTCP.close()