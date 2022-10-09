import pandas as pd
from sqlalchemy import func, select, desc
from sqlalchemy.sql.elements import and_, or_

from app import app
from apps.db_models.account import Account
from apps.db_models.activity import Activity
from apps.db_models.app import App
from apps.db_models.app_category_association import AppCategoryAssociation
from apps.db_models.category import Category
from apps.db_models.developer import Developer
from apps.db_models.device import Device
from apps.db_models.device_ownership import DeviceOwnership
from apps.db_models.school import School
from apps.utils.database import query_for_df, hour
from apps.utils.decorators import apply_filter_decorator, apply_filters
from database import Session


@app.cache.memoize()
def get_first_and_last_dates():
    with Session() as session:
        base_query = session.query(func.min(Activity.started), func.max(Activity.started))
        return list(base_query)[0]


def app_usage_figure_df(graph_filter, *filters_):
    """
    Query the average app usage duration by the graph filter and list of filters
    :param graph_filter:
    :param filters_: list of filters
    :return: pandas dataframe
    """
    avg = func.avg(Activity.duration / 60).label("avg")
    if graph_filter == "BY CATEGORY":
        xaxis = Category.name.label("xaxis")
        base_query = select(avg, xaxis).select_from(
            DeviceOwnership).join(Account).join(School).join(Device).join(Activity).join(AppCategoryAssociation,
                                                                                         AppCategoryAssociation.appid == Activity.appid).join(
            Category).group_by(
            Category.id).order_by(desc(avg))
    if graph_filter == "BY DEVELOPER":
        xaxis = Developer.name.label("xaxis")
        base_query = select(avg, xaxis).select_from(
            DeviceOwnership).join(Account).join(School).join(Device).join(Activity).join(App,
                                                                                         App.id == Activity.appid).join(
            Developer).group_by(
            Developer.id).order_by(desc(avg))
    if graph_filter == "BY RATING":
        xaxis = App.rating.label("xaxis")
        base_query = select(avg, xaxis).select_from(
            DeviceOwnership).join(Account).join(School).join(Device).join(Activity).join(App,
                                                                                         App.id == Activity.appid).group_by(
            xaxis).order_by(desc(avg))

    base_query = apply_filters(base_query, filters_)

    df = query_for_df(base_query)

    df = pd.concat([df.iloc[0:5], pd.DataFrame([{"avg": df["avg"].iloc[5:].mean(), "xaxis": "Others"}])])
    df["xaxis"] = df["xaxis"].astype(str)

    return df


def get_sum_duration():
    """
    Queries the sum of Activity duration filtered
    """
    query = select(func.sum(Activity.duration)).select_from(
        Activity).join(DeviceOwnership, Activity.deviceid == DeviceOwnership.deviceid).join(Account).join(
        School)
    return query


def most_popular_apps_figure_df(graph_filter, *filters_):
    """
    Queries the most popular apps
    :param graph_filter: string
    :param filters_: filter decorator functions
    :return: pandas datafrane
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

    df = query_for_df(base_query)

    df = pd.concat([df.iloc[0:7], pd.DataFrame([{"total": df["total"].iloc[7:].sum(), "appName": "Others"}])])

    return df


def usage_of_apps_by_location_figure_df(graph_filter, *filters_: list):
    """
    Generate the usage of apps by location according to the graph filter and location filters
    :param graph_filter: string
    :param filters_: list of filters
    :return: pandas dataframe
    """
    duration_func = {"BY TOTAL USAGE": func.sum, "BY AVG USAGE": func.avg, "BY LONGEST USAGE": func.max,
                     "BY SCHOOL TIME USAGE": func.sum, "BY OUTSIDE SCHOOL TIME USAGE": func.sum}

    duration_hours = (duration_func[graph_filter](Activity.duration) / 60 / 60).label("duration (hours)")

    base_query = select(duration_hours, School.latitude, School.longitude, School.school_name).select_from(
        DeviceOwnership).join(Account).join(School).join(Device).join(Activity).group_by(School.id)

    if graph_filter == "BY SCHOOL TIME USAGE":
        filter_ = and_(hour(Activity.started) <= 15, hour(Activity.started) >= 8)
    elif graph_filter == "BY OUTSIDE SCHOOL TIME USAGE":
        filter_ = or_(hour(Activity.started) > 15, hour(Activity.started) < 8)
    else:
        filter_ = None

    filters_ += (apply_filter_decorator(filter_),)

    base_query = apply_filters(base_query, filters_)

    df = query_for_df(base_query)

    return df
