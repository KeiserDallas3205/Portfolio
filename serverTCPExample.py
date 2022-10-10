"""
Name: Keiser Dallas
Date: 10/10/2022
Desc: This program is an example of how to establish the server side of a TCP connection.
      The server will run indefinitely, receive messages, and send a slightly altered message
      back to the client side. 
"""

from socket import * 
import sys


# Create a server socket (to receive messages)
server_socket = socket(AF_INET, SOCK_STREAM)

# Bind server socket to port 12000
server_socket.bind(('',12000))

# Make the socket listen to for messages
server_socket.listen(1)



while(True):
    # Wait for message
    print("Server is ready to connect...\n")

    # Receive new client 
    connection_socket, address = server_socket.accept()  

    # Display the client server information
    print("Connection is established with {}\n".format(address))

    # Receive the new message, and display the decoded version
    incoming_message = connection_socket.recv(2048)
    print("Message: {}".format(incoming_message.decode())) 

    # Change the incoming message, and display the modified message
    modified_message = incoming_message.upper()
    print("Message: {}".format(modified_message.decode())) 

    # Send the modified message back to client 
    connection_socket.send(modified_message) 
    print("Message sent.\n")

    # Clean up the TCP connection
    connection_socket.close() 
    
  
