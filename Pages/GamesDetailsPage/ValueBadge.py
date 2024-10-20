import dash_bootstrap_components as dbc


class ValueBadge:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(value: str) -> dbc.Badge:
        badge = dbc.Badge(value, style={'fontSize': '2vh'})
        return badge
