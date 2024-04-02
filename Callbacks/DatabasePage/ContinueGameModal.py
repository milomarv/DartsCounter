from dash import html
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger
from Models.ModelsOperations import ModelsOperations


class ContinueGameModal(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [
            Input({'type': 'game-entry-continue-button', 'index': ALL}, 'n_clicks'),
            Input('continue-game-confirm-button', 'n_clicks')
        ]
        self.outputs = [
            Output('continue-game-confirm-modal', 'is_open'),
            Output('continue-game-confirm-modal-body', 'children'),
            Output('game-continue-key', 'data')
        ]
        self.states = [
            State('game-continue-key', 'data')
        ]

        self.models_operations = ModelsOperations()
        self.games_repository = dependency_container.games_repository
        self.game = dependency_container.game

        self.logger.info('Initialized Continue Game Modal Callback')

    def callback(self, continue_clicks: list[int | None], _confirm_clicks: int | None, game_continue_key: str | None) \
            -> list[bool | html.Div | str]:
        prop_id = self.get_prop_from_context()
        if prop_id == 'continue-game-confirm-button':
            self.logger.info(f'Loading last instance of game: \'{game_continue_key}\' to continue it')
            game = self.get_last_version_of_game_key(game_continue_key)

            game_n_sets, \
                game_set_type, \
                game_n_legs, \
                game_leg_type, \
                game_initial_player_alignment = self.models_operations.get_parameters_from_old_game_class(game)

            self.game.__init__(
                ts = game.ts,
                version = game.version,
                started = True,
                players = game.players,
                initial_player_alignment = game_initial_player_alignment,
                n_sets = game_n_sets,
                set_type = game_set_type,
                n_legs = game_n_legs,
                leg_type = game_leg_type,
                points = game.points,
                out = game.out,
                sets = game.sets,
                repository = game.repository
            )
            return [False, None, None]
        elif any(continue_clicks):
            game_key = prop_id['index']
            self.logger.info(f'Open confirm Modal for continuing game: \'{game_key}\'')
            game_ts_pretty = self.format_game_ts_pretty(game_key)
            modal_content = html.Div(
                children = [
                    'The last state of the following Game will be started:',
                    html.Br(),
                    html.B(game_ts_pretty),
                    html.Br(),
                    '❗ This will also overwrite the current active Game ❗'
                ],
                style = {
                    'font-size': '1.5rem',
                    'text-align': 'center'
                }
            )
            return [True, modal_content, game_key]
        else:
            raise PreventUpdate
