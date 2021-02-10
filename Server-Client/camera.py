# following tutorial from https://www.geeksforgeeks.org/socket-programming-python/

# Import socket module 
import socket   

new_parking_spot = input("What parking spot is open: ")  
  
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 1233              
  
# connect to the server on local computer 
s.connect(('3.16.24.149', port)) 
# s.connect(('127.0.0.1', port)) 

# send data to the server 
s.sendall(bytes(new_parking_spot, 'utf-8'))
# close the connection 
s.close()  