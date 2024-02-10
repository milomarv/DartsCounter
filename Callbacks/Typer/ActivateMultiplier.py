from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from Logging.Logger import Logger
from Callbacks.CallbackBase import CallbackBase

class ActivateMultiplier(CallbackBase):
    def __init__(self, dependencyContainer):
        self.logger = Logger(__name__)
        self.app = dependencyContainer.app
        self.inputs = [
            Input("x2-score-button", "n_clicks"),
            Input("x3-score-button", "n_clicks"),
            Input("0-score-button", "n_clicks"),
            Input("1-score-button", "n_clicks"),
            Input("2-score-button", "n_clicks"),
            Input("3-score-button", "n_clicks"),
            Input("4-score-button", "n_clicks"),
            Input("5-score-button", "n_clicks"),
            Input("6-score-button", "n_clicks"),
            Input("7-score-button", "n_clicks"),
            Input("8-score-button", "n_clicks"),
            Input("9-score-button", "n_clicks"),
            Input("10-score-button", "n_clicks"),
            Input("11-score-button", "n_clicks"),
            Input("12-score-button", "n_clicks"),
            Input("13-score-button", "n_clicks"),
            Input("14-score-button", "n_clicks"),
            Input("15-score-button", "n_clicks"),
            Input("16-score-button", "n_clicks"),
            Input("17-score-button", "n_clicks"),
            Input("18-score-button", "n_clicks"),
            Input("19-score-button", "n_clicks"),
            Input("20-score-button", "n_clicks"),
        ]
        self.outputs = [
            Output("x2-score-button", "active"),
            Output("x3-score-button", "active"),
            Output("25-score-button", "disabled"),
            Output("50-score-button", "disabled")
        ]
        self.states = [
            State("x2-score-button", "active"),
            State("x3-score-button", "active")
        ]
        self.logger.info("Initialized Activate Mulitplier Callback")
    
    def Callback(
        self, 
        n_clicks_x2, n_clicks_x3, 
        s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10,
        s11, s12, s13, s14, s15, s16, s17, s18, s19, s20,
        x2_active, x3_active
    ):
        prop_id = self.getPropFromContext()
        if prop_id == "x2-score-button":
            if x2_active:
                return [False, False, False, False]
            else:
                return [True, False, True, True]
        elif prop_id == "x3-score-button":
            if x3_active:
                return [False, False, False, False]
            else:
                return [False, True, True, True]
        elif not prop_id.startswith("x"):
            return [False, False, False, False]
        raise PreventUpdate