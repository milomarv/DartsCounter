from dash import html
import dash_bootstrap_components as dbc


def load_release_notes(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


class ReleaseNotesPageLayout:
    def __init__(self) -> None:
        self.release_notes_path = './RELEASENOTES.md'

    def build(self) -> html.Div:
        return html.Div(
            children=[
                html.H1('📜Release Notes'),
                dbc.Card(
                    html.H1('⌛ Loading...'),
                    id='release-notes-content',
                    style={
                        'display': 'flex',
                        'height': '75%',
                        'overflowY': 'scroll',
                        'padding': '2.5rem',
                        'justifyContent': 'center',
                        'width': '50%',
                        'text-align': 'center',
                    },
                ),
            ],
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'flexDirection': 'column',
                'height': '100vh',
            },
        )
