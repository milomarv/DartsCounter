import dash
from dash.exceptions import PreventUpdate


class CallbackBase:
    def register(self) -> None:
        self.app.callback(
            self.outputs,
            self.inputs,
            self.states
        )(self.callback)

    @staticmethod
    def get_prop_from_context(block_initial: bool = True) -> str | None:
        ctx = dash.callback_context
        if not ctx.triggered:
            if block_initial:
                raise PreventUpdate
            else:
                return None
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        return prop_id
