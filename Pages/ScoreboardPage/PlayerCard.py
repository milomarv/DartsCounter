import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from dash import html, dcc

from Pages.TyperPage.DartIcon import DartIcon


class PlayerCard:
    def __init__(self):
        self.textStyle = {
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'flexDirection': 'column'
        }

        self.polarVals = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
        self.polarTickVals = [f"Score {n}" for n in self.polarVals]
        self.polarTickText = [f"{n}" for n in self.polarVals]

        self.dartIcon = DartIcon(
            flexDirection="row",
            iconSize=0.5,
            paddingBottom="1.5vh"
        )

    def Build(
            self,
            active=False,
            name: str = "Name",
            pointsLeft: int = "N/A",
            avg: float = "N/A",
            thrownDarts: int = 0,
            setWins: int = 0,
            legWins: int = 0,
            single: int = 0,
            double: int = 0,
            triple: int = 0,
            miss: int = 0,
            singlePerc: int = 0,
            doublePerc: int = 0,
            triplePerc: int = 0,
            missPerc: int = 0,
            nHits: list = [],
            dartIcon1: DartIcon = None,
            dartIcon2: DartIcon = None,
            dartIcon3: DartIcon = None,
            totalScore: int = 0,
            checkoutRate: str = "N/A",
            checkoutCounter: str = "N/A"
    ):
        if active:
            cardHeaderColor = "#375a7f"
        else:
            cardHeaderColor = "#444444"

        if not dartIcon1:
            dartIcon1 = self.dartIcon.Build()
        if not dartIcon2:
            dartIcon2 = self.dartIcon.Build()
        if not dartIcon3:
            dartIcon3 = self.dartIcon.Build()

        return dbc.Card(
            children=[
                dbc.CardHeader(
                    html.Div(
                        name,
                        id="typer-player-name",
                        style={
                            **self.textStyle,
                            'height': '5vh',
                            'fontSize': '3vh',
                            'fontWeight': 'bold'
                        }
                    ),
                    style={
                        "backgroundColor": cardHeaderColor,
                    }
                ),
                dbc.CardBody(
                    children=[
                        html.Div(
                            html.H1(
                                pointsLeft,
                                id="typer-score",
                                style={
                                    **self.textStyle,
                                    'height': '8.5vh',
                                    'fontSize': '7.5vh',
                                    'fontWeight': 'bold'
                                }
                            )
                        ),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        html.H5(
                                            "Average:",
                                            style={
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            avg,
                                            style={
                                                **self.textStyle,
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children=[
                                        html.H5(
                                            "Darts:",
                                            style={
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            thrownDarts,
                                            style={
                                                **self.textStyle,
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children=[
                                        html.H5(
                                            "Checkouts:",
                                            style={
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            checkoutCounter,
                                            style={
                                                **self.textStyle,
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        html.H5(
                                            "Set Wins:",
                                            style={
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            setWins,
                                            style={
                                                **self.textStyle,
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children=[
                                        html.H5(
                                            "Leg Wins:",
                                            style={
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            legWins,
                                            style={
                                                **self.textStyle,
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    children=[
                                        html.H5(
                                            "Checkout Rate:",
                                            style={
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            checkoutRate,
                                            style={
                                                **self.textStyle,
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ]
                                )
                            ]
                        ),
                        dcc.Graph(
                            figure={
                                "data": [
                                    {
                                        "x": ["Single", "Double", "Triple", "Miss"],
                                        "y": [singlePerc, doublePerc, triplePerc, missPerc],
                                        "type": "bar",
                                        "marker": {
                                            "color": "#375a7f"
                                        },
                                        "text": [
                                            f"{round(perc * 100, 1)}%<br>({darts})" for darts, perc in
                                            zip([single, double, triple, miss],
                                                [singlePerc, doublePerc, triplePerc, missPerc])
                                        ],
                                        "textposition": "auto",
                                        "textfont": {
                                            "color": "white",
                                            "size": 15
                                        }
                                    }
                                ],
                                "layout": {
                                    "paper_bgcolor": "#303030",
                                    "plot_bgcolor": "#303030",
                                    "font": {
                                        "color": "white"
                                    },
                                    "margin": {"t": 30, "l": 30, "r": 30, "b": 50},
                                    "yaxis": {
                                        "type": "log",  # TODO lines in background are ugly
                                        "tickformat": ".0%",
                                        "gridcolor": "#444444",
                                        "range": [-1.5, 0],  # TODO bars are missing when to less data
                                        "tickfont": {
                                            "color": "#303030"
                                        }
                                    },
                                    "xaxis": {
                                        "tickfont": {"size": 20}
                                    }
                                }
                            },
                            style={
                                "height": "25vh"
                            }
                        ),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    dcc.Graph(  # TODO numbers are cut when to small Player Cards Hello World
                                        figure={
                                            'data': [
                                                go.Scatterpolar(
                                                    r=np.log(np.array(nHits) + 0.9),
                                                    theta=self.polarTickVals,
                                                    fill='toself',
                                                    name='Example Data',
                                                    text=[f"{score}:<br>{nHit} hits" for score, nHit in
                                                          zip(self.polarTickVals, nHits)],
                                                    hoverinfo="text",
                                                    mode="markers+lines",
                                                )
                                            ],
                                            'layout': go.Layout(
                                                polar=dict(
                                                    radialaxis_angle=90,
                                                    radialaxis=dict(
                                                        showticklabels=False,
                                                        showline=False,
                                                        gridcolor="#444444",
                                                    ),
                                                    angularaxis=dict(
                                                        tickvals=self.polarTickVals,
                                                        ticktext=self.polarTickText,
                                                        tickfont={"size": 15}
                                                    ),
                                                    bgcolor="#303030",
                                                ),
                                                showlegend=False,
                                                margin={"t": 30, "b": 30, "l": 0, "r": 0},
                                                paper_bgcolor="#303030",
                                                font={
                                                    "color": "white"
                                                }
                                            )
                                        },
                                        style={
                                            'backgroundColor': '#303030',
                                            'height': '25vh',
                                            'margin-bottom': '1vh'
                                        }
                                    )
                                ),
                                dbc.Col(
                                    children=[
                                        dartIcon1,
                                        dartIcon2,
                                        dartIcon3,
                                        html.Div(
                                            children=[
                                                html.H5(
                                                    "Total:",
                                                    style={
                                                        **self.textStyle,
                                                        'color': 'grey',
                                                        'width': f'{7.5 * 0.5}vh',
                                                        "margin-left": "1rem",
                                                        "margin-right": "1rem"
                                                    }
                                                ),
                                                dbc.Badge(
                                                    totalScore,
                                                    style={
                                                        "width": "5rem",
                                                        "fontSize": "1.5rem",
                                                        "fontWeight": "bold"
                                                    },
                                                    color="primary"
                                                ),
                                            ],
                                            style={
                                                'display': 'flex',
                                                'justifyContent': 'center',
                                                'alignItems': 'center',
                                                'flexDirection': "row"
                                            }
                                        )
                                    ],
                                    width=5
                                )
                            ],
                            style={
                                "margin-right": "1.5vw",
                                "margin-left": "1.5vw",
                                "display": "flex",
                                "flex-wrap": "nowrap",
                            }
                        )

                    ]
                )
            ],
            style={
                "minWidth": "35rem",
                "maxWidth": "35rem",
                "margin": "10px"
            },
            className="mx-auto"
        )
