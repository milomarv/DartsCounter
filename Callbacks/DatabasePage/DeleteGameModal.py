from dash import html
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger


class DeleteGameModal(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [
            Input({'type': 'game-entry-delete-button', 'index': ALL}, 'n_clicks'),
            Input('delete-game-confirm-button', 'n_clicks')
        ]
        self.outputs = [
            Output('delete-game-confirm-modal', 'is_open'),
            Output('delete-game-confirm-modal-body', 'children'),
            Output('game-deletion-key', 'data')
        ]
        self.states = [
            State('game-deletion-key', 'data')
        ]

        self.games_repository = dependency_container.games_repository

        self.logger.info('Initialized open delete game Modal')

    def callback(self, delete_clicks: list[int | None], _confirm_click: int | None, game_deletion_key: str | None) -> \
            list[bool | html.Div | str]:
        prop_id = self.get_prop_from_context()
        if prop_id == 'delete-game-confirm-button':
            self.logger.info(f'Deleting game: {game_deletion_key}')
            self.games_repository.delete_game(game_deletion_key)
            return [False, None, None]
        elif any(delete_clicks):
            game_key = prop_id['index']
            self.logger.info(f'Open confirm Modal for deleting game {game_key}')
            game_ts_pretty = self.format_game_ts_pretty(game_key)
            modal_content = html.Div(
                children = [
                    'Are you sure you want to delete game from date:',
                    html.Br(),
                    html.B(game_ts_pretty)
                ],
                style = {
                    'font-size': '1.5rem',
                    'text-align': 'center'
                }
            )
            return [True, modal_content, game_key]
        else:
            raise PreventUpdate
