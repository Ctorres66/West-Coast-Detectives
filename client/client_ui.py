import pygame

from shared.game_entities import Button
from shared.game_constants import SCREEN_WIDTH, SCREEN_HEIGHT


class ClientUI:
    def __init__(self, game):
        self.game = game  # Store the game state
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Clue-Less Game")

    def draw(self):
        # Clear the screen
        self.screen.fill((255, 255, 255))  # Assuming white is the desired background color
        # Draw game-related elements (players, rooms, etc.)
        # You would access the game state via self.game here
        # Example: self.game.board.draw(self.screen)

        # Refresh the display
        pygame.display.flip()

    def handle_events(self, event):
        # Handle user input events
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass  # Add logic for mouse button down events
        # Add logic for other events if necessary


class BoardPanel:
    def __init__(self, board, button_panel, notification_box, cards):
        self.board = board
        self.button_panel = button_panel
        self.notification_box = notification_box
        self.cards = cards  # This could be a list of card objects or images

    def draw(self, screen):
        # Draw the board
        self.board.draw(screen)
        # Draw the button panel
        self.button_panel.draw(screen)
        # Draw the notification box
        self.notification_box.draw(screen)
        # Draw the cards
        for card in self.cards:
            card.draw(screen)


class ButtonPanel:
    def __init__(self, x, y, button_width, button_height, button_color, buttons_info):
        self.buttons = []
        for i, (text, text_color) in enumerate(buttons_info):
            button_x = x + (button_width + 10) * i  # 10 pixels between buttons
            button = Button(button_x, y, button_width, button_height, button_color, text, text_color)
            self.buttons.append(button)

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def check_click(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                print(f"{button.text} button was clicked")  # Placeholder for actual button click handling
                return button.text  # You can also call a method here or pass a callback to each button
        return None


class NotificationBox:
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.messages = []

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
