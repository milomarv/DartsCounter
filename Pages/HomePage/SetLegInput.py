from dash import html
import dash_bootstrap_components as dbc
from Models.TypeSetLeg import BEST_OF, FIRST_TO

class SetLegInput:
    def __init__(self, prettyText, idText):
        self.prettyText = prettyText
        self.idText = idText

    def Build(self):
        return html.Div(
            children = [
                dbc.Label(f"Number of {self.prettyText}s:", html_for=f"number-of-{self.idText}s-input"),
                dbc.Input(type="number", id=f"number-of-{self.idText}s-input", value=3, min=1),
                html.Br(),
                dbc.Label(f"{self.prettyText} Mode:", html_for=f"{self.idText}-mode-select"),
                dbc.Select(
                    id=f"{self.idText}-mode-select",
                    options=[
                        {"label": "First to", "value": FIRST_TO},
                        {"label": "Best of", "value": BEST_OF}
                    ],
                    value = FIRST_TO
                )
            ]
        )
