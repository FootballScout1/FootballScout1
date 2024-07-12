#!/usr/bin/python3
""" holds class Skill """
# import models
from models import storage_t
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Skill(BaseModel, Base):
    """Representation of Skill"""
    if storage_t == 'db':
        __tablename__ = 'skills'
        name = Column(String(128), nullable=False)
        players = relationship("Player",
                               secondary='player_skill',
                               viewonly=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes Skill"""
        super().__init__(*args, **kwargs)
