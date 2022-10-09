from sqlalchemy import Column, ForeignKey

from .app import App
from .base import Base
from .category import Category


class AppCategoryAssociation(Base):
    __tablename__ = 'appcategoryassociation'
    appid = Column(ForeignKey(App.id), primary_key=True)
    categoryid = Column(ForeignKey(Category.id), primary_key=True)
