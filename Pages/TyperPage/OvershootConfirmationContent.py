from dash import html

from .ConfirmationContentBase import ConfirmationContentBase


class OvershootConfirmationContent(ConfirmationContentBase):
    def __init__(self) -> None:
        super().__init__()
        self.playerTextStyle = {
            'fontSize': '5vh',
            **self.baseStyle,
            **self.textBaseStyle
        }
        self.playerNameTextStyle = {
            'fontSize': '7.5vh',
            **self.baseStyle,
            **self.infoBaseStyle
        }
        self.scoreTextStyle = {
            'fontSize': '10vh',
            'color': '#993227',
            **self.baseStyle,
            **self.textBaseStyle
        }
        self.scoreStyle = {
            'fontSize': '15vh',
            'color': '#e74c3c',
            **self.baseStyle,
            **self.infoBaseStyle
        }

    def build(self, player_name: str, score: int) -> html.Div:
        return html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div('Player ', style=self.playerTextStyle),
                        html.Div(player_name, style=self.playerNameTextStyle),
                        html.Div(' overshot 😟', style=self.playerTextStyle),
                    ],
                    style=self.textRowStyle
                ),
                html.Div(
                    children=[
                        html.Div(score, style=self.scoreStyle),
                        html.H1('points', style=self.scoreTextStyle)
                    ],
                    style=self.textRowStyle
                )
            ],
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'flexDirection': 'column'
            }
        )
