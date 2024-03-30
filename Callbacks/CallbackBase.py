import json
from typing import Any

import dash
from dash.exceptions import PreventUpdate


class CallbackBase:
    def __init__(self, dash_package: Any = dash) -> None:
        self.dash = dash_package

    def register(self) -> None:
        # noinspection PyUnresolvedReferences
        self.app.callback(
            self.outputs,
            self.inputs,
            self.states
        )(self.callback)

    def get_prop_from_context(self, block_initial: bool = True) -> str | dict | None:
        ctx = self.dash.callback_context
        if not ctx.triggered:
            if block_initial:
                raise PreventUpdate
            else:
                return None
        prop_id = '.'.join(ctx.triggered[0]['prop_id'].split('.')[:-1])
        try:
            return json.loads(prop_id)
        except json.decoder.JSONDecodeError:
            return prop_id
