# Tasks
- Log and time format
- Multi-threading clients
- Server and Client exception handling
- Server file download
- Code documentations
- Report.pdf file & README file
- Git repository
- Remoate connection using addresses

# Completion
## Oct 11, 2024
Checklist (Complete):
- Single Client handling
- Add Server response to Client message
- Add Client log with Client number dictionary & history of connections with the same Client number
- Create formatted time using datatime library
- Create formatted dictionary string using dumps(, indent=2)
- Create formatted Client name using {currentClient:02} that zeros second digit (e.g. Client01)
- Fix Client appending rejoins into log

Checlist (Complete):
- Multi Clients handling (multithreading)
- Add initial "You are Client##!" Server message before Server message loop
- Allow dictionary to be transferred to client through byte string deserialization
- Fix Client number to accomodate Client with larger number quitting before the lower (e.g. Client02 quit before Client01)
Client-side:
- Add Client message loop
- Add graceful exit (rather than forced server disconnection)

## Oct 12, 2024
Checklist (Complete):
- Add Server and Client exception handling
Server-side:
- Fix ctrl-c blocked by .accept()
- Add Server graceful exit by ctrl-c
- Add timeout loop
- Fix sys.exit() does not end program until all thread completes
- Add Server full message
Client-side:
- Add exception handling for server or client side disconnection
- Add timeout for when server's full

Checklist (Complete):
- Add Server file listing and downloading
- Add 'list' command that list all txt file in current directory
- Add 'get xxx.txt' command for file reading
- Fix file reading encoding error by setting 'utf-8'
- Add file reading exception handling
- Increase clientSocket.recv() size

- Add code header with name and student ID

## Oct 13, 2024
Checklist (Complete):
- Complete code testing
- Complete report.docx
- Upload to Git Hub
- Submission