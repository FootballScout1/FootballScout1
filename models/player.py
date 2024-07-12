#!/usr/bin/python3

"""
Module for the Player class
"""
from models import storage_t
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, DateTime, String, ForeignKey, Integer, Table
from sqlalchemy.orm import backref, relationship
from models.scout import Scout
from models.post import Post
from models.like import Like
from models.comment import Comment


players_positions = Table('players_positions', Base.metadata,
                          Column('player_id', ForeignKey('players.id'),
                                 primary_key=True),
                          Column('position_id', ForeignKey('positions.id'),
                                 primary_key=True)
                          )


scouts_players = Table('scouts_players', Base.metadata,
                       Column('scout_id', ForeignKey('scouts.id'),
                              primary_key=True),
                       Column('player_id', ForeignKey('players.id'),
                              primary_key=True)
                       )


class Player(BaseModel, Base):
    """
    Player class
    """
    if storage_t == 'db':
        __tablename__ = 'players'
        email = Column(String(60), nullable=False)
        password = Column(String(60), nullable=False)
        first_name = Column(String(60), nullable=False)
        second_name = Column(String(60), nullable=False)
        height = Column(Integer, nullable=False, default=0)
        weight = Column(Integer, nullable=False, default=0)
        date_of_birth = Column(DateTime, nullable=False)
        club_id = Column(Integer, ForeignKey('clubs.id'), nullable=False)

        positions = relationship('Position', secondary=players_positions,
                                 back_populates='players')
        scouts = relationship('Scout', secondary=scouts_players,
                              back_populates='players')
        posts = relationship('Post', backref=backref("player"),
                             cascade="all, delete, delete-orphan")
        likes = relationship('Like', backref=backref("player"),
                             cascade="all, delete, delete-orphan")
        comments = relationship('Comment', backref=backref("player"),
                                cascade="all, delete, delete-orphan")

    else:
        email = ""
        password = ""
        first_name = ""
        second_name = ""
        height = 0
        weight = 0
        date_of_birth = ""
        club_id = ""
        positions = []
        scouts = []
        posts = []
        likes = []
        comments = []


    def __init__(self, *args, **kwargs):
        """initializes Like"""
        super().__init__(*args, **kwargs)
