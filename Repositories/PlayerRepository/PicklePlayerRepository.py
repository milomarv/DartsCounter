import pickle

from Logging.Logger import Logger
from Models.Player import Player
from Repositories.PlayerRepository.AbstractPlayerRepository import AbstractPlayerRepository


class PicklePlayerRepository(AbstractPlayerRepository):
    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger(__name__)
        self.picklePath = './Repositories/pickle_databases/Players.pkl'

        try:
            with open(self.picklePath, 'rb'):
                pass
            self.logger.info(f'Database initialized with picklePath: {self.picklePath}')
        except FileNotFoundError:
            with open(self.picklePath, 'wb') as f:
                pickle.dump(list(), f)
            self.logger.warning(f'Database file not found. Created new file at: {self.picklePath}')

    def add(self, player: Player) -> bool:
        with open(self.picklePath, 'rb') as f:
            players = pickle.load(f)
        existing_players = [p.name for p in players]
        if player.name in existing_players:
            self.logger.warning(f'Player {player.name} already exists in database. Player can not be added!')
            return False
        players.append(player)
        with open(self.picklePath, 'wb') as f:
            pickle.dump(players, f)
        self.logger.info(f'Player added: {player}')
        return True

    def load(self) -> list[Player]:
        with open(self.picklePath, 'rb') as f:
            players = pickle.load(f)
        self.logger.info(f'Loaded {len(players)} players from database')
        return players
