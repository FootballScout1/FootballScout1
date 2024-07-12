#!/usr/bin/python3
"""
Module defines mysql db wrapped in sqlalchemy orm
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from os import getenv


class DBStorage:
    """
    Module defines db to map classes onto mysqldb
    """
    __engine = None
    __session = None

    def __init__(self):
        """Instaniates a DBStorage instance"""
        # user = getenv('HBNB_MYSQL_USER')
        # password = getenv('HBNB_MYSQL_PWD')
        # hostname = getenv('HBNB_MYSQL_HOST')
        # database = getenv('HBNB_MYSQL_DB')
        _env = getenv('FOOTBALL_SCOUT_ENV')

        # self.__engine = create_engine(
        #     "mysql+mysqldb://{}:{}@{}/{}"
        #     .format(user, password, hostname, database),
        #     pool_pre_ping=True, echo=False
        # )
        db = "sqlite:///footDB.db"
        self.__engine = create_engine(db, pool_pre_ping=True)

        if _env == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Returns all instances of type"""
        from models.country import Country
        from models.club import Club
        from models.user import User
        from models.player import Player
        from models.scout import Scout
        from models.post import Post
        from models.comment import Comment
        from models.like import Like
        from models.position import Position

        _classes = [Country, Club, User, Player, Post, Comment, Like, Position, Scout]
        all_obj = {}
        if self.__session is None:
            self.reload()
        if cls:
            for obj in self.__session.query(cls):
                all_obj[obj.__class__.__name__ + "." + obj.id] = obj
        else:
            for model in _classes:
                for obj in self.__session.query(model):
                    all_obj[obj.__class__.__name__ + "." + obj.id] = obj

        return (all_obj)

    def new(self, obj):
        """Adds obj to current db"""
        if self.__session is None:
            self.reload()
        self.__session.add(obj)
        self.__session.flush()

    def save(self):
        """Commits all changes to current db"""
        if self.__session is None:
            self.reload()
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from current db"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all mapped tables into db and a new session
        """
        from models.country import Country
        from models.club import Club
        from models.user import User
        from models.player import Player
        from models.scout import Scout
        from models.post import Post
        from models.comment import Comment
        from models.like import Like
        from models.position import Position
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False
            )
        )

    def close(self):
        """Calls remove method on private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        from models import storage
        from models.country import Country
        from models.club import Club
        from models.user import User
        from models.player import Player
        from models.scout import Scout
        from models.post import Post
        from models.comment import Comment
        from models.like import Like
        from models.position import Position
        _classes = [Country, Club, User, Player, Post, Comment, Like, Position, Scout]
        if cls not in _classes:
            return None

        complete_cls = storage.all(cls)
        for value in complete_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        Returns the number of objects in storage matching
        the given class. If no class is passed,
        returns the count of all objects in storage
        """
        from models import storage
        from models.country import Country
        from models.club import Club
        from models.user import User
        from models.player import Player
        from models.scout import Scout
        from models.post import Post
        from models.comment import Comment
        from models.like import Like
        from models.position import Position
        _classes = [Country, Club, User, Player, Post, Comment, Like, Position, Scout]
        complete_class = _classes

        if not cls:
            count = 0
            for item in complete_class:
                count += len(storage.all(item).values())
        else:
            count = len(storage.all(cls).values())

        return count
