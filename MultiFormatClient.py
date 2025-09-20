from socket import *

def behaviourNonJSON(connectionSocketLocal):
        request = input("Enter your command: ")
        connectionSocketLocal.send(request.encode())
        message = connectionSocketLocal.recv(1024).decode()
        response = input(message + ': ')
        connectionSocketLocal.send(response.encode())
        result = connectionSocketLocal.recv(1024).decode()
        print('Result from server: ' + result)

def behaviourJSON(connectionSocketLocal):
        #This message will be moved once I create a JSON server
        print("The following commands are accepted: random, add, subtract" \
        "all must be immediately succeeded by the required numbers seperated by spaces")
        request = input("Enter your command: ")
        connectionSocketLocal.send(request.encode())
        result = connectionSocketLocal.recv(1024).decode()
        print('Result from server: ' + result)

serverAdress = '127.0.0.1'
serverPort = 12345
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverAdress, serverPort))

ICanStoreAFunctionHere = behaviourNonJSON #Det kan godt være at det er en no-brainer for jer garvede programmører, men jeg synes det er lidt sejt... hvis det virker...

serverType = clientSocket.recv(1024).decode()

if serverType == 'ServerTypeNonJSON':
    ICanStoreAFunctionHere = behaviourNonJSON
elif serverType == 'ServerTypeJSON':
    ICanStoreAFunctionHere = behaviourJSON

print(clientSocket.recv(1024).decode()) #Her fortæller jeg hvad serveren kan

while True:
    ICanStoreAFunctionHere(clientSocket)



