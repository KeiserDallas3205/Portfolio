from socket import *

client_socket = socket(AF_INET, SOCK_STREAM)

# Create a client socket w/ given IP and port number
server_ip = input("Server ip: ")
server_port = input("Server port: ")

# Connect socket to the server
client_socket.connect((server_ip, int(server_port)))
print("Connection established.\n")

# Ask for a message and send it to server socket 
message = input("Message: ")
client_socket.send(message.encode())

# Receive a message from a server and display
received_message = client_socket.recv(2048)
print("Receieved message: {}".format(received_message))

# Clean up the TCP connection 
client_socket.close()
