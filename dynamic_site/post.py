#!/usr/bin/env python3
"""
Makes Post page dynamic
"""
from flask import Flask
from models import storage
from models.scout import Scout
from models.player import Player
from models.club import Club
from models.country import Country
from models.post import Post
from models.like import Like
from models.comment import Comment
from models.position import Position
from models.user import User

fbs = Flask(__name__)


@fbs.route('/post/<post_id>', strict_slashes=False)
def describe_post():
    """
    Displays a post with its comments
    """
    post = storage.get(Post, post_id)
