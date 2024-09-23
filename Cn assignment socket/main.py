import socket

host = '127.0.0.1'
port = 8080

HTML_FILES = {
    '/': 'index.html',
    '/index.html': 'index.html',
    '/about.html': 'about.html',
    '/another_page.html': 'another_page.html',
    '/contact.html': 'contact.html',
    '/examples.html': 'examples.html',
}

HTTP_200_OK = 'HTTP/1.0 200 OK\n\n'
HTTP_404_NOT_FOUND = 'HTTP/1.0 404 NOT FOUND\n\n'

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print('Serving port...')

def file(path):
    with open(path, 'r') as f:
        return f.read()

while True:
    connection, address = s.accept()
    message = connection.recv(1024).decode()
    path = message.split()[1]
    path = HTML_FILES.get(path, None)
    
    if not path:
        response_message = HTTP_404_NOT_FOUND.encode()
        connection.sendall(response_message)
        connection.close()
        continue
    
    file_contents = file(path)
    response_message = (HTTP_200_OK + file_contents).encode()
    connection.sendall(response_message)

    connection.close()
