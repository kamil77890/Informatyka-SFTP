import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import paramiko
from time import sleep
import os


def connect_to_server(host, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, port=port,
                       username=username, password=password)
        return client
    except Exception as e:
        messagebox.showerror("Connection Failed", str(e))
        return None


def send_command(client, operation, filepath):
    filename = os.path.basename(filepath)
    if client:
        shell = client.invoke_shell()
        if operation == "put":
            shell.send(f"put {filename}\n")
            sleep(1)
            with open(filepath, 'rb') as file:
                data = file.read()
                shell.send(data)
            shell.send(b"\n")
        elif operation == "get":
            shell.send(f"get {filename}\n")
            sleep(1)
            if shell.recv_ready():
                data = shell.recv(4096)
                save_path = os.path.join(os.path.dirname(
                    filepath), f"received_{filename}")
                with open(save_path, 'wb') as file:
                    file.write(data)
                messagebox.showinfo(
                    "Success", f"Received file {filename} and saved as {save_path}.")
        shell.close()


def main(host, port, username, password):
    client = connect_to_server(host, port, username, password)
    if client:
        messagebox.showinfo("Success", "Connected to the server.")

        operation = simpledialog.askstring(
            "Input", "Enter operation (put or get):")
        if operation in ["put", "get"]:
            filename = filedialog.askopenfilename(
            ) if operation == "put" else filedialog.asksaveasfilename()
            send_command(client, operation, filename)
        else:
            messagebox.showerror("Error", "Invalid operation.")
        client.close()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    main("localhost", 22, "abc", "def")
