class ConfirmationContentBase:
    def __init__(self) -> None:
        self.baseStyle = {
            'white-space': 'nowrap'
        }
        self.textBaseStyle = {
            'color': 'grey',
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
