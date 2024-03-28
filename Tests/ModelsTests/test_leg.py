from parameterized import parameterized

from Models.DartScore import DOUBLE, SINGLE, TRIPLE
from ModelsTests.ModelsBaseTests import ModelsBaseTests


class LegTest(ModelsBaseTests):
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
        set_instance = game.get_current_set()
        leg_instance = set_instance.get_current_leg()

        # Act
        score_count = leg_instance.get_score_count(attribute, desired_val, player_instance)

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
        set_instance = game.get_current_set()
        leg_instance = set_instance.get_current_leg()

        # Act
        possible_checkouts, successful_checkouts = leg_instance.get_possible_and_successful_checkouts(player)

        # Assert
        self.assertEqual(possible_checkouts, actual_possible_checkouts)
        self.assertEqual(successful_checkouts, actual_successful_checkouts)

    @parameterized.expand([
        ['Player1', 79],
        ['Player2', 34],
        ['Player3', 49]
    ])
    def test_get_avg_score(self, player_name: str, actual_avg: int) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_avg_data)

        # Act
        game = game_simulation.run()
        set_instance = game.get_current_set()
        leg_instance = set_instance.get_current_leg()
        avg_player = leg_instance.get_avg_score(game_simulation.players[player_name])

        # Assert
        self.assertEqual(avg_player, actual_avg)

    def test_get_avg_score_while_no_dart_is_thrown(self) -> None:
        # Arrange
        game_simulation = self.simulation({'Player1': [], 'Player2': []})

        # Act
        game = game_simulation.run()
        set_instance = game.get_current_set()
        leg_instance = set_instance.get_current_leg()
        avg_score = leg_instance.get_avg_score(game_simulation.players['Player1'])

        # Assert
        self.assertEqual(avg_score, None)
