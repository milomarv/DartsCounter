from dash import html, dcc
import dash_bootstrap_components as dbc

from Pages.ScoreboardPage.PlayerCard import PlayerCard
from Pages.ScoreboardPage.FilterButton import FilterButton

class ScoreboardPageLayout:
    def __init__(self):
        self.playerCard = PlayerCard()
        self.filterButton = FilterButton()

    def Build(self):
        return html.Div(
            children = [
                dbc.Row(
                    children = [
                        dbc.Col(self.filterButton.Build("Game", "game")),
                        dbc.Col(self.filterButton.Build("Current Set", "current-set")),
                        dbc.Col(self.filterButton.Build("Current Leg", "current-leg", active = True))
                    ],
                ),
                html.Br(),
                html.Div(
                    dbc.Stack(
                        children = [
                            self.playerCard.Build(False, "Player 1"),
                            self.playerCard.Build(False, "Player 2"),
                            self.playerCard.Build(False, "Player 3")
                        ],
                        id = "scoreboard-player-area",
                        direction = "horizontal",
                        gap = 5
                    ),
                    style = {
                        "overflowX": "auto",
                        "width": "95vw"
                    }
                ),
                dcc.Interval(
                    id = "scoreboard-update-interval",
                    interval = 1000,
                    n_intervals = 0
                )
            ],
            style = {
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "flexDirection": "column",
                "height": "100vh"
            }
        )
