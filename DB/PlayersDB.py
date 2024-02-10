import pickle

from Logging.Logger import Logger
from Models.Player import Player

class PlayersDB:
    def __init__(self):
        self.logger = Logger(__name__)
        self.picklePath = "./DB/databases/Players.pkl"

        try:
            with open(self.picklePath, 'rb') as f:
                pass
            self.logger.info(f"Database initialized with picklePath: {self.picklePath}")
        except FileNotFoundError:
            with open(self.picklePath, 'wb') as f:
                pickle.dump(list(), f)
            self.logger.warning(f"Database file not found. Created new file at: {self.picklePath}")
    
    def add(self, player: Player):
        with open(self.picklePath, 'rb') as f:
            players = pickle.load(f)
        existingPlayers = [p.name for p in players]
        if player.name in existingPlayers:
            self.logger.warning(f"Player {player.name} already exists in database. Player can not be added!")
            return
        players.append(player)
        with open(self.picklePath, 'wb') as f:
            pickle.dump(players, f)
        self.logger.info(f"Player added: {player}")
    
    def load(self):
        with open(self.picklePath, 'rb') as f:
            players = pickle.load(f)
        self.logger.info(f"Loaded {len(players)} players from database")
        return players