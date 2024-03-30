import dash_bootstrap_components as dbc


class PlayerBadge:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(name: str) -> dbc.Col:
        return dbc.Col(
            dbc.Badge(
                name,
                color = 'primary',
                style = {
                    'margin-right': '0.35rem'
                }
            ),
            width = 'auto'
        )
