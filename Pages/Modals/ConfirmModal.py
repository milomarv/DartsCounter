import dash_bootstrap_components as dbc
from dash import html

from Pages.Modals.BaseModal import BaseModal


class ConfirmModal(BaseModal):
    def __init__(
            self,
            identifier: str,
            title: str,
            children: list,
            close_able: bool = True,
            href: str = None,
            size: str = 'lg',
    ):
        super().__init__(identifier, title, children, close_able, size)
        self.children = children
        self.topicTemplate = '↩️ Confirm Action: {0}'
        self.idBodyTemplate = '{0}-confirm-modal-body'
        self.idTemplate = '{0}-confirm-modal'
        self.footer = html.Div(
            dbc.Button(
                html.B('Confirm', style={'font-size': '2.5vh'}),
                id=f'{identifier}-confirm-button',
                href=href,
                color='primary',
                className='mr-1',
                style={
                    'margin': '2vh',
                    'height': '7.5vh',
                    'width': '20vw',
                    'padding': '2vh'
                }
            ),
            style={
                'display': 'flex',
                'justifyContent': 'center'
            }
        )
