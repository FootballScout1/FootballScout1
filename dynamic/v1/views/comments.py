#!/usr/bin/python3
"""
View module for handling Comment objects
"""

from os import path, getenv
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, g, session, send_from_directory
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
from dynamic.v1.views import app_views
from models import storage, User, UserRoleEnum, Club, Player, Scout, Post
from models.comment import Comment
from console import FootballScoutCommand
import logging
from sqlalchemy.orm import sessionmaker, joinedload
from models.base_model import Base
import uuid

logging.basicConfig(level=logging.DEBUG)

# Database setup
# db = "sqlite:///footDB.db"
# engine = create_engine(db, pool_pre_ping=True)

# Database setup
# engine = create_engine('mysql+mysqlconnector://football_scout_dev:football_scout_dev_pwd@localhost/football_scout_dev_db')

# Database setup
# Extract the PostgreSQL connection details from environment variables
user = getenv('FOOTBALL_SCOUT_DEV_PGSQL_USER', 'football_scout_dev')
password = getenv('FOOTBALL_SCOUT_DEV_PGSQL_PWD', '8i0QuEi2hDvNDyUgmQpBY0tA2ztryywF')
host = getenv('FOOTBALL_SCOUT_DEV_PGSQL_HOST', 'dpg-cqarnd08fa8c73asb9h0-a.oregon-postgres.render.com')
database = getenv('FOOTBALL_SCOUT_DEV_PGSQL_DB', 'football_scout_dev_db')

# Create the engine using the PostgreSQL connection string
DATABASE_URL = f'postgresql://{user}:{password}@{host}/{database}'
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session_db = Session()

@app_views.before_request
def load_user():
    user_id = get_current_user_id()  # Function to get the current user ID
    if user_id:
        user = storage.get(User, user_id)
        if user:
            g.user_content = user.to_dict()
        else:
            g.user_content = {}
    else:
        g.user_content = {}

def get_current_user_id():
    """Get the current user ID from the session."""
    return session.get('user_id')


@app_views.route('/comments', methods=['GET'], strict_slashes=False)
def get_comments():
    """Retrieve all comments"""
    comments = storage.all(Comment).values()
    return jsonify([comment.to_dict() for comment in comments])

@app_views.route('/comments/<comment_id>/<post_id>', methods=['GET'], strict_slashes=False)
def get_comment(comment_id, post_id):
    """Retrieve a comment by ID"""
    comment = storage.get(Comment, comment_id)
    # post = storage.get(Post, post_id)
    # comment = session_db.query(Comment).options(
    #    joinedload(Comment.user),
    #    joinedload(Comment.post),
    #    joinedload(Comment.player),
    #    joinedload(Comment.scout)
    # ).filter_by(id=comment_id).first()

    # if comment is None or post is None:
    #    abort(404)

    # comment_dict = comment.to_dict()
    
    # Add related information to the comment dictionary
    # if comment.user:
    #    comment_dict['user'] = comment.user.to_dict()
    # if comment.post:
    #    comment_dict['post'] = comment.post.to_dict()
    # if comment.player:
    #    comment_dict['player'] = comment.player.to_dict()
    # if comment.scout:
    #    comment_dict['scout'] = comment.scout.to_dict()



    # return jsonify(comment.to_dict(), post_id=post_id)
    # return jsonify(comment_dict)

    if not comment:
        abort(404)
    data = comment.to_dict()
    data['post_id'] = post_id
    return jsonify(data)

@app_views.route('/comments/<post_id>', methods=['POST'], strict_slashes=False)
def create_comment(post_id):
    """Create a new comment"""
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    
    logging.debug(f"Received data: {data}")
    text = data.get('text')
    post_id = data.get('post_id')
    user_id = data.get('user_id')
    player_id = data.get('player_id')
    scout_id = data.get('scout_id')

    if not text or not user_id:
        return jsonify({"error": "text or user_id is missing"}), 400

    comment = Comment(text=text, post_id=post_id, user_id=user_id, player_id=player_id, scout_id=scout_id)
    comment.save()
    return jsonify({"message": "Comment posted successfully", "comment": comment.to_dict()}), 201

@app_views.route('/comments/<comment_id>', methods=['PUT'], strict_slashes=False)
def update_comment(comment_id):
    """Update an existing comment"""
    comment = storage.get(Comment, comment_id)
    if comment is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        setattr(comment, key, value)
    comment.save()
    return jsonify(comment.to_dict())

@app_views.route('/comments/<comment_id>', methods=['DELETE'], strict_slashes=False)
def delete_comment(comment_id):
    """Delete a comment"""
    comment = storage.get(Comment, comment_id)
    if comment is None:
        abort(404)
    comment.delete()
    storage.save()
    return jsonify({}), 200

