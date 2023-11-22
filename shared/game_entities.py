import json

import pygame
import os

from shared.game_constants import *

# Constants for image path and default colors
DEFAULT_EMPTY_COLOR = pygame.Color('lightslategrey')


class Board:
    def __init__(self, rows=None, cols=None, dict_data=None):
        if dict_data is not None:
            metadata = dict_data.get('metadata')
            self.rows = metadata.get('num_rows')
            self.cols = metadata.get('num_cols')
            self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
            for room_dict in dict_data.get('rooms'):
                room = room_dict.get('room')
                # Corrected index order: first 'y' (row), then 'x' (column)
                x = room_dict.get('x')  # Column
                y = room_dict.get('y')  # Row
                if y is not None and x is not None:
                    self.grid[y][x] = Room(room.get('name'), room.get('image_filename'))
        else:
            self.rows = rows if rows is not None else 0
            self.cols = cols if cols is not None else 0
            self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def add_room(self, room, x, y):
        if 0 <= x < self.rows and 0 <= y < self.cols:
            self.grid[x][y] = room

    # Function to encode the current Board state to Json format
    def encode(self):
        board_data = {
            'metadata': {
                'num_rows': self.rows,
                'num_cols': self.cols,
            },
            'rooms': []
        }
        for x, row in enumerate(self.grid):
            for y, room in enumerate(row):
                if room is None:
                    continue
                board_data.get('rooms').append({
                    'x': x,
                    'y': y,
                    'room': room.to_dict(),
                })
        return json.dumps(board_data, indent=4)

    def draw_rooms(self, surface, start_x, start_y, room_width, room_height):
        for x, row in enumerate(self.grid):
            for y, room in enumerate(row):
                # Calculate the position for each room
                rect_x = start_x + x * room_width
                rect_y = start_y + y * room_height
                rect = pygame.Rect(rect_x, rect_y, room_width, room_height)

                # Draw the room if it exists, otherwise draw an empty rectangle
                if room:
                    room.draw(surface, rect)
                else:
                    pygame.draw.rect(surface, DEFAULT_EMPTY_COLOR, rect, 1)

    def draw_board_outline(self, surface, start_x, start_y, room_width, room_height):
        # Calculate the total width and height of the board based on rooms
        board_width = self.cols * room_width
        board_height = self.rows * room_height

        # Create a rectangle representing the board's border
        board_rect = pygame.Rect(start_x, start_y, board_width, board_height)

        # Draw the board's border on the surface
        pygame.draw.rect(surface, pygame.Color(COLOR_BLACK), board_rect, 2)  # The '2' is the thickness of the border

    def draw(self, surface):
        # Define starting position, room width, and height
        start_x = 300
        start_y = 100
        room_width = ROOM_WIDTH  # This should be defined somewhere in your code
        room_height = ROOM_HEIGHT  # This should be defined somewhere in your code

        # Draw the rooms on the board
        self.draw_rooms(surface, start_x, start_y, room_width, room_height)

        # Draw the board outline
        self.draw_board_outline(surface, start_x, start_y, room_width, room_height)


class Room:
    def __init__(self, name, image_filename=None):
        self.name = name
        self.image_filename = image_filename
        self.image = None
        self.has_secret_passage = False
        self.connected_rooms = []  # List of other rooms that are connected to this one, these are specified when
        # you make a Room object
        if image_filename:
            self.load_image()

    def load_image(self):
        # Assuming images are stored in a directory named 'images'
        # NOTE TO CARLOS, CHANGE THIS TO YOUR OWN LOCAL IMAGES FOLDER
        image_path = os.path.join('../assets/images', self.image_filename)
        try:
            self.image = pygame.image.load(image_path)
        except pygame.error as e:
            print(f"Error loading image for room '{self.name}': {e}")
            self.image = None  # Set to None if there's an error loading

    def to_dict(self):
        return {
            'name': self.name,
            'image_filename': self.image_filename,
        }

    def draw(self, surface, rect):
        if self.image:
            # Scale the image to fit the cell and draw it
            scaled_image = pygame.transform.scale(self.image, (rect.width, rect.height))
            surface.blit(scaled_image, rect.topleft)
        else:
            # Draw a placeholder or leave the cell empty
            pygame.draw.rect(surface, pygame.Color('gray'), rect)  # Example placeholder


class Button:
    def __init__(self, x, y, text, color):
        self.font = pygame.font.SysFont('Arial', 24)
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.color = color,
        self.text = text
        self.text_color = COLOR_BLACK
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT

    def draw(self, screen):
        # Draw the button rectangle
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw the button text
        self._draw_text(screen)

    def _draw_text(self, screen):
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Blit the text onto the surface
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


