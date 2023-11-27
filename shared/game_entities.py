import json

import pygame
import os

from shared.game_constants import *

# Constants for image path and default colors
DEFAULT_EMPTY_COLOR = pygame.Color('lightslategrey')


class Board:
    def __init__(self):
        self.rows = 5
        self.cols = 5
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.initialize_board()

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
            self.add_room(room, *coords)

    def add_room(self, room, x, y):
        if 0 <= x < self.rows and 0 <= y < self.cols:
            self.grid[x][y] = room

    def draw_rooms(self, surface, start_x, start_y, room_size):
        for x, row in enumerate(self.grid):
            for y, room in enumerate(row):

                # Calculate the position for each room
                rect_x = start_x + x * room_size
                rect_y = start_y + y * room_size
                rect = pygame.Rect(rect_x, rect_y, room_size, room_size)

                if (x == 1 and y == 1) or (x == 1 and y == 3) or (x == 3 and y == 1) or (x == 3 and y == 3):
                    pygame.draw.rect(surface, 'grey', rect)
                    continue

                # Draw the room if it exists, otherwise draw an empty rectangle
                if room:
                    room.draw(surface, rect)
                else:
                    pygame.draw.rect(surface, COLOR_WHITE, rect)
                    pygame.draw.rect(surface, COLOR_BLACK, rect, 1)

    def draw_board_outline(self, surface, start_x, start_y, room_size):
        # Calculate the total width and height of the board based on rooms
        board_width = self.cols * room_size
        board_height = self.rows * room_size

        # Create a rectangle representing the board's border
        board_rect = pygame.Rect(start_x, start_y, board_width, board_height)

        # Draw the board's border on the surface
        pygame.draw.rect(surface, pygame.Color(COLOR_BLACK), board_rect, 2)  # The '2' is the thickness of the border

    def draw(self, surface):
        # Define starting position, room width, and height

        room_size = ROOM_SIZE  # This should be defined somewhere in your code

        # Draw the rooms on the board
        self.draw_rooms(surface, BOARD_START_X, BOARD_START_Y, room_size)

        # Draw the board outline
        self.draw_board_outline(surface, BOARD_START_X, BOARD_START_Y, room_size)


class Room:
    def __init__(self, name, image_filename=None):
        self.name = name
        self.image_filename = image_filename
        self.image = None
        self.has_secret_passage = False
        if image_filename:
            self.load_image()

    def draw(self, surface, rect):
        font_size = 15
        font = pygame.font.SysFont('Arial', font_size)

        if self.image:
            # Scale the image to fit the cell and draw it
            scaled_image = pygame.transform.scale(self.image, (rect.width, rect.height))
            surface.blit(scaled_image, rect.topleft)

        # Render the room name
        text = font.render(self.name, True, COLOR_BLACK)  # White text
        text_width, text_height = text.get_size()

        # Calculate the position to place the text at the bottom of the cell
        text_x = rect.left + (rect.width - text_width) // 2
        text_y = rect.bottom - text_height - 5  # 5 pixels above the bottom

        # Draw the text
        surface.blit(text, (text_x, text_y))

        if not self.image:
            # Draw a placeholder or leave the cell empty
            pygame.draw.rect(surface, pygame.Color('red'), rect)  # Example placeholder

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
        # Load the image only once
        if self.image is not None:
            return  # Image already loaded

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

        if self.image:
            self.draw_image(surface, position)

    def draw_text(self, surface, text, position):
        font = pygame.font.Font(None, 24)
        rendered_text = font.render(text, True, pygame.Color('black'))
        surface.blit(rendered_text, position)

    def draw_image(self, surface, position):
        # Use the pre-loaded image
        if self.image:
            image_rect = self.image.get_rect(center=(position[0] + 50, position[1] + 75))
            surface.blit(self.image, image_rect)


class Player:
    def __init__(self, player_id, character, current_location):
        self.player_id = player_id
        self.character = character
        self.current_location = current_location
        self.cards = []

    # def update_position(self, new_location):
    #     if new_location != self.current_location:
    #         self.current_location = new_location
    #         return self.encode()  # Return the encoded data only if the position changes
    #     return None  # Return None if the position hasn't changed

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
