import pygame
import json  # Assuming JSON is used for server communication
from shared.game_entities import Board, Room


class ClientGame:
    def __init__(self, network):
        self.network = network
        self.board = Board(5, 5)  # Assuming a 5x5 board for the game
        # self.player = Player()  # Uncomment and define Player class as needed

    def update(self):
        # Handle local game state updates that are not dependent on server data
        # e.g., animations, local player input, etc.
        self.update_local_state()

        # Receive data from the server
        server_data = self.network.receive()
        if server_data:
            # Interpret the data and update the game state accordingly
            self.process_server_data(server_data)

    def process_server_data(self, data):
        """
        Process the data received from the server.
        """
        try:
            # Assuming the data from the server is in JSON format
            print("server data is: {}".format(data))

            parsed_data = json.loads(data)

            # Here, we need to update our game state based on the received data
            # This will depend on the structure of the data sent from the server
            # For example, if the server sends a complete board state:
            self.update_board(parsed_data['board'])
        except json.JSONDecodeError as e:
            print(f"Error decoding server data: {e}")

    def update_board(self, board_data):
        # Update the board based on the received data
        # You will need to implement this depending on your game's logic
        # and the format of the board data
        pass

    def update_local_state(self):
        """
        Update the local state of the game.
        This could include animating sprites, handling local input, etc.
        """
        # For example, update animations here
        pass

    def send_player_action(self, action):
        """
        Send a player action to the server.
        """
        try:
            # Serialize the action into JSON or another format
            action_data = json.dumps(action)
            self.network.send(action_data)
        except TypeError as e:
            print(f"Error serializing action data: {e}")

    def handle_input(self, event):
        """
        Handle player input.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Example action
                self.send_player_action({'action': 'move', 'direction': 'up'})
            # Handle other keypresses and input events

        # You can also process mouse events, etc.

# More methods can be added for handling specific aspects of the game,
# like collision detection, player stats updates, and more.
