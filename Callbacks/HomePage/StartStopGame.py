import dash
from dash import ALL
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from Logging.Logger import Logger
from Callbacks.CallbackBase import CallbackBase
from Models.Player import Player
from Models.Out import Out
from Models.TypeSetLeg import TypeSetLeg

class StartStopGame(CallbackBase):
    def __init__(self, dependencyContainer):
        self.logger = Logger(__name__)
        self.app = dependencyContainer.app
        self.game = dependencyContainer.game
        self.inputs = [
            Input("start-stop-game-button", "n_clicks"),
            Input("end-game-confirm-button", "n_clicks")
        ]
        self.outputs = [
            Output("start-stop-game-button", "children"),
            Output("start-stop-game-button", "className"),
            Output("start-game-error-modal", "is_open"),
            Output("start-game-error-modal-body", "children"),
            Output("end-game-confirm-modal", "is_open")
        ]
        self.states = [
            State({"type": "player-input", "index": ALL}, "value"),
            State("number-of-sets-input", "value"),
            State("number-of-legs-input", "value"),
            State("set-mode-select", "value"),
            State("leg-mode-select", "value"),
            State("points-input", "value"),
            State("out-variant-select", "value")
        ]
        self.logger.info("Initialized StartStopGame Callback")
    
    def Callback(self, n_start, n_stop, players, nSets, nLegs, setType, legType, points, out):
        if self.getPropFromContext(blockInital=False) == "start-stop-game-button":
            if not self.game.started:
                self.game.stop()
                print(out)
                try:
                    self.game.start(
                        players=[Player(name) for name in players if name],
                        nSets=nSets,
                        setType=TypeSetLeg(setType),
                        nLegs=nLegs,
                        legType=TypeSetLeg(legType),
                        points=points,
                        out=Out(out)
                    )
                    self.game.save()
                    return ["Stop Game", "btn btn-danger", False, None, False]
                except ValueError as e:
                    return ["Start Game", "btn btn-success", True, str(e), False]
            else:
                return ["Stop Game", "btn btn-danger", False, None, True]
        elif self.getPropFromContext(blockInital=False) == "end-game-confirm-button":
            self.game.started = False
            return ["Start Game", "btn btn-success", False, None, False]
        elif self.game.started:
            return ["Stop Game", "btn btn-danger", False, None, False]
        else:
            return ["Start Game", "btn btn-success", False, None, False]
