from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger


class ActivateMultiplier(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [
            Input('x2-score-button', 'n_clicks'),
            Input('x3-score-button', 'n_clicks'),
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
        ]
        self.outputs = [
            Output('x2-score-button', 'active'),
            Output('x3-score-button', 'active'),
            Output('25-score-button', 'disabled'),
            Output('50-score-button', 'disabled'),
            Output('x2-score-button', 'color'),
            Output('x3-score-button', 'color'),
            Output('25-score-button', 'color'),
            Output('50-score-button', 'color')
        ]
        self.states = [
            State('x2-score-button', 'active'),
            State('x3-score-button', 'active')
        ]
        self.logger.info('Initialized Activate Multiplier Callback')

    def callback(
        self,
        _n_clicks_x2: int, _n_clicks_x3: int,
        _s0: int, _s1: int, _s2: int, _s3: int, _s4: int, _s5: int, _s6: int, _s7: int, _s8: int, _s9: int,
        _s10: int,
        _s11: int, _s12: int, _s13: int, _s14: int, _s15: int, _s16: int, _s17: int, _s18: int, _s19: int,
        _s20: int,
        x2_active: bool, x3_active: bool
    ) -> list[bool | str]:
        prop_id = self.get_prop_from_context()
        if prop_id == 'x2-score-button':
            if x2_active:
                return [False, False, False, False, 'primary', 'primary', 'primary', 'primary']
            else:
                return [True, False, True, True, 'success', 'primary', 'secondary', 'secondary']
        elif prop_id == 'x3-score-button':
            if x3_active:
                return [False, False, False, False, 'primary', 'primary', 'primary', 'primary']
            else:
                return [False, True, True, True, 'primary', 'success', 'secondary', 'secondary']
        elif not prop_id.startswith('x'):
            return [False, False, False, False, 'primary', 'primary', 'primary', 'primary']
        raise PreventUpdate
