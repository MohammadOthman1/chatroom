import mysql.connector 
import sys
from passlib.hash import bcrypt
class DatabaseCommands():
    def __init__(self):
        self.localhost = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "chatroom"
        self.cursor = None
        self.connection = None

    def connectDB(self):
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                connect_timeout = 30
            )

            self.cursor = self.connection.cursor()
            self.cursor.execute("SHOW DATABASES LIKE '{}'".format(self.database))
            DBexists = self.cursor.fetchall()

            if DBexists:
                self.cursor.execute("USE {}".format(self.database))
                return

            self.cursor.execute("CREATE DATABASE {}".format(self.database))
            self.cursor.execute("USE {}".format(self.database))
            self.cursor.execute("""
                CREATE TABLE ranks(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                )
            """)
            self.cursor.execute("""
                CREATE TABLE users(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255),
                    password VARCAHR(255),
                    email VARCHAR(255),
                    fk_rank INT,
                    FOREIGN KEY (fk_rank) REFERENCES rank(id)
                )
            """)

        except mysql.connector.Error as e:
            if isinstance(e, mysql.connector.errors.InterfaceError):
                print("\nError: Connection to MySQL refused. Please check the status or the MySQL server configuration.")
            else:
                print("\nAn error occurred: ", str(e))

            sys.exit(1)

    def closeDB (self):
        try:
            self.cursor.close()
            self.connection.close()
        except Exception as e:
            print(f"There is an Error: {str(e)} ")

    def insertUser(self, username, password, email, rank):
        self.connectDB()
        queryUsername = "SELECT username FROM users WHERE username LIKE %s"
        valuesUsername = (f"%{username}%", )
        self.cursor.execute(queryUsername, valuesUsername)
        resultUsername = self.cursor.fetchone()
        if resultUsername:
            return 1
        queryEmail = "SELECT username FROM users WHERE username LIKE %s"
        passwordHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))
        query = "INSERT INTO users (username, password, email, fk_rank) VALUES (%s, %s, %s,%s)"
        values = (username, passwordHash, email, rank)

        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Succesfully inserted new user")
        except Exception as e:
            self.connection.rollback()
            print(f"There is an Error: {str(e)} ")

        self.closeDB()

    def checkLogin(self, username, password):
        query = "SELECT id FROM users WHERE username LIKE %s" # %s placeholder for username   |   checks if user is in databnase
        values = (f"%{username}%",)#username here will go instead of the %s when user tries to login 
        self.cursor.execute(query, values) 
        result = self.cursor.fetchone() #this Result is being used down result[0]
        if result is None:
            return False
        
        query = "SELECT password FROM users WHERE id = %s"    # checks passwords and gives the info to result 2 
        values = (result[0],) #result[0] because fetchone returns info like this (1, ) or passwords like this (mohamado, )
        self.cursor.execute(query, values)
        result2 = self.cursor.fetchone() #this Result is being used down result[0] result returns tuple 
        if result2 is None:
            return False
        
        if bcrypt.checkpw(password.encode(), result2[0].encode()):
            return True
        return False
