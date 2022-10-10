"""
Name: Keiser Dallas
Date: 10/10/2022
Desc: This program is an example of establishing TCP connection on the client side.
      The program prompts the user for a server ip address and port number, then it
      sends the desired message to that server. Afterwards, an altered message is
      received from the server and the connection is closed. 

"""

# Import socket for establishing TCP connection
from socket import *

# Create the client socket
client_socket = socket(AF_INET, SOCK_STREAM)

# Ask user for server IP address and port number
server_ip = input("Server ip: ")
server_port = input("Server port: ")

# Connect client socket to the server socket
client_socket.connect((server_ip, int(server_port)))
print("Connection established.\n")

# Ask user for a message and send it to server socket 
message = input("Message: ")
client_socket.send(message.encode())

# Receive a message from a server and display
received_message = client_socket.recv(2048)
print("Receieved message: {}".format(received_message))

# Clean up the TCP connection 
client_socket.close()
