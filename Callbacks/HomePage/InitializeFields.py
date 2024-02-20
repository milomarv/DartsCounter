from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import ALL
import time

from Logging.Logger import Logger
from Callbacks.CallbackBase import CallbackBase
from Models.TypeSetLeg import FIRST_TO
from Models.Out import DOUBLE_OUT

class InitializeFields(CallbackBase):
    def __init__(self, dependencyContainer):
        self.logger = Logger(__name__)
        self.app = dependencyContainer.app
        self.game = dependencyContainer.game
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
        self.nDisbale = 7
    
    def Callback(self, url, start_stop_game, end_game_confirm, playerInputs):
        if self.getPropFromContext(blockInital=False) in ["start-stop-game-button", "end-game-confirm-button"]:
            time.sleep(0.1)
        if url in ["/", "/home"]:
            if self.game.started:
                disableFields = [True for _ in range(self.nDisbale)]
                disablePlayerFields = [True if playerInputs else False for _ in range(len(playerInputs))]

                playerValues = list()
                for i in range(len(playerInputs)):
                    try:
                        playerValues.append(self.game.players[i].name)
                    except IndexError:
                        playerValues.append(None)

                return [
                    self.game.nSets, self.game.nLegs,
                    self.game.setType.value, self.game.legType.value,
                    self.game.points, self.game.out.value,
                    playerValues,
                    *disableFields, disablePlayerFields
                ]
            else:
                disableFields = [False for _ in range(self.nDisbale)]
                disablePlayerFields = [False for _ in range(len(playerInputs))]
                playerValues = [None for _ in range(len(playerInputs))]

                return [
                    3, 3,
                    FIRST_TO, FIRST_TO,
                    501, DOUBLE_OUT,
                    playerValues,
                    *disableFields, disablePlayerFields
                ]
        else:
            raise PreventUpdate