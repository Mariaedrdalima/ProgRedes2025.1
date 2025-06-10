import hashlib, struct

bitsZero = 12
nonce = 0

while True:
	m = hashlib.sha256()
	m.update (struct.pack(">I", nonce))
	m.update (b'JTAG - Jane, Tiago, Amanda, Giovanna')
	hash = m.digest()
	fourBytes = struct.unpack(">I", hash[0:4])[0]
	if (fourBytes >> (32-bitsZero)) == 0:
		print (f"Nonce encontrado: {nonce} ({nonce:04x})",
			   "Hash[0:4]:", hash[0:4])
        break
	nonce += 1
	
	if (nonce % 10000) == 0:
		print ("Tentando nonce ", nonce)
