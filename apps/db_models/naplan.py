from sqlalchemy import Column, Integer, ForeignKey, String
from .base import Base
from .school import School


class Naplan(Base):
    __tablename__ = 'naplan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    schoolid = Column(Integer, ForeignKey(School.id), nullable=True)
    year = Column(Integer)
    areaOfStudy = Column(String(250))
    grade = Column(String(250))
    averageScore = Column(Integer)
    numStudents = Column(Integer)
