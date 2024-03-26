import random
from unittest.mock import Mock

from Errors import NotAllDartsThrownYetError
from Models.AbstractGamePart import AbstractGamePart
from Models.DartScore import DOUBLE, DartScore, MISS, SINGLE, TRIPLE
from Models.Game import Game
from Models.Leg import Leg
from Models.Out import DOUBLE_OUT, Out
from Models.Player import Player
from Models.Round import Round
from Models.Set import Set
from Models.Turn import Turn
from Models.TypeSetLeg import FIRST_TO, TypeSetLeg


class GameSimulation:
    def __init__(self, simulation_data=dict[str, list[set[DartScore]]]) -> None:
        self.simulation_data = simulation_data
        # noinspection PyArgumentList
        self.players = {name: Player(name) for name in self.simulation_data.keys()}

        self.finished = False
        self.thrown_darts = 0

        self.game_repository_mock = Mock()

        self.game = Game(repository=self.game_repository_mock)

    @property
    def __random_score__(self) -> DartScore:
        score = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25])
        multiplier = random.choice([SINGLE, DOUBLE, TRIPLE, MISS])
        if multiplier == MISS:
            score = 0
        if score in [25, 50]:
            multiplier = SINGLE
        return DartScore(score, multiplier)

    def __simulate_darts_throws__(self, current_turn: Turn):
        # noinspection PyArgumentList
        try:
            scores = self.simulation_data[current_turn.player.name].pop(0)
        except IndexError:
            self.finished = True
            return current_turn

        for score in scores:
            current_turn.throw_dart(score)

            if current_turn.overshot or current_turn.checkout:
                if current_turn.checkout:
                    self.finished = True
                break

        try:
            current_turn.finish()
        except NotAllDartsThrownYetError:
            self.finished = True

        return current_turn

    @staticmethod
    def __finish_game_part__(game_part: AbstractGamePart) -> AbstractGamePart:
        game_part.finish()
        return game_part

    def __simulate_game_part__(
            self,
            current_part: AbstractGamePart,
            begin_new_function_attr: str,
            get_next_function_attr: str,
            return_attribute: str = None,
            loop_limit: int = None
    ) -> AbstractGamePart:
        iteration = 0

        while True:
            getattr(current_part, begin_new_function_attr)()
            next_part = getattr(current_part, get_next_function_attr)()

            match next_part:
                case Set():
                    self.__simulate_game_part__(next_part, 'begin_new_leg', 'get_current_leg')
                case Leg():
                    self.__simulate_game_part__(next_part, 'begin_new_round', 'get_current_round')
                case Round():
                    next_loop_limit = len(self.players)
                    self.__simulate_game_part__(next_part, 'begin_next_turn', 'get_current_turn', 'checkout',
                                                next_loop_limit)
                case Turn():
                    self.__simulate_darts_throws__(next_part)

            if self.finished:
                return current_part

            iteration += 1
            if loop_limit is not None and iteration >= loop_limit:
                return self.__finish_game_part__(current_part)
            elif return_attribute:
                if getattr(next_part, return_attribute):
                    return self.__finish_game_part__(current_part)
            elif getattr(current_part, 'winner'):
                return self.__finish_game_part__(current_part)

    def run(self) -> AbstractGamePart:
        self.game.start(
            players=list(self.players.values()),
            n_sets=3,
            set_type=TypeSetLeg(FIRST_TO),
            n_legs=3,
            leg_type=TypeSetLeg(FIRST_TO),
            points=501,
            out=Out(DOUBLE_OUT)
        )

        self.game = self.__simulate_game_part__(self.game, 'begin_new_set', 'get_current_set')

        return self.game
