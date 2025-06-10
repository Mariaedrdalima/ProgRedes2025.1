import sys, struct, datetime

countProt = {}

if len(sys.argv) < 2:
    print (f"uso: {sys.argv[0]} arquivo.pcap")
    sys.exit(1)

fd = open (sys.argv[1], "rb")
fd.seek (24, 0)

hPacket = fd.read(16)
while len(hPacket) == 16:
    ts, ms, lenCap, lenPacket = struct.unpack ("<IIII", hPacket)
    # print (datetime.datetime.fromtimestamp(ts), ms)
    fd.seek(12, 1)
    proto = int.from_bytes(fd.read(2), 'big')
    countProt[proto] = countProt.get(proto, 0) + 1
    fd.seek(lenCap-14, 1)
    hPacket = fd.read(16)
fd.close()
print (countProt)
