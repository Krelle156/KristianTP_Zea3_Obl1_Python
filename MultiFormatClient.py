from threading import Thread
from socket import *
import json as JavaScriptObjectNotation_Bourne

connection_alive = True

def behaviourNonJSON(connectionSocketLocal):
        global connection_alive
        if not connection_alive:
            return
        try:
             command = input("Enter your command: ")
             connectionSocketLocal.send(command.encode())

             data_expected_prompt = connectionSocketLocal.recv(1024)
             if not data_expected_prompt:
                 print("Server closed the connection")
                 connection_alive = False
                 return
             prompt = data_expected_prompt.decode(errors="replace")

             if prompt == 'error':
                 print("Server reported an error with the command.")
                 return
             
             input_data = input(prompt + ': ')
             connectionSocketLocal.send(input_data.encode())

             data_expected_result = connectionSocketLocal.recv(1024)
             if not data_expected_result:
                 print("Server closed the connection")
                 connection_alive = False
                 return
             print(f'Result from server: {data_expected_result.decode(errors="replace")}')
        except TimeoutError: #Hvis serveren ikke svarer inden for timeout perioden, lukkes forbindelsen
            print("Timeout error occurred while waiting for server response.")
            connection_alive = False
        except Exception as e: #Jeg har besluttet bare at fange andre fejl under en undtagelse, når nu fejlhåndtering ikke er en del af opgaven
            print(f"An error occurred: {e}")
            connection_alive = False
        


def behaviourJSON(connectionSocketLocal):

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
        else:
            print("Unknown command. Accepted commands are: random, add, subtract")
            return

              
        
        connectionSocketLocal.send(JavaScriptObjectNotation_Bourne.dumps(requestDict).encode())

def listenerJSON(connectionSocketLocal):
    global connection_alive
    while connection_alive:
        try:
            data = connectionSocketLocal.recv(1024)
            if not data:
                print("Server closed the connection")
                connection_alive = False
                break
            result = data.decode(errors="replace")
            resultDict = JavaScriptObjectNotation_Bourne.loads(result)
            print(f'Result from server: {resultDict["response"]}')
        except TimeoutError:
            print("Timeout error occurred while waiting for server response.")
            connection_alive = False
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            connection_alive = False
            break

serverAdress = '127.0.0.1'
serverPort = 12345
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverAdress, serverPort))
clientSocket.settimeout(180)

ICanStoreAFunctionHere = behaviourNonJSON #Det kan godt være at det er en no-brainer for jer garvede programmører, men jeg synes det er lidt sejt at man kan gemme en funktion... og det virker endda.

serverType = clientSocket.recv(1024).decode(errors="replace")

print(clientSocket.recv(1024).decode(errors="replace")) #Her modtager jeg en besked der fortæller hvad serveren siger den kan

if serverType == 'ServerTypeNonJSON':
    ICanStoreAFunctionHere = behaviourNonJSON
elif serverType == 'ServerTypeJSON':
    Thread(target=listenerJSON, args=(clientSocket,), daemon=True).start()
    ICanStoreAFunctionHere = behaviourJSON


while connection_alive:
    ICanStoreAFunctionHere(clientSocket)
clientSocket.close()



