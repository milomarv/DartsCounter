import dash_bootstrap_components as dbc
from dash import html


class GameDetailsPlayerDetailsModal:
    @staticmethod
    def build(player_name: str, content: html.Div) -> dbc.Modal:
        return dbc.Modal(
            children=[
                dbc.ModalHeader(
                    children=[
                        html.H3('Player Details:', style={'padding-right': '1vh'}),
                        html.H3(html.B(player_name)),
                    ],
                    style={'background-color': '#375a7f'},
                ),
                dbc.ModalBody(content),
            ],
            id='game-details-player-details-modal',
            is_open=True,
            centered=True,
        )
