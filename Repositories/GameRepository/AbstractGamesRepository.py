from abc import ABC, abstractmethod

from Models import Game


class AbstractGamesRepository(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def save(self, game: Game) -> bool:
        pass

    @abstractmethod
    def load(self, game_ts: str, game_version: str) -> Game:
        pass

    @abstractmethod
    def delete_game(self, game_ts: str) -> bool:
        pass

    @abstractmethod
    def delete_version(self, game_ts: str, game_version: str) -> bool:
        pass

    @abstractmethod
    def list_games(self) -> list[str]:
        pass

    @abstractmethod
    def list_versions(self, game_ts: str) -> list[str]:
        pass
