import dash
import pandas as pd
from dash import dcc, html

from apps.layouts.compare import compare_by_options_funcs, naplan_results_div, app_usage_dropdown, app_usage_div, \
    most_popular_apps_dropdown, most_popular_apps_div
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, ALL, State

from sqlalchemy.sql.functions import concat

from app import app

from apps.db_models.school import School
from apps.callbacks.common import location_filtered_callback
from apps.layouts.graphs import Graphs
from apps.queries.compare import most_popular_apps_figure_query_school, most_popular_apps_figure_query_suburb, \
    most_popular_apps_figure_query_state, app_usage_figure_df_school, app_usage_figure_df_postcode, \
    app_usage_figure_df_suburb, app_usage_figure_df_state, naplan_results_figure_df_state, \
    naplan_results_figure_df_suburb, naplan_results_figure_df_school, naplan_results_figure_df_postcode, \
    most_popular_apps_figure_query_postcode
from apps.utils.database import query_for_df
from apps.utils.loader import MyLoading
from apps.utils.transform import grouper
from database import Session


@app.callback(
    Output("filter_dropdowns", 'children'),
    Output("graph-body", 'style'),
    Output("select-aggregation-type", 'style'),
    Input("compare_by", 'value'))
@app.cache.memoize()
def set_compare_by(value):
    """
        Sets the school, postcode, suburb or state dropdown components
        :param value: string
        :return tuple of list of dash Components, dict, dict
    """
    if not value:
        return dash.no_update

    if value not in ['SCHOOL', 'POSTCODE', 'SUBURB', 'STATE']:
        raise Exception("value must be postcode, school, state or suburb")

    options = compare_by_options_funcs[value]()

    return [
               dbc.Col(MyLoading(children=[dcc.Dropdown(id={'type': f'dynamic-{value.lower()}-dropdown', 'index': i},
                                                          placeholder=f'Select {value.title()} {i + 1}',
                                                          options=options, optionHeight=45)], type="circle"), style={"padding": 0}, md=12, lg=3, className="filter-menu-dropdown") for i
               in range(0, 4)], {"display": "block", "marginTop": "1rem"}, {"display": "none"}


@location_filtered_callback(
    inputs=[{'type': 'dynamic-school-dropdown', 'index': ALL}, {'type': 'dynamic-postcode-dropdown', 'index': ALL},
            {'type': 'dynamic-suburb-dropdown', 'index': ALL}, {'type': 'dynamic-state-dropdown', 'index': ALL}],
    states=[State("compare_by", "value")],
    outputs=[Output(naplan_results_div, 'children')], accessibility=True, prevent_initial_call=True)
@app.cache.memoize()
def naplan_results_figure_update(schools, postcodes, suburbs, states,
                                 text_size, text_font, colourblind_mode, dark_mode, compare_by):
    """
    Generates the naplan results figure based on parameters
    :param schools: list of school ids
    :param postcodes: list of postcodes
    :param suburbs: list of suburbs
    :param states: list of states
    :param text_size: integer
    :param text_font: string
    :param colourblind_mode:
    :param dark_mode: boolean
    :param compare_by: string
    :return: dbc component
    """
    df = None
    comparator = None
    # check if any of the dropdowns have value set
    if any(x is not None for x in schools):
        df = naplan_results_figure_df_school(*filter(lambda x: x is not None, schools))
        comparator = "School"
    elif any(x is not None for x in postcodes):
        comparator = "Postcode"
        df = naplan_results_figure_df_postcode(*filter(lambda x: x is not None, postcodes))
    elif any(x is not None for x in suburbs):
        comparator = "Suburb"
        df = naplan_results_figure_df_suburb(*filter(lambda x: x is not None, suburbs))
    elif any(x is not None for x in states):
        comparator = "State"
        df = naplan_results_figure_df_state(*filter(lambda x: x is not None, states))

    if comparator:
        if df.empty:
            return Graphs.no_data()
        figures = []
        for group_name, group in df.groupby("Subject"):
            naplan_results_figure = Graphs.bar(data_frame=group, x="Grade", y="Naplan Score",
                                               color=comparator, barmode='group',
                                               text_size=text_size,
                                               text_font=text_font,
                                               colourblind_mode=colourblind_mode,
                                               dark_mode=dark_mode,
                                               export_button=True,
                                               export_filename="naplan_results",
                                               update_layout={"title": group.iloc[0]["Subject"],
                                                              "legend": dict(yanchor="top", y=0.9, xanchor="left",
                                                                             x=0.4, bgcolor="#FFFFFF", font_color="#000000")})
            figures.append(naplan_results_figure)
        return [dbc.Row([dbc.Col(c, md=12, lg=6) for c in chunk]) for chunk in grouper(figures, 2)]
    else:
        return html.B(f"Please select comparison {compare_by.lower()}s")


@location_filtered_callback(
    inputs=[{'type': 'dynamic-school-dropdown', 'index': ALL}, {'type': 'dynamic-postcode-dropdown', 'index': ALL},
            {'type': 'dynamic-suburb-dropdown', 'index': ALL}, {'type': 'dynamic-state-dropdown', 'index': ALL},
            app_usage_dropdown],
    states=[State("compare_by", "value")],
    outputs=[Output(app_usage_div, 'children')], accessibility=True, prevent_initial_call=True)
