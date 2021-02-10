# following tutorial from https://www.geeksforgeeks.org/socket-programming-python/

# Import socket module 
import socket                
  
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 1233               
  
# connect to the server on local computer 
s.connect(('18.191.80.98', port)) 
  
# receive data from the server 
print("Received data from server.\nNew parking spot open at: " + s.recv(1024).decode("utf-8"))
# close the connection 
s.close()  