import select
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
        try:
            ready_to_read, _, _ = select.select([self.client], [], [], 0.5)
            if ready_to_read:
                data = self.client.recv(bufsize).decode()
                return data
            else:
                # The socket wasn't ready for reading.
                return None
        except socket.error as e:
            print(f"Receiving error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
