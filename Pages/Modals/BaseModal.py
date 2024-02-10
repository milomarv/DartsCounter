import dash_bootstrap_components as dbc

class BaseModal:
    def __init__(self, id :str, title: str, children: list, closeAble: bool = True, size: str = "lg"):
        self.id = id
        self.title = title
        self.children = children
        self.closeAble = closeAble
        self.size = size

        self.topicTemplate = "{0}"
        self.idBodyTemplate = "{0}-modal-body"
        self.idTemplate = "{0}-modal"
        self.footer = None

    def Build(self):
        return dbc.Modal(
            [
                dbc.ModalHeader(
                    self.topicTemplate.format(self.title),
                    style={'font-size': '24px'},
                    close_button = self.closeAble
                ),
                dbc.ModalBody(
                    children = self.children,
                    id = self.idBodyTemplate.format(self.id),
                    style = {
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "left",
                    }
                ),
                self.footer
            ],
            id = self.idTemplate.format(self.id),
            is_open = False,
            centered=True,
            size=self.size,
            backdrop="static",
            keyboard=False
        )