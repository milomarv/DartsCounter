from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger


class CallbackTemplate(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [
            Input('id', 'property')
        ]
        self.outputs = [
            Output('id', 'property')
        ]
        self.states = []
        self.logger.info('Initialized Callback Template')

    def callback(self, prop_val: object) -> object:
        raise PreventUpdate
