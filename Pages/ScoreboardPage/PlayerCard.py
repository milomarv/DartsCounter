from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

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

    def Build(
        self, 
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
        nHits: list = []
    ):
        return dbc.Card(
            children = [
                dbc.CardHeader(
                    html.H1(
                        name,
                        id = "typer-player-name",
                        style={
                            **self.textStyle,
                            'height': '5vh',
                            'fontSize': '3vh',
                            'fontWeight': 'bold'
                        }
                    )
                ),
                dbc.CardBody(
                    children = [
                        html.Div(
                            html.H1(
                                pointsLeft,
                                id = "typer-score",
                                style={
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
                                            "Average:",
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
                                            "Darts:",
                                            style = {
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            thrownDarts,
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
                                            "Set Wins:",
                                            style = {
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            setWins,
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
                                            "Leg Wins:",
                                            style = {
                                                **self.textStyle,
                                                'color': 'grey'
                                            }
                                        ),
                                        html.H4(
                                            legWins,
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
                                "data": [
                                    {
                                        "x": ["Single", "Double", "Triple", "Miss"],
                                        "y": [singlePerc, doublePerc, triplePerc, missPerc],
                                        "type": "bar",
                                        "marker": {
                                            "color": "#375a7f"
                                        },
                                        "text": [
                                            f"{round(perc*100, 1)}%<br>({darts})" for darts, perc in 
                                            zip([single, double, triple, miss],[singlePerc, doublePerc, triplePerc, missPerc])
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
                                        "tickformat": ".0%",
                                        "gridcolor": "#444444",
                                        "tickfont": {
                                            "color": "#303030"
                                        }
                                    },
                                    "xaxis": {
                                        "tickfont": {"size": 20}
                                    }
                                }
                            },
                            style = {
                                "height": "25vh"
                            }
                        ),
                        dcc.Graph(
                            figure={
                                'data': [
                                    go.Scatterpolar(
                                        r=nHits,
                                        theta = self.polarTickVals,
                                        fill='toself',
                                        name='Example Data',
                                        text = [f"{score}:<br>{nHit} hits" for score, nHit in zip(self.polarTickVals, nHits)],
                                        hoverinfo = "text",
                                        mode = "markers+lines",
                                    )
                                ],
                                'layout': go.Layout(
                                    polar = dict(
                                        radialaxis_angle = 90,
                                        radialaxis = dict(
                                            showticklabels = False,
                                            showline = False,
                                            gridcolor = "#444444",
                                        ),
                                        angularaxis = dict(
                                            tickvals = self.polarTickVals,
                                            ticktext = self.polarTickText,
                                            tickfont = {"size": 15}
                                        ),
                                        bgcolor = "#303030",
                                    ),
                                    showlegend=False,
                                    margin={"t": 30, "b": 30},
                                    paper_bgcolor="#303030",
                                    font = {
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
                    ]
                )
            ],
            style = {
                "minWidth": "30rem",
                "margin": "10px"
            },
            className="mx-auto"
        )