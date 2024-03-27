import dash_bootstrap_components as dbc
from dash import html


class Card:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(title: str, children: list) -> dbc.Card:
        return dbc.Card(
            dbc.CardBody(
                children=[
                    html.H4(title, className='card-title'),
                    html.Br(),
                    html.Div(
                        html.Div(children=children),
                        style={
                            'maxHeight': '22.5rem',
                            'overflowY': 'auto',
                            'overflowX': 'hidden'
                        }
                    )
                ]
            ),
            style={
                'width': '30rem',
                'padding': '15px',
                'height': '30rem'
            }
        )
