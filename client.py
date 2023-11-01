import socket 
import threading
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import re
import json 

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
        self.singupPage()
        # self.main_page()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def landingPage(self):
        self.geometry("400x350")
        self.title("Chatroom")

        label = tk.Label(self, text="Chatroom", font=('Arial', 28))
        label.grid(row=0, column= 0, padx=110, pady=0)

        loginButton = tk.Button(self, text="Click here to login", font=('Arial', 18), command=self.loginPage)
        loginButton.grid(pady=30)
        
        signupButton = tk.Button(self, text="Click here to signup", font=('Arial', 18), command=self.singupPage)
        signupButton.grid()

    def singupPage(self):
        self.geometry("1000x350")
        self.title("Signup Page")

        label = tk.Label(self, text="Sign Up", font=('Arial', 28))
        label.grid(row=0, column= 0, padx=10, pady=0)

        usernameLabel = tk.Label(self, text="Enter your username", font=('Arial', 18))
        usernameLabel.grid(row=1, column=0)
        self.usernameEntry = tk.Entry(self,width=50, font=('Arial', 16))
        self.usernameEntry.grid(row=1, column=1, padx=0, pady=10)

        emailLabel = tk.Label(self, text="Enter your email", font=('Arial', 18))
        emailLabel.grid(row=2, column=0)
        self.emailEntry = tk.Entry(self, width=50, font=('Arial', 16))
        self.emailEntry.grid(row=2, column=1, padx=0, pady=10)

        passwordLabel = tk.Label(self, text="Enter your password", font=('Arial', 18))
        passwordLabel.grid(row=3, column=0)
        self.passwordEntry = tk.Entry(self, width=50, font=('Arial', 16),show="*")
        self.passwordEntry.grid(row=3, column=1, padx=0, pady=10)

        passwordReentryLabel = tk.Label(self, text="Re-enter your password", font=('Arial', 18))
        passwordReentryLabel.grid(row=4, column=0)
        self.passwordReentryEntry = tk.Entry(self, width=50, font=('Arial', 16),show="*")
        self.passwordReentryEntry.grid(row=4, column=1, padx=0, pady=10)

        signupButton = tk.Button(self, text="Signup", font=('Arial', 18), command=self.signup)
        signupButton.grid(row=5, column=1, pady=20)
    
    def signup(self):
        username = self.usernameEntry.get()
        email = self.emailEntry.get()
        password = self.passwordEntry.get()
        passwordReentry = self.passwordReentryEntry.get()
        if password != passwordReentry:
            messagebox.showinfo(title="Error", message="Passwords dont match")
            return
        if not self.emailCheck(email):
            messagebox.showinfo(title="Error", message="Email invalid")
            return
        
        dic = {
            "username": username,
            "password": password,
            "email": email,
            "rank": 3,
        }
        dictionary = json.dumps(dic)

        self.send(dictionary)
        response = client.recv(2048).decode(FORMAT)       
        if response:
            messagebox.showinfo(self, message = f"{response} already exists")
            return
        messagebox.showinfo(self,message="Signup succesfull, please login")
    def loginPage(self):
        self.geometry("1000x350")
        self.title("Login Page")

        label = tk.Label(self, text="Login", font=('Arial', 28))
        label.grid(row=0, column= 0, padx=10, pady=0)

        usernameLabel = tk.Label(self, text="Enter your username", font=('Arial', 18))
        usernameLabel.grid(row=1, column=0)
        usernameEntry = tk.Entry(self,width=50, font=('Arial', 16))
        usernameEntry.grid(row=1, column=1, padx=0, pady=10)


        passwordLabel = tk.Label(self, text="Enter your password", font=('Arial', 18))
        passwordLabel.grid(row=2, column=0)
        self.passwordEntry = tk.Entry(self, width=50, font=('Arial', 16),show="*")
        self.passwordEntry.grid(row=2, column=1, padx=0, pady=10)

        loginButton = tk.Button(self, text="Login", font=('Arial', 18))
        loginButton.grid(row=5, column=1, pady=20)

    def main_page(self):
        self.txt = tk.Text(self, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60) #Creates the textbox for the messages
        self.txt.config(state=DISABLED) #Modifies the textbox read only
        self.txt.pack() #Shows / places the textbox in the tkinter window
        
        scrollbar = tk.Scrollbar(self.txt) #Creates scrollbar
        scrollbar.place(relheight=1, relx=0.974)
        
        self.entrybox = tk.Entry(self, font=("Arial", 16))
        self.entrybox.pack(padx=10, pady=10)
        
        button = tk.Button(self, text="Send", font=("Arial", 16), command=self.send_message)
        button.pack(padx=10, pady=10)
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
            self.destroy()
            self.send(DISCONNECT_MESSAGE)
            

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
    def emailCheck(self,email):
        # Define a regular expression pattern for a valid email address
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        # Use the re.match() function to check if the input matches the pattern
        if re.match(pattern, email):
            return True

        return False
    def main(self):
        threadReceive = threading.Thread(target=self.receive)
        threadReceive.start()
        
C = Chatroom()
C.main()
C.mainloop()