from threading import Thread
from socket import *
import json as JavaScriptObjectNotation_Bourne

def behaviourNonJSON(connectionSocketLocal):
        Thread(target=listenerNonJSON, args=(connectionSocketLocal,)).start()
        request = input("Enter your command: ")
        connectionSocketLocal.send(request.encode())
        message = connectionSocketLocal.recv(1024).decode()
        response = input(message + ': ')
        connectionSocketLocal.send(response.encode())

def listenerNonJSON(connectionSocketLocal):
     result = connectionSocketLocal.recv(1024).decode()
     print('Result from server: ' + result)

def behaviourJSON(connectionSocketLocal):
        Thread(target=listenerJSON, args=(connectionSocketLocal,)).start()

        request = input("Enter your command: ")
        splitRequest = request.split(' ')
        requestDict = {}
        if len(splitRequest) != 3:
            print("Invalid command format. Use: command param1 param2")
            return
        if splitRequest[0].lower() == "random":
            requestDict = {
                "command": "random",
                "num1": splitRequest[1],
                "num2": splitRequest[2]
            }
        elif splitRequest[0].lower() == "add":
            requestDict = {
                "command": "add",
                "num1": splitRequest[1],
                "num2": splitRequest[2]
            }
        elif splitRequest[0].lower() == "subtract":
            requestDict = {
                "command": "subtract",
                "num1": splitRequest[1],
                "num2": splitRequest[2]
            }

              
        
        connectionSocketLocal.send(JavaScriptObjectNotation_Bourne.dumps(requestDict).encode())

def listenerJSON(connectionSocketLocal):
     result = connectionSocketLocal.recv(1024).decode()
     resultDict = JavaScriptObjectNotation_Bourne.loads(result)
     print(f'Result from server: {resultDict["response"]}')

serverAdress = '127.0.0.1'
serverPort = 12345
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverAdress, serverPort))

ICanStoreAFunctionHere = behaviourNonJSON #Det kan godt være at det er en no-brainer for jer garvede programmører, men jeg synes det er lidt sejt at man kan gemme en funktion... og det virker endda.

serverType = clientSocket.recv(1024).decode()

if serverType == 'ServerTypeNonJSON':
    ICanStoreAFunctionHere = behaviourNonJSON
elif serverType == 'ServerTypeJSON':
    ICanStoreAFunctionHere = behaviourJSON

print(clientSocket.recv(1024).decode()) #Her sender jeg en besked der fortæller hvad serveren kan

while True:
    ICanStoreAFunctionHere(clientSocket)



