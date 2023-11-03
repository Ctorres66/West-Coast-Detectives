import pygame

class Room:
    def __init__(self, name, image_filename):
        self.name = name
        self.image_filename = image_filename
        self.image = None  # This will be loaded later with Pygame

    def load_image(self, cell_width, cell_height):
        # Assuming the images are in the 'images/' directory
        self.image = pygame.transform.scale(
            pygame.image.load(f'constants/image/{self.image_filename}'),
            (cell_width, cell_height)
        )

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]  # Create a 5x5 grid

    def add_room(self, room, x, y):
        self.grid[y][x] = room  # Place the room at the specified coordinates

    def draw(self, surface):
        cell_width = surface.get_width() // self.cols
        cell_height = surface.get_height() // self.rows

        for y in range(self.rows):
            for x in range(self.cols):
                room = self.grid[y][x]
                if room and room.image:
                    surface.blit(room.image, (x * cell_width, y * cell_height))
                else:
                    # Draw an empty cell or hallway
                    pygame.draw.rect(
                        surface,
                        pygame.Color('lightslategrey'),  # Color for empty cells
                        (x * cell_width, y * cell_height, cell_width, cell_height),
                        1  # Width of the drawn border. Set to 0 for filled.
                    )

