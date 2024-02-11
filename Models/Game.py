import datetime as dt
from typing import List

from Errors import *
from Logging.Logger import Logger
from DB.GamesDB import GamesDB
from .Player import Player
from .Out import Out
from .TypeSetLeg import TypeSetLeg, BEST_OF, FIRST_TO
from .Set import Set

class Game:
    def __init__(
        self,
        ts: float = None,
        version: float = None,
        started: bool = False,
        players: List[Player] = [],
        nSets: int = None,
        setType: TypeSetLeg = None,
        nLegs: int = None,
        legType: TypeSetLeg = None,
        points: int = 0,
        out: Out = None,
        winner: Player = None,
        sets: List[Set] = [],
    ):
        self.logger = Logger(__name__)
        self.DB = GamesDB()
        if ts:
            self.ts = ts
        else:
            self.ts = self.__createTs__()
        if version:
            self.version = version
        else:
            self.version = self.ts
        self.started = started
        self.players = players
        self.nSets = nSets
        self.setType = setType
        self.nLegs = nLegs
        self.legType = legType
        self.points = points
        self.out = out
        self.winner = winner
        self.sets = sets
    
    def __str__(self):
        gameString = f"GAME - {dt.datetime.fromtimestamp(self.ts)} -Version: {self.version}\n"
        gameString += f"Number of Players: {len(self.players)}\n"
        gameString += f"Number of Sets: {self.nSets}\n"
        gameString += f"Set Type: {self.setType}\n"
        gameString += f"Number of Legs: {self.nLegs}\n"
        gameString += f"Leg Type: {self.legType}\n"
        gameString += f"Points: {self.points}\n"
        gameString += f"Out: {self.out}\n"
        gameString += f"Set Wins: {[f'{player.name}: {self.getSetWins(player)}' for player in self.players]}\n"
        gameString += f"Winner: {self.winner}\n"
        return gameString
    
    def __createTs__(self):
        return dt.datetime.now().timestamp()

    def start(
        self,
        players: List[Player], 
        nSets: int, 
        setType: TypeSetLeg, 
        nLegs: int, 
        legType: TypeSetLeg, 
        points: int, 
        out: Out = Out(2)
    ):
        self.__init__(None, None, True, players, nSets, setType, nLegs, legType, points, out, None, [])
        print(self.sets)
        try:
            self.DB.deleteGame(str(self.ts))
        except DBEntryDoesNotExistError:
            pass
        self.logger.info(f"Game was started")
        if len(players) < 1:
            error_msg = "At least one player is required to start a game."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        self.started = True
    
    def stop(self):
        self.__init__(None, None, True, [], None, None, None, None, None, None, [])
    
    def save(self):
        self.version = self.__createTs__()
        self.DB.save(self)
    
    def rollback(self, nVersions=1):
        self.logger.info(f"Rolling back {nVersions} versions")
        try:
            prevVersion = self.DB.listVersions(str(self.ts))[-nVersions-1]
        except IndexError:
            error_msg = f"Version '{self.version}' is the first version of game '{self.ts}'. No previous version exists."
            self.logger.error(error_msg)
            raise GameRollBackNotPossibleError(error_msg)
        prevGame = self.DB.load(str(self.ts), prevVersion)
        self.DB.deleteVersion(str(self.ts), self.version)
        self.__init__(
            ts=prevGame.ts,
            version=prevGame.version,
            started=prevGame.started,
            players=prevGame.players,
            nSets=prevGame.nSets,
            setType=prevGame.setType,
            nLegs=prevGame.nLegs,
            legType=prevGame.legType,
            points=prevGame.points,
            out=prevGame.out,
            winner=prevGame.winner,
            sets=prevGame.sets
        )
    
    def getCurrentSet(self):
        if not self.started:
            error_msg = "Tried to get Information about current Game, but no game has been started yet."
            self.logger.error(error_msg)
            raise GameNotStartedError(error_msg)
        try:
            return self.sets[-1]
        except IndexError:
            error_msg = "Tried to get Information about current Set. No set has been startet yet."
            self.logger.error(error_msg)
            raise NoSetCreatedError(error_msg)
    
    def beginNewSet(self):
        try:
            currentSet = self.getCurrentSet()
        except NoSetCreatedError:
            currentSet = None
        if currentSet and not currentSet.winner:
            error_msg = "Tried to begin new set. Current set has not been finished yet."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        if self.winner:
            error_msg = "Game has already been finished (winner is declared). No new set can be created."
            self.logger.error(error_msg)
            raise GameAlreadyFinishedError(error_msg)
        else:
            gameSet = Set(
                players=self.players,
                game=self,
                setType=self.setType,
                nLegs=self.nLegs,
                legType=self.legType,
                points=self.points,
                out=self.out
            )
            self.sets.append(gameSet)
    
    def getSetWins(self, player: Player):
        setWins = 0
        for gameSet in self.sets:
            if gameSet.winner == player:
                setWins += 1
        return setWins
    
    def getNSetWinsforGameWin(self):
        if self.setType.value == BEST_OF:
            return self.nSets // 2 + 1
        elif self.setType.value == FIRST_TO:
            return self.nSets
        else:
            error_msg = "Invalid Set Type"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
    
    def getAvgScore(self, player: Player):
        scoreCount = 0
        nRounds = 0
        for set in self.sets:
            for leg in set.legs:
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
        for set in self.sets:
            for leg in set.legs:
                for round in leg.rounds:
                    try:
                        thrownDarts += round.turns[player].getThrownDarts()
                    except AttributeError:
                        pass
        return thrownDarts
    
    def getMultipliers(self, player: Player, multiplier: int):
        nMultipliers = 0
        for set in self.sets:
            for leg in set.legs:
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
        for set in self.sets:
            for leg in set.legs:
                for round in leg.rounds:
                    playerTurn = round.turns[player]
                    if playerTurn:
                        for score in playerTurn.scores.values():
                            if not type(score) == type(None):
                                if score.score == number:
                                    nHits += 1
        return nHits
    
    def getNtotalLegs(self):
        nTotalLegs = 0
        for set in self.sets:
            nTotalLegs += len(set.legs)
        return nTotalLegs