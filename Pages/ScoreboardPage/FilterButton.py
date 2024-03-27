import dash_bootstrap_components as dbc


class FilterButton:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build(pretty_name: str, identifier: str, active=False):
        if active:
            className = 'btn btn-primary'
        else:
            className = 'btn btn-secondary'
        return dbc.Button(
            pretty_name,
            id=f'{identifier}-filter-button',
            className=className,
            style={
                'width': '200px',
                'height': '50px',
                'fontSize': '20px'
            }
        )
