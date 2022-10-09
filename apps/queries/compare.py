from sqlalchemy import select, desc, and_, or_, distinct, exists
from sqlalchemy.orm import aliased
from sqlalchemy.sql.functions import concat, func

from app import app
from apps.db_models.account import Account
from apps.db_models.activity import Activity
from apps.db_models.app import App
from apps.db_models.app_category_association import AppCategoryAssociation
from apps.db_models.category import Category
from apps.db_models.developer import Developer
from apps.db_models.device import Device
from apps.db_models.device_ownership import DeviceOwnership
from apps.db_models.naplan import Naplan
from apps.db_models.school import School
from apps.utils.decorators import apply_filter_decorator, apply_filters
from apps.utils.database import hour, query_for_df
from database import Session


@app.cache.memoize()
def get_postcode_options():
    """
    Get distinct postcodes where Naplan and Activity data exist
    """
    with Session() as session:
        school_alias = aliased(School)
        base_query = session.query(distinct(School.postcode)).filter(
            exists(select(Naplan.id).select_from(Naplan).join(school_alias).filter(
                school_alias.postcode == School.postcode))).filter(
            exists(select(Activity.id).select_from(Activity).join(DeviceOwnership,
                                                                  DeviceOwnership.deviceid == Activity.deviceid).join(
                Account).join(school_alias).filter(school_alias.postcode == School.postcode))).order_by(School.postcode)
        return [{"label": d[0], "value": d[0]} for d in base_query]


@app.cache.memoize()
def get_suburb_options():
    """
    Get distinct suburbs where Naplan and Activity data exist
    """
    with Session() as session:
        school_alias = aliased(School)
        base_query = session.query(School.suburb, School.state).filter(
            exists(select(Naplan.id).select_from(Naplan).join(school_alias).filter(and_(
                school_alias.suburb == School.suburb, school_alias.state == School.state)))).filter(
            exists(select(Activity.id).select_from(Activity).join(DeviceOwnership,
                                                                  DeviceOwnership.deviceid == Activity.deviceid).join(
                Account).join(school_alias).filter(and_(
                school_alias.suburb == School.suburb, school_alias.state == School.state)))).group_by(School.suburb,
                                                                                                      School.state).order_by(
            School.suburb, School.state)
        return [{"label": f'{d[0]} - {d[1]}', "value": f'{d[0]}||||{d[1]}'} for d in base_query]


@app.cache.memoize()
def get_school_options():
    """
    Get distinct schools where Naplan and Activity data exist
    """
    with Session() as session:
        school_alias = aliased(School)
        base_query = session.query(School.school_name, School.postcode, School.id).filter(
            exists(select(Naplan.id).select_from(Naplan).join(school_alias).filter(
                school_alias.id == School.id))).filter(
            exists(select(Activity.id).select_from(Activity).join(DeviceOwnership,
                                                                  DeviceOwnership.deviceid == Activity.deviceid).join(
                Account).join(school_alias).filter(school_alias.id == School.id))).group_by(School.id).order_by(
            School.school_name, School.postcode)
        return [{"label": f'{d[0]} {(d[1])}', "value": d[2]} for d in base_query]


@app.cache.memoize()
def get_state_options():
    """
        Get distinct state where Naplan and Activity data exist
    """
    with Session() as session:
        school_alias = aliased(School)
        base_query = session.query(distinct(School.state)).filter(
            exists(select(Naplan.id).select_from(Naplan).join(school_alias).filter(
                school_alias.state == School.state))).filter(
            exists(select(Activity.id).select_from(Activity).join(DeviceOwnership,
                                                                  DeviceOwnership.deviceid == Activity.deviceid).join(
                Account).join(school_alias).filter(school_alias.state == School.state))).order_by(School.state)
        return [{"label": d[0], "value": d[0]} for d in base_query]


def naplan_results_figure_df(select_, in_, *group_by):
    """
    "Query the average score, grade and subject along with select_ column grouped by group by
    :param select_: SQLAlchemy Column to select
    :param in_: SQLALchemy in clause
    :param group_by: SQLAlchemy Columns to group by
    :return: pandas dataframe
    """
    base_query = select(func.avg(Naplan.averageScore).label("Naplan Score"), Naplan.grade.label("Grade"),
                        Naplan.areaOfStudy.label("Subject"),
                        select_).select_from(
        Naplan).join(School).where(in_).group_by(*group_by, Naplan.grade, Naplan.areaOfStudy)
    return query_for_df(base_query)


def naplan_results_figure_df_school(*schools):
    """
    Call naplan_results_figure_df with parameters for school
    :param schools: list of schools
    :return: pandas dataframe
    """
    return naplan_results_figure_df(concat(School.school_name, " (", School.postcode, ")").label("School"),
                                    School.id.in_(schools), School.id)


def naplan_results_figure_df_postcode(*postcodes):
    """
    Call naplan_results_figure_df with parameters for postcode
    :param postcodes: list of postcodes
    :return: pandas dataframe
    """
    return naplan_results_figure_df(School.postcode.label("Postcode"), School.postcode.in_(postcodes), School.postcode)


def naplan_results_figure_df_suburb(*suburbs):
    """
    Call naplan_results_figure_df with parameters for suburbs
    :param suburbs: list of suburbs
    :return: pandas dataframe
    """
    return naplan_results_figure_df(concat(School.suburb, " - ", School.state).label("Suburb"),
                                    concat(School.suburb, "||||", School.state).in_(suburbs), School.suburb,
                                    School.state)


def naplan_results_figure_df_state(*states):
    """
    Call naplan_results_figure_df with parameters for states
    :param states: list of states
    :return: pandas dataframe
    """
    return naplan_results_figure_df(School.state.label("State"), School.state.in_(states), School.state)


