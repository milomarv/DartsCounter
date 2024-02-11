from Errors import *
from Models.Player import Player
from Logging.Logger import Logger
from Models.DartScore import DartScore, MISS, NODART, POSSIBLESCORES

class Turn:
    def __init__(self, player: Player, leg):
        self.logger = Logger(__name__)
        self.player = player
        self.leg = leg
        self.scores = {"Dart 1": None, "Dart 2": None, "Dart 3": None}
        self.overshooted = False
        self.checkout = False
        self.finished = False
        self.logger.info(f"New turn started for Player {player.name}")
    
    def __str__(self):
        turnString = f"TURN\n"
        turnString += f"Player: {self.player.name}\n"
        for dart, score in self.scores.items():
            if score:
                turnString += f"{dart}: {score}\n"
            else:
                turnString += f"{dart}: Pending\n"
        turnString += f"Total Score: {self.getScore()}\n"
        return turnString

    def __getPossibleCheckouts__(self, outVal: int = 2):
        checkouts = []
        if outVal == 1:
            checkouts = POSSIBLESCORES[1:]
        if outVal == 2 or outVal == 1:
            checkouts += [x * 2 for x in POSSIBLESCORES[1:]]
        if outVal == 3 or outVal == 1:
            checkouts += [x * 3 for x in POSSIBLESCORES[1:-1]]
        return checkouts
    
    def __overshoot__(self):
        self.logger.info(f"Player {self.player.name} overshoots the points left ({self.leg.getPointsLeft(self.player)}). All Scores of this turn are set to 0.")
        for dart, score in self.scores.items():
            if not score:
                self.scores[dart] = DartScore(0, NODART, NoDart=True)
            else:
                self.scores[dart] = DartScore(0, MISS, checkOutPossible=score.checkOutPossible)
        self.overshooted = True
    
    def getNextDart(self):
        for dart, score in self.scores.items():
            if not score:
                return dart
        return None

    def throwDart(self, score: DartScore):
        if self.leg.winner:
            error_msg = "Tried to throw a dart. Leg has already been finished."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        if self.finished:
            error_msg = "Tried to throw a dart. Turn has already been finished."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        if self.overshooted:
            error_msg = "Tried to throw a dart. Turn has already been finished because of overshooting."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        nextDart = self.getNextDart()
        if nextDart:
            self.logger.info(f"Player {self.player.name} threw {nextDart}: {score}")
            possibleCheckouts = self.__getPossibleCheckouts__(self.leg.out.value)
            if self.leg.getPointsLeft(self.player) in possibleCheckouts:
                score.checkOutPossible = True
                score.checkOutSuccess = False
            if score.total == self.leg.getPointsLeft(self.player):
                if score.multiplier == self.leg.out.value or self.leg.out.value == 1:
                    self.checkout = True
                    self.leg.winner = self.player
                    self.scores[nextDart] = score
                    for dart, dartScore in self.scores.items():
                        if not dartScore:
                            self.scores[dart] = DartScore(0, NODART, NoDart=True)
                    score.checkOutSuccess = True
                    self.logger.info(f"Player {self.player.name} finished the leg with a checkout on {score}")
                    return
                else:
                    self.logger.info(f"Player {self.player.name} had wrong checkout")
                    self.scores[nextDart] = score
                    self.__overshoot__()
                    return
            if score.total > self.leg.getPointsLeft(self.player) - self.leg.out.value:
                self.scores[nextDart] = score
                self.__overshoot__()
                return
            self.scores[nextDart] = score
        else:
            error_msg = "Tried to throw a dart. No darts left to throw in this turn!"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
    
    def getThrownDarts(self):
        thrownDarts = 0
        for dart, score in self.scores.items():
            if score and not score.NoDart:
                thrownDarts += 1
        return thrownDarts
    
    def getScore(self):
        totalScore = 0
        for dart, score in self.scores.items():
            if score and not score.NoDart:
                totalScore += score.total
        return totalScore
    
    def finish(self):
        if not self.checkout:
            for dart, score in self.scores.items():
                if not score:
                    error_msg = "Tried to finish turn. Not all darts have been thrown yet."
                    self.logger.error(error_msg)
                    raise ValueError(error_msg)
        if self.finished:
            error_msg = "Tried to finish turn. Turn has already been finished."
            self.logger.error(error_msg)
            raise AlreadyFinishedError(error_msg)
        self.finished = True
        self.logger.info(f"Player {self.player.name} finished turn with a total score of {self.getScore()} points")