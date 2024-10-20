from typing import Optional

import dash_bootstrap_components as dbc


class GamesDetailsCard:
    @staticmethod
    def build(
        title: str,
        content: list,
        height: Optional[str] = None,
        width: Optional[str] = None,
        max_width: Optional[str] = None,
    ) -> dbc.Card:
        details_card = dbc.Card(
            children=[
                dbc.CardHeader(title, style={'font-size': '2.5vh', 'padding': '1vh'}),
                dbc.CardFooter(
                    content,
                    style={
                        'height': '100%',
                        'background-color': '#303030',
                        'overflow': 'auto',
                        'padding-top': '2vh',
                    },
                ),
            ],
            style={
                'height': height,
                'width': width,
                'max-width': max_width,
            },
        )

        return details_card
