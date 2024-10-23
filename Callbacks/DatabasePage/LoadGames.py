import time

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_bootstrap_components import Card

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger
from Pages.DatabasePage.GameEntry import GameEntry


class LoadGames(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [
            Input('url', 'pathname'),
            Input('delete-game-confirm-button', 'n_clicks'),
            Input('continue-game-confirm-button', 'n_clicks'),
        ]
        self.outputs = [
            Output('games-db-list', 'children'),
            Output('games-db-list-frame', 'style'),
            Output('games-db-list', 'style'),
        ]
        self.states = [State('games-db-list-frame', 'style')]

        self.games_repository = dependency_container.games_repository
        self.current_game = dependency_container.game

        self.game_entry = GameEntry()

        self.logger.info('Initialized Callback Load Games')

    def callback(
        self,
        url: str,
        _confirm_delete_clicks: int | None,
        _confirm_continue_clicks: int | None,
        frame_style: dict,
    ) -> list[list[Card] | dict | dict]:
        if url == '/database':
            self.logger.info('Triggered loading games for frontend')
            time.sleep(1)
            game_keys = self.games_repository.list_games()
            game_keys = reversed(sorted(game_keys))

            game_entries = list()
            for game_key in game_keys:
                game_ts_pretty = self.format_game_ts_pretty(game_key)

                try:
                    last_game_version = self.games_repository.list_versions(game_key)[
                        -1
                    ]
                except (ValueError, FileNotFoundError):
                    continue
                game = self.games_repository.load(game_key, last_game_version)

                game_winner = None
                if game.winner:
                    game_finished = 'finished'
                    game_winner = game.winner.name
                elif game.ts == self.current_game.ts and self.current_game.started:
                    game_finished = 'in_progress'
                else:
                    game_finished = 'not_finished'

                finished_sets = game.get_n_total_finished_sets()
                finished_legs = game.get_n_total_finished_legs()

                try:
                    players_alignment = game.initial_player_alignment
                except AttributeError:
                    players_alignment = game.players
                players = [p.name for p in players_alignment]

                game_entry = self.game_entry.build(
                    game_key,
                    game_ts_pretty,
                    game_finished,
                    game_winner,
                    finished_sets,
                    finished_legs,
                    players,
                )
                game_entries.append(game_entry)

            frame_style['width'] = None

            return [game_entries, frame_style, {}]
        else:
            raise PreventUpdate
