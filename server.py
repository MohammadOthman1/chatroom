import socket 
import threading

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