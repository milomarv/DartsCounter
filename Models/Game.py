import datetime as dt
import threading
from typing import List

from Errors import DBEntryDoesNotExistError, GameAlreadyFinishedError, GameNotStartedError, \
    GameRollBackNotPossibleError, NoSetCreatedError
from Logging.Logger import Logger
from Repositories.GameRepository.AbstractGamesRepository import AbstractGamesRepository
from .AbstractGamePart import AbstractGamePart
from .Out import Out
from .Player import Player
from .Set import Set
from .TypeSetLeg import BEST_OF, FIRST_TO, TypeSetLeg


class Game(AbstractGamePart):
    def __init__(
            self,
            ts: float = None,
            version: float = None,
            started: bool = False,
            players=None,
            n_sets: int = None,
            set_type: TypeSetLeg = None,
            n_legs: int = None,
            leg_type: TypeSetLeg = None,
            points: int = 0,
            out: Out = None,
            winner: Player = None,
            sets=None,
            repository: AbstractGamesRepository = None
    ):
        super().__init__()

        if sets is None:
            sets = list()
        if players is None:
            players = list()

        self.logger = Logger(__name__)
        self.repository = repository
        if ts:
            self.ts = ts
        else:
            self.ts = self.__create_ts__()
        if version:
            self.version = version
        else:
            self.version = self.ts
        self.started = started
        self.players = players
        self.nSets = n_sets
        self.setType = set_type
        self.nLegs = n_legs
        self.legType = leg_type
        self.points = points
        self.out = out
        self.winner = winner
        self.sets = sets

    def __str__(self) -> str:
        game_string = f'GAME - {dt.datetime.fromtimestamp(self.ts)} -Version: {self.version}\n'
        game_string += f'Number of Players: {len(self.players)}\n'
        game_string += f'Number of Sets: {self.nSets}\n'
        game_string += f'Set Type: {self.setType}\n'
        game_string += f'Number of Legs: {self.nLegs}\n'
        game_string += f'Leg Type: {self.legType}\n'
        game_string += f'Points: {self.points}\n'
        game_string += f'Out: {self.out}\n'
        game_string += f"Set Wins: {[f'{player.name}: {self.get_set_wins(player)}' for player in self.players]}\n"
        game_string += f'Winner: {self.winner}\n'
        return game_string

    @staticmethod
    def __create_ts__() -> float:
        return dt.datetime.now().timestamp()

    def start(
            self,
            players: List[Player],
            n_sets: int,
            set_type: TypeSetLeg,
            n_legs: int,
            leg_type: TypeSetLeg,
            points: int,
            out: Out = Out(2)
    ) -> None:
        self.__init__(players=players, n_sets=n_sets, set_type=set_type, n_legs=n_legs, leg_type=leg_type,
                      points=points, out=out, repository=self.repository)
        try:
            self.repository.delete_game(str(self.ts))
        except DBEntryDoesNotExistError:
            pass
        self.logger.info('Game was started')
        if len(players) < 1:
            error_msg = 'At least one player is required to start a game.'
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        player_names = [player.name for player in players]
        if len(player_names) != len(set(player_names)):
            error_msg = 'Player names must be unique. No duplicate names allowed.'
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        self.started = True

    def finish(self) -> None:
        self.__init__(started=True, repository=self.repository)

    def save(self) -> bool:
        self.version = self.__create_ts__()
        save_thread = threading.Thread(target=self.repository.save, args=(self,))
        save_thread.start()
        return True

    def rollback(self, n_versions: int = 1) -> None:
        self.logger.info(f'Rolling back {n_versions} versions')
        try:
            prev_version = self.repository.list_versions(str(self.ts))[-n_versions - 1]
        except IndexError:
            error_msg = f"Version '{self.version}' is the first version of game '{self.ts}'.\
No previous version exists."
            self.logger.error(error_msg)
            raise GameRollBackNotPossibleError(error_msg)
        prev_game = self.repository.load(str(self.ts), prev_version)
        self.repository.delete_version(str(self.ts), str(self.version))
        self.__init__(
            ts=prev_game.ts,
            version=prev_game.version,
            started=prev_game.started,
            players=prev_game.players,
            n_sets=prev_game.nSets,
            set_type=prev_game.setType,
            n_legs=prev_game.nLegs,
            leg_type=prev_game.legType,
            points=prev_game.points,
            out=prev_game.out,
            winner=prev_game.winner,
            sets=prev_game.sets,
            repository=self.repository
        )

    def get_current_set(self) -> Set:
        if not self.started:
            error_msg = 'Tried to get Information about current Game, but no game has been started yet.'
            self.logger.error(error_msg)
            raise GameNotStartedError(error_msg)
        try:
            return self.sets[-1]
        except IndexError:
            error_msg = 'Tried to get Information about current Set. No set has been startet yet.'
            self.logger.error(error_msg)
            raise NoSetCreatedError(error_msg)

    def begin_new_set(self) -> None:
        try:
            current_set = self.get_current_set()
        except NoSetCreatedError:
            current_set = None
        if current_set and not current_set.winner:
            error_msg = 'Tried to begin new set. Current set has not been finished yet.'
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        if self.winner:
            error_msg = 'Game has already been finished (winner is declared). No new set can be created.'
            self.logger.error(error_msg)
            raise GameAlreadyFinishedError(error_msg)
        else:
            game_set = Set(
                players=self.players,
                game=self,
                set_type=self.setType,
                n_legs=self.nLegs,
                leg_type=self.legType,
                points=self.points,
                out=self.out
            )
            self.sets.append(game_set)

    def get_set_wins(self, player: Player) -> int:
        set_wins = 0
        for gameSet in self.sets:
            if gameSet.winner == player:
                set_wins += 1
        return set_wins

    def get_n_set_wins_for_game_win(self) -> int:
        if self.setType.value == BEST_OF:
            return self.nSets // 2 + 1
        elif self.setType.value == FIRST_TO:
            return self.nSets
        else:
            error_msg = 'Invalid Set Type'
            self.logger.error(error_msg)
            raise ValueError(error_msg)

    def get_avg_score(self, player: Player) -> float | None:
        score_count = 0
        n_rounds = 0
        for i_set in self.sets:
            set_score_count, set_rounds = i_set.__get_score_count_and_n_rounds__(player)
            score_count += set_score_count
            n_rounds += set_rounds
        try:
            return score_count / n_rounds
        except ZeroDivisionError:
            return None

    def get_thrown_darts(self, player: Player) -> int:
        thrown_darts = 0
        for i_set in self.sets:
            for leg in i_set.legs:
                for i_round in leg.rounds:
                    try:
                        thrown_darts += i_round.turns[player].get_thrown_darts()
                    except AttributeError:
                        pass
        return thrown_darts

    def get_score_count(self, attribute: str, desired_val: int, player: Player) -> int:
        n_counts = 0
        for i_set in self.sets:
            set_counts = i_set.get_score_count(attribute, desired_val, player)
            n_counts += set_counts
        return n_counts

    def get_n_hits_on_numbers(self) -> None:
        raise NotImplementedError('removed method -> use get_score_count instead with attribute: score')

    # TODO adapt down till leg with unit test
    def get_possible_and_successful_checkouts(self, player: Player) -> tuple[int, int]:
        n_possible_checkouts, n_successful_checkouts = 0, 0
        for i_set in self.sets:
            set_possible_checkouts, set_successful_checkouts = i_set.get_possible_and_successful_checkouts(player)
            n_possible_checkouts += set_possible_checkouts
            n_successful_checkouts += set_successful_checkouts
        return n_possible_checkouts, n_successful_checkouts

    def get_n_total_legs(self) -> int:
        n_total_legs = 0
        for i_set in self.sets:
            n_total_legs += len(i_set.legs)
        return n_total_legs
