class RouterConfig:
    home: list[str] = ['/home', '/']
    typer: str = '/typer'
    scoreboard: str = '/scoreboard'
    database: str = '/database'
    database_game_details: str = '/database/game-details'
    release_notes: str = '/release-notes'

    @staticmethod
    def is_route(pathname: str, route: list[str]) -> bool:
        if isinstance(route, list):
            return pathname in route
        elif isinstance(route, str):
            return pathname == route
        else:
            raise ValueError('Route must be a string or list of strings')
