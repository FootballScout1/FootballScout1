#!/usr/bin/python3
"""
View module for handling Post objects
"""

from os import path, getenv
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, g, session, send_from_directory
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
from dynamic.v1.views import app_views
from models import storage, User, UserRoleEnum, Club, Player, Scout, Comment, Post, Like
from console import FootballScoutCommand
import logging
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
import uuid

logging.basicConfig(level=logging.DEBUG)

# Database setup
db = "sqlite:///footDB.db"
engine = create_engine(db, pool_pre_ping=True)

# Database setup
# engine = create_engine('mysql+mysqlconnector://football_scout_dev:football_scout_dev_pwd@localhost/football_scout_dev_db')

# Database setup
# Extract the PostgreSQL connection details from environment variables
# user = getenv('FOOTBALL_SCOUT_DEV_PGSQL_USER', 'football_scout_dev')
# password = getenv('FOOTBALL_SCOUT_DEV_PGSQL_PWD', '8i0QuEi2hDvNDyUgmQpBY0tA2ztryywF')
# host = getenv('FOOTBALL_SCOUT_DEV_PGSQL_HOST', 'dpg-cqarnd08fa8c73asb9h0-a.oregon-postgres.render.com')
# database = getenv('FOOTBALL_SCOUT_DEV_PGSQL_DB', 'football_scout_dev_db')

# Create the engine using the PostgreSQL connection string
# DATABASE_URL = f'postgresql://{user}:{password}@{host}/{database}'
# engine = create_engine(DATABASE_URL)

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

@app_views.route('/posts', methods=['GET'], strict_slashes=False)
def get_posts():
    """Retrieve all posts"""
    posts = storage.all(Post).values()
    return jsonify([post.to_dict() for post in posts])

@app_views.route('/posts/<post_id>', methods=['GET'], strict_slashes=False)
def get_post(post_id):
    """Retrieve a post by ID"""
    post = storage.get(Post, post_id)
    if post is None:
        abort(404)
    return jsonify(post.to_dict())

@app_views.route('/posts', methods=['POST'], strict_slashes=False)
def create_post():
    """Create a new post"""
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    post = Post(**data)
    post.save()
    return jsonify(post.to_dict()), 201

@app_views.route('/posts/<post_id>', methods=['PUT'], strict_slashes=False)
def update_post(post_id):
    """Update an existing post"""
    post = storage.get(Post, post_id)
    if post is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        setattr(post, key, value)
    post.save()
    return jsonify(post.to_dict())

@app_views.route('/posts/<post_id>', methods=['DELETE'], strict_slashes=False)
def delete_post(post_id):
    """Delete a post"""
    post = storage.get(Post, post_id)
    if post is None:
        abort(404)
    post.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/posts/<post_id>/comments', methods=['GET'], strict_slashes=False)
def get_post_comments(post_id):
    """Fetches all comments for a specific post"""
    post = storage.get(Post, post_id)
    if not post:
        abort(404)
    comments = [comment.to_dict() for comment in post.comments]
    return jsonify(comments)

@app_views.route('/posts/<post_id>/comments', methods=['POST'], strict_slashes=False)
def create_post_comment(post_id):
    """Creates a new comment for a specific post"""
    post = storage.get(Post, post_id)
    if not post:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'text' not in data:
        abort(400, description="Missing text")
    data['post_id'] = post_id
    comment = Comment(**data)
    comment.save()
    return jsonify(comment.to_dict()), 201

@app_views.route('/posts/<post_id>/likes', methods=['POST'], strict_slashes=False)
def add_like_to_post(post_id):
    """Adds a like to a specific post"""
    post = storage.get(Post, post_id)
    if not post:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    data['post_id'] = post_id
    like = Like(**data)
    like.save()
    return jsonify(like.to_dict()), 201

@app_views.route('/posts/<post_id>/likes/<like_id>', methods=['DELETE'], strict_slashes=False)
def remove_like_from_post(post_id, like_id):
    """Removes a like from a specific post"""
    post = storage.get(Post, post_id)
    if not post:
        abort(404)
    like = storage.get(Like, like_id)
    if not like:
        abort(404)
    like.delete()
    storage.save()
    return jsonify({}), 200
