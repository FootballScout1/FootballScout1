#!/usr/bin/python3
""" holds class Post """
# import models
from models import storage_t
from models.base_model import BaseModel, Base
# from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Post(BaseModel, Base):
    """Representation of Post"""
    if storage_t == 'db':
        __tablename__ = 'posts'
        video_link = Column(String(255), nullable=True)
        comments = relationship("Comment", backref="post", cascade="all, delete, delete-orphan")
    else:
        video_link = ""

    def __init__(self, *args, **kwargs):
        """initializes Post"""
        super().__init__(*args, **kwargs)
