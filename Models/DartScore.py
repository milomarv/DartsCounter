SINGLE = 1
DOUBLE = 2
TRIPLE = 3
MISS = None
NO_DART = None

POSSIBLE_SCORES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25]


class DartScore:
    def __init__(self, score: int, multiplier: int, no_dart: bool = False, check_out_possible: bool = False,
                 check_out_success: bool = False):
        if score not in POSSIBLE_SCORES:
            raise ValueError('Score must be between 0 and 20 or 25')
        if multiplier:
            if multiplier < 1 or multiplier > 3:
                raise ValueError('Multiplier must be between 1 and 3')
            if multiplier > 2 and score == 25:
                raise ValueError('Bull is of type Single or Double')
            if multiplier > 1 and score == 0:
                raise ValueError('Cannot apply multiplier to Miss or NoDart')

        self.score = score
        self.multiplier = multiplier
        if not multiplier:
            self.total = 0
            self.miss = True
        else:
            self.total = score * multiplier
            self.miss = False
        self.no_dart = no_dart
        self.check_out_possible = check_out_possible
        self.check_out_success = check_out_success

    def __str__(self) -> str:
        multiplier_string = 'Single' if self.multiplier == 1 \
            else 'Double' if self.multiplier == 2 \
            else 'Triple' if self.multiplier == 3 \
            else 'Miss'
        return f'{multiplier_string} {self.score} ({self.total} points)'
