import dash_bootstrap_components as dbc
from dash import html

from Models.Out import Out
from Models.TypeSetLeg import TypeSetLeg
from Pages.DatabasePage.ProgressBadge import ProgressBadge
from Pages.GamesDetailsPage.GameValue import GameValue
from Pages.GamesDetailsPage.ValueBadge import ValueBadge


class GameStatistics:
    def __init__(self) -> None:
        self.game_value = GameValue()
        self.progress_badge = ProgressBadge()
        self.value_badge = ValueBadge()

    def build(
        self,
        finished: str,
        points: int,
        out: Out,
        legs: int,
        total_legs: int,
        leg_mode: TypeSetLeg,
        sets: int,
        total_sets: int,
        set_mode: TypeSetLeg,
    ) -> html.Div:
        progress_badge = self.progress_badge.build(
            finished, additional_text_style={'fontSize': '2vh'}
        )

        statistics_div = html.Div(
            [
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                self.game_value.build(
                                    value_name='Progress', content=progress_badge
                                ),
                                self.game_value.build(
                                    value_name='Points',
                                    content=points,
                                ),
                                self.game_value.build(
                                    value_name='Checkout',
                                    content=self.value_badge.build(str(out)),
                                ),
                            ]
                        ),
                        dbc.Col(
                            children=[
                                self.game_value.build(
                                    value_name='Legs to Set Win', content=legs
                                ),
                                self.game_value.build(
                                    value_name='Total Legs played', content=total_legs
                                ),
                                self.game_value.build(
                                    value_name='Leg Mode',
                                    content=self.value_badge.build(str(leg_mode)),
                                ),
                            ]
                        ),
                        dbc.Col(
                            children=[
                                self.game_value.build(
                                    value_name='Sets to Game Win', content=sets
                                ),
                                self.game_value.build(
                                    value_name='Total Sets played', content=total_sets
                                ),
                                self.game_value.build(
                                    value_name='Set Mode',
                                    content=self.value_badge.build(str(set_mode)),
                                ),
                            ]
                        ),
                    ],
                    style={'width': '100%'},
                )
            ],
            style={'width': '100%', 'padding-left': '1vw'},
        )
        return statistics_div
