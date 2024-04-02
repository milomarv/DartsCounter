from dash.dependencies import Input, Output, State

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Errors import AllLegsFinishedError, AllTurnsFinishedError, AlreadyFinishedError, GameAlreadyFinishedError, \
    GameNotStartedError, \
    GameRollBackNotPossibleError, \
    NoLegCreatedError, \
    NoRoundCreatedError, \
    NoSetCreatedError, NoTurnCreatedError
from Logging.Logger import Logger
from Models import Leg, Player, Set, Turn
from Models.DartScore import DOUBLE, DartScore, MISS, SINGLE, TRIPLE
from Pages.TyperPage.DartIcon import DartIcon
from Pages.TyperPage.GameWinConfirmationContent import GameWinConfirmationContent
from Pages.TyperPage.LegWinConfirmationContent import LegWinConfirmationContent
from Pages.TyperPage.OvershootConfirmationContent import OvershootConfirmationContent
from Pages.TyperPage.ScoreConfirmationContent import ScoreConfirmationContent
from Pages.TyperPage.SetWinConfirmationContent import SetWinConfirmationContent


class ThrowDart(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.game = dependency_container.game
        self.online_mode = dependency_container.online_mode
        self.inputs = [
            Input('0-score-button', 'n_clicks'),
            Input('1-score-button', 'n_clicks'),
            Input('2-score-button', 'n_clicks'),
            Input('3-score-button', 'n_clicks'),
            Input('4-score-button', 'n_clicks'),
            Input('5-score-button', 'n_clicks'),
            Input('6-score-button', 'n_clicks'),
            Input('7-score-button', 'n_clicks'),
            Input('8-score-button', 'n_clicks'),
            Input('9-score-button', 'n_clicks'),
            Input('10-score-button', 'n_clicks'),
            Input('11-score-button', 'n_clicks'),
            Input('12-score-button', 'n_clicks'),
            Input('13-score-button', 'n_clicks'),
            Input('14-score-button', 'n_clicks'),
            Input('15-score-button', 'n_clicks'),
            Input('16-score-button', 'n_clicks'),
            Input('17-score-button', 'n_clicks'),
            Input('18-score-button', 'n_clicks'),
            Input('19-score-button', 'n_clicks'),
            Input('20-score-button', 'n_clicks'),
            Input('25-score-button', 'n_clicks'),
            Input('50-score-button', 'n_clicks'),
            Input('go-back-score-button', 'n_clicks'),
            Input('score-confirm-button', 'n_clicks'),
            Input('leg-win-confirm-button', 'n_clicks'),
            Input('set-win-confirm-button', 'n_clicks'),
            Input('rollback-not-possible-confirm-button', 'n_clicks'),
            Input('typer-interval', 'n_intervals')
        ]
        self.outputs = [
            Output('typer-score', 'children'),
            Output('dart1-icon', 'children'),
            Output('dart2-icon', 'children'),
            Output('dart3-icon', 'children'),
            Output('typer-player-name', 'children'),
            Output('typer-leg-avg', 'children'),
            Output('load-game-info-error-modal', 'is_open'),
            Output('load-game-info-error-modal-body', 'children'),
            Output('score-confirm-modal', 'is_open'),
            Output('score-confirm-modal-body', 'children'),
            Output('leg-win-confirm-modal', 'is_open'),
            Output('leg-win-confirm-modal-body', 'children'),
            Output('set-win-confirm-modal', 'is_open'),
            Output('set-win-confirm-modal-body', 'children'),
            Output('game-win-confirm-modal', 'is_open'),
            Output('game-win-confirm-modal-body', 'children'),
            Output('rollback-not-possible-confirm-modal', 'is_open'),
            Output('typer-interval', 'disabled'),
            Output('typer-interval', 'interval')
        ]
        self.states = [
            State('x2-score-button', 'active'),
            State('x3-score-button', 'active'),
            State('score-confirm-modal', 'is_open')
        ]
        self.emptyDartIcon = DartIcon().build()
        self.emptyAllDartsIcon = [self.emptyDartIcon, self.emptyDartIcon, self.emptyDartIcon]
        self.ScoreConfirmationContent = ScoreConfirmationContent()
        self.OvershootConfirmationContent = OvershootConfirmationContent()
        self.LegWinConfirmationContent = LegWinConfirmationContent()
        self.SetWinConfirmationContent = SetWinConfirmationContent()
        self.GameWinConfirmationContent = GameWinConfirmationContent()
        self.UpdateInterval = 2000
        self.logger.info('Initialized ThrowDart Template')

    def callback(
        self,
        _s0: int, _s1: int, _s2: int, _s3: int, _s4: int, _s5: int, _s6: int, _s7: int, _s8: int, _s9: int,
        _s10: int, _s11: int, _s12: int, _s13: int, _s14: int, _s15: int, _s16: int, _s17: int, _s18: int,
        _s19: int, _s20: int, _s25: int, _s50: int, _go_back: int,
        _score_confirm: int, _leg_win_confirm: int, _set_win_confirm: int, _roll_back_not_possible_confirm: int,
        _n_update_interval: int, x2_active: bool, x3_active: bool, score_confirm_modal_is_open: bool
    ) -> list:
        prop_id = self.get_prop_from_context(block_initial = False)

        if prop_id == 'go-back-score-button':
            try:
                self.game.rollback()
            except GameRollBackNotPossibleError:
                return [
                    'N/A', *self.emptyAllDartsIcon, 'Player', '0',
                    False, None, False, None, False, None, False, None, False, None, True, True, self.UpdateInterval
                ]

        try:
            current_set = self.game.get_current_set()
        except GameNotStartedError as e:
            return [
                'N/A', *self.emptyAllDartsIcon, 'Player', '0',
                True, str(e), False, None, False, None, False, None, False, None, False, True, self.UpdateInterval
            ]
        except NoSetCreatedError:
            self.game.begin_new_set()
            current_set = self.game.get_current_set()

        try:
            current_leg = current_set.get_current_leg()
        except NoLegCreatedError:
            current_set.begin_new_leg()
            current_leg = current_set.get_current_leg()

        try:
            current_round = current_leg.get_current_round()
        except NoRoundCreatedError:
            current_leg.begin_new_round()
            current_round = current_leg.get_current_round()

        try:
            current_turn = current_round.get_current_turn()
        except NoTurnCreatedError:
            current_round.begin_next_turn()
            current_turn = current_round.get_current_turn()

        if self.check_for_darts_throw(prop_id):
            score = int(prop_id.split('-')[0])
            if x2_active:
                multiplier = DOUBLE
            elif x3_active:
                multiplier = TRIPLE
            elif prop_id == '50-score-button':
                multiplier = DOUBLE
                score = 25
            elif prop_id == '0-score-button':
                multiplier = MISS
            else:
                multiplier = SINGLE
            current_turn.throw_dart(DartScore(score, multiplier))
            if current_turn.get_next_dart():
                self.game.save()

        dart_icons = self.generate_darts_icons(current_turn)

        avg_leg_score = self.calculate_avg(current_leg, current_turn.player)

        if prop_id == 'score-confirm-button' or (prop_id == 'typer-interval' and score_confirm_modal_is_open):
            if current_leg.winner:
                leg_win_confirm_modal_body = self.LegWinConfirmationContent.build(
                    current_leg.winner.name,
                    current_leg.get_thrown_darts(current_leg.winner)
                )
                return [
                    str(current_leg.get_points_left(current_turn.player)),
                    *dart_icons,
                    current_turn.player.name, 0,
                    False, None, False, None, True, leg_win_confirm_modal_body, False, None, False, None, False, True,
                    self.UpdateInterval
                ]
            try:
                try:
                    current_round.begin_next_turn()
                    current_turn = current_round.get_current_turn()
                except AlreadyFinishedError:
                    pass
            except AllTurnsFinishedError:
                current_round.finish()
                current_leg.begin_new_round()
                current_round = current_leg.get_current_round()
                current_round.begin_next_turn()
                current_turn = current_round.get_current_turn()
            self.game.save()
            dart_icons = self.generate_darts_icons(current_turn)
            avg_leg_score = self.calculate_avg(current_leg, current_turn.player)

        if prop_id == 'leg-win-confirm-button':
            try:
                try:
                    current_leg.finish()
                    avg_leg_score, current_turn, current_leg, dart_icons = self.begin_new_leg(
                        current_set)
                except AlreadyFinishedError:
                    pass
            except AllLegsFinishedError:
                set_win_confirm_modal_body = self.SetWinConfirmationContent.build(
                    current_set.winner.name,
                    round(current_set.get_avg_score(current_set.winner), 2),
                )
                return [
                    str(current_leg.get_points_left(current_turn.player)),
                    *dart_icons,
                    current_turn.player.name, avg_leg_score,
                    False, None, False, None, False, None, True, set_win_confirm_modal_body, False, None, False, True,
                    self.UpdateInterval
                ]

        if prop_id == 'set-win-confirm-button':
            try:
                current_set.finish()
                self.game.begin_new_set()
                current_set = self.game.get_current_set()
                avg_leg_score, current_turn, current_leg, dart_icons = self.begin_new_leg(
                    current_set)
            except GameAlreadyFinishedError:
                game_win_confirm_modal_body = self.GameWinConfirmationContent.build(
                    self.game.winner.name,
                    round(self.game.get_avg_score(self.game.winner), 2)
                )
                self.game.started = False
                self.game.save()
                return [
                    str(current_leg.get_points_left(current_turn.player)),
                    *dart_icons,
                    current_turn.player.name, avg_leg_score,
                    False, None, False, None, False, None, False, None, True, game_win_confirm_modal_body, False, True,
                    self.UpdateInterval
                ]
            except AlreadyFinishedError:
                pass

        if not current_turn.get_next_dart():
            try:
                current_turn.finish()
            except AlreadyFinishedError:
                pass
            open_score_confirm_modal = True
            if current_turn.overshot:
                score_confirm_modal_body = self.OvershootConfirmationContent.build(
                    current_turn.player.name,
                    current_turn.get_score()
                )
            else:
                score_confirm_modal_body = self.ScoreConfirmationContent.build(
                    current_turn.player.name,
                    current_turn.get_score()
                )
            update_interval = 5000
            interval_is_disabled = False
        else:
            open_score_confirm_modal = False
            score_confirm_modal_body = None
            update_interval = 1000
            interval_is_disabled = not self.online_mode.value

        return [
            str(current_leg.get_points_left(current_turn.player)),
            *dart_icons,
            current_turn.player.name, avg_leg_score,
            False, None, open_score_confirm_modal, score_confirm_modal_body,
            False, None, False, None, False, None, False,
            interval_is_disabled, update_interval
        ]

    def begin_new_leg(self, current_set: Set) -> tuple:
        current_set.begin_new_leg()
        current_leg = current_set.get_current_leg()
        current_leg.begin_new_round()
        current_round = current_leg.get_current_round()
        current_round.begin_next_turn()
        current_turn = current_round.get_current_turn()
        dart_icons = self.generate_darts_icons(current_turn)
        avg_leg_score = self.calculate_avg(current_leg, current_turn.player)
        return avg_leg_score, current_turn, current_leg, dart_icons

    @staticmethod
    def generate_darts_icons(current_turn: Turn) -> list:
        dart_icons = []
        for dart in current_turn.scores.values():
            dart_icons.append(DartIcon().build(dart))
        return dart_icons

    @staticmethod
    def calculate_avg(current_leg: Leg, player: Player) -> float:
        avg_leg_score = current_leg.get_avg_score(player)
        if not avg_leg_score:
            avg_leg_score = 0
        avg_leg_score = round(avg_leg_score, 2)
        return avg_leg_score

    @staticmethod
    def check_for_darts_throw(prop_id: str) -> bool:
        if prop_id \
                and not prop_id.startswith('score-confirm') \
                and not prop_id.startswith('leg-win-confirm') \
                and not prop_id.startswith('set-win-confirm') \
                and not prop_id.startswith('rollback-not-possible') \
                and not prop_id.startswith('go-back') \
                and not prop_id.startswith('typer-interval'):
            return True
        else:
            return False
