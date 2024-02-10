from dash import html
import dash_bootstrap_components as dbc

class FilterButton:
    def __init__(self):
        pass

    def Build(self, prettyName: str, id: str, active = False):
        if active:
            className = "btn btn-primary"
        else:
            className = "btn btn-secondary"
        return dbc.Button(
            prettyName,
            id = f"{id}-filter-button",
            className = className,
            style = {
                "width": "200px",
                "height": "50px",
                "fontSize": "20px"
            }
        )