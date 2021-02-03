# following tutorial from https://www.geeksforgeeks.org/socket-programming-python/

# first of all import the socket library 
import socket 
import errno
  
# next create a socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
print("Socket successfully created")

# s.setblocking(False)

# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 1234              
  
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
s.bind(('', port))       
print("socket binded to %s" %(port))
  
# put the socket into listening mode 
s.listen(5)      
print("socket is listening")         
  
# a forever loop until we interrupt it or  
# an error occurs 

data = b''

while True: 

    try:

        # Establish connection with client. 
        c, addr = s.accept()  
        c.setblocking(0)
        print('Got connection from', addr )

        # if camera sending data
        try: 
            data = c.recv(1024)

            if not data: break

            print("Parking spot open at: "+data.decode("utf-8"))

            # Close the connection with the client 
            c.close() 

        # if client wanting to receive data
        except socket.error:
            print("Sending data to client")
            # err = e.args[0]
            # if err == errno.EAGAIN or err == errno.EWOULDBLOCK:

            # Tell client that new parking spot opened up 
            c.send(data) 
            
            # Close the connection with the client 
            c.close() 

            data = b"No new parking spots are open"

    except socket.error:
        print("Error Occured.")
        break
  
   