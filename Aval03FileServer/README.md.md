#Cliente-Servidor com Socket TCP e Multithreading

Este projeto implementa uma arquitetura **cliente-servidor** utilizando **sockets TCP** e **multithreading** em Python, permitindo múltiplas conexões simultâneas para transferência de arquivos.

##Tecnologias Utilizadas

- Python 3.11+
- Socket (TCP)
- Multithreading
- Compactação de arquivos (.zip)

##Funcionalidades

###Servidor

- Aceita múltiplas conexões de clientes simultaneamente.
- Cada cliente é tratado por uma thread separada.
- Suporta comandos:
  - `LISTAR` → lista os arquivos disponíveis no servidor.
  - `DOWNLOAD <nome_arquivo>` → envia um único arquivo.
  - `DOWNLOADMULTI <arquivo1> <arquivo2> ...` → compacta os arquivos e envia um .zip.
  - `SAIR` → encerra a conexão do cliente.

###Cliente

- Conecta-se ao servidor e envia comandos.
- Recebe arquivos e salva localmente.
- Pode solicitar múltiplos arquivos simultaneamente com `DOWNLOADMULTI`.

##Como Executar

###21. Iniciar o Servidor

```bash
python servidor.py
```

###2. Iniciar o Cliente

```bash
python cliente.py
```

##Estrutura Multithread

Cada cliente conectado é gerenciado por uma nova thread:

```python
thread = threading.Thread(target=multi_download, args=(conn, client_id))
thread.start()
```

Isso permite múltiplas conexões sem bloqueio entre elas.

##Exemplo de Comando

```bash
DOWNLOADMULTI arquivo1.txt arquivo2.txt imagem.png
```

O servidor cria uma pasta temporária, move os arquivos, gera um `.zip` e envia pela mesma conexão socket.

---

##Autora

Projeto desenvolvido por **Eduarda Lima** para disciplina de Programação de Redes (2025.1).