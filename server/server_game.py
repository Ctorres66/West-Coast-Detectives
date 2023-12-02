import json
import random
from shared.game_constants import *
from shared.game_entities import Card, Player


class ServerGame:
    def __init__(self, clients):
        self.current_turn_index = 1
        self.player_order = None
        self.deck = []
        self.initialize_deck()  # shuffle cards to initialize deck
        self.solution = None
        self.clients = clients  # Dictionary, <player_id, conn>
        self.players = {}  # Dictionary to keep track of player states, <player_id, player info>

    def broadcast(self, message):
        # Assuming this method sends the message to all connected clients
        for client in self.clients.values():
            try:
                print(f"message: {message}")
                client.sendall(message.encode())
            except Exception as e:
                print(f"Error broadcasting to client: {e}")

    def start_game(self):
        # Shuffle and assign characters and starting positions to players
        self.assign_characters_and_positions()

        # Prepare the solution and deal cards
        self.prepare_solution()
        self.deal_cards()

        player_data = self.encode_players()
        start_game_data = {
            "players_data": player_data,
            "game_start": True,
            "current_turn_number": self.current_turn_index
        }
        self.broadcast(json.dumps(start_game_data, indent=4))

    def update_game_state(self):
        updated_state = self.encode_players()
        self.broadcast(json.dumps(updated_state, indent=4))

    def next_player_turn(self):
        while True:
            # Increment the turn number
            self.current_turn_index = (self.current_turn_index % len(self.players)) + 1
            # Get the player ID corresponding to the current turn number
            current_player_id = self.get_player_id_by_turn(self.current_turn_index)
            # Check if the player is still active (i.e., hasn't quit the game)
            if current_player_id in self.players:
                # Found an active player, broadcast whose turn it is
                self.broadcast(f"It's now player {current_player_id}'s turn.")
                break  # Exit the loop as we have found the next player

    def get_player_id_by_turn(self, turn_number):
        for player_id, player in self.players.items():
            if player.turn_number == turn_number:
                return player_id
        return None

    def add_player(self, player_id):
        turn_number = len(self.players) + 1  # Assign turn number based on the order of joining
        player = Player(player_id, character=None, current_location=None, turn_number=turn_number)
        print(f"turn number is {turn_number}")
        self.players[player_id] = player

    def assign_characters_and_positions(self):
        player_ids = list(self.players.keys())
        random.shuffle(player_ids)

        for player_id, suspect in zip(player_ids, SUSPECTS):
            self.players[player_id].character = suspect
            self.players[player_id].current_location = STARTING_POSITIONS[suspect]

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

    def deal_cards(self):
        # Shuffle the deck
        random.shuffle(self.deck)

        # Distribute the cards evenly among players
        player_ids = list(self.players.keys())
        while len(self.deck) > 0:
            for player_id in player_ids:
                if len(self.deck) == 0:
                    # Break the loop if there are no more cards to deal
                    break

                # Take the top card from the deck
                card = self.deck.pop(0)

                # Append the card to the player's hand
                self.players[player_id].cards.append(card)

    def encode_players(self):
        player_data = []
        for player in self.players.values():
            player_dict = player.to_dict()
            print(f"Player data: {player_dict}")  # Debugging print
            player_data.append(player_dict)
        return player_data

    def remove_player(self, player_id):
        # Remove a player from the game
        if player_id in self.players:
            del self.players[player_id]
            self.broadcast(f"Player {player_id} has left the game.")

    # player move logic
    def handle_move_action(self, player_id, move):
        print(f"move info: {move} ")
        # Check if the move is valid
        if move in ROOMS:  # Assuming move is the name of a room
            print(f"move infos: {move} ")
            new_position = ROOM_COORDS[move]
            self.players[player_id].current_location = new_position
            self.update_game_state()  # Broadcast the updated game state
        else:
            # Handle invalid move (e.g., send error message to player)
            pass
