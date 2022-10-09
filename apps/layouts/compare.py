from dash import dcc, html
import dash_bootstrap_components as dbc
from apps.queries.compare import get_postcode_options, get_state_options, get_school_options, get_suburb_options
from apps.utils.loader import MyLoading

location_filters_html = [
    dbc.Row([dbc.Col("COMPARE BY", md=12, lg=6),
             dbc.Col(dcc.Dropdown(['SCHOOL', 'POSTCODE', 'SUBURB', 'STATE'], id="compare_by",
                                  placeholder='Select aggregation type', clearable=False), md=12, lg=6, style={"border": 0})],
            className="filter-menu-header"),
    MyLoading(dbc.Row(id="filter_dropdowns",
                        className="filter-menu"))]

compare_by_options_funcs = {'SCHOOL': get_school_options, 'POSTCODE': get_postcode_options,
                            'SUBURB': get_suburb_options, 'STATE': get_state_options}

naplan_results_div = html.Div()

naplan_results_components = [dbc.Row([html.B("NAPLAN RESULTS")], style={"marginTop": "10px"}),
                             dbc.Row(MyLoading(children=[
                                 naplan_results_div], type="cube", parent_style={"minHeight": "300px"}))
                             ]

app_usage_div = html.Div()

app_usage_dropdown = dcc.Dropdown(['BY CATEGORY', 'BY DEVELOPER', 'BY RATING'], 'BY CATEGORY',
                                  searchable=False,
                                  clearable=False)

app_usage_components = [dbc.Row([dbc.Col(html.B("APP USAGE")), dbc.Col(app_usage_dropdown)]),
                        dbc.Row(MyLoading(children=[
                            app_usage_div], type="cube", parent_style={"minHeight": "300px"}))
                        ]

most_popular_apps_div = html.Div()

most_popular_apps_dropdown = dcc.Dropdown(['BY ALL USAGE', 'BY SCHOOL TIME USAGE', 'BY OUTSIDE SCHOOL TIME USAGE'],
                                          'BY ALL USAGE',
                                          searchable=False,
                                          clearable=False)

most_popular_apps_components = [dbc.Row([dbc.Col(html.B("MOST POPULAR APPS")), dbc.Col(most_popular_apps_dropdown)]),
                                dbc.Row([dbc.Col(MyLoading(children=[most_popular_apps_div], type="cube", parent_style={"minHeight": "300px"}))])]

layout = html.Div(
    location_filters_html +
    [dbc.Row(html.P("Please select an aggregation type", style={"text-align": "center", "marginTop": "14px"}),
             id="select-aggregation-type"),
     dbc.Row([dbc.Row(app_usage_components), dbc.Row(most_popular_apps_components),
              dbc.Row(naplan_results_components)], style={"marginTop": "14px", "display": "none"}, id="graph-body")])
