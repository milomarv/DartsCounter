FIRST_TO = 'firstto'
BEST_OF = 'bestof'


class TypeSetLeg:
    def __init__(self, value: str) -> None:
        if value not in ['firstto', 'bestof']:
            raise ValueError("TypeSetLeg value must be 'firstto' or 'bestof'")
        self.value = value

    def __str__(self) -> str:
        if self.value == 'firstto':
            return 'First to'
        else:
            return 'Best of'
