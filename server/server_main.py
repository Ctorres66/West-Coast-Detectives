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
        self.clients = {}  # Dictionary to keep track of clients, <player_id, conn>

        try:
            self.server_socket.bind((self.host, self.port))
        except socket.error as e:
            print(f"Server binding error: {e}")
            exit()

        self.server_socket.listen()
        print(f"Server started on {self.host}:{self.port}. Waiting for connections...")

    def client_thread(self, conn, player_id):
        print(f"Connected to: {player_id}")

        while True:
            try:
                data = conn.recv(2048).decode()
                if not data:
                    print(f"Client {player_id} has disconnected.")
                    break  # Client disconnected

                # Process received data
                # You'll need to implement this logic based on your game's requirements
                # response = self.process_client_action(player_id, data)
                #
                # # Send response back to the client
                # if response:
                #     conn.sendall(str.encode(response))

            except Exception as e:
                print(f"Error with client {player_id}: {e}")
                break  # Exit the loop in case of an error

        self.cleanup_client_connection(player_id, conn)

    def cleanup_client_connection(self, player_id, conn):
        """
        Clean up after a client has disconnected.

        :param player_id: The ID of the player who has disconnected.
        :param conn: The socket connection associated with the player.
        """
        # Close the connection
        conn.close()

        # Remove the player from the active clients list
        if player_id in self.clients:
            del self.clients[player_id]

        # Optionally, perform additional cleanup related to game state
        # For instance, if the game needs to be aware of player disconnections,
        # update the game state accordingly.
        self.game_engine.remove_player(player_id)

        # Log or print the disconnection
        print(f"Player {player_id} has disconnected and cleanup is complete.")

    # def process_client_action(self, action, player_id, conn):
    #     if action['type'] == 'start_game':
    #         self.game_engine.start_game(conn)
    #     elif action['type'] == 'add_player':
    #         self.game_engine.add_player(player_id, conn)

    # Handle other action types...

    def run(self):
        try:
            while True:
                conn, addr = self.server_socket.accept()
                player_id = addr

                if len(self.game_engine.players) < 6:  # Assuming a max of 6 players
                    self.game_engine.add_player(player_id)
                    print(f"Player {player_id} added to the game.")
                else:
                    print("Maximum number of players reached. Connection refused.")
                    conn.close()
                    continue  # Skip to the next iteration of the loop

                self.clients[player_id] = conn
                start_new_thread(self.client_thread, (conn, player_id))

                if self.game_engine.game_started:  # and someone need to press button to start game
                    self.game_engine.start_game(self.clients)

        except KeyboardInterrupt:
            print("Server shutdown requested by user. Cleaning up...")

            # Perform any necessary cleanup here
            self.cleanup()

            print("Server shut down successfully.")

    def cleanup(self):
        """
        Clean up the server resources before shutting down.
        """

        # Close all client connections
        for player_id, conn in self.clients.items():
            conn.close()
            print(f"Connection with player {player_id} closed.")

        # Close the server socket
        self.server_socket.close()
        print("Server socket closed.")

        # Optionally, perform additional cleanup tasks


if __name__ == "__main__":
    server = Server(socket.gethostname(), PORT)  # Use the correct host and PORT from your constants
    server.run()
