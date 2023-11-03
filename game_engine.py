import pygame
from board import Board, Room
from button_panel import ButtonPanel
from constants.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_BLACK, COLOR_GRAY, BUTTON_WIDTH,
    BUTTON_HEIGHT, BUTTON_MARGIN, NOTIFICATION_HEIGHT, CARD_DISPLAY_HEIGHT
)

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Clue-Less")
        self.clock = pygame.time.Clock()
        self.board = Board(5, 5)
        self.running = True
        self.buttons = self.create_button_panel()
        self.current_player = None  # You'll need to create a Player class
        self.notification_text = "Welcome to Clue-Less!"
        self.load_rooms()

    def load_rooms(self):
        # Create Room objects with specific positions on the board
        rooms_info = {
            "KITCHEN": ("Kitchen", "Kitchen.jpg", (4, 4)),
            "BALLROOM": ("Ballroom", "Ballroom.jpg", (4, 2)),
            "CONSERVATORY": ("Conservatory", "Conservatory.jpg", (4, 0)),
            "BILLIARD_ROOM": ("Billiard Room", "Billiard Room.jpg", (2, 2)),
            "LIBRARY": ("Library", "Library.jpg", (2, 0)),
            "STUDY": ("Study", "Study.jpg", (0, 0)),
            "HALL": ("Hall", "Hall.jpg", (0, 2)),
            "DINING_ROOM": ("Dining Room", "Dining Room.jpg", (2, 4)),
            # ... Other rooms ...
        }

        cell_width = SCREEN_WIDTH // self.board.cols
        cell_height = SCREEN_HEIGHT // self.board.rows

        for room_name, (name, image_filename, (x, y)) in rooms_info.items():
            room = Room(name, image_filename)
            room.load_image(cell_width, cell_height)
            self.board.add_room(room, x, y)

    def create_button_panel(self):
        # Define buttons info: list of tuples (text, text_color)
        buttons_info = [
            ("Move", (0, 0, 0)),
            ("Suggestion", (0, 0, 0)),
            ("Accusation", (0, 0, 0)),
            ("End Turn", (0, 0, 0))
        ]
        # Create and return ButtonPanel instance
        return ButtonPanel(50, SCREEN_HEIGHT - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT, COLOR_GRAY, buttons_info)

    def draw(self):
        self.screen.fill(COLOR_WHITE)
        self.board.draw(self.screen)
        self.buttons.draw(self.screen)
        # Draw the notification area and player cards here
        # ...

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    button_clicked = self.buttons.check_click(event)
                    if button_clicked:
                        # Handle button click events
                        self.handle_button_click(button_clicked)

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_button_click(self, button_text):
        # Update this method to handle button click events
        print(f"{button_text} button was clicked")

# The Player class should have attributes related to the player's cards and actions
# This should be implemented in a separate player.py file.

if __name__ == "__main__":
    game_engine = GameEngine()
    game_engine.run()
