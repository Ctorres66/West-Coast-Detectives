# ClientUI only for pygame draw without any data
import pygame

from shared.game_constants import *
from shared.game_entities import Button, Board


class ClientUI:
    def __init__(self):
        # initial board
        self.board = Board()
        # self.game = game  # This is an instance of the ClientGame class
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        pygame.display.set_caption("Clueless")
        # Load images or fonts here
        # self.background_image = pygame.image.load('path_to_background_image.png')
        # self.font = pygame.font.SysFont('Arial', 24)

        # Initialize the UI components here
        self.board_panel = BoardPanel(
            board=self.board,
            button_panel=ButtonPanel(x=50, y=10),
            notification_box=NotificationBox(x=850, y=100),
        )

    def update_initial_ui(self):
        """Update the entire game UI."""
        self.screen.fill(COLOR_WHITE)  # Clear the screen with black or any background
        self.board_panel.draw(self.screen)
        pygame.display.flip()  # Update the full display Surface to the screen

    def update_players(self, character, current_location):
        print(f"start to draw players info here {character}")
        square_size = 50
        font_size = 24

        # Extract x and y from current_location
        x = current_location[0]
        y = current_location[1]
        print(f"x: {x} y: {y}")

        # Create and draw the rectangle
        rect = pygame.Rect(x, y, square_size, square_size)
        pygame.draw.rect(self.screen, (0, 0, 255), rect)  # Blue square

        # Create a font object
        font = pygame.font.SysFont('Arial', font_size)

        # Render the text
        text = font.render(character, True, (255, 255, 255))  # White text

        # Calculate the position to center the text in the square
        text_width, text_height = text.get_size()
        text_x = x + (square_size - text_width) // 2
        text_y = y + (square_size - text_height) // 2

        # Draw the text
        self.screen.blit(text, (text_x, text_y))

    def draw_local_player_cards(self, local_cards):
        # Define the starting position for the cards
        start_x = 10  # 10 pixels from the left edge of the screen
        start_y = 80  # 10 pixels below the notification box

        # Draw each card in the hand
        for index, card in enumerate(local_cards):
            card_x = start_x + (index * (card.width + 10))  # Add space between cards
            card_y = start_y
            # Assuming the Card class has a draw method
            card.draw(self.screen, (card_x, card_y))

    def update_player_info(self, players, local_player_cards):
        self.board_panel.players = players
        self.board_panel.cards = local_player_cards

    def handle_events(self, event):
        """Handle UI-related events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_button = self.board_panel.button_panel.check_click(event)
            if clicked_button:
                # Handle the button click event
                print(f"{clicked_button} was clicked")
                return clicked_button
        # Handle other events like button clicks, mouse hover, etc.
        return None


class BoardPanel:
    def __init__(self, button_panel, notification_box, board):
        self.board = board
        self.button_panel = button_panel
        self.notification_box = notification_box

    def draw(self, screen):
        self.board.draw(screen)
        # Draw the button panel
        self.button_panel.draw(screen)
        # Draw the notification box
        self.notification_box.draw(screen)


class ButtonPanel:
    def __init__(self, x, y):
        self.buttons = []
        colors = [(239, 244, 248), (192, 211, 228), (243, 219, 233), (149, 155, 189)]
        texts = ["MOVE", "SUGGESTION", "ACCUSATION", "END TURN"]

        for i, (color, text) in enumerate(zip(colors, texts)):
            # Calculate the y position for each button
            y = BUTTON_HEIGHT + i * (BUTTON_HEIGHT + BUTTON_MARGIN)
            button = Button(x, y, text, color)
            self.buttons.append(button)

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def check_click(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                print(f"{button.text} button was clicked")
                return button.text
        return None


class NotificationBox:
    def __init__(self, x, y, width=BOX_WIDTH, height=BOX_HEIGHT):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = COLOR_GRAY
        self.messages = ["Game Start!"]

    def add_message(self, message):
        self.messages.append(message)

    def draw(self, screen):
        # Draw the notification box
        pygame.draw.rect(screen, self.color, self.rect)
        # Display the messages
        font = pygame.font.SysFont('arial', 24)
        for idx, message in enumerate(self.messages):
            text_surface = font.render(message, True, (0, 0, 0))
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5 + idx * 20))
