#!/usr/bin/python3
""" holds class User """

from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
# from hashlib import md5

# from enum import Enum
from models.user_role_enum import UserRoleEnum

from models.scout import Scout
from models.player import Player
# from .user import UserRoleEnum

# class UserRoleEnum(Enum):
#    ordinary = 'ordinary'
#    player = 'player'
#    scout = 'scout'

class User(BaseModel, Base):
    """Representation of a User"""
    if storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(255), nullable=False, unique=True)
        password = Column(String(255), nullable=False)
        first_name = Column(String(255), nullable=False)
        last_name = Column(String(255), nullable=False)
        profile_picture = Column(String(128), nullable=True)
        
        # Use UserRoleEnum directly as the Enum class
        role = Column(Enum(UserRoleEnum), nullable=False, default=UserRoleEnum.ordinary)

        comments = relationship("Comment", backref="user",
                                cascade="all, delete, delete-orphan")
        likes = relationship("Like", backref="user",
                             cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

        role = UserRoleEnum.ordinary # "ordinary"

        comments = []
        likes = []
    
    __mapper_args__ = {
        'exclude_properties': ['_sa_instance_state']
    }

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

        # if kwargs.get("password"):
        #    self.password = md5(kwargs["password"].encode()).hexdigest()

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        # if name == "password":
        #    value = md5(value.encode()).hexdigest()
        if name == "role" and isinstance(value, str):
            value = UserRoleEnum[value]
        super().__setattr__(name, value)

    def to_dict(self):
        """Converts the object to a dictionary format"""

        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'role': self.role.value if self.role else None,
            'created_at': self.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'updated_at': self.updated_at.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'profile_picture': self.profile_picture
        }
        # user_dict = super().to_dict()
        # if self.role:
        #    user_dict['role'] = self.role.value  # Convert Enum to its string value
        # if "_sa_instance_state" in user_dict:
        #    del user_dict["_sa_instance_state"]
        # return user_dict

#    def switch_role(self, new_role):
#        """Switch user role and inherit attributes"""
#        if new_role not in ['ordinary', 'scout', 'player']:
#            raise ValueError("Invalid role")
#        self.role = new_role
#
#        # Convert the current user to a dictionary to inherit attributes
#        user_dict = self.to_dict()
#
#        if new_role == 'scout':
#            new_scout = Scout(
#                email=self.email,
#                password=self.password,
#                first_name=self.first_name,
#                last_name=self.last_name,
#                # club_id=self.club_id  # Assuming club_id exists in User model
#            )
#            new_scout.save()
#        elif new_role == 'player':
#            new_player = Player(
#                email=self.email,
#                password=self.password,
#                first_name=self.first_name,
#                last_name=self.last_name,
#                # club_id=self.club_id  # Assuming club_id exists in User model
#            )
#            new_player.save()
#        # self.save()
#        self.delete()
#        from models import storage
#        storage.save()
