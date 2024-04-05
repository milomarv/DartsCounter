import dash_bootstrap_components as dbc
import dash_extensions as de
from dash import dcc, html

from Pages.ScoreboardPage.FilterButton import FilterButton
from Pages.ScoreboardPage.PlayerCard import PlayerCard
from Pages.ScoreboardPage.ScoreBoardEditLabelField import ScoreBoardEditLabelField
from Pages.ScoreboardPage.ScoreBoardLabelText import ScoreBoardLabelText
from Pages.ScoreboardPage.TopLevelCard import TopLevelCard


class ScoreboardPageLayout:
    def __init__(self) -> None:
        self.player_card = PlayerCard()
        self.filter_button = FilterButton()
        self.top_level_card = TopLevelCard()
        self.scoreboard_label_text = ScoreBoardLabelText()
        self.scoreboard_edit_label_field = ScoreBoardEditLabelField()

    def build(self) -> html.Div:
        return html.Div(
            children = [
                dbc.Row(
                    children = [
                        dbc.Col(
                            self.top_level_card.build(
                                children = [
                                    dbc.Row(
                                        children = [
                                            dbc.Col(
                                                de.Keyboard(
                                                    html.Div(
                                                        children = self.scoreboard_label_text.build(''),
                                                        id = 'scoreboard-label'
                                                    ),
                                                    captureKeys = ['Enter'],
                                                    id = 'edit-scoreboard-label-enter-input',
                                                ),
                                                width = 'auto'
                                            ),
                                            dbc.Col(
                                                dbc.Button(
                                                    html.Img(
                                                        src = './assets/edit.svg',
                                                        id = 'edit-scoreboard-label-svg',
                                                        style = {
                                                            'height': '2rem',
                                                        }
                                                    ),
                                                    id = 'edit-scoreboard-label'
                                                ),
                                                width = 'auto'
                                            ),
                                            dcc.Store(
                                                id = 'scoreboard-label-value',
                                                storage_type = 'session',
                                                data = 'Scoreboard',
                                            )
                                        ],
                                        align = 'center'
                                    )
                                ],
                                color = '#375a7f'
                            ),
                            width = 'auto'
                        ),
                        dbc.Col(
                            self.top_level_card.build(
                                children = [
                                    dbc.Row(
                                        children = [
                                            dbc.Col(
                                                'Filter:',
                                                style = {
                                                    'font-size': '1.5rem',
                                                    'color': '#808080'
                                                }
                                            ),
                                            dbc.Col(
                                                self.filter_button.build('Game', 'game')
                                            ),
                                            dbc.Col(
                                                self.filter_button.build('Current Set', 'current-set')
                                            ),
                                            dbc.Col(
                                                self.filter_button.build('Current Leg', 'current-leg', active = True)
                                            )
                                        ],
                                        align = 'center'
                                    )
                                ]
                            ),
                            width = 'auto'
                        )
                    ]
                ),
                html.Div(style = {'height': '0.5rem'}),
                html.Div(
                    dbc.Stack(
                        children = [
                            self.player_card.build(name = 'Player 1'),
                            self.player_card.build(name = 'Player 2'),
                            self.player_card.build(name = 'Player 3')
                        ],
                        id = 'scoreboard-player-area',
                        direction = 'horizontal',
                        gap = 5
                    ),
                    style = {
                        'overflowX': 'auto',
                        'width': '95vw'
                    }
                ),
                dcc.Interval(
                    id = 'scoreboard-update-interval',
                    interval = 1000,
                    n_intervals = 0
                )
            ],
            style = {
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'flexDirection': 'column',
                'height': '100vh'
            }
        )
