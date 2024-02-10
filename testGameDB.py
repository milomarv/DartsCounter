import time

from DB.GamesDB import GamesDB
from Models.Game import Game
from Models.Player import Player
from Models.TypeSetLeg import TypeSetLeg, FIRST_TO
from Models.DartScore import DartScore

game = Game()
gameDB = GamesDB()

# gameDB.save(game)
# gamesInDB = gameDB.listGames()
# print(gamesInDB)
# gameVersionsInDB = gameDB.listVersions(gamesInDB[-1])
# print(gameVersionsInDB)
# game = gameDB.load(gamesInDB[-1], gameVersionsInDB[0])
# print(game)

game.start(
    players = [Player("Player 1"), Player("Player 2")],
    nSets = 3,
    setType = TypeSetLeg(FIRST_TO),
    nLegs = 5,
    legType = TypeSetLeg(FIRST_TO),
    points = 501
)
game.beginNewSet()
currentSet = game.getCurrentSet()
currentSet.beginNewLeg()
currentLeg = currentSet.getCurrentLeg()
currentLeg.beginNewRound()
currentRound = currentLeg.getCurrentRound()
currentRound.beginNextTurn()
currentTurn = currentRound.getCurrentTurn()
currentTurn.throwDart(DartScore(20, 3))
game.save()
print(game.version)
time.sleep(1)
currentTurn.throwDart(DartScore(17, 3))
game.save()
print(game.version)
currentTurn.throwDart(DartScore(16, 3))
game.save()
print(game.version)

print(game.getCurrentSet().getCurrentLeg().getCurrentRound().getCurrentTurn())

game.rollback(2)

print(game.getCurrentSet().getCurrentLeg().getCurrentRound().getCurrentTurn())
currentTurn = game.getCurrentSet().getCurrentLeg().getCurrentRound().getCurrentTurn()
currentTurn.throwDart(DartScore(10, 3))
currentTurn.throwDart(DartScore(12, 3))

print(game.getCurrentSet().getCurrentLeg().getCurrentRound().getCurrentTurn())
