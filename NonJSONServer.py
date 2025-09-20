from threading import Thread
from socket import *
from ServerServiceFunctions import *

serverport = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverport))
serverSocket.listen(2)

def serviceClient(connectionSocketLocal):
    while True:

        message = connectionSocketLocal.recv(1024).decode()

        # Nu er det nok ikke en super god praksis, men siden at opaven ikke efterspørger fejlhåndtering kan jeg lige så godt antage at det altid er random/add/subtract
        # Og at respons så derfor altid bør være "input numbers"
        inputRequest = 'input numbers'
        connectionSocketLocal.send(inputRequest.encode())
        response = ''

        if message.lower() == 'random':
            clientInputMsg = connectionSocketLocal.recv(1024).decode()
            numbers = clientInputMsg.split(' ')
            response = randomInRange(int(numbers[0]), int(numbers[1]))
        elif message.lower() == 'add':
            clientInputMsg = connectionSocketLocal.recv(1024).decode()
            numbers = clientInputMsg.split(' ')
            response = Add(int(numbers[0]), int(numbers[1]))
        elif message.lower() == 'subtract':
            clientInputMsg = connectionSocketLocal.recv(1024).decode()
            numbers = clientInputMsg.split(' ')
            response = Subtract(int(numbers[0]), int(numbers[1]))

        connectionSocketLocal.send(str(response).encode())


print('The server is listening on port', serverport)
while True:
    clientSocket, addr = serverSocket.accept()
    print('Client, ', addr, 'connected')
    
    clientSocket.send('ServerTypeNonJSON'.encode())
    clientSocket.send("The following commands are accepted: random, add, subtract" \
        "the server will prompt for the required numbers seperated by spaces".encode())
    
    Thread(target=serviceClient, args=(clientSocket,)).start()

    