def app_usage_figure_df(graph_filter, select_, in_, *group_by):
    """
    Queries the avg usage by duration for a school
    :param graph_filter: string
    :param select_: SQLAlchemy column to select
    :param in_: SQLAlchemy in
    :param group_by: columns to group by
    :return: pandas dataframe
    """
    avg = func.avg(Activity.duration / 60).label("avg")
    if graph_filter == "BY CATEGORY":
        xaxis = Category.name.label("xaxis")
        base_query = select(avg, xaxis,
                            select_).select_from(
            DeviceOwnership).join(Account).join(School).join(Device).join(Activity).join(AppCategoryAssociation,
                                                                                         AppCategoryAssociation.appid == Activity.appid).join(
            Category).where(
            in_).group_by(
            *group_by, Category.id).order_by(desc(avg))
    elif graph_filter == "BY DEVELOPER":
        xaxis = Developer.name.label("xaxis")
        base_query = select(avg, xaxis, select_).select_from(
            DeviceOwnership).join(Account).join(School).join(Device).join(Activity).join(App,
                                                                                         App.id == Activity.appid).join(
            Developer).where(
            in_).group_by(
            *group_by, Developer.id).order_by(desc(avg))
    elif graph_filter == "BY RATING":
        xaxis = App.rating.label("xaxis")
        base_query = select(avg, xaxis, select_).select_from(
            DeviceOwnership).join(Account).join(School).join(Device).join(Activity).join(App,
                                                                                         App.id == Activity.appid).where(
            in_).group_by(
            *group_by, xaxis).order_by(desc(avg))

    df = query_for_df(base_query)
    return df


def app_usage_figure_df_school(graph_filter, *schools):
    """
    Queries the avg usage by duration for a school
    :param graph_filter: string
    :param schools: list of school ids
    :return: pandas dataframe
    """
    return app_usage_figure_df(graph_filter, concat(School.school_name, " (", School.postcode, ")").label("School"),
                               School.id.in_(schools), School.id)


def app_usage_figure_df_postcode(graph_filter, *postcodes):
    """
    Queries the avg usage by duration for a postcode
    :param graph_filter: string
    :param postcodes: list of postcodes
    :return: pandas dataframe
    """
    return app_usage_figure_df(graph_filter, School.postcode.label("Postcode"), School.postcode.in_(postcodes),
                               School.postcode)


def app_usage_figure_df_suburb(graph_filter, *suburbs):
    """
    Queries the avg usage by duration for a suburb
    :param graph_filter: string
    :param suburbs: list of suburbs/state in form 'School.suburb||||School.state'
    :return: pandas dataframe
    """
    return app_usage_figure_df(graph_filter, concat(School.suburb, " - ", School.state).label("Suburb"),
                               concat(School.suburb, "||||", School.state).in_(suburbs), School.suburb, School.state)


def app_usage_figure_df_state(graph_filter, *states):
    """
    Queries the avg usage by duration for a state
    :param graph_filter: string
    :param states: list of states
    :return: pandas dataframe
    """
    return app_usage_figure_df(graph_filter, School.state.label("State"), School.state.in_(states), School.state)


def get_sum_duration():
    """
    Queries the sum of Activity duration filtered
    :param filters: list of filters
    """
    return select(func.sum(Activity.duration)).select_from(
        Activity).join(DeviceOwnership, Activity.deviceid == DeviceOwnership.deviceid).join(Account).join(
        School).as_scalar()


def most_popular_apps_figure_query(graph_filter, *filters_):
    """
        Queries the most popular apps
        :param graph_filter: string
        :param filter_: SQLAlchemy filter
        :return: SQLAlchemy query
    """
    if graph_filter == 'BY ALL USAGE':
        filters = None
    elif graph_filter == 'BY SCHOOL TIME USAGE':
        filters = and_(hour(Activity.started) <= 15, hour(Activity.started) >= 8)
    elif graph_filter == 'BY OUTSIDE SCHOOL TIME USAGE':
        filters = and_(or_(hour(Activity.started) > 15, hour(Activity.started) < 8))

    filters_ += (apply_filter_decorator(filters),)

    sum_duration = get_sum_duration()
    sum_duration = apply_filters(sum_duration, filters_)

    total = (100 * func.sum(Activity.duration) / sum_duration.as_scalar()).label("total")

    base_query = select(total, App.appName).select_from(
        DeviceOwnership).join(Account).join(School).join(Device).join(Activity).join(App).group_by(
        App.appName).order_by(desc(total))

    base_query = apply_filters(base_query, filters_)

    return base_query


def most_popular_apps_figure_query_school(graph_filter, school):
    """
    Queries the most popular apps by school id
    :param graph_filter: string
    :param school: string
    :return: SQLAlchemy query
    """
    return most_popular_apps_figure_query(graph_filter, School.id == school)


def most_popular_apps_figure_query_postcode(graph_filter, postcode):
    """
    Queries the most popular apps by postcode
    :param graph_filter: string
    :param postcode: string
    :return: SQLAlchemy query
    """
    return most_popular_apps_figure_query(graph_filter, School.postcode == postcode)


def most_popular_apps_figure_query_suburb(graph_filter, suburb):
    """
    Queries the most popular apps by suburb
    :param graph_filter: string
    :param suburb: string in the form of "School.suburb||||School.state"
    :return: SQLAlchemy query
    """
    return most_popular_apps_figure_query(graph_filter, concat(School.suburb, "||||", School.state) == suburb)


def most_popular_apps_figure_query_state(graph_filter, state):
    """
    Queries the most popular apps by state
    :param graph_filter: string
    :param state: string
    :return: SQLAlchemy Query
    """
    return most_popular_apps_figure_query(graph_filter, School.state == state)
