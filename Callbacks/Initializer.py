from Callbacks.HomePage.AddPlayer import AddPlayer
from Callbacks.HomePage.InitializeFields import InitializeFields
from Callbacks.HomePage.SetOnllineMode import SetOnlineMode
from Callbacks.HomePage.StartStopGame import StartStopGame
from Callbacks.Router import Router
from Callbacks.ScoreBoard.SelectFilter import SelectFilter
from Callbacks.ScoreBoard.UpdatePlayerCards import UpdatePlayerCards
from Callbacks.Typer.ActivateMultiplier import ActivateMultiplier
from Callbacks.Typer.ThrowDart import ThrowDart
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger


class Initializer:
    def __init__(self, dependency_container: DependencyContainer) -> None:
        self.logger = Logger(__name__)
        self.dependency_container = dependency_container

    def run(self) -> None:
        Router(self.dependency_container).register()

        AddPlayer(self.dependency_container).register()
        StartStopGame(self.dependency_container).register()
        SetOnlineMode(self.dependency_container).register()
        InitializeFields(self.dependency_container).register()

        ThrowDart(self.dependency_container).register()
        ActivateMultiplier(self.dependency_container).register()

        UpdatePlayerCards(self.dependency_container).register()
        SelectFilter(self.dependency_container).register()
