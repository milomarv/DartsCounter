from dash import html
import dash_bootstrap_components as dbc

class ScoreButton:
    def __init__(self, color: str, fontMultiplier: int = 1, vhMultiplier: int = 1):
        self.vhMultiplier = vhMultiplier + 0.125 * (vhMultiplier - 1)
        self.fontMultiplier = fontMultiplier
        self.color = color

    def Build(self, displayText: str, id: str):
        return dbc.Button(
            displayText, 
            style = {
                "width": "100%", 
                "height": f"{13*self.vhMultiplier}vh",
                "fontSize": f"{3*self.fontMultiplier}rem",
                "fontWeight": "bold",
                "margin": "1vh"
            },
            color=self.color,
            id = f"{id}-score-button"
        )