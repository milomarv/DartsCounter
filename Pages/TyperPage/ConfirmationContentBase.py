from dash import html
import dash_bootstrap_components as dbc

class ConfirmationContentBase:
    def __init__(self):
        self.baseStyle = {
            'white-space': 'nowrap'
        }
        self.textBaseStyle = {
            'corlor': 'grey',
            'margin-left': '1vw',
            'margin-right': '1vw'
        }
        self.infoBaseStyle = {
            'fontWeight': 'bold'
        }
        self.textRowStyle = {
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'flexDirection': 'row',
            'white-space': 'nowrap'
        }