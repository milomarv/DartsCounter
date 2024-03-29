from dash.dependencies import Input, Output

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger
from Pages.HomePage.HomePageLayout import HomePageLayout
from Pages.NotFoundPage import NotFoundPageLayout
from Pages.ScoreboardPage.ScoreboardPageLayout import ScoreboardPageLayout
from Pages.TyperPage.TyperPageLayout import TyperPageLayout


class Router(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__()
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [Input('url', 'pathname')]
        self.outputs = [Output('page-content', 'children')]
        self.states = []
        self.logger.info('Initialized Router Callback')

    def callback(self, pathname: str) -> list:
        if pathname in ['/', '/home']:
            self.logger.info('Routing to HomePage')
            return [HomePageLayout().build()]
        elif pathname == '/typer':
            self.logger.info('Routing to TyperPage')
            return [TyperPageLayout().build()]
        elif pathname == '/scoreboard':
            self.logger.info('Routing to DashboardPage')
            return [ScoreboardPageLayout().build()]
        else:
            self.logger.info('Routing to NotFoundPage')
            return [NotFoundPageLayout().build()]
