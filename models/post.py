#!/usr/bin/python3
""" holds class Post """
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship

class Post(BaseModel, Base):
    """Representation of Post"""
    if models.storage_t == 'db':
        __tablename__ = 'posts'
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        title = Column(String(128), nullable=False)
        content = Column(Text, nullable=False)
        comments = relationship("Comment", backref="post", cascade="all, delete, delete-orphan")
        likes = relationship("Like", backref="post", cascade="all, delete, delete-orphan")
    else:
        user_id = ""
        title = ""
        content = ""

    def __init__(self, *args, **kwargs):
        """initializes Post"""
        super().__init__(*args, **kwargs)

