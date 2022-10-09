from dash.dependencies import Input, Output, State

# clientside callback to set the pagename in the browser when the page changes
from app import app
from apps.layouts import home, dashboard, contact, devices, apps, naplan, compare
from apps.utils.transform import remove_trailing_slash

app.clientside_callback(
    """
    function(pagename) {
        document.title = 'OLPC Dashboard - ' + pagename;
        return pagename;
    }
    """,
    Output('page-name', 'children'),
    [Input('page-name-store', 'value')]
)


@app.callback([Output("app-content", "children"), Output("page-name-store", "value")],
              [Input('url_dashboard', 'pathname')])
def switch_page(pathname):
    """
    Returns page content and page name based on url
    :param pathname: string
    :return: tuple of dash components and page name
    """
    pathname = remove_trailing_slash(pathname)
    if pathname == "/app":
        return home.layout, "Home"
    elif pathname == "/app/dashboard":
        return dashboard.generate_layout(None, dashboard.layout), "Dashboard"
    elif pathname == "/app/contact":
        return contact.layout, "Contact"
    elif pathname == "/app/dashboard/apps":
        return dashboard.generate_layout("apps", apps.layout), "Apps"
    elif pathname == "/app/dashboard/devices":
        return dashboard.generate_layout("devices", devices.layout), "Devices"
    elif pathname == "/app/dashboard/naplan":
        return dashboard.generate_layout("naplan", naplan.layout), "Naplan"
    elif pathname == "/app/dashboard/compare":
        return dashboard.generate_layout("compare", compare.layout), "Compare"


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n_clicks, is_open):
    """
    Toggles the navbar collapsing for mobile responsiveness
    :param n_clicks: int
    :param is_open: boolean
    :return: boolean
    """
    if n_clicks:
        return not is_open
    return is_open
