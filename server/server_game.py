import json
import random
from shared.game_constants import *
from shared.game_entities import Board, Room, Card


class ServerGame:
    def __init__(self):
        self.solution = None
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

            # Prepare and send the hand to the player
            hand_info = {
                'player_info': self.players[player_id]['info'],  # General player info
                'hand': [card.to_dict() for card in player_hand]  # Player's hand of cards
            }
            self.send_to_player(player_id, json.dumps(hand_info))  # Serialize and send player info and cards

    def process_client_action(self, data):
        pass

    def add_player(self, player_id, player_info):
        if player_id not in self.players:
            if len(self.players) < 6:  # Assuming a maximum of 6 players
                # Filter out characters that have already been assigned
                assigned_characters = [player['info']['character'] for player in self.players.values()]
                available_characters = [s for s in SUSPECTS if s not in assigned_characters]

                if not available_characters:
                    print("No more characters available to assign.")
                    return

                character = random.choice(available_characters)
                player_info['character'] = character

                self.players[player_id] = {
                    'info': player_info,
                    'hand': [],
                    'position': STARTING_POSITIONS[character],
                    'in_game': True,
                }
                print(f"Player {player_id} added as {character} starting at {STARTING_POSITIONS[character]}")
            else:
                print("Maximum player limit reached.")
        else:
            print(f"Player {player_id} is already in the game.")

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
        if len(self.players) >= 3:  # Ensuring minimum players for Clue
            self.prepare_solution()  # Method to select and set aside the solution cards
            self.deal_cards()  # Deal the remaining cards to players
        # Other game start logic here
            print("Game has started.")
        else:
            print("Not enough players to start the game.")

    def prepare_solution(self):
        # Randomly select one card of each type for the solution
        solution_suspect = random.choice([card for card in self.deck if card.card_type == 'Suspect'])
        solution_weapon = random.choice([card for card in self.deck if card.card_type == 'Weapon'])
        solution_room = random.choice([card for card in self.deck if card.card_type == 'Room'])

        # Remove the selected cards from the deck
        self.deck.remove(solution_suspect)
        self.deck.remove(solution_weapon)
        self.deck.remove(solution_room)

        # Set aside the solution (you can store it in a variable)
        self.solution = (solution_suspect, solution_weapon, solution_room)
        print(f"Solution prepared: {self.solution}")

    def send_game_data(self):
        # Generate common game state metadata
        metadata = self.generate_metadata()
        metadata_json = json.dumps({'metadata': metadata})

        # Iterate over all players to send them their specific data and the metadata
        for player_id, player in self.players.items():
            # Player-specific hand data
            hand_data = {
                'hand': [card.to_dict() for card in player['hand']]  # Player's hand of cards
            }
            hand_data_json = json.dumps(hand_data)

            # Send the hand data and metadata to the player
            self.send_to_player(player_id, hand_data_json)
            self.send_to_player(player_id, metadata_json)

    def generate_metadata(self):
        # Example implementation
        metadata = {
            'board': self.board.encode()  # Assuming this returns the board's layout in JSON format
            # Include other relevant game state data here
        }
        return metadata

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
