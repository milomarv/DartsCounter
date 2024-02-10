from dash import html
import dash_bootstrap_components as dbc

class PlayerInput:
    def __init__(self):
        self.index = 0

    def Build(self):
        self.index += 1
        return dbc.InputGroup(
            children = [
                dbc.InputGroupText(f"Player {self.index}"),
                dbc.Input(
                    id = {"type": "player-input", "index": self.index}
                ),

            ],
            style = {
                "margin-bottom": "15px",
            }
        )