import dash_bootstrap_components as dbc
from dash import html

layout = html.Div([
    html.Div(html.Div(html.Div(html.Span("help", className="material-icons"), className="fab-content"),
                      className="fab shadow"), className="fab-container", id="open_help", style={"cursor": "pointer"}),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("HELP")),
            dbc.ModalBody(id="help_modal_body")
        ],
        id="help_modal",
        is_open=False,
        size="xl",
        centered=True,
        scrollable=True,
    )
])
