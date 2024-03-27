from dash import html


class NotFoundPageLayout:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build() -> html.Div:
        return html.Div(
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'flexDirection': 'column',
                'height': '100vh'
            },
            children=[
                html.H1(html.Strong("404")),
                html.H3("Page not found!")
            ]
        )
