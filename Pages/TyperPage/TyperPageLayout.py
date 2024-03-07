import dash_bootstrap_components as dbc
from dash import html, dcc

from Pages.Modals import *
from Pages.TyperPage.Card import Card
from Pages.TyperPage.DartIcon import DartIcon
from Pages.TyperPage.ScoreButton import ScoreButton


class TyperPageLayout:
    def __init__(self):
        self.card = Card()
        self.generalScoreButton = ScoreButton("secondary")
        self.specialScoreButton = ScoreButton("primary", fontMultiplier=0.5)
        self.returnButton = ScoreButton("danger", fontMultiplier=2, vhMultiplier=2)
        self.multiplierButton = ScoreButton("primary")
        self.dartIcon = DartIcon()
        self.loadGameInfoErrorModal = ErrorModal(
            "load-game-info",
            title="Load Game Information Error",
            children=[],
            closeAble=False
        )
        self.confrimScoreModal = ConfirmModal(
            "score",
            title="Player Score",
            children=[],
            closeAble=False
        )
        self.confirmLegWinModal = ConfirmModal(
            "leg-win",
            title="Leg Win",
            children=[],
            closeAble=False
        )
        self.confirmSetWinModal = ConfirmModal(
            "set-win",
            title="Set Win",
            children=[],
            closeAble=False
        )
        self.confirmGameWinModal = ConfirmModal(
            "game-win",
            title="Game Win",
            children=[],
            closeAble=False,
            size="xl",
            href="/"
        )
        self.infoRollbackNotPossibleModal = ConfirmModal(
            "rollback-not-possible",
            title="Rollback not possible",
            children=["Going back further is not possible. No previous states of the game are available."],
            closeAble=False
        )
        self.scoreCardTextStyle = {
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'flexDirection': 'column'
        }

    def Build(self):
        return html.Div([
            dbc.Row(
                children=[
                    dbc.Col(
                        self.card.Build(
                            children=[
                                html.Div(
                                    html.H1(
                                        "N/A",
                                        id="typer-score",
                                        style={
                                            **self.scoreCardTextStyle,
                                            'height': '30vh',
                                            'fontSize': '17.5vh',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ),
                                html.Div(
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                self.dartIcon.Build(),
                                                id="dart1-icon"
                                            ),
                                            dbc.Col(
                                                self.dartIcon.Build(),
                                                id="dart2-icon"
                                            ),
                                            dbc.Col(
                                                self.dartIcon.Build(),
                                                id="dart3-icon"
                                            ),
                                        ]
                                    ),
                                    style={
                                        **self.scoreCardTextStyle,
                                        'height': '10vh'
                                    }
                                ),
                                html.Div(style={"height": "8vh"}),
                                html.Div(
                                    html.H1(
                                        "Player:",
                                        style={
                                            **self.scoreCardTextStyle,
                                            'height': '5vh',
                                            'color': 'grey'
                                        }
                                    )
                                ),
                                html.Div(
                                    html.H1(
                                        "Player",  # TODO line break when to long Player Name
                                        id="typer-player-name",
                                        style={
                                            **self.scoreCardTextStyle,
                                            'height': '12vh',
                                            'fontSize': '7.5vh',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ),
                                html.Div(style={"height": "1vh"}),
                                html.Div(
                                    html.H2(
                                        "Average of Leg:",
                                        style={
                                            **self.scoreCardTextStyle,
                                            'height': '8vh',
                                            'color': 'grey'
                                        }
                                    )
                                ),
                                html.Div(
                                    html.H1(
                                        "0",
                                        id="typer-leg-avg",
                                        style={
                                            **self.scoreCardTextStyle,
                                            'height': '8vh',
                                            'fontSize': '6vh',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                )
                            ]
                        ),
                        width=4
                    ),
                    dbc.Col(
                        self.card.Build(
                            children=[
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            children=[
                                                self.generalScoreButton.Build("1", "1"),
                                                self.generalScoreButton.Build("5", "5"),
                                                self.generalScoreButton.Build("9", "9"),
                                                self.generalScoreButton.Build("13", "13"),
                                                self.generalScoreButton.Build("17", "17"),
                                            ]
                                        ),
                                        dbc.Col(
                                            children=[
                                                self.generalScoreButton.Build("2", "2"),
                                                self.generalScoreButton.Build("6", "6"),
                                                self.generalScoreButton.Build("10", "10"),
                                                self.generalScoreButton.Build("14", "14"),
                                                self.generalScoreButton.Build("18", "18"),
                                            ]
                                        ),
                                        dbc.Col(
                                            children=[
                                                self.generalScoreButton.Build("3", "3"),
                                                self.generalScoreButton.Build("7", "7"),
                                                self.generalScoreButton.Build("11", "11"),
                                                self.generalScoreButton.Build("15", "15"),
                                                self.generalScoreButton.Build("19", "19"),
                                            ]
                                        ),
                                        dbc.Col(
                                            children=[
                                                self.generalScoreButton.Build("4", "4"),
                                                self.generalScoreButton.Build("8", "8"),
                                                self.generalScoreButton.Build("12", "12"),
                                                self.generalScoreButton.Build("16", "16"),
                                                self.generalScoreButton.Build("20", "20"),
                                            ]
                                        ),
                                        dbc.Col(
                                            children=[
                                                self.specialScoreButton.Build("MISS", "0"),
                                                self.specialScoreButton.Build("BULL", "25"),
                                                self.specialScoreButton.Build("BULLS EYE", "50"),
                                                self.returnButton.Build("↻", "go-back")
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            self.multiplierButton.Build("DOUBLE", "x2")
                                        ),
                                        dbc.Col(
                                            self.multiplierButton.Build("TRIPLE", "x3")
                                        )
                                    ]
                                )
                            ]
                        ),
                        width=8
                    )
                ],
                style={
                    "width": "100vw"
                },
                className="g-0"
            ),
            self.loadGameInfoErrorModal.Build(),
            self.confrimScoreModal.Build(),
            self.confirmLegWinModal.Build(),
            self.confirmSetWinModal.Build(),
            self.confirmGameWinModal.Build(),
            self.infoRollbackNotPossibleModal.Build(),
            dcc.Interval(id="typer-interval", interval=1000, n_intervals=0)
        ])
