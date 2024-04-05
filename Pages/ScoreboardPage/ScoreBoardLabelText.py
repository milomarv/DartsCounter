from dash import html


class ScoreBoardLabelText:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(text: str) -> html.Div:
        return html.Div(
            text,
            style = {
                'font-size': '2rem',
                'font-weight': 'bold',
                'padding-left': '2rem'
            }
        )
