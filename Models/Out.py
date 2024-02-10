SINGLE_OUT = 1
DOUBLE_OUT = 2
MASTER_OUT = 3

class Out:
    def __init__(self, value):
        if value not in [1, 2, 3]:
            raise ValueError("Out value must be 1, 2 or 3")
        self.value = value

    def __str__(self):
        if self.value == 1:
            return "Single Out"
        elif self.value == 2:
            return "Double Out"
        else:
            return "Master Out"