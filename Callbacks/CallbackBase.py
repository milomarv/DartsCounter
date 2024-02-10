import dash
from dash.exceptions import PreventUpdate

class CallbackBase:
    def Register(self):
        self.app.callback(
            self.outputs,
            self.inputs,
            self.states
        )(self.Callback)
    
    def getPropFromContext(self, blockInital =True):
        ctx = dash.callback_context
        if not ctx.triggered:
            if blockInital:
                raise PreventUpdate
            else:
                return None
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        return prop_id