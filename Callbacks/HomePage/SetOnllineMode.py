from typing import List

from dash.dependencies import Input, Output

from Callbacks.CallbackBase import CallbackBase
from DependencyContainer import DependencyContainer
from Logging.Logger import Logger


class SetOnlineMode(CallbackBase):
    def __init__(self, dependency_container: DependencyContainer) -> None:
        super().__init__(dependency_container)
        self.logger = Logger(__name__)
        self.app = dependency_container.app
        self.online_mode = dependency_container.online_mode
        self.inputs = [
            Input('online-switch', 'value')
        ]
        self.outputs = [
            Output('online-switch', 'label')
        ]
        self.states = []
        self.running = []
        self.logger.info('Initialized set Online Mode Callback')

    def callback(self, switch_val: bool) -> List[str]:
        if type(switch_val) is type(None):
            if self.online_mode.value:
                return ['Online']
            else:
                return ['Offline']
        else:
            if switch_val:
                self.logger.info('Switched to Online Mode')
                self.online_mode.value = True
                return ['Online']
            else:
                self.logger.info('Switched to Offline Mode')
                self.online_mode.value = False
                return ['Offline']
