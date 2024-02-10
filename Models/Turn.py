from Models.Player import Player
from Logging.Logger import Logger
from Models.DartScore import DartScore, MISS

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
    
    def __overshoot__(self):
        self.logger.info(f"Player {self.player.name} overshoots the points left ({self.leg.getPointsLeft(self.player)}). All Scores of this turn are set to 0.")
        self.scores = {d: DartScore(0, MISS) for d in self.scores.keys()}
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
            if score.total == self.leg.getPointsLeft(self.player):
                if score.multiplier == self.leg.out.value:
                    self.checkout = True
                    self.leg.winner = self.player
                    self.scores[nextDart] = score
                    self.logger.info(f"Player {self.player.name} finished the leg with a checkout on {score}")
                    return
                else:
                    self.logger.info(f"Player {self.player.name} had wrong checkout")
                    self.__overshoot__()
                    return
            if score.total > self.leg.getPointsLeft(self.player) - self.leg.out.value:
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
            if score:
                thrownDarts += 1
        return thrownDarts
    
    def getScore(self):
        totalScore = 0
        for dart, score in self.scores.items():
            if score:
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
            raise ValueError(error_msg)
        self.finished = True
        self.logger.info(f"Player {self.player.name} finished turn with a total score of {self.getScore()} points")