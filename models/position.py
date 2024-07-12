#!/usr/bin/python3
"""
Module defines class Position
"""

from models import storage_t
from models.base_model import Base, BaseModel
from models.player import Player, players_positions
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Position(BaseModel, Base):
    """
    Class defines a Position
    """
    if storage_t == "db":
        __tablename__ = "positions"
        name = Column(String(60), nullable=False)
        abbrev = Column(String(4), nullable=False)
        players = relationship('Player', secondary=players_positions,
                               back_populates='positions')
    else:
        name = ""
        abbrev = ""
        players = []

    def __init__(self, *args, **kwargs):
        """
        Initializes a Position object
        """
        super().__init__(*args, **kwargs)
