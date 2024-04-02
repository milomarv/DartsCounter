from unittest.mock import Mock

from dash import dcc
from dash.exceptions import PreventUpdate

from Callbacks.GameDetailsPage.LoadGameDetailsGraph import LoadGameDetailsGraph
from Callbacks.GameDetailsPage.LoadGameDetailsTitle import LoadGameDetailsTitle
from CallbacksTests.CallbacksBaseTests import CallbacksBaseTests


class GameDetailsPageCallbacksTest(CallbacksBaseTests):
    def setUp(self) -> None:
        super().setUp()

    def test_load_game_details_graph(self) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_data)
        callback_class = LoadGameDetailsGraph(self.dependency_mock)
        callback_class.get_last_version_of_game_key = Mock()
        callback_class.get_last_version_of_game_key.return_value = game_simulation.run()

        # Act
        response = callback_class.callback('/database/game-details/1711979685.758767')

        # Assert
        self.assertEqual(len(response), 1)
        self.assertTrue(isinstance(response[0], dcc.Graph))

    def test_load_game_details_graph_call_on_other_page(self) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_data)
        callback_class = LoadGameDetailsGraph(self.dependency_mock)
        callback_class.get_last_version_of_game_key = Mock()
        callback_class.get_last_version_of_game_key.return_value = game_simulation.run()

        # Act & Assert
        with self.assertRaises(PreventUpdate):
            callback_class.callback('/scoreboard')

    def test_load_game_details_title(self) -> None:
        # Arrange
        callback_class = LoadGameDetailsTitle(self.dependency_mock)

        # Act
        response = callback_class.callback('/database/game-details/1711979685.758767')

        # Assert
        self.assertEqual(1, len(response))
        self.assertTrue(isinstance(response[0], list))

    def test_load_game_details_title_call_on_other_page(self) -> None:
        # Arrange
        callback_class = LoadGameDetailsTitle(self.dependency_mock)

        # Act & Assert
        with self.assertRaises(PreventUpdate):
            callback_class.callback('/scoreboard')
