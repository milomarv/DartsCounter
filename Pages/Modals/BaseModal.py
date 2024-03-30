import dash_bootstrap_components as dbc


class BaseModal:
    def __init__(self, identifier: str, title: str, children: list, close_able: bool = True, size: str = 'lg',
                 is_open: bool = False):
        self.id = identifier
        self.title = title
        self.children = children
        self.closeAble = close_able
        self.size = size
        self.is_open = is_open

        self.topicTemplate = '{0}'
        self.idBodyTemplate = '{0}-modal-body'
        self.idTemplate = '{0}-modal'
        self.footer = None

    def build(self) -> dbc.Modal:
        return dbc.Modal(
            [
                dbc.ModalHeader(
                    self.topicTemplate.format(self.title),
                    style = {'font-size': '24px'},
                    close_button = self.closeAble
                ),
                dbc.ModalBody(
                    children = self.children,
                    id = self.idBodyTemplate.format(self.id),
                    style = {
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'left',
                    }
                ),
                self.footer
            ],
            id = self.idTemplate.format(self.id),
            is_open = self.is_open,
            centered = True,
            size = self.size,
            backdrop = 'static',
            keyboard = False
        )
