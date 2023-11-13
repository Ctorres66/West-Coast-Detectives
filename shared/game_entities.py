import json

import pygame
import os

from shared.game_constants import BUTTON_WIDTH, BUTTON_HEIGHT, COLOR_BLACK, ROOM_WIDTH, ROOM_HEIGHT

# Constants for image path and default colors
IMAGE_PATH = 'assets/images/'
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
                self.grid[room_dict.get('x')][room_dict.get('y')] = Room(room.get('name'), room.get('image_filename'))
        else:
            self.rows = rows
            self.cols = cols
            self.grid = [[None for _ in range(cols)] for _ in range(rows)]

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
        self.image = None  # Default to None if no image is provided
        if image_filename:
            self.load_image()

    def load_image(self):
        # Assuming images are stored in a directory named 'images'
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