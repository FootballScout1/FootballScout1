#!/usr/bin/python3
""" holds class Rating """
# import models
from models import storage_t
from models.base_model import BaseModel, Base
# from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Rating(BaseModel, Base):
    """Representation of Rating"""
    if storage_t == 'db':
        __tablename__ = 'ratings'
        player_id = Column(
            String(60),
            ForeignKey('players.id'),
            nullable=False)
        scout_id = Column(String(60), ForeignKey('scouts.id'), nullable=False)
        score = Column(Integer, nullable=False)
        comment = Column(String(1024), nullable=True)
    else:
        player_id = ""
        scout_id = ""
        score = 0
        comment = ""

    def __init__(self, *args, **kwargs):
        """initializes Rating"""
        super().__init__(*args, **kwargs)
