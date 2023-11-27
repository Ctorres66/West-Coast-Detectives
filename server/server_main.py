import socket
import threading
from _thread import start_new_thread
from server_game import ServerGame
from shared.game_constants import PORT


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}
        self.game_engine = ServerGame(self.clients)
        self.game_started_event = threading.Event()
        self.game_started = False

        try:
            self.server_socket.bind((self.host, self.port))
        except socket.error as e:
            print(f"Server binding error: {e}")
            exit()
        print(f"Server initialized on {self.host}:{self.port}")

    def accept_connections(self):
        self.server_socket.listen(6)
        print("Waiting for connections...")
        while len(self.clients) < 6 and not self.game_started_event.is_set():
            conn, addr = self.server_socket.accept()
            player_id = f"{addr[0]}:{addr[1]}"
            print(f"Connected to: {addr}, Players: {len(self.clients) + 1}/6")
            self.clients[player_id] = conn
            self.game_engine.add_player(player_id)
            start_new_thread(self.client_thread, (conn, player_id))

    def client_thread(self, conn, player_id):
        print(f"Client {player_id} thread started.")
        while True:
            try:
                data = conn.recv(2048).decode()
                if not data:
                    break

                if data == "START_GAME":
                    self.game_engine.start_game(self.clients, player_id)

            except Exception as e:
                print(f"Error with client {player_id}: {e}")
                break

        self.cleanup_client_connection(player_id, conn)

    def run(self):
        try:
            self.accept_connections()

        except KeyboardInterrupt:
            print("Server shutdown requested by user. Cleaning up...")

            # Perform any necessary cleanup here
            self.cleanup()

            print("Server shut down successfully.")

    def cleanup(self):
        print("Initiating server cleanup.")

        # Close all active client connections
        for player_id, conn in self.clients.items():
            try:
                conn.close()
                print(f"Closed connection with {player_id}")
            except Exception as e:
                print(f"Error closing connection with {player_id}: {e}")

        # Close the server socket
        try:
            self.server_socket.close()
            print("Server socket closed.")
        except Exception as e:
            print(f"Error closing server socket: {e}")

        # Perform any additional cleanup if necessary
        # e.g., saving game state, releasing resources, etc.

    def cleanup_client_connection(self, player_id, conn):
        """
        Clean up after a client has disconnected.

        :param player_id: The ID of the player who has disconnected.
        :param conn: The socket connection associated with the player.
        """
        # Close the client's connection
        try:
            conn.close()
            print(f"Connection with player {player_id} closed.")
        except Exception as e:
            print(f"Error closing connection with player {player_id}: {e}")

        # Remove the player from the active clients list
        if player_id in self.clients:
            del self.clients[player_id]
            print(f"Player {player_id} removed from active clients.")

        # Update the game state to reflect the player's disconnection
        # This is dependent on how your game engine handles player disconnections
        self.game_engine.remove_player(player_id)

        # Any additional cleanup related to the player can be done here
        # For example, notify other players about the disconnection, adjust game state, etc.
        self.game_engine.broadcast(f"Player {player_id} has disconnected.")


if __name__ == "__main__":
    server = Server(socket.gethostname(), PORT)
    server.run()
