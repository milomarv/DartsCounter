from typing import Optional

from Errors import AllTurnsFinishedError, AlreadyFinishedError, NoTurnCreatedError
from Logging.Logger import Logger
from Models import Player
from Models.AbstractGamePart import AbstractGamePart
from Models.Turn import Turn


# noinspection PyTypeChecker
class Round(AbstractGamePart):
    def __init__(self, players: Player, leg):
        super().__init__()
        self.logger = Logger(__name__)
        self.players = players
        self.leg = leg
        self.turns = {player: None for player in players}
        self.finished = False
        self.logger.info('New round created')

    def __str__(self) -> str:
        roundString = 'ROUND\n'
        roundString += f'Number of Players: {len(self.players)}\n'
        for player, turn in self.turns.items():
            if turn:
                roundString += f'{player}: Finished\n'
            else:
                roundString += f'{player}: Pending\n'
        return roundString

    def get_next_player(self) -> Optional[Player]:
        for player, turn in self.turns.items():
            if not turn:
                return player
        return None

    def begin_next_turn(self) -> None:
        try:
            currentTurn = self.get_current_turn(suppress_logger=True)
        except NoTurnCreatedError:
            currentTurn = None
        # noinspection PyUnresolvedReferences
        if currentTurn and not currentTurn.finished:
            # noinspection PyUnresolvedReferences
            error_msg = f'Tried to begin new turn.\
Current turn for Player {currentTurn.player.name} has not been finished yet.'
            self.logger.error(error_msg)
            raise AlreadyFinishedError(error_msg)
        else:
            nextPlayer = self.get_next_player()
            if not nextPlayer:
                error_msg = 'Tried to begin new turn. All turns have already been finished.'
                self.logger.error(error_msg)
                raise AllTurnsFinishedError(error_msg)
            turn = Turn(nextPlayer, self.leg)
            self.turns[nextPlayer] = turn

    def get_current_turn(self, suppress_logger: bool = False) -> Turn:
        currentTurn = None
        for player, turn in self.turns.items():
            if turn:
                currentTurn = turn
            else:
                break
        if currentTurn:
            return currentTurn
        else:
            error_msg = 'Tried to get Information about current Turn. No turn has been created yet.\
Use createNextTurn() to create a turn.'
            if not suppress_logger:
                self.logger.error(error_msg)
            raise NoTurnCreatedError(error_msg)

    def finish(self) -> None:
        if not self.leg.winner:
            for player, turn in self.turns.items():
                # noinspection PyUnresolvedReferences
                if not turn or not turn.finished:
                    error_msg = 'Tried to finish round. Not all turns have been finished yet.'
                    self.logger.error(error_msg)
                    raise ValueError(error_msg)
        self.finished = True
        self.logger.info('Round finished')
