from dash import Output, Input, State, html

from app import app
import dash_bootstrap_components as dbc

from apps.layouts.accessibility import colourblind_mode, dark_mode


@app.callback(
    Output("help_modal", "is_open"),
    [Input("open_help", "n_clicks")],
    [State("help_modal", "is_open")],
)
def toggle_help_modal(n_clicks, is_open):
    """
    Open and close modal
    :param n_clicks: integer
    :param is_open: boolean
    :return: boolean
    """
    if n_clicks:
        return not is_open
    return is_open


@app.callback(
    Output("help_modal_body", "children"),
    [Input("help_modal_body", "children"),
     Input(colourblind_mode, 'value'),
     Input(dark_mode, 'value')],
)
def help_modal_body_update(_, colourblind_mode, dark_mode):
    """
    Return the components for the help model based on the accessibility parameters
    :param _: dummy variable
    :param colourblind_mode: boolean
    :param dark_mode: boolean
    :return: list of Dash components
    """
    if colourblind_mode:
        suffix = "cb"
    elif dark_mode:
        suffix = "dk"
    else:
        suffix = "default"

    return [
            dbc.Row(dbc.Row([html.H3("How to access accessibility settings"), html.P("To access the accessibility settings, click the icon in the header menu as shown below"), html.Img(src=f"/assets/accessibility_{suffix}.png", className="help-img")])),
            dbc.Row(dbc.Row([html.H3("How to filter by location"), html.P("To filter the data by location, click on the dropdowns and choose a location as shown below"), html.Img(src=f"/assets/filter_menu_{suffix}.png", className="help-img")])),
            dbc.Row(dbc.Row([html.H3("How to export download graph as image"), html.P("To export an graph as an image, click the button as shown below"), html.Img(src=f"/assets/download_png_{suffix}.png", className="help-img")])),
            dbc.Row(dbc.Row([html.H3("How to export chart data"), html.P("To export an graph as an a csv, xlsx or json file, click the button as shown below"), html.Img(src=f"/assets/export_chart_data_{suffix}.png", className="help-img")])),
            dbc.Row(dbc.Row([html.H3("How to filter by date range"), html.P("To filter the data by date range, slide the handles of the date slider to your specified date range as shown below"), html.Img(src=f"/assets/date_filter_{suffix}.png", className="help-img")])),
    ]