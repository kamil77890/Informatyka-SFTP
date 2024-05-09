import socket
import paramiko
import os
import sys

HOST = 'localhost'
PORT = 22


class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        pass

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == 'abc' and password == 'def':
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


def handle_command(channel):
    try:
        while not channel.closed:
            command = channel.recv(1024).decode('utf-8').strip()
            if command == "":
                print("connection lost")
                break

            print(f"Command received: {command}")
            process_command(command, channel)
    except Exception as e:
        print(f"Exception in receiving command: {e}")
    finally:
        print("Cleaning up channel.")
        channel.close()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.close()


def process_command(command, channel):
    if command.startswith("echo"):
        response = command[5:]
        channel.sendall(response.encode('utf-8'))
    elif command.startswith("get"):
        filename = command.split(maxsplit=1)[1]
        try:
            with open(filename, 'rb') as file:
                data = file.read()
            channel.sendall(data)
        except FileNotFoundError:
            channel.sendall(b"File not found")
    elif command.startswith("put"):
        filename = command.split(maxsplit=1)[1]
        with open(filename, 'wb') as file:
            while True:
                data = channel.recv(1024)
                if not data:
                    break
                file.write(data)
        channel.sendall(b"File received successfully")
    elif command == "exit":
        channel.sendall(b"Exiting.")
        channel.close()
    else:
        channel.sendall(b"invalid command")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Listening for connections on {HOST}:{PORT}...")

    try:
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
            except paramiko.SSHException:
                continue

            channel = transport.accept()
            if channel is None:
                print("No channel")
                transport.close()
                continue

            handle_command(channel)
            transport.close()
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
