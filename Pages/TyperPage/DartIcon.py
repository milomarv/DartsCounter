from dash import html
import dash_bootstrap_components as dbc

class DartIcon:
    def __init__(self):
        pass

    def Build(self, color = "grey", score = "0"):
        return html.Div(
            children = [
                html.Img(
                    src = f"./assets/dart-{color}.svg",
                    style={
                        'height': '7.5vh',
                        'margin-bottom': '1vh'
                    }
                ),
                dbc.Badge(
                    html.H4(score),
                    style = {"width": "5rem"},
                )
            ],
            style = {
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'flexDirection': 'column'
            }
        )