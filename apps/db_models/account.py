from sqlalchemy import Column, Integer, ForeignKey, String
from .base import Base
from .school import School


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    schoolid = Column(Integer, ForeignKey(School.id))
    account_id = Column(String(18), unique=True)
