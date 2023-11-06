import socket


class ClientNetwork:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (self.server_ip, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
        except socket.error as e:
            print(f"Connection error: {e}")

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(f"Sending error: {e}")

    def receive(self, bufsize=2048):
        """
        Receive data from the server.
        :param bufsize: The maximum amount of data to be received at once.
        :return: Decoded data received from the server.
        """
        try:
            data = self.client.recv(bufsize).decode()
            return data
        except socket.error as e:
            print(f"Receiving error: {e}")
            return None