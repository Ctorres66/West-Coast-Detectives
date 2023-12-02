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
    game = ClientGame(network)
    ui = ClientUI(screen, game)
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
            # clock.tick(60)

    except KeyboardInterrupt:
        print("Game interrupted by user. Exiting...")

    finally:
        # Cleanup
        network.client.close()
        pygame.quit()
        print("Game closed properly.")


def handle_mouse_click(event, game, ui):
    if ui.dropdown_active:
        selected_move = ui.handle_dropdown_selection(event.pos)
        if selected_move:
            game.send_move_to_server(selected_move)
            ui.hide_dropdown()
            ui.draw()
    else:
        clicked_button = ui.handle_events(event)
        if clicked_button == "START GAME":
            game.send_start_game_to_server()
        elif clicked_button == "MOVE":
            game.handle_move_action()


if __name__ == '__main__':
    main()
