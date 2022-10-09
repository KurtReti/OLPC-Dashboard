from dash import Input, Output, html
from sqlalchemy import distinct
from dash import dcc
import dash_bootstrap_components as dbc
from app import app
from apps.db_models.school import School
from apps.utils.loader import MyLoading
from database import Session


def create_location_filters(custom_filter=None):
    """
    Creates the location filters, dropdowns and associated callbacks
    :param custom_filter: A SQLAlchemy BooleanExpression that filters each query
    :return: a tuple containing states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown, location_filters_html, set_state_options, set_suburbs_options, set_postcode_options, apply_location_filters
    """
    states_dropdown = dcc.Dropdown(placeholder='ALL', value='ALL', className="states-dropdown", clearable=False)
    suburbs_dropdown = dcc.Dropdown(placeholder='ALL', value='ALL', className="suburbs-dropdown", clearable=False)
    postcodes_dropdown = dcc.Dropdown(placeholder='ALL', value='ALL', className="postcodes-dropdown", clearable=False)
    schools_dropdown = dcc.Dropdown(placeholder='ALL', value='ALL', className="schools-dropdown", clearable=False)

    location_filters_html = [
        dbc.Row([dbc.Col([html.Div("STATE", className="filter-menu-header"), html.Div(MyLoading(children=[states_dropdown], type="circle"), className="filter-menu-dropdown")], style={"padding": 0}, md=12, lg=3),
                 dbc.Col([html.Div("SUBURB", className="filter-menu-header"), html.Div(MyLoading(children=[suburbs_dropdown], type="circle"), className="filter-menu-dropdown")], style={"padding": 0}, md=12, lg=3),
                 dbc.Col([html.Div("POSTCODE", className="filter-menu-header"), html.Div(MyLoading(children=[postcodes_dropdown], type="circle"), className="filter-menu-dropdown")], style={"padding": 0}, md=12, lg=3),
                 dbc.Col([html.Div("SCHOOL", className="filter-menu-header"), html.Div(MyLoading(children=[schools_dropdown], type="circle"), className="filter-menu-dropdown")], style={"padding": 0}, md=12, lg=3)], className="filter-menu")]

    @app.callback(
        Output(states_dropdown, 'options'),
        Output(states_dropdown, 'value'),
        Input(states_dropdown, 'children'))
    @app.cache.memoize()
    def set_state_options(_):
        """
        Callback to set the states dropdown values
        :param _: dummy parameter
        :return: tuple of list of options and and default value
        """
        with Session() as session:
            base_query = session.query(distinct(School.state))
            if custom_filter is not None:
                base_query = base_query.filter(custom_filter)
            base_query = base_query.order_by(School.state)
            return ["ALL"] + [d[0] for d in base_query], "ALL"

    @app.callback(
        Output(suburbs_dropdown, 'options'),
        Output(suburbs_dropdown, 'value'),
        Input(states_dropdown, 'value'))
    @app.cache.memoize()
    def set_suburbs_options(selected_state):
        """
        Callback to set suburbs options
        :param selected_state:
        :return:  a tuple of suburbs and default value
        """
        with Session() as session:
            base_query = session.query(School.suburb, School.state)
            if custom_filter is not None:
                base_query = base_query.filter(custom_filter)
            base_query = base_query.group_by(School.suburb, School.state).order_by(
                School.suburb, School.state)

            if selected_state == "ALL":
                return [{"label": "ALL", "value": "ALL"}] + [
                    {"label": f"{d[0]} ({d[1]})", "value": d[0] + "||||" + d[1]}
                    for d in base_query], "ALL"
            else:
                return ["ALL"] + [d[0] for d in base_query.filter(School.state == selected_state)], "ALL"

    @app.callback(
        Output(postcodes_dropdown, 'options'),
        Output(postcodes_dropdown, 'value'),
        Input(states_dropdown, 'value'),
        Input(suburbs_dropdown, 'value'))
    @app.cache.memoize()
    def set_postcode_options(selected_state, selected_suburb):
        """
        Callback to set the postcode options
        :param selected_state: string
        :param selected_suburb: string
        :return: tuple of suburb options and default value
        """
        with Session() as session:
            base_query = session.query(distinct(School.postcode)).order_by(School.postcode)
            if custom_filter is not None:
                base_query = base_query.filter(custom_filter)
            if selected_state == "ALL" and selected_suburb == "ALL":
                pass
            elif selected_state == "ALL" and selected_suburb != "ALL":
                suburb, state = selected_suburb.split("||||")
                base_query = base_query.filter(School.state == state).filter(School.suburb == suburb)
            elif selected_state != "ALL" and selected_suburb == "ALL":
                base_query = base_query.filter(School.state == selected_state)
            else:
                base_query = base_query.filter(School.state == selected_state).filter(School.suburb == selected_suburb)
            return ["ALL"] + [d[0] for d in base_query], "ALL"

    @app.callback(
        Output(schools_dropdown, 'options'),
        Output(schools_dropdown, 'value'),
        Input(states_dropdown, 'value'),
        Input(suburbs_dropdown, 'value'),
        Input(postcodes_dropdown, 'value'))
    @app.cache.memoize()
    def set_schools_options(selected_state, selected_suburb, selected_postcode):
        """
        Callback to set schools options
        :param selected_state: string
        :param selected_suburb: string
        :param selected_postcode: string
        :return: tuple of list of schools options and default value
        """
        with Session() as session:
            base_query = session.query(School.school_name, School.id).order_by(School.school_name)
            if custom_filter is not None:
                base_query = base_query.filter(custom_filter)
            if selected_state == "ALL" and selected_suburb == "ALL" and selected_postcode == "ALL":
                pass
            elif selected_state == "ALL" and selected_suburb == "ALL" and selected_postcode != "ALL":
                base_query = base_query.filter(School.postcode == selected_postcode)
            elif selected_state == "ALL" and selected_suburb != "ALL" and selected_postcode == "ALL":
                suburb, state = selected_suburb.split("||||")
                base_query = base_query.filter(School.state == state).filter(School.suburb == suburb)
            elif selected_state != "ALL" and selected_suburb == "ALL" and selected_postcode == "ALL":
                base_query = base_query.filter(School.state == selected_state)
            elif selected_state != "ALL" and selected_suburb != "ALL" and selected_postcode == "ALL":
                base_query = base_query.filter(School.state == selected_state).filter(School.suburb == selected_suburb)
            elif selected_state != "ALL" and selected_suburb != "ALL" and selected_postcode != "ALL":
                base_query = base_query.filter(School.state == selected_state).filter(
                    School.suburb == selected_suburb).filter(School.postcode == selected_postcode)
            elif selected_state == "ALL" and selected_suburb != "ALL" and selected_postcode != "ALL":
                suburb, state = selected_suburb.split("||||")
                base_query = base_query.filter(School.state == state).filter(School.suburb == suburb).filter(
                    School.postcode == selected_postcode)
            elif selected_state != "ALL" and selected_suburb == "ALL" and selected_postcode != "ALL":
                base_query = base_query.filter(School.state == selected_state).filter(
                    School.postcode == selected_postcode)
            return [{"label": "ALL", "value": "ALL"}] + [{"label": d[0], "value": d[1]} for d in base_query], "ALL"

    def apply_location_filters(query, selected_state, selected_suburb, selected_postcode, selected_school):
        """
        Function to transform query by selected filters
        :param query: SQLAlchemy Query
        :param selected_state: string
        :param selected_suburb: string
        :param selected_postcode: string
        :param selected_school: string
        :return: SQLAlchemy Query
        """
        if selected_state == "ALL" and selected_suburb == "ALL" and selected_postcode == "ALL" and selected_school == "ALL":
            pass
        elif selected_school != "ALL":
            query = query.filter(School.id == selected_school)
        elif selected_state == "ALL" and selected_suburb != "ALL" and selected_postcode == "ALL":
            suburb, state = selected_suburb.split("||||")
            query = query.filter(School.state == state).filter(School.suburb == suburb)
        elif selected_state != "ALL" and selected_suburb == "ALL" and selected_postcode == "ALL":
            query = query.filter(School.state == selected_state)
        elif selected_state != "ALL" and selected_suburb != "ALL" and selected_postcode == "ALL":
            query = query.filter(School.state == selected_state).filter(School.suburb == selected_suburb)
        elif selected_state != "ALL" and selected_suburb != "ALL" and selected_postcode != "ALL":
            query = query.filter(School.state == selected_state).filter(School.suburb == selected_suburb).filter(
                School.postcode == selected_postcode)
        elif selected_state == "ALL" and selected_suburb == "ALL" and selected_postcode != "ALL":
            query = query.filter(School.postcode == selected_postcode)
        elif selected_state == "ALL" and selected_suburb != "ALL" and selected_postcode != "ALL":
            suburb, state = selected_suburb.split("||||")
            query = query.filter(School.state == state).filter(School.suburb == suburb).filter(
                School.postcode == selected_postcode)
        elif selected_state != "ALL" and selected_suburb == "ALL" and selected_postcode != "ALL":
            query = query.filter(School.state == selected_state).filter(School.postcode == selected_postcode)
        return query

    return states_dropdown, suburbs_dropdown, postcodes_dropdown, schools_dropdown, location_filters_html, set_state_options, set_suburbs_options, set_postcode_options, apply_location_filters
