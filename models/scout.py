#!/usr/bin/python3

"""
Module defines the Scout class
"""
from models import storage_t
from models.base_model import BaseModel, Base
# from models.user import User
from sqlalchemy import Column, DateTime, String, ForeignKey, Integer
from sqlalchemy.orm import backref, relationship
# from models.player import scouts_players
# from models.player import Player, scouts_players
# from models.post import Post
# from models.like import Like
# from models.comment import Comment
# from hashlib import md5


class Scout(BaseModel, Base):
    """
    Scout class
    """
    if storage_t == 'db':
        __tablename__ = "scouts"

        # id = Column(Integer, ForeignKey('users.id'), primary_key=True)  # Establish foreign key relationship

        email = Column(String(255), nullable=False)
        password = Column(String(255), nullable=False)
        first_name = Column(String(255), nullable=False)
        last_name = Column(String(255), nullable=False)
        club_id = Column(String(60), ForeignKey('clubs.id'), nullable=False)
        
        from models.player import scouts_players
        players = relationship('Player', secondary=scouts_players,
                               back_populates='scouts')
        likes = relationship('Like', backref=backref("scout"))
        comments = relationship('Comment', backref=backref("scout"))
        posts = relationship('Post', backref=backref("scout"))


    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        club_id = ""

        players = []
        likes = []
        comments = []
        posts = []

    def __init__(self, *args, **kwargs):
        """
        Initializes Scout
        """

        # if kwargs.get("email"):
        #    self.email = kwargs["email"]
        # if kwargs.get("password"):
        #    self.password = kwargs["password"]
        # if kwargs.get("first_name"):
        #    self.first_name = kwargs["first_name"]
        # if kwargs.get("last_name"):
        #    self.last_name = kwargs["last_name"]

        super().__init__(*args, **kwargs)

        # if kwargs.get("password"):
            # self.password = md5(kwargs["password"].encode()).hexdigest()

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        # if name == "password":
        #    value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

    # def to_dict(self):
    #    """Converts the object to a dictionary format"""
    #    scout_dict = super().to_dict()
    #    if "_sa_instance_state" in scout_dict:
    #        del scout_dict["_sa_instance_state"]
    #    return scout_dict

    def to_dict(self):
        """
        Returns a dictionary representation of a Scout instance.
        """
        scout_dict = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'players': [player.to_dict() for player in self.players]  # Convert related Player objects to dictionaries
        }
        return scout_dict
