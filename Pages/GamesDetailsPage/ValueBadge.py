import dash_bootstrap_components as dbc


class ValueBadge:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(value) -> dbc.Badge:
        badge = dbc.Badge(
            value,
            style = {'fontSize': '1rem'}
        )
        return badge
