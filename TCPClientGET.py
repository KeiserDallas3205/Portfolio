"""
Name: Keiser Dallas
Date: 12/16/2021
CSC 450-001
Winter 2022
Desc: This program established a client TCP connection that sends a GET request to a desired
      server, and receives a status back from the server. The program needs to be ran through 
      the terminal with the <server ip> <GET request> <server port #> as command line arguments
      in that order.
"""

# Import socket library for establishing connection
from socket import *
# Import systems for command line arguments 
import sys 

# Get the host and GET_request from command line arguments
    
server_ip = sys.argv[1] # Host Name
GET_request = sys.argv[3]
server_port = sys.argv[2] 

# Create client socket
client_socket = socket(AF_INET, SOCK_STREAM)   

# Connect client socket to the server socket 
client_socket.connect((server_ip, int(server_port))) 

# Format the GET request
message = " {} HTTP/1.1".format(GET_request)

# Display the client request to screen
print("HTTP request to server:\n GET /{} \n Host: {}".format(message, server_ip))

# Send the message to server socket
client_socket.send(message.encode())

# Receive a status from the server socket and display
status = client_socket.recv(2048) 
print("HTTP response from server:\n {}".format(status.decode()))

# Close the client socket
client_socket.close()   
