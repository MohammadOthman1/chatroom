import socket 
import threading
import json 

from db import DatabaseCommands
DB = DatabaseCommands()

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
clientsLock = threading.Lock()

#this will be running for each connection
def handle_client(conn, username): 
    print(f"[NEW CONNECTION]{username} connected.")
    try:
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                if msg == DISCONNECT_MESSAGE:
                    connected = False

                print(f"[{username}] {msg}")
                for client in clients :
                    if client == conn :
                        continue

                    client.send(f"[{username}]: {msg}".encode(FORMAT))
    finally:
        with clientsLock:
            for client in clients :
                if client == conn :
                    clients.remove(client)
        conn.close()

def jsonCheck(msg):
    try:
        json.loads(msg)
        return True
    except json.JSONDecodeError:
        return False

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr  = server.accept()
        msg_length = conn.recv(HEADER).decode(FORMAT)
        username = conn.recv(int(msg_length)).decode(FORMAT)
        with clientsLock :
            clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, username))
        thread.start()
        print(f"[Active CONNECTIONS] {threading.active_count() - 1 } ") 

print("[STARTING] Server is starting...")
start()