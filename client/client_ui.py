import pygame
from shared.game_constants import *
from shared.game_entities import Button, Board, Card


class ClientUI:
    def __init__(self, screen):
        self.screen = screen
        self.game = None  # This is an instance of the ClientGame class
        self.room_active = False

        # Create a surface for the board
        self.board_surface = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
        # initial board
        self.board = Board()
        self.button_panel = ButtonPanel()
        self.notification_box = NotificationBox()

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

    def set_game(self, game):
        self.game = game

    def ui_draw(self, screen):
        print(f"rerender")
        # Clear the screen
        self.screen.fill(COLOR_WHITE)
        # Draw the board first
        self.board.draw_rooms(self.board_surface)
        # Now draw the border on the board surface
        pygame.draw.rect(self.board_surface, COLOR_BLACK, self.board_surface.get_rect(), 2)
        # Blit the board surface (with the board and border) to the screen
        screen.blit(self.board_surface, (BOARD_START_X, BOARD_START_Y))
        # Draw players and other UI elements
        self.draw_players()
        self.button_panel.button_draw(self.screen)
        self.notification_box.notification_draw(self.screen)

        # Update the display
        pygame.display.flip()

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

    def draw_players(self):
        for player_id, player_info in self.game.players.items():
            character = player_info.get('character')
            current_location = player_info.get('current_location')
            # Draw each player
            self.draw_player(character, current_location, player_id)

            if player_id == self.game.local_player_id:
                local_cards = player_info.get('cards')
                self.draw_local_player_cards(local_cards)

    def draw_player(self, character, current_location, player_id):
        square_size = ROOM_SIZE
        font_size = 24

        # Translate board coordinates to screen coordinates
        x = BOARD_START_X + current_location[0] * square_size
        y = BOARD_START_Y + current_location[1] * square_size

        # Check if current location is a room and mark it as occupied
        for row in self.board.grid:
            for room in row:
                if room is not None and room.coord == current_location:
                    room.occupied = True
                    break

        # Define the radius and center of the circle
        circle_radius = square_size // 4
        circle_center = (x + square_size // 2, y + square_size // 2)

        player_color = COLOR_BLACK
        if player_id == self.game.local_player_id:
            player_color = COLOR_PURPLE

        # Draw a circle with the random color
        pygame.draw.circle(self.screen, player_color, circle_center, circle_radius)

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
        # Draw each card in the hand
        for index, card_dict in enumerate(local_cards):
            # Create a Card instance from the dictionary
            card = Card(card_type=card_dict['card_type'],
                        card_name=card_dict['card_name'],
                        card_image=card_dict['card_image'])

            card_x = CARD_START_X + (index * (CARD_WIDTH + 10))  # Add space between cards
            card_y = CARD_START_Y

            # Assuming the Card class has a draw method
            card.card_draw(self.screen, (card_x, card_y))

    def handle_events(self, event):
        """Handle UI-related events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_button = self.button_panel.check_click(event)
            if clicked_button:
                # Handle the button click event
                print(f"{clicked_button} was clicked")
                return clicked_button
        return None

    def handle_events_room(self, event):
        print(f"ui handle event")
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"clicked")
            clicked_board = self.check_room_click(event)
            print(f"clicked room is : {clicked_board}")
            if clicked_board:
                # Handle the button click event
                print(f"{clicked_board} was clicked")
                return clicked_board
        return None

    def check_room_click(self, event):
        print(f" start to check board click")
        for row in self.board.grid:
            for room in row:
                if room is not None:
                    print(f"room = {room.coord}, and room is click or not: {room.room_is_clicked(event)}")
                    if room.room_is_clicked(event):
                        print(f"{room.coord} room was clicked")
                        return room.coord
        return None

    def highlight_valid_moves(self, valid_moves_coords):
        print(f"start draw highlight rooms")
        # Set highlight for valid move locations
        for coords in valid_moves_coords:
            for row in self.board.grid:
                for room in row:
                    if room is not None and room.coord == coords:
                        room.highlight = True  # Highlight the room

    def reset_room_highlight(self):
        print(f"reset highlight rooms")
        # Reset highlights
        for row in self.board.grid:
            for room in row:
                if room is not None:
                    room.highlight = False  # Reset existing highlights


class ButtonPanel:
    def __init__(self):
        self.buttons = []
        colors = [(239, 244, 248), (192, 211, 228), (243, 219, 233), (149, 155, 189), (149, 155, 149)]
        texts = ["START GAME", "MOVE", "SUGGESTION", "ACCUSATION", "END TURN"]

        for i, (color, text) in enumerate(zip(colors, texts)):
            # Calculate the y position for each button
            y = BUTTON_START_Y + i * (BUTTON_HEIGHT + BUTTON_MARGIN)
            button = Button(BUTTON_START_X, y, text, color)
            self.buttons.append(button)

    def button_draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def check_click(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                print(f"{button.text} button was clicked")
                return button.text
        return None


class NotificationBox:
    def __init__(self, width=BOX_WIDTH, height=BOX_HEIGHT):
        self.rect = pygame.Rect(BOX_START_X, BOX_START_Y, width, height)
        self.color = COLOR_GRAY
        self.messages = ["Game Start!"]
        self.latest_message = None

    def add_message(self, message):
        self.messages.append(message)
        self.latest_message = message
        self.messages = self.messages[-8:]  # Keep only the last 8 messages

    def notification_draw(self, screen):
        # Draw the notification box
        pygame.draw.rect(screen, self.color, self.rect)
        # Display the messages
        font = pygame.font.SysFont('arial', 24)
        if self.latest_message:
            text_surface = font.render(self.latest_message, True, (0, 0, 0))
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5 + (len(self.messages) - 1) * 20))
