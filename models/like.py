#!/usr/bin/python3
""" holds class Like """
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import CheckConstraint
from sqlalchemy import Column, String, ForeignKey


class Like(BaseModel, Base):
    """Representation of Like"""
    if storage_t == 'db':
        __tablename__ = 'likes'
        post_id = Column(String(60), ForeignKey('posts.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=True)
        player_id = Column(String(60), ForeignKey('players.id'), nullable=True)
        scout_id = Column(String(60), ForeignKey('scouts.id'), nullable=True)

        __table_args__ = (
            CheckConstraint('user_id IS NOT NULL OR \
            player_id IS NOT NULL OR scout_id IS NOT NULL',
                            name='check_at_least_one_id'),
        )

    else:
        post_id = ""
        user_id = ""
        player_id = ""
        scout_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Like"""
        super().__init__(*args, **kwargs)
