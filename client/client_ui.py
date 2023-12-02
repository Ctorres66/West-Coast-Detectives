# ClientUI only for pygame draw without any data
import pygame
from shared.game_constants import *
from shared.game_entities import Button, Board, Card


class ClientUI:
    def __init__(self, screen, game):
        self.screen = screen
        # initial board
        self.board = Board()
        self.game = game  # This is an instance of the ClientGame class
        self.dropdown_rect = None
        self.dropdown_active = False
        self.dropdown_options = []

        # Initialize the UI components here
        self.board_panel = BoardPanel(
            board=self.board,
            button_panel=ButtonPanel(x=50, y=10),
            notification_box=NotificationBox(x=850, y=100),
        )

    def ui_draw(self, screen):
        # Draw static elements only if the game hasn't started
        if not self.game.game_started:
            self.board_panel.board_panel_draw(screen)

        # Always draw dynamic elements like players
        # Assuming a method to draw players exists
        self.draw_players()

    def clear_players_area(self, player):
        """Clear the areas where players were previously drawn."""
        # Assuming player has an attribute current_location storing their board coordinates
        x, y = player.current_location
        rect_x = BOARD_START_X + x * ROOM_SIZE
        rect_y = BOARD_START_Y + y * ROOM_SIZE
        rect = pygame.Rect(rect_x, rect_y, ROOM_SIZE, ROOM_SIZE)
        self.screen.blit(self.board_panel.board_surface, (rect_x, rect_y), rect)

    def draw_players(self):
        for player_id, player_data in self.game.players.items():
            character = player_data.get('character')
            current_location = player_data.get('current_location')
            # Draw each player
            self.draw_player(character, current_location)

    def draw_player(self, character, current_location):
        square_size = ROOM_SIZE
        font_size = 24

        # Translate board coordinates to screen coordinates
        x = BOARD_START_X + current_location[0] * square_size
        y = BOARD_START_Y + current_location[1] * square_size

        # Define the radius and center of the circle
        circle_radius = square_size // 4
        circle_center = (x + square_size // 2, y + square_size // 2)

        # Generate a random color
        random_color = (0,0,0)

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

    def handle_dropdown_selection(self, pos):
        if not self.dropdown_active:
            return None
        if self.dropdown_rect.collidepoint(pos):
            index = (pos[1] - self.dropdown_rect.y) // OPTION_HEIGHT
            if 0 <= index < len(self.dropdown_options):
                print(f"Dropdown option selected: {self.dropdown_options[index]}")  # Debugging line
                return self.dropdown_options[index]
        return None

    def show_dropdown(self, room_names):
        self.dropdown_active = True
        self.dropdown_options = room_names
        # Position and dimensions for the dropdown
        self.dropdown_rect = pygame.Rect(DROPDOWN_X, DROPDOWN_Y, DROPDOWN_WIDTH, DROPDOWN_HEIGHT)

    def hide_dropdown(self):
        print("Hiding dropdown")  # Debugging line
        self.dropdown_active = False
        self.dropdown_options = []



    def draw_dropdown(self, screen):
        # Initialize font for dropdown
        pygame.font.init()  # Initialize the font module
        font = pygame.font.SysFont('Arial', 24)  # Replace 'Arial' with your font choice

        pygame.draw.rect(screen, DROPDOWN_BG_COLOR, self.dropdown_rect)
        # Draw each dropdown option
        for i, option in enumerate(self.dropdown_options):
            text_surface = font.render(option, True, TEXT_COLOR)
            screen.blit(text_surface, (self.dropdown_rect.x, self.dropdown_rect.y + i * OPTION_HEIGHT))


class BoardPanel:
    def __init__(self, button_panel, notification_box, board):
        self.board = board
        self.button_panel = button_panel
        self.notification_box = notification_box

        # Create a surface for the board
        self.board_surface = pygame.Surface((self.board.cols * ROOM_SIZE, self.board.rows * ROOM_SIZE))
        self.board.board_draw(self.board_surface)

    def board_panel_draw(self, screen):
        screen.fill(COLOR_WHITE)  # Clear the screen with black or any background
        screen.blit(self.board_surface, (BOARD_START_X, BOARD_START_Y))
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
