import json

import dash
import pandas as pd
from dash import Output, Input, State, ALL, dcc

from app import app
from apps.layouts.export import export_data_modal, export_data_store, export_data_dropdown, export_data_button, \
    export_data_download


@app.callback(
    Output(export_data_download, 'data'),
    Input(export_data_button, 'n_clicks'),
    State(export_data_dropdown, 'value'),
    State(export_data_store, 'data')
)
def export_func(n_clicks, file_type, data):
    """
    Returns content for download based on export button clicked
    :param n_clicks: int
    :param file_type: string
    :param data: string of json
    :return: dict of dataframe content
    """
    if n_clicks:
        df = pd.DataFrame(json.loads(data["df"]))
        if file_type == "CSV":
            return dcc.send_data_frame(df.to_csv, f"{data['filename']}.csv")
        elif file_type == "XLSX":
            return dcc.send_data_frame(df.to_excel, f"{data['filename']}.xlsx")
        elif file_type == "JSON":
            return dcc.send_data_frame(df.to_json, f"{data['filename']}.json")
    return dash.no_update


@app.callback(
    [Output(export_data_modal, "is_open"),
     Output(export_data_store, "data")],
    [Input({'type': 'dynamic-button', 'index': ALL}, 'n_clicks')],
    [State({'type': 'dynamic-store', 'index': ALL}, 'data'),
     State(export_data_modal, "is_open")],
    prevent_initial_call=True
)
def toggle_export_modal(n_clicks, data, is_open):
    """
    Toggles the export data modal to select file type to download
    :param n_clicks:int
    :param data: dict
    :param is_open: boolean
    :return: tuple of boolean and json string
    """
    # iterate through all the dynamic data store and find one which corresponds to the button that was triggered
    graph_id = [d for d in data if
                dash.callback_context.triggered[0]["prop_id"].startswith(f'{{"index":"{d["id"]}"') and
                dash.callback_context.triggered[0]["value"]]
    if graph_id:
        return not is_open, graph_id[0]
    return is_open, dash.no_update
