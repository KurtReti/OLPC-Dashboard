import base64
from dash import dcc, html
import dash_bootstrap_components as dbc
from apps.layouts import help_, export
from apps.layouts import accessibility

encoded_image = base64.b64encode(open("assets/accessibility.svg", 'rb').read()).decode()

nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("HOME", active=True, href="/app"), className="d-flex align-items-center"),
        dbc.NavItem(dbc.NavLink("DASHBOARD", href="/app/dashboard"), className="d-flex align-items-center"),
        dbc.NavItem(dbc.NavLink("CONTACT", href="/app/contact"), className="d-flex align-items-center"),
        dbc.NavItem(dbc.NavLink(html.Img(
            src='data:image/svg+xml;base64,{}'.format(encoded_image),
            className="settings_img",
            height="30px"), id="open_settings"), className="no-border pointer"),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0 header-navbar",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            dcc.Link(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/OLPCLogo.png", className="olpc-logo")),
                        dbc.Col(html.Span(className="header-title", id="page-name")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/app",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                nav,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    className="header"
)

layout = [
    navbar,
    dbc.Container(
        [dbc.Card(id='app-content'),
         dcc.Store(id='page-name-store'),
         dcc.Location(id='url_dashboard', refresh=False),
         ]
    ),
    html.Div(html.Br()),
    accessibility.layout,
    export.layout,
    help_.layout
]
