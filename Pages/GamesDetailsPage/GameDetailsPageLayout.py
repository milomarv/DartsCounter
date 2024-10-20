import dash_bootstrap_components as dbc
from dash import html
from Pages.GamesDetailsPage.GameDetailsCard import GamesDetailsCard
from Pages.GamesDetailsPage.PlaceholderText import PlaceholderText


# TODO empty game /game-details/<NO GAME TS HERE>
# TODO loading ugly format
class GamesDetailsPageLayout:
    def __init__(self) -> None:
        self.details_card = GamesDetailsCard()
        self.placeholder_text = PlaceholderText()

    def build(self) -> html.Div:
        return html.Div(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                dbc.Card(
                                    children=['Game Details'],
                                    id='game-details-title',
                                    color='primary',
                                    style={
                                        'padding': '1.5vh',
                                        'height': '8.5vh',
                                        'font-size': '3.5vh',
                                        'display': 'flex',
                                        'flex-direction': 'row',
                                    },
                                ),
                                html.Div(
                                    style={
                                        'height': '2.5vh',
                                    }
                                ),
                                self.details_card.build(
                                    title='Set and Leg Wins',
                                    content=[
                                        self.placeholder_text.build(
                                            '⌛ Loading...',
                                            'game-details-graph-div',
                                            height='100%',
                                        )
                                    ],
                                    height='44vh',
                                    width='100%',
                                ),
                                html.Div(style={'height': '2.5vh'}),
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            self.details_card.build(
                                                title='Statistics',
                                                content=[
                                                    self.placeholder_text.build(
                                                        '⌛ Loading...',
                                                        'game-details-statistics-div',
                                                    )
                                                ],
                                                height='30vh',
                                                width='100%',
                                            )
                                        ),
                                        dbc.Col(
                                            self.details_card.build(
                                                title='Operations',
                                                content=[
                                                    self.placeholder_text.build(
                                                        # TODO Coming Soon
                                                        '⌛ Coming soon!',
                                                        'game-details-operations-div',
                                                    )
                                                ],
                                                height='30vh',
                                                width='100%',
                                            ),
                                            width=3,
                                            style={'padding-left': '1vw'},
                                        ),
                                    ]
                                ),
                            ],
                            width='auto',
                            style={'max-width': '50vw'},
                        ),
                        dbc.Col(
                            children=self.details_card.build(
                                title='Set Details',
                                content=[
                                    self.placeholder_text.build(
                                        # TODO Coming Soon
                                        '⌛ Coming soon!',
                                        'game-details-set-leg-throw-details',
                                    )
                                ],
                                height='87.25vh',
                                width='20vw',
                            ),
                            width='auto',
                            style={'padding-left': '1vw'},
                        ),
                        dbc.Col(
                            children=self.details_card.build(
                                title='Player Details',
                                content=[
                                    self.placeholder_text.build(
                                        # TODO Coming Soon
                                        '⌛ Coming soon!',
                                        'game-details-player-details',
                                    )
                                ],
                                height='87.25vh',
                                width='20vw',
                            ),
                            width='auto',
                            style={'padding-left': '1vw'},
                        ),
                    ]
                ),
                html.Div(dbc.Modal(), id='game-details-player-details-modal-div'),
            ],
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'flexDirection': 'column',
                'height': '100vh',
            },
        )
