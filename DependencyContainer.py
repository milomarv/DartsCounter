from typing import Any

import dash

from Callbacks.Router.RouterConfig import RouterConfig
from Models.Game import Game
from Repositories.GameRepository.PickleGamesRepository import PickleGamesRepository
from Repositories.PlayerRepository.PicklePlayerRepository import PicklePlayerRepository


class State:
    def __init__(self, value: Any) -> None:
        self.value = value


class DependencyContainer:
    def __init__(self, app: dash.Dash) -> None:
        self.version = 'v1.0.1'
        self.app = app
        self.online_mode = State(False)
        self.router_config = RouterConfig()
        self.games_repository = PickleGamesRepository()
        self.player_repository = PicklePlayerRepository()
        self.game = Game(repository=self.games_repository)
