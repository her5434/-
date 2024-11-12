
import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                broadcast(message, client_socket)
            else:
                remove(client_socket)
                break
        except:
            continue

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                remove(client)

def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen(100)

clients = []

print("Сервер запущен...")
while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    print(f"Подключен: {addr}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
