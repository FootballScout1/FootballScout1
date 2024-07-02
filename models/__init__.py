#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv
# from models.base_model import BaseModel, Base
# from models.club import Club
# from models.location import Location
# from models.player import Player
# from models.scout import Scout
# from models.skill import Skill
# from models.rating import Rating
# from models.comment import Comment
# from models.like import Like
# from models.post import Post
# from models.user import User


storage_t = getenv("FOOTBALL_SCOUT_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()

# Delay the import of model classes
def init_models():
    """ Function to import models after setting storage_t """
    global Club, Player, Scout, Comment, Like, Post, User
    from models.club import Club
    from models.player import Player
    from models.scout import Scout
    from models.comment import Comment
    from models.like import Like
    from models.post import Post
    from models.user import User

init_models()
