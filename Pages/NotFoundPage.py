from dash import html

class NotFoundPageLayout:
    def __init__(self):
        pass

    def Build(self):
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
