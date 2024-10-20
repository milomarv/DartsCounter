from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger

from Callbacks.GameDetailsPage import GAME_DETAILS_PATH
from Pages.GamesDetailsPage.GamePlayerCard import GamePlayerCard


class LoadGameDetailsPlayers(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [
            Input('url', 'pathname'),
        ]
        self.outputs = [
            Output('game-details-player-details', 'children'),
            Output('game-details-player-details', 'style'),
        ]
        self.states = [Input('game-details-player-details', 'style')]
        self.logger.info('Initialized Load Game Details Players Callback')

    def callback(self, url: str, style: dict) -> list[GamePlayerCard]:
        if url.startswith(GAME_DETAILS_PATH):
            game_key = url.split('/')[-1]
            game = self.get_last_version_of_game_key(game_key)

            style['justify-content'] = 'flex-start'

            player_cards = []
            for player in game.players:
                possible_checkouts, successful_checkouts = (
                    game.get_possible_and_successful_checkouts(player)
                )
                checkout_counter_str = f'{successful_checkouts}/{possible_checkouts}'
                player_cards.append(
                    GamePlayerCard().build(
                        player_name=player.name,
                        player_id=player.id,
                        avg=game.get_avg_score(player),
                        thrown_darts=game.get_thrown_darts(player),
                        checkout_counter=checkout_counter_str,
                        checkout_rate=game.get_checkout_rate(player),
                        set_wins=game.get_set_wins(player),
                        leg_wins=game.get_leg_wins(player),
                    )
                )

            return [player_cards, style]
        else:
            raise PreventUpdate
