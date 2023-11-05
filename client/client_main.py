import pygame

# Make sure the import paths are correct based on your project structure.
from client_game import ClientGame
from client_network import ClientNetwork
from client_ui import ClientUI


def main():
    pygame.init()
    # Assuming your server IP and port are correct
    network = ClientNetwork('10.0.0.61', 5555)
    game = ClientGame(network)
    ui = ClientUI(game)  # Pass the game instance to the UI

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle other events like key presses, mouse movements, etc.

        # Network communication
        # Send and receive data here if needed, for example:
        # server_response = network.send("Your data here")
        # Update the game state based on server_response, if applicable

        # UI and game state updates
        game.update()
        ui.draw()

        pygame.display.flip()  # Update the full display Surface to the screen
        pygame.time.Clock().tick(60)  # Maintain 60 frames per second

    # When you're done running, you should properly close the network connection
    network.client.close()
    pygame.quit()


if __name__ == '__main__':
    main()
