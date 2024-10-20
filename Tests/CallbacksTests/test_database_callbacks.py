from unittest.mock import Mock

from dash import html
from dash.exceptions import PreventUpdate

from Callbacks.DatabasePage.ContinueGameModal import ContinueGameModal
from Callbacks.DatabasePage.DeleteGameModal import DeleteGameModal
from Callbacks.DatabasePage.LoadGames import LoadGames
from CallbacksTests.CallbacksBaseTests import CallbacksBaseTests
from Models.Game import Game


class DatabaseCallbacksTest(CallbacksBaseTests):
    # noinspection PyPep8Naming
    def setUp(self) -> None:
        super().setUp()
        self.url = '/database'
        self.frame_style = {
            'height': '30rem',
            'display': 'flex',
            'flex-wrap': 'wrap',
            'align-content': 'center',
            'justify-content': 'center',
        }

    def test_load_games_old_version_with_no_initial_player_alignment(self) -> None:
        game_simulation = self.simulation(self.simulation_data)
        game = game_simulation.run()
        del game.initial_player_alignment
        self.dependency_mock.games_repository.load.return_value = game
        self.dependency_mock.games_repository.list_games.return_value = [
            '1711631564.271273',
            '1711652784.985871',
            '1711652844.830463',
        ]
        self.dependency_mock.games_repository.list_versions.return_value = [
            '1711716794.867666',
            '1711716802.085491',
            '1711716803.288263',
            '1711716810.73072',
            '1711716811.613999',
            '1711716833.329125',
        ]
        callback_class = LoadGames(self.dependency_mock)

        response = callback_class.callback(self.url, 0, 0, self.frame_style)
        assert response

    def test_load_games_currently_running(self) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_data)
        game = game_simulation.run()
        self.dependency_mock.games_repository.load.return_value = game
        self.dependency_mock.games_repository.list_games.return_value = [
            '1711631564.271273',
            '1711652784.985871',
            '1711652844.830463',
        ]
        self.dependency_mock.games_repository.list_versions.return_value = [
            '1711716794.867666',
            '1711716802.085491',
            '1711716803.288263',
            '1711716810.73072',
            '1711716811.613999',
            '1711716833.329125',
        ]
        self.dependency_mock.game = game
        callback_class = LoadGames(self.dependency_mock)

        # Act
        response = callback_class.callback(self.url, 0, 0, self.frame_style)

        progress_content = response[0][0].children[1].children[0].children[0]
        assert progress_content.children.children[1].children.children == 'In Progress'

    def test_load_games_with_was_already_deleted(self) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_data)
        self.dependency_mock.games_repository.load.return_value = game_simulation.run()
        self.dependency_mock.games_repository.list_games.return_value = [
            '1711631564.271273',
            '1711652784.985871',
            '1711652844.830463',
        ]
        self.dependency_mock.games_repository.list_versions.side_effect = ValueError()
        callback_class = LoadGames(self.dependency_mock)

        # Act
        response = callback_class.callback(self.url, 0, 0, self.frame_style)

        # Assert
        self.assertTrue(len(response) == 3)
        self.assertTrue(len(response[0]) == 0)
        # noinspection PyTypeChecker
        self.assertEqual(response[1]['width'], None)
        self.assertEqual(response[2], {})

    def test_load_games_with_winner(self) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_data)
        game = game_simulation.run()
        game.winner = game.players[0]
        self.dependency_mock.games_repository.load.return_value = game
        self.dependency_mock.games_repository.list_games.return_value = [
            '1711631564.271273',
            '1711652784.985871',
            '1711652844.830463',
        ]
        self.dependency_mock.games_repository.list_versions.return_value = [
            '1711716794.867666',
            '1711716802.085491',
            '1711716803.288263',
            '1711716810.73072',
            '1711716811.613999',
            '1711716833.329125',
        ]
        callback_class = LoadGames(self.dependency_mock)

        response = callback_class.callback(self.url, 0, 0, self.frame_style)

        winner_content = response[0][0].children[1].children[0].children[1]
        assert winner_content.children.children[1].children.children == 'Player1'

    def test_load_games_triggered_when_database_page_is_not_loaded(self) -> None:
        # Arrange
        callback_class = LoadGames(self.dependency_mock)

        # Act & Assert
        with self.assertRaises(PreventUpdate):
            callback_class.callback('/other_url', 0, 0, self.frame_style)

    def test_open_delete_game_modal(self) -> None:
        # Arrange
        callback_class = DeleteGameModal(self.dependency_mock)
        callback_class.get_prop_from_context = Mock()
        callback_class.get_prop_from_context.return_value = {
            'index': '1711733259.033643',
            'type': 'game-entry-delete-button',
        }
        callback_class.operations = Mock()
        callback_class.operations.format_game_ts_pretty.return_value = (
            '18:27 - 29.Mar.2024'
        )

        delete_clicks = [1, None, None, None]

        # Act
        response = callback_class.callback(delete_clicks, 0, None)

        # Arrange
        self.assertTrue(len(response) == 3)
        self.assertTrue(response[0])
        self.assertTrue(isinstance(response[1], html.Div))
        self.assertEqual('1711733259.033643', response[2])

    def test_open_delete_game_modal_initial_call(self) -> None:
        # Arrange
        callback_class = DeleteGameModal(self.dependency_mock)
        callback_class.get_prop_from_context = Mock()
        callback_class.get_prop_from_context.return_value = {
            'index': '1711733259.033643',
            'type': 'game-entry-delete-button',
        }
        callback_class.operations = Mock()
        callback_class.operations.format_game_ts_pretty.return_value = (
            '18:27 - 29.Mar.2024'
        )

        delete_clicks = [None, None, None, None]

        # Act & Arrange
        with self.assertRaises(PreventUpdate):
            callback_class.callback(delete_clicks, 0, None)

    def test_delete_game(self) -> None:
        # Arrange
        callback_class = DeleteGameModal(self.dependency_mock)
        callback_class.get_prop_from_context = Mock()
        callback_class.get_prop_from_context.return_value = 'delete-game-confirm-button'
        callback_class.games_repository = Mock()

        delete_clicks = [1, None, None, None]

        # Act
        response = callback_class.callback(delete_clicks, 1, '1711733259.033643')

        # Arrange
        self.assertTrue(len(response) == 3)
        self.assertFalse(response[0])
        self.assertIsNone(response[1])
        self.assertIsNone(response[2])
        callback_class.games_repository.delete_game.assert_called_once_with(
            '1711733259.033643'
        )

    def test_open_continue_game_modal(self) -> None:
        # Arrange
        callback_class = ContinueGameModal(self.dependency_mock)
        callback_class.get_prop_from_context = Mock()
        callback_class.get_prop_from_context.return_value = {
            'index': '1711733259.033643',
            'type': 'game-entry-delete-button',
        }
        callback_class.operations = Mock()
        callback_class.operations.format_game_ts_pretty.return_value = (
            '18:27 - 29.Mar.2024'
        )

        continue_clicks = [1, None, None, None]

        # Act
        response = callback_class.callback(continue_clicks, 0, None)

        # Arrange
        self.assertTrue(len(response) == 3)
        self.assertTrue(response[0])
        self.assertTrue(isinstance(response[1], html.Div))
        self.assertEqual('1711733259.033643', response[2])

    def test_open_continue_game_modal_initial_call(self) -> None:
        # Arrange
        callback_class = ContinueGameModal(self.dependency_mock)
        callback_class.get_prop_from_context = Mock()
        callback_class.get_prop_from_context.return_value = {
            'index': '1711733259.033643',
            'type': 'game-entry-delete-button',
        }
        callback_class.operations = Mock()
        callback_class.operations.format_game_ts_pretty.return_value = (
            '18:27 - 29.Mar.2024'
        )

        continue_clicks = [None, None, None, None]

        # Act & Arrange
        with self.assertRaises(PreventUpdate):
            callback_class.callback(continue_clicks, 0, None)

    def test_continue_game(self) -> None:
        # Arrange
        callback_class = ContinueGameModal(self.dependency_mock)
        callback_class.get_prop_from_context = Mock()
        callback_class.get_prop_from_context.return_value = (
            'continue-game-confirm-button'
        )

        callback_class.games_repository = Mock()
        callback_class.games_repository.list_versions.return_value = [
            '1711716794.867666',
            '1711716802.085491',
            '1711716803.288263',
            '1711716810.73072',
            '1711716811.613999',
            '1711716833.329125',
        ]
        callback_class.games_repository.load.return_value = Game(
            ts=1711733259.033643, version=1711716833.329125
        )

        callback_class.game = Game()

        continue_clicks = [1, None, None, None]

        # Act
        response = callback_class.callback(continue_clicks, 1, '1711733259.033643')

        # Assert
        self.assertTrue(len(response) == 3)
        self.assertFalse(response[0])
        self.assertIsNone(response[1])
        self.assertIsNone(response[2])
        callback_class.games_repository.load.assert_called_once_with(
            '1711733259.033643', '1711716833.329125'
        )
        self.assertEqual(callback_class.game.ts, 1711733259.033643)
        self.assertEqual(callback_class.game.version, 1711716833.329125)
        self.assertTrue(callback_class.game.started)
