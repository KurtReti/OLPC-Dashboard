from dash import Output

from app import app
from apps.callbacks.common import location_filtered_callback
from apps.layouts.apps import app_usage_dropdown, states_dropdown, suburbs_dropdown, postcodes_dropdown, \
    schools_dropdown, date_slider, app_usage_div, apply_location_filters, most_popular_apps_dropdown, \
    most_popular_apps_div, usage_of_apps_by_location_dropdown, usage_of_apps_by_location_div
from apps.layouts.graphs import Graphs
from apps.queries.apps import usage_of_apps_by_location_figure_df, app_usage_figure_df, most_popular_apps_figure_df
from apps.utils.decorators import apply_location_filters_decorator, apply_date_filter_decorator


@location_filtered_callback(
    inputs=[app_usage_dropdown, states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown, date_slider],
    outputs=[Output(app_usage_div, 'children')], accessibility=True)
@app.cache.memoize()
def app_usage_figure_update(graph_filter, selected_state, selected_suburb, selected_postcode, selected_school,
                            selected_date_range,
                            text_size, text_font, colourblind_mode, dark_mode):
    """
    Update the app usage figure based on the parameters
    :param graph_filter: string
    :param selected_state: string
    :param selected_suburb: string
    :param selected_postcode: string
    :param selected_school: string
    :param selected_date_range: tuple
    :param text_size: int
    :param text_font: string
    :param colourblind_mode: boolean
    :param dark_mode: boolean
    :return: dash Figure
    """
    xtitle = None
    if graph_filter == "BY CATEGORY":
        xtitle = "Category"
    elif graph_filter == "BY DEVELOPER":
        xtitle = "Developer"
    elif graph_filter == "BY RATING":
        xtitle = "Rating"
    location_filters = apply_location_filters_decorator(apply_location_filters, selected_state, selected_suburb,
                                                        selected_postcode,
                                                        selected_school)

    df = app_usage_figure_df(graph_filter, location_filters, apply_date_filter_decorator(selected_date_range))
    if len(df) == 1:
        return Graphs.no_data()

    app_usage_figure = Graphs.bar(data_frame=df, x="xaxis", y="avg", color="xaxis", labels={"xaxis": xtitle},
                                  update_layout={"yaxis": {"title": 'App Usage (mins/session)'},
                                                 "xaxis": {"title": xtitle}},
                                  text_size=text_size,
                                  text_font=text_font,
                                  colourblind_mode=colourblind_mode,
                                  dark_mode=dark_mode,
                                  export_button=True,
                                  export_filename="app_usage"
                                  )
    return app_usage_figure


@location_filtered_callback(
    inputs=[most_popular_apps_dropdown, states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown,
            date_slider],
    outputs=[Output(most_popular_apps_div, 'children')], accessibility=True, prevent_initial_call=True)
@app.cache.memoize()
def most_popular_apps_figure_update(graph_filter, selected_state, selected_suburb, selected_postcode, selected_school,
                                    selected_date_range,
                                    text_size, text_font, colourblind_mode, dark_mode):
    """
    Update the most popular apps figure based on parameters
    :param graph_filter: string
    :param selected_state: string
    :param selected_suburb: string
    :param selected_postcode: string
    :param selected_school: string
    :param selected_date_range: tuple
    :param text_size: int
    :param text_font: string
    :param colourblind_mode: boolean
    :param dark_mode: boolean
    :return: dash Figure
    """
    location_filters = apply_location_filters_decorator(apply_location_filters, selected_state, selected_suburb,
                                                        selected_postcode,
                                                        selected_school)
    df = most_popular_apps_figure_df(graph_filter, location_filters, apply_date_filter_decorator(selected_date_range))
    if len(df) == 1:
        return Graphs.no_data()
    most_popular_apps_figure = Graphs.pie(data_frame=df, names="appName", values="total", text_size=text_size,
                                          text_font=text_font,
                                          colourblind_mode=colourblind_mode,
                                          dark_mode=dark_mode,
                                          export_button=True,
                                          export_filename="most_popular_apps")

    return most_popular_apps_figure


@location_filtered_callback(
    inputs=[usage_of_apps_by_location_dropdown, states_dropdown, suburbs_dropdown, postcodes_dropdown,
            schools_dropdown, date_slider], outputs=[Output(usage_of_apps_by_location_div, 'children')],
    accessibility=True)
@app.cache.memoize()
def usage_of_apps_by_location_figure_update(graph_filter, selected_state, selected_suburb, selected_postcode,
                                            selected_school, selected_date_range, text_size, text_font,
                                            colourblind_mode, dark_mode):
    """
    Update the usage of apps by location figure based on parameters
    :param graph_filter: string
    :param selected_state: string
    :param selected_suburb: string
    :param selected_postcode: string
    :param selected_school: string
    :param selected_date_range: tuple
    :param text_size: int
    :param text_font: string
    :param colourblind_mode: boolean
    :param dark_mode: boolean
    :return: dash Figure
    """
    location_filters = apply_location_filters_decorator(apply_location_filters, selected_state, selected_suburb,
                                                        selected_postcode,
                                                        selected_school)

    df = usage_of_apps_by_location_figure_df(graph_filter, location_filters,
                                             apply_date_filter_decorator(selected_date_range))

    usage_of_apps_by_location_figure = Graphs.scatter_mapbox(data_frame=df, lat="latitude", lon="longitude",
                                                             color="duration (hours)", hover_name="school_name",
                                                             zoom=2.5,
                                                             center={"lat": -26.84673174970853,
                                                                     "lon": 134.8500249708139},
                                                             text_size=text_size,
                                                             text_font=text_font,
                                                             colourblind_mode=colourblind_mode,
                                                             dark_mode=dark_mode,
                                                             export_button=True,
                                                             export_filename="usage_of_apps_by_location")

    return usage_of_apps_by_location_figure
