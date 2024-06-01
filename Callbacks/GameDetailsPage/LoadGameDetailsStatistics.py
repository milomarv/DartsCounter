from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger
from Pages.GamesDetailsPage.GameStatistics import GameStatistics


class LoadGameDetailsStatistics(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [
            Input('url', 'pathname')
        ]
        self.outputs = [
            Output('game-details-statistics-div', 'children')
        ]
        self.states = []
        self.logger.info('Initialized Load GameDetails Statistics Callback')

        self.current_game = dependency_container.game

    def callback(self, url: str) -> list[html.Div]:
        if url.startswith('/database/game-details/'):
            game_key = url.split('/')[-1]
            game = self.get_last_version_of_game_key(game_key)

            if game.winner:
                game_finished = 'finished'
            elif game.ts == self.current_game.ts and self.current_game.started:
                game_finished = 'in_progress'
            else:
                game_finished = 'not_finished'

            statistics_div = GameStatistics().build(
                finished = game_finished,
                points = game.points,
                out = game.out,
                legs = game.n_legs,
                total_legs = game.get_n_total_legs(),
                leg_mode = game.leg_type,
                sets = game.n_sets,
                total_sets = len(game.sets),
                set_mode = game.set_type
            )
            return [statistics_div]
        else:
            raise PreventUpdate
