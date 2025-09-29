from socket import *
from ServerServiceFunctions import *
from threading import Thread
import json as Jason_Bourne

serverPort = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(2)



def serviceClient(connectionSocketLocal):
    while True:
        message = connectionSocketLocal.recv(1024).decode()
        messageDict = Jason_Bourne.loads(message)

        if messageDict["command"].lower() == "random":
            response = randomInRange(int(messageDict["num1"]), int(messageDict["num2"]))
        elif messageDict["command"].lower() == 'add':
            response = Add(int(messageDict["num1"]), int(messageDict["num2"]))
        elif messageDict["command"].lower() == 'subtract':
            response = Subtract(int(messageDict["num1"]), int(messageDict["num2"]))
        
        responseDict = {"response": response}
        connectionSocketLocal.send(Jason_Bourne.dumps(responseDict).encode())

print('The server is listening on port', serverPort)

while True:
    clientSocket, addr = serverSocket.accept()
    print('Client, ', addr, 'connected')
    
    clientSocket.send('ServerTypeJSON'.encode())
    clientSocket.send("The following commands are accepted: random, add, subtract" \
        "\nAll must be immediately succeeded by the required numbers seperated by spaces".encode())
    
    Thread(target=serviceClient, args=(clientSocket,)).start()