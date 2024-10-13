"""
-------------------------------------------------------
Server
-------------------------------------------------------
Author:  Hubert Bao
ID:      169077248
Email:   baox7248@mylaurier.ca
-------------------------------------------------------
Author:  Adnan Awad
ID:      169028425
Email:   awad8425@mylaurier.ca
-------------------------------------------------------
__updated__ = "2024-10-12"
-------------------------------------------------------
"""
# Imports
from socket import *
import sys # for program termination
# import json # for byte stream deserialization

# Variables
serverName = 'localhost'
serverPort = 6789   # Assign a port number
receive_filesize = 2000000  # max file size for 'get' command: 2MB

# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.settimeout(5)  # timeout when socket communication waits >5 seconds

# Handle exception
try:
    # Recieve client number
    clientNumber = clientSocket.recv(1024).decode()
    print(f"You are {clientNumber}")

    # Persistent connection
    while True:
        message = input("Enter message: ")
        clientSocket.send(message.encode())
        # if message == "status":
        #     serverResponse = json.loads(serverResponse)   # Deserialize byte string to dictionary
        if message == "exit":
            break
        else:
            serverResponse = clientSocket.recv(receive_filesize).decode()
        print(f"Server response: {serverResponse}")
# Case: client socket lost connection to server, or server disconnect
except ConnectionResetError:
    print("Connection lost")
# Case: server inresponsive, server delay, or server full
except TimeoutError:
    print("Timeout disconnect")
except Exception as e:
    print(f"Error {type(e)}: {e}")
    clientSocket.close()
    print("Connection terminated")
    sys.exit()