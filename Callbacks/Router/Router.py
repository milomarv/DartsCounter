from dash.dependencies import Input, Output

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger
from Pages.DatabasePage.DatabasePageLayout import DatabasePageLayout
from Pages.GamesDetailsPage.GameDetailsPageLayout import GamesDetailsPageLayout
from Pages.HomePage.HomePageLayout import HomePageLayout
from Pages.NotFoundPage import NotFoundPageLayout
from Pages.ReleaseNotesPage.ReleaseNotesPageLayout import ReleaseNotesPageLayout
from Pages.ScoreboardPage.ScoreboardPageLayout import ScoreboardPageLayout
from Pages.TyperPage.TyperPageLayout import TyperPageLayout


class Router(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.dependency_container = dependency_container
        self.inputs = [Input('url', 'pathname')]
        self.outputs = [Output('page-content', 'children')]
        self.states = []
        self.logger.info('Initialized Router Callback')

    def callback(self, pathname: str) -> list:
        if self.dependency_container.router_config.is_route(
            pathname, self.dependency_container.router_config.home
        ):
            self.logger.info('Routing to HomePage')
            return [HomePageLayout().build()]

        elif self.dependency_container.router_config.is_route(
            pathname, self.dependency_container.router_config.typer
        ):
            self.logger.info('Routing to TyperPage')
            return [TyperPageLayout().build()]

        elif self.dependency_container.router_config.is_route(
            pathname, self.dependency_container.router_config.scoreboard
        ):
            self.logger.info('Routing to DashboardPage')
            return [ScoreboardPageLayout().build()]

        elif self.dependency_container.router_config.is_route(
            pathname, self.dependency_container.router_config.database
        ):
            self.logger.info('Routing to DatabasePage')
            return [DatabasePageLayout().build()]

        elif self.dependency_container.router_config.startswith_route(
            pathname, self.dependency_container.router_config.database_game_details
        ):
            self.logger.info('Routing to Game Details')
            return [GamesDetailsPageLayout().build()]

        elif self.dependency_container.router_config.is_route(
            pathname, self.dependency_container.router_config.release_notes
        ):
            self.logger.info('Routing to ReleaseNotesPage')
            return [ReleaseNotesPageLayout().build()]

        else:
            self.logger.info('Routing to NotFoundPage')
            return [NotFoundPageLayout().build()]
