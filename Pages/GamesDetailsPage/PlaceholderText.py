from dash import html


class PlaceholderText:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(text: str, identifier: str, height: str = '100%') -> html.Div:
        return html.Div(
            text,
            id=identifier,
            style={
                'height': height,
                'display': 'flex',
                'flex-wrap': 'nowrap',
                'align-content': 'center',
                'justify-content': 'center',
                'text-align': 'center',
                'flex-direction': 'column',
                'font-size': '3vh',
            },
        )
