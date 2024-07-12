#!/usr/bin/python3
""" holds class User """

from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a User"""
    if storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(255), nullable=False)
        password = Column(String(255), nullable=False)
        first_name = Column(String(255), nullable=False)
        second_name = Column(String(255), nullable=False)
        comments = relationship("Comment", backref="user",
                                cascade="all, delete, delete-orphan")
        likes = relationship("Like", backref="user",
                             cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        second_name = ""

        comments = []
        likes = []

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

        if kwargs.get("password"):
            self.password = md5(kwargs["password"].encode()).hexdigest()

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
