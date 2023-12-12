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
        self.is_suggesting = False
        self.has_moved = False
        self.has_suggested = False
        self.has_accused = False

        self.network = network
        self.ui = ui
        self.players = {}
        self.characters = {}  # Player_id, character
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
        self.suggesting_select = [None, None, None]

    def update_data(self):
        server_data = self.network.receive()
        if server_data:
            try:
                # Attempt to decode JSON data
                print(f"parsed_data: {json.loads(server_data)}")

                parsed_data = json.loads(server_data)
                print("server data is: {}".format(parsed_data))
                # Process different types of JSON data
                if 'start_game' in parsed_data:
                    self.game_started = True
                    self.ui.notification_box.add_message("Game Start!")
                    start_game_data = parsed_data['start_game']
                    self.current_turn_number = start_game_data['current_turn_number']
                    self.update_players(start_game_data['players_data'], True)

                if 'update_game_data' in parsed_data:
                    update_game_data = parsed_data['update_game_data']
                    self.current_turn_number = update_game_data['current_turn_number']
                    self.update_players(update_game_data['players_data'], False)

                if 'winner' in parsed_data:
                    print(f"winner: {parsed_data['winner']}")
                    print(f"self.characters: {self.characters}")
                    winner_character = self.characters[parsed_data['winner']]
                    self.ui.notification_box.add_message(f"Winner is: {winner_character}!! Game End")
                    self.game_started = False

                if 'loser' in parsed_data:
                    print(f"self.characters: {self.characters}")
                    loser_character = self.characters[parsed_data['loser']]
                    self.ui.notification_box.add_message(f"Incorrect accusation! {loser_character} has lost the game.")
                if 'who_suggest' in parsed_data:
                    who_suggest = self.characters[parsed_data['who_suggest']]
                    suggesting_select = parsed_data['suggest_what']
                    self.ui.notification_box.add_message(f" Player {who_suggest} made "
                                                         f"the suggestion {suggesting_select}. Waiting for disprove...")
                if 'card_you_suggest' in parsed_data:
                    card_info = parsed_data['card_you_suggest']
                    print(f"card_you_suggest: {card_info['card']}, {card_info['suggest_id']}.")
                    player_is_suggesting = self.characters[card_info['suggest_id']]
                    card = card_info['card']

                    self.ui.notification_box.add_message(f"Your can disprove the suggestion with "
                                                         f"{card} to {player_is_suggesting}.")

                if 'suggested_cards' in parsed_data:
                    cards_data = parsed_data['suggested_cards']
                    print(f"suggested_cards: {cards_data}")
                    if cards_data:
                        for player_id, card_info in cards_data.items():
                            character = self.characters[player_id]
                            self.ui.notification_box.add_message(
                                f"Your suggestion '{card_info}' is disproved by Player {character}.")

                    else:
                        self.ui.notification_box.add_message("No one could disprove the suggestion.")

                # Add more conditions here for other types of JSON keys
                if self.game_started and not self.skip_player:
                    self.whose_turn()
            except json.JSONDecodeError as e:
                print(f"Error decoding server data: {e}")

    def update_players(self, data, start_data):
        for player_info in data:
            player_id = player_info.get('player_id')

            if start_data and player_id not in self.characters.keys():
                self.characters[player_id] = player_info.get('character')
                print(f"self.characters: {self.characters}")

            # Convert current_location to a tuple if it's not already
            if player_info.get('current_location') is not None:
                player_info['current_location'] = tuple(player_info.get('current_location'))
            self.players[player_id] = player_info

            if player_id == self.network.player_id:
                print(f"Local player ID in ClientGame: {player_id}")
                self.local_location = player_info.get('current_location')
                if start_data and self.local_character is None:
                    self.local_character = player_info.get('character')
                    self.ui.notification_box.add_message(f"You are assigned to {self.local_character}")
                if start_data and self.local_player_id is None:
                    self.local_player_id = player_id
                if start_data and self.local_turn_number is None:
                    self.local_turn_number = player_info.get('turn_number')

    def send_start_game_to_server(self):
        action_data = {'action': 'start_game'}
        self.send_player_action(action_data)

    def handle_move_action(self):
        self.is_selecting_move = True
        self.ui.notification_box.add_message("Please select your move.")
        self.valid_moves = self.get_valid_moves()

    def send_move_to_server(self, coord):
        print(f"sending to server moves")
        action_data = {'action': 'move', 'move_coord': coord, 'is_room': self.is_room()}
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
        valid_moves_coords.extend(self.get_adjacent_locations())

        # valid_moves_names = [get_location_name(coords) for coords in valid_moves_coords]
        # self.ui.notification_box.add_message(f"valid moves: {valid_moves_names}")
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
            print(f"adj location: {adjacent_location}")
            if adjacent_location not in (ROOM_COORDS.keys() | HALLWAYS_COORDS.keys()):
                print(f"invalid adj")
                continue
            if self.is_hallway_occupied(adjacent_location):
                continue

            valid_locations.append(adjacent_location)
        return valid_locations

    def is_hallway_occupied(self, location):
        for player_id, player in self.players.items():
            if player.get('current_location') == location:
                return True
        return False

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
        self.local_location = coord
        name = get_location_name(coord)
        self.ui.notification_box.add_message(f"Successfully moved to: {name}")
        self.ui.reset_room_highlight()
        print(f"sending move to server??")
        self.send_move_to_server(coord)
        if not self.is_room():
            self.ui.notification_box.add_message(f"Well played, {self.local_character}! "
                                                 f"Let's move to the next player's turn.")
        self.is_selecting_move = False
        self.has_moved = True

    def handle_suggestion_action(self, event):
        if not self.ui.handle_suggestion_events(event):
            return
        if all(self.suggesting_select):
            self.suggesting_select[0] = get_location_name(self.local_location)
            action_data = {
                'action': 'suggestion',
                'suggesting_select': self.suggesting_select
            }
            self.send_player_action(action_data)
            self.suggesting_select = [None, None, None]  # Reset the selections
            self.is_suggesting = False
            self.has_suggested = True

    def handle_accusation_action(self, event):
        if not self.ui.handle_accusation_events(event):
            return
        # Ensure all selections are made
        if all(self.accusing_select):
            action_data = {
                'action': 'accusation',
                'room': self.accusing_select[0],
                'suspect': self.accusing_select[1],
                'weapon': self.accusing_select[2]
            }
            self.send_player_action(action_data)
            self.accusing_select = [None, None, None]  # Reset the selections
            self.is_accusing = False
            self.has_accused = True

    def handle_end_turn(self):
        self.ui.notification_box.add_message(f"Well played, {self.local_character}! "
                                             f"Let's move to the next player's turn.")
        self.has_suggested = False
        self.has_moved = False
        self.send_player_action({'action': 'end_turn'})

    def whose_turn(self):
        for player_id, player_info in self.players.items():
            if player_info.get('turn_number') == self.current_turn_number:
                character = player_info.get('character')
                self.ui.notification_box.add_message(f"{character}'s turn.")
