import socket 
import threading
import tkinter as tk
from tkinter import *
from tkinter import messagebox

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.15"
ADDR = (SERVER, PORT)
BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

class Chatroom(tk.Tk):
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        self.txt = tk.Text(self, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60) #Creates the textbox for the messages
        self.txt.config(state=DISABLED) #Modifies the textbox read only
        self.txt.pack() #Shows / places the textbox in the tkinter window
        
        self.scrollbar = tk.Scrollbar(self.txt) #Creates scrollbar
        self.scrollbar.place(relheight=1, relx=0.974)
        
        self.entrybox = tk.Entry(self, font=("Arial", 16))
        self.entrybox.pack(padx=10, pady=10)
        
        self.button = tk.Button(self, text="Send", font=("Arial", 16), command=self.send_message)
        self.button.pack(padx=10, pady=10)
    #This function makes the message box normal when it wants to insert a message and the makes it Read Only
    def add_message(self, msg, who): 
        self.txt.config(state=tk.NORMAL) #This line makes it normal
        self.txt.insert(tk.END, f"{who}: " + msg + "\n")
        self.txt.config(state=tk.DISABLED) # This line makes it Read Only

    def send(self, msg): #msg is user_input from send_message
        message = msg.encode(FORMAT)
        msg_length = str(len(message)).zfill(HEADER)
        client.send(msg_length.encode(FORMAT))
        client.send(message)

    def on_closing (self):
        if messagebox.askyesno(title= "Quit?", message="Do u want to quit this app"):
            messagebox.showinfo(title= "Closing",message="Bye kid")
            self.send(DISCONNECT_MESSAGE)
            self.destroy()
            
    #Chat Gpt
    # def send(self, msg):
    #     message = msg.encode(FORMAT)
    #     msg_length = len(message)
    #     client.send(msg_length.to_bytes(HEADER, byteorder='big'))
    #     client.send(message)

    #Original 
    # def send(self, msg):
    #     message = msg.encode(FORMAT)
    #     msg_length = len(message)
    #     send_length = str(msg_length).encode(FORMAT)
    #     send_length += b' ' * (HEADER - len(send_length))
    #     client.send(send_length)
    #     client.send(message)

    def send_message(self):
        user_input = self.entrybox.get()
        self.send(user_input)
        self.entrybox.delete(0, END)
        self.add_message(user_input, "YOU")

    def receive(self):
        while True:
            msg = client.recv(2048).decode(FORMAT)
            if msg:
                self.add_message(msg, "USER")

    def main(self):
        threadReceive = threading.Thread(target=self.receive)
        threadReceive.start()

C = Chatroom()
C.main()
C.mainloop()