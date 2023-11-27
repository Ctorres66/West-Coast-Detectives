import pygame
from client_game import ClientGame
from client_network import ClientNetwork
from client_ui import ClientUI
from shared.game_constants import PORT, SERVER_IP


def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Set the desired window size
    pygame.display.set_caption("Game Title")  # Set your window title
    # Initialize client components
    network = ClientNetwork(SERVER_IP, PORT)  # Replace with actual server IP and port
    ui = ClientUI()
    game = ClientGame(network, ui)

    ui.update_initial_ui()
    clock = pygame.time.Clock()  # Create a clock object to manage frame rate

    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     # Check if the Start Game button is clicked
                #     if ui.start_button.is_clicked(event.pos):
                #         game.start_game()
                #
                #     # Check if the Move button is clicked
                #     elif ui.move_button.is_clicked(event.pos):
                #         game.move_player()

                # if start_button.collidepoint(event.pos):
                #     # Send a 'start game' signal to the server
                #     # Assuming you have a socket connection 's' already established
                #     s.sendall("START_GAME".encode())

                else:
                    game.handle_input(event)
                    clicked_button = ui.handle_events(event)

                    if clicked_button == "START GAME":
                        game.handle_start_game()
                    elif clicked_button == "MOVE":
                        game.handle_move_action()

            # game logic
            game.update_data()
            pygame.display.flip()
            clock.tick(60)

    except KeyboardInterrupt:
        print("Game interrupted by user. Exiting...")

    finally:
        # Cleanup
        network.client.close()
        pygame.quit()
        print("Game closed properly.")


if __name__ == '__main__':
    main()
