class GameNotStartedError(Exception):
    pass


class AlreadyFinishedError(Exception):
    pass


class NoSetCreatedError(Exception):
    pass


class NoLegCreatedError(Exception):
    pass


class NoRoundCreatedError(Exception):
    pass


class NoTurnCreatedError(Exception):
    pass


class AllTurnsFinishedError(Exception):
    pass


class AllLegsFinishedError(Exception):
    pass


class GameAlreadyFinishedError(Exception):
    pass


class DBEntryAlreadyExistsError(Exception):
    pass


class DBEntryDoesNotExistError(Exception):
    pass


class GameRollBackNotPossibleError(Exception):
    pass


class NotAllDartsThrownYetError(Exception):
    pass
