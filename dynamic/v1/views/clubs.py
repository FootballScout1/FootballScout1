#!/usr/bin/python3
"""
View module for handling Club objects
"""

from os import path, getenv
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, g, session, send_from_directory
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
from dynamic.v1.views import app_views
from models import storage, User, UserRoleEnum, Club, Player, Scout
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

@app_views.route('/clubs', methods=['GET'])
def get_clubs():
    """Retrieves the list of all Club objects"""
    clubs = storage.all(Club).values()
    return jsonify([club.to_dict() for club in clubs])

@app_views.route('/clubs/<club_id>', methods=['GET'])
def get_club(club_id):
    """Retrieves a Club object"""
    club = storage.get(Club, club_id)
    if not club:
        abort(404)
    return jsonify(club.to_dict())

@app_views.route('/clubs/<club_id>', methods=['DELETE'])
def delete_club(club_id):
    """Deletes a Club object"""
    club = storage.get(Club, club_id)
    if not club:
        abort(404)
    club.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/clubs', methods=['POST'])
def create_club():
    """Creates a Club object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    club = Club(**data)
    club.save()
    return jsonify(club.to_dict()), 201

@app_views.route('/clubs/<club_id>', methods=['PUT'])
def update_club(club_id):
    """Updates a Club object"""
    club = storage.get(Club, club_id)
    if not club:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(club, key, value)
    club.save()
    return jsonify(club.to_dict()), 200

@app_views.route('/clubs/<club_id>/players', methods=['GET'])
def get_players_in_club(club_id):
    """Retrieves the list of all Player objects in a club"""
    club = storage.get(Club, club_id)
    if not club:
        abort(404)
    players = [player.to_dict() for player in club.players]
    return jsonify(players)

@app_views.route('/clubs/<club_id>/scouts', methods=['GET'])
def get_scouts_in_club(club_id):
    """Retrieves the list of all Scout objects in a club"""
    club = storage.get(Club, club_id)
    if not club:
        abort(404)
    scouts = [scout.to_dict() for scout in club.scouts]
    return jsonify(scouts)
