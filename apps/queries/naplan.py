from sqlalchemy import select, func, distinct, desc

from app import app
from apps.db_models.naplan import Naplan
from apps.db_models.school import School
from apps.utils.database import query_for_df


def school_sector(location_filter):
    """
    Get the school sector based on location filter
    :param location_filter: function to filter query
    :return: string
    """
    base_query = select(School.school_sector)
    base_query = location_filter(base_query)
    df = query_for_df(base_query)
    return df.iloc[0]["school_sector"]


def total_number_of_schools(location_filter):
    """
    Get the total number of schools based on location filter
    :param location_filter: function to filter query
    :return: string
    """
    total = func.count(distinct(School.id)).label("total")
    base_query = select(total).select_from(Naplan).join(School)

    base_query = location_filter(base_query)

    df = query_for_df(base_query)

    return df.iloc[0]["total"]


def total_number_of_tests_df(location_filter):
    """
    Gets the total number of tests by location filter
    :param location_filter: function to filter query
    :return: int
    """
    total = func.sum(Naplan.numStudents).label("total")
    base_query = select(total).select_from(Naplan).join(School)

    base_query = location_filter(base_query)

    df = query_for_df(base_query)

    if df.empty:
        return 0

    return df.iloc[0]["total"]


def school_type(location_filter):
    """
    Gets the school type by location filter
    :param location_filter: function to filter query
    :return: string
    """
    base_query = select(School.school_type)
    base_query = location_filter(base_query)
    df = query_for_df(base_query)
    return df.iloc[0]["school_type"]


def highest_naplan_score_update_df(location_filter):
    """
    Gets the highest naplan score and school name
    :param location_filter: function to filter query
    :return: string
    """
    max = func.avg(Naplan.averageScore).label("max")
    base_query = select(max, School.school_name).select_from(Naplan).join(School).group_by(School.id).order_by(
        desc(max)).limit(1)

    base_query = location_filter(base_query)

    df = query_for_df(base_query)
    if df.empty:
        return ""

    return f'{df.iloc[0]["max"]} ({df.iloc[0]["school_name"]})'


def naplan_results_figure_df(graph_filter, location_filters):
    """
    Gets the average naplan score grouped by area of study and grade by locatio filter
    :param graph_filter: string
    :param location_filters: function to filter query
    :return: pandas dataframe
    """
    if graph_filter == 'ALL SCHOOLS':
        avg = func.avg(Naplan.averageScore).label("avg")
        base_query = select(avg, Naplan.areaOfStudy.label("xaxis"), Naplan.grade).select_from(
            Naplan).join(School).group_by(Naplan.areaOfStudy, Naplan.grade)
    elif graph_filter == 'GOVERNMENT':
        avg = func.avg(Naplan.averageScore).label("avg")
        base_query = select(avg, Naplan.areaOfStudy.label("xaxis"), Naplan.grade).select_from(
            Naplan).join(School).filter(School.school_sector == "Government").group_by(Naplan.areaOfStudy, Naplan.grade)
    elif graph_filter == 'CATHOLIC':
        avg = func.avg(Naplan.averageScore).label("avg")
        base_query = select(avg, Naplan.areaOfStudy.label("xaxis"), Naplan.grade).select_from(
            Naplan).join(School).filter(School.school_sector == "Catholic").group_by(Naplan.areaOfStudy, Naplan.grade)
    elif graph_filter == 'INDEPENDENT':
        avg = func.avg(Naplan.averageScore).label("avg")
        base_query = select(avg, Naplan.areaOfStudy.label("xaxis"), Naplan.grade).select_from(
            Naplan).join(School).filter(School.school_sector == "Independent").group_by(Naplan.areaOfStudy,
                                                                                        Naplan.grade)

    base_query = location_filters(base_query)

    return query_for_df(base_query)
