import time
from typing import List

from dash import ALL
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from Callbacks.CallbackBase import CallbackBase
from Callbacks.DependencyContainer import DependencyContainer
from Logging.Logger import Logger
from Models.Out import DOUBLE_OUT
from Models.TypeSetLeg import FIRST_TO


class InitializeFields(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__()
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.game = dependency_container.game
        self.inputs = [
            Input("url", "pathname"),
            Input("start-stop-game-button", "n_clicks"),
            Input("end-game-confirm-button", "n_clicks")
        ]
        self.outputs = [
            Output("number-of-sets-input", "value"),
            Output("number-of-legs-input", "value"),
            Output("set-mode-select", "value"),
            Output("leg-mode-select", "value"),
            Output("points-input", "value"),
            Output("out-variant-select", "value"),
            Output({"type": "player-input", "index": ALL}, "value"),
            Output("number-of-sets-input", "disabled"),
            Output("number-of-legs-input", "disabled"),
            Output("set-mode-select", "disabled"),
            Output("leg-mode-select", "disabled"),
            Output("points-input", "disabled"),
            Output("out-variant-select", "disabled"),
            Output("add-player", "disabled"),
            Output({"type": "player-input", "index": ALL}, "disabled"),
        ]
        self.states = [
            State({"type": "player-input", "index": ALL}, "value")
        ]
        self.logger.info("Initialized Initialize Fields Callback")
        self.n_disable = 7

    def callback(self, url: str, _start_stop_game: int, _end_game_confirm: int, player_inputs: List[str]) -> list:
        if self.get_prop_from_context(block_initial=False) in ["start-stop-game-button", "end-game-confirm-button"]:
            time.sleep(0.1)
        if url in ["/", "/home"]:
            if self.game.started:
                disable_fields = [True for _ in range(self.n_disable)]
                disable_player_fields = [True if player_inputs else False for _ in range(len(player_inputs))]

                player_values = list()
                for i in range(len(player_inputs)):
                    try:
                        player_values.append(self.game.players[i].name)
                    except IndexError:
                        player_values.append(None)

                return [
                    self.game.nSets, self.game.nLegs,
                    self.game.setType.value, self.game.legType.value,
                    self.game.points, self.game.out.value,
                    player_values,
                    *disable_fields, disable_player_fields
                ]
            else:
                disable_fields = [False for _ in range(self.n_disable)]
                disable_player_fields = [False for _ in range(len(player_inputs))]
                player_values = [None for _ in range(len(player_inputs))]

                return [
                    3, 3,
                    FIRST_TO, FIRST_TO,
                    501, DOUBLE_OUT,
                    player_values,
                    *disable_fields, disable_player_fields
                ]
        else:
            raise PreventUpdate
