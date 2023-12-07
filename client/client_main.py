import pygame
from client_game import ClientGame
from client_network import ClientNetwork
from client_ui import ClientUI
from shared.game_constants import PORT, SERVER_IP, SCREEN_WIDTH, SCREEN_HEIGHT


def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set the desired window size
    pygame.display.set_caption("Game Title")  # Set your window title
    # Initialize client components
    network = ClientNetwork(SERVER_IP, PORT)  # Replace with actual server IP and port
    ui = ClientUI(screen)
    game = ClientGame(network, ui)
    ui.set_game(game)
    clock = pygame.time.Clock()  # Create a clock object to manage frame rate

    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    handle_mouse_click(event, game, ui)

            # game logic
            game.update_data()
            ui.ui_draw(screen)
            pygame.display.flip()
            clock.tick(60)

    except KeyboardInterrupt:
        print("Game interrupted by user. Exiting...")

    finally:
        # Cleanup
        network.client.close()
        pygame.quit()
        print("Game closed properly.")


def handle_mouse_click(event, game, ui):
    if game.is_selecting_move:
        clicked_room = ui.handle_events_room(event)
        if clicked_room in game.valid_moves:
            game.handle_room_pick_action(clicked_room)
        else:
            ui.notification_box.add_message("Invalid move. Please select a valid room.")
        return

    clicked_button = ui.handle_events(event)
    if clicked_button == "START GAME":
        game.send_start_game_to_server()

    if game.local_turn_number == game.current_turn_number:
        if clicked_button == "MOVE":
            game.handle_move_action()
        elif clicked_button == "SUGGESTION":
            ui.draw_suggestion_ui()
            game.handle_suggestion_action()
        elif clicked_button == "ACCUSATION":
            ui.draw_accusation_ui()
            game.handle_accusation_action()
    else:
        print("It's not your turn.")
        ui.notification_box.add_message("It's not your turn.")


if __name__ == '__main__':
    main()
