#!/usr/bin/python3
""" holds class Comment """
from models import storage_t
from models.base_model import BaseModel, Base
from models.post import Post
from models.user import User
from models.player import Player
from models.scout import Scout
from sqlalchemy import CheckConstraint, Column, String, ForeignKey


class Comment(BaseModel, Base):
    """Representation of Comment"""
    if storage_t == 'db':
        __tablename__ = 'comments'
        text = Column(String(1024), nullable=False)
        post_id = Column(String(60), ForeignKey('posts.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=True)
        player_id = Column(String(60), ForeignKey('players.id'), nullable=True)
        scout_id = Column(String(60), ForeignKey('scouts.id'), nullable=True)

        __table_args__ = (
            CheckConstraint(
                'user_id IS NOT NULL OR player_id IS NOT NULL OR scout_id IS NOT NULL',
                name='check_at_least_one_comment_id'  # Renamed constraint
            ),
        )

    else:
        text = ""
        post_id = ""
        user_id = ""
        player_id = ""
        scout_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Comment"""
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """Converts the object to a dictionary format"""
        comment_dict = super().to_dict()
        if "_sa_instance_state" in comment_dict:
            del comment_dict["_sa_instance_state"]
        return comment_dict
