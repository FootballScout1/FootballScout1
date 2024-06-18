#!/usr/bin/python
""" holds class Location"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String # ForeignKey
from sqlalchemy.orm import relationship


class Location(BaseModel, Base):
    """Representation of Location """
    if models.storage_t == "db":
        __tablename__ = 'locations'
        # club_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        clubs = relationship("Club",
                              backref="location",
                              cascade="all, delete, delete-orphan")
    else:
        # club_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes location"""
        super().__init__(*args, **kwargs)
