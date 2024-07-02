#!/usr/bin/python3
""" holds class Comment """
# import models
from models import storage_t
from models.base_model import BaseModel, Base
# from os import getenv
# import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer


class Comment(BaseModel, Base):
    """Representation of Comment"""
    if storage_t == 'db':
        __tablename__ = 'comments'
        text = Column(String(1024), nullable=False)
        post_id = Column(String(60), ForeignKey('posts.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        # player_id = Column(Integer, ForeignKey('players.sofifa_id', ondelete='CASCADE'), nullable=True)
        player_id = Column(String(60), ForeignKey('players.id'), nullable=True)
        scout_id = Column(String(60), ForeignKey('scouts.id'), nullable=True)
    else:
        text = ""
        post_id = ""
        user_id = ""
        player_id = ""
        scout_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Comment"""
        super().__init__(*args, **kwargs)
