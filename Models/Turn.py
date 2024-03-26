from typing import Optional

from Errors import AlreadyFinishedError, NotAllDartsThrownYetError
from Logging.Logger import Logger
from Models.AbstractGamePart import AbstractGamePart
from Models.DartScore import DartScore, MISS, NO_DART, POSSIBLE_SCORES
from Models.Player import Player


class Turn(AbstractGamePart):
    def __init__(self, player: Player, leg):
        super().__init__()
        self.logger = Logger(__name__)
        self.player = player
        self.leg = leg
        self.scores = {'Dart 1': None, 'Dart 2': None, 'Dart 3': None}
        self.overshot = False
        self.checkout = False
        self.finished = False
        self.logger.info(f'New turn started for Player {player.name}')

    def __str__(self) -> str:
        turnString = 'TURN\n'
        turnString += f'Player: {self.player.name}\n'
        for dart, score in self.scores.items():
            if score:
                turnString += f'{dart}: {score}\n'
            else:
                turnString += f'{dart}: Pending\n'
        turnString += f'Total Score: {self.get_score()}\n'
        return turnString

    @staticmethod
    def __get_possible_checkouts__(out_val: int = 2):
        checkouts = []
        if out_val == 1:
            checkouts = POSSIBLE_SCORES[1:]
        if out_val == 2 or out_val == 1:
            checkouts += [x * 2 for x in POSSIBLE_SCORES[1:]]
        if out_val == 3 or out_val == 1:
            checkouts += [x * 3 for x in POSSIBLE_SCORES[1:-1]]
        return checkouts

    def __overshoot__(self) -> None:
        self.logger.info(
            f'Player {self.player.name} overshoots the points left ({self.leg.get_points_left(self.player)}).\
All Scores of this turn are set to 0.')
        for dart, score in self.scores.items():
            if not score:
                self.scores[dart] = DartScore(0, NO_DART, no_dart=True)
            else:
                # noinspection PyUnresolvedReferences
                self.scores[dart] = DartScore(0, MISS, check_out_possible=score.check_out_possible)
        self.overshot = True

    def get_next_dart(self) -> Optional[str]:
        for dart, score in self.scores.items():
            if not score:
                return dart
        return None

    def throw_dart(self, score: DartScore) -> None:
        if self.leg.winner:
            error_msg = 'Tried to throw a dart. Leg has already been finished.'
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        if self.finished:
            error_msg = 'Tried to throw a dart. Turn has already been finished.'
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        if self.overshot:
            error_msg = 'Tried to throw a dart. Turn has already been finished because of overshooting.'
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        nextDart = self.get_next_dart()
        if nextDart:
            self.logger.info(f'Player {self.player.name} threw {nextDart}: {score}')
            possibleCheckouts = self.__get_possible_checkouts__(self.leg.out.value)
            if self.leg.get_points_left(self.player) in possibleCheckouts:
                score.check_out_possible = True
                score.check_out_success = False
            if score.total == self.leg.get_points_left(self.player):
                if score.multiplier == self.leg.out.value or self.leg.out.value == 1:
                    self.checkout = True
                    self.leg.winner = self.player
                    self.scores[nextDart] = score
                    for dart, dartScore in self.scores.items():
                        if not dartScore:
                            self.scores[dart] = DartScore(0, NO_DART, no_dart=True)
                    score.check_out_success = True
                    self.logger.info(f'Player {self.player.name} finished the leg with a checkout on {score}')
                    return
                else:
                    self.logger.info(f'Player {self.player.name} had wrong checkout')
                    self.scores[nextDart] = score
                    self.__overshoot__()
                    return
            if score.total > self.leg.get_points_left(self.player) - self.leg.out.value:
                self.scores[nextDart] = score
                self.__overshoot__()
                return
            self.scores[nextDart] = score
        else:
            error_msg = 'Tried to throw a dart. No darts left to throw in this turn!'
            self.logger.error(error_msg)
            raise ValueError(error_msg)

    def get_thrown_darts(self) -> int:
        thrownDarts = 0
        for dart, score in self.scores.items():
            # noinspection PyUnresolvedReferences
            if score and not score.no_dart:
                thrownDarts += 1
        return thrownDarts

    def get_score(self) -> int:
        totalScore = 0
        for dart, score in self.scores.items():
            # noinspection PyUnresolvedReferences
            if score and not score.no_dart:
                # noinspection PyUnresolvedReferences
                totalScore += score.total
        return totalScore

    def finish(self) -> None:
        if not self.checkout:
            for dart, score in self.scores.items():
                if not score:
                    error_msg = 'Tried to finish turn. Not all darts have been thrown yet.'
                    self.logger.error(error_msg)
                    raise NotAllDartsThrownYetError(error_msg)
        if self.finished:
            error_msg = 'Tried to finish turn. Turn has already been finished.'
            self.logger.error(error_msg)
            raise AlreadyFinishedError(error_msg)
        self.finished = True
        self.logger.info(f'Player {self.player.name} finished turn with a total score of {self.get_score()} points')
