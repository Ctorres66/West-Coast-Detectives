import pygame
from board import Room, Board

# Pygame initialization
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Clueless")

# Create a 5x5 Board
board = Board(5, 5)

# Create Room objects
rooms = {
    "KITCHEN": Room("Kitchen", "Kitchen.jpg"),
    "BALLROOM": Room("Ballroom", "Ballroom.jpg"),
    "CONSERVATORY": Room("Conservatory", "Conservatory.jpg"),
    "BILLIARD_ROOM": Room("Billiard Room", "Billiard Room.jpg"),
    "LIBRARY": Room("Library", "Library.jpg"),
    "STUDY": Room("Study", "Study.jpg"),
    "HALL": Room("Hall", "Hall.jpg"),
    #"LOUNGE": Room("Lounge", "Lounge.jpg"),
    "DINING_ROOM": Room("Dining Room", "Dining Room.jpg"),
}

# Add rooms to the board at specific coordinates
room_coordinates = {
    "KITCHEN": (4, 4),
    "BALLROOM": (4, 2),
    "CONSERVATORY": (4, 0),
    "BILLIARD_ROOM": (2, 2),
    "LIBRARY": (2, 0),
    "STUDY": (0, 0),
    "HALL": (0, 2),
    "LOUNGE": (0, 4),
    "DINING_ROOM": (2, 4),
}

for room_name, (x, y) in room_coordinates.items():
    room = rooms.get(room_name)
    if room:
        board.add_room(room, x, y)

# Calculate grid cell size based on screen dimensions and board size
cell_width = SCREEN_WIDTH // board.width
cell_height = SCREEN_HEIGHT // board.height

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic goes here

    # Clear the screen
    screen.fill(WHITE)

    # Drawing grid
    grid_color = (0, 0, 0)  # Color of the grid lines
    grid_width = 2  # Width of the grid lines

    # Draw horizontal lines
    for y in range(0, SCREEN_HEIGHT, cell_height):
        pygame.draw.line(screen, grid_color, (0, y), (SCREEN_WIDTH, y), grid_width)

    # Draw vertical lines
    for x in range(0, SCREEN_WIDTH, cell_width):
        pygame.draw.line(screen, grid_color, (x, 0), (x, SCREEN_HEIGHT), grid_width)

    # Iterate over the board and draw rooms
    for y in range(board.height):
        for x in range(board.width):
            room = board.grid[y][x]
            if room:
                # Construct the correct path to the image in the "assets" folder
                image_path = f"assets/{room.image}"
                try:
                    image = pygame.image.load(image_path)
                    # Resize image to fit the cell
                    image = pygame.transform.scale(image, (cell_width, cell_height))
                    screen.blit(image, (x * cell_width, y * cell_height))
                except pygame.error:
                    print(f"Could not load image: {image_path}")

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
