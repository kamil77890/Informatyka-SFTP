import socket
import paramiko
import os
import signal
import sys
import logging

logging.basicConfig(level=logging.INFO)

HOST = 'localhost'
PORT = 22


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

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True  # Always allow PTY requests

    def check_channel_shell_request(self, channel):
        return True  # Always allow shell requests


def handle_command(channel):
    try:
        while not channel.closed:
            channel.settimeout(None)  # Disable timeout for blocking recv call
            command = channel.recv(1024).decode('utf-8').strip()
            if command == "":
                logging.info(
                    "No command received, possibly connection was closed.")
                break

            logging.info(f"Command received: {command}")
            process_command(command, channel)
    except Exception as e:
        logging.error(f"Exception in receiving command: {e}")
    finally:
        logging.info("Cleaning up channel.")
        channel.close()


def process_command(command, channel):
    if command.startswith("echo"):
        response = command[5:]  # Assumes echo command like "echo message"
        channel.sendall(response.encode('utf-8'))
    elif command.startswith("get"):
        filename = command.split(maxsplit=1)[1]  # get filename from command
        try:
            with open(filename, 'rb') as file:
                data = file.read()
            channel.sendall(data)
        except FileNotFoundError:
            channel.sendall(b"File not found")
    elif command.startswith("put"):
        filename = command.split(maxsplit=1)[1]  # get filename from command
        with open(filename, 'wb') as file:
            while True:
                data = channel.recv(1024)
                if not data:
                    break  # no more data to write
                file.write(data)
        channel.sendall(b"File received successfully")
    elif command == "exit":
        channel.sendall(b"Exiting.")
        channel.close()
    else:
        channel.sendall(b"Invalid command")


def signal_handler(sig, frame):
    logging.info('Shutting down server...')
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    logging.info(f"Listening for connections on {HOST}:{PORT}...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            logging.info(
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
                logging.error("No channel. Closing transport.")
                transport.close()
                continue

            handle_command(channel)
            transport.close()
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
