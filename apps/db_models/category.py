from sqlalchemy import Column, Integer, String
from .base import Base


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
