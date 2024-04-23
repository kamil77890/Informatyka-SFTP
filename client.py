import paramiko


def send_command(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    return stdout.read() + stderr.read()


def main():
    host = "127.0.0.1"  # Use the correct IP address or hostname of the server
    port = 222
    username = "abc"
    password = "def"

    # Create a new SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the server
        client.connect(hostname=host, port=port,
                       username=username, password=password)
        print("Connected to the server.")

        # Open an SSH transport
        transport = client.get_transport()
        session = transport.open_session()
        session.set_combine_stderr(True)
        session.get_pty()

        # Start the SSH session
        session.exec_command('bash')  # Start a bash shell
        print("Interactive SSH session started.")

        # Implement command sending here
        # For example, to download a file:
        command = 'get /somefile.txt'
        session.send(command + '\n')
        # Increase buffer size if file is larger
        file_content = session.recv(1024)
        print("Received file content:", file_content.decode())

        # For example, to upload a file:
        command = 'put /newfile.txt'
        session.send(command + '\n')
        session.send(b"Hello, this is the content of the new file.")
        session.shutdown_write()  # Indicate the end of file transfer

        response = session.recv(1024)  # Wait for server response
        print("Server response:", response.decode())

    except Exception as e:
        print(f"Failed to connect or error in file transfer: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
