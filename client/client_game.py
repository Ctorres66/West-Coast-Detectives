from shared.game_entities import *


class ClientGame:
    def __init__(self, network, ui):
        self.ui = ui
        self.network = network
        self.board = None

        self.players = {}

        # local player info
        self.local_player_id = network.addr
        self.local_character = None
        self.local_location = None

    def update_data(self):
        # Receive data from the server
        server_data = self.network.receive()
        if server_data:
            """
            Process the data received from the server.
            """
            try:
                parsed_data = json.loads(server_data)
                # Assuming the data from the server is in JSON format
                print("server data is: {}".format(server_data))

                if 'players_data' in parsed_data:
                    self.update_players(parsed_data)

            except json.JSONDecodeError as e:
                print(f"Error decoding server data: {e}")

    def update_players(self, data):
        for player_dict in data.get('players_data'):
            player_id = player_dict.get('player_id')
            character = player_dict.get('character')
            current_location = player_dict.get('current_location')
            cards = player_dict.get('cards', [])

            print(f"player info is: {character} and {current_location}")
            self.ui.update_players(character, current_location)

            if player_id == self.local_player_id:
                # Extract player information
                # local_character = character
                # local_location = current_location
                local_cards = cards

                self.ui.draw_local_player_cards(local_cards)

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
