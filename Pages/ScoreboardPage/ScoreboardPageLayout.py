import dash_bootstrap_components as dbc
from dash import dcc, html

from Pages.ScoreboardPage.FilterButton import FilterButton
from Pages.ScoreboardPage.PlayerCard import PlayerCard


class ScoreboardPageLayout:
    def __init__(self) -> None:
        self.playerCard = PlayerCard()
        self.filterButton = FilterButton()

    def build(self) -> html.Div:
        return html.Div(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(self.filterButton.build('Game', 'game')),
                        dbc.Col(self.filterButton.build('Current Set', 'current-set')),
                        dbc.Col(self.filterButton.build('Current Leg', 'current-leg', active=True))
                    ],
                ),
                html.Br(),
                html.Div(
                    dbc.Stack(
                        children=[
                            self.playerCard.build(name='Player 1'),
                            self.playerCard.build(name='Player 2'),
                            self.playerCard.build(name='Player 3')
                        ],
                        id='scoreboard-player-area',
                        direction='horizontal',
                        gap=5
                    ),
                    style={
                        'overflowX': 'auto',
                        'width': '95vw'
                    }
                ),
                dcc.Interval(
                    id='scoreboard-update-interval',
                    interval=1000,
                    n_intervals=0
                )
            ],
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'flexDirection': 'column',
                'height': '100vh'
            }
        )
