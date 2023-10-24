import socket 
import threading
import tkinter as tk

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.15"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

class MyGUI:

    def __init__(self):
        self.root = tk.Tk()

        self.textbox = tk.Text(self.root, height=5, font=("Arial", 16))
        self.textbox.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text="Send", font=("Arial", 16),command=self.send_message)
        self.button.pack(padx=10, pady=10)

    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    def close_window(self):
        self.root.quit()  # exit the tkinter main loop


    def send_message(self):
        inputt = self.textbox.get('1.0', tk.END)
        if inputt == "exit":
            self.close_window() 
            self.send(DISCONNECT_MESSAGE)
        else:
            self.send(inputt)
            self.textbox.delete('1.0', tk.END)

def receive():
    while True:
        print(client.recv(2048).decode(FORMAT))

def main():
    my_gui = MyGUI()
    threadReceive = threading.Thread(target=receive)
    threadReceive.start()
    my_gui.root.mainloop()  # Start the Tkinter main loop

main()
