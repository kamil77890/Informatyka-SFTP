import socket
import paramiko
import argparse


class SSHServer(paramiko.ServerInterface):
    def __init__(self, args) -> None:
        self.username = args.user
        self.password = args.pwd
        super().__init__()

    def check_auth_password(self, username, password):
        if username == self.username:
            # if password is present then check it, if not then don't bother
            if self.password:
                if password == self.password:
                    return paramiko.AUTH_SUCCESSFUL
                return paramiko.AUTH_FAILED
            return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True


def handle_command(channel):
    while not channel.closed:
        channel.settimeout(None)
        command = channel.recv(1024).decode('utf-8').strip()
        if command == "":
            print("Invalid Command")
        process_command(command, channel)

    channel.close()


def process_command(command, channel):
    parts = command.split()
    if not parts:
        return
    cmd = parts[0]
    if cmd == "echo":
        response = ' '.join(parts[1:])
        channel.sendall(response.encode('utf-8'))
    elif cmd == "get":
        filename = parts[1]
        with open(filename, 'rb') as file:
            data = file.read()
            print(data)
        channel.sendall(data)

    elif cmd == "put":
        filename = parts[1]
        with open(filename, 'wb') as file:
            while True:
                data = channel.recv(4096)
                if not data or data.endswith(b'\n'):
                    break
                file.write(data)
            channel.sendall("Udało się!")
    else:
        channel.sendall(b"Jestes glupi???")


def main(args):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((args.host, args.port))
    server_socket.listen(1)
    print(f"Server initialized on {args.host}:{args.port}")

    while True:
        client_socket, client_address = server_socket.accept()
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(paramiko.RSAKey.generate(2048))
        server = SSHServer(args)

        transport.start_server(server=server)

        channel = transport.accept(20)
        if channel is None:
            transport.close()
            continue

        handle_command(channel)
        transport.close()


if __name__ == "__main__":
    """
    SFTP server args:
      -H / --host:
        Host address, by default set to localhost. (Optional)
      -p / --port:
        Host port, by default set to 22. (Optional)
      -u / --user
        FTP username. (Required)
      -P / --pwd
        FTP password. (Optional)
    """
    parser = argparse.ArgumentParser(prog='SFTP_Server', description='SFPT Server made in Python')
    parser.add_argument('-H','--host',type=str,required=False,default="localhost")
    parser.add_argument('-p','--port',type=int,required=False,default=22)
    parser.add_argument('-u','--user',type=str,required=True)
    parser.add_argument('-P','--pwd',type=str,required=False)
    args = parser.parse_args()
    print("Custom SFTP server - by kamil77980 & bambus80")
    main(args)
