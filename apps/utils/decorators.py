from datetime import datetime

from sqlalchemy.sql.elements import BinaryExpression

from apps.db_models.activity import Activity


def date_filter(query, start_date, end_date):
    """
    Function to filter query by date range
    :param query: SQLAlchemy query
    :param start_date: timestamp
    :param end_date: timestamp
    :return: SQLAlchemy query
    """
    query = query.filter(Activity.started >= datetime.fromtimestamp(start_date)).filter(
        Activity.started <= datetime.fromtimestamp(end_date))
    return query


def apply_date_filter_decorator(date_range):
    """
    Decorator to apply date filter function
    :param date_range: tuple of start and end date as timestamp
    :return: function
    """

    def _filter(query):
        return date_filter(query, date_range[0], date_range[1])

    return _filter


def apply_location_filters_decorator(apply_location_filters, selected_state, selected_suburb, selected_postcode,
                                     selected_school):
    """
    Decorator to apply location filter function
    :param apply_location_filters: location filter function
    :param selected_state: string
    :param selected_suburb: string
    :param selected_postcode: string
    :param selected_school: string
    :return: function
    """

    def _filter(query):
        return apply_location_filters(query, selected_state, selected_suburb, selected_postcode, selected_school)

    return _filter


def apply_filter_decorator(filters=None):
    """
    Decorator to apply filters to SQLAlchemy queries
    :param filters: SQLAlchemy BinaryExpression
    :return: function
    """

    def _filter(query):
        if filters is not None:
            return query.filter(filters)
        else:
            return query

    return _filter


def apply_filters(query, filters):
    """
    Applies filters to a SQLAlchemy query
    :param query: SQLAlchemy query
    :param filters: list of filter eith a BinaryExpression or a function
    :return: SQLAlchemy query
    """
    for filter_ in filters:
        if isinstance(filter_, BinaryExpression):
            query = query.filter(filter_)
        else:
            query = filter_(query)
    return query
