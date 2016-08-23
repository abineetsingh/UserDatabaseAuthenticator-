#This is a login authentication program
#This program takes in user credentials and then checks to see if the information exists in the database, and if so is it correct 

from Crypto.Hash import SHA256
import getpass
import sqlite3

#Function used to generate a 16 bit hex salt that will be used for stronger password hashes
def Generate_Salt():
    return urandom(16).encode("Hex") 
  
#Function used to hash a password using SHA
def SHA_256(salt, userInput):
    hash = SHA256.new(salt + userInput)
    return hash.hexdigest()

#This function is used to check if the inputted user credentials are correct 
def authenticate(username, password, connect):
    #Initialization of a cursor class
    cur = connect.cursor() 

    #A 1 element tuple indicated by a , at the end  
    credentials = (username,) 
    cur.execute("SELECT * FROM Users WHERE Username=?", credentials)

    #This will be like a list containing each of the elements from the columns of the users table 
    fetchedCredential = cur.fetchone()
    
    #If a user enters in information that isnt contained in the database then deal with the nonetype error 
    #An error check if the user credential is not found in the database, then a NoneType is returned
    if fetchedCredential == None: 
        print("User not found!") 
    #If the credentials are correct 
    elif fetchedCredential[2] == SHA_256(fetchedCredential[3], password): 
        print("Welcome " + username)
    #If the user information exists in the database but is entered incorrectly 
    else:
        print("Incorrect username or password, dont make me pull out the captcha...") 

#RUN
#Connect to the database
connect = sqlite3.connect("Hashed_Passwords.db")
#Input, getpass hides what characters are typed for the password
username = raw_input("Enter your username: ")
password = getpass.getpass("Enter your password: ")  
authenticate(username, password, connect) 

