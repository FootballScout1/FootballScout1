#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import BaseModel
from models.club import Club
from models.location import Location
from models.player import Player
from models.scout import Scout
from models.skill import Skill
from models.rating import Rating
from models.comment import Comment
from models.like import Like
from models.post import Post
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Club": Club, "Location": Location,
           "Player": Player, "Scout": Scout, "Skill": Skill,
           "Rating": Rating, "Comment": Comment, "Like": Like,
           "Post": Post, "User": User}


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        FBS_MYSQL_USER = getenv('FBS_MYSQL_USER')
        FBS_MYSQL_PWD = getenv('FBS_MYSQL_PWD')
        FBS_MYSQL_HOST = getenv('FBS_MYSQL_HOST')
        FBS_MYSQL_DB = getenv('FBS_MYSQL_DB')
        FBS_ENV = getenv('FBS_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(FBS_MYSQL_USER,
                                             FBS_MYSQL_PWD,
                                             FBS_MYSQL_HOST,
                                             FBS_MYSQL_DB))

        # self.__engine = create_engine(sqlite3:///test.db)
        if FBS_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
