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
        player_count_at_location = {}
        for player_id, player_info in self.game.players.items():
            current_location = player_info.get('current_location')
            character = player_info.get('character')
            if current_location not in player_count_at_location:
                player_count_at_location[current_location] = 0
            else:
                player_count_at_location[current_location] += 1
            # Draw each player
            self.draw_player(character, current_location, player_id, player_count_at_location[current_location])
            if player_id == self.game.local_player_id:
                local_cards = player_info.get('cards')
                self.draw_local_player_cards(local_cards)

    def draw_player(self, character, current_location, player_id, num_players_already_draw):
        # Fixed vertical offset for each player
        vertical_offset = ROOM_SIZE // 6 * num_players_already_draw + 6

        # Define the text properties
        font = pygame.font.SysFont('Arial', 11)
        font.set_bold(True)
        text = font.render(character, True, COLOR_WHITE)
        text_width, text_height = text.get_size()

        # Calculate the x and y positions for the rectangle, text, and circle
        x = BOARD_START_X + current_location[1] * ROOM_SIZE
        y = BOARD_START_Y + current_location[0] * ROOM_SIZE + vertical_offset

        rect_x = x + 6
        rect_y = y
        rect_height = ROOM_SIZE // 6 - 2
        rect_color = COLOR_BLACK
        if player_id == self.game.local_player_id:
            rect_color = COLOR_PURPLE
        pygame.draw.rect(self.screen, rect_color, (rect_x, rect_y, ROOM_SIZE - 12, rect_height))

        # Position for the text
        text_x = rect_x + 6
        text_y = rect_y + (rect_height - text_height) // 2

        # Draw the character's name inside the rectangle
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
                return clicked_button
        return None

    def handle_events_room(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_board = self.check_room_click(event)
            if clicked_board:
                # Handle the button click event
                return clicked_board
        return None

    def check_room_click(self, event):
        for row in self.board.grid:
            for room in row:
                if room is not None:
                    print(f"room = {room.coord}, and room is click or not: {room.room_is_clicked(event)}")
                    if room.room_is_clicked(event):
                        print(f"{room.coord} room was clicked")
                        return room.coord
        return None

    def highlight_valid_moves(self, valid_moves_coords):
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
    def __init__(self):
        self.rect = pygame.Rect(BOX_START_X, BOX_START_Y, BOX_WIDTH, BOX_HEIGHT)
        self.color = COLOR_GRAY
        self.messages = ["Game Start!"]

    def add_message(self, message):
        self.messages.append(message)
        self.messages = self.messages[-20:]  # Keep only the last 8 messages

    def notification_draw(self, screen):
        # Draw the notification box
        pygame.draw.rect(screen, self.color, self.rect)

        # Display the messages
        font = pygame.font.SysFont('arial', 15)
        line_height = 20  # Adjust as needed for spacing between lines
        start_x = self.rect.x + 5  # Slight offset from the left edge of the box
        start_y = self.rect.y + 5  # Slight offset from the top edge of the box
        max_text_width = self.rect.width - 10  # Width of text area

        current_y = start_y
        for message in self.messages:
            wrapped_lines = self.wrap_text(message, font, max_text_width)
            for line in wrapped_lines:
                # Render the message line
                text = font.render(line, True, COLOR_BLACK)  # Use COLOR_BLACK or any other desired text color
                screen.blit(text, (start_x, current_y))
                current_y += line_height
                if current_y > self.rect.bottom:  # Stop if we run out of space
                    return

    def wrap_text(self, text, font, max_width):
        """Wrap text to fit into the specified width."""
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            text_size = font.size(test_line)
            if text_size[0] > max_width:
                lines.append(current_line)
                current_line = word + ' '
            else:
                current_line = test_line
        lines.append(current_line)  # Add the last line
        return lines
