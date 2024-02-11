from typing import List

from Errors import *
from Logging.Logger import Logger
from .Player import Player
from .Out import Out
from .TypeSetLeg import TypeSetLeg, BEST_OF, FIRST_TO
from .Leg import Leg

class Set:
    def __init__(
        self, 
        players: List[Player],
        game,
        setType: TypeSetLeg,
        nLegs: int, 
        legType: TypeSetLeg, 
        points: int, 
        out: Out = 2
    ):
        self.logger = Logger(__name__)
        self.players = players
        self.game = game
        self.setType = setType
        self.nLegs = nLegs
        self.legType = legType
        self.points = points
        self.out = out
        self.winner = None
        self.legs = []
        self.logger.info(f"New set created")
    
    def __str__(self):
        setString = f"SET\n"
        setString += f"Number of Players: {len(self.players)}\n"
        setString += f"Set Type: {self.setType}\n"
        setString += f"Number of Legs: {self.nLegs}\n"
        setString += f"Leg Type: {self.legType}\n"
        setString += f"Points: {self.points}\n"
        setString += f"Out: {self.out}\n"
        setString += f"Leg Wins: {[f'{player.name}: {self.getLegWins(player)}' for player in self.players]}\n"
        setString += f"Winner: {self.winner}\n"
        return setString
    
    def getCurrentLeg(self, suppress_logger=False):
        try:
            return self.legs[-1]
        except IndexError:
            error_msg = "Tried to get Information about current Leg. No leg has been created yet. Use createNewLeg() to create a leg."
            if not suppress_logger:
                self.logger.error(error_msg)
            raise NoLegCreatedError(error_msg)
    
    def beginNewLeg(self):
        try:
            currentLeg = self.getCurrentLeg(suppress_logger=True)
        except NoLegCreatedError:
            currentLeg = None
        if currentLeg and not currentLeg.winner:
            error_msg = "Tried to begin new leg. Current leg has not been finished yet."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        if self.winner:
            error_msg = "Tried to begin new leg. Set has already been finished."
            self.logger.error(error_msg)
            raise AllLegsFinishedError(error_msg)
        else:
            if self.game.getNtotalLegs():
                first_player = self.game.players.pop(0)
                self.game.players.append(first_player)
            leg = Leg(
                players=self.players,
                set=self,
                legType=self.legType,
                points=self.points,
                out=self.out
            )
            self.legs.append(leg)
    
    def getLegWins(self, player: Player):
        wins = 0
        for leg in self.legs:
            if leg.winner == player:
                wins += 1
        return wins
    
    def getNLegWinsforSetWin(self):
        if self.legType.value == BEST_OF:
            return self.nLegs // len(self.players) + 1
        elif self.legType.value == FIRST_TO:
            return self.nLegs
        else:
            error_msg = f"Unknown Set Type: {self.setType}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
    
    def getAvgScore(self, player: Player):
        scoreCount = 0
        nRounds = 0
        for leg in self.legs:
            for round in leg.rounds:
                playerTurn = round.turns[player]
                if playerTurn:
                    oneDartHit = False
                    for score in playerTurn.scores.values():
                        if not type(score) == type(None):
                            scoreCount += score.total
                            oneDartHit = True
                    if oneDartHit:
                        nRounds += 1
        try:
            return scoreCount / nRounds
        except ZeroDivisionError:
            return None
    
    def getThrownDarts(self, player: Player):
        thrownDarts = 0
        for leg in self.legs:
            for round in leg.rounds:
                try:
                    thrownDarts += round.turns[player].getThrownDarts()
                except AttributeError:
                    pass
        return thrownDarts

    def getMultipliers(self, player: Player, multiplier: int):
        nMultipliers = 0
        for leg in self.legs:
            for round in leg.rounds:
                playerTurn = round.turns[player]
                if playerTurn:
                    for score in playerTurn.scores.values():
                        if not type(score) == type(None):
                            if score.multiplier == multiplier:
                                nMultipliers += 1
        return nMultipliers
    
    def getNHitsOnNumbers(self, player: Player, number: int):
        nHits = 0
        for leg in self.legs:
            for round in leg.rounds:
                playerTurn = round.turns[player]
                if playerTurn:
                    for score in playerTurn.scores.values():
                        if not type(score) == type(None):
                            if score.score == number:
                                nHits += 1
        return nHits
    
    def finish(self):
        if not self.winner:
            error_msg = "Tried to finish set. Set has no winner yet."
            self.logger.error(error_msg)
            raise AlreadyFinishedError(error_msg)
        self.logger.info(f"Set finished - Winner: {self.winner}")
        for player in self.players:
            if self.game.getSetWins(player) == self.game.getNSetWinsforGameWin():
                self.logger.info(f"Set has been finished. Winner of the set: {player.name}")
                self.game.winner = player
                break

