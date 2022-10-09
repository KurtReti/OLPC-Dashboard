from dash import dcc, html
from sqlalchemy import select, exists
import dash_bootstrap_components as dbc
from apps.db_models.naplan import Naplan
from apps.db_models.school import School
from apps.layouts.loaders import cube_loader, default_loader
from apps.callbacks.location_filters import create_location_filters
from apps.utils.loader import MyLoading

filter_only_with_naplan_data = exists(select(Naplan.id).filter(Naplan.schoolid == School.id))

states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown, location_filters_components, set_state_options, set_suburbs_options, set_postcode_options, apply_location_filters = create_location_filters(
    filter_only_with_naplan_data)

number_of_schools_div = html.Div(default_loader, className="card-text", style={"textAlign": "center"})
number_of_schools_title = html.B(className="card-title")

number_of_schools_components = dbc.Card([dbc.CardHeader(number_of_schools_title),dbc.CardBody(
        MyLoading(children=[number_of_schools_div])
    )]
)

total_number_of_tests_div = html.Div(default_loader, className="card-text", style={"textAlign": "center"})
total_number_of_tests_title = html.B(className="card-title")

total_number_of_tests_components = dbc.Card([dbc.CardHeader(total_number_of_tests_title), dbc.CardBody(
        MyLoading(children=[total_number_of_tests_div]),
    )]
)

highest_naplan_score_div = html.Div(default_loader, className="card-text", style={"textAlign": "center"})
highest_naplan_score_title = html.B(className="card-title")

highest_naplan_score_components = dbc.Card([dbc.CardHeader(highest_naplan_score_title), dbc.CardBody(
        MyLoading(children=[highest_naplan_score_div])
)
    ]
)

naplan_results_div = html.Div(cube_loader)

naplan_results_dropdown = dcc.Dropdown(['ALL SCHOOLS', 'GOVERNMENT', 'CATHOLIC', "INDEPENDENT"], 'ALL SCHOOLS',
                                       searchable=False, clearable=False, style={"visibility": "hidden"})

naplan_results_components = [dbc.Row([dbc.Col(html.B("NAPLAN RESULTS")), dbc.Col(
    naplan_results_dropdown)]),
                             dbc.Row(MyLoading(children=[
                                 naplan_results_div], type="cube"))
                             ]

layout = html.Div(location_filters_components + [
    dbc.Row(html.Br()),
    dbc.Row([dbc.Col(number_of_schools_components, md=12, lg=4, style={"marginBottom": "14px"}),
             dbc.Col(highest_naplan_score_components, md=12, lg=4, style={"marginBottom": "14px"}),
             dbc.Col(total_number_of_tests_components, md=12, lg=4, style={"marginBottom": "14px"})]),
    dbc.Row(html.Br()),
    dbc.Row(naplan_results_components)])
