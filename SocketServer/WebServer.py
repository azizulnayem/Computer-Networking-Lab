from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('127.0.0.1', 6789))
serverSocket.listen(1)
print('Ready to serve...')

while True:
    connectionSocket, addr = serverSocket.accept()
    
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        
        with open(filename[1:], 'r') as f:
            outputdata = f.read()
        
        connectionSocket.send(b"HTTP/1.1 200 OK\r\n")
        connectionSocket.send(b"Content-Type: text/html\r\n")
        connectionSocket.send(b"\r\n")
        
        connectionSocket.send(outputdata.encode())
        
    except IOError:
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n")
        connectionSocket.send(b"Content-Type: text/html\r\n")
        connectionSocket.send(b"\r\n")
        connectionSocket.send(b"404 Not Found")
        
    finally:
        connectionSocket.close()

serverSocket.close()
