import socket
import sys
import struct

#dictionary for hostname and IP address
dns = {}
#opening a file and real line by line
f = open('dns-master.txt', 'r')
file = f.readlines()

#will populate the dictionary with hostnames and IP adresses
for x in file:
    #if the line does not start with a comment
    if x[0] != '#' and x[0] != '\n':
        #find the spot where the hostname ends and the IP address starts
        index = x.find('A IN') + 5
        dns[x[: index]] = x[index:len(x)-1]

f.close()
#print(dns)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversocket.bind((sys.argv[1], int(sys.argv[2])))

while True:
    data, clientAdd = serversocket.recvfrom(1024)
    size = struct.calcsize('hhihh')
    mType, rCode, mIdentifier, qLength, aLength = struct.unpack('hhihh', data[:size])
    #must decode the question before it is readable
    query = data[size:].decode()

    print(mType, rCode, mIdentifier, qLength, aLength, query)

    #if it can find the hostname in the dns master list it will return the correct IP Address
    if query in dns:
        answer = query + dns[query]
        aLength = len(answer.encode('utf-8'))
    #otherwise the answer is null and the return code is 1 which is failure
    else:
        answer =""
        rCode = 1
    mCode = 2

    message = struct.pack('hhihh', mType, rCode, mIdentifier, qLength, aLength) + query.encode() + answer.encode()

    serversocket.sendto(message, clientAdd)