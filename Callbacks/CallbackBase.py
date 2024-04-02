import datetime as dt
import json
from typing import Any

import dash
from dash.exceptions import PreventUpdate

from DependencyContainer import DependencyContainer
from Models.Game import Game


class CallbackBase:
    def __init__(self, dependency_container: DependencyContainer, dash_package: Any = dash) -> None:
        self.dash = dash_package
        self.games_repository = dependency_container.games_repository

    def register(self) -> None:
        # noinspection PyUnresolvedReferences
        self.app.callback(
            self.outputs,
            self.inputs,
            self.states
        )(self.callback)

    def get_prop_from_context(self, block_initial: bool = True) -> str | dict | None:
        ctx = self.dash.callback_context
        if not ctx.triggered:
            if block_initial:
                raise PreventUpdate
            else:
                return None
        prop_id = '.'.join(ctx.triggered[0]['prop_id'].split('.')[:-1])
        try:
            return json.loads(prop_id)
        except json.decoder.JSONDecodeError:
            return prop_id

    @staticmethod
    def format_game_ts_pretty(game_ts_string: str) -> str:
        game_ts = dt.datetime.fromtimestamp(float(game_ts_string))
        game_ts_pretty = game_ts.strftime('%H:%M - %d.%b.%Y')
        return game_ts_pretty

    def get_last_version_of_game_key(self, game_key: str) -> Game:
        last_game_version = self.games_repository.list_versions(game_key)[-1]
        game = self.games_repository.load(game_key, last_game_version)
        return game
