import dash

from Callbacks.DependencyContainer import DependencyContainer
from Callbacks.HomePage.AddPlayer import AddPlayer
from Callbacks.HomePage.InitializeFields import InitializeFields
from Callbacks.HomePage.SetOnllineMode import SetOnlineMode
from Callbacks.HomePage.StartStopGame import StartStopGame
from Callbacks.Router import Router
from Callbacks.ScoreBoard.SelectFilter import SelectFilter
from Callbacks.ScoreBoard.UpdatePlayerCards import UpdatePlayerCards
from Callbacks.Typer.ActivateMultiplier import ActivateMultiplier
from Callbacks.Typer.ThrowDart import ThrowDart
from Logging.Logger import Logger


class Initializer:
    def __init__(self, app: dash.Dash) -> None:
        self.logger = Logger(__name__)
        self.dependencyContainer = DependencyContainer(app)
        self.logger.info("Created Dependency Container")

    def run(self) -> None:
        Router(self.dependencyContainer).register()

        AddPlayer(self.dependencyContainer).register()
        StartStopGame(self.dependencyContainer).register()
        SetOnlineMode(self.dependencyContainer).register()
        InitializeFields(self.dependencyContainer).register()

        ThrowDart(self.dependencyContainer).register()
        ActivateMultiplier(self.dependencyContainer).register()

        UpdatePlayerCards(self.dependencyContainer).register()
        SelectFilter(self.dependencyContainer).register()
