from dash import html
import dash_bootstrap_components as dbc

class Card:
    def __init__(self):
        pass

    def Build(self, title: str, children: list):
        return dbc.Card(
            dbc.CardBody(
                children = [
                    html.H4(title, className="card-title"),
                    html.Br(),
                    html.Div(
                        html.Div(children = children),
                        style={
                            "maxHeight": "22.5rem", 
                            "overflowY": "auto", 
                            "overflowX": "hidden"
                        }
                    )
                ]
            ),
            style = {
                "width": "30rem",
                "padding": "15px",
                "height": "30rem"
            }
        )