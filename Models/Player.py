from Logging.Logger import Logger


class Player:
    def __init__(self, name: str) -> None:
        self.logger = Logger(__name__)
        self.name = name
        self.logger.info(f'Player {name} created')

    def __str__(self) -> str:
        return f'Player: {self.name}'
