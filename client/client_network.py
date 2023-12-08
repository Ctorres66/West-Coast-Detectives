import select
import socket


class ClientNetwork:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (self.server_ip, self.port)
        self.player_id = None
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            local_ip, local_port = self.client.getsockname()
            self.player_id = f"{local_ip}:{local_port}"
        except socket.error as e:
            print(f"Connection error: {e}")

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            print(f"Sending error: {e}")

    def receive(self, bufsize=4096):
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
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
