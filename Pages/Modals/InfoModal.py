from dash import html
import dash_bootstrap_components as dbc

from Pages.Modals.BaseModal import BaseModal

class InfoModal(BaseModal):
    def __init__(self, id :str, title: str, children: list, closeAble: bool = True):
        super().__init__(id, title, children, closeAble)
        self.topicTemplate = "ℹ️ Info: {0}"
        self.idBodyTemplate = "{0}-info-modal-body"
        self.idTemplate = "{0}-info-modal"