from dash import ALL
from dash.dependencies import Input, Output, State

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger
from Models.Out import Out
from Models.Player import Player
from Models.TypeSetLeg import TypeSetLeg


class StartStopGame(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__()
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.game = dependency_container.game
        self.inputs = [
            Input('start-stop-game-button', 'n_clicks'),
            Input('end-game-confirm-button', 'n_clicks')
        ]
        self.outputs = [
            Output('start-stop-game-button', 'children'),
            Output('start-stop-game-button', 'className'),
            Output('start-game-error-modal', 'is_open'),
            Output('start-game-error-modal-body', 'children'),
            Output('end-game-confirm-modal', 'is_open')
        ]
        self.states = [
            State({'type': 'player-input', 'index': ALL}, 'value'),
            State('number-of-sets-input', 'value'),
            State('number-of-legs-input', 'value'),
            State('set-mode-select', 'value'),
            State('leg-mode-select', 'value'),
            State('points-input', 'value'),
            State('out-variant-select', 'value')
        ]
        self.logger.info('Initialized StartStopGame Callback')

    def callback(
            self,
            _n_start: int,
            _n_stop: int,
            players: list[str],
            n_sets: int,
            n_legs: int,
            set_type: str,
            leg_type: str,
            points: int,
            out: int
    ) -> list[str | bool | None]:
        if self.get_prop_from_context(block_initial=False) == 'start-stop-game-button':
            if not self.game.started:
                self.game.stop()
                try:
                    self.game.start(
                        players=[Player(name) for name in players if name],
                        nSets=n_sets,
                        setType=TypeSetLeg(set_type),
                        nLegs=n_legs,
                        legType=TypeSetLeg(leg_type),
                        points=points,
                        out=Out(out)
                    )
                    self.game.save()
                    return ['Stop Game', 'btn btn-danger', False, None, False]
                except ValueError as e:
                    return ['Start Game', 'btn btn-success', True, str(e), False]
            else:
                return ['Stop Game', 'btn btn-danger', False, None, True]
        elif self.get_prop_from_context(block_initial=False) == 'end-game-confirm-button':
            self.game.started = False
            return ['Start Game', 'btn btn-success', False, None, False]
        elif self.game.started:
            return ['Stop Game', 'btn btn-danger', False, None, False]
        else:
            return ['Start Game', 'btn btn-success', False, None, False]
