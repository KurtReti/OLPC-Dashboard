import os

from dash import dcc, html
import plotly.express as px

import dash_bootstrap_components as dbc
from sqlalchemy import select, exists

from apps.db_models.account import Account
from apps.db_models.device_ownership import DeviceOwnership
from apps.db_models.school import School
from apps.layouts.loaders import cube_loader, default_loader
from apps.callbacks.location_filters import create_location_filters
from apps.utils.loader import MyLoading

px.set_mapbox_access_token(os.getenv("MAPBOX_TOKEN"))

filter_only_with_device_data = exists(select(DeviceOwnership.accountid).select_from(DeviceOwnership).join(Account).filter(Account.schoolid == School.id))

states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown, location_filters_components, set_state_options, set_suburbs_options, set_postcode_options, apply_location_filters = create_location_filters(
    filter_only_with_device_data)

total_number_devices_div = html.Div(default_loader,
                                    className="card-text",
                                    style={"textAlign": "center"}
                                    )

total_number_devices_title = html.B(className="card-title")

total_number_devices_components = dbc.Card([dbc.CardHeader(total_number_devices_title),dbc.CardBody(
        MyLoading(children=[total_number_devices_div])
    )]
)

avg_number_of_devices_per_school_or_school_type_div = html.Div(default_loader,
                                                               className="card-text",
                                                               style={"textAlign": "center"}
                                                               )

avg_number_of_devices_per_school_or_school_type_title = html.B(className="card-title")

avg_number_of_devices_per_school_or_school_type_components = dbc.Card([dbc.CardHeader(avg_number_of_devices_per_school_or_school_type_title),dbc.CardBody(
        MyLoading(children=[avg_number_of_devices_per_school_or_school_type_div])
    )]
)

school_with_most_devices_or_school_sector_devices = html.Div(default_loader,
                                                             className="card-text",
                                                             style={"textAlign": "center"}
                                                             )

school_with_most_devices_or_school_sector_title = html.B(className="card-title")

school_with_most_devices_or_school_sector_components = dbc.Card([dbc.CardHeader(school_with_most_devices_or_school_sector_title),dbc.CardBody(
        MyLoading(children=[school_with_most_devices_or_school_sector_devices])
    )]
)
devices_by_location_div = html.Div(cube_loader)

devices_by_location_dropdown = dcc.Dropdown(['BY TOTAL DEVICES', "BY TOTAL USES"], 'BY TOTAL DEVICES', searchable=False,
                                            clearable=False)

devices_by_location_components = [dbc.Row([dbc.Col(html.B("DEVICES BY LOCATION")),
                                           dbc.Col(devices_by_location_dropdown)]),
                                  dbc.Row(MyLoading(children=[
                                      devices_by_location_div],
                                      type="cube"))]

layout = html.Div(location_filters_components + [
    dbc.Row(html.Br()),
    dbc.Row([
        dbc.Col(total_number_devices_components, md=12, lg=4, style={"marginBottom": "1rem"}),
        dbc.Col(avg_number_of_devices_per_school_or_school_type_components, md=12, lg=4, style={"marginBottom": "1rem"}),
        dbc.Col(school_with_most_devices_or_school_sector_components, md=12, lg=4, style={"marginBottom": "1rem"})
    ]),
    dbc.Row(html.Br()),
    dbc.Row(devices_by_location_components)
])
