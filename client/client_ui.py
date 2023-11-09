# ClientUI only for pygame draw without any data
import pygame

from shared.game_entities import Button


class ClientUI:
    def __init__(self, game, width=800, height=600):
        self.game = game  # This is an instance of the ClientGame class
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Clueless")
        # Load images or fonts here
        # self.background_image = pygame.image.load('path_to_background_image.png')
        # self.font = pygame.font.SysFont('Arial', 24)

        # Initialize the UI components here
        self.board_panel = BoardPanel(
            button_panel=ButtonPanel(
                x=0, y=self.height - 100,  # Example position
                button_width=80,
                button_height=30,
                button_color=(100, 200, 255),
                buttons_info=[("Button1", (255, 255, 255)), ("Button2", (255, 255, 255))]
            ),
            notification_box=NotificationBox(
                x=0, y=0,
                width=self.width,
                height=50  # Example size
            ),
            cards=[]  # Initialize with actual card data
        )

    def update(self, board):
        """Update the entire game UI."""
        self.screen.fill((0, 0, 0))  # Clear the screen with black or any background
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
