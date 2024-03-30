import datetime as dt


class DatabaseCallbacksOperations:
    @staticmethod
    def format_game_ts_pretty(game_ts_string: str) -> str:
        game_ts = dt.datetime.fromtimestamp(float(game_ts_string))
        game_ts_pretty = game_ts.strftime('%H:%M - %d.%b.%Y')
        return game_ts_pretty
