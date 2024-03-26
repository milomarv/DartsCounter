from typing import List

from Errors import AlreadyFinishedError, NoRoundCreatedError
from Logging.Logger import Logger
from .AbstractGamePart import AbstractGamePart
from .Out import Out
from .Player import Player
from .Round import Round
from .Turn import Turn
from .TypeSetLeg import TypeSetLeg


class Leg(AbstractGamePart):
    def __init__(
            self,
            players: List[Player],
            set_instance,
            leg_type: TypeSetLeg,
            points: int,
            out: Out = 2
    ):
        super().__init__()
        self.logger = Logger(__name__)
        self.players = players
        self.legType = leg_type
        self.points = points
        self.out = out
        self.set = set_instance
        self.rounds = []
        self.winner = None
        self.logger.info('New leg created')

    def __str__(self) -> str:
        leg_string = 'LEG\n'
        leg_string += f'Number of Players: {len(self.players)}\n'
        leg_string += f'Leg Type: {self.legType}\n'
        leg_string += f'Points: {self.points}\n'
        leg_string += f'Out: {self.out}\n'
        return leg_string

    def __get_score_count_and_n_rounds__(self, player: Player) -> tuple[int, int]:
        score_count = 0
        n_rounds = 0
        for i_round in self.rounds:
            player_turn = i_round.turns[player]
            if player_turn:
                one_dart_hit = False
                for score in player_turn.scores.values():
                    if type(score) is not type(None) and not score.no_dart:
                        score_count += score.total
                        one_dart_hit = True
                if one_dart_hit:
                    n_rounds += 1
        return score_count, n_rounds

    def get_current_round(self, suppress_logger: bool = False) -> Round:
        try:
            return self.rounds[-1]
        except IndexError:
            error_msg = 'Tried to get Information about current Round. No round has been created yet. \
Use createNewRound() to create a round.'
            if not suppress_logger:
                self.logger.error(error_msg)
            raise NoRoundCreatedError(error_msg)

    def get_round_number(self) -> int:
        if len(self.rounds):
            return len(self.rounds)
        else:
            error_msg = 'Tried to get Information about current Round. No round has been created yet. \
Use createNewRound() to create a round.'
            self.logger.error(error_msg)
            raise ValueError(error_msg)

    # TODO insert into Set function get_thrown darts
    def get_thrown_darts(self, player: Player) -> int:
        thrown_darts = 0
        for i_round in self.rounds:
            try:
                thrown_darts += i_round.turns[player].get_thrown_darts()
            except AttributeError:
                pass
        return thrown_darts

    def get_points_left(self, player: Player) -> int:
        points_left = self.points
        for i_round in self.rounds:
            try:
                points_left -= i_round.turns[player].get_score()
            except AttributeError:
                pass
            except TypeError:
                pass
        return points_left

    def get_last_turn(self, player: Player) -> Turn:
        last_turn = None
        for i_round in self.rounds[::-1]:
            if type(i_round.turns[player]) is not type(None):
                last_turn = i_round.turns[player]
            if last_turn:
                break
        return last_turn

    def get_avg_score(self, player: Player) -> float | None:
        score_count, n_rounds = self.__get_score_count_and_n_rounds__(player)
        try:
            return score_count / n_rounds
        except ZeroDivisionError:
            return None

    def get_score_count(self, attribute: str, desired_val: int, player: Player) -> int:
        n_counts = 0
        for i_round in self.rounds:
            player_turn = i_round.turns[player]
            if player_turn:
                for score in player_turn.scores.values():
                    if type(score) is not type(None) and not score.no_dart:
                        if getattr(score, attribute) == desired_val:
                            n_counts += 1
        return n_counts

    def get_n_hits_on_numbers(self) -> None:
        raise NotImplementedError('removed method -> use get_score_count instead with attribute: score')

    def get_possible_and_successful_checkouts(self, player: Player) -> tuple[int, int]:
        n_possible_checkouts, n_successful_checkouts = 0, 0
        for i_round in self.rounds:
            player_turn = i_round.turns[player]
            if player_turn:
                for score in player_turn.scores.values():
                    if type(score) is not type(None) and not score.no_dart:
                        if score.check_out_possible:
                            n_possible_checkouts += 1
                        if score.check_out_success:
                            n_successful_checkouts += 1
        return n_possible_checkouts, n_successful_checkouts

    def begin_new_round(self) -> None:
        try:
            current_round = self.get_current_round(suppress_logger=True)
        except NoRoundCreatedError:
            current_round = None
        if current_round and not current_round.finished:
            error_msg = 'Tried to begin new round. Current round has not been finished yet.'
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        elif self.winner:
            error_msg = 'Tried to begin new round. Leg has already been won.'
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        else:
            i_round = Round(self.players, self)
            self.rounds.append(i_round)
            self.logger.info(f'Round {len(self.rounds)} started')

    def finish(self) -> None:
        if not self.winner:
            error_msg = 'Tried to finish leg. No declared winner yet.'
            self.logger.error(error_msg)
            raise AlreadyFinishedError(error_msg)
        self.logger.info(f'Leg finished with winner: {self.winner.name}')
        for player in self.players:
            if self.set.get_leg_wins(player) == self.set.get_n_leg_wins_for_set_win():
                self.logger.info(f'Set has been finished. Winner of the set: {player.name}')
                self.set.winner = player
                break
