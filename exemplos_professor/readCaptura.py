import datetime, struct

fd = open ("captura.pcap", "rb")

header = fd.read(24)

print (header)
if header[0:4] in [ b'\xD4\xC3\xB2\xA1', b'\xD4\x3C\xB2\xA1']:
    hPacket = fd.read(16)
    
    while hPacket != b'':
        (time, msec, capLen, origLen) = struct.unpack("<IIII", hPacket)
        print (datetime.datetime.fromtimestamp(time), msec, end=" -> ")
        packet = fd.read(capLen)
        print ("MAC Src: ", packet[0:6], "MAC Dst: ", packet[6:12], end=" -> ")
        headerIP = packet[14:34]
        print ("IP Src: ", [x for x in headerIP[12:16]], "IP Dst: ", [x for x in headerIP[16:20]])
        hPacket = fd.read(16)

    fd.close()