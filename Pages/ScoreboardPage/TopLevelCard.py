import dash_bootstrap_components as dbc


class TopLevelCard:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(children: list, color: str = '#303030') -> dbc.Card:
        return dbc.Card(
            children = children,
            style = {
                'padding': '1rem',
                'margin-top': '1rem',
                'height': '5.25rem',
                'background-color': color,
                'display': 'flex',
                'justify-content': 'center'
            }
        )
