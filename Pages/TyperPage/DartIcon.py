from dash import html
import dash_bootstrap_components as dbc

from Models.DartScore import DartScore

class DartIcon:
    def __init__(self, flexDirection = "column", iconSize: float = 1.0, paddingBottom = None):
        self.flexDirection = flexDirection
        self.iconSize = iconSize
        self.paddingBottom = paddingBottom

    def Build(self, dartScore: DartScore = None):
        if not dartScore or dartScore.NoDart:
            color = "grey"
            prefix = ""
            score = 0
        else:
            color = "blue"
            score = dartScore.score
            if dartScore.multiplier == 2:
                prefix = "D"
            elif dartScore.multiplier == 3:
                prefix = "T"
            else:
                prefix = ""

        return html.Div(
            children = [
                html.Img(
                    src = f"./assets/dart-{color}.svg",
                    style={
                        'height': f'{7.5*self.iconSize}vh',
                        'margin-bottom': '1vh',
                        "margin-left": "1rem",
                        "margin-right": "1rem"
                    }
                ),
                dbc.Badge(
                    f"{prefix}{score}",
                    style = {
                        "width": "5rem",
                        "fontSize": "1.5rem",
                        "fontWeight": "bold"
                    },
                )
            ],
            style = {
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'flexDirection': self.flexDirection,
                "padding-bottom": self.paddingBottom
            }
        )