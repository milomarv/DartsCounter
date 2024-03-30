import datetime as dt
import os
import pickle
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv

from Errors import DBEntryAlreadyExistsError, DBEntryDoesNotExistError
from Logging.Logger import Logger
from Models import Game
from Repositories.GameRepository.AbstractGamesRepository import AbstractGamesRepository

load_dotenv()


class PickleGamesRepository(AbstractGamesRepository):
    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger(__name__)
        self.folderPath = './Repositories/pickle_databases/games/'
        self.deleteAfterNDays = int(os.getenv('DELETE_GAME_AFTER_N_DAYS'))
        self.maxEntries = int(os.getenv('MAX_DB_ENTRIES'))

    @staticmethod
    def __create_folder_if_not_exists_decorator__(func: Callable) -> Callable:
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            Path(self.folderPath).mkdir(parents = True, exist_ok = True)
            return func(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def __delete_old_games_decorator__(func: Callable) -> Callable:
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            games = self.list_games(suppress_logger = True)
            for game in games:
                game_ts = dt.datetime.fromtimestamp(float(game))
                if (dt.datetime.now() - game_ts).days > self.deleteAfterNDays:
                    self.logger.info(f"Game '{game}' is older than {self.deleteAfterNDays} days")
                    self.delete_game(game)
            return func(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def __delete_to_many_entries_decorator__(func: Callable) -> Callable:
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            games = self.list_games(suppress_logger = True)
            games.reverse()
            n_entries = 0
            for game in games:
                game_versions = self.list_versions(game, suppress_logger = True)
                game_versions.reverse()
                for entry in game_versions:
                    n_entries += 1
                    # noinspection PyChainedComparisons
                    if self.maxEntries > 0 and n_entries > self.maxEntries:
                        self.logger.info(
                            f"Deleting version '{entry}' from database,\
because it exceeds the maximum number of entries ({self.maxEntries})")
                        self.delete_version(game, entry, suppress_logger = True)
                n_versions = self.list_versions(game, suppress_logger = True)
                if len(n_versions) == 0:
                    self.logger.info(f"Deleting game '{game}' from database, because it has no versions left")
                    self.delete_game(game, suppress_logger = True)
            return func(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def __format_ts_to_string__(ts: float) -> str:
        return dt.datetime.fromtimestamp(ts).strftime('%Y.%m.%d %H:%M:%S')

    @staticmethod
    def __format_string_to_ts__(ts_string: str) -> dt.datetime:
        return dt.datetime.strptime(ts_string, '%Y.%m.%d %H:%M:%S')

    def __get_paths__(self, game: Game) -> tuple[str, str, Path, Path]:
        folder_name = str(game.ts)
        file_name = f'{game.version}.pkl'
        folder_path = Path(self.folderPath) / folder_name
        game_path = folder_path / file_name
        return folder_name, file_name, folder_path, game_path

    @__create_folder_if_not_exists_decorator__
    @__delete_old_games_decorator__
    @__delete_to_many_entries_decorator__
    def save(self, game: Game) -> bool:
        self.logger.info(f"Saving game '{game.ts}.{game.version}' to database")
        folder_name, file_name, folder_path, game_path = self.__get_paths__(game)

        if Path(game_path).exists():
            error_msg = f"Game '{game.ts}.{game.version}' already exists in database. Game can not be saved!"
            self.logger.error(error_msg)
            raise DBEntryAlreadyExistsError(error_msg)

        Path(folder_path).mkdir(parents = True, exist_ok = True)

        with open(game_path, 'wb') as f:
            pickle.dump(game, f)

        return True

    @__create_folder_if_not_exists_decorator__
    @__delete_old_games_decorator__
    @__delete_to_many_entries_decorator__
    def load(self, game_ts: str, game_version: str) -> Game:
        self.logger.info(f"Loading game '{game_ts}.{game_version}' from database")
        game_path = Path(self.folderPath) / game_ts / f'{game_version}.pkl'

        if not Path(game_path).exists():
            error_msg = f"Game '{game_ts}.{game_version}' does not exist in database. Game can not be loaded!"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        with open(game_path, 'rb') as f:
            game = pickle.load(f)

        return game

    @__create_folder_if_not_exists_decorator__
    def delete_game(self, game_ts: str, suppress_logger: bool = False) -> bool:
        if not suppress_logger:
            self.logger.info(f"Deleting game '{game_ts}' from database")
        folder_path = Path(self.folderPath) / game_ts

        if not Path(folder_path).exists():
            error_msg = f"Game '{game_ts}' does not exist in database. Game can not be deleted!"
            self.logger.error(error_msg)
            raise DBEntryDoesNotExistError(error_msg)

        for version in folder_path.iterdir():
            version.unlink()
        folder_path.rmdir()

        return True

    @__create_folder_if_not_exists_decorator__
    @__delete_old_games_decorator__
    def delete_version(self, game_ts: str, game_version: str, suppress_logger: bool = False) -> bool:
        if not suppress_logger:
            self.logger.info(f"Deleting version '{game_ts}.{game_version}' from database")
        game_path = Path(self.folderPath) / str(game_ts) / f'{game_version}.pkl'

        if not Path(game_path).exists():
            error_msg = f"Version '{game_ts}.{game_version}' does not exist in database. Version can not be deleted!"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        game_path.unlink()

        return True

    @__create_folder_if_not_exists_decorator__
    def list_games(self, suppress_logger: bool = False) -> list[str]:
        if not suppress_logger:
            self.logger.info('Listing all games from database')
        game_folders = []
        for folder in Path(self.folderPath).iterdir():
            try:
                float(folder.parts[-1])
            except ValueError:
                break
            game_folders.append(folder.parts[-1])
        game_folders = sorted(game_folders)
        return game_folders

    @__create_folder_if_not_exists_decorator__
    def list_versions(self, game_ts: str, suppress_logger: bool = False) -> list[str]:
        if not suppress_logger:
            self.logger.info(f"Listing all versions of game '{game_ts}' from database")

        if not Path(self.folderPath).exists():
            error_msg = 'Database folder does not exist. No versions can be listed.'
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        folder_path = Path(self.folderPath) / game_ts
        game_versions = []
        for version in folder_path.iterdir():
            game_versions.append('.'.join(version.parts[-1].split('.')[0:2]))
        game_versions = sorted(game_versions)
        return game_versions
