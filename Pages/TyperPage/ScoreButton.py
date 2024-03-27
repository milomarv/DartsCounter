import dash_bootstrap_components as dbc


class ScoreButton:
    def __init__(self, color: str, font_multiplier: float = 1, vh_multiplier: int = 1):
        self.vhMultiplier = vh_multiplier + 0.125 * (vh_multiplier - 1)
        self.fontMultiplier = font_multiplier
        self.color = color

    def build(self, display_text: str, identifier: str) -> dbc.Button:
        return dbc.Button(
            display_text,
            style={
                'width': '100%',
                'height': f'{13 * self.vhMultiplier}vh',
                'fontSize': f'{3 * self.fontMultiplier}rem',
                'fontWeight': 'bold',
                'margin': '1vh'
            },
            color=self.color,
            id=f'{identifier}-score-button'
        )
