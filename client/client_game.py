from shared.game_entities import *


class ClientGame:
    def __init__(self, network, ui):
        self.is_selecting_move = None
        self.network = network
        self.ui = ui
        self.board = None

        self.players = {}

        # local player info
        self.local_player_id = network.player_id
        print(f"Local player ID in ClientGame: {self.local_player_id}")  # Debugging print
        self.game_started = False
        self.local_location = None
        self.local_turn_number = None
        self.current_turn_number = None

    def update_data(self):
        server_data = self.network.receive()
        if server_data:
            try:
                # Attempt to decode JSON data
                parsed_data = json.loads(server_data)
                print("server data is: {}".format(parsed_data))
                # Process different types of JSON data
                if 'players_data' in parsed_data:
                    self.update_players(parsed_data['players_data'])

                if 'game_start' in parsed_data:
                    self.game_started = True

                if 'current_turn_number' in parsed_data:
                    self.current_turn_number = parsed_data['current_turn_number']

                # Add more conditions here for other types of JSON keys

            except json.JSONDecodeError as e:
                print(f"Error decoding server data: {e}")

    def update_players(self, data):
        for player_info in data:
            print(f"player info: {player_info}")
            player_id = player_info.get('player_id')
            self.players[player_id] = player_info

            if player_id == self.network.player_id:
                self.local_location = player_info.get('current_location')
                self.local_turn_number = player_info.get('turn_number')

    def send_start_game_to_server(self):
        start_game_message = json.dumps({'action': 'start_game'})
        self.network.send(start_game_message)

    def handle_move_action(self):
        if self.current_turn_number == self.local_turn_number:
            valid_moves = self.get_valid_moves()
            self.ui.board_panel.notification_box.add_message(f"valid moves: {valid_moves}")
        else:
            print("It's not your turn.")

    def send_move_to_server(self, selected_move):
        # Format the move as a message (e.g., a JSON object)
        move_message = json.dumps({'action': 'move', 'move': selected_move})
        self.network.send(move_message)

        # Reset the move selection state
        self.is_selecting_move = False

    def get_valid_moves(self):
        # Start with an empty list of valid moves
        valid_moves_coords = []

        # Check if the current location is a room
        if self.is_room(self.local_location):
            # If in a room, add adjacent unblocked hallways to the valid moves
            valid_moves_coords.extend(self.get_adjacent_hallways(self.local_location))

            # Check for a secret passage and add its destination if available
            if self.has_secret_passage(self.local_location):
                valid_moves_coords.append(self.get_opposite_room(self.local_location))

        # If the current location is not a room, it must be a hallway
        else:
            # Add adjacent rooms to the valid moves
            valid_moves_coords.extend(self.get_adjacent_rooms(self.local_location))

        # Translate coordinates to room names
        valid_moves_names = [self.get_room_name_from_coords(coords) for coords in valid_moves_coords]
        return [name for name in valid_moves_names if name is not None]

    def get_room_name_from_coords(self, coords):
        for room_name, room_coords in ROOM_COORDS.items():
            if coords == room_coords:
                return room_name
        return None  # Return None if no match is found

    def is_room(self, location):
        # Iterate through all room coordinates
        for room_coords in ROOM_COORDS.values():
            if location == room_coords:
                return True
        return False

    def get_adjacent_hallways(self, room_location):
        adjacent_hallways = []

        # Define offsets to find adjacent hallways
        # These offsets represent the relative positions of the adjacent hallways
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right relative to the room

        for dx, dy in offsets:
            hallway_location = (room_location[0] + dx, room_location[1] + dy)

            # Check if the hallway location is valid (within the bounds of the 5x5 board)
            if self.is_valid_hallway(hallway_location) and not self.is_hallway_occupied(hallway_location):
                adjacent_hallways.append(hallway_location)

        return adjacent_hallways

    def is_valid_hallway(self, location):
        # Check if the location is within the 5x5 board and not a room
        max_coord = 4  # Maximum coordinate value for a 5x5 grid
        x, y = location

        if 0 <= x <= max_coord and 0 <= y <= max_coord and location not in ROOM_COORDS.values():
            return True
        return False

    def is_hallway_occupied(self, location):
        # Iterate through all players
        for player in self.players:
            # Check if any player's current location matches the hallway location
            if player.current_location == location:
                return True  # Hallway is occupied
        return False  # Hallway is not occupied

    def get_adjacent_rooms(self, hallway_location):
        adjacent_rooms = []

        # Logic to determine adjacent rooms to the hallway
        # This will depend on the specifics of your board layout
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Potential adjacent room positions

        for dx, dy in offsets:
            room_location = (hallway_location[0] + dx, hallway_location[1] + dy)

            if room_location in ROOM_COORDS.values():
                adjacent_rooms.append(room_location)

        return adjacent_rooms

    def has_secret_passage(self, room_location):
        # Define rooms with secret passages
        rooms_with_passages = [ROOM_COORDS[KITCHEN], ROOM_COORDS[CONSERVATORY],
                               ROOM_COORDS[STUDY], ROOM_COORDS[LOUNGE]]

        return room_location in rooms_with_passages

    def get_opposite_room(self, room_location):
        # Map of secret passages between rooms
        secret_passage_map = {
            ROOM_COORDS[KITCHEN]: ROOM_COORDS[STUDY],
            ROOM_COORDS[STUDY]: ROOM_COORDS[KITCHEN],
            ROOM_COORDS[CONSERVATORY]: ROOM_COORDS[LOUNGE],
            ROOM_COORDS[LOUNGE]: ROOM_COORDS[CONSERVATORY]
        }

        return secret_passage_map.get(room_location, None)

    def send_player_action(self, action):
        """
        Send a player action to the server.
        """
        try:
            # Serialize the action into JSON or another format
            action_data = json.dumps(action)
            print(f"action data send to server: {action_data}")
            self.network.send(action_data)
        except TypeError as e:
            print(f"Error serializing action data: {e}")
