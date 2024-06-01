from typing import Optional

import dash_bootstrap_components as dbc
from dash import html

from Pages.DatabasePage.GameValue import GameValue
from Pages.DatabasePage.PlayerBadge import PlayerBadge
from Pages.DatabasePage.ProgressBadge import ProgressBadge


# TODO add more Setting of Game
class GameEntry:
    def __init__(self) -> None:
        self.player_badge = PlayerBadge()
        self.game_entry_value = GameValue()
        self.progress_badge = ProgressBadge()

        self.initial_key_width = 2.5

    def build(self,
              index: str,
              title: str,
              finished: str = 'not_finished',
              winner: Optional[str] = None,
              sets: int = 0,
              legs: int = 0,
              players: Optional[list[str]] = None
              ) -> dbc.Card:
        if players is None:
            players = []

        continue_button_style = {'display': 'none'}
        delete_button_style = {}
        if finished == 'in_progress':
            delete_button_style = {'display': 'none'}
        else:
            continue_button_style = {}

        finished_badge = self.progress_badge.build(finished)

        if winner:
            winner_badge_text = winner
            winner_badge_color = 'primary'
        else:
            winner_badge_text = 'N/A'
            winner_badge_color = 'dark'
        winner_badge = dbc.Badge(
            winner_badge_text,
            color = winner_badge_color,
            style = {'font-size': '1rem'}
        )

        player_badges = [self.player_badge.build(p) for p in players]

        return dbc.Card(
            children = [
                dbc.CardHeader(
                    html.B(title, style = {'font-size': '20px'}),
                    style = {'background-color': '#375a7f'}
                ),
                dbc.CardFooter(
                    children = [
                        dbc.Row(
                            children = [
                                self.game_entry_value.build(
                                    value_name = 'Progress',
                                    content = finished_badge
                                ),
                                self.game_entry_value.build(
                                    value_name = 'Winner',
                                    content = winner_badge
                                ),
                                self.game_entry_value.build(
                                    value_name = 'Sets',
                                    content = sets
                                ),
                                self.game_entry_value.build(
                                    value_name = 'Legs',
                                    content = legs
                                ),
                                html.Div()
                            ]
                        ),
                        self.game_entry_value.build(
                            value_name = 'Players',
                            content = dbc.Row(
                                children = player_badges,
                                justify = 'start',
                                className = 'g-0',
                            )
                        ),
                        dbc.Stack(
                            children = [
                                dbc.Button(
                                    '🔎 See Details',
                                    color = 'primary',
                                    id = {'type': 'game-entry-details-button', 'index': index},
                                    href = f'database/game-details/{index}'
                                ),
                                dbc.Button(
                                    '↪️ Continue',
                                    color = 'primary',
                                    id = {'type': 'game-entry-continue-button', 'index': index},
                                    style = continue_button_style
                                ),
                                dbc.Button(
                                    '🗑️ Delete',
                                    color = 'danger',
                                    id = {'type': 'game-entry-delete-button', 'index': index},
                                    style = delete_button_style
                                )
                            ],
                            direction = 'horizontal',
                            gap = 3
                        )
                    ],
                    style = {'background-color': '#444444'}
                ),
            ],
            style = {
                'padding-bottom': '1rem',
                'border': '0'
            }
        )
