from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Errors import GameNotStartedError, NoLegCreatedError, NoSetCreatedError
from Logging.Logger import Logger
from Models.DartScore import DOUBLE, MISS, SINGLE, TRIPLE
from Pages.ScoreboardPage.PlayerCard import PlayerCard


class UpdatePlayerCards(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.game = dependency_container.game
        self.inputs = [
            Input('scoreboard-update-interval', 'n_intervals'),
        ]
        self.outputs = [Output('scoreboard-player-area', 'children')]
        self.states = [
            State('game-filter-button', 'className'),
            State('current-set-filter-button', 'className'),
            State('current-leg-filter-button', 'className'),
        ]
        self.logger.info('Initialized Callback Template')
        self.player_card = PlayerCard()
        self.emptyDartIcon = self.player_card.dartIcon.build()

    def callback(
        self, _n_intervals: int, game_filter: str, set_filter: str, leg_filter: str
    ) -> list:
        que_on = None
        try:
            if game_filter == 'btn btn-primary':
                que_on = self.game
            elif set_filter == 'btn btn-primary':
                que_on = self.game.get_current_set()
            elif leg_filter == 'btn btn-primary':
                que_on = self.game.get_current_set().get_current_leg()
        except (GameNotStartedError, NoSetCreatedError):
            raise PreventUpdate

        return_cols = []
        for player in self.game.players:
            # Get Player Name
            player_name = player.name

            # Get If Player is on current turn
            try:
                current_turn = (
                    self.game.get_current_set()
                    .get_current_leg()
                    .get_current_round()
                    .get_current_turn()
                )
                if current_turn.player == player:
                    active = True
                else:
                    active = False
            except NoSetCreatedError:
                active = False

            # Get Player Current Score
            try:
                current_leg = self.game.get_current_set().get_current_leg()
                player_points_left = current_leg.get_points_left(player)
            except KeyError:
                player_points_left = 'N/A'
            except NoSetCreatedError:
                player_points_left = 'N/A'
            except NoLegCreatedError:
                player_points_left = 'N/A'
            except GameNotStartedError:
                player_points_left = 'N/A'

            # Get Player Current Avg
            if que_on:
                player_avg = que_on.get_avg_score(player)
                if not player_avg:
                    player_avg = 'N/A'
                else:
                    player_avg = round(player_avg, 2)
            else:
                player_avg = 'N/A'

            # Get Player Thrown Darts
            if que_on:
                player_darts = que_on.get_thrown_darts(player)
                if not player_darts:
                    player_darts = 0
            else:
                player_darts = 0

            # Get Set Wins
            set_wins = self.game.get_set_wins(player)

            # Get Leg Wins
            try:
                leg_wins = self.game.get_current_set().get_leg_wins(player)
            except NoSetCreatedError:
                leg_wins = 0
            except GameNotStartedError:
                leg_wins = 0

            # Get Singles, Doubles, Triples, Misses
            if que_on:
                try:
                    single = que_on.get_score_count('multiplier', SINGLE, player)
                    single_perc = single / player_darts
                    double = que_on.get_score_count('multiplier', DOUBLE, player)
                    double_perc = double / player_darts
                    triple = que_on.get_score_count('multiplier', TRIPLE, player)
                    triple_perc = triple / player_darts
                    miss = que_on.get_score_count('multiplier', MISS, player)
                    miss_perc = miss / player_darts
                except ZeroDivisionError:
                    single, double, triple, miss = 0, 0, 0, 0
                    single_perc, double_perc, triple_perc, miss_perc = 0, 0, 0, 0
            else:
                single, double, triple, miss = 0, 0, 0, 0
                single_perc, double_perc, triple_perc, miss_perc = 0, 0, 0, 0

            # Get N Hits on Numbers
            numbers = self.player_card.player_stats.polarVals
            if que_on:
                n_hits = []
                for n in numbers:
                    n_hits.append(que_on.get_score_count('score', n, player))
            else:
                n_hits = [0 for _ in numbers]

            # Get Players Last 3 Darts
            try:
                last_turn = (
                    self.game.get_current_set().get_current_leg().get_last_turn(player)
                )
                if last_turn:
                    dart_icons = []
                    total_score = 0
                    for dart in last_turn.scores.values():
                        if dart and not dart.no_dart:
                            dart_icons.append(self.player_card.dartIcon.build(dart))
                            total_score += dart.total
                        else:
                            dart_icons.append(self.emptyDartIcon)
                else:
                    dart_icons = [
                        self.emptyDartIcon,
                        self.emptyDartIcon,
                        self.emptyDartIcon,
                    ]
                    total_score = 0
            except NoSetCreatedError:
                dart_icons = [
                    self.emptyDartIcon,
                    self.emptyDartIcon,
                    self.emptyDartIcon,
                ]
                total_score = 0

            # Get Possible Checkouts
            if que_on:
                n_possible_checkouts, n_successful_checkouts = (
                    que_on.get_possible_and_successful_checkouts(player)
                )
            else:
                n_possible_checkouts, n_successful_checkouts = None, None
            if n_possible_checkouts or n_successful_checkouts:
                checkout_rate = (
                    f'{round(n_successful_checkouts / n_possible_checkouts * 100, 2)} %'
                )
                checkout_count = f'{n_successful_checkouts}/{n_possible_checkouts}'
            else:
                checkout_rate, checkout_count = 'N/A', 'N/A'

            player_stats_card = self.player_card.build(
                active,
                player_name,
                player_points_left,
                player_avg,
                player_darts,
                set_wins,
                leg_wins,
                single,
                double,
                triple,
                miss,
                single_perc,
                double_perc,
                triple_perc,
                miss_perc,
                n_hits,
                total_score,
                checkout_rate,
                checkout_count,
                *dart_icons,
            )
            return_cols.append(player_stats_card)
        return [return_cols]

    # def emptyDarts(self) -> object:
    #     dart1 = DartScore(0, NO_DART, NoDart=True)
    #     dart2 = DartScore(0, NO_DART, NoDart=True)
    #     dart3 = DartScore(0, NO_DART, NoDart=True)
    #     return dart1, dart2, dart3
