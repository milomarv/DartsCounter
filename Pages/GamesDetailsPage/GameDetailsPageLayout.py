from dash import html

from Pages.DatabasePage.DatabaseCallbacksOperations import DatabaseCallbacksOperations


class GamesDetailsPageLayout:
    def __init__(self) -> None:
        self.operations = DatabaseCallbacksOperations()

    def build(self, pathname: str) -> html.Div:
        game_key = pathname.split('/')[-1]
        pretty_game_ts = self.operations.format_game_ts_pretty(game_key)

        return html.Div(
            html.Div(
                children = [
                    'Details fo Game:',
                    html.Br(),
                    html.B(pretty_game_ts),
                    html.Br(),
                    html.Br(),
                    '⌛ Coming soon! ⌛'
                ],
                style = {
                    'text-align': 'center',
                    'font-size': '2rem'
                }
            ),
            style = {
                'width': '100%',
                'height': '100vh',
                'display': 'flex',
                'justify-content': 'center',
                'flex-wrap': 'wrap',
                'align-content': 'center'
            }
        )
