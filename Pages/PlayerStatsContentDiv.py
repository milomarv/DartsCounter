from typing import Optional
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np

from Pages.GamesDetailsPage.GameValue import GameValue
from Pages.TyperPage.DartIcon import DartIcon


class PlayerStatsContentDiv:
    def __init__(self) -> None:
        self.textStyle = {
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'flexDirection': 'column',
        }

        self.game_value = GameValue()

        self.polarVals = [
            6,
            13,
            4,
            18,
            1,
            20,
            5,
            12,
            9,
            14,
            11,
            8,
            16,
            7,
            19,
            3,
            17,
            2,
            15,
            10,
        ]
        self.polarTickVals = [f'Score {n}' for n in self.polarVals]
        self.polarTickText = [f'{n}' for n in self.polarVals]

        self.logarithmic_level = -1.5

    def build(
        self,
        avg: float | str = 'N/A',
        thrown_darts: int = 0,
        checkout_counter: str = 'N/A',
        set_wins: int = 0,
        leg_wins: int = 0,
        checkout_rate: str = 'N/A',
        single: int = 0,
        double: int = 0,
        triple: int = 0,
        miss: int = 0,
        single_perc: float = 0,
        double_perc: float = 0,
        triple_perc: float = 0,
        miss_perc: float = 0,
        show_points_left: Optional[bool] = True,
        points_left: Optional[int | str] = 'N/A',
        n_hits: Optional[list] = [],
        dart_icon1: Optional[DartIcon] = None,
        dart_icon2: Optional[DartIcon] = None,
        dart_icon3: Optional[DartIcon] = None,
        total_score: Optional[int] = None,
    ) -> html.Div:
        if not show_points_left:
            points_left_style = {'display': 'none'}
        else:
            points_left_style = {}

        if isinstance(total_score, type(None)):
            dart_scores_div_style = {'display': 'none'}
            polar_graph_width = 'auto'
        else:
            dart_scores_div_style = {}
            polar_graph_width = 7

        return html.Div(
            children=[
                html.Div(
                    html.H1(
                        points_left,
                        id='typer-score',
                        style={
                            **self.textStyle,
                            'height': '8.5vh',
                            'fontSize': '7.5vh',
                            'fontWeight': 'bold',
                        },
                    ),
                    style=points_left_style,
                ),
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[self.game_value.build('Average', avg)],
                        ),
                        dbc.Col(
                            children=[self.game_value.build('Darts', thrown_darts)],
                        ),
                        dbc.Col(
                            children=[
                                self.game_value.build('Checkouts', checkout_counter),
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                self.game_value.build('Set Wins', set_wins),
                            ]
                        ),
                        dbc.Col(
                            children=[
                                self.game_value.build('Leg Wins', leg_wins),
                            ]
                        ),
                        dbc.Col(
                            children=[
                                self.game_value.build('Checkout Rate', checkout_rate),
                            ]
                        ),
                    ]
                ),
                dcc.Graph(
                    figure={
                        'data': [
                            {
                                'x': ['Single', 'Double', 'Triple', 'Miss'],
                                'y': [
                                    single_perc + 10**self.logarithmic_level,
                                    double_perc + 10**self.logarithmic_level,
                                    triple_perc + 10**self.logarithmic_level,
                                    miss_perc + 10**self.logarithmic_level,
                                ],
                                'type': 'bar',
                                'marker': {'color': '#375a7f'},
                                'text': [
                                    f'{round(perc * 100, 1)}%<br>({darts})'
                                    for darts, perc in zip(
                                        [single, double, triple, miss],
                                        [
                                            single_perc,
                                            double_perc,
                                            triple_perc,
                                            miss_perc,
                                        ],
                                    )
                                ],
                                'textposition': 'auto',
                                'textfont': {'color': 'white', 'size': 15},
                            }
                        ],
                        'layout': {
                            'paper_bgcolor': '#303030',
                            'plot_bgcolor': '#393939',
                            'font': {'color': 'white'},
                            'margin': {'t': 30, 'l': 30, 'r': 30, 'b': 50},
                            'yaxis': {
                                'type': 'log',
                                'tickformat': '.0%',
                                'gridcolor': '#393939',
                                'range': [self.logarithmic_level, 0.1],
                                'tickfont': {'color': '#303030'},
                            },
                            'xaxis': {'tickfont': {'size': 20}},
                        },
                    },
                    style={'height': '22.5vh'},
                ),
                dbc.Row(
                    children=[
                        dbc.Col(
                            dcc.Graph(
                                figure={
                                    'data': [
                                        go.Scatterpolar(
                                            r=np.log(np.array(n_hits) + 0.9),
                                            theta=self.polarTickVals,
                                            fill='toself',
                                            name='Example Data',
                                            text=[
                                                f'{score}:<br>{nHit} hits'
                                                for score, nHit in zip(
                                                    self.polarTickVals, n_hits
                                                )
                                            ],
                                            hoverinfo='text',
                                            mode='markers+lines',
                                        )
                                    ],
                                    'layout': go.Layout(
                                        polar=dict(
                                            radialaxis_angle=90,
                                            radialaxis=dict(
                                                showticklabels=False,
                                                showline=False,
                                                gridcolor='#444444',
                                            ),
                                            angularaxis=dict(
                                                tickvals=self.polarTickVals,
                                                ticktext=self.polarTickText,
                                                tickfont={'size': 15},
                                            ),
                                            bgcolor='#303030',
                                        ),
                                        showlegend=False,
                                        margin={
                                            't': 30,
                                            'b': 30,
                                            'l': 30,
                                            'r': 30,
                                        },
                                        paper_bgcolor='#303030',
                                        font={'color': 'white'},
                                    ),
                                },
                                style={
                                    'backgroundColor': '#303030',
                                    'height': '25vh',
                                    'margin-bottom': '1vh',
                                },
                            ),
                            width=polar_graph_width,
                        ),
                        dbc.Col(
                            children=[
                                dart_icon1,
                                dart_icon2,
                                dart_icon3,
                                html.Div(
                                    children=[
                                        html.H5(
                                            'Total:',
                                            style={
                                                **self.textStyle,
                                                'color': 'grey',
                                                'width': f'{7.5 * 0.5}vh',
                                                'margin-left': '1rem',
                                                'margin-right': '1rem',
                                            },
                                        ),
                                        dbc.Badge(
                                            total_score,
                                            style={
                                                'width': '5rem',
                                                'fontSize': '1.5rem',
                                                'fontWeight': 'bold',
                                            },
                                            color='primary',
                                        ),
                                    ],
                                    style={
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center',
                                        'flexDirection': 'row',
                                    },
                                ),
                            ],
                            width=5,
                            style=dart_scores_div_style,
                        ),
                    ],
                    style={
                        'margin-right': '1.5vw',
                        'margin-left': '1.5vw',
                        'display': 'flex',
                        'flex-wrap': 'nowrap',
                    },
                ),
            ]
        )
