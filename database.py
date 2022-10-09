import sqlalchemy as db
import os
from sqlalchemy.orm import sessionmaker
from apps.db_models.base import Base

if os.getenv("DB_URI"):
    engine = db.create_engine(os.getenv("DB_URI"))
elif os.getenv("DB_TYPE") != "sqlite":
    engine = db.create_engine(
        f'{os.getenv("DB_TYPE")}://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
else:
    engine = db.create_engine(f'sqlite:///assets/{os.getenv("DB_NAME")}.db')

Session = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)