class Card:
    def __init__(self, card_type, name, image_filename=None):
        """
        Initialize a new card with a type, name, and optional image.

        :param card_type: The type of card (e.g., 'suspect', 'weapon', 'room')
        :param name: The name of the card (e.g., 'Miss Scarlet', 'Rope', 'Kitchen')
        :param image_filename: The filename of the image associated with the card
        """
        self.card_type = card_type
        self.name = name
        self.image_filename = image_filename
        self.image = None  # Default to None if no image is provided

        if image_filename:
            self.load_image()

    def __repr__(self):
        """
        Return a string representation of the card.

        :return: String representation of the card
        """
        return f"Card(Type: {self.card_type}, Name: {self.name})"

    def to_dict(self):
        """
        Serialize the card to a dictionary.

        :return: A dictionary representation of the card
        """
        return {
            'card_type': self.card_type,
            'name': self.name,
            'image_filename': self.image_filename
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Card instance from a dictionary.

        :param data: A dictionary with keys 'card_type', 'name', and 'image_filename'
        :return: A Card instance
        """
        return cls(data['card_type'], data['name'], data['image_filename'])

    def to_json(self):
        """
        Serialize the card to a JSON string.

        :return: A JSON string representation of the card
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str):
        """
        Create a Card instance from a JSON string.

        :param json_str: A JSON string representation of a card
        :return: A Card instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)

    def load_image(self):
        # Assuming images are stored in a directory named 'images' under 'assets'
        image_path = os.path.join('../assets/images', self.image_filename)
        try:
            self.image = pygame.image.load(image_path)
        except pygame.error as e:
            print(f"Error loading image for card '{self.name}': {e}")
            self.image = None  # Set to None if there's an error loading

    def draw(self, surface, position):

        # Create a rectangle for the card
        card_rect = pygame.Rect(position, (CARD_WIDTH, CARD_HEIGHT))

        # Draw the rectangle
        pygame.draw.rect(surface, pygame.Color('white'), card_rect)

        # Position for the text inside the rectangle
        text_position = (position[0] + PADDING, position[1] + PADDING)

        # Draw the card type and name
        self.draw_text(surface, self.card_type, text_position)
        self.draw_text(surface, self.name, (text_position[0], text_position[1] + TEXT_HEIGHT))

        # Check if there is an image filename and draw the image
        if self.image_filename:
            self.draw_image(surface, position)

    def draw_text(self, surface, text, position):
        font = pygame.font.Font(None, 24)
        rendered_text = font.render(text, True, pygame.Color('black'))
        surface.blit(rendered_text, position)

    def draw_image(self, surface, position):
        try:
            image = pygame.image.load(self.image_filename)
            image_rect = image.get_rect(center=(position[0] + 50, position[1] + 75))  # Adjust position as needed
            surface.blit(image, image_rect)
        except pygame.error:
            pass  # Optionally handle the error here


class Player:
    def __init__(self, player_id, character, current_location, cards):
        self.player_id = player_id
        self.character = character
        self.current_location = current_location
        self.cards = cards

    def update_position(self, new_location):
        if new_location != self.current_location:
            self.current_location = new_location
            return self.encode()  # Return the encoded data only if the position changes
        return None  # Return None if the position hasn't changed

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'character': self.character,
            'current_location': self.current_location,
            'cards': [card.to_dict() for card in self.cards]
        }

    def move_to_hallway(self, hallway):
        if hallway.is_occupied():
            raise ValueError("The hallway is blocked.")
        self.current_location = hallway

    # game logic for each player
    def move_to_room(self, room):
        if room.has_secret_passage():
            self.current_location = room.get_diagonal_room()
            # self.make_suggestion()
            # keep commented for now, player should be able to choose to make a suggestion or not here
        else:
            self.current_location = room

    def make_suggestion(self):
        # Logic to make a suggestion
        # This would involve choosing a character and a weapon
        # And then notifying the game engine to process the suggestion
        suggestion = {'character': 'Miss Scarlet', 'weapon': 'Candlestick'}
        self.game.make_suggestion(suggestion)

    def make_accusation(self):
        # Logic to make an accusation
        # This would involve choosing a character, weapon, and room
        # And then notifying the game engine to process the accusation
        accusation = {'character': 'Colonel Mustard', 'weapon': 'Dagger', 'room': 'Library'}
        self.game.make_accusation(accusation)

    def stay_or_move(self, moved_by_suggestion):
        if moved_by_suggestion:
            # Player decides to stay and make a suggestion
            self.make_suggestion()
        else:
            # Logic for the player to choose to move through a doorway or take a secret passage
            pass  # Implement UI interaction or other logic to enable the player to choose
