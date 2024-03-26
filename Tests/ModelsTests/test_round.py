from Errors import AllTurnsFinishedError, AlreadyFinishedError
from Models.DartScore import DOUBLE, DartScore, SINGLE, TRIPLE
from ModelsTests.ModelsBaseTests import ModelsBaseTests


class TestRound(ModelsBaseTests):
    def setUp(self) -> None:
        super().setUp()
        self.begin_next_turn_simulation_data = {
            'Player1': [
                (DartScore(17, DOUBLE), DartScore(5, TRIPLE), DartScore(15, SINGLE))
            ],
            'Player2': [
                (DartScore(6, TRIPLE), DartScore(15, DOUBLE), DartScore(7, SINGLE))
            ],
            'Player3': [
                (DartScore(2, TRIPLE), DartScore(10, SINGLE))
            ]
        }

    def test_begin_next_turn_while_player_has_not_finished(self) -> None:
        # Arrange
        game_simulation = self.simulation(self.begin_next_turn_simulation_data)
        game = game_simulation.run()

        # Act
        current_set = game.get_current_set()
        current_leg = current_set.get_current_leg()
        current_round = current_leg.get_current_round()

        # Assert
        with self.assertRaises(AlreadyFinishedError):
            current_round.begin_next_turn()

    def test_begin_new_turn_while_all_players_have_finished(self) -> None:
        game_simulation = self.simulation(self.begin_next_turn_simulation_data)
        game = game_simulation.run()

        # Act
        current_set = game.get_current_set()
        current_leg = current_set.get_current_leg()
        current_round = current_leg.get_current_round()
        current_turn = current_round.get_current_turn()
        current_turn.throw_dart(DartScore(5, DOUBLE))
        current_turn.finish()

        # Assert
        with self.assertRaises(AllTurnsFinishedError):
            current_round.begin_next_turn()
