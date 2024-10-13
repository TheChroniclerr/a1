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
from threading import Thread, Lock  # for multi-threading clients
from datetime import datetime   # for time format & log
import sys  # for graceful termination of program
import json # for dictionary byte serialization
import os   # for directory file reading

# Functions
def get_formatted_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

def get_directory_txts(directory):
    files = os.listdir(directory)
    text_files = [file for file in files if file.endswith('.txt')]
    return text_files

def get_txt_string(filename):
    default_encoding = "utf-8"
    with open(filename, 'r', encoding=default_encoding) as file:
        content = file.read()
        return content

def handle_client(connectionSocket, addr, currentClient):    # multithread client handler function
    global avaliableClients
    global clientLogs
    global directory
    
    # Handle exception locally as it does not proprogate back to main thread
    try:
        print(f"\tClient{currentClient:02} joined!")

        # Case: when client rejoin, it changes existing record rather than appending a new one
        # Create new dictionary key if it doesn't already exist, and only use append if it does so pre-exsiting log aren't modified
        if clientLogs.get(f"Client{currentClient:02}") is None:
            clientLogs[f"Client{currentClient:02}"] = []

        # Log client data
        clientLogs[f"Client{currentClient:02}"].append(
            {
                "address": addr,
                "connected_at": get_formatted_time(),
                "disconnected_at": "Currently Active"
            }
        )
        
        # Send client number
        connectionSocket.send(f"Client{currentClient:02}".encode())

        # Persistent connection (open until client enters "exit")
        while True:
            # Client listener (holds thread)
            clientMessage = connectionSocket.recv(1024).decode()
            
            # Server response
            if clientMessage == "exit":
                break   # finally handles exit clean ups
            elif clientMessage == "status":
                stringLog = json.dumps(clientLogs, indent=2)  # serialization (turn dictionary to string for encoding)
                connectionSocket.send(stringLog.encode())
            elif clientMessage == "list":
                txtList = get_directory_txts(directory)
                stringList = json.dumps(txtList, indent=2)
                connectionSocket.send(stringList.encode())
            elif clientMessage.startswith("get "):
                filename = clientMessage[4:]
                try:
                    stringFileContent = get_txt_string(filename)
                    print(f"\tClient{currentClient:02} accessed {filename}")
                except FileNotFoundError:
                    stringFileContent = "Invalid filename, please try again"
                connectionSocket.send(stringFileContent.encode())
            else:
                connectionSocket.send(f"{clientMessage} ACK".encode())
    except Exception as e:
        print(f"Error {type(e)}: {e}")
    finally:
        connectionSocket.close()
        # Clean ups
        clientLogs[f"Client{currentClient:02}"][-1]["disconnected_at"] = get_formatted_time()
        print(f"\tClient{currentClient:02} left!")
        avaliableClients[currentClient - 1] = 0 # re-empty client spot at index (i.e. client number -1)

# Variables
# lock = Lock() # Case: no race-condition because client numbers are unique; they do not conflict
serverPort = 6789   # Assign a port number
maxClients = 3
avaliableClients = [0] * maxClients
directory = '.'
clientLogs = {}

# Create and bind a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Case: serverSocket.accpet() blocks call; program cannot terminate using Ctrl-C
serverSocket.settimeout(5)  # Set a five second timeout that allows program to check for keyboard interrupts

# Specify maximum number of clients to listen
serverSocket.listen(maxClients)

ip_address, port = serverSocket.getsockname()
print(f"Server listening on {ip_address}:{port}")

# Server listens to incoming clients, add connectionSocket to new thread
try:
    while True:
        # Timeout loop
        try:
            # Set up a new connection from the client
            print("Waiting for connection...")
            connectionSocket, addr = serverSocket.accept()
            
            # Case: Client with lower number disconnect before higher (e.g. Client03 disconnects before Client02)
            # Use index to find the first avaliable client spot
            clientNumber = avaliableClients.index(0) + 1    # add one since client number starts at 1 whereas index starts at 0
            avaliableClients[clientNumber - 1] = 1
            
            # Multithread each client connection
            # Case: sys.exit() does not terminate program and waits for non-daemon threads to finish
            # Setting thread as daemon automatically terminate threads when sys.exit() is called
            clientThread = Thread(target=handle_client, args=(connectionSocket, addr, clientNumber), daemon=True)
            clientThread.start()
        # Check for keyboard interrupts
        except TimeoutError:
            pass
        # Check for >3 client join attempts
        except ValueError:
            print(f"\tServer full: Client join failed")
            pass
except KeyboardInterrupt:
    pass
except Exception as e:
    print(f"Error {type(e)}: {e}")
finally:
    serverSocket.close()
    print("Server shut down")
    sys.exit()  #Terminate the program
    print("program exits")