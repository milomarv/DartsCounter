import re
import datetime as dt
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger


class LoadReleaseNotes(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [
            Input('url', 'pathname'),
            Input('release-notes-content', 'style'),
        ]
        self.outputs = [
            Output('release-notes-content', 'children'),
            Output('release-notes-content', 'style'),
        ]
        self.states = []
        self.logger.info('Initialized Load Release Notes Callback')

    # TODO test this
    def callback(self, url: str, style: dict) -> object:
        if url == '/release-notes':
            self.logger.info('Loading Release Notes')
            with open('./RELEASENOTES.md', 'r', encoding='utf-8') as file:
                release_notes_content = file.read()

            sections = re.split(
                r'(^## [^\n]+)', release_notes_content, flags=re.MULTILINE
            )

            release_notes = {}
            for i in range(1, len(sections), 2):
                topic = sections[i].strip()
                content = sections[i + 1].strip()
                release_notes[topic] = content

            output_content = []
            for topic, content in release_notes.items():
                topic = topic[3:]
                version, date = topic.split(' - ')
                date = dt.datetime.strptime(date, '%Y-%m-%d').strftime('%d %B %Y')
                output_content.append(
                    dbc.Row(
                        children=[
                            dbc.Col(html.H3(version), width='auto'),
                            dbc.Col(
                                dbc.Badge(
                                    date, color='primary', style={'fontSize': '1rem'}
                                )
                            ),
                        ],
                        style={'alignItems': 'center'},
                    )
                )
                output_content.append(
                    dbc.Card(
                        dcc.Markdown(content),
                        style={'padding': '1rem'},
                        color='#444444',
                    )
                )
                output_content.append(html.Br())
            output_content.pop()

            del style['justifyContent']
            del style['text-align']

            return [output_content, style]

        raise PreventUpdate
