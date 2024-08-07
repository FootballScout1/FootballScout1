#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
from models import storage_t
# import models
from os import getenv
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

# from enum import Enum

# class UserRoleEnum(Enum):
#    ordinary = 'ordinary'
#    player = 'player'
#    scout = 'scout'

time = "%Y-%m-%dT%H:%M:%S.%f"

Base = object
if storage_t == "db":
    Base = declarative_base()

class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if storage_t == "db":
        __abstract__ = True
        id = Column(String(60), primary_key=True, nullable=False, default=str(uuid.uuid4()))
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if storage_t != "db":
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                # self.created_at = datetime.utcnow()
                self.created_at = kwargs.get("created_at", datetime.utcnow())
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                # self.updated_at = datetime.utcnow()
                self.updated_at = kwargs.get("updated_at", datetime.utcnow())
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        # new_dict.pop('_sa_instance_state', None)
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        from models import storage
        storage.delete(self)
