import pygame

# Make sure the import paths are correct based on your project structure.
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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle other events like key presses, mouse movements, etc.
            else:
                # Delegate other event handling to the game logic
                game.handle_input(event)
                ui.handle_events(event)

        # Network communication
        game.update()
        ui.update(game.board)

        # Update the display
        pygame.display.flip()

        # Maintain a frame rate
        clock.tick(60)

    # When you're done running, you should properly close the network connection
    network.client.close()
    pygame.quit()


if __name__ == '__main__':
    main()
