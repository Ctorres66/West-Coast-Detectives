# ClientUI only for pygame draw without any data
import pygame

from shared.game_constants import COLOR_WHITE, COLOR_GRAY, COLOR_YELLOW, SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_HEIGHT, \
    BUTTON_MARGIN, BOX_WIDTH, BOX_HEIGHT
from shared.game_entities import Button


class ClientUI:
    def __init__(self, game):
        self.game = game  # This is an instance of the ClientGame class
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Clueless")
        # Load images or fonts here
        # self.background_image = pygame.image.load('path_to_background_image.png')
        # self.font = pygame.font.SysFont('Arial', 24)

        # Initialize the UI components here
        self.board_panel = BoardPanel(
            button_panel=ButtonPanel(x=50, y=10),
            notification_box=NotificationBox(x=850, y=100),
            cards=[]  # Initialize with actual card data
        )

    def update(self, board):
        """Update the entire game UI."""
        self.screen.fill(COLOR_WHITE)  # Clear the screen with black or any background
        self.board_panel.draw(self.screen, board)
        pygame.display.flip()  # Update the full display Surface to the screen

    def handle_events(self, event):
        """Handle UI-related events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_button = self.board_panel.button_panel.check_click(event)
            if clicked_button:
                # Handle the button click event
                pass
        # Handle other events like button clicks, mouse hover, etc.


class BoardPanel:
    def __init__(self, button_panel, notification_box, cards):
        self.button_panel = button_panel
        self.notification_box = notification_box
        self.cards = cards  # This could be a list of card objects or images

    def draw(self, screen, board):
        board.draw(screen)
        # Draw the button panel
        self.button_panel.draw(screen)
        # Draw the notification box
        self.notification_box.draw(screen)
        # Draw the cards
        for card in self.cards:
            card.draw(screen)


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


class Card:
    def __init__(self, image_filename, x, y, width, height):
        self.image = pygame.image.load(image_filename)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
