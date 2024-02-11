from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from Errors import *
from Logging.Logger import Logger
from Callbacks.CallbackBase import CallbackBase

from Models.DartScore import DartScore, SINGLE, DOUBLE, TRIPLE, MISS
from Pages.TyperPage import *

class ThrowDart(CallbackBase):
    def __init__(self, dependencyContainer):
        self.logger = Logger(__name__)
        self.app = dependencyContainer.app
        self.game = dependencyContainer.game
        self.inputs = [
            Input("0-score-button", "n_clicks"),
            Input("1-score-button", "n_clicks"),
            Input("2-score-button", "n_clicks"),
            Input("3-score-button", "n_clicks"),
            Input("4-score-button", "n_clicks"),
            Input("5-score-button", "n_clicks"),
            Input("6-score-button", "n_clicks"),
            Input("7-score-button", "n_clicks"),
            Input("8-score-button", "n_clicks"),
            Input("9-score-button", "n_clicks"),
            Input("10-score-button", "n_clicks"),
            Input("11-score-button", "n_clicks"),
            Input("12-score-button", "n_clicks"),
            Input("13-score-button", "n_clicks"),
            Input("14-score-button", "n_clicks"),
            Input("15-score-button", "n_clicks"),
            Input("16-score-button", "n_clicks"),
            Input("17-score-button", "n_clicks"),
            Input("18-score-button", "n_clicks"),
            Input("19-score-button", "n_clicks"),
            Input("20-score-button", "n_clicks"),
            Input("25-score-button", "n_clicks"),
            Input("50-score-button", "n_clicks"),
            Input("go-back-score-button", "n_clicks"),
            Input("score-confirm-button", "n_clicks"),
            Input("leg-win-confirm-button", "n_clicks"),
            Input("set-win-confirm-button", "n_clicks"),
            Input("rollback-not-possible-confirm-button", "n_clicks"),
            Input("typer-interval", "n_intervals")
        ]
        self.outputs = [
            Output("typer-score", "children"),
            Output("dart1-icon", "children"),
            Output("dart2-icon", "children"),
            Output("dart3-icon", "children"),
            Output("typer-player-name", "children"),
            Output("typer-leg-avg", "children"),
            Output("load-game-info-error-modal", "is_open"),
            Output("load-game-info-error-modal-body", "children"),
            Output("score-confirm-modal", "is_open"),
            Output("score-confirm-modal-body", "children"),
            Output("leg-win-confirm-modal", "is_open"),
            Output("leg-win-confirm-modal-body", "children"),
            Output("set-win-confirm-modal", "is_open"),
            Output("set-win-confirm-modal-body", "children"),
            Output("game-win-confirm-modal", "is_open"),
            Output("game-win-confirm-modal-body", "children"),
            Output("rollback-not-possible-confirm-modal", "is_open"),
            Output("typer-interval", "disabled"),
            Output("typer-interval", "interval")
        ]
        self.states = [
            State("x2-score-button", "active"),
            State("x3-score-button", "active"),
            State("score-confirm-modal", "is_open")
        ]
        self.emptyDartIcon = DartIcon().Build()
        self.emptyAllDartsIcon = [self.emptyDartIcon, self.emptyDartIcon, self.emptyDartIcon]
        self.ScoreConfirmationContent = ScoreConfirmationContent()
        self.OvershootConfirmationContent = OvershootConfirmationContent()
        self.LegWinConfirmationContent = LegWinConfirmationContent()
        self.SetWinConfirmationContent = SetWinConfirmationContent()
        self.GameWinConfirmationContent = GameWinConfirmationContent()
        self.UpdateInterval = 2000
        self.logger.info("Initialized ThrowDart Template")
    
    def Callback(
        self,
        s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10,
        s11, s12, s13, s14, s15, s16, s17, s18, s19, s20,
        s25, s50, goBack, scoreConfirm, legWinConfirm, setWinConfirm, rollBackNotPossibleConfirm,
        nUpdateInterval, x2_active, x3_active, scoreConfirmModalIsOpen
    ):
        prop_id = self.getPropFromContext(blockInital=False)

        if prop_id == "go-back-score-button":
            try:
                self.game.rollback()
            except GameRollBackNotPossibleError:
                return [
                    "N/A", *self.emptyAllDartsIcon, "Player", "0", 
                    False, None, False, None, False, None, False, None, False, None, True, True, self.UpdateInterval
                ]

        try:
            currentSet = self.game.getCurrentSet()
        except GameNotStartedError as e:
            return [
                "N/A", *self.emptyAllDartsIcon, "Player", "0", 
                True, str(e), False, None, False, None, False, None, False, None, False, True, self.UpdateInterval
            ]
        except NoSetCreatedError:
            self.game.beginNewSet()
            currentSet = self.game.getCurrentSet()
        
        try:
            currentLeg = currentSet.getCurrentLeg()
        except NoLegCreatedError:
            currentSet.beginNewLeg()
            currentLeg = currentSet.getCurrentLeg()
        
        try:
            currentRound = currentLeg.getCurrentRound()
        except NoRoundCreatedError:
            currentLeg.beginNewRound()
            currentRound = currentLeg.getCurrentRound()
        
        try:
            currentTurn = currentRound.getCurrentTurn()
        except NoTurnCreatedError:
            currentRound.beginNextTurn()
            currentTurn = currentRound.getCurrentTurn()

        if self.checkForDartsThrow(prop_id):
            score = int(prop_id.split("-")[0])
            if x2_active:
                multiplier = DOUBLE
            elif x3_active:
                multiplier = TRIPLE
            elif prop_id == "50-score-button":
                multiplier = DOUBLE
                score = 25
            elif prop_id == "0-score-button":
                multiplier = MISS
            else:
                multiplier = SINGLE
            currentTurn.throwDart(DartScore(score, multiplier))
            if currentTurn.getNextDart():
                self.game.save()
        
        dartIcons = self.generateDartsIcons(currentTurn)
        
        avgLegScore = self.calculateAvg(currentLeg, currentTurn.player)

        if prop_id == "score-confirm-button" or (prop_id == "typer-interval" and scoreConfirmModalIsOpen):
            if currentLeg.winner:
                legWinConfirmModalBody = self.LegWinConfirmationContent.Build(
                    currentLeg.winner.name,
                    currentLeg.getThrownDarts(currentLeg.winner)
                )
                return [
                    str(currentLeg.getPointsLeft(currentTurn.player)),
                    *dartIcons,
                    currentTurn.player.name, 0,
                    False, None, False, None, True, legWinConfirmModalBody, False, None, False, None, False, True, self.UpdateInterval
                ]
            try:
                try:
                    currentRound.beginNextTurn()
                    currentTurn = currentRound.getCurrentTurn()
                except AlreadyFinishedError:
                    pass
            except AllTurnsFinishedError:
                currentRound.finish()
                currentLeg.beginNewRound()
                currentRound = currentLeg.getCurrentRound()
                currentRound.beginNextTurn()
                currentTurn = currentRound.getCurrentTurn()
                self.game.save()
            dartIcons = self.generateDartsIcons(currentTurn)
            avgLegScore = self.calculateAvg(currentLeg, currentTurn.player)

        if prop_id == "leg-win-confirm-button":
            try:
                try:
                    currentLeg.finish()
                    currentSet.beginNewLeg()
                    currentLeg = currentSet.getCurrentLeg()
                    currentLeg.beginNewRound()
                    currentRound = currentLeg.getCurrentRound()
                    currentRound.beginNextTurn()
                    currentTurn = currentRound.getCurrentTurn()
                    dartIcons = self.generateDartsIcons(currentTurn)
                    avgLegScore = self.calculateAvg(currentLeg, currentTurn.player)
                except AlreadyFinishedError:
                    pass
            except AllLegsFinishedError:
                setWinConfirmModalBody = self.SetWinConfirmationContent.Build(
                    currentSet.winner.name,
                    round(currentSet.getAvgScore(currentSet.winner), 2),
                )
                return [
                    str(currentLeg.getPointsLeft(currentTurn.player)),
                    *dartIcons,
                    currentTurn.player.name, avgLegScore,
                    False, None, False, None, False, None, True, setWinConfirmModalBody, False, None, False, True, self.UpdateInterval
                ]
        
        if prop_id == "set-win-confirm-button":
            try:
                currentSet.finish()
                self.game.beginNewSet()
                currentSet = self.game.getCurrentSet()
                currentSet.beginNewLeg()
                currentLeg = currentSet.getCurrentLeg()
                currentLeg.beginNewRound()
                currentRound = currentLeg.getCurrentRound()
                currentRound.beginNextTurn()
                currentTurn = currentRound.getCurrentTurn()
                dartIcons = self.generateDartsIcons(currentTurn)
                avgLegScore = self.calculateAvg(currentLeg, currentTurn.player)
            except GameAlreadyFinishedError:
                gameWinConfirmModalBody = self.GameWinConfirmationContent.Build(
                    self.game.winner.name,
                    round(self.game.getAvgScore(self.game.winner), 2)
                )
                return [
                    str(currentLeg.getPointsLeft(currentTurn.player)),
                    *dartIcons,
                    currentTurn.player.name, avgLegScore,
                    False, None, False, None, False, None, False, None, True, gameWinConfirmModalBody, False, True, self.UpdateInterval
                ]
            except AlreadyFinishedError:
                pass

        if not currentTurn.getNextDart():
            try:
                currentTurn.finish()
            except AlreadyFinishedError:
                pass
            openScoreConfirmModal = True
            if currentTurn.overshooted:
                scoreConfirmModalBody = self.OvershootConfirmationContent.Build(
                    currentTurn.player.name,
                    currentTurn.getScore()
                )
            else:
                scoreConfirmModalBody = self.ScoreConfirmationContent.Build(
                    currentTurn.player.name,
                    currentTurn.getScore()
                )
            updateInterval = 5000
        else:
            openScoreConfirmModal = False
            scoreConfirmModalBody = None
            updateInterval = 1000
        
        if not prop_id == "typer-interval":
            print("FINISH")

        return [
            str(currentLeg.getPointsLeft(currentTurn.player)),
            *dartIcons,
            currentTurn.player.name, avgLegScore,
            False, None, openScoreConfirmModal, scoreConfirmModalBody, False, None, False, None, False, None, False, False, updateInterval
        ]

    def generateDartsIcons(self, currentTurn):
        dartIcons = []
        for dart in currentTurn.scores.values():
            if dart and not dart.NoDart:
                dartIcons.append(DartIcon().Build(color = "blue", score = dart.total))
            else:
                dartIcons.append(self.emptyDartIcon)
        return dartIcons

    def calculateAvg(self, currentLeg, player):
        avgLegScore = currentLeg.getAvgScore(player)
        if not avgLegScore:
            avgLegScore = 0
        avgLegScore = round(avgLegScore, 2)
        return avgLegScore
        
    
    def checkForDartsThrow(self, prop_id):
        if prop_id \
            and not prop_id.startswith("score-confirm") \
            and not prop_id.startswith("leg-win-confirm") \
            and not prop_id.startswith("set-win-confirm") \
            and not prop_id.startswith("rollback-not-possible") \
            and not prop_id.startswith("go-back") \
            and not prop_id.startswith("typer-interval"):
            return True
        else:
            return False