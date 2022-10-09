from sqlalchemy import Column, Integer, String
from .base import Base


class Developer(Base):
    __tablename__ = 'developer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(75), unique=True)
