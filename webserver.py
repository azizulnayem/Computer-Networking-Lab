#import socket module
from socket import *

#Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM)
host = '127.0.0.1'
port = 4445 # server port number
serverSocket.bind((host, port)) #bind socket to server address and server port

serverSocket.listen(1) #at a time listen to 1 connection 

while True:
  print('Ready to serve...')
  #Establish the connection from the client
  connectionSocket, addr = serverSocket.accept() 

  try:
    message = connectionSocket.recv(4096) #receive message from client
    filename = message.split()[1]
    f = open(filename[1:])
    outputdata = f.read() 
    
    #Send one HTTP header line into socket
    headerMessage = 'HTTP/1.1 200 OK\r\n\r\n'
    connectionSocket.send(headerMessage.encode())
    
    #Send the content of the requested file to the client
    for i in range(0, len(outputdata)):
      connectionSocket.send(outputdata[i].encode())
    connectionSocket.close()
    
  except IOError:
    #Send response message for file not found
    headerMessage = 'HTTP/1.1 404 Not Found\r\n\r\n404 File not found'
    connectionSocket.send(headerMessage.encode())
    
    #Close client socket
    connectionSocket.close()

serverSocket.close()