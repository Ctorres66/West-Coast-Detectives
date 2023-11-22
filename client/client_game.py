import json  # Assuming JSON is used for server communication

import pygame

from client.client_player import ClientPlayer
from shared.game_entities import Board, Card


class ClientGame:
    def __init__(self, network):
        self.ui = None
        self.network = network
        self.board = None

        self.players = {}

        # local player info
        self.player_id = network.addr
        self.current_location = None
        self.cards = None

    def update(self):
        # Handle local game state updates that are not dependent on server data
        # e.g., animations, local player input, etc.
        self.update_local_state()

        # Receive data from the server
        server_data = self.network.receive()
        print(f"print out server_data: {server_data}")

        if server_data:
            # Interpret the data and update the game state accordingly
            self.process_server_data(server_data)

    def process_server_data(self, data):
        """
        Process the data received from the server.
        """
        try:
            parsed_data = json.loads(data)
            # Assuming the data from the server is in JSON format
            print("server data is: {}".format(data))

            # Add conditions as needed based on the data structure sent by the server
            if 'metadata' in parsed_data:
                self.update_board(parsed_data)

            if 'players' in parsed_data:
                self.update_players(parsed_data)

        except json.JSONDecodeError as e:
            print(f"Error decoding server data: {e}")

    def update_board(self, data):
        # Initialize the board if the response contains metadata
        if data.get('metadata') is not None:
            self.board = Board(rows=None, cols=None, dict_data=data)

    def update_players(self, data):
        for player_dict in data.get('players'):

            # Extract player information
            player_id = player_dict.get('player_id')
            current_location = player_dict.get('current_location')
            cards = player_dict.get('cards', [])

            # Create a single ClientPlayer object for the local player if not already exists
            if self.player_id not in self.players:
                self.players[self.player_id] = ClientPlayer(player_id=self.player_id)

            # Update the existing player object or create a new one if the player doesn't exist
            player = self.players.get(player_id)
            if not player:
                player = ClientPlayer(player_id=player_id)
                self.players[player_id] = player

            # Update the player's information
            player.current_location = current_location
            player.cards = cards

            # Update the local player's data if it's the current player
            if player_id == self.player_id:
                self.current_location = current_location
                self.cards = cards

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
            # Handle other key presses and input events

        # You can also process mouse events, etc.

    def receive_card_data(self, card_data):
        """
        Receive and process card data from the server.

        :param card_data: A list of dictionaries, each representing a card
        """
        # Create Card objects from the received data
        self.hand = [Card(**card_info) for card_info in card_data]

        # Print details of each card in the hand
        print("Received cards:")
        for card in self.hand:
            print(card)  # This will use the __str__ or __repr__ method of Card

        # Notify the UI to update the display
        # This assumes you have a reference to the ClientUI instance
        # Make sure the ClientUI has an update_hand method implemented
        self.ui.update_hand(self.hand)
