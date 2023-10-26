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
def handle_client(conn, addr): 
    print(f"[NEW CONNECTION]{addr} connected.")
    try:
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if jsonCheck(msg):
                    unpackedData = json.loads(msg)
                    values_list = [value for value in unpackedData.values()]
                    #when u print inserted data it prints the returned value of insertUser in db which is "username"
                    insertedData = DB.insertUser(values_list[0], values_list[1], values_list[2], values_list[3])
                    if not insertedData:
                        continue
                    if insertedData == "username":
                        conn.send("username".encode(FORMAT))
                        continue
                    if insertedData == "email":
                        conn.send("email".encode(FORMAT))

                else:
                    if msg == DISCONNECT_MESSAGE:
                        connected = False

                    print(f"[{addr}] {msg}")
                    for client in clients :
                        if client == conn :
                            continue
                        
                        client.send(f"[{addr}] {msg}".encode(FORMAT))
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
        with clientsLock :
            clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[Active CONNECTIONS] {threading.active_count() - 1 } ") 

print("[STARTING] Server is starting...")
start()