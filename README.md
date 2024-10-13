This code allows up to 3 clients to communicate simultaneously with a TCP server. The server handles client requests through this connection and logs the client activities. 

# Operations
Client communicates with the server via 4 commands:
1.	“exit”: Disconnects the clients and logs the disconnection.
2.	“status”: Returns a JSON string with all cached and current client connections.
3.	“list”: Returns a JSON string of accessible text files in the server directory.
4.	“get <filename.txt>”: Returns the content of the specified text file or an error message if the file does not exist.

# Code Overview
Initialization:
-	Sets up a TCP “serverSocket”, binds it to a specified port, and listens for incoming connections (maximum of 3 clients).
-	Initializes a list “avaliableClients” to track available client slots.
-	Initializes a dictionary “clientLogs” to track client logs.
Connection Loop:
-	Continuously waits for client connections, timeout every 5 seconds.
-	Upon client connection request, initialize a “connectionSocket” with client, assigns a client number, and starts a new thread under “handle_client()” function to handle client messages.
Client Handle:
-	Client slots, client log, and directory are stored globally and can be modified by all connection threads.
-	Create or update client log for every new connection, notifies clients of their client number, and enters message loop.
-	Message loop responds continuously to client commands until client exits.

Client Side:
-	Input loop continues to receive and deliver commands to server.
-	Gracefully terminate on user exits or exception.

# Special consideration
1.	Server timeouts every 5 seconds to check for ctrl-c keystroke termination.
2.	Server can only read file encoded in “utf-8”.
3.	Server automatically closes all thread on sys.exit().
4.	Client receives up to 2MB.
5.	Server multi-threads each client connection.
6.	Server and client handles exceptions and gracefully shuts down.
7.	Uses JSON for data serialization to send structured responses.
