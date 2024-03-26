from abc import ABC, abstractmethod

from Models import Player


class AbstractPlayerRepository(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, player: Player) -> bool:
        pass

    @abstractmethod
    def load(self) -> list[Player]:
        pass
