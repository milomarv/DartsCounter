from typing import Any, Optional

from dash import html


class GameValue:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(
        value_name: str,
        content: Any,
        bottom_margin: str = '0.5vh',
        additional_text_style: Optional[dict] = None,
    ) -> html.Div:
        if not additional_text_style:
            additional_text_style = {}

        if isinstance(content, float):
            content = str(round(content, 2))

        if isinstance(content, type(None)):
            content = 'N/A'

        game_value = html.Div(
            children=[
                html.H6(
                    f'{value_name}:',
                    style={
                        **additional_text_style,
                        'color': 'grey',
                        'margin-bottom': '0.05vh',
                        'text-align': 'left',
                        'font-size': '2vh',
                    },
                ),
                html.H5(
                    content,
                    style={
                        **additional_text_style,
                        'fontWeight': 'bold',
                        'font-size': '2.5vh',
                    },
                ),
            ],
            style={
                'height': '6.5vh',
                'margin-bottom': bottom_margin,
                'display': 'flex',
                'flex-direction': 'column',
                'align-items': 'center',
                'align-content': 'flex-start',
            },
        )
        return game_value
