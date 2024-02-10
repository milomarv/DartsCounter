import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from Logging.Logger import Logger

import Callbacks

logger = Logger(__name__)

app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    suppress_callback_exceptions=True
)

app.title = "Darts Counter"

app.layout = html.Div([
    html.Link(
        rel='shortcut icon',
        href='/assets/favicon.ico',
    ),
    html.Div(id = "page-content"),
    dcc.Location(id = "url", refresh = False)
])

server = app.server

logger.info("Inizialized Dash App")

Callbacks.Initializer(app).Run()
logger.info("Initialized Callbacks")

if __name__ == "__main__":
    app.run_server(debug=True, host = "0.0.0.0")
