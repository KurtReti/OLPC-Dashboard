from sqlalchemy import Column, Integer, ForeignKey, DateTime
from .app import App
from .base import Base
from .device import Device


class Activity(Base):
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    deviceid = Column(ForeignKey(Device.id))
    appid = Column(Integer, ForeignKey(App.id))
    started = Column(DateTime)
    duration = Column(Integer)
