from dash import html

from .ConfirmationContentBase import ConfirmationContentBase


class LegWinConfirmationContent(ConfirmationContentBase):
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
        self.dartsTextStyle = {
            'fontSize': '5vh',
            **self.baseStyle,
            **self.textBaseStyle
        }
        self.dartsStyle = {
            'fontSize': '7.5vh',
            **self.baseStyle,
            **self.infoBaseStyle
        }

    def build(self, player_name: str, n_darts: int) -> html.Div:
        return html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div('Player ', style=self.playerTextStyle),
                        html.Div(player_name, style=self.playerNameTextStyle),
                        html.Div('won the Leg! 🎉', style=self.playerTextStyle),
                    ],
                    style=self.textRowStyle
                ),
                html.Div(
                    children=[
                        html.Div('Required', style=self.dartsTextStyle),
                        html.Div(n_darts, style=self.dartsStyle),
                        html.Div('Darts.', style=self.dartsTextStyle)
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
