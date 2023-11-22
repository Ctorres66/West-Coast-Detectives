import pygame
from client_game import ClientGame
from client_network import ClientNetwork
from client_ui import ClientUI


def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Set the desired window size
    pygame.display.set_caption("Game Title")  # Set your window title

    server_ip = 'Royas-MacBook-Air.local'  # Replace with the actual server IP
    port = 5555  # Assuming this is the port your server is listening on

    # Initialize client components
    network = ClientNetwork(server_ip, port)  # Replace with actual server IP and port
    game = ClientGame(network)
    ui = ClientUI(game)
    clock = pygame.time.Clock()  # Create a clock object to manage frame rate

    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    game.handle_input(event)
                    clicked_button = ui.handle_events(event)

                    if clicked_button == "MOVE":
                        game.handle_move_action()

            game.update()
            ui.update(game.board)
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
