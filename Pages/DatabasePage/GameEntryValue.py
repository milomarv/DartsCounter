from typing import Any

import dash_bootstrap_components as dbc
from dash import html


class GameEntryValue:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(value_name: str, content: Any, bottom_padding: str = '1rem') -> dbc.Col:
        return dbc.Col(
            dbc.Row(
                children = [
                    dbc.Col(
                        html.Div(
                            html.B(f'{value_name}:'),
                            style = {'padding-right': '0.5rem'}
                        ),
                        width = 'auto'
                    ),
                    dbc.Col(content)
                ],
                className = 'g-0',
                style = {'padding-bottom': bottom_padding}
            ),
            style = {'padding-right': '2rem'},
            width = 'auto'
        )
