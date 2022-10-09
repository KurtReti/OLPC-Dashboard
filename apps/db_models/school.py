from sqlalchemy import Column, Integer, String, Float
from .base import Base


class School(Base):
    __tablename__ = 'school'
    id = Column(Integer, primary_key=True, autoincrement=True)
    school_id = Column(Integer)
    school_name = Column(String(300))
    suburb = Column(String(100))
    state = Column(String(10))
    postcode = Column(String(4))
    school_sector = Column(String(100))
    school_type = Column(String(100))
    longitude = Column(Float)
    latitude = Column(Float)
