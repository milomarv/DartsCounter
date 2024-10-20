import json
from dash.dependencies import Input, Output, ALL
from dash.exceptions import PreventUpdate
from dash import callback_context

from Callbacks.CallbackBase import CallbackBase
from Callbacks.GameDetailsPage import GAME_DETAILS_PATH
from Models.DartScore import DOUBLE, MISS, SINGLE, TRIPLE
from Pages.PlayerStatsContentDiv import PlayerStatsContentDiv
from Pages.GamesDetailsPage.GameDetailsPlayerDetailsModal import (
    GameDetailsPlayerDetailsModal,
)
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger


class LoadGameDetailsPlayerModal(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [
            Input('url', 'pathname'),
            Input({'type': 'game-details-player-button', 'index': ALL}, 'n_clicks'),
        ]
        self.outputs = [Output('game-details-player-details-modal-div', 'children')]
        self.states = []
        self.logger.info('Initialized Game Details Player Modal Callback')

        self.player_card = PlayerStatsContentDiv()

    def callback(self, url: str, n_clicks: int) -> object:
        ctx = callback_context
        if url.startswith(GAME_DETAILS_PATH) and any(n_clicks) and ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            button_id_dict = json.loads(button_id)
            player_id = button_id_dict['index']

            game_key = url.split('/')[-1]
            game = self.get_last_version_of_game_key(game_key)
            player = [player for player in game.players if str(player.id) == player_id][
                0
            ]

            possible_checkouts, successful_checkouts = (
                game.get_possible_and_successful_checkouts(player)
            )
            checkout_counter_str = f'{successful_checkouts}/{possible_checkouts}'

            thrown_darts = game.get_thrown_darts(player)
            single = game.get_score_count('multiplier', SINGLE, player)
            single_perc = single / thrown_darts
            double = game.get_score_count('multiplier', DOUBLE, player)
            double_perc = double / thrown_darts
            triple = game.get_score_count('multiplier', TRIPLE, player)
            triple_perc = triple / thrown_darts
            miss = game.get_score_count('multiplier', MISS, player)
            miss_perc = miss / thrown_darts

            numbers = self.player_card.polarVals
            n_hits = []
            for n in numbers:
                n_hits.append(game.get_score_count('score', n, player))

            player_stats = PlayerStatsContentDiv().build(
                show_points_left=False,
                avg=game.get_avg_score(player),
                thrown_darts=game.get_thrown_darts(player),
                checkout_counter=checkout_counter_str,
                set_wins=game.get_set_wins(player),
                leg_wins=game.get_leg_wins(player),
                checkout_rate=game.get_checkout_rate(player),
                single=single,
                double=double,
                triple=triple,
                miss=miss,
                single_perc=single_perc,
                double_perc=double_perc,
                triple_perc=triple_perc,
                miss_perc=miss_perc,
                n_hits=n_hits,
            )
            player_modal = GameDetailsPlayerDetailsModal().build(
                player.name, player_stats
            )

            return [player_modal]
        raise PreventUpdate
