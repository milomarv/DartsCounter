import dash_bootstrap_components as dbc


class ScoreBoardEditLabelField:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(value: str) -> dbc.Input:
        return dbc.Input(
            value = value
        )
