import pickle
import datetime as dt
from pathlib import Path

from Errors import *
from Logging.Logger import Logger

class GamesDB:
    def __init__(self):
        self.logger = Logger(__name__)
        self.folderPath = "./DB/databases/games/"
        self.deleteAfterNDays = 30
    
    def __deleteOldGamesDecorator__(func):
        def wrapper(self, *args, **kwargs):
            games = self.listGames(suppress_logger=True)
            for game in games:
                gameTs = dt.datetime.fromtimestamp(float(game))
                if (dt.datetime.now() - gameTs).days > self.deleteAfterNDays:
                    self.logger.info(f"Game '{game}' is older than {self.deleteAfterNDays} days")
                    self.deleteGame(game)
            return func(self, *args, **kwargs)
        return wrapper

    def __formatTStoString__(self, ts):
        return dt.datetime.fromtimestamp(ts).strftime("%Y.%m.%d %H:%M:%S")
    
    def __formatStringToTS__(self, tsString):
        return dt.datetime.strptime(tsString, "%Y.%m.%d %H:%M:%S")
    
    def __getPaths__(self, game):
        folderName = str(game.ts)
        fileName = f"{game.version}.pkl"
        folderPath = Path(self.folderPath) / folderName
        gamePath = folderPath / fileName
        return folderName, fileName, folderPath, gamePath
    
    @__deleteOldGamesDecorator__
    def save(self, game):
        self.logger.info(f"Saving game '{game.ts}.{game.version}' to database")
        folderName, fileName, folderPath, gamePath = self.__getPaths__(game)
        
        if Path(gamePath).exists():
            error_msg = f"Game '{game.ts}.{game.version}' already exists in database. Game can not be saved!"
            self.logger.error(error_msg)
            raise DBEntryAlreadyExistsError(error_msg)
        
        Path(folderPath).mkdir(parents=True, exist_ok=True)

        with open(gamePath, 'wb') as f:
            pickle.dump(game, f)
    
    @__deleteOldGamesDecorator__
    def load(self, gameTs, gameVersion):
        self.logger.info(f"Loading game '{gameTs}.{gameVersion}' from database")
        gamePath = Path(self.folderPath) / str(gameTs) / f"{gameVersion}.pkl"

        if not Path(gamePath).exists():
            error_msg = f"Game '{gameTs}.{gameVersion}' does not exist in database. Game can not be loaded!"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        
        with open(gamePath, 'rb') as f:
            game = pickle.load(f)
        
        return game
    
    @__deleteOldGamesDecorator__
    def deleteVersion(self, gameTs, gameVersion):
        self.logger.info(f"Deleting version '{gameTs}.{gameVersion}' from database")
        gamePath = Path(self.folderPath) / str(gameTs) / f"{gameVersion}.pkl"

        if not Path(gamePath).exists():
            error_msg = f"Version '{gameTs}.{gameVersion}' does not exist in database. Version can not be deleted!"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        
        gamePath.unlink()
    
    def deleteGame(self, gameTs):
        self.logger.info(f"Deleting game '{gameTs}' from database")
        folderPath = Path(self.folderPath) / gameTs

        if not Path(folderPath).exists():
            error_msg = f"Game '{gameTs}' does not exist in database. Game can not be deleted!"
            self.logger.error(error_msg)
            raise DBEntryDoesNotExistError(error_msg)
        
        for version in folderPath.iterdir():
            version.unlink()
        folderPath.rmdir()
    
    def listGames(self, suppress_logger=False):
        if not suppress_logger:
            self.logger.info(f"Listing all games from database")
        gameFolders = []
        for folder in Path(self.folderPath).iterdir():
            gameFolders.append(folder.parts[-1])
        return gameFolders
    
    def listVersions(self, gameTs):
        self.logger.info(f"Listing all versions of game '{gameTs}' from database")

        if not Path(self.folderPath).exists():
            error_msg = f"Database folder does not exist. No versions can be listed."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        
        folderPath = Path(self.folderPath) / gameTs
        gameVersions = []
        for version in folderPath.iterdir():
            gameVersions.append(".".join(version.parts[-1].split(".")[0:2]))
        return gameVersions