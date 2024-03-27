from Pages.Modals.BaseModal import BaseModal


class ErrorModal(BaseModal):
    def __init__(self, identifier: str, title: str, children: list, close_able: bool = True):
        super().__init__(identifier, title, children, close_able)
        self.topicTemplate = '⚠️ ERROR: {0}'
        self.idBodyTemplate = '{0}-error-modal-body'
        self.idTemplate = '{0}-error-modal'
