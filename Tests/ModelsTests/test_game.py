from parameterized import parameterized

from Models.DartScore import DOUBLE, SINGLE, TRIPLE
from Tests.ModelsTests.ModelsBaseTests import ModelsBaseTests


class GameTests(ModelsBaseTests):
    @parameterized.expand([
        ['Player1', 79],
        ['Player2', 34],
        ['Player3', 52]
    ])
    def test_get_avg_score(self, player_name: str, actual_avg: int) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_avg_data)

        # Act
        game = game_simulation.run()
        avg_player = game.get_avg_score(game_simulation.players[player_name])

        # Assert
        self.assertEqual(avg_player, actual_avg)

    @parameterized.expand([
        ['multiplier', 'Player1', SINGLE, 3],
        ['multiplier', 'Player2', DOUBLE, 3],
        ['multiplier', 'Player3', TRIPLE, 3],
        ['score', 'Player1', 2, 1],
        ['score', 'Player2', 4, 1],
        ['score', 'Player3', 6, 1]
    ])
    def test_score_count(self, attribute: str, player: str, desired_val: int, counted_val: int) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_data)
        player_instance = game_simulation.players[player]
        game = game_simulation.run()

        # Act
        score_count = game.get_score_count(attribute, desired_val, player_instance)

        # Assert
        self.assertEqual(score_count, counted_val)

    @parameterized.expand([
        ['Player1', 2, 0],
        ['Player2', 2, 0],
        ['Player3', 4, 1]
    ])
    def test_get_possible_and_successful_checkouts(self, player_name: str, actual_possible_checkouts: int,
                                                   actual_successful_checkouts: int) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_checkout_data)
        player = game_simulation.players[player_name]
        game = game_simulation.run()

        # Act
        possible_checkouts, successful_checkouts = game.get_possible_and_successful_checkouts(player)

        # Assert
        self.assertEqual(possible_checkouts, actual_possible_checkouts)
        self.assertEqual(successful_checkouts, actual_successful_checkouts)
