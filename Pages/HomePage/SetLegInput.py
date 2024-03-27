import dash_bootstrap_components as dbc
from dash import html

from Models.TypeSetLeg import BEST_OF, FIRST_TO


class SetLegInput:
    def __init__(self, pretty_text: str, id_text: str) -> None:
        self.prettyText = pretty_text
        self.idText = id_text

    def build(self) -> html.Div:
        return html.Div(
            children=[
                dbc.Label(f'Number of {self.prettyText}s:', html_for=f'number-of-{self.idText}s-input'),
                dbc.Input(type='number', id=f'number-of-{self.idText}s-input', min=1),
                html.Br(),
                dbc.Label(f'{self.prettyText} Mode:', html_for=f'{self.idText}-mode-select'),
                dbc.Select(
                    id=f'{self.idText}-mode-select',
                    options=[
                        {'label': 'First to', 'value': FIRST_TO},
                        {'label': 'Best of', 'value': BEST_OF}
                    ],
                    value=FIRST_TO
                )
            ]
        )
