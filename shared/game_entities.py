import pygame
import os

# Constants for image path and default colors
IMAGE_PATH = 'assets/images/'
DEFAULT_EMPTY_COLOR = pygame.Color('lightslategrey')
DEFAULT_TEXT_COLOR = (0, 0, 0)


class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def add_room(self, room, x, y):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            self.grid[y][x] = room

    def draw(self, surface):
        cell_width = surface.get_width() // self.cols
        cell_height = surface.get_height() // self.rows

        for y, row in enumerate(self.grid):
            for x, room in enumerate(row):
                rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
                if room:
                    room.draw(surface, rect)
                else:
                    pygame.draw.rect(surface, DEFAULT_EMPTY_COLOR, rect, 1)


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

    def draw(self, surface, rect):
        if self.image:
            # Scale the image to fit the cell and draw it
            scaled_image = pygame.transform.scale(self.image, (rect.width, rect.height))
            surface.blit(scaled_image, rect.topleft)
        else:
            # Draw a placeholder or leave the cell empty
            pygame.draw.rect(surface, pygame.Color('gray'), rect)  # Example placeholder


class Button:
    def __init__(self, x, y, width, height, color, text, text_color=DEFAULT_TEXT_COLOR, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        # self.font = pygame.font.SysFont(None, font_size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        self._draw_text(screen)

    def _draw_text(self, screen):
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
