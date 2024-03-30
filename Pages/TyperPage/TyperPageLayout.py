import dash_bootstrap_components as dbc
from dash import dcc, html

from Pages.Modals.ConfirmModal import ConfirmModal
from Pages.Modals.ErrorModal import ErrorModal
from Pages.TyperPage.Card import Card
from Pages.TyperPage.DartIcon import DartIcon
from Pages.TyperPage.ScoreButton import ScoreButton


class TyperPageLayout:
    def __init__(self) -> None:
        self.card = Card()
        self.generalScoreButton = ScoreButton('secondary')
        self.specialScoreButton = ScoreButton('primary', font_multiplier = 0.5)
        self.returnButton = ScoreButton('danger', font_multiplier = 2, vh_multiplier = 2)
        self.multiplierButton = ScoreButton('primary')
        self.dartIcon = DartIcon()
        self.loadGameInfoErrorModal = ErrorModal(
            'load-game-info',
            title = 'Load Game Information Error',
            children = [],
            close_able = False
        )
        self.confirmScoreModal = ConfirmModal(
            'score',
            title = 'Player Score',
            children = [],
            close_able = False
        )
        self.confirmLegWinModal = ConfirmModal(
            'leg-win',
            title = 'Leg Win',
            children = [],
            close_able = False
        )
        self.confirmSetWinModal = ConfirmModal(
            'set-win',
            title = 'Set Win',
            children = [],
            close_able = False
        )
        self.confirmGameWinModal = ConfirmModal(
            'game-win',
            title = 'Game Win',
            children = [],
            close_able = False,
            size = 'xl',
            href = '/'
        )
        self.infoRollbackNotPossibleModal = ConfirmModal(
            'rollback-not-possible',
            title = 'Rollback not possible',
            children = ['Going back further is not possible. No previous states of the game are available.'],
            close_able = False
        )
        self.scoreCardTextStyle = {
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'flexDirection': 'column'
        }

    def build(self) -> html.Div:
        return html.Div([
            dbc.Row(
                children = [
                    dbc.Col(
                        self.card.build(
                            children = [
                                html.Div(
                                    html.H1(
                                        'N/A',
                                        id = 'typer-score',
                                        style = {
                                            **self.scoreCardTextStyle,
                                            'height': '30vh',
                                            'fontSize': '17.5vh',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ),
                                html.Div(
                                    dbc.Row(
                                        children = [
                                            dbc.Col(
                                                self.dartIcon.build(),
                                                id = 'dart1-icon'
                                            ),
                                            dbc.Col(
                                                self.dartIcon.build(),
                                                id = 'dart2-icon'
                                            ),
                                            dbc.Col(
                                                self.dartIcon.build(),
                                                id = 'dart3-icon'
                                            ),
                                        ]
                                    ),
                                    style = {
                                        **self.scoreCardTextStyle,
                                        'height': '10vh'
                                    }
                                ),
                                html.Div(style = {'height': '8vh'}),
                                html.Div(
                                    html.H1(
                                        'Player:',
                                        style = {
                                            **self.scoreCardTextStyle,
                                            'height': '5vh',
                                            'color': 'grey'
                                        }
                                    )
                                ),
                                html.Div(
                                    html.H1(
                                        'Player',  # TODO line break when to long Player Name
                                        id = 'typer-player-name',
                                        style = {
                                            **self.scoreCardTextStyle,
                                            'height': '12vh',
                                            'fontSize': '7.5vh',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ),
                                html.Div(style = {'height': '1vh'}),
                                html.Div(
                                    html.H2(
                                        'Average of Leg:',
                                        style = {
                                            **self.scoreCardTextStyle,
                                            'height': '8vh',
                                            'color': 'grey'
                                        }
                                    )
                                ),
                                html.Div(
                                    html.H1(
                                        '0',
                                        id = 'typer-leg-avg',
                                        style = {
                                            **self.scoreCardTextStyle,
                                            'height': '8vh',
                                            'fontSize': '6vh',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                )
                            ]
                        ),
                        width = 4
                    ),
                    dbc.Col(
                        self.card.build(
                            children = [
                                dbc.Row(
                                    children = [
                                        dbc.Col(
                                            children = [
                                                self.generalScoreButton.build('1', '1'),
                                                self.generalScoreButton.build('5', '5'),
                                                self.generalScoreButton.build('9', '9'),
                                                self.generalScoreButton.build('13', '13'),
                                                self.generalScoreButton.build('17', '17'),
                                            ]
                                        ),
                                        dbc.Col(
                                            children = [
                                                self.generalScoreButton.build('2', '2'),
                                                self.generalScoreButton.build('6', '6'),
                                                self.generalScoreButton.build('10', '10'),
                                                self.generalScoreButton.build('14', '14'),
                                                self.generalScoreButton.build('18', '18'),
                                            ]
                                        ),
                                        dbc.Col(
                                            children = [
                                                self.generalScoreButton.build('3', '3'),
                                                self.generalScoreButton.build('7', '7'),
                                                self.generalScoreButton.build('11', '11'),
                                                self.generalScoreButton.build('15', '15'),
                                                self.generalScoreButton.build('19', '19'),
                                            ]
                                        ),
                                        dbc.Col(
                                            children = [
                                                self.generalScoreButton.build('4', '4'),
                                                self.generalScoreButton.build('8', '8'),
                                                self.generalScoreButton.build('12', '12'),
                                                self.generalScoreButton.build('16', '16'),
                                                self.generalScoreButton.build('20', '20'),
                                            ]
                                        ),
                                        dbc.Col(
                                            children = [
                                                self.specialScoreButton.build('MISS', '0'),
                                                self.specialScoreButton.build('BULL', '25'),
                                                self.specialScoreButton.build('BULLS EYE', '50'),
                                                self.returnButton.build('↻', 'go-back')
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    children = [
                                        dbc.Col(
                                            self.multiplierButton.build('DOUBLE', 'x2')
                                        ),
                                        dbc.Col(
                                            self.multiplierButton.build('TRIPLE', 'x3')
                                        )
                                    ]
                                )
                            ]
                        ),
                        width = 8
                    )
                ],
                style = {
                    'width': '100vw'
                },
                className = 'g-0'
            ),
            self.loadGameInfoErrorModal.build(),
            self.confirmScoreModal.build(),
            self.confirmLegWinModal.build(),
            self.confirmSetWinModal.build(),
            self.confirmGameWinModal.build(),
            self.infoRollbackNotPossibleModal.build(),
            dcc.Interval(id = 'typer-interval', interval = 1000, n_intervals = 0),
            html.Div('dummy-output-finish-game', style = {'display': 'none'})
        ])
