from unittest.mock import Mock, patch

from dash import dcc, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from parameterized import parameterized

from Callbacks.CallbackBase import CallbackBase
from Callbacks.GameDetailsPage.LoadGameDetailsPlayerModal import (
    LoadGameDetailsPlayerModal,
)
from Callbacks.GameDetailsPage.LoadGameDetailsGraph import LoadGameDetailsGraph
from Callbacks.GameDetailsPage.LoadGameDetailsPlayers import LoadGameDetailsPlayers
from Callbacks.GameDetailsPage.LoadGameDetailsStatistics import (
    LoadGameDetailsStatistics,
)
from Callbacks.GameDetailsPage.LoadGameDetailsTitle import LoadGameDetailsTitle
from CallbacksTests.CallbacksBaseTests import CallbacksBaseTests
from Models.DartScore import DOUBLE
from Models.Game import Game
from Models.Leg import Leg
from Models.Player import Player
from Models.TypeSetLeg import FIRST_TO, TypeSetLeg


class GameDetailsPageCallbacksTest(CallbacksBaseTests):
    def setUp(self) -> None:
        super().setUp()

    def test_load_game_details_graph(self) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_data)
        callback_class = LoadGameDetailsGraph(self.dependency_mock)
        game = game_simulation.run()
        game.sets[0].legs.append(
            Leg(
                players=[Player('Player1')],
                set_instance=set,
                leg_type=TypeSetLeg(FIRST_TO),
                points=501,
                out=DOUBLE,
            )
        )
        callback_class.get_last_version_of_game_key = Mock()
        callback_class.get_last_version_of_game_key.return_value = game

        # Act
        response = callback_class.callback('/database/game-details/1711979685.758767')

        # Assert
        self.assertEqual(len(response), 1)
        self.assertTrue(isinstance(response[0], dcc.Graph))

    def test_load_game_details_graph_no_leg_finished(self) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_data)
        callback_class = LoadGameDetailsGraph(self.dependency_mock)
        callback_class.get_last_version_of_game_key = Mock()
        callback_class.get_last_version_of_game_key.return_value = game_simulation.run()

        # Act
        response = callback_class.callback('/database/game-details/1711979685.758767')

        # Assert
        self.assertEqual(len(response), 1)
        self.assertTrue(response[0].children == '📈 No Legs finished in this Game!')

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

    def test_load_game_details_statistics(self) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_data)
        callback_class = LoadGameDetailsStatistics(self.dependency_mock)
        callback_class.get_last_version_of_game_key = Mock()
        callback_class.get_last_version_of_game_key.return_value = game_simulation.run()

        # Act
        response = callback_class.callback(
            '/database/game-details/1711979685.758767', {}
        )

        # Assert
        self.assertEqual(len(response), 2)
        self.assertTrue(isinstance(response[0], html.Div))

    def test_load_game_details_statistics_call_on_other_page(self) -> None:
        # Arrange
        callback_class = LoadGameDetailsStatistics(self.dependency_mock)

        # Act & Assert
        with self.assertRaises(PreventUpdate):
            callback_class.callback('/scoreboard', {})

    def test_load_game_details_statistics_of_finished_game(self) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_data)
        simulated_game = game_simulation.run()
        simulated_game.winner = Player(name='John Doe')
        callback_class = LoadGameDetailsStatistics(self.dependency_mock)
        callback_class.get_last_version_of_game_key = Mock()
        callback_class.get_last_version_of_game_key.return_value = simulated_game

        # Act
        response = callback_class.callback(
            '/database/game-details/1711979685.758767', {}
        )

        # Assert
        self.assertEqual(len(response), 2)
        self.assertTrue(isinstance(response[0], html.Div))

    def test_load_game_details_statistics_of_game_in_progress(self) -> None:
        # Arrange
        game_simulation = self.simulation(self.simulation_data)
        simulated_game = game_simulation.run()
        dependency_mock = self.dependency_mock.copy()
        dependency_mock.game = simulated_game
        callback_class = LoadGameDetailsStatistics(dependency_mock)
        callback_class.get_last_version_of_game_key = Mock()
        callback_class.get_last_version_of_game_key.return_value = simulated_game

        # Act
        response = callback_class.callback(
            '/database/game-details/1711979685.758767', {}
        )

        # Assert
        self.assertEqual(len(response), 2)
        self.assertTrue(isinstance(response[0], html.Div))


class GameDetailsPlayersCallbackTests(CallbacksBaseTests):
    def setUp(self) -> None:
        super().setUp()
        self.game_simulation = self.simulation(self.simulation_data)

    def test_load_game_details_players(self) -> None:
        self.callback_class = LoadGameDetailsPlayers(self.dependency_mock)
        self.callback_class.get_last_version_of_game_key = Mock()
        self.callback_class.get_last_version_of_game_key.return_value = (
            self.game_simulation.run()
        )

        response = self.callback_class.callback(
            '/database/game-details/1711979685.758767', {}
        )

        self.assertEqual(len(response), 2)
        self.assertTrue(isinstance(response[0][0], dbc.Card))

    @patch('Callbacks.GameDetailsPage.LoadGameDetailsPlayerModal.callback_context')
    def test_load_game_details_player_modals(self, ctx_mock: Mock) -> None:
        self.callback_class = LoadGameDetailsPlayerModal(self.dependency_mock)
        self.callback_class.get_last_version_of_game_key = Mock()
        self.callback_class.get_last_version_of_game_key.return_value = (
            self.game_simulation.run()
        )

        ctx_mock.triggered = [
            {
                'prop_id': f'{{"index":"{self.game_simulation.game.players[0].id}","type":"game-details-player-button"}}.n_clicks'
            }
        ]

        response = self.callback_class.callback(
            '/database/game-details/1711979685.758767', [0, 1]
        )

        assert isinstance(response[0], dbc.Modal)

    @patch('Callbacks.GameDetailsPage.LoadGameDetailsPlayerModal.callback_context')
    def test_load_game_details_player_modal_no_dart_thrown(
        self, ctx_mock: Mock
    ) -> None:
        game = Game(players=[Player('Player1'), Player('Player2')])
        self.callback_class = LoadGameDetailsPlayerModal(self.dependency_mock)
        self.callback_class.get_last_version_of_game_key = Mock()
        self.callback_class.get_last_version_of_game_key.return_value = game

        ctx_mock.triggered = [
            {
                'prop_id': f'{{"index":"{game.players[0].id}","type":"game-details-player-button"}}.n_clicks'
            }
        ]

        response = self.callback_class.callback(
            '/database/game-details/1711979685.758767', [0, 1]
        )

        assert isinstance(response[0], dbc.Modal)

    @parameterized.expand(
        [
            (LoadGameDetailsPlayers,),
            (LoadGameDetailsPlayerModal,),
        ]
    )
    def test_call_on_other_page(self, callback_class: CallbackBase) -> None:
        with self.assertRaises(PreventUpdate):
            callback_class(self.dependency_mock).callback('/scoreboard', Mock())
