from Logging.Logger import Logger

from Callbacks.DependencyContainer import DependencyContainer

from Callbacks.Router import Router

from Callbacks.HomePage.AddPlayer import AddPlayer
from Callbacks.HomePage.StartStopGame import StartStopGame
from Callbacks.HomePage.SetOnllineMode import SetOnlineMode
from Callbacks.HomePage.InitializeFields import InitializeFields

from Callbacks.Typer.ThrowDart import ThrowDart
from Callbacks.Typer.ActivateMultiplier import ActivateMultiplier

from Callbacks.ScoreBoard.UpdatePlayerCards import UpdatePlayerCards
from Callbacks.ScoreBoard.SelectFilter import SelectFilter

class Initializer:
    def __init__(self, app):
        self.logger = Logger(__name__)
        self.dependencyContainer = DependencyContainer(app)
        self.logger.info("Created Dependency Container")

    def Run(self):
        Router(self.dependencyContainer).Register()

        AddPlayer(self.dependencyContainer).Register()
        StartStopGame(self.dependencyContainer).Register()
        SetOnlineMode(self.dependencyContainer).Register()
        InitializeFields(self.dependencyContainer).Register()

        ThrowDart(self.dependencyContainer).Register()
        ActivateMultiplier(self.dependencyContainer).Register()

        UpdatePlayerCards(self.dependencyContainer).Register()
        SelectFilter(self.dependencyContainer).Register()


