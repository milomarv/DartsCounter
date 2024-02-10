from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from Logging.Logger import Logger
from Callbacks.CallbackBase import CallbackBase

class CallbackTemplate(CallbackBase):
    def __init__(self, dependencyContainer):
        self.logger = Logger(__name__)
        self.app = dependencyContainer.app
        self.inputs = [
            Input("id", "property")
        ]
        self.outputs = [
            Output("id", "property")
        ]
        self.states = []
        self.logger.info("Initialized Callback Template")
    
    def Callback(self, prop_val):
        raise PreventUpdate
