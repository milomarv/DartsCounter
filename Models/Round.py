from Errors import *
from Logging.Logger import Logger
from Models import Player
from Models.Turn import Turn

class Round:
    def __init__(self, players: Player, leg):
        self.logger = Logger(__name__)
        self.players = players
        self.leg = leg
        self.turns = {player: None for player in players}
        self.finished = False
        self.logger.info(f"New round created")
    
    def __str__(self):
        roundString = f"ROUND\n"
        roundString += f"Number of Players: {len(self.players)}\n"
        for player, turn in self.turns.items():
            if turn:
                roundString += f"{player}: Finished\n"
            else:
                roundString += f"{player}: Pending\n"
        return roundString
    
    def getNextPlayer(self):
        for player, turn in self.turns.items():
            if not turn:
                return player
        return None
    
    def beginNextTurn(self):
        try:
            currentTurn = self.getCurrentTurn(suppress_logger=True)
        except NoTurnCreatedError:
            currentTurn = None
        if currentTurn and not currentTurn.finished:
            error_msg = f"Tried to begin new turn. Current turn for Player {currentTurn.player.name} has not been finished yet."
            self.logger.error(error_msg)
            raise AlreadyFinishedError(error_msg)
        else:
            nextPlayer = self.getNextPlayer()
            if not nextPlayer:
                error_msg = "Tried to begin new turn. All turns have already been finished."
                self.logger.error(error_msg)
                raise AllTurnsFinishedError(error_msg)
            turn = Turn(nextPlayer, self.leg)
            self.turns[nextPlayer] = turn
    
    def getCurrentTurn(self, suppress_logger=False):
        currentTurn = None
        for player, turn in self.turns.items():
            if turn:
                currentTurn = turn
            else:
                break
        if currentTurn:
            return currentTurn
        else:
            error_msg = "Tried to get Information about current Turn. No turn has been created yet. Use createNextTurn() to create a turn."
            if not suppress_logger:
                self.logger.error(error_msg)
            raise NoTurnCreatedError(error_msg)
    
    def finish(self):
        if not self.leg.winner:
            for player, turn in self.turns.items():
                if not turn or not turn.finished:
                    error_msg = f"Tried to finish round. Not all turns have been finished yet."
                    self.logger.error(error_msg)
                    raise ValueError(error_msg)
        self.finished = True
        self.logger.info(f"Round finished")