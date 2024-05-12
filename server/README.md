# SFTP Client by kamil77890 & bambus80

This is the server part of a custom implementation of the SFTP (SSH File Transfer Protocol) in Python, using SSH methods from the `paramiko` library. It is run from command line.

# Command-line arguments

#### -H / --host:

Host address, by default set to `localhost`. (Optional)

#### -p / --port:

Host port, by default set to 22. (Optional)

#### -u / --user

FTP username. **(Required)**

#### -P / --password

FTP password, by default set to none. (Optional)
> If the password is left blank, the server will accept any connection matching the username. For security reasons, we do not recommend it.

# Files

Files used and put by the server are stored inside `/PATH/TO/FILE/contents` folder.

# FTP Commands

The server accepts following FTP commands:

#### `get` - Send file to client

#### `put` - Save file in the server

#### `ls` - Get a list of all files in the directory