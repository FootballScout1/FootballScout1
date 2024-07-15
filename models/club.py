#!/usr/bin/python3
""" holds class Club"""
from models.base_model import BaseModel, Base

# from models import storage_t
# from models.location import Location
# from os import getenv
# import sqlalchemy
# from sqlalchemy import Column, String #, ForeignKey
# from sqlalchemy.orm import relationship
# from models.scout_club import scout_club

# from models.player import Player
# from models.scout import Scout
# from models.country import Country
from models import storage_t
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship, backref


class Club(BaseModel, Base):
    """Representation of Club """
    if storage_t == "db":
        __tablename__ = 'clubs'
        name = Column(String(128), nullable=False)
        country_id = Column(String(60), ForeignKey('countries.id'))

        players = relationship("Player", backref=backref("club"),
                               cascade="all, delete, delete-orphan")
        scouts = relationship("Scout", backref=backref("club"),
                              cascade="all, delete, delete-orphan")
    else:
        name = ""
        country_id = ""

        players = []
        scouts = []

    def __init__(self, *args, **kwargs):
        """initializes club"""
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """Converts the object to a dictionary format"""
        club_dict = super().to_dict()
        if "_sa_instance_state" in club_dict:
            del club_dict["_sa_instance_state"]
        return club_dict
