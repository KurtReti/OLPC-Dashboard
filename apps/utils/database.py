import os

import pandas as pd
from sqlalchemy import func, Integer

from app import app
from database import Session


def hour(element):
    """
    Queries the hour from a date form sqlite and other sql databases
    :param element: SQLAlchemy element
    :return: SQLAlchemy decorator
    """
    if os.getenv("DB_TYPE") == "sqlite":
        return func.strftime('%H', element).cast(Integer)
    else:
        return func.hour(element)


@app.cache.memoize()
def read_sql_as_pd(query):
    with Session() as session:
        return pd.read_sql(query, session.bind)


def query_for_df(query):
    """
    Runs a SQLAlchemy query as pandas dataframe
    :param query: SQLAlchemy query
    :return: pandas dataframe
    """
    # compile query and convert to string to allow cache key to be generated propely
    return read_sql_as_pd(str(query.compile(compile_kwargs={"literal_binds": True})))
