from dash import html


class PlaceholderText:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(text: str, identifier: str, height: str = '100%') -> html.Div:
        return html.Div(
            html.H3(text),
            id = identifier,
            style = {
                'height': height,
                'display': 'flex',
                'flex-wrap': 'wrap',
                'align-content': 'center',
                'justify-content': 'center',
                'text-align': 'center'
            }
        )
