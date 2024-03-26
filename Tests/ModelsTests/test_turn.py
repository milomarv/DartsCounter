from Errors import NotAllDartsThrownYetError
from ModelsTests.ModelsBaseTests import ModelsBaseTests


class TestTurn(ModelsBaseTests):
    def test_finishing_turn_but_not_all_darts_thrown_yet(self) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_turn_data)
        game = game_simulation.run()

        # Act
        current_set = game.get_current_set()
        current_leg = current_set.get_current_leg()
        current_round = current_leg.get_current_round()
        current_turn = current_round.get_current_turn()

        # Assert
        with self.assertRaises(NotAllDartsThrownYetError):
            current_turn.finish()

    def test_get_thrown_darts(self) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_turn_data)
        game = game_simulation.run()

        # Act
        current_set = game.get_current_set()
        current_leg = current_set.get_current_leg()
        current_round = current_leg.get_current_round()
        current_turn = current_round.get_current_turn()
        thrown_darts = current_turn.get_thrown_darts()

        # Assert
        self.assertEqual(thrown_darts, 2)