@app.cache.memoize()
def app_usage_figure_update(schools, postcodes, suburbs, states, graph_filter,
                            text_size, text_font, colourblind_mode, dark_mode, compare_by):
    """
    Generates the app usage figure based on parameters
    :param schools: list of school ids
    :param postcodes: list of postcodes
    :param suburbs: list of suburbs
    :param states: list of states
    :param graph_filter: string
    :param text_size: integer
    :param text_font: string
    :param colourblind_mode:
    :param dark_mode: boolean
    :param compare_by: string
    :return: dbc component
    """

    xtitle = None
    if graph_filter == "BY CATEGORY":
        xtitle = "Category"
    elif graph_filter == "BY DEVELOPER":
        xtitle = "Developer"
    elif graph_filter == "BY RATING":
        xtitle = "Rating"

    df = None
    comparator = None
    if any(x is not None for x in schools):
        df = app_usage_figure_df_school(graph_filter, *filter(lambda x: x is not None, schools))
        comparator = "School"
    elif any(x is not None for x in postcodes):
        comparator = "Postcode"
        df = app_usage_figure_df_postcode(graph_filter, *filter(lambda x: x is not None, postcodes))
    elif any(x is not None for x in suburbs):
        comparator = "Suburb"
        df = app_usage_figure_df_suburb(graph_filter, *filter(lambda x: x is not None, suburbs))
    elif any(x is not None for x in states):
        comparator = "State"
        df = app_usage_figure_df_state(graph_filter, *filter(lambda x: x is not None, states))
    if comparator:
        if df.empty or len(df) == 1:
            return Graphs.no_data()
        groups = []
        df["xaxis"] = df["xaxis"].astype(str)
        for group_name, group in df.groupby(comparator):
            groups.append(group.iloc[0:5])
            groups.append(pd.DataFrame(
                [{"avg": df["avg"].iloc[5:].mean(), "xaxis": "Others", comparator: group.iloc[0][comparator]}]))
        df = pd.concat(groups)
        app_usage_figure = Graphs.bar(data_frame=df, x="xaxis", y="avg", color=comparator,
                                      labels={"xaxis": xtitle, comparator: comparator},
                                      barmode="group",
                                      text_size=text_size,
                                      text_font=text_font,
                                      colourblind_mode=colourblind_mode,
                                      dark_mode=dark_mode,
                                      export_button=True,
                                      export_filename="app_usage",
                                      update_layout={"yaxis": {"title": 'App Usage (mins/session)'},
                                                     "xaxis": {"title": xtitle},
                                                     "legend": dict(yanchor="top", y=0.9, xanchor="left",
                                                                    x=0.4, bgcolor="#FFFFFF", font_color="#000000")}
                                      )
        return dbc.Row(app_usage_figure)
    return html.B(f"Please select comparison {compare_by.lower()}s")


@location_filtered_callback(
    inputs=[most_popular_apps_dropdown,
            {'type': 'dynamic-school-dropdown', 'index': ALL}, {'type': 'dynamic-postcode-dropdown', 'index': ALL},
            {'type': 'dynamic-suburb-dropdown', 'index': ALL}, {'type': 'dynamic-state-dropdown', 'index': ALL}],
    states=[State("compare_by", "value")],
    outputs=[Output(most_popular_apps_div, 'children')],
    accessibility=True, prevent_initial_call=True)
@app.cache.memoize()
def most_popular_apps_figure_update(graph_filter, schools, postcodes, suburbs, states,
                                    text_size, text_font, colourblind_mode, dark_mode, compare_by):
    """
    Generates the most popular apps usage figure based on parameters
    :param graph_filter: string
    :param schools: list of school ids
    :param postcodes: list of postcodes
    :param suburbs: list of suburbs
    :param states: list of states
    :param text_size: integer
    :param text_font: string
    :param colourblind_mode:
    :param dark_mode: boolean
    :param compare_by: string
    :return: dbc component
    """
    values = []
    figures = []
    comparator = None
    query_func = None
    if any(x is not None for x in schools):
        values = filter(lambda x: x is not None, schools)
        comparator = "School"
        query_func = most_popular_apps_figure_query_school
    elif any(x is not None for x in postcodes):
        values = filter(lambda x: x is not None, postcodes)
        comparator = "Postcode"
        query_func = most_popular_apps_figure_query_postcode
    elif any(x is not None for x in suburbs):
        values = filter(lambda x: x is not None, suburbs)
        comparator = "Suburb"
        query_func = most_popular_apps_figure_query_suburb
    elif any(x is not None for x in states):
        values = filter(lambda x: x is not None, states)
        comparator = "State"
        query_func = most_popular_apps_figure_query_state

    if comparator:
        for value in values:
            base_query = query_func(graph_filter, value)
            df = query_for_df(base_query)
            if df.empty:
                figures.append(Graphs.no_data())
            df = pd.concat([df.iloc[0:7], pd.DataFrame([{"total": df["total"].iloc[7:].sum(), "appName": "Others"}])])

            if comparator == "School":
                with Session() as session:
                    data = session.query(concat(School.school_name, " (", School.postcode, ")")).filter(
                        School.id == value).limit(1)
                    value = data[0][0]
            if comparator == "Suburb":
                value = value.replace("||||", " - ")
            most_popular_apps_figure = Graphs.pie(data_frame=df, names="appName", values="total",
                                                  text_size=text_size,
                                                  text_font=text_font,
                                                  colourblind_mode=colourblind_mode,
                                                  dark_mode=dark_mode,
                                                  update_layout={"title": f"{comparator}: {value}"},
                                                  export_button=True,
                                                  export_filename="most_popular_apps"
                                                  )
            figures.append(most_popular_apps_figure)

    if figures:
        return [dbc.Row([dbc.Col(c, md=12, lg=6) for c in chunk]) for chunk in grouper(figures, 2)]
    else:
        return html.B(f"Please select comparison {compare_by.lower()}s")
