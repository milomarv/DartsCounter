import dash_bootstrap_components as dbc
from dash import html

from Pages.GamesDetailsPage.GameDetailsCard import GamesDetailsCard
from Pages.GamesDetailsPage.PlaceholderText import PlaceholderText


class GamesDetailsPageLayout:
    def __init__(self) -> None:
        self.details_card = GamesDetailsCard()
        self.placeholder_text = PlaceholderText()

    def build(self) -> html.Div:
        return html.Div(
            dbc.Row(
                children = [
                    dbc.Col(
                        children = [
                            dbc.Card(
                                children = [
                                    'Game Details'
                                ],
                                id = 'game-details-title',
                                color = 'primary',
                                style = {
                                    'padding': '1.5vh',
                                    'height': '8.5vh',
                                    'font-size': '3.5vh',
                                    'display': 'flex',
                                    'flex-direction': 'row'
                                }
                            ),
                            html.Div(style = {'height': '2.5vh'}),
                            self.details_card.build(
                                title = 'Set and Leg Wins',
                                content = [
                                    self.placeholder_text.build('⌛ Loading...', 'game-details-graph-div',
                                                                height = '36vh')
                                ],
                                height = '44vh'
                            ),
                            html.Div(style = {'height': '2.5vh'}),
                            # TODO make content scrollable
                            dbc.Row(
                                children = [
                                    dbc.Col(
                                        self.details_card.build(
                                            title = 'Statistics',
                                            content = [
                                                self.placeholder_text.build('⌛ Loading...',
                                                                            'game-details-statistics-div')
                                            ],
                                            height = '30vh'
                                        )
                                    ),
                                    dbc.Col(
                                        self.details_card.build(
                                            title = 'Operations',
                                            content = [
                                                self.placeholder_text.build('⌛ Coming soon!',
                                                                            'game-details-operations-div')
                                            ],
                                            height = '30vh'
                                        ),
                                        width = 3
                                    )
                                ]
                            )
                        ],
                        width = 6
                    ),
                    dbc.Col(
                        children = self.details_card.build(
                            title = 'Set Details',
                            content = [
                                self.placeholder_text.build('⌛ Coming soon!', 'game-details-set-leg-throw-details')
                            ],
                            height = '87.25vh'
                        )
                    ),
                    dbc.Col(
                        children = self.details_card.build(
                            title = 'Player Details',
                            content = [
                                self.placeholder_text.build('⌛ Coming soon!', 'game-details-player-details')
                            ],
                            height = '87.25vh'
                        )
                    )
                ]
            ),
            style = {
                'width': '95vw',
                'margin': '3.5rem'
            }
        )
