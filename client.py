import socket
import threading
import json

global host 
global port

with open('config.json') as f:
    config = json.load(f)
    host = config['host']
    port = config['port']


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("Connection lost.")
            client_socket.close()
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    username = input("Enter your username: ")
    client.send(username.encode())

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input()
        if(message != ''):
            client.send(message.encode())

if __name__ == "__main__":
    main()
