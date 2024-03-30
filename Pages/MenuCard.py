from typing import Optional

import dash_bootstrap_components as dbc
from dash import html


class MenuCard:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(
        title: str,
        children: list,
        identifier: Optional[str] = None,
        width: Optional[str] = '30rem',
        max_height_rem: int = 30
    ) -> dbc.Card:
        menu_card = dbc.Card(
            dbc.CardBody(
                children = [
                    html.H4(title, className = 'card-title'),
                    html.Br(),
                    html.Div(
                        html.Div(children = children),
                        style = {
                            'maxHeight': f'{max_height_rem - 7.5}rem',
                            'overflowY': 'auto',
                            'overflowX': 'hidden'
                        }
                    )
                ]
            ),
            style = {
                'width': width,
                'padding': '15px',
                'height': f'{max_height_rem}rem'
            }
        )

        if identifier is not None:
            menu_card.id = identifier

        return menu_card
