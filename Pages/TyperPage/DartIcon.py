import dash_bootstrap_components as dbc
from dash import html

from Models.DartScore import DartScore


class DartIcon:
    def __init__(self, flex_direction='column', icon_size: float = 1.0, padding_bottom=None):
        self.flexDirection = flex_direction
        self.iconSize = icon_size
        self.paddingBottom = padding_bottom

    def build(self, dart_score: DartScore = None) -> html.Div:
        if not dart_score or dart_score.no_dart:
            color = 'grey'
            prefix = ''
            score = 0
        else:
            color = 'blue'
            score = dart_score.score
            if dart_score.multiplier == 2:
                prefix = 'D'
            elif dart_score.multiplier == 3:
                prefix = 'T'
            else:
                prefix = ''

        return html.Div(
            children=[
                html.Img(
                    src=f'./assets/dart-{color}.svg',
                    style={
                        'height': f'{7.5 * self.iconSize}vh',
                        'margin-bottom': '1vh',
                        'margin-left': '1rem',
                        'margin-right': '1rem'
                    }
                ),
                dbc.Badge(
                    f'{prefix}{score}',
                    style={
                        'width': '5rem',
                        'fontSize': '1.5rem',
                        'fontWeight': 'bold'
                    },
                )
            ],
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'flexDirection': self.flexDirection,
                'padding-bottom': self.paddingBottom
            }
        )
