# SFTP Client

### by kamil77890 & bambus80

---

# Overview

This is the client part of a custom implementation of the SFTP (SSH File Transfer Protocol) in Python, using SSH methods from the `paramiko` library. It is run from command line.

---

# Command-line arguments

#### -H / --host:

Host address, by default set to `localhost`. (Optional)

#### -p / --port:

Host port, by default set to 22. (Optional)

#### -u / --user

FTP username. **(Required)**

#### -P / --pwd

FTP password, by default set to none. (Optional)

---

# Files

Files used and put by the server are stored inside `/PATH/TO/FILE/contents` folder.
