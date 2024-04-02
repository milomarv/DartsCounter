from typing import Optional

import dash_bootstrap_components as dbc


class GamesDetailsCard:
    @staticmethod
    def build(title: str, content: list, height: Optional[str] = None) -> dbc.Card:
        details_card = dbc.Card(
            children = [
                dbc.CardHeader(
                    title,
                    style = {
                        'font-size': '1.5rem'
                    }
                ),
                dbc.CardFooter(
                    content,
                    style = {
                        'height': '100%',
                        'background-color': '#303030'
                    }
                )
            ],
            style = {
                'height': height
            }
        )

        return details_card
