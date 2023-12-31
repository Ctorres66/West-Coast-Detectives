import json
import random
import time

from shared.game_constants import *
from shared.game_entities import Card, Player


class ServerGame:
    def __init__(self, clients):
        self.current_turn_index = 1
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
        print(f"player data when start: {player_data}")
        start_game_data = {
            "players_data": player_data,
            "game_start": True,
            "current_turn_number": self.current_turn_index
        }
        self.broadcast(json.dumps({'start_game': start_game_data}, indent=4))

    def next_turn(self):
        print("Next turn triggered.")
        while True:
            # Increment the current turn index and wrap around if it exceeds the number of players
            self.current_turn_index = self.current_turn_index % len(self.players) + 1
            print(f"current_turn_index: {self.current_turn_index}")

            # Retrieve the player information for the current turn index
            for player_id, player_info in self.players.items():
                print(f"player_info.turn_number:{player_info.turn_number}")
                if self.current_turn_index == player_info.turn_number:
                    # Check if the player has lost the game
                    if not player_info.lose_game:
                        # If the player hasn't lost, it's their turn
                        print(f"It's now player {player_id}'s turn.")
                        return  # Exit the loop and proceed with the game

    def update_game_state(self):
        updated_player_state = self.encode_players()
        update_game_data = {
            "current_turn_number": self.current_turn_index,
            "players_data": updated_player_state
        }
        self.broadcast(json.dumps({'update_game_data': update_game_data}, indent=4))

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
        print(f"turn number after move: {self.current_turn_index}")

    def handle_accusation_action(self, player_id, room, suspect, weapon):
        # Detailed comparison
        is_correct_accusation = all([
            room == self.solution[0].card_name,
            suspect == self.solution[1].card_name,
            weapon == self.solution[2].card_name
        ])

        if is_correct_accusation:
            print(f"Player {player_id} wins! The accusation is correct.")
            self.broadcast(json.dumps({"winner": player_id}, indent=4))
            return True
        else:
            print(f"Player {player_id}'s accusation is incorrect.")
            self.players[player_id].lose_game = True
            self.broadcast(json.dumps({"loser": player_id}, indent=4))
            return False

    def handle_suggestion_action(self, suggesting_player_id, suggesting_select):
        suggest_data = {
            "who_suggest": suggesting_player_id,
            "suggest_what": suggesting_select
        }
        self.broadcast(json.dumps(suggest_data))
        time.sleep(1)
        print(f"Received suggestion from {suggesting_player_id}: {suggesting_select}")
        print(f"suspect: {suggesting_select[1]}")
        for player_id, player_info in self.players.items():
            print(f"self.players[player_id].character: {self.players[player_id].character}")
            if self.players[player_id].character == suggesting_select[1]:
                print(f"suspect is player")
                self.players[player_id].current_location = self.players[suggesting_player_id].current_location
                print(f"after assign new location: {self.players[player_id].current_location}")

        suggested_cards = {}  # disproven by , cards
        for player_id, player in self.players.items():
            if player_id != suggesting_player_id:
                card_you_suggest = player_has_card(player, suggesting_select)
                if card_you_suggest is not None:
                    suggest = {
                        "card": card_you_suggest,
                        "suggest_id": suggesting_player_id
                    }
                    self.broadcast(json.dumps({"card_you_suggest": suggest}, indent=4), player_id)
                    suggested_cards[player_id] = card_you_suggest

        print(f"{suggesting_player_id} can disprove the suggestion with {suggested_cards}")
        self.broadcast(json.dumps({"suggested_cards": suggested_cards}, indent=4), suggesting_player_id)


def player_has_card(player_info, cards):
    for hand_cards in player_info.cards:
        for each_suggest_card in cards:
            if hand_cards.card_name == each_suggest_card:
                return each_suggest_card
    return None
