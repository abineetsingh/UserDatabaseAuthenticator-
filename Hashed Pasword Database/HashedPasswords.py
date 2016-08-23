#This program initializes a database with a users table that will hold User credentials 
#and hash passwords with a concatenated salt

from Crypto.Hash import SHA256
from os import urandom
import sqlite3 
import getpass

#Initialize the Database
connect = sqlite3.connect("Hashed_Passwords.db")
print("Accessed the database successfully!") 

#Format of our table in the database, can be accessed via .schema in sqlite3
def makeTable(connect): 
    connect.execute('''CREATE TABLE Users 
    (ID             integer Primary Key     Not Null,      
     Username       text                    Not Null,
     Hash           text                    Not Null,
     Salt           text                    Not Null);''')

    print("User table created successfully!")

#This function is used to create an admin in the first row of the database 
def createAdmin(connect): 
    cur = connect.cursor()     
    #A query 
    cur.execute("SELECT * FROM Users WHERE Username='admin'")     

    #If an admin doesnt exist create a new one 
    if cur.fetchone() == None:
        print("Creating Admin account!") 
        salt = Generate_Salt()   
        admin = (SHA_256(salt, "password123"), salt) 
        cur.execute("INSERT INTO Users (ID, Username, Hash, Salt) \
                     VALUES (01, 'admin', ?, ?)", admin)
        connect.commit() 

def addNewUser(connect, username, hashedPassword, salt): 
    #Credentials is a tuple which we make in order to pass the values we want to insert in the specified columns
    credentials = (username, hashedPassword, salt) 

    #This is essentially a prepared statement which will prevent SQL injection attacks by using the tuple made above
    connect.execute("INSERT INTO Users (Username, Hash, Salt) VALUES (?, ?, ?)", credentials) 
    connect.commit() 

#Function used to generate a 16 character hex salt that will be used for stronger password hashes
def Generate_Salt():
    return urandom(16).encode("Hex") 
  
#Function that will be used to hash the Users password concatenated with a salt
def SHA_256(salt, userInput):
    hash = SHA256.new(salt + userInput)
    return hash.hexdigest()

#RUN
#Comment the below line once the table is made, makeTable is only called when the database is first initialized
makeTable(connect) 
createAdmin(connect)
salt = Generate_Salt()
#Input, getpass hides what characters are typed for the password
username = raw_input("Enter your username: ")
password = getpass.getpass("Enter your password: ")  
hashedPassword = SHA_256(salt, password)
addNewUser(connect, username, hashedPassword, salt) 
