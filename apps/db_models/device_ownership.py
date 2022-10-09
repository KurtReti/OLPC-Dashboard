from sqlalchemy import Column, Integer, ForeignKey
from .account import Account
from .base import Base
from .device import Device


class DeviceOwnership(Base):
    __tablename__ = 'device_ownership'
    id = Column(Integer, primary_key=True, autoincrement=True)
    deviceid = Column(Integer, ForeignKey(Device.id))
    accountid = Column(Integer, ForeignKey(Account.id))
