import paramiko
import argparse
from time import sleep

import paramiko.ssh_exception


def main(args):
    host = args.host
    port = args.port
    username = args.user
    password = args.pwd

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=port,
                       username=username, password=password)
        print(f"Connected to {host}:{port}!")
    except Exception as e:
        print(f"Failed to connect to {host}:{port}!")
        print(e)
        return

    shell = client.invoke_shell()
    print("Client initialized")

    operation = input("Enter operation (put or get): ")
    filename = input("Enter filename: ")

    if operation == "put":
        shell.send(f"put {filename}\n")
        sleep(2)
        with open(filename, 'rb') as file:
            data = file.read()
            shell.send(data)
        shell.send(b"\n")
    elif operation == "get":
        shell.send(f"get {filename}\n")
        sleep(1)
        received_data = bytearray()
        while True:
            if shell.recv_ready():
                data = shell.recv(4096)
                received_data.extend(data)
                if len(data) < 4096:
                    break
            else:
                sleep(0.1)
        with open(f"received_{filename}", 'wb') as file:
            file.write(received_data)
        print(f"Received file {filename} and saved as received_{filename}.")
    else:
        print("Invalid operation.")

    shell.close()
    client.close()


if __name__ == "__main__":
    """
    SFTP client args:
      -H / --host:
        Host address, by default set to localhost. (Optional)
      -p / --port:
        Host port, by default set to 22. (Optional)
      -u / --user
        FTP username. (Required)
      -P / --pwd
        FTP password. (Optional)
    """
    parser = argparse.ArgumentParser(prog='SFTP_Client', description='SFPT Client made in Python')
    parser.add_argument('-H','--host',type=str,required=False,default="localhost")
    parser.add_argument('-p','--port',type=int,required=False,default=22)
    parser.add_argument('-u','--user',type=str,required=True)
    parser.add_argument('-P','--pwd',type=str,required=False)
    args = parser.parse_args()
    print("Custom SFTP client - by kamil77980 & bambus80")
    main(args)
