from typing import Any

from dash import html


class GameValue:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(value_name: str, content: Any, bottom_padding: str = '1rem') -> html.Div:
        game_value = html.Div(
            children = [
                html.B(
                    f'{value_name}:',
                    style = {'textAlign': 'left'}
                ),
                content
            ],
            style = {
                'padding-bottom': bottom_padding,
                'display': 'flex',
                'flex-direction': 'column',
                'align-items': 'flex-start',
                'align-content': 'flex-start',
            }
        )
        return game_value
