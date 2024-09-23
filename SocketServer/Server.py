from socket import *
import threading

host = "127.0.0.1"
port = 4446

clients = {}
client_names = ["Client1", "Client2", "Client3"]
client_status = [False, False, False]
message_history = []

def broadcast(message, sender_socket=None):
    message_history.append(message.decode())
    for client in clients.values():
        if client['socket'] != sender_socket:
            try:
                client['socket'].send(message)
            except:
                client['socket'].close()

def handle_client(client_socket, addr, client_name, client_index):
    print(f"{client_name} ({addr[0]}:{addr[1]}) connected.")
    client_socket.send(f"Welcome {client_name}!\n\n\nHere's the chat history:\n".encode())

    if message_history:
        for message in message_history:
            client_socket.send(f"{message}\n".encode())

    if client_status[client_index] is False:
        broadcast(f"{client_name} has joined the chat.".encode())
    else:
        broadcast(f"{client_name} has rejoined the chat.".encode(), client_socket)

    client_status[client_index] = True  

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"{client_name}: {message.decode()}")
            broadcast(f"{client_name}: {message.decode()}".encode(), client_socket)
        except:
            break

    print(f"{client_name} disconnected.")
    client_socket.close()
    clients.pop(client_name)
    client_status[client_index] = False 
    broadcast(f"{client_name} has left the chat.".encode())

def start_server():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is listening on {host}:{port}...")

    while True:
        client_socket, addr = server_socket.accept()

        available_index = next((i for i, connected in enumerate(client_status) if not connected), None)

        if available_index is not None:
            client_name = client_names[available_index]
            clients[client_name] = {'socket': client_socket}

            threading.Thread(target=handle_client, args=(client_socket, addr, client_name, available_index)).start()
        else:
            client_socket.send("Chat room is full. Please try again later.".encode())
            client_socket.close()

start_server()
