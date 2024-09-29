database = {
  'google.com'   : [[192,12,0,1,0,1,0,0,1,4,0,4,192,165,1,1], [192,12,0,1,0,1,0,0,1,4,0,4,192,165,1,10]],
  'youtube.com'  : [[192,12,0,1,0,1,0,0,0,160,0,4,192,165,1,2]],
  'uwaterloo.ca' : [[192,12,0,1,0,1,0,0,0,160,0,4,192,165,1,3]],
  'wikipedia.org': [[192,12,0,1,0,1,0,0,0,160,0,4,192,165,1,4]],
  'amazon.ca'    : [[192,12,0,1,0,1,0,0,0,160,0,4,192,165,1,5]]
}

from socket import *

# Listen for incoming connections on port 10587
serverIP = '127.0.0.1'
serverPort = 10587
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))
print("The server is ready to receive")

while True:
  # Block until connection detected. Recieve data and client addr.
  bytestream, clientAddr = serverSocket.recvfrom(2048)
  message0 = bytestream.hex()
  print("Request:\n"+' '.join(message0[i:i+2] for i in range(0, len(message0), 2)))
  
  # Parse domain name
  len1 = bytestream[12]
  len2 = bytestream[13+len1]
  domain = bytestream[13:13+len1].decode()
  domain += '.'
  domain += bytestream[14+len1:14+len1+len2].decode()

  # Append database entry to current bytestream
  response = bytearray(bytestream)
  response[2] = 0x84                  # Change QR to response
  response[7] = len(database[domain]) # Change ANCOUNT (num of records)
  for i in range(len(database[domain])):
    response.extend(bytes(database[domain][i]))
  message1 = response.hex()
  print("Response:\n"+' '.join(message1[i:i+2] for i in range(0, len(message1), 2)))

  # Send response to client
  serverSocket.sendto(response, clientAddr)
  