"""
Name: Keiser Dallas
Date: 12/16/2021
CSC 450-001
Winter 2022
Desc: This program establishes a TCP connection on the server side that receives a GET request,
      processes it, and sends the status code back to the client. The program waits indefinitely
      on port 12000 and listens for messages. 

"""

# Import the socket library for establishing connections
from socket import *

# Import request library to make GET requests
import requests




# Create a socket
server_socket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to port 12000
server_socket.bind(('',12000))

# Listen for incoming messages 
server_socket.listen(1)




while(True):

    # Wait for a connection
    print("Server is ready to receive...\n")
    connection_socket, clientPort = server_socket.accept()

    
    # Receive GET request, and display it along with client info
    incomingMessage = connection_socket.recv(2048) 
    print("HTTP request:\n  GET /{} \n Host: {}\n".format(incoming_message.decode(), connection_socket))

    # Complete the GET request
    gRequest = requests.get(incoming_message.decode())

    # Get the status code and display it to screen
    status = gRequest.status_code
    print("HTTP response message:\n {}".format(status))

    # Send the status code back to the client 
    connection_socket.send(status.encode()) 
    
    # Clean up the TCP connection
    connection_socket.close() 
    
