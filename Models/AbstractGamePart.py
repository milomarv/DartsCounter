from abc import ABC, abstractmethod


class AbstractGamePart(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def finish(self) -> None:
        pass
