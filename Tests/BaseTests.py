import unittest

from Models.DartScore import DOUBLE, DartScore, MISS, SINGLE, TRIPLE
from ModelsTests.GameSimulation import GameSimulation


class BaseTests(unittest.TestCase):
    # noinspection PyPep8Naming
    def setUp(self) -> None:
        self.simulation = GameSimulation

        self.simulation_avg_data = {
            'Player1': [
                (DartScore(20, TRIPLE), DartScore(1, SINGLE), DartScore(19, DOUBLE)),
                (DartScore(15, SINGLE), DartScore(7, DOUBLE), DartScore(12, TRIPLE)),
                (DartScore(5, DOUBLE), DartScore(20, TRIPLE), DartScore(3, SINGLE)),
            ],
            'Player2': [
                (DartScore(10, DOUBLE), DartScore(2, TRIPLE), DartScore(10, SINGLE)),
                (DartScore(8, SINGLE), DartScore(5, TRIPLE), DartScore(7, DOUBLE)),
                (DartScore(1, TRIPLE), DartScore(14, SINGLE), DartScore(6, DOUBLE)),
            ],
            'Player3': [
                (DartScore(4, SINGLE), DartScore(6, DOUBLE), DartScore(18, TRIPLE)),
                (DartScore(11, DOUBLE), DartScore(18, SINGLE), DartScore(4, TRIPLE)),
                [DartScore(5, TRIPLE)],
            ]
        }

        self.simulation_data = {
            'Player1': [
                (DartScore(17, DOUBLE), DartScore(5, TRIPLE), DartScore(15, SINGLE)),
                (DartScore(13, DOUBLE), DartScore(10, SINGLE), DartScore(11, TRIPLE)),
                (DartScore(8, SINGLE), DartScore(14, DOUBLE), DartScore(2, TRIPLE)),
            ],
            'Player2': [
                (DartScore(6, TRIPLE), DartScore(15, DOUBLE), DartScore(7, SINGLE)),
                (DartScore(9, DOUBLE), DartScore(4, TRIPLE), DartScore(12, SINGLE)),
                (DartScore(3, SINGLE), DartScore(13, DOUBLE), DartScore(6, TRIPLE)),
            ],
            'Player3': [
                (DartScore(2, TRIPLE), DartScore(10, SINGLE), DartScore(16, DOUBLE)),
                (DartScore(12, SINGLE), DartScore(17, TRIPLE), DartScore(4, DOUBLE)),
                (DartScore(14, DOUBLE), DartScore(6, TRIPLE), DartScore(10, SINGLE)),
            ]
        }

        self.simulation_checkout_data = {
            'Player1': [
                (DartScore(20, TRIPLE), DartScore(20, TRIPLE), DartScore(20, TRIPLE)),
                (DartScore(20, TRIPLE), DartScore(20, TRIPLE), DartScore(20, TRIPLE)),
                (DartScore(20, TRIPLE), DartScore(19, TRIPLE), DartScore(0, MISS, check_out_possible = True)),
                (DartScore(9, SINGLE, check_out_possible = True), DartScore(0, MISS), (DartScore(0, MISS)))
            ],
            'Player2': [
                (DartScore(20, TRIPLE), DartScore(20, TRIPLE), DartScore(20, TRIPLE)),
                (DartScore(20, TRIPLE), DartScore(20, TRIPLE), DartScore(20, TRIPLE)),
                (DartScore(20, TRIPLE), DartScore(0, MISS), DartScore(0, MISS)),
                (DartScore(19, TRIPLE), DartScore(0, MISS, check_out_possible = True),
                 DartScore(0, MISS, check_out_possible = True))
            ],
            'Player3': [
                (DartScore(20, TRIPLE), DartScore(20, TRIPLE), DartScore(20, TRIPLE)),
                (DartScore(20, TRIPLE), DartScore(20, TRIPLE), DartScore(20, TRIPLE)),
                (DartScore(20, TRIPLE), DartScore(19, TRIPLE), DartScore(0, MISS, check_out_possible = True)),
                (DartScore(0, MISS, check_out_possible = True), DartScore(0, MISS, check_out_possible = True),
                 DartScore(12, DOUBLE, check_out_possible = True, check_out_success = True))
            ],
        }

        self.simulation_turn_data = {
            'Player1': [
                (DartScore(12, SINGLE), DartScore(12, SINGLE))
            ]
        }
