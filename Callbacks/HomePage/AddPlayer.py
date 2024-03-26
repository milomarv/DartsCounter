from dash import Patch
from dash.dependencies import Input, Output

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger
from Pages.HomePage.PlayerInput import PlayerInput


class AddPlayer(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer):
        super().__init__()
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [Input('add-player', 'n_clicks')]
        self.outputs = [Output('player-inputs-div', 'children')]
        self.states = []
        self.playerInput = PlayerInput()
        self.logger.info('Initialized AddPlayer Callback')

    def callback(self, n_clicks: int) -> list:
        if n_clicks:
            repeat = 1
        else:
            self.playerInput = PlayerInput()
            repeat = 4
        patched_children = Patch()
        for r in range(repeat):
            patched_children.append(
                self.playerInput.Build()
            )
        self.logger.info(f"Added '{repeat}' Player Inputs to HomePage")
        return [patched_children]
