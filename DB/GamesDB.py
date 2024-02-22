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
        self.maxEntries = 100
    
    def __createFolderIfNotExistsDecorator__(func):
        def wrapper(self, *args, **kwargs):
            Path(self.folderPath).mkdir(parents=True, exist_ok=True)
            return func(self, *args, **kwargs)
        return wrapper

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
    
    def __deleteToManyEntriesDecorator__(func):
        def wrapper(self, *args, **kwargs):
            games = self.listGames(suppress_logger=True)
            games.reverse()
            nEntries = 0
            for game in games:
                gameVersions = self.listVersions(game, suppress_logger=True)
                gameVersions.reverse()
                for entry in gameVersions:
                    nEntries += 1
                    if nEntries > self.maxEntries:
                        self.logger.info(f"Deleting version '{entry}' from database, because it exceeds the maximum number of entries ({self.maxEntries})")
                        self.deleteVersion(game, entry, suppress_logger=True)
                nVersions = self.listVersions(game, suppress_logger=True)
                if len(nVersions) == 0:
                    self.logger.info(f"Deleting game '{game}' from database, because it has no versions left")
                    self.deleteGame(game, suppress_logger=True)
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
    
    @__createFolderIfNotExistsDecorator__
    @__deleteOldGamesDecorator__
    @__deleteToManyEntriesDecorator__
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
    
    @__createFolderIfNotExistsDecorator__
    @__deleteOldGamesDecorator__
    @__deleteToManyEntriesDecorator__
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
    
    @__createFolderIfNotExistsDecorator__
    @__deleteOldGamesDecorator__
    def deleteVersion(self, gameTs, gameVersion, suppress_logger=False):
        if not suppress_logger:
            self.logger.info(f"Deleting version '{gameTs}.{gameVersion}' from database")
        gamePath = Path(self.folderPath) / str(gameTs) / f"{gameVersion}.pkl"

        if not Path(gamePath).exists():
            error_msg = f"Version '{gameTs}.{gameVersion}' does not exist in database. Version can not be deleted!"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        
        gamePath.unlink()
    
    @__createFolderIfNotExistsDecorator__
    def deleteGame(self, gameTs, suppress_logger=False):
        if not suppress_logger:
            self.logger.info(f"Deleting game '{gameTs}' from database")
        folderPath = Path(self.folderPath) / gameTs

        if not Path(folderPath).exists():
            error_msg = f"Game '{gameTs}' does not exist in database. Game can not be deleted!"
            self.logger.error(error_msg)
            raise DBEntryDoesNotExistError(error_msg)
        
        for version in folderPath.iterdir():
            version.unlink()
        folderPath.rmdir()
    
    @__createFolderIfNotExistsDecorator__
    def listGames(self, suppress_logger=False):
        if not suppress_logger:
            self.logger.info(f"Listing all games from database")
        gameFolders = []
        for folder in Path(self.folderPath).iterdir():
            try:
                float(folder.parts[-1])
            except ValueError:
                break
            gameFolders.append(folder.parts[-1])
        gameFolders = sorted(gameFolders)
        return gameFolders
    
    @__createFolderIfNotExistsDecorator__
    def listVersions(self, gameTs, suppress_logger=False):
        if not suppress_logger:
            self.logger.info(f"Listing all versions of game '{gameTs}' from database")

        if not Path(self.folderPath).exists():
            error_msg = f"Database folder does not exist. No versions can be listed."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        
        folderPath = Path(self.folderPath) / gameTs
        gameVersions = []
        for version in folderPath.iterdir():
            gameVersions.append(".".join(version.parts[-1].split(".")[0:2]))
        gameVersions = sorted(gameVersions)
        return gameVersions
