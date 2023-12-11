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

    def broadcast(self, message, client_id=None):
        if client_id:
            client = self.clients.get(client_id)
            if client:
                try:
                    client.sendall(message.encode())
                except Exception as e:
                    print(f"Error sending to client {client_id}: {e}")
        else:
            # Assuming this method sends the message to all connected clients
            for client in self.clients.values():
                try:
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

    def next_turn(self):
        self.current_turn_index = (self.current_turn_index % len(self.players)) + 1

    def update_game_state(self):

        updated_player_state = self.encode_players()
        update_game_data = {
            "players_data": updated_player_state,
            "current_turn_number": self.current_turn_index
        }
        self.broadcast(json.dumps(update_game_data, indent=4))

    def add_player(self, player_id):
        turn_number = len(self.players) + 1  # Assign turn number based on the order of joining
        player = Player(player_id, character=None, current_location=None, turn_number=turn_number)
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
        self.solution = (solution_room, solution_suspect, solution_weapon)
        print(f"Solution prepared: "
              f"Room - {solution_room.card_name}, "
              f"Suspect - {solution_suspect.card_name}, "
              f"Weapon - {solution_weapon.card_name}")

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
            player_data.append(player_dict)
        return player_data

    def remove_player(self, player_id):
        # Remove a player from the game
        if player_id in self.players:
            del self.players[player_id]
            self.broadcast(f"Player {player_id} has left the game.")

    # player move logic
    def handle_move_action(self, player_id, move_coord, is_room):
        # move should be a coord
        print(f"move info: {move_coord} player_id: {player_id} is_room: {is_room}")
        self.players[player_id].current_location = move_coord
        if not is_room:
            self.next_turn()
        self.update_game_state()  # Broadcast the updated game state

    def handle_accusation_action(self, player_id, room, suspect, weapon):
        # Detailed comparison
        is_correct_accusation = all([
            room == self.solution[0].card_name,
            suspect == self.solution[1].card_name,
            weapon == self.solution[2].card_name
        ])

        if is_correct_accusation:
            print(f"Player {player_id} wins! The accusation is correct.")
            end_game_data = {
                "winner": player_id,
                "game_end": True
            }
            self.broadcast(json.dumps(end_game_data, indent=4))
        else:
            print(f"Player {player_id}'s accusation is incorrect.")
            self.players[player_id].lose_game = True
            self.broadcast(json.dumps({"loser": player_id}, indent=4))

        self.update_game_state()  # Broadcast the updated game state

    def handle_suggestion_action(self, suggesting_player_id, suggesting_select):
        # Print statements for debugging
        print(f"Received suggestion from {suggesting_player_id}: {suggesting_select}")
        suggested_cards = []
        for player_id, player in self.players.items():
            if player_id != suggesting_player_id:
                card_you_suggest = player_has_card(player, suggesting_select)
                if card_you_suggest is not None:
                    self.broadcast(json.dumps({"card_you_suggest": card_you_suggest}, indent=4), player_id)
                    suggested_cards.append(card_you_suggest)

        print(f"{suggesting_player_id} can disprove the suggestion with {suggested_cards}")
        self.broadcast(json.dumps({"suggested_cards": suggested_cards}, indent=4), suggesting_player_id)


def player_has_card(player_info, cards):
    for hand_cards in player_info.cards:
        for each_suggest_card in cards:
            if hand_cards.card_name == each_suggest_card:
                return each_suggest_card
    return None
