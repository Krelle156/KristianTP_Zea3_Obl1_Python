from threading import *
from socket import *
from ServerServiceFunctions import *

serverport = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverport))
serverSocket.listen(2)

def serviceClient(connectionSocketLocal):
    while True:
        message = connectionSocketLocal.recv(1024).decode()


    

while True:
    print('The server is listening on port', serverport)
    clientSocket, addr = serverSocket.accept()
    print('Client, ', addr, 'connected')
    