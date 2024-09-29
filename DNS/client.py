ANSWER_LENGTH = 16

from socket import *
from random import getrandbits

serverIP = '127.0.0.1'
serverPort = 10587
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Send msg
while True:
  domain = input("Enter Domain Name: ")
  if (domain == 'end'):
    clientSocket.close()
    print("Session Ended") 
    exit()
  
  # Split website into two ids
  id = domain.split('.')
  
  # Header
  dns_msg = [getrandbits(8),getrandbits(8),4,0,0,1,0,0,0,0,0,0]
  # Question
  dns_msg.append(len(id[0]))
  for i in range(len(id[0])):
    dns_msg.append(ord(id[0][i]))
  dns_msg.append(len(id[1]))
  for i in range(len(id[1])):
    dns_msg.append(ord(id[1][i]))
  dns_msg.extend([0,0,1,0,1])
  
  # Convert DNS message to byte stream
  dns_msg = bytearray(dns_msg)
  
  # Send DNS query
  clientSocket.sendto(dns_msg, (serverIP, serverPort))
  
  # Receive DNS response
  response, serverAddr = clientSocket.recvfrom(2048)

  # Parse DNS response
  count = len(dns_msg)
  for i in range(response[7]):
    TTL = str(int.from_bytes(response[count+6:count+10], 'big'))
    IP = str(response[count+12])+'.'+str(response[count+13])+'.'+str(response[count+14])+'.'+str(response[count+15])
    print(domain+': '+"type A, class IN, TTL "+TTL+", addr (4) "+IP)
    count += ANSWER_LENGTH