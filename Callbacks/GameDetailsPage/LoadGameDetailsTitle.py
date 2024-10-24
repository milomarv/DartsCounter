from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger


class LoadGameDetailsTitle(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.router_config = dependency_container.router_config
        self.inputs = [Input('url', 'pathname')]
        self.outputs = [Output('game-details-title', 'children')]
        self.states = []
        self.logger.info('Initialized Load Game Details Title Callback')

    def callback(self, url: str) -> list:
        if self.router_config.startswith_route(
            url, self.router_config.database_game_details
        ):
            game_key = url.split('/')[-1]
            game_ts = self.format_game_ts_pretty(game_key)
            game_title = [
                html.Div('Game Details |', style={'padding-right': '0.5rem'}),
                html.B(game_ts),
            ]
            return [game_title]
        else:
            raise PreventUpdate
