import pygame
import os

from shared.game_constants import *


class Board:
    def __init__(self):
        self.rows = 5
        self.cols = 5
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.initialize_board()

    def initialize_board(self):
        # Initialize rooms on the board using the ROOMS constant
        for room_coord, room_name in ROOM_COORDS.items():
            # Use the room name to construct the image filename dynamically
            image_filename = f"{room_name.replace(' ', '_')}.png"
            # Create a Room instance
            room = Room(room_name, room_coord, image_filename)
            # Add the room to the board at the specified coordinates
            self.add_room(room)

        for hallway_coord, hallway_name in HALLWAYS_COORDS.items():
            # Create a Room instance
            hallway = Room(hallway_name, hallway_coord)
            # Add the room to the board at the specified coordinates
            self.add_room(hallway)

    def add_room(self, room):
        x, y = room.coord
        if 0 <= x < self.rows and 0 <= y < self.cols:
            self.grid[x][y] = room

    def draw_rooms(self, surface):
        for x, row in enumerate(self.grid):
            for y, room in enumerate(row):

                # Calculate the position for each room
                rect_ver = x * ROOM_SIZE
                rect_hor = y * ROOM_SIZE
                rect = pygame.Rect(rect_hor, rect_ver, ROOM_SIZE, ROOM_SIZE)

                # Draw the room if it exists, otherwise draw a gray rectangle
                if room:
                    pygame.draw.rect(surface, COLOR_WHITE, rect)
                    room.room_draw(surface, rect)
                else:
                    pygame.draw.rect(surface, COLOR_GRAY, rect)


class Room:
    def __init__(self, name, coord, image_filename=None):
        self.name = name
        self.coord = coord
        self.image = self.load_image(image_filename) if image_filename else None
        self.highlight = False  # Set to False by default
        self.rect = None

    def room_draw(self, surface, rect):
        self.rect = rect
        # Draw the base rectangle
        pygame.draw.rect(surface, pygame.Color(COLOR_BLACK), rect, 1)

        # Draw the room image if it exists
        if self.image:
            # Scale the image to fit the cell and draw it
            scaled_image = pygame.transform.scale(self.image, (rect.width, rect.height))
            surface.blit(scaled_image, rect.topleft)

        # Draw the semi-transparent highlight if needed
        if self.highlight:
            highlight_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            highlight_surface.fill(COLOR_YELLOW + (128,))  # Fill the surface with the semi-transparent color
            surface.blit(highlight_surface, rect.topleft)

    def load_image(self, image_filename):
        """Load an image for the room, return None if unable to load."""
        image_path = os.path.join('../assets', image_filename)
        try:
            return pygame.image.load(image_path)
        except pygame.error as e:
            print(f"Error loading image for room '{self.name}': {e}")
            return None

    def to_dict(self):
        return {
            'name': self.name,
            'image': self.image
        }

    def room_is_clicked(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the current mouse position
            mouse_pos = pygame.mouse.get_pos()
            surface_offset = (BOARD_START_X, BOARD_START_Y)
            adjusted_rect = self.rect.move(surface_offset)
            # Check if the mouse click was within the room's rectangle
            if adjusted_rect.collidepoint(mouse_pos):
                return True

        return False


class Button:
    def __init__(self, x, y, text, color):
        self.font = pygame.font.SysFont('Arial', 20)
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


def load_image(card_name):
    """Load an image and return it, return None if unable to load."""
    path_to_image = f"../assets/cards/{card_name}.png"
    try:
        return pygame.image.load(path_to_image)
    except pygame.error as e:
        print(f"Error loading image for card '{card_name}': {e}")
        return None


class Card:
    def __init__(self, card_type, card_name=None):
        self.card_type = card_type
        self.card_name = card_name
        self.card_image = load_image(card_name) if card_name else None

    def to_dict(self):
        return {
            'card_type': self.card_type,
            'card_name': self.card_name,
        }

    def card_draw(self, surface, position):
        # Create a rectangle for the card
        card_rect = pygame.Rect(position, (CARD_WIDTH, CARD_HEIGHT))
        # Draw the rectangle
        pygame.draw.rect(surface, COLOR_GRAY, card_rect)
        # Check if there is an image filename and draw the image
        if self.card_image:
            self.draw_image(surface, position)

    def draw_image(self, surface, position):

        if self.card_image:
            scaled_image = pygame.transform.scale(self.card_image, (CARD_WIDTH, CARD_HEIGHT))

            image_rect = scaled_image.get_rect(center=(position[0] + CARD_WIDTH // 2,
                                                       position[1] + CARD_HEIGHT // 2))

            surface.blit(scaled_image, image_rect)


class Player:
    def __init__(self, player_id, character, current_location, turn_number):
        self.player_id = player_id
        self.character = character
        self.current_location = current_location
        self.cards = []
        self.turn_number = turn_number
        self.lose_game = False

    def to_dict(self):
        if self.lose_game:
            self.current_location = None
        return {
            'player_id': self.player_id,
            'character': self.character,
            'current_location': self.current_location,
            'cards': [card.to_dict() for card in self.cards],
            'turn_number': self.turn_number,
            'lose_game': self.lose_game
        }
