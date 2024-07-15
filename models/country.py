#!/usr/bin/python
""" holds class Country"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref


class Country(BaseModel, Base):
    """Representation of Location """
    if storage_t == "db":
        __tablename__ = 'countries'
        name = Column(String(60), nullable=False)
        clubs = relationship("Club",
                             backref=backref("country"),
                             cascade="all, delete, delete-orphan")
    else:
        name = ""
        clubs = []

    def __init__(self, *args, **kwargs):
        """initializes location"""
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """Converts the object to a dictionary format"""
        country_dict = super().to_dict()
        if "_sa_instance_state" in country_dict:
            del country_dict["_sa_instance_state"]
        return country_dict
