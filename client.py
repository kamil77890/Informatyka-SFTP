import paramiko
from time import sleep


def main():
    host = "localhost"
    port = 22
    username = "abc"
    password = "def"

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port,
                   username=username, password=password)
    print("Połączenie udane!!!!")

    shell = client.invoke_shell()

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
    main()
