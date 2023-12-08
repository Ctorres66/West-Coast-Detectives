import json

from shared.game_entities import *


def get_location_name(coord):
    # First, try to get the name from ROOM_COORDS
    if coord in ROOM_COORDS:
        return ROOM_COORDS[coord]

    # If not found in ROOM_COORDS, try to get the name from HALLWAYS_COORDS
    return HALLWAYS_COORDS.get(coord)


class ClientGame:
    def __init__(self, network, ui):
        self.is_selecting_move = False
        self.is_accusing = False
        self.network = network
        self.ui = ui
        self.players = {}
        self.characters = {}    # Player_id, character
        # local player info
        self.game_started = False
        self.current_turn_number = None
        self.local_player_id = None
        self.local_turn_number = None
        self.local_location = None
        self.local_character = None
        self.skip_player = False
        self.valid_moves = None
        self.accusing_select = [None, None, None]

    def update_data(self):
        server_data = self.network.receive()
        if server_data:
            try:
                # Attempt to decode JSON data
                parsed_data = json.loads(server_data)
                print("server data is: {}".format(parsed_data))
                # Process different types of JSON data
                if 'game_start' in parsed_data:
                    self.game_started = True
                if 'current_turn_number' in parsed_data:
                    self.current_turn_number = parsed_data['current_turn_number']
                if 'players_data' in parsed_data:
                    self.update_players(parsed_data['players_data'])
                if 'game_end' in parsed_data:
                    winner_character = self.characters[parsed_data['winner']]
                    self.ui.notification_box.add_message(f"Winner is: {winner_character}")
                    self.game_started = False
                    # Add more conditions here for other types of JSON keys
            except json.JSONDecodeError as e:
                print(f"Error decoding server data: {e}")

    def update_players(self, data):
        for player_info in data:
            player_id = player_info.get('player_id')
            if player_id not in self.characters:
                self.characters[player_id] = player_info.get('character')
            # Convert current_location to a tuple if it's not already
            if player_info.get('current_location') is not None:
                player_info['current_location'] = tuple(player_info.get('current_location'))
            self.players[player_id] = player_info

            if player_id == self.network.player_id:
                print(f"Local player ID in ClientGame: {player_id}")
                self.local_location = player_info.get('current_location')
                if self.local_character is None:
                    self.local_character = player_info.get('character')
                    self.ui.notification_box.add_message(f"You are assigned to {self.local_character}")
                if self.local_player_id is None:
                    self.local_player_id = player_id
                if self.local_turn_number is None:
                    self.local_turn_number = player_info.get('turn_number')
                if self.players[player_id]['turn_number'] == self.current_turn_number:
                    if self.players[player_id]['loss_game']:
                        self.skip_player = True
                        action_data = {'action': 'skip_player'}
                        self.send_player_action(action_data)

    def send_start_game_to_server(self):
        action_data = {'action': 'start_game'}
        self.send_player_action(action_data)

    def handle_move_action(self):
        self.is_selecting_move = True
        self.valid_moves = self.get_valid_moves()

    def send_move_to_server(self, coord):
        action_data = {'action': 'move', 'move_coord': coord}
        self.send_player_action(action_data)

    def get_valid_moves(self):
        # Start with an empty list of valid moves
        valid_moves_coords = []

        # Check if the current location is a room
        if self.is_room():
            # Check for a secret passage and add its destination if available
            opposite_room = self.has_opposite_room()
            if opposite_room is not None:
                valid_moves_coords.append(opposite_room)
            # If in a room, add adjacent unblocked hallways to the valid moves
            valid_moves_coords.extend(self.get_adjacent_locations())

        # If the current location is not a room, it must be a hallway
        else:
            # Add adjacent rooms to the valid moves
            valid_moves_coords.extend(self.get_adjacent_locations())

        valid_moves_names = [get_location_name(coords) for coords in valid_moves_coords]
        self.ui.notification_box.add_message(f"valid moves: {valid_moves_names}")
        self.ui.highlight_valid_moves(valid_moves_coords)

        return valid_moves_coords

    def get_adjacent_locations(self):
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        valid_locations = []
        for dx, dy in offsets:
            x = self.local_location[0] + dx
            y = self.local_location[1] + dy
            if x < 0 or x == 5 or y < 0 or y == 5:
                continue
            adjacent_location = (x, y)

            if self.local_location in ROOM_COORDS.keys():
                if adjacent_location in HALLWAYS_COORDS.keys() and not self.is_hallway_occupied(adjacent_location):
                    valid_locations.append(adjacent_location)
            else:
                if adjacent_location in ROOM_COORDS.keys():
                    valid_locations.append(adjacent_location)
        return valid_locations

    def is_hallway_occupied(self, location):
        for row in self.ui.board.grid:
            for room in row:
                if room is not None and room.coord == location:
                    return room.occupied

    def has_secret_passage(self):
        # Define rooms with secret passages
        secret_passage_coords = [(4, 4), (4, 0), (0, 0), (0, 4)]  # Kitchen, Conservatory, Study, Lounge
        return self.local_location in secret_passage_coords

    def has_opposite_room(self):
        # Map of secret passages between rooms
        secret_passage_map = {
            (4, 4): (0, 0),  # Kitchen to Study
            (0, 0): (4, 4),  # Study to Kitchen
            (4, 0): (0, 4),  # Conservatory to Lounge
            (0, 4): (4, 0)  # Lounge to Conservatory
        }
        for secret_room in secret_passage_map.keys():
            if self.local_location == secret_room:
                return secret_passage_map.get(self.local_location)
        return None

    def is_room(self):
        # Iterate through all room coordinates
        for room_coords in ROOM_COORDS.keys():
            if self.local_location == room_coords:
                return True
        return False

    def send_player_action(self, action_data):
        """
        Send a player action to the server.
        """
        try:
            # Serialize the action data into JSON
            serialized_data = json.dumps(action_data)
            print(f"Sending to server: {serialized_data}")
            self.network.send(serialized_data)
        except TypeError as e:
            print(f"Error serializing action data: {e}")

    def handle_room_pick_action(self, coord):
        name = get_location_name(coord)
        self.ui.notification_box.add_message(f"Successfully moved to: {name}")
        self.send_move_to_server(coord)
        self.is_selecting_move = False
        self.ui.reset_room_highlight()

    def handle_suggestion_action(self):
        pass

    def handle_accusation_action(self, event):
        if not self.ui.handle_accusation_events(event):
            return
        # Ensure all selections are made
        if all(self.accusing_select):
            action_data = {
                'action': 'accusation',
                'suspect': self.accusing_select[0],
                'room': self.accusing_select[1],
                'weapon': self.accusing_select[2]
            }
            self.send_player_action(action_data)
            self.accusing_select = [None, None, None]  # Reset the selections
            self.is_accusing = False
