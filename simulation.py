import random

from Logging import *
from Models import *


def randomScore():
    score = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 50])
    multiplier = random.choice([SINGLE, DOUBLE, TRIPLE, MISS])
    if multiplier == MISS:
        score = 0
    if score in [25, 50]:
        multiplier = SINGLE
    return DartScore(score, multiplier)


logger = Logger(__name__)
logger.info('Start Simulation')

playersDB = PlayersDB()

for name in ['Wilson', 'DerDicke', 'Lappler']:
    newPlayer = Player(name)
    playersDB.add(newPlayer)

players = playersDB.load()
# for player in players:
#     print(player)
playerWilson = players[0]

game = Game(
    players=players[:2],
    nSets=5,
    setType=TypeSetLeg(FIRST_TO),
    nLegs=3,
    legType=TypeSetLeg(BEST_OF),
    points=501,
    out=Out(DOUBLE_OUT)
)

while True:
    game.beginNewSet()
    currentSet = game.getCurrentSet()
    while True:
        currentSet.beginNewLeg()
        currentLeg = currentSet.getCurrentLeg()
        while True:
            currentLeg.beginNewRound()
            currentRound = currentLeg.getCurrentRound()
            for player in game.players:
                currentRound.beginNextTurn()
                currentTurn = currentRound.getCurrentTurn()
                for i in range(3):
                    currentTurn.throwDart(randomScore())
                    if currentTurn.overshooted or currentTurn.checkout:
                        break
                currentTurn.finish()
                if currentTurn.checkout:
                    break
            currentRound.finish()
            if currentLeg.winner:
                break
        currentLeg.finish()
        if currentSet.winner:
            break
    currentSet.finish()
    if game.winner:
        break
print(game)
