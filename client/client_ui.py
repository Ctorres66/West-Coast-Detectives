# ClientUI only for pygame draw without any data
import pygame
import random

from shared.game_constants import *
from shared.game_entities import Button, Board, Card


class ClientUI:
    def __init__(self):
        # initial board
        self.board = Board()
        # self.game = game  # This is an instance of the ClientGame class
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        pygame.display.set_caption("Clueless")

        # Initialize the UI components here
        self.board_panel = BoardPanel(
            board=self.board,
            button_panel=ButtonPanel(x=50, y=10),
            notification_box=NotificationBox(x=850, y=100),
        )
        # Add text input components
        self.suggestion_button = pygame.Rect(200, 400, 200, 50)
        # Initialize font
        self.font = pygame.font.Font(None, 32)  # You can replace 'None' with a specific font file if needed
        # Add text input components
        self.suggestion_button = pygame.Rect(200, 400, 200, 50)
        self.suggestion_input_boxes = [
            pygame.Rect(200, 100, 200, 32),
            pygame.Rect(200, 150, 200, 32),
            pygame.Rect(200, 200, 200, 32),
        ]
        self.suggestion_text = ['Enter character', 'Enter weapon', 'Enter room']
        self.suggestion_texts = ['', '', '']
        self.send_suggestion_button = pygame.Rect(250, 250, 100, 40)

        # New state variable to track if suggestion is sent
        self.suggestion_sent = False

        self.accusation_button = pygame.Rect(200, 400, 200, 50)
        self.accusation_input_boxes = [
            pygame.Rect(200, 450, 200, 32),  # Adjusted Y-coordinate
            pygame.Rect(200, 500, 200, 32),  # Adjusted Y-coordinate
            pygame.Rect(200, 550, 200, 32),  # Adjusted Y-coordinate
        ]
        self.accusation_text = ['Accuse character', 'Accuse weapon', 'Accuse room']
        self.accusation_texts = ['', '', '']
        self.send_accusation_button = pygame.Rect(250, 600, 100, 40)  # Adjusted Y-coordinate
        self.accusation_sent = False

    def draw_suggestion_ui(self):
        # Draw suggestion UI components only if suggestion is not sent
        if not self.suggestion_sent:
            pygame.draw.rect(self.screen, (0, 255, 0), self.send_suggestion_button)

            for i, box in enumerate(self.suggestion_input_boxes):
                pygame.draw.rect(self.screen, (0, 0, 255), box, 2)
                self.draw_text(self.suggestion_texts[i], (0, 0, 0), box)  # Use black color for text

            # Draw text on button
            self.draw_text('SEND', (255, 255, 255), self.send_suggestion_button)

    def handle_suggestion_events(self, event):
        # Handle events for the suggestion UI
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.suggestion_button.collidepoint(event.pos):
                self.draw_suggestion_ui()
            elif self.send_suggestion_button.collidepoint(event.pos):
                # Send the suggestion tuple to the server
                suggestion_tuple = tuple(self.suggestion_texts)
                # Assuming you have a method in the ClientGame class to handle sending suggestions
                self.game.handle_send_suggestion(suggestion_tuple)
                # Set the suggestion_sent flag to True to hide the UI components
                self.suggestion_sent = True

        elif event.type == pygame.KEYDOWN:
            for i, box in enumerate(self.suggestion_input_boxes):
                if box.collidepoint(event.pos) and not self.suggestion_sent:
                    if event.key == pygame.K_RETURN:
                        # Move to the next input box or send suggestion on Enter
                        self.suggestion_texts[i] = self.suggestion_text[i]
                        if i < 2:
                            self.suggestion_texts[i + 1] = self.suggestion_text[i + 1]
                    elif event.key == pygame.K_BACKSPACE:
                        # Allow backspace to delete characters
                        self.suggestion_texts[i] = self.suggestion_texts[i][:-1]
                    else:
                        # Append typed characters to the current input box
                        self.suggestion_texts[i] += event.unicode

    def draw_accusation_ui(self):
        # Draw accusation UI components only if accusation is not sent
        if not self.accusation_sent:
            pygame.draw.rect(self.screen, (0, 255, 0), self.send_accusation_button)

            for i, box in enumerate(self.accusation_input_boxes):
                pygame.draw.rect(self.screen, (0, 0, 255), box, 2)
                self.draw_text(self.accusation_texts[i], (0, 0, 0), box)  # Use black color for text

            # Draw text on buttons
            self.draw_text('SEND', (255, 255, 255), self.send_accusation_button)

    def handle_accusation_events(self, event):
        # Handle events for the accusation UI
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.accusation_button.collidepoint(event.pos):
                self.draw_accusation_ui()
            elif self.send_accusation_button.collidepoint(event.pos):
                # Send the accusation tuple to the server
                accusation_tuple = tuple(self.accusation_texts)
                # Assuming you have a method in the ClientGame class to handle sending accusations
                self.game.handle_send_accusation(accusation_tuple)
                # Set the accusation_sent flag to True to hide the UI components
                self.accusation_sent = True

        elif event.type == pygame.KEYDOWN:
            for i, box in enumerate(self.accusation_input_boxes):
                if box.collidepoint(event.pos) and not self.accusation_sent:
                    if event.key == pygame.K_RETURN:
                        # Move to the next input box or send accusation on Enter
                        self.accusation_texts[i] = self.accusation_text[i]
                        if i < 2:
                            self.accusation_texts[i + 1] = self.accusation_text[i + 1]
                    elif event.key == pygame.K_BACKSPACE:
                        # Allow backspace to delete characters
                        self.accusation_texts[i] = self.accusation_texts[i][:-1]
                    else:
                        # Append typed characters to the current input box
                        self.accusation_texts[i] += event.unicode



    def draw_text(self, text, color, rect):
        # Draw text on the specified rectangle
        txt_surface = self.font.render(text, True, color)
        width = max(rect.width, txt_surface.get_width() + 10)
        rect.w = width
        self.screen.blit(txt_surface, (rect.x + 5, rect.y + 5))
        pygame.draw.rect(self.screen, color, rect, 2)


    def update_initial_ui(self):
        """Update the entire game UI."""
        self.screen.fill(COLOR_WHITE)  # Clear the screen with black or any background
        self.board_panel.draw(self.screen)
        pygame.display.flip()  # Update the full display Surface to the screen

    def update_players(self, character, current_location):
        print(f"Start to draw player {character} at location {current_location}")
        square_size = ROOM_SIZE
        font_size = 24

        # Translate board coordinates to screen coordinates
        x = BOARD_START_X + current_location[0] * square_size
        y = BOARD_START_Y + current_location[1] * square_size

        # Define the radius and center of the circle
        circle_radius = square_size // 4
        circle_center = (x + square_size // 2, y + square_size // 2)

        # Generate a random color
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Draw a circle with the random color
        pygame.draw.circle(self.screen, random_color, circle_center, circle_radius)

        # Create a font object
        font = pygame.font.SysFont('Arial', font_size)

        # Render the text
        text = font.render(character, True, (255, 255, 255))  # White text

        # Calculate the position to center the text in the circle
        text_width, text_height = text.get_size()
        text_x = circle_center[0] - text_width // 2
        text_y = circle_center[1] - text_height // 2

        # Draw the text
        self.screen.blit(text, (text_x, text_y))

    def draw_local_player_cards(self, local_cards):

        print(f"local_cards info: {local_cards}")
        # Draw each card in the hand
        for index, card_dict in enumerate(local_cards):
            # Create a Card instance from the dictionary
            card = Card(card_type=card_dict['card_type'],
                        name=card_dict['name'],
                        image_filename=card_dict['image_filename'])

            card_x = CARD_START_X + (index * (CARD_WIDTH + 10))  # Add space between cards
            card_y = CARD_START_Y

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
        texts = ["MOVE", "SUGGESTION", "ACCUSATION", "START GAME"]

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
