import dash
from dash import Output

from app import app
from apps.callbacks.common import location_filtered_callback
from apps.layouts.graphs import Graphs
from apps.layouts.naplan import apply_location_filters, naplan_results_div, naplan_results_dropdown, suburbs_dropdown, \
    states_dropdown, postcodes_dropdown, schools_dropdown, highest_naplan_score_div, highest_naplan_score_title, \
    number_of_schools_div, number_of_schools_title, total_number_of_tests_div, total_number_of_tests_title
from apps.queries.naplan import naplan_results_figure_df, highest_naplan_score_update_df, school_type, \
    total_number_of_schools, school_sector, total_number_of_tests_df
from apps.utils.decorators import apply_location_filters_decorator


@location_filtered_callback(inputs=[states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown],
                            outputs=[Output(number_of_schools_div, 'children'),
                                     Output(number_of_schools_title, 'children')])
@app.cache.memoize()
def number_of_schools_or_school_sector_update(selected_state, selected_suburb, selected_postcode,
                                              selected_school):
    """
    Callback to update the number of schools or school sector
    :param selected_state: string
    :param selected_suburb: string
    :param selected_postcode: string
    :param selected_school: string
    :return: tuple of string, string
    """
    location_filters = apply_location_filters_decorator(apply_location_filters, selected_state, selected_suburb,
                                                        selected_postcode, selected_school)

    if selected_school != "ALL":
        return school_sector(location_filters), "SCHOOL SECTOR"

    return total_number_of_schools(location_filters), "TOTAL NUMBER OF SCHOOLS"


@location_filtered_callback(inputs=[states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown],
                            outputs=[Output(total_number_of_tests_div, 'children'),
                                     Output(total_number_of_tests_title, 'children')])
@app.cache.memoize()
def total_number_of_tests_update(selected_state, selected_suburb, selected_postcode,
                                 selected_school):
    """
    Callback to update the number of tests
    :param selected_state: string
    :param selected_suburb: string
    :param selected_postcode: string
    :param selected_school: string
    :return: tuple of string, string
    """
    location_filters = apply_location_filters_decorator(apply_location_filters, selected_state, selected_suburb,
                                                        selected_postcode, selected_school)

    return total_number_of_tests_df(location_filters), "TOTAL NUMBER OF TESTS"


@location_filtered_callback(inputs=[states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown],
                            outputs=[Output(highest_naplan_score_div, 'children'),
                                     Output(highest_naplan_score_title, 'children')])
@app.cache.memoize()
def highest_naplan_score_or_school_type_update(selected_state, selected_suburb, selected_postcode,
                                               selected_school):
    """
    Callback for the highest naplan score or school type
    :param selected_state: string
    :param selected_suburb: string
    :param selected_postcode: string
    :param selected_school: string
    :return: tuple of string, string
    """
    location_filters = apply_location_filters_decorator(apply_location_filters, selected_state, selected_suburb,
                                                        selected_postcode, selected_school)

    if selected_school != "ALL":
        return school_type(location_filters), "SCHOOL TYPE"

    return highest_naplan_score_update_df(location_filters), "HIGHEST NAPLAN SCORE"


@location_filtered_callback(
    inputs=[naplan_results_dropdown, states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown],
    outputs=[Output(naplan_results_div, 'children'), Output(naplan_results_dropdown, 'style')], accessibility=True,
    prevent_initial_call=True)
@app.cache.memoize()
def naplan_results_figure_update(graph_filter, selected_state, selected_suburb, selected_postcode, selected_school,
                                 text_size, text_font, colourblind_mode, dark_mode):
    """
    Callback to update the naplan results figure based on the location and accessibility parameters
    :param graph_filter: string
    :param selected_state: string
    :param selected_suburb: string
    :param selected_postcode: string
    :param selected_school: string
    :param text_size: int
    :param text_font: string
    :param colourblind_mode: boolean
    :param dark_mode: boolean
    :return: tuple of Dash Figure, dict
    """
    location_filters = apply_location_filters_decorator(apply_location_filters, selected_state, selected_suburb,
                                                        selected_postcode, selected_school)

    dropdown_style = {"visibility": "visible"}
    if selected_school != "ALL":
        dropdown_style = {"visibility": "hidden"}
    if graph_filter == 'ALL SCHOOLS':
        xtitle = "ALL SCHOOLS"
    elif graph_filter == 'GOVERNMENT':
        xtitle = "GOVERNMENT"
    elif graph_filter == 'CATHOLIC':
        xtitle = "CATHOLIC"
    elif graph_filter == 'INDEPENDENT':
        xtitle = "INDEPENDENT"

    df = naplan_results_figure_df(graph_filter, location_filters)

    if df.empty:
        return Graphs.no_data(), dash.no_update

    naplan_results_figure = Graphs.histogram(data_frame=df, x="xaxis", y="avg",
                                             color='grade', barmode='group',
                                             update_layout={"yaxis": {"title": 'Naplan Score'},
                                                            "xaxis": {"title": xtitle}},
                                             text_size=text_size,
                                             text_font=text_font,
                                             colourblind_mode=colourblind_mode,
                                             dark_mode=dark_mode,
                                             export_button=True,
                                             export_filename="naplan_results")

    return naplan_results_figure, dropdown_style
