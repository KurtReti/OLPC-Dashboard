from sqlalchemy import Column, Integer, ForeignKey, String, Float
from .base import Base
from .developer import Developer


class App(Base):
    __tablename__ = 'app'
    id = Column(Integer, primary_key=True, autoincrement=True)
    appid = Column(String(275), unique=True)
    developerid = Column(Integer, ForeignKey(Developer.id))
    appName = Column(String(125))
    rating = Column(Float)
    numDownloads = Column(Integer)
