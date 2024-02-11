SINGLE_OUT = 1
DOUBLE_OUT = 2
MASTER_OUT = 3

class Out:
    def __init__(self, value: int):
        if int(value) == 1 or int(value) == 2 or int(value) == 3:
            self.value = int(value)
        else:
            raise ValueError("Out value must be 1, 2 or 3")

    def __str__(self):
        if self.value == 1:
            return "Single Out"
        elif self.value == 2:
            return "Double Out"
        else:
            return "Master Out"