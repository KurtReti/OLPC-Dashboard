import dash_bootstrap_components as dbc
from dash import html, dcc

text_size = dcc.Slider(id="text_size", marks={
    0: {'label': 'S', 'style': {'font-size': '0.8em'}},
    3: {'label': 'M', 'style': {'font-size': '1em'}},
    6: {'label': 'L', 'style': {'font-size': '1.3em'}}
}, value=3, step=None, persistence=True
                       )

text_font = dcc.Dropdown(["Inter", "Arial", "Calibri", "Open Sans", "Montserrat", "Roboto"], value='Inter', id="text_font", clearable=False,
                         persistence=True)

colourblind_mode = dbc.Switch(
    id="colourblind_mode",
    value=False
)

dark_mode = dbc.Switch(
    id="dark_mode",
    value=False
)

colourblind_dark_mode_store = dcc.Store(id='colourblind_dark_mode_store', storage_type='local')

layout = html.Div([colourblind_dark_mode_store, dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("ACCESSIBILITY SETTINGS")),
        dbc.ModalBody([dbc.Row([
            dbc.Col([
                dbc.Label("Text size", html_for=text_size.id),
                text_size,
            ]),
            dbc.Col([
                dbc.Label("Text font", html_for=text_font.id),
                text_font
            ])]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Colourblind mode", html_for=colourblind_mode.id),
                    colourblind_mode,
                ]),
                dbc.Col([
                    dbc.Label("Dark Mode", html_for=dark_mode.id),
                    dark_mode,
                ])])
        ])
    ],
    id="accessibility_modal",
    is_open=False,
    centered=True)])
