from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from Errors import *
from Logging.Logger import Logger
from Callbacks.CallbackBase import CallbackBase
from Models.DartScore import DartScore, SINGLE, DOUBLE, TRIPLE, MISS, NODART
from Pages.ScoreboardPage.PlayerCard import PlayerCard

class UpdatePlayerCards(CallbackBase):
    def __init__(self, dependencyContainer):
        self.logger = Logger(__name__)
        self.app = dependencyContainer.app
        self.game = dependencyContainer.game
        self.inputs = [
            Input("scoreboard-update-interval", "n_intervals"),
        ]
        self.outputs = [
            Output("scoreboard-player-area", "children")
        ]
        self.states = [
            State("game-filter-button", "className"),
            State("current-set-filter-button", "className"),
            State("current-leg-filter-button", "className")
        ]
        self.logger.info("Initialized Callback Template")
        self.playerCard = PlayerCard()
        self.emptyDartIcon = self.playerCard.dartIcon.Build()
    
    def Callback(self, n_intervals, gameFilter, setFilter, legFilter):
        try:
            if gameFilter == "btn btn-primary":
                queOn = self.game
            elif setFilter == "btn btn-primary":
                queOn = self.game.getCurrentSet()
            elif legFilter == "btn btn-primary":
                queOn = self.game.getCurrentSet().getCurrentLeg()
        except NoSetCreatedError:
            queOn = None
        except NoLegCreatedError:
            queOn = None
        except GameNotStartedError:
            raise PreventUpdate

        returnCols = []
        for player in self.game.players:
            # Get Player Name
            playerName = player.name

            # Get If Player is on current turn
            try:
                currentTurn = self.game.getCurrentSet().getCurrentLeg().getCurrentRound().getCurrentTurn()
                if currentTurn.player == player:
                    active = True
                else:
                    active = False
            except NoSetCreatedError:
                active = False


            # Get Player Current Score
            try:
                currentLeg = self.game.getCurrentSet().getCurrentLeg()
                playerPointsLeft = currentLeg.getPointsLeft(player)
            except KeyError:
                playerPointsLeft = "N/A"
            except NoSetCreatedError:
                playerPointsLeft = "N/A"
            except NoLegCreatedError:
                playerPointsLeft = "N/A"
            except GameNotStartedError:
                playerPointsLeft = "N/A"
            
            # Get Player Current Avg
            if queOn:
                playerAvg = queOn.getAvgScore(player)
                if not playerAvg:
                    playerAvg = "N/A"
                else:
                    playerAvg = round(playerAvg, 2)
            else:
                playerAvg = "N/A"
            
            # Get Player Thrown Darts
            if queOn:
                playerDarts = queOn.getThrownDarts(player)
                if not playerDarts:
                    playerDarts = 0
            else:
                playerDarts = 0
            
            # Get Set Wins
            setWins = self.game.getSetWins(player)

            # Get Leg Wins
            try:
                legWins = self.game.getCurrentSet().getLegWins(player)
            except NoSetCreatedError:
                legWins = 0
            except GameNotStartedError:
                legWins = 0
            
            # Get Singles, Doubles, Triples, Misses
            if queOn:
                try:
                    single = queOn.getMultipliers(player, SINGLE)
                    singlePerc = single/playerDarts
                    double = queOn.getMultipliers(player, DOUBLE)
                    doublePerc = double/playerDarts
                    triple = queOn.getMultipliers(player, TRIPLE)
                    triplePerc = triple/playerDarts
                    miss = queOn.getMultipliers(player, MISS)
                    missPerc = miss/playerDarts
                except ZeroDivisionError:
                    single, double, triple, miss = 0, 0, 0, 0
                    singlePerc, doublePerc, triplePerc, missPerc = 0, 0, 0, 0
            else:
                single, double, triple, miss = 0, 0, 0, 0
                singlePerc, doublePerc, triplePerc, missPerc = 0, 0, 0, 0

            # Get N Hits on Numbers
            numbers = self.playerCard.polarVals
            if queOn:
                nHits = []
                for n in numbers:
                    nHits.append(queOn.getNHitsOnNumbers(player, n))
            else:
                nHits = [0 for _ in numbers]

            # Get Players Last 3 Darts
            try:
                lastTurn = self.game.getCurrentSet().getCurrentLeg().getLastTurn(player)
                if lastTurn:
                    dartIcons = []
                    totalScore = 0
                    for dart in lastTurn.scores.values():
                        if dart and not dart.NoDart:
                            dartIcons.append(self.playerCard.dartIcon.Build(dart))
                            totalScore += dart.total
                        else:
                            dartIcons.append(self.emptyDartIcon)
                else:
                    dartIcons = [self.emptyDartIcon, self.emptyDartIcon, self.emptyDartIcon]
                    totalScore = 0
            except NoSetCreatedError:
                dartIcons = [self.emptyDartIcon, self.emptyDartIcon, self.emptyDartIcon]
                totalScore = 0
            
            # Get Possible Checkouts
            if queOn:
                nPossibleCheckouts, nSuccessfullCheckouts = queOn.getPossibleCheckouts(player)
            else:
                nPossibleCheckouts, nSuccessfullCheckouts = None, None
            if nPossibleCheckouts or nSuccessfullCheckouts:
                checkoutRate = f"{round(nSuccessfullCheckouts / nPossibleCheckouts * 100, 2)} %"
                checkoutCount = f"{nSuccessfullCheckouts}/{nPossibleCheckouts}"
            else:
                checkoutRate, checkoutCount = "N/A", "N/A"

            playerStatsCard = self.playerCard.Build(
                active, playerName, playerPointsLeft, playerAvg, playerDarts, setWins, legWins,
                single, double, triple, miss,
                singlePerc, doublePerc, triplePerc, missPerc, nHits,
                *dartIcons, totalScore,
                checkoutRate, checkoutCount
            )
            returnCols.append(playerStatsCard)
        return [returnCols]
        raise PreventUpdate
    
    def emptyDarts(self):
        dart1 = DartScore(0, NODART, NoDart=True)
        dart2 = DartScore(0, NODART, NoDart=True)
        dart3 = DartScore(0, NODART, NoDart=True)
        return dart1, dart2, dart3