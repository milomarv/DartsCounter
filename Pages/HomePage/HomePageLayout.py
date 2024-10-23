import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash import html

from Models.Out import DOUBLE_OUT, MASTER_OUT, SINGLE_OUT
from Pages.HomePage.SetLegInput import SetLegInput
from Pages.MenuCard import MenuCard
from Pages.Modals.ConfirmModal import ConfirmModal
from Pages.Modals.ErrorModal import ErrorModal


class HomePageLayout:
    def __init__(self) -> None:
        self.card = MenuCard()
        self.setInput = SetLegInput('Set', 'set')
        self.legInput = SetLegInput('Leg', 'leg')
        self.start_game_error_modal = ErrorModal(
            'start-game', title='Start Game Error', children=[]
        )
        self.end_game_confirm_modal = ConfirmModal(
            'end-game',
            title='End Game',
            children=['Are you sure you want to end the game?'],
        )
        self.button_style = {'width': '250px', 'height': '50px', 'fontSize': '20px'}

    def build(self) -> html.Div:
        return html.Div(
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'flexDirection': 'column',
                'height': '100vh',
            },
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(html.H1('🎯 Darts Counter'), width='auto'),
                        dbc.Col(
                            html.H3(
                                dcc.Link(
                                    'v0.0.0', href='/release-notes', id='version-link'
                                )
                            ),
                        ),
                    ],
                    style={'alignItems': 'flex-end'},
                ),
                html.Br(),
                html.Div(
                    dbc.Stack(
                        children=[
                            self.card.build(
                                title='⚙️ Game Settings',
                                children=[
                                    dbc.Row(
                                        children=[
                                            dbc.Col(self.setInput.build()),
                                            dbc.Col(self.legInput.build()),
                                        ]
                                    ),
                                    html.Br(),
                                    html.Hr(),
                                    html.Br(),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                children=[
                                                    dbc.Label(
                                                        'Points:',
                                                        html_for='points-input',
                                                    ),
                                                    dbc.Input(
                                                        type='number',
                                                        id='points-input',
                                                        min=101,
                                                        step=100,
                                                    ),
                                                ]
                                            ),
                                            dbc.Col(
                                                children=[
                                                    dbc.Label(
                                                        'Out Variant:',
                                                        html_for='out-variant-select',
                                                    ),
                                                    dbc.Select(
                                                        id='out-variant-select',
                                                        options=[
                                                            {
                                                                'label': 'Single Out',
                                                                'value': SINGLE_OUT,
                                                            },
                                                            {
                                                                'label': 'Double Out',
                                                                'value': DOUBLE_OUT,
                                                            },
                                                            {
                                                                'label': 'Master Out',
                                                                'value': MASTER_OUT,
                                                            },
                                                        ],
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                            self.card.build(
                                title='🧑🏽 Players',
                                children=[
                                    html.Div(id='player-inputs-div'),
                                    html.Br(),
                                    dbc.Button(
                                        'Add Player',
                                        id='add-player',
                                        color='primary',
                                        className='mr-1',
                                    ),
                                ],
                            ),
                        ],
                        direction='horizontal',
                        gap=5,
                    )
                ),
                html.Br(),
                dbc.Button(
                    'Game',
                    id='start-stop-game-button',
                    n_clicks=0,
                    className='btn btn-secondary',
                    style=self.button_style,
                ),
                html.Br(),
                dbc.Switch(id='online-switch', value=False),
                dbc.Tooltip(
                    'This switch turns on the online mode. That means the Typerboard has a automatic refresh.\
So multiple Typerboards can be used at the same time.',
                    target='online-switch',
                    placement='left',
                ),
                html.Br(),
                dbc.Row(
                    children=[
                        dbc.Col(
                            dbc.Button(
                                '📲 Type in Scores',
                                href='/typer',
                                className='btn btn-primary',
                                style=self.button_style,
                            )
                        ),
                        dbc.Col(
                            dbc.Button(
                                '📊 Go to Scoreboard',
                                href='/scoreboard',
                                className='btn btn-primary',
                                style=self.button_style,
                            )
                        ),
                        dbc.Col(
                            dbc.Button(
                                '💾 Database',
                                href='/database',
                                className='btn btn-primary',
                                style=self.button_style,
                            )
                        ),
                    ]
                ),
                self.start_game_error_modal.build(),
                self.end_game_confirm_modal.build(),
            ],
        )
