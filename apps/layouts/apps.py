import os
import pandas as pd
from dash import dcc, html
from sqlalchemy import select, exists
import dash_bootstrap_components as dbc
from apps.db_models.account import Account
from apps.db_models.activity import Activity
from apps.db_models.device_ownership import DeviceOwnership
from apps.db_models.school import School
from apps.layouts.loaders import cube_loader
from apps.queries.apps import get_first_and_last_dates
from apps.callbacks.location_filters import create_location_filters
import plotly.express as px

from apps.utils.loader import MyLoading

px.set_mapbox_access_token(os.getenv("MAPBOX_TOKEN"))

filter_only_with_activity_data = exists(
    select(Activity.id).select_from(Activity).join(DeviceOwnership, DeviceOwnership.deviceid == Activity.deviceid).join(
        Account).filter(Account.schoolid == School.id))

states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown, location_filters_html, set_state_options, set_suburbs_options, set_postcode_options, apply_location_filters = create_location_filters(
    filter_only_with_activity_data)

app_usage_div = html.Div(cube_loader)

app_usage_dropdown = dcc.Dropdown(['BY CATEGORY', 'BY DEVELOPER', 'BY RATING'], 'BY CATEGORY', searchable=False,
                                  clearable=False)


def create_date_slider():
    dates = get_first_and_last_dates()
    r = (pd.date_range(pd.to_datetime(dates[0]),
                       pd.to_datetime(dates[1]) + pd.offsets.QuarterBegin(1), freq='Q')
         .tolist())
    all_dates = {int(x.timestamp()): x.strftime("%b %Y") for x in r}

    dates = list(all_dates.keys())
    slider = dcc.RangeSlider(
        min=dates[0],
        max=dates[-1],
        marks=all_dates,
        value=[dates[0], dates[-1]],
        tooltip={"always_visible": False, "placement": "top"},
        allowCross=False,
        className="tooltip-as-date"
    )
    return slider


date_slider = create_date_slider()

app_usage_components = [dbc.Row([dbc.Col(html.B("APP USAGE")), dbc.Col(
    app_usage_dropdown)]), dbc.Row(
    MyLoading(children=[
        app_usage_div], type="cube"))]

most_popular_apps_div = html.Div(cube_loader)

most_popular_apps_dropdown = dcc.Dropdown(['BY ALL USAGE', 'BY SCHOOL TIME USAGE', 'BY OUTSIDE SCHOOL TIME USAGE'],
                                          'BY ALL USAGE',
                                          searchable=False,
                                          clearable=False)

most_popular_apps_components = [dbc.Row([dbc.Col(html.B("MOST POPULAR APPS")), dbc.Col(
    most_popular_apps_dropdown)]), dbc.Row(
    MyLoading(children=[most_popular_apps_div], type="cube"))]

usage_of_apps_by_location_div = html.Div(cube_loader)

usage_of_apps_by_location_dropdown = dcc.Dropdown(
    ['BY TOTAL USAGE', 'BY AVG USAGE', 'BY LONGEST USAGE', 'BY SCHOOL TIME USAGE',
     'BY OUTSIDE SCHOOL TIME USAGE'], 'BY TOTAL USAGE', searchable=False, clearable=False
)

usage_of_apps_by_location_components = [dbc.Row([dbc.Col(html.B("USAGE OF APPS BY LOCATION")), dbc.Col(
    usage_of_apps_by_location_dropdown)]), dbc.Row(
    MyLoading(children=[usage_of_apps_by_location_div], type="cube"))
                                        ]

layout = html.Div(location_filters_html +
                  [
                      dbc.Row([date_slider], style={"padding": "25px"}),
                      dbc.Row([dbc.Col(app_usage_components, md=12, lg=6),
                               dbc.Col(most_popular_apps_components, md=12, lg=6)]),
                      dbc.Row(usage_of_apps_by_location_components)])
