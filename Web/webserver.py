from socket import *
from os import path
from time import gmtime, strftime

# Listen for incoming connections on port 10587
serverIP = '127.0.0.1'
serverPort = 10589
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

while True:
  # Block until connection detected. Create client socket and recieve data.
  connectionSocket, clientAddr = serverSocket.accept()
  message = connectionSocket.recv(2048).decode()
  
  # Parse method and requested file from header
  parseHDR = message.split(' ')
  if (len(parseHDR) < 2):
    continue
  method = parseHDR[0]
  filePath = parseHDR[1].strip('/')

  # if file exists, construct appropriate header + file.
  try:
    file = open(filePath)
    data = file.read()
    file.close()

    # Construct HTML Header
    hdr = "HTTP/1.1 200 OK\n"
    hdr += "Connection: close\n"
    hdr += "Date: " + strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()) + '\n'
    hdr += "Server: Lab2/1.0\n"
    hdr += "Last Modified: " + strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime(path.getmtime(filePath))) + '\n'
    hdr += "Content-Length: " + str(len(data)) + '\n'
    hdr += "Content-Type: text/html; charset=UTF-8\n\n"
    
    # Respond with header and data  
    if (method == 'GET'):
        connectionSocket.send((hdr + data).encode('utf-8'))
    
    # Just respond with header (no data).
    if (method == 'HEAD'):
        connectionSocket.send(hdr.encode('utf-8'))
    
  # else, throw 404 error.
  except Exception as e:
    hdr = "HTTP/1.1 404 Not Found\n"
    hdr += "Connection: close\n"
    hdr += "Date: " + strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()) + '\n'
    hdr += "Server: Lab2/1.0\n\n"
    connectionSocket.send(hdr.encode('utf-8'))

  # Non-persistent connection.
  connectionSocket.close()