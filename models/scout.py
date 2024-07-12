#!/usr/bin/python3

"""
Module defines the Scout class
"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, DateTime, String, ForeignKey, Integer
from sqlalchemy.orm import backref, relationship
from models.player import scouts_players
# from models.player import Player, scouts_players
# from models.post import Post
# from models.like import Like
# from models.comment import Comment
from hashlib import md5


class Scout(BaseModel, Base):
    """
    Scout class
    """
    if storage_t == 'db':
        __tablename__ = "scouts"

        email = Column(String(60), nullable=False)
        password = Column(String(60), nullable=False)
        first_name = Column(String(60), nullable=False)
        second_name = Column(String(60), nullable=False)
        club_id = Column(String(60), ForeignKey('clubs.id'), nullable=False)

        players = relationship('Player', secondary=scouts_players,
                               back_populates='scouts')
        likes = relationship('Like', backref=backref("scout"))
        comments = relationship('Comment', backref=backref("scout"))
        posts = relationship('Post', backref=backref("scout"))

    else:
        email = ""
        password = ""
        first_name = ""
        second_name = ""
        club_id = ""

        players = []
        likes = []
        comments = []
        posts = []

    def __init__(self, *args, **kwargs):
        """
        Initializes Scout
        """
        super().__init__(*args, **kwargs)

        if kwargs.get("password"):
            self.password = md5(kwargs["password"].encode()).hexdigest()

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
