from typing import Any

import dash

from Models.Game import Game


class State:
    def __init__(self, value: Any) -> None:
        self.value = value


class DependencyContainer:
    def __init__(self, app: dash.Dash) -> None:
        self.app = app
        self.game = Game()
        self.online_mode = State(False)
