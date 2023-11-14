import unittest
from server.server_game import ServerGame


class TestServerGame(unittest.TestCase):

    def test_deal_cards(self):
        game = ServerGame()
        game.add_player('player1', {'name': 'Alice'})
        game.add_player('player2', {'name': 'Bob'})
        game.add_player('player3', {'name': 'Tom'})
        game.start_game()

        # Check if players have cards
        self.assertTrue(len(game.players['player1']['hand']) > 0)
        self.assertTrue(len(game.players['player2']['hand']) > 0)
        self.assertTrue(len(game.players['player3']['hand']) > 0)

        # Add more assertions as needed


if __name__ == '__main__':
    unittest.main()
