import dash_bootstrap_components as dbc
from dash import dcc, html

from Pages.MenuCard import MenuCard
from Pages.Modals.ConfirmModal import ConfirmModal


# TODO if no games existing show something like 'No games found' instead of nothing
class DatabasePageLayout:
    def __init__(self) -> None:
        self.card = MenuCard()

        self.confirm_delete_game_modal = ConfirmModal(
            'delete-game',
            title='Delete Game?',
            children=[],
            confirm_button_color='danger',
        )
        self.confirm_continue_game_modal = ConfirmModal(
            'continue-game', title='Continue Game?', children=[]
        )

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
                html.H1('💾 Database'),
                html.Br(),
                html.Div(
                    dbc.Stack(
                        children=[
                            self.card.build(
                                title='🎯 Games Database',
                                identifier='games-db-list-frame',
                                children=[
                                    html.Div(
                                        html.H3('⌛ Loading...'),
                                        id='games-db-list',
                                        style={
                                            'height': '30rem',
                                            'display': 'flex',
                                            'flex-wrap': 'wrap',
                                            'align-content': 'center',
                                            'justify-content': 'center',
                                        },
                                    )
                                ],
                                max_height_rem=40,
                            ),
                            self.card.build(
                                title='🧑🏽 Players Database',
                                children=[
                                    html.Div(
                                        # TODO Coming Soon
                                        html.H3('⌛ Coming Soon!'),
                                        style={
                                            'height': '30rem',
                                            'display': 'flex',
                                            'flex-wrap': 'wrap',
                                            'align-content': 'center',
                                            'justify-content': 'center',
                                        },
                                    )
                                ],
                                max_height_rem=40,
                            ),
                        ],
                        direction='horizontal',
                        gap=5,
                    )
                ),
                self.confirm_delete_game_modal.build(),
                self.confirm_continue_game_modal.build(),
                dcc.Store(id='game-deletion-key'),
                dcc.Store(id='game-continue-key'),
            ],
        )
