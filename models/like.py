#!/usr/bin/python3
""" holds class Like """
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey

class Like(BaseModel, Base):
    """Representation of Like"""
    if models.storage_t == 'db':
        __tablename__ = 'likes'
        post_id = Column(String(60), ForeignKey('posts.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        post_id = ""
        user_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Like"""
        super().__init__(*args, **kwargs)

