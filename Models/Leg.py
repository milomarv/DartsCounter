from typing import List

from Errors import *
from Logging.Logger import Logger
from .Player import Player
from .Out import Out
from .TypeSetLeg import TypeSetLeg, BEST_OF, FIRST_TO
from .Round import Round

class Leg:
    def __init__(
        self, 
        players: List[Player],
        set,
        legType: TypeSetLeg, 
        points: int, 
        out: Out = 2
    ):
        self.logger = Logger(__name__)
        self.players = players
        self.legType = legType
        self.points = points
        self.out = out
        self.set = set
        self.rounds = []
        self.winner = None
        self.logger.info(f"New leg created")
    
    def __str__(self):
        legString = f"LEG\n"
        legString += f"Number of Players: {len(self.players)}\n"
        legString += f"Leg Type: {self.legType}\n"
        legString += f"Points: {self.points}\n"
        legString += f"Out: {self.out}\n"
        return legString
    
    def getCurrentRound(self, suppress_logger=False):
        try:
            return self.rounds[-1]
        except IndexError:
            error_msg = "Tried to get Information about current Round. No round has been created yet. Use createNewRound() to create a round."
            if not suppress_logger:
                self.logger.error(error_msg)
            raise NoRoundCreatedError(error_msg)
    
    def getRoundNumber(self):
        if len(self.rounds):
            return len(self.rounds)
        else:
            error_msg = "Tried to get Information about current Round. No round has been created yet. Use createNewRound() to create a round."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
    
    def getThrownDarts(self, player: Player):
        thrownDarts = 0
        for round in self.rounds:
            try:
                thrownDarts += round.turns[player].getThrownDarts()
            except AttributeError:
                pass
        return thrownDarts
    
    def getScore(self, player: Player):
        score = 0
        for round in self.rounds:
            try:
                score += round.turns[player].totalScore
            except AttributeError:
                pass
        return score
    
    def getPointsLeft(self, player: Player):
        pointsLeft = self.points
        for round in self.rounds:
            try:
                pointsLeft -= round.turns[player].getScore()
            except AttributeError:
                pass
            except TypeError:
                pass
        return pointsLeft
    
    def getAvgScore(self, player: Player):
        scoreCount = 0
        nRounds = 0
        for round in self.rounds:
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
    
    def getMultipliers(self, player: Player, multiplier: int):
        nMultipliers = 0
        for round in self.rounds:
            playerTurn = round.turns[player]
            if playerTurn:
                for score in playerTurn.scores.values():
                    if not type(score) == type(None):
                        if score.multiplier == multiplier:
                            nMultipliers += 1
        return nMultipliers
    
    def getNHitsOnNumbers(self, player: Player, number: int):
        nHits = 0
        for round in self.rounds:
            playerTurn = round.turns[player]
            if playerTurn:
                for score in playerTurn.scores.values():
                    if not type(score) == type(None):
                        if score.score == number:
                            nHits += 1
        return nHits
            
    def beginNewRound(self):
        try:
            currentRound = self.getCurrentRound(suppress_logger=True)
        except NoRoundCreatedError:
            currentRound = None
        if currentRound and not currentRound.finished:
            error_msg = f"Tried to begin new round. Current round has not been finished yet."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        elif self.winner:
            error_msg = "Tried to begin new round. Leg has already been won."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        else:
            round = Round(self.players, self)
            self.rounds.append(round)
            self.logger.info(f"Round {len(self.rounds)} started")
    
    def finish(self):
        if not self.winner:
            error_msg = "Tried to finish leg. No declared winner yet."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        self.logger.info(f"Leg finished with winner: {self.winner.name}")
        for player in self.players:
            if self.set.getLegWins(player) == self.set.getNLegWinsforSetWin():
                self.logger.info(f"Set has been finished. Winner of the set: {player.name}")
                self.set.winner = player
                break

