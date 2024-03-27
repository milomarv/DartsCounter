from Pages.Modals.BaseModal import BaseModal


class InfoModal(BaseModal):
    def __init__(self, identifier: str, title: str, children: list, close_able: bool = True):
        super().__init__(identifier, title, children, close_able)
        self.topicTemplate = 'ℹ️ Info: {0}'
        self.idBodyTemplate = '{0}-info-modal-body'
        self.idTemplate = '{0}-info-modal'
