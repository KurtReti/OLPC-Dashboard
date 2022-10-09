import uuid
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.development.base_component import rd

export_data_dropdown = dcc.Dropdown(['CSV', 'XLSX', 'JSON'], 'CSV',
                                    searchable=False,
                                    clearable=False)

export_data_store = dcc.Store(id="export_data_store")
export_data_button = dbc.Button("Download", className="me-1 export-button")
export_data_download = dcc.Download()

export_data_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Export Data")),
        dbc.ModalBody([dbc.Row(dbc.Col(export_data_dropdown, width=6), className="justify-content-center",
                               style={"margin": "10px"}),
                       dbc.Row(dbc.Col(export_data_button, width=6, className="d-flex justify-content-center"),
                               className="justify-content-center", style={"margin": "10px"})]),
        export_data_store,
        export_data_download
    ],
    is_open=False,
    centered=True,
    id="export_data_modal")

layout = html.Div(export_data_modal)


def create_export_components(df, filename):
    """
    Creates components needed for export to function
    :param df: pandas Dataframe
    :param filename: string
    :return: tuple of html.Button, dcc.Store, dcc.Download
    """
    id = str(uuid.UUID(int=rd.randint(0, 2 ** 128)))

    export_button = html.Button(style={"visibility": "hidden"}, id={
        'type': 'dynamic-button',
        'index': id
    }, role="export")

    store = dcc.Store(id={
        'type': 'dynamic-store',
        'index': id
    }, data={"df": df.to_json(orient="records"), "filename": filename, "id": id})

    download = dcc.Download(id={
        'type': 'dynamic-download',
        'index': id
    })
    return export_button, store, download
