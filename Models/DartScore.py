SINGLE = 1
DOUBLE = 2
TRIPLE = 3
MISS = None
NODART = None

class DartScore:
    def __init__(self, score: int, multiplier: str, NoDart: bool = False):
        if score not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25]:
            raise ValueError("Score must be between 0 and 20")
        if multiplier:
            if multiplier < 1 or multiplier > 3:
                raise ValueError("Multiplier must be between 1 and 3")
            if multiplier > 2 and score == 25:
                raise ValueError("Bull is of type Single or Double")
            if multiplier > 1 and score == 0:
                raise ValueError("Cannot apply multiplier to Miss or NoDart")
        
        self.score = score
        self.multiplier = multiplier
        if not multiplier:
            self.total = 0
            self.miss = True
        else:
            self.total = score * multiplier
            self.miss = False
        self.NoDart = NoDart
    
    def __str__(self):
        multiplierString = "Single" if self.multiplier == 1 \
            else "Double" if self.multiplier == 2 \
            else "Triple" if self.multiplier == 3 \
            else "Miss"
        return f"{multiplierString} {self.score} ({self.total} points) Miss: {self.miss} NoDart: {self.NoDart}"