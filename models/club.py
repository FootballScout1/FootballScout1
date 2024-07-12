#!/usr/bin/python3
""" holds class Club"""
# import models
from models.base_model import BaseModel, Base
# from models import storage_t
# from models.location import Location
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String #, ForeignKey
from sqlalchemy.orm import relationship
# from models.scout_club import scout_club

storage_t = getenv("FOOTBALL_SCOUT_TYPE_STORAGE")

class Club(BaseModel, Base):
    """Representation of Club """
    if storage_t == "db":
        __tablename__ = 'clubs'
        name = Column(String(128), nullable=False)
        # location_id = Column(
        #    String(60),
        #    ForeignKey('locations.id'),
        #    nullable=False)
        # players = relationship("Player",
        #                       backref="club",
        #                       cascade="all, delete, delete-orphan")
        country = Column(String(128), nullable=False)
        league = Column(String(128), nullable=False)
        players = relationship("Player", back_populates="club", cascade="all, delete, delete-orphan")
        scouts = relationship("Scout", back_populates="club", cascade="all, delete, delete-orphan")
        # scouts = relationship("Scout", secondary=scout_club, back_populates="clubs")
    else:
        name = ""
        # location_id = ""
        country = ""
        league = ""
        # scouts = []

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
