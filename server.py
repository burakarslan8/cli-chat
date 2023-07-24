import socket
import threading
import json

clients = []

global host 
global port

with open('config.json') as f:
    config = json.load(f)
    host = config['host']
    port = config['port']

def handle_client(client_socket):
    
    username = client_socket.recv(1024).decode()
    print(f"[*] {username} connected.")

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            
            message_with_username = f"{username}: {message.decode()}"
            
            for client in clients:
                if client != client_socket:
                    client.send(message_with_username.encode())
        except:
            break

    # if a client disconnects, remove it from the list
    clients.remove(client_socket)
    client_socket.close()
    print(f"[*] {username} disconnected.")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        clients.append(client)
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    main()
