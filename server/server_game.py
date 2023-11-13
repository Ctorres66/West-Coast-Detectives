import random
from shared.game_constants import *
from shared.game_entities import Board, Room, Card


class ServerGame:
    def __init__(self):
        self.board = Board(5, 5)  # Assuming a 5x5 grid for the game board
        self.players = {}  # Dictionary to keep track of player states
        self.initialize_board()
        self.deck = []  # This will hold all the cards
        self.initialize_deck()

    def initialize_board(self):

        # Initialize rooms on the board using the ROOMS constant
        for room_name in ROOMS:
            # Use the room name to construct the image filename dynamically
            image_filename = f"{room_name.replace(' ', '_')}.png"
            # Get the coordinates for the room from the Board instance
            coords = self.board.get_coords_for_room(room_name)
            # Create a Room instance
            room = Room(room_name, image_filename)
            # Add the room to the board at the specified coordinates
            self.board.add_room(room, *coords)

    def initialize_deck(self):
        # Create suspect cards
        for suspect in SUSPECTS:
            self.deck.append(Card(SUSPECT, suspect))

        # Create weapon cards
        for weapon in WEAPONS:
            self.deck.append(Card(WEAPON, weapon))

        # Create room cards based on the ROOMS constant
        for room_name in ROOMS:
            self.deck.append(Card(ROOM, room_name))

    def deal_cards(self):
        # Shuffle the deck
        random.shuffle(self.deck)

        # Calculate the number of cards per player
        num_players = len(self.players)
        cards_per_player = len(self.deck) // num_players

        # Deal the cards
        for player_id in self.players:
            player_hand = self.deck[:cards_per_player]
            self.deck = self.deck[cards_per_player:]
            self.players[player_id]['hand'] = player_hand

            # Send the hand to the player
            self.send_to_player(player_id, player_hand)

    def process_client_action(self, data):
        pass

    def add_player(self, player_id, player_info):
        # Add a new player to the game
        pass

    def remove_player(self, player_id):
        # Remove a player from the game
        pass

    def broadcast(self, message):
        # Send a message to all players
        pass

    def send_to_player(self, player_id, message):
        # Send a message to a specific player
        pass

    def start_game(self):
        # Logic to start a new game
        self.deal_cards()
        pass

    def update_game_state(self):
        # Update the game state based on player actions
        pass

    def process_player_action(self, player_id, action):
        # Process an action taken by a player
        pass

    def check_win_condition(self):
        # Check if the win condition has been met
        pass

    def calculate_scores(self):
        # Calculate and update player scores
        pass

    def handle_incoming_data(self, data):
        # Handle data received from a player
        pass

    def disconnect_client(self, client_id):
        # Disconnect a client safely
        pass

    def shutdown(self):
        # Clean up and shut down the server game
        pass

# You can add more methods as needed for your game logic.
