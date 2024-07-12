#!/usr/bin/python3
""" holds class Club"""
from models.base_model import BaseModel, Base
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
