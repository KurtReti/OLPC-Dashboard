from dash import Output, Input

from app import app


@app.callback(Output('url_dashboard', 'pathname'), Input("tabs", "active_tab"),
              prevent_initial_call=True)
def switch_tab(tab):
    """
    Callback for when tab is clicked and changes the pathname which triggers switch_page callback to render content
    :param tab: string
    :return: string pathname
    """
    if tab == "apps":
        return "/app/dashboard/apps"
    elif tab == "devices":
        return "/app/dashboard/devices"
    elif tab == "naplan":
        return "/app/dashboard/naplan"
    elif tab == "compare":
        return "/app/dashboard/compare"
    return "/app/dashboard"
