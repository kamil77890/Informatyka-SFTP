# SFTP Client by kamil77890 & bambus80

This is the client part of a custom implementation of the SFTP (SSH File Transfer Protocol) in Python, using SSH methods from the `paramiko` library. It is run from command line.

# Command-line arguments

#### -H / --host:

Host address, by default set to `localhost`. (Optional)

#### -p / --port:

Host port, by default set to 22. (Optional)

#### -u / --user

FTP username. **(Required)**

#### -P / --password

FTP password, by default set to none. (Optional)

# Files

Files used and put by the server are stored inside `/PATH/TO/FILE/contents` folder.

# Commands

The client accepts following commands:

#### `help` - Show list of commands and connection info

#### `exit` - Disconnect and leave the program

#### `get` - Send file to client

#### `put` - Save file in the server

#### `ls` - Get a list of all files in the directory