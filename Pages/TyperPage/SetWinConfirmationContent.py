from dash import html
import dash_bootstrap_components as dbc

from .ConfirmationContentBase import ConfirmationContentBase

class SetWinConfirmationContent(ConfirmationContentBase):
    def __init__(self):
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
        self.avgSetTextStyle = {
            'fontSize': '5vh',
            **self.baseStyle,
            **self.textBaseStyle
        }
        self.avgSetStyle = {
            'fontSize': '7.5vh',
            **self.baseStyle,
            **self.infoBaseStyle
        }

    def Build(self, playerName: str, nDarts: int):
        return html.Div(
            children = [
                html.Div(
                    children = [
                        html.Div("Player ", style = self.playerTextStyle),
                        html.Div(playerName, style = self.playerNameTextStyle),
                        html.Div("won the Set! 🎉", style = self.playerTextStyle),
                    ],
                    style = self.textRowStyle
                ),
                html.Div(
                    children = [
                        html.Div("Got Average of: ", style = self.avgSetTextStyle),
                        html.Div(nDarts, style = self.avgSetStyle)
                    ],
                    style = self.textRowStyle
                )
            ],
            style = {
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'flexDirection': 'column'
            }
        )