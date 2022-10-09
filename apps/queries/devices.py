from sqlalchemy import select, func

from app import app
from apps.db_models.account import Account
from apps.db_models.activity import Activity
from apps.db_models.device import Device
from apps.db_models.device_ownership import DeviceOwnership
from apps.db_models.school import School
from apps.utils.database import query_for_df


def total_number_of_devices_df(location_filter):
    """
    Gets the total number of devices by location filter
    :param location_filter: function to filter query
    :return: int
    """
    total = func.count(DeviceOwnership.id).label("total")

    base_query = select(total).join(Account).join(School)

    base_query = location_filter(base_query)

    df = query_for_df(base_query)

    if df.empty:
        return ""

    return df.iloc[0]["total"]


def school_type_df(location_filter):
    """
    Gets the school type by location filter
    :param location_filter: function to filter query
    :return: string
    """
    base_query = select(School.school_type)
    base_query = location_filter(base_query)
    df = query_for_df(base_query)
    return df.iloc[0]["school_type"]


def avg_number_of_devices_per_school_df(location_filter):
    """
    Get the average number of devices per a school based on location filter
    :param location_filter: function to filter query
    :return: float
    """
    sub_query = select(func.count(School.id))
    sub_query = location_filter(sub_query)

    total = func.count(DeviceOwnership.id).label("total")

    base_query = select((total / sub_query.scalar_subquery()).label("avg")).join(Account).join(School)

    base_query = location_filter(base_query)

    df = query_for_df(base_query)
    if df.empty:
        return ""

    return df.iloc[0]["avg"]


def school_sector_df(location_filter):
    """
    Gets the school sector by location filter
    :param location_filter: function to filter query
    :return: string
    """
    base_query = select(School.school_sector)
    base_query = location_filter(base_query)
    df = query_for_df(base_query)
    return df.iloc[0]["school_sector"]


def school_with_most_devices_df(location_filter):
    """
    Get the school with most devices based on location filter
    :param location_filter: function to filter query
    :return: string
    """
    total = func.count(DeviceOwnership.deviceid).label("total")
    base_query = select(total, School.school_name).select_from(DeviceOwnership).join(Account).join(School).group_by(
        School.id)

    base_query = location_filter(base_query)

    df = query_for_df(base_query)
    if df.empty:
        return ""

    return f'{df.iloc[0]["school_name"]} ({df.iloc[0]["total"]})'


def devices_by_location_figure_df(graph_filter, location_filters):
    """
    Get the amount of devices grouped by school
    :param graph_filter: string
    :param location_filters: function to filter query
    :return: pandas dataframe
    """
    if graph_filter == 'BY TOTAL DEVICES':
        total = func.count('*').label("total")
        base_query = select(total, School.latitude, School.longitude, School.school_name).select_from(
            DeviceOwnership).join(Account).join(School).group_by(School.id)
    if graph_filter == "BY TOTAL USES":
        total = func.count('*').label("total")
        base_query = select(total, School.latitude, School.longitude, School.school_name).select_from(
            Activity).join(Device).join(DeviceOwnership).join(Account).join(School).group_by(School.id)

    base_query = location_filters(base_query)

    return query_for_df(base_query)
