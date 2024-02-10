from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from Logging.Logger import Logger
from Callbacks.CallbackBase import CallbackBase

class SelectFilter(CallbackBase):
    def __init__(self, dependencyContainer):
        self.logger = Logger(__name__)
        self.app = dependencyContainer.app
        self.inputs = [
            Input("game-filter-button", "n_clicks"),
            Input("current-set-filter-button", "n_clicks"),
            Input("current-leg-filter-button", "n_clicks"),
        ]
        self.outputs = [
            Output("game-filter-button", "className"),
            Output("current-set-filter-button", "className"),
            Output("current-leg-filter-button", "className"),
        ]
        self.states = []
        self.logger.info("Initialized Select Filter Callback")
    
    def Callback(self, n_game_filter, n_set_filter, n_leg_filter):
        prop_id = self.getPropFromContext()
        if prop_id == "game-filter-button":
            return ["btn btn-primary", "btn btn-secondary", "btn btn-secondary"]
        elif prop_id == "current-set-filter-button":
            return ["btn btn-secondary", "btn btn-primary", "btn btn-secondary"]
        elif prop_id == "current-leg-filter-button":
            return ["btn btn-secondary", "btn btn-secondary", "btn btn-primary"]
        raise PreventUpdate
