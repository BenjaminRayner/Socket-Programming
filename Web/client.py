from socket import *

serverIP = "127.0.0.1"
serverPort = 10589
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

request = 'GET /HelloWorld.html HTTP/1.1\n'
clientSocket.send(request.encode())
recieve = clientSocket.recv(2048)

print(recieve.decode())
clientSocket.close()