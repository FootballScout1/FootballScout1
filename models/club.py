#!/usr/bin/python3
""" holds class Club"""
import models
from models.base_model import BaseModel, Base
from models.location import Location
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Club(BaseModel, Base):
    """Representation of Club """
    if models.storage_t == "db":
        __tablename__ = 'clubs'
        name = Column(String(128), nullable=False)
        location_id = Column(String(60), ForeignKey('locations.id'), nullable=False)
        players = relationship("Player",
                              backref="club",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""
        location_id = ""

    def __init__(self, *args, **kwargs):
        """initializes club"""
        super().__init__(*args, **kwargs)

#     if models.storage_t != "db":
#         @property
#         def location(self):
#             """getter for list of location instances related to the club"""
#             location_list = []
#             all_locations = models.storage.all(Location)
#             for location in all_locations.values():
#                 if location.club_id == self.id:
#                     location_list.append(location)
#             return location_list
