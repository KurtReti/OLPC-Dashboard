from dash import Output

from app import app
from apps.callbacks.common import location_filtered_callback
from apps.layouts.devices import states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown, \
    total_number_devices_div, total_number_devices_title, apply_location_filters, \
    avg_number_of_devices_per_school_or_school_type_div, avg_number_of_devices_per_school_or_school_type_title, \
    school_with_most_devices_or_school_sector_devices, school_with_most_devices_or_school_sector_title, \
    devices_by_location_dropdown, devices_by_location_div
from apps.layouts.graphs import Graphs
from apps.utils.decorators import apply_location_filters_decorator
from apps.queries.devices import devices_by_location_figure_df, total_number_of_devices_df, school_type_df, \
    avg_number_of_devices_per_school_df, school_sector_df, school_with_most_devices_df


@location_filtered_callback(inputs=[states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown],
                            outputs=[Output(total_number_devices_div, 'children'),
                                     Output(total_number_devices_title, 'children')])
@app.cache.memoize()
def total_number_of_devices_update(selected_state, selected_suburb, selected_postcode, selected_school):
    """
    Get the total number of devices by filter parameters and update the dash components
    :param selected_state: string
    :param selected_suburb: string
    :param selected_postcode: string
    :param selected_school: string
    :return: tuple of string, string
    """
    total_devices = total_number_of_devices_df(
        apply_location_filters_decorator(apply_location_filters, selected_state, selected_suburb, selected_postcode,
                                         selected_school))

    return total_devices, "TOTAL NUMBER OF DEVICES"


@location_filtered_callback(inputs=[states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown],
                            outputs=[Output(avg_number_of_devices_per_school_or_school_type_div, 'children'),
                                     Output(avg_number_of_devices_per_school_or_school_type_title, 'children')])
@app.cache.memoize()
def avg_number_of_devices_per_school_or_school_type_update(selected_state, selected_suburb, selected_postcode,
                                                           selected_school):
    """
    Gets the average devices per school or school type by filter parameters and updates the dash components
    :param selected_state: string
    :param selected_suburb: string
    :param selected_postcode: string
    :param selected_school: string
    :return: tuple of string, string
    """
    location_filters = apply_location_filters_decorator(apply_location_filters, selected_state, selected_suburb,
                                                        selected_postcode, selected_school)

    if selected_school != "ALL":
        return school_type_df(location_filters), "SCHOOL TYPE"
    else:
        return avg_number_of_devices_per_school_df(location_filters), "AVERAGE NO. OF DEVICES PER SCHOOL"


@location_filtered_callback(inputs=[states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown],
                            outputs=[Output(school_with_most_devices_or_school_sector_devices, 'children'),
                                     Output(school_with_most_devices_or_school_sector_title, 'children')])
@app.cache.memoize()
def school_with_most_devices_or_school_sector_update(selected_state, selected_suburb, selected_postcode,
                                                     selected_school):
    """
    Gets the school with most devices or school sector and updates the dash components
    :param selected_state: string
    :param selected_suburb: string
    :param selected_postcode: string
    :param selected_school: string
    :return: tuple of string, string
    """
    location_filters = apply_location_filters_decorator(apply_location_filters, selected_state, selected_suburb,
                                                        selected_postcode, selected_school)
    if selected_school != "ALL":
        return school_sector_df(location_filters), "SCHOOL SECTOR"
    else:
        return school_with_most_devices_df(location_filters), "SCHOOL WITH MOST NUMBER OF DEVICES"


@location_filtered_callback(
    inputs=[devices_by_location_dropdown, states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown],
    outputs=[Output(devices_by_location_div, 'children')], accessibility=True, prevent_initial_call=True)
@app.cache.memoize()
def devices_by_location_figure_update(graph_filter, selected_state, selected_suburb, selected_postcode,
                                      selected_school, text_size, text_font, colourblind_mode, dark_mode):
    """
    Get the devices by location and updates the dash components
    :param graph_filter: string
    :param selected_state: string
    :param selected_suburb: string
    :param selected_postcode: string
    :param selected_school: string
    :param text_size: int
    :param text_font: string
    :param colourblind_mode: boolean
    :param dark_mode: boolean
    :return: dash Figure
    """
    df = devices_by_location_figure_df(graph_filter,
                                       apply_location_filters_decorator(apply_location_filters, selected_state,
                                                                        selected_suburb, selected_postcode,
                                                                        selected_school))

    if df.empty:
        return Graphs.no_data()

    # center of australia {"lat": -26.84673174970853, "lon": 134.8500249708139}
    devices_by_location_figure = Graphs.scatter_mapbox(data_frame=df, lat="latitude", lon="longitude",
                                                       color="total", hover_name="school_name",
                                                       zoom=2.5,
                                                       center={"lat": -26.84673174970853,
                                                               "lon": 134.8500249708139},
                                                       text_size=text_size,
                                                       text_font=text_font,
                                                       colourblind_mode=colourblind_mode,
                                                       dark_mode=dark_mode,
                                                       export_button=True,
                                                       export_filename="devices_by_location")
    return devices_by_location_figure
