import json
import random
from shared.game_constants import *
from shared.game_entities import Board, Room, Card, Player


class ServerGame:
    def __init__(self):
        self.game_started = False
        self.deck = []
        self.initialize_deck()  # shuffle cards to initialize deck
        self.solution = None
        self.board = Board(5, 5)  # Assuming a 5x5 grid for the game board
        self.initialize_board()
        self.encoded_board = self.board.encode()
        self.players = {}  # Dictionary to keep track of player states, <player_id, player info>
        self.players_data = []

    def add_player(self, player_id, conn):
        player = Player(player_id, character=None, current_location=None, cards=[])
        self.players[player_id] = player

        conn.sendall(str.encode(self.encoded_board))
        print(f"send data to client here: {self.encoded_board}")
        if len(self.players) >= 3:  # shall begin
            self.game_started = True

    def start_game(self, clients):
        # Shuffle and assign characters and starting positions to players
        self.assign_characters_and_positions()

        # Prepare the solution and deal cards
        self.prepare_solution()
        self.deal_cards()

        encoded_player_data = self.encode_players()
        for player_id in clients:
            clients[player_id].sendall(str.encode(encoded_player_data))

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
                if len(self.deck) > 0:
                    # Take the top card from the deck
                    card = self.deck.pop(0)

                    # Append the card to the player's hand
                    self.players[player_id].cards.append(card)

    def initialize_board(self):
        # Initialize rooms on the board using the ROOMS constant
        for room_name in ROOMS:
            # Use the room name to construct the image filename dynamically
            image_filename = f"{room_name.replace(' ', '_')}.png"
            # Get the coordinates for the room from the Board instance
            coords = ROOM_COORDS[room_name]
            # Create a Room instance
            room = Room(room_name, image_filename)
            # Add the room to the board at the specified coordinates
            self.board.add_room(room, *coords)

    def encode_players(self):
        # Create a dictionary representation of the player
        player_data = {
            'players': []
        }
        for player in self.players.values():
            player_data.get('players').append(
                player.to_dict()
            )
        # Convert the dictionary to a JSON string
        return json.dumps(player_data)

    def remove_player(self, player_id):
        # Remove a player from the game
        if player_id in self.players:
            del self.players[player_id]
            self.broadcast(f"Player {player_id} has left the game.")

    def broadcast(self, message):
        # Send a message to all players
        pass

    def update_game_state(self):
        # Update the game state based on player actions
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

    def send_valid_moves(self, player_id):
        valid_moves = self.get_valid_moves(player_id)
        move_data = {
            'valid_moves': valid_moves
        }
        self.send_to_player(player_id, json.dumps(move_data))

    def handle_move_action(self, player_id, action):
        valid_moves = self.get_valid_moves(player_id)
        requested_move = action['target']  # Assuming 'target' holds the desired move location

        if requested_move in valid_moves:
            # Update player position. This should handle both room and hallway moves
            self.players[player_id]['position'] = self.get_position_from_target(requested_move)
            self.update_game_state()  # Broadcast the new game state
        else:
            error_message = f"Invalid move. You cannot move to {requested_move}."
            self.send_to_player(player_id, json.dumps({'error': error_message}))

    def get_position_from_target(self, target):
        # Check if the target is a room name
        if target in self.board.room_coords:
            return self.board.get_coords_for_room(target)

        # If the target is not a room, it could be a hallway.
        # Assuming hallways are represented by their grid coordinates (x, y)
        elif isinstance(target, tuple) and len(target) == 2:
            x, y = target
            if 0 <= x < self.board.rows and 0 <= y < self.board.cols:
                return x, y

        # If the target is neither a valid room nor a valid hallway coordinate, return None or handle it appropriately
        else:
            return None

    def get_valid_moves(self, player_id):
        player_position = self.players[player_id]['position']
        valid_moves = []

        if self.is_in_room(player_position):
            # Check adjacent hallways
            valid_moves.extend(self.get_adjacent_hallways(player_position))
            if self.is_corner_room(player_position):
                valid_moves.append(self.get_diagonal_room(player_position))
        else:
            # If the player is not in a room, they must be in a hallway, so check for adjacent rooms
            valid_moves.extend(self.get_accessible_rooms(player_position))

        return valid_moves

    def is_in_room(self, position):
        # Check if the position corresponds to a room
        # position should be a tuple (x, y) representing coordinates on the board
        if not isinstance(position, tuple) or len(position) != 2:
            return False

        # Iterate through the room coordinates to check if the position matches any of them
        for room_coords in self.board.room_coords.values():
            if position == room_coords:
                return True

        return False

    def is_corner_room(self, position):
        # Define the coordinates for the four corner rooms
        corner_rooms = [
            self.board.room_coords[KITCHEN],  # Bottom-right corner
            self.board.room_coords[CONSERVATORY],  # Bottom-left corner
            self.board.room_coords[STUDY],  # Top-left corner
            self.board.room_coords[LOUNGE]  # Top-right corner
        ]

        return position in corner_rooms

    def get_adjacent_hallways(self, room_position):
        adjacent_hallways = []

        # Calculate potential adjacent hallways based on the room's position
        # Assuming hallways are directly adjacent to rooms (i.e., one step north, south, east, or west)
        potential_hallways = [
            (room_position[0] - 1, room_position[1]),  # North
            (room_position[0] + 1, room_position[1]),  # South
            (room_position[0], room_position[1] - 1),  # West
            (room_position[0], room_position[1] + 1)  # East
        ]

        # Filter out hallways that are outside the board or occupied
        for hallway in potential_hallways:
            if self.is_valid_hallway(hallway) and not self.is_hallway_occupied(hallway):
                adjacent_hallways.append(hallway)

        return adjacent_hallways

    def is_valid_hallway(self, position):
        # Check if the position is within the board's boundaries and is a hallway
        x, y = position
        return 0 <= x < self.board.rows and 0 <= y < self.board.cols and self.is_in_hallway(position)

    def is_hallway_occupied(self, hallway_position):
        # Check if any player is currently in the given hallway
        return any(player['position'] == hallway_position for player in self.players.values())

    def get_accessible_rooms(self, hallway_position):
        accessible_rooms = []

        # Calculate potential accessible rooms based on the hallway's position
        potential_rooms = [
            (hallway_position[0] - 1, hallway_position[1]),  # North
            (hallway_position[0] + 1, hallway_position[1]),  # South
            (hallway_position[0], hallway_position[1] - 1),  # West
            (hallway_position[0], hallway_position[1] + 1)  # East
        ]

        # Filter out positions that are outside the board or not rooms
        for room_pos in potential_rooms:
            if self.is_valid_room_position(room_pos):
                accessible_rooms.append(room_pos)

        return accessible_rooms

    def is_valid_room_position(self, position):
        # Check if the position is within the board's boundaries and is a room
        x, y = position
        return 0 <= x < self.board.rows and 0 <= y < self.board.cols and self.is_in_room(position)

    def get_diagonal_room(self, corner_room_position):
        # Define the diagonal relationships between corner rooms
        diagonal_pairs = {
            self.board.room_coords[KITCHEN]: self.board.room_coords[STUDY],  # Bottom-right to top-left
            self.board.room_coords[CONSERVATORY]: self.board.room_coords[LOUNGE],  # Bottom-left to top-right
            self.board.room_coords[STUDY]: self.board.room_coords[KITCHEN],  # Top-left to bottom-right
            self.board.room_coords[LOUNGE]: self.board.room_coords[CONSERVATORY]  # Top-right to bottom-left
        }

        # Return the diagonally opposite room's coordinates
        return diagonal_pairs.get(corner_room_position)

    def move_player(self, player_id, new_position):
        pass
