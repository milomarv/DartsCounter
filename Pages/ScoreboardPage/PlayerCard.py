import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from dash import dcc, html

from Pages.TyperPage.DartIcon import DartIcon


class PlayerCard:
    def __init__(self) -> None:
        self.textStyle = {
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'flexDirection': 'column'
        }

        self.polarVals = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
        self.polarTickVals = [f'Score {n}' for n in self.polarVals]
        self.polarTickText = [f'{n}' for n in self.polarVals]

        self.logarithmic_level = -1.5

        self.dartIcon = DartIcon(
            flex_direction = 'row',
            icon_size = 0.5,
            padding_bottom = '1.5vh'
        )

    def build(
        self,
        active = False,
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
        n_hits = None,
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
            children = [
                dbc.CardHeader(
                    html.Div(
                        name,
                        id = 'typer-player-name',
                        style = {
                            **self.textStyle,
                            'height': '5vh',
                            'fontSize': '3vh',
                            'fontWeight': 'bold'
                        }
                    ),
                    style = {
                        'backgroundColor': card_header_color,
                    }
                ),
                dbc.CardBody(
                    children = [
                        html.Div(
                            html.H1(
                                points_left,
                                id = 'typer-score',
                                style = {
                                    **self.textStyle,
                                    'height': '8.5vh',
                                    'fontSize': '7.5vh',
                                    'fontWeight': 'bold'
                                }
                            )
                        ),
                        dbc.Row(
                            children = [
                                dbc.Col(
                                    children = [
                                        html.H5(
                                            'Average:',
                                            style = {
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            avg,
                                            style = {
                                                **self.textStyle,
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        html.H5(
                                            'Darts:',
                                            style = {
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            thrown_darts,
                                            style = {
                                                **self.textStyle,
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        html.H5(
                                            'Checkouts:',
                                            style = {
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            checkout_counter,
                                            style = {
                                                **self.textStyle,
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            children = [
                                dbc.Col(
                                    children = [
                                        html.H5(
                                            'Set Wins:',
                                            style = {
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            set_wins,
                                            style = {
                                                **self.textStyle,
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        html.H5(
                                            'Leg Wins:',
                                            style = {
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            leg_wins,
                                            style = {
                                                **self.textStyle,
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children = [
                                        html.H5(
                                            'Checkout Rate:',
                                            style = {
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            checkout_rate,
                                            style = {
                                                **self.textStyle,
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ]
                                )
                            ]
                        ),
                        dcc.Graph(
                            figure = {
                                'data': [
                                    {
                                        'x': ['Single', 'Double', 'Triple', 'Miss'],
                                        'y': [
                                            single_perc + 10 ** self.logarithmic_level,
                                            double_perc + 10 ** self.logarithmic_level,
                                            triple_perc + 10 ** self.logarithmic_level,
                                            miss_perc + 10 ** self.logarithmic_level
                                        ],
                                        'type': 'bar',
                                        'marker': {
                                            'color': '#375a7f'
                                        },
                                        'text': [
                                            f'{round(perc * 100, 1)}%<br>({darts})' for darts, perc in
                                            zip([single, double, triple, miss],
                                                [single_perc, double_perc, triple_perc, miss_perc])
                                        ],
                                        'textposition': 'auto',
                                        'textfont': {
                                            'color': 'white',
                                            'size': 15
                                        }
                                    }
                                ],
                                'layout': {
                                    'paper_bgcolor': '#303030',
                                    'plot_bgcolor': '#393939',
                                    'font': {
                                        'color': 'white'
                                    },
                                    'margin': {'t': 30, 'l': 30, 'r': 30, 'b': 50},
                                    'yaxis': {
                                        'type': 'log',
                                        'tickformat': '.0%',
                                        'gridcolor': '#393939',
                                        'range': [self.logarithmic_level, 0.1],
                                        'tickfont': {
                                            'color': '#303030'
                                        }
                                    },
                                    'xaxis': {
                                        'tickfont': {'size': 20}
                                    }
                                }
                            },
                            style = {
                                'height': '22.5vh'
                            }
                        ),
                        dbc.Row(
                            children = [
                                dbc.Col(
                                    dcc.Graph(
                                        figure = {
                                            'data': [
                                                go.Scatterpolar(
                                                    r = np.log(np.array(n_hits) + 0.9),
                                                    theta = self.polarTickVals,
                                                    fill = 'toself',
                                                    name = 'Example Data',
                                                    text = [f'{score}:<br>{nHit} hits' for score, nHit in
                                                            zip(self.polarTickVals, n_hits)],
                                                    hoverinfo = 'text',
                                                    mode = 'markers+lines',
                                                )
                                            ],
                                            'layout': go.Layout(
                                                polar = dict(
                                                    radialaxis_angle = 90,
                                                    radialaxis = dict(
                                                        showticklabels = False,
                                                        showline = False,
                                                        gridcolor = '#444444',
                                                    ),
                                                    angularaxis = dict(
                                                        tickvals = self.polarTickVals,
                                                        ticktext = self.polarTickText,
                                                        tickfont = {'size': 15}
                                                    ),
                                                    bgcolor = '#303030',
                                                ),
                                                showlegend = False,
                                                margin = {'t': 30, 'b': 30, 'l': 30, 'r': 30},
                                                paper_bgcolor = '#303030',
                                                font = {
                                                    'color': 'white'
                                                }
                                            )
                                        },
                                        style = {
                                            'backgroundColor': '#303030',
                                            'height': '25vh',
                                            'margin-bottom': '1vh'
                                        }
                                    )
                                ),
                                dbc.Col(
                                    children = [
                                        dart_icon1,
                                        dart_icon2,
                                        dart_icon3,
                                        html.Div(
                                            children = [
                                                html.H5(
                                                    'Total:',
                                                    style = {
                                                        **self.textStyle,
                                                        'color': 'grey',
                                                        'width': f'{7.5 * 0.5}vh',
                                                        'margin-left': '1rem',
                                                        'margin-right': '1rem'
                                                    }
                                                ),
                                                dbc.Badge(
                                                    total_score,
                                                    style = {
                                                        'width': '5rem',
                                                        'fontSize': '1.5rem',
                                                        'fontWeight': 'bold'
                                                    },
                                                    color = 'primary'
                                                ),
                                            ],
                                            style = {
                                                'display': 'flex',
                                                'justifyContent': 'center',
                                                'alignItems': 'center',
                                                'flexDirection': 'row'
                                            }
                                        )
                                    ],
                                    width = 5
                                )
                            ],
                            style = {
                                'margin-right': '1.5vw',
                                'margin-left': '1.5vw',
                                'display': 'flex',
                                'flex-wrap': 'nowrap',
                            }
                        )

                    ]
                )
            ],
            style = {
                'minWidth': '35rem',
                'maxWidth': '35rem',
                'margin': '10px'
            },
            className = 'mx-auto'
        )
