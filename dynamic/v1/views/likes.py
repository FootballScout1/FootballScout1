#!/usr/bin/python3
"""
View module for handling Like objects
"""

from os import path, getenv
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, g, session, send_from_directory
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
from dynamic.v1.views import app_views
from models import storage, User, UserRoleEnum, Club, Player, Scout, Like
from console import FootballScoutCommand
import logging
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
import uuid
from dynamic.v1 import Session

logging.basicConfig(level=logging.DEBUG)

# Database setup
# db = "sqlite:///footDB.db"
# engine = create_engine(db, pool_pre_ping=True)

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
# Session = sessionmaker(bind=engine)
session_db = Session()

#@app_views.before_request
#def load_user():
#    user_id = get_current_user_id()  # Function to get the current user ID
#    if user_id:
#        user = storage.get(User, user_id)
#        if user:
#            g.user_content = user.to_dict()
#        else:
#            g.user_content = {}
#    else:
#        g.user_content = {}
#
#def get_current_user_id():
#    """Get the current user ID from the session."""
#    return session.get('user_id')

@app_views.route('/likes', methods=['GET'], strict_slashes=False)
def get_likes():
    """Retrieve all likes"""
    likes = storage.all(Like).values()
    return jsonify([like.to_dict() for like in likes])

@app_views.route('/likes/<like_id>', methods=['GET'], strict_slashes=False)
def get_like(like_id):
    """Retrieve a like by ID"""
    like = storage.get(Like, like_id)
    if like is None:
        abort(404)
    return jsonify(like.to_dict())

@app_views.route('/likes', methods=['POST'], strict_slashes=False)
def create_like():
    """Create a new like"""
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    like = Like(**data)
    like.save()
    return jsonify(like.to_dict()), 201

@app_views.route('/likes/<like_id>', methods=['PUT'], strict_slashes=False)
def update_like(like_id):
    """Update an existing like"""
    like = storage.get(Like, like_id)
    if like is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        setattr(like, key, value)
    like.save()
    return jsonify(like.to_dict())

@app_views.route('/likes/<like_id>', methods=['DELETE'], strict_slashes=False)
def delete_like(like_id):
    """Delete a like"""
    like = storage.get(Like, like_id)
    if like is None:
        abort(404)
    like.delete()
    storage.save()
    return jsonify({}), 200

