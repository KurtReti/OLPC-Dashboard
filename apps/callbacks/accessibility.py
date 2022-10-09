from dash.dependencies import Input, Output, State
from app import app

# clientside callback to set the font size
from apps.layouts.accessibility import text_size, text_font, colourblind_mode, dark_mode, colourblind_dark_mode_store

app.clientside_callback(
    """
    function(value) {
        switch (value) {
            case 0:
                document.documentElement.style.fontSize = "80%"
                break;
            case 3:
                document.documentElement.style.fontSize = "100%"
                break;
            case 6:
                document.documentElement.style.fontSize = "120%"
                break;
        }
        return window.dash_clientside.no_update
    }
    """,
    Output(text_size, 'value'),
    Input(text_size, 'value'),
)

# clientside callback to set the font family
app.clientside_callback(
    """
    function(value) {
        document.body.style.fontFamily = value

        return window.dash_clientside.no_update
    }
    """,
    Output(text_font, 'value'),
    Input(text_font, 'value'),
)

# clientside callback to set the colourblind and dark mode css sheets
app.clientside_callback(
    """
    function(colourblind_mode, dark_mode, colourblind_dark_mode_store) {
        triggered_by_colourblind = false;
        // check if callback has been triggered by element not page load
        if (window.dash_clientside.callback_context.triggered.length){
            triggered_by_colourblind = window.dash_clientside.callback_context.triggered[0]["prop_id"] == "colourblind_mode.value"
        } else {
            // retrieve values from data store if exists
            if(colourblind_dark_mode_store != undefined){
                colourblind_mode = colourblind_dark_mode_store[0]
                dark_mode = colourblind_dark_mode_store[1]
            }
        }
        // if both are currently toggled check which one triggered it and set other one un-toggled
        if(colourblind_mode && dark_mode){
            if(triggered_by_colourblind){
                dark_mode = false;
            } else {
                colourblind_mode = false;
            }
        }

        const theme = document.querySelector("#site-theme");
        const theme_default = document.querySelector("#site-theme-default");
        const theme_colourblind = document.querySelector("#site-theme-colourblind");
        const theme_dark = document.querySelector("#site-theme-dark");

        if(colourblind_mode){
            theme.href = theme_colourblind.getAttribute("href")
        } else if(dark_mode){
            theme.href = theme_dark.getAttribute("href")
        } else {
            theme.href = theme_default.getAttribute("href")
        }

        // return as array since dash needs multi-output callbacks to return tuple
        return [colourblind_mode, dark_mode, [colourblind_mode, dark_mode]]
    }
    """,
    Output(colourblind_mode, 'value'),
    Output(dark_mode, 'value'),
    Output(colourblind_dark_mode_store, 'data'),
    Input(colourblind_mode, 'value'),
    Input(dark_mode, 'value'),
    State(colourblind_dark_mode_store, 'data')
)


@app.callback(
    Output("accessibility_modal", "is_open"),
    [Input("open_settings", "n_clicks")],
    [State("accessibility_modal", "is_open")],
)
def toggle_accessibility_modal(n_clicks, is_open):
    """
    Open and close modal
    :param n_clicks: integer
    :param is_open: boolean
    :return: boolean
    """
    if n_clicks:
        return not is_open
    return is_open
