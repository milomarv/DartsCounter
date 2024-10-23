from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger


class LoadVersion(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [Input('url', 'pathname')]
        self.outputs = [Output('version-link', 'children')]
        self.states = []
        self.dependency_container = dependency_container
        self.logger.info('Initialized Load Version Callback')

    def callback(self, url: str) -> object:
        if self.dependency_container.router_config.is_route(
            url, self.dependency_container.router_config.home
        ):
            return [self.dependency_container.version]
        raise PreventUpdate
