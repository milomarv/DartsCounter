from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from Callbacks.CallbackBase import CallbackBase
from Callbacks.DependencyContainer import DependencyContainer
from Logging.Logger import Logger


class SelectFilter(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__()
        self.logger = Logger(__name__)
        self.app = dependency_container.app
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

    def callback(self, _n_game_filter: int, _n_set_filter: int, _n_leg_filter: int) -> list[str]:
        prop_id = self.get_prop_from_context()
        if prop_id == "game-filter-button":
            return ["btn btn-primary", "btn btn-secondary", "btn btn-secondary"]
        elif prop_id == "current-set-filter-button":
            return ["btn btn-secondary", "btn btn-primary", "btn btn-secondary"]
        elif prop_id == "current-leg-filter-button":
            return ["btn btn-secondary", "btn btn-secondary", "btn btn-primary"]
        raise PreventUpdate
