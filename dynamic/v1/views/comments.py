#!/usr/bin/python3
"""
View module for handling User objects
"""

from os import path, getenv
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, g, session, send_from_directory
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
from dynamic.v1.views import app_views
from models import storage, User, UserRoleEnum, Club, Player, Scout
from models.comment import Comment
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


# from flask import Blueprint, jsonify, request, abort
# from models import storage
# from models.comment import Comment
# from dynamic.v1.views import app_views

# app_views = Blueprint('comments', __name__, url_prefix='/api/v1/comments')

@app_views.route('/', methods=['GET'], strict_slashes=False)
def get_comments():
    """Retrieve all comments"""
    comments = storage.all(Comment).values()
    return jsonify([comment.to_dict() for comment in comments])

@app_views.route('/<comment_id>', methods=['GET'], strict_slashes=False)
def get_comment(comment_id):
    """Retrieve a comment by ID"""
    comment = storage.get(Comment, comment_id)
    if comment is None:
        abort(404)
    return jsonify(comment.to_dict())

@app_views.route('/', methods=['POST'], strict_slashes=False)
def create_comment():
    """Create a new comment"""
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    comment = Comment(**data)
    comment.save()
    return jsonify(comment.to_dict()), 201

@app_views.route('/<comment_id>', methods=['PUT'], strict_slashes=False)
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

@app_views.route('/<comment_id>', methods=['DELETE'], strict_slashes=False)
def delete_comment(comment_id):
    """Delete a comment"""
    comment = storage.get(Comment, comment_id)
    if comment is None:
        abort(404)
    comment.delete()
    storage.save()
    return jsonify({}), 200

