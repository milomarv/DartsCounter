from dash import Patch
from dash.dependencies import Input, Output, State

from Logging.Logger import Logger
from Callbacks.CallbackBase import CallbackBase
from Pages import *
from Pages.HomePage.PlayerInput import PlayerInput

class AddPlayer(CallbackBase):
    def __init__(self, dependencyContainer):
        self.logger = Logger(__name__)
        self.app = dependencyContainer.app
        self.inputs = [Input("add-player", "n_clicks")]
        self.outputs = [Output("player-inputs-div", "children")]
        self.states = []
        self.playerInput = PlayerInput()
        self.logger.info("Initialized AddPlayer Callback")
    
    def Callback(self, n_clicks):
        if n_clicks:
            repeat = 1
        else:
            self.playerInput = PlayerInput()
            repeat = 4
        patchedChildren = Patch()
        for r in range(repeat):
            patchedChildren.append(
                self.playerInput.Build()
            )
        self.logger.info(f"Added '{repeat}' Player Inputs to HomePage")
        return [patchedChildren]