#!/usr/bin/python
""" holds class Country"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref


class Country(BaseModel, Base):
    """Representation of Location """
    if storage_t == "db":
        __tablename__ = 'countries'
        name = Column(String(60), nullable=False)
        clubs = relationship("Club",
                             backref=backref("country"),
                             cascade="all, delete, delete-orphan")
    else:
        name = ""
        clubs = []

    def __init__(self, *args, **kwargs):
        """initializes location"""
        super().__init__(*args, **kwargs)
