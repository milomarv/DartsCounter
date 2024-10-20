from uuid import UUID
import dash_bootstrap_components as dbc
from dash import html

from Pages.GamesDetailsPage.GameValue import GameValue


# TODO continue here in callback LoadGameDetailsPlayerModal -> RELEASE
class GamePlayerCard:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(
        player_name: str,
        player_id: UUID,
        avg: float,
        thrown_darts: int,
        checkout_counter: int,
        set_wins: int,
        leg_wins: int,
        checkout_rate: str,
    ) -> dbc.Card:
        return dbc.Card(
            children=[
                dbc.CardHeader(
                    html.B(player_name),
                    style={
                        'background-color': '#375a7f',
                        'font-size': '2.5vh',
                        'padding': '1vh',
                    },
                ),
                dbc.CardFooter(
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[GameValue.build('Average', avg)],
                                ),
                                dbc.Col(
                                    children=[GameValue.build('Darts', thrown_darts)],
                                ),
                            ]
                        ),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        GameValue.build('Set Wins', set_wins),
                                    ]
                                ),
                                dbc.Col(
                                    children=[
                                        GameValue.build('Leg Wins', leg_wins),
                                    ]
                                ),
                            ]
                        ),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        GameValue.build('Checkouts', checkout_counter),
                                    ]
                                ),
                                dbc.Col(
                                    children=[
                                        GameValue.build('Checkout Rate', checkout_rate),
                                    ]
                                ),
                            ]
                        ),
                        dbc.Button(
                            'Details',
                            color='primary',
                            style={'width': '75%'},
                            id={
                                'type': 'game-details-player-button',
                                'index': str(player_id),
                            },
                        ),
                    ],
                    style={'background-color': '#444444', 'font-size': '2vh'},
                ),
            ],
            style={'padding-bottom': '1rem', 'border': '0', 'width': '100%'},
        )
