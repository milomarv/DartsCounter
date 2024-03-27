import dash_bootstrap_components as dbc


class Card:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(children: list) -> dbc.Card:
        return dbc.Card(
            dbc.CardBody(
                children=children
            ),
            style={
                'height': '96vh',
                'margin-top': '2vh',
                'margin-bottom': '2vh',
                'margin-left': '1vw',
                'margin-right': '1vw',
                'padding': '15px'
            }
        )
