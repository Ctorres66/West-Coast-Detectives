import socket
from _thread import start_new_thread

from server_game import ServerGame
from shared.game_constants import PORT


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.game_engine = ServerGame()  # Assuming ServerGame is defined in server_game.py
        self.clients = {}  # Dictionary to keep track of clients

        try:
            self.server_socket.bind((self.host, self.port))
        except socket.error as e:
            print(f"Server binding error: {e}")
            exit()

        self.server_socket.listen()
        print(f"Server started on {self.host}:{self.port}. Waiting for connections...")

    def client_thread(self, conn, addr):
        print(f"Connected to: {addr}")

        # Generate a unique player ID
        # This can be a combination of address and a unique counter or timestamp
        player_id = f"{addr[0]}_{addr[1]}"

        # Gather player info. You might want to extend this with more relevant data.
        player_info = {'address': addr, 'id': player_id}

        # Check if the maximum number of players hasn't been exceeded
        if len(self.game_engine.players) < 6:  # Assuming a max of 6 players
            # Add the player to the game
            self.game_engine.add_player(player_id, player_info)
            print(f"Player {player_id} added to the game.")
        else:
            print("Maximum number of players reached. Connection refused.")
            conn.close()
            return

        # Send initial game state or welcome message
        conn.sendall(str.encode(self.game_engine.board.encode()))

        while True:
            try:
                data = conn.recv(2048).decode()
                if not data:
                    break  # Client disconnected

                # Process the data through the game engine and get a response
                response = self.game_engine.process_client_action(data)
                conn.sendall(str.encode(response))

            except Exception as e:
                print(f"Error with client {addr}: {e}")
                break

        # Remove client from dictionary and close connection
        print(f"Connection closed with {addr}")
        del self.clients[addr]
        conn.close()

    def run(self):
        while True:
            conn, addr = self.server_socket.accept()
            self.clients[addr] = conn
            start_new_thread(self.client_thread, (conn, addr))


if __name__ == "__main__":
    server = Server(socket.gethostname(), PORT)  # Use the correct host and PORT from your constants
    server.run()
