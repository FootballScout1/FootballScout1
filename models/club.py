#!/usr/bin/python3
""" holds class Club"""
# import models
from models.base_model import BaseModel, Base
# from models import storage_t
# from models.location import Location
from os import getenv
import sqlalchemy
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

storage_t = getenv("FOOTBALL_SCOUT_TYPE_STORAGE")


class Club(BaseModel, Base):
    """Representation of Club """
    if storage_t == "db":
        __tablename__ = 'clubs'
        name = Column(String(128), nullable=False)
        country_id = Column(String(60), ForeignKey('countries.id'))
        players = relationship("Player", backref=backref("club"), cascade="all, delete, delete-orphan")
        scouts = relationship("Scout", backref=backref("club"), cascade="all, delete, delete-orphan")
    else:
        name = ""
        country = ""
        players = []
        scouts = []

    def __init__(self, *args, **kwargs):
        """initializes club"""
        super().__init__(*args, **kwargs)
