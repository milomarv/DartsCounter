from typing import List, Optional

from Errors import AllLegsFinishedError, AlreadyFinishedError, NoLegCreatedError
from Logging.Logger import Logger
from .AbstractGamePart import AbstractGamePart
from .Leg import Leg
from .Out import Out
from .Player import Player
from .TypeSetLeg import BEST_OF, FIRST_TO, TypeSetLeg


class Set(AbstractGamePart):
    def __init__(
        self,
        players: List[Player],
        game,  # * cannot be imported from Game due to circular import  # noqa: ANN001
        set_type: TypeSetLeg,
        n_legs: int,
        leg_type: TypeSetLeg,
        points: int,
        out: Out = 2,
    ) -> None:
        super().__init__()
        self.logger = Logger(__name__)
        self.players = players
        self.game = game
        self.setType = set_type
        self.nLegs = n_legs
        self.legType = leg_type
        self.points = points
        self.out = out
        self.winner = None
        self.legs = []
        self.logger.info('New set created')

    def __str__(self) -> str:
        setString = 'SET\n'
        setString += f'Number of Players: {len(self.players)}\n'
        setString += f'Set Type: {self.setType}\n'
        setString += f'Number of Legs: {self.nLegs}\n'
        setString += f'Leg Type: {self.legType}\n'
        setString += f'Points: {self.points}\n'
        setString += f'Out: {self.out}\n'
        setString += f"Leg Wins: {[f'{player.name}: {self.get_leg_wins(player)}' for player in self.players]}\n"
        setString += f'Winner: {self.winner}\n'
        return setString

    def __get_score_count_and_n_rounds__(self, player: Player) -> tuple[int, int]:
        score_count = 0
        n_rounds = 0
        for i_leg in self.legs:
            set_score_count, set_rounds = i_leg.__get_score_count_and_n_rounds__(player)
            score_count += set_score_count
            n_rounds += set_rounds
        return score_count, n_rounds

    def get_current_leg(self, suppress_logger: bool = False) -> Leg:
        try:
            return self.legs[-1]
        except IndexError:
            error_msg = (
                'Tried to get Information about current Leg. No leg has been created yet.\
Use createNewLeg() to create a leg.'
            )
            if not suppress_logger:
                self.logger.error(error_msg)
            raise NoLegCreatedError(error_msg)

    def begin_new_leg(self) -> None:
        try:
            currentLeg = self.get_current_leg(suppress_logger=True)
        except NoLegCreatedError:
            currentLeg = None
        if currentLeg and not currentLeg.winner:
            error_msg = 'Tried to begin new leg. Current leg has not been finished yet.'
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        if self.winner:
            error_msg = 'Tried to begin new leg. Set has already been finished.'
            self.logger.error(error_msg)
            raise AllLegsFinishedError(error_msg)
        else:
            if self.game.get_n_total_legs():
                first_player = self.game.players.pop(0)
                self.game.players.append(first_player)
            leg = Leg(
                players=self.players,
                set_instance=self,
                leg_type=self.legType,
                points=self.points,
                out=self.out,
            )
            self.legs.append(leg)

    def get_leg_wins(self, player: Player) -> int:
        wins = 0
        for leg in self.legs:
            if leg.winner == player:
                wins += 1
        return wins

    def get_n_leg_wins_for_set_win(self) -> int:
        if self.legType.value == BEST_OF:
            return self.nLegs // len(self.players) + 1
        elif self.legType.value == FIRST_TO:
            return self.nLegs
        else:
            error_msg = f'Unknown Set Type: {self.setType}'
            self.logger.error(error_msg)
            raise ValueError(error_msg)

    def get_avg_score(self, player: Player) -> Optional[float]:
        score_count, n_rounds = self.__get_score_count_and_n_rounds__(player)
        try:
            return score_count / n_rounds
        except ZeroDivisionError:
            return None

    # TODO insert function into thrown darts Game
    def get_thrown_darts(self, player: Player) -> int:
        thrownDarts = 0
        for leg in self.legs:
            for i_round in leg.rounds:
                try:
                    thrownDarts += i_round.turns[player].get_thrown_darts()
                except AttributeError:
                    pass
        return thrownDarts

    def get_score_count(self, attribute: str, desired_val: int, player: Player) -> int:
        n_counts = 0
        for i_leg in self.legs:
            leg_counts = i_leg.get_score_count(attribute, desired_val, player)
            n_counts += leg_counts
        return n_counts

    def get_n_hits_on_numbers(self) -> None:
        raise NotImplementedError(
            'removed method -> use get_score_count instead with attribute: score'
        )

    def get_possible_and_successful_checkouts(self, player: Player) -> tuple[int, int]:
        n_possible_checkouts, n_successful_checkouts = 0, 0
        for i_leg in self.legs:
            leg_possible_checkouts, leg_successful_checkouts = (
                i_leg.get_possible_and_successful_checkouts(player)
            )
            n_possible_checkouts += leg_possible_checkouts
            n_successful_checkouts += leg_successful_checkouts
        return n_possible_checkouts, n_successful_checkouts

    def finish(self) -> None:
        if not self.winner:
            error_msg = 'Tried to finish set. Set has no winner yet.'
            self.logger.error(error_msg)
            raise AlreadyFinishedError(error_msg)
        self.logger.info(f'Set finished - Winner: {self.winner}')
        for player in self.players:
            if (
                self.game.get_set_wins(player)
                == self.game.get_n_set_wins_for_game_win()
            ):
                self.logger.info(
                    f'Set has been finished. Winner of the set: {player.name}'
                )
                self.game.winner = player
                break
