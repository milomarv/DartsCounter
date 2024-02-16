from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from Logging.Logger import Logger
from Callbacks.CallbackBase import CallbackBase

class SetOnlineMode(CallbackBase):
    def __init__(self, dependencyContainer):
        self.logger = Logger(__name__)
        self.app = dependencyContainer.app
        self.online_mode = dependencyContainer.online_mode
        self.inputs = [
            Input("online-switch", "value")
        ]
        self.outputs = [
            Output("online-switch", "label")
        ]
        self.states = []
        self.running = []
        self.logger.info("Initialized set Online Mode Callback")
    
    def Callback(self, switch_val):
        if type(switch_val) == type(None):
            if self.online_mode.value:
                return ["Online"]
            else:
                return ["Offline"]
        else:
            if switch_val:
                self.logger.info("Switched to Online Mode")
                self.online_mode.value = True
                return ["Online"]
            else:
                self.logger.info("Switched to Offline Mode")
                self.online_mode.value = False
                return ["Offline"]
        raise PreventUpdate