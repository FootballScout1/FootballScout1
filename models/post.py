#!/usr/bin/python3
""" holds class Post """
from models import storage_t
from models.base_model import BaseModel, Base
from models.comment import Comment
from models.like import Like
from models.player import Player
from models.scout import Scout
from sqlalchemy import Column, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship


class Post(BaseModel, Base):
    """Representation of Post"""
    if storage_t == 'db':
        __tablename__ = 'posts'
        content = Column(String(1024), nullable=False)
        video_link = Column(String(255), nullable=True)
        player_id = Column(String(60), ForeignKey('players.id'), nullable=True)
        scout_id = Column(String(60), ForeignKey('scouts.id'), nullable=True)

        comments = relationship("Comment", backref="post",
                                cascade="all, delete, delete-orphan")
        likes = relationship("Like", backref="post",
                             cascade="all, delete, delete-orphan")

        __table_args__ = (
            CheckConstraint('player_id IS NOT NULL OR scout_id IS NOT NULL',
                            name='check_at_least_one_id'),
        )
    else:
        content = ""
        video_link = ""
        player = ""
        scout = ""

        comments = []
        likes = []

    def __init__(self, *args, **kwargs):
        """initializes Post"""
        super().__init__(*args, **kwargs)
