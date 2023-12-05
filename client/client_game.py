import json

from shared.game_entities import *


class ClientGame:
    def __init__(self, network, ui):
        self.is_selecting_move = False
        self.network = network
        self.ui = ui
        self.players = {}
        # local player info
        self.game_started = False
        self.current_turn_number = None
        self.local_player_id = None
        self.local_turn_number = None
        self.local_location = None

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
                print(f"Local player ID in ClientGame: {player_id}")
                self.local_player_id = player_id
                self.local_turn_number = player_info.get('turn_number')
                self.local_location = player_info.get('current_location')

    def send_start_game_to_server(self):
        action_data = {'action': 'start_game'}
        self.send_player_action(action_data)

    def handle_move_action(self):
        self.is_selecting_move = True
        self.get_valid_moves()

    def send_move_to_server(self, coord):
        action_data = {'action': 'move', 'move_coord': coord}
        self.send_player_action(action_data)
        self.is_selecting_move = False

    def get_valid_moves(self):
        print(f"local_location: {self.local_location}")
        # Start with an empty list of valid moves
        valid_moves_coords = []

        # Check if the current location is a room
        if self.is_room():
            # If in a room, add adjacent unblocked hallways to the valid moves
            valid_moves_coords.extend(self.get_adjacent_locations())

            # Check for a secret passage and add its destination if available
            if self.has_secret_passage():
                valid_moves_coords.append(self.get_opposite_room())

        # If the current location is not a room, it must be a hallway
        else:
            # Add adjacent rooms to the valid moves
            print(f"valid_moves_coords before: {valid_moves_coords}")
            valid_moves_coords.extend(self.get_adjacent_locations())
            print(f"valid_moves_coords after: {valid_moves_coords}")

        # change room highlight variable to true

        valid_moves_names = [ROOM_COORDS.get(coords) for coords in valid_moves_coords]
        self.ui.notification_box.add_message(f"valid moves: {valid_moves_names}")
        self.ui.highlight_valid_moves(valid_moves_coords)

        return valid_moves_coords

    def get_adjacent_locations(self):
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        valid_locations = []
        print(f"start the offset")
        for dx, dy in offsets:
            print(f"dx = {dx}, dy = {dy}, local_location = {self.local_location}")

            x = self.local_location[0] + dx
            y = self.local_location[1] + dy
            print(f"x = {x}, y = {y}")
            if x < 0 or x == 5 or y < 0 or y == 5:
                print(f"out of boundary")
                continue
            adjacent_location = (x, y)
            print(f"adjacent_location: {adjacent_location}")

            print(f"room_coords: {ROOM_COORDS.keys()}")
            if tuple(self.local_location) in ROOM_COORDS.keys():
                print(f"location is in room")
                if adjacent_location in HALLWAYS_COORDS.keys() and not self.is_hallway_occupied(adjacent_location):
                    valid_locations.append(adjacent_location)
                    print(f"valid_locations after add valid hallway: {valid_locations}")
            else:
                print(f"location is in hallway")
                if adjacent_location in ROOM_COORDS.keys():
                    print(f"valid_locations before add valid room: {valid_locations}")
                    valid_locations.append(adjacent_location)
                    print(f"valid_locations after add valid rooms: {valid_locations}")

        print(f"return valid moves list: {valid_locations}")
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

    def get_opposite_room(self):
        # Map of secret passages between rooms
        secret_passage_map = {
            (4, 4): (0, 0),  # Kitchen to Study
            (0, 0): (4, 4),  # Study to Kitchen
            (4, 0): (0, 4),  # Conservatory to Lounge
            (0, 4): (4, 0)  # Lounge to Conservatory
        }
        return secret_passage_map.get(self.local_location, None)

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
        print(f"send picked room to server")
        self.send_move_to_server(coord)
        self.ui.reset_room_highlight()

    def handle_suggestion_action(self):
        pass

    def handle_accusation_action(self):
        pass
