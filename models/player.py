#!/usr/bin/python3

"""
Module for the Player class
"""
from models import storage_t
from models.base_model import BaseModel, Base
# from models.user import User
from sqlalchemy import Column, DateTime, String, ForeignKey, Integer, Table
from sqlalchemy.orm import backref, relationship
# from models.scout import Scout
# from models.post import Post
# from models.like import Like
# from models.comment import Comment
# from hashlib import md5


if storage_t == 'db':
    players_positions = Table('players_positions', Base.metadata,
                              Column('player_id', ForeignKey('players.id'),
                                     primary_key=True),
                              Column('position_id', ForeignKey('positions.id'),
                                     primary_key=True)
                              )

    scouts_players = Table('scouts_players', Base.metadata,
                           Column('scout_id', ForeignKey('scouts.id'),
                                  primary_key=True),
                           Column('player_id', ForeignKey('players.id'),
                                  primary_key=True)
                           )


class Player(BaseModel, Base):
    """
    Player class
    """
    if storage_t == 'db':
        __tablename__ = 'players'

        # id = Column(Integer, ForeignKey('users.id'), primary_key=True)  # Establish foreign key relationship

        email = Column(String(255), nullable=False)
        password = Column(String(255), nullable=False)
        first_name = Column(String(255), nullable=False)
        last_name = Column(String(255), nullable=False)
        height = Column(Integer, nullable=False, default=0)
        weight = Column(Integer, nullable=False, default=0)
        date_of_birth = Column(DateTime, nullable=True)
        # date_of_birth = Column(String(60), nullable=True)
        club_id = Column(String(60), ForeignKey('clubs.id'), nullable=False) # Integer

        positions = relationship('Position', secondary=players_positions,
                                 back_populates='players')
        scouts = relationship('Scout', secondary=scouts_players,
                              back_populates='players')
        posts = relationship('Post', backref=backref("player"),
                             cascade="all, delete, delete-orphan")
        likes = relationship('Like', backref=backref("player"),
                             cascade="all, delete, delete-orphan")
        comments = relationship('Comment', backref=backref("player"),
                                cascade="all, delete, delete-orphan")

    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        height = 0
        weight = 0
        date_of_birth = ""
        club_id = ""

        positions = []
        scouts = []
        posts = []
        likes = []
        comments = []

    # __mapper_args__ = {
    #    'exclude_properties': ['_sa_instance_state']
    # }

    def __init__(self, *args, **kwargs):
        """initializes Like"""
        super().__init__(*args, **kwargs)

        # if kwargs.get("password"):
        #    self.password = md5(kwargs["password"].encode()).hexdigest()

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        # if name == "password":
        #    value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

    # def to_dict(self):
    #    """Converts the object to a dictionary format"""
    #    player_dict = super().to_dict()
    #    if "_sa_instance_state" in player_dict:
    #        del player_dict["_sa_instance_state"]
    #    return player_dict

    def to_dict(self):
        """
        Returns a dictionary representation of a Player instance.
        """
        player_dict = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'height': self.height,
            'weight': self.weight,
            'date_of_birth': self.date_of_birth,
            'club_id': self.club_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        return player_dict
