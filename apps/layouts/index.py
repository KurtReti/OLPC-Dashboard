import os
from dash import dcc, html

layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Location(id='redirect', refresh=True),
    html.Div(id='page-content'),
    html.Div([html.Img(src=f"/assets/{f_name}") for f_name in os.listdir("assets") if f_name.endswith(".png")],
             id="preload", style={"display": "none"})
])
