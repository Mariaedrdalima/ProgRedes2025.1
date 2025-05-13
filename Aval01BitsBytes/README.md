Adicionei shebang #!/usr/bin/env python3 nas questões. 01 e 02 permite passar argumento via linha de comando
*******************************************************************************************************************************************************
Na questão 01 seguirá o seguinte formato:
/exemplo/user#./q1 <ip> <bits em zero>
Exemplo:
user#./q1 8.8.8.8 10

![image](https://github.com/user-attachments/assets/ec39227f-6240-4c17-82d1-abb8c62ddc85)


*******************************************************************************************************************************************************
Na questão 02 o usuario poderá chamar o script no terminal passando os argumentos, ou simplesmente executá-lo para visualizar a tabela:
/exemplo/user#./q2 <bits em zero> <data>

Exemplo:
/exemplo/user#./q2 2 Teste

Caso executado da seguinte maneira:
/exemplo/user#./q2

Retorna:
![image](https://github.com/user-attachments/assets/5443ff2a-ab24-488e-8ff0-4a8557469675)

*******************************************************************************************************************************************************
3) Faça um programa que leia os primeiros 6 bytes da imagem JPEG em anexo. Nas
posições 4 e 5 há um valor que especifica o tamanho dos metadados presentes nessa
imagem. Obtenha esse número (chame-o app1DataSize). Feche o arquivo.


>>>>Primeiros 6 bytes -> FF D8 FF E1 50 EA
>>>>app1DataSize em 4 e 5 -> 50 EA -> 20714

-----------------------------------------------------------------------------------
a) Abra o arquivo novamente, leia 4 bytes e os ignore. Agora leia o número de
bytes em app1DataSize para app1Data. Na posição 16 de app1Data há 2 bytes que indicam quantos metadados essa imagem tem. Descubra-o e
informe.

>>>>FF D8 FF E1 -> Bytes ignorados

>>>>50 EA 45 78 69 66 00 00 4D 4D 00 2A 00 00 00 08 00 0D

>>>>posições 16 e 17 -> 00 0D -> 13


-----------------------------------------------------------------------------------
b) A partir da posição 18 de app1Data há efetivamente os metadados. Cada
metadado tem o formato:


>>>>01 00 00 03 00 00 00 01 0F F0
>>>>01 01 00 03 00 00 00 01 0B F4

2 bytes - qual o metadado: 0100
2 bytes - o tipo do metadado: 0003
4 bytes - o número de repetições que esse metadados tem: 00000001
4 bytes - o valor do metadado: 0ff0
2 bytes - qual o metadado: 0101
2 bytes - o tipo do metadado: 0003
4 bytes - o número de repetições que esse metadados tem: 00000001
4 bytes - o valor do metadado: 0bf4
