from sqlalchemy import Column, Integer, String
from .base import Base


class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hash = Column(String(40))
    serial = Column(String(12))
