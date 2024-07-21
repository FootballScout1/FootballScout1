#!/usr/bin/python3
"""
Defines the RESTful API actions for Player objects (Search)
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

@app_views.route('/players_search', methods=['POST'], strict_slashes=False)
def players_search():
    """
    Retrieves all Player objects depending on the JSON in the request body
    """
    if not request.is_json:
        abort(400, description="Not a JSON")

    search_dict = request.get_json()
    if not search_dict:
        players = storage.all(Player).values()
        return jsonify([player.to_dict() for player in players])

    clubs = search_dict.get('clubs', [])
    scouts = search_dict.get('scouts', [])
    users = search_dict.get('users', [])

    players = set()

    if clubs:
        for club_id in clubs:
            club = storage.get(Club, club_id)
            if club:
                for player in club.players:
                    players.add(player)

    if scouts:
        for scout_id in scouts:
            scout = storage.get(Scout, scout_id)
            if scout:
                for player in scout.players:
                    players.add(player)

    if users:
        for user_id in users:
            user = storage.get(User, user_id)
            if user:
                for player in user.players:
                    players.add(player)

    return jsonify([player.to_dict() for player in players])


