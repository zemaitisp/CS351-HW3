import sys
import socket
import struct
import random

host = sys.argv[1]
port = sys.argv[2]


messageType = 1
returnCode = 0
messageIdentifier = random.randrange(100)
questionLength = len(sys.argv[3].encode('utf-8'))
answerLength = 0
questionString = sys.argv[3] + " A IN "
packedQuestion = questionString.encode()

message = struct.pack('hhihh', messageType, returnCode, messageIdentifier, questionLength, answerLength) + packedQuestion


#Creates UPD client socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)

#printing information for the user to know what is being sent
print("Sending Request to ", host, port)
print("Message ID: ", messageIdentifier)
print("Question Length: ", questionLength, "bytes")
print("Answer Length: ", answerLength, " bytes")
print("Question: ", questionString, "\n")


count = 0
messageNotSent = True
while count < 3 and messageNotSent:
    try:
        clientsocket.sendto(message, (host, int(port)))
        #if it can connect no need to retry
        rMessage, serverAdd = clientsocket.recvfrom(1024)
        messageNotSent = False
    except:
        #retrying three times
        print("Request Timed Out")
        count = count + 1


if messageNotSent:
    print("Server could not be reached")
#iff the server could be reached
else:
    #size of all the numbers
    size = struct.calcsize('hhihh')

    #will unpack the message and save all the important details into variables to be accessed later
    mType, rCode, mIdentifier, qLength, aLength = struct.unpack('hhihh', rMessage[:size])

    #Will gather the question and answer
    returnAnswer = rMessage[size:].decode()
    qLen = len(questionString)
    question = returnAnswer[:qLen]
    answer = returnAnswer[qLen:]

    #will print regardless of failure or success
    print("Received Request to ", serverAdd[1], serverAdd[0])
    print("Return Code: ", rCode)
    print("Message ID: ", mIdentifier)
    print("Question Length: ", qLength)
    print("Answer Length: ", aLength)
    print("Question: ", question)

    #will see it there was an answer or if there was a error
    if len(answer) > qLen:
        print('Answer: ', answer)
