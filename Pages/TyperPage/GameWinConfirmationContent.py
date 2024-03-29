from dash import html

from .ConfirmationContentBase import ConfirmationContentBase


class GameWinConfirmationContent(ConfirmationContentBase):
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
        self.avgGameTextStyle = {
            'fontSize': '5vh',
            **self.baseStyle,
            **self.textBaseStyle
        }
        self.avgGameStyle = {
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
                        html.Div('won the Game! 🎉', style=self.playerTextStyle),
                    ],
                    style=self.textRowStyle
                ),
                html.Div(
                    children=[
                        html.Div('Got Average of: ', style=self.avgGameTextStyle),
                        html.Div(n_darts, style=self.avgGameStyle)
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
