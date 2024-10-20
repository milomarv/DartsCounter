from typing import Optional
import dash_bootstrap_components as dbc
from dash import html

from Pages.PlayerStatsContentDiv import PlayerStatsContentDiv
from Pages.TyperPage.DartIcon import DartIcon


class PlayerCard:
    def __init__(self) -> None:
        self.player_stats = PlayerStatsContentDiv()

        self.textStyle = {
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'flexDirection': 'column',
        }
        self.player_stats.textStyle = self.textStyle

        self.dartIcon = DartIcon(
            flex_direction='row', icon_size=0.5, padding_bottom='1.5vh'
        )

    def build(
        self,
        active: bool = False,
        name: str = 'Name',
        points_left: int = 'N/A',
        avg: float = 'N/A',
        thrown_darts: int = 0,
        set_wins: int = 0,
        leg_wins: int = 0,
        single: int = 0,
        double: int = 0,
        triple: int = 0,
        miss: int = 0,
        single_perc: int = 0,
        double_perc: int = 0,
        triple_perc: int = 0,
        miss_perc: int = 0,
        n_hits: Optional[list] = None,
        total_score: int = 0,
        checkout_rate: str = 'N/A',
        checkout_counter: str = 'N/A',
        dart_icon1: DartIcon = None,
        dart_icon2: DartIcon = None,
        dart_icon3: DartIcon = None,
    ) -> dbc.Card:
        if n_hits is None:
            n_hits = []
        if active:
            card_header_color = '#375a7f'
        else:
            card_header_color = '#444444'

        if not dart_icon1:
            dart_icon1 = self.dartIcon.build()
        if not dart_icon2:
            dart_icon2 = self.dartIcon.build()
        if not dart_icon3:
            dart_icon3 = self.dartIcon.build()

        return dbc.Card(
            children=[
                dbc.CardHeader(
                    html.Div(
                        name,
                        id='typer-player-name',
                        style={
                            **self.textStyle,
                            'height': '5vh',
                            'fontSize': '3vh',
                            'fontWeight': 'bold',
                        },
                    ),
                    style={
                        'backgroundColor': card_header_color,
                    },
                ),
                dbc.CardBody(
                    children=[
                        self.player_stats.build(
                            points_left=points_left,
                            avg=avg,
                            thrown_darts=thrown_darts,
                            set_wins=set_wins,
                            leg_wins=leg_wins,
                            single=single,
                            double=double,
                            triple=triple,
                            miss=miss,
                            single_perc=single_perc,
                            double_perc=double_perc,
                            triple_perc=triple_perc,
                            miss_perc=miss_perc,
                            n_hits=n_hits,
                            total_score=total_score,
                            checkout_rate=checkout_rate,
                            checkout_counter=checkout_counter,
                            dart_icon1=dart_icon1,
                            dart_icon2=dart_icon2,
                            dart_icon3=dart_icon3,
                        )
                    ]
                ),
            ],
            style={'minWidth': '35rem', 'maxWidth': '35rem', 'margin': '10px'},
            className='mx-auto',
        )
