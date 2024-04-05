from typing import Any, Optional

from dash.dependencies import Input, Output, State
from dash.html import Div

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger
from Pages.ScoreboardPage.ScoreBoardEditLabelField import ScoreBoardEditLabelField
from Pages.ScoreboardPage.ScoreBoardLabelText import ScoreBoardLabelText


# TODO CONTINUE HERE
#   - write unit tests
#   - runt two games at once block each other

class EditScoreboardLabelCallback(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.inputs = [
            Input('edit-scoreboard-label', 'n_clicks'),
            Input('edit-scoreboard-label-enter-input', 'n_keydowns')
        ]
        self.outputs = [
            Output('scoreboard-label', 'children'),
            Output('edit-scoreboard-label-svg', 'src'),
            Output('scoreboard-label-value', 'data')
        ]
        self.states = [
            State('scoreboard-label', 'children'),
            State('scoreboard-label-value', 'data')
        ]

        self.scoreboard_edit_label_field = ScoreBoardEditLabelField()
        self.scoreboard_label_text = ScoreBoardLabelText()

        self.logger.info('Initialized Callback Edit Scoreboard Label')

    def callback(self, n_clicks: Optional[int], n_enter: Optional[int], current_children: Any, current_val: str) -> \
            list[Input | str] | list[Div | str]:
        current_type = current_children['type']

        if current_type == 'Div':
            if n_clicks or n_enter:
                return [self.scoreboard_edit_label_field.build(current_val), './assets/edit-save.svg', current_val]
        else:
            current_val = current_children['props']['value']

        return [self.scoreboard_label_text.build(current_val), './assets/edit.svg', current_val]
