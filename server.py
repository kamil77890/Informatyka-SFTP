import socket
import paramiko
import os

HOST = 'localhost'
PORT = 222


class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = None

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == 'abc' and password == 'def':
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


def handle_file_transfer(channel):
    while True:
        command = channel.recv(1024).decode('utf-8').strip()
        if command.startswith("get"):
            filepath = command.split(" ", 1)[1]
            if os.path.exists(filepath):
                with open(filepath, 'rb') as file:
                    data = file.read()
                    channel.sendall(data)
            else:
                channel.sendall(b"File not found")
        elif command.startswith("put"):
            _, filepath = command.split(" ", 1)
            with open(filepath, 'wb') as file:
                while True:
                    data = channel.recv(1024)
                    if not data:
                        break
                    file.write(data)
            channel.sendall(b"File received successfully")
        elif command == "exit":
            break
        else:
            channel.sendall(b"Invalid command")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    print(f"Listening for connections on {HOST}:{PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(
            f"Accepted connection from {client_address[0]}:{client_address[1]}")

        ssh_server = SSHServer()
        transport = paramiko.Transport(client_socket)
        host_key = paramiko.RSAKey.generate(2048)
        transport.add_server_key(host_key)

        try:
            transport.start_server(server=ssh_server)
        except paramiko.SSHException as e:
            print(f"SSH negotiation failed: {str(e)}")
            continue

        channel = transport.accept(20)
        if channel is None:
            transport.close()
            continue

        print("Authentication successful!")
        print(transport)
        try:
            handle_file_transfer(channel)
        except Exception as e:
            print(f"Error during file transfer: {str(e)}")

        channel.close()
        transport.close()


if __name__ == "__main__":
    main()
