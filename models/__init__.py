#!/usr/bin/env python3
"""
initialize the models package
"""
from os import getenv
# Access the variables
storage_t = getenv("FOOTBALL_SCOUT_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
#
#
# # Delay the import of model classes
def init_models():
     """ Function to import models after setting storage_t """
     global Club, Player, Scout, Comment, Like, Post, User, Position, Country, UserRoleEnum
     from models.country import Country
     from models.club import Club
     from models.position import Position
     from models.post import Post
     from models.comment import Comment
     from models.like import Like
     from models.player import Player
     from models.scout import Scout
     from models.user import User
     from models.user_role_enum import UserRoleEnum
#
#
init_models()
