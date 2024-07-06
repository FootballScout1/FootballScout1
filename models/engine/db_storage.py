#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from dotenv import load_dotenv

# import models
# from models import storage
from models.base_model import BaseModel, Base
from models.club import Club
# from models.location import Location
from models.player import Player
from models.scout import Scout
# from models.skill import Skill
# from models.rating import Rating
from models.comment import Comment
from models.like import Like
from models.post import Post
from models.user import User
from os import getenv
# import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()

FOOTBALL_SCOUT_ENV = getenv("FOOTBALL_SCOUT_ENV")
FOOTBALL_SCOUT_TYPE_STORAGE = getenv("FOOTBALL_SCOUT_TYPE_STORAGE")

classes = {"Club": Club, "Player": Player, "Scout": Scout,
           "Comment": Comment, "Like": Like,
           "Post": Post, "User": User}


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        # FBS_MYSQL_USER = getenv('FBS_MYSQL_USER')
        # FBS_MYSQL_PWD = getenv('FBS_MYSQL_PWD')
        # FBS_MYSQL_HOST = getenv('FBS_MYSQL_HOST')
        # FBS_MYSQL_DB = getenv('FBS_MYSQL_DB')
        # FBS_ENV = getenv('FBS_ENV')
        # self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
        #                              format(FBS_MYSQL_USER,
        #                                     FBS_MYSQL_PWD,
        #                                     FBS_MYSQL_HOST,
        #                                     FBS_MYSQL_DB))

        # self.__engine = create_engine(sqlite3:///test.db)
        # if FBS_ENV == "test":
        #    Base.metadata.drop_all(self.__engine)
        
        FOOTBALL_SCOUT_ENV = getenv('FOOTBALL_SCOUT_ENV')
        if FOOTBALL_SCOUT_ENV == 'test':
            FOOTBALL_SCOUT_MYSQL_USER = getenv('FOOTBALL_SCOUT_TEST_MYSQL_USER')
            FOOTBALL_SCOUT_MYSQL_PWD = getenv('FOOTBALL_SCOUT_TEST_MYSQL_PWD')
            FOOTBALL_SCOUT_MYSQL_HOST = getenv('FOOTBALL_SCOUT_TEST_MYSQL_HOST')
            FOOTBALL_SCOUT_MYSQL_DB = getenv('FOOTBALL_SCOUT_TEST_MYSQL_DB')
        else:
            FOOTBALL_SCOUT_MYSQL_USER = getenv('FOOTBALL_SCOUT_DEV_MYSQL_USER')
            FOOTBALL_SCOUT_MYSQL_PWD = getenv('FOOTBALL_SCOUT_DEV_MYSQL_PWD')
            FOOTBALL_SCOUT_MYSQL_HOST = getenv('FOOTBALL_SCOUT_DEV_MYSQL_HOST')
            FOOTBALL_SCOUT_MYSQL_DB = getenv('FOOTBALL_SCOUT_DEV_MYSQL_DB')

        FOOTBALL_SCOUT_TYPE_STORAGE = getenv('FOOTBALL_SCOUT_TYPE_STORAGE')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(FOOTBALL_SCOUT_MYSQL_USER,
                                             FOOTBALL_SCOUT_MYSQL_PWD,
                                             FOOTBALL_SCOUT_MYSQL_HOST,
                                             FOOTBALL_SCOUT_MYSQL_DB))

        if FOOTBALL_SCOUT_ENV == "test":  #dev
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

    def drop_table(self, table):
        """Drops a specific table"""
        # self.delete_dependent_records(table)
        Base.metadata.drop_all(self.__engine, tables=[table.__table__])

    def create_tables(self):
        """Creates all tables defined in Base.metadata"""
        Base.metadata.create_all(self.__engine)

    def reload(self):
        """reloads data from the database"""
        # self.create_tables()
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session
        # self.drop_table(Player)

    # def delete_dependent_records(self, table):
    #    """Delete records from dependent tables before dropping the table."""
    #    if table == Player:
            # Delete comments related to players
    #        self.__session.query(Comment).filter(Comment.player_id.in_(
    #            self.__session.query(Player.sofifa_id)
    #        )).delete(synchronize_session=False)
            # Delete likes related to players
    #        self.__session.query(Like).filter(Like.player_id.in_(
    #            self.__session.query(Player.sofifaid)
    #        )).delete(synchronize_session=False)
            # Commit the changes
    #        self.__session.commit()

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

        # all_cls = storage.all(cls)
        all_cls = self.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        # all_class = classes.values()

        # if not cls:
        #    count = 0
        #    for clas in all_class:
        #        count += len(storage.all(clas).values())
        # else:
        #    count = len(storage.all(cls).values())

        # return count

        # if cls:
        #    return len(self.all(cls))
        # else:
        #    return len(self.all())

        if cls:
            return self.__session.query(cls).count()
        else:
            counts = {}
            for _cls in [User, Club, Comment, Like, Player, Post, Scout]:
                counts[_cls.__name__.lower()] = self.__session.query(_cls).count()
            return counts
