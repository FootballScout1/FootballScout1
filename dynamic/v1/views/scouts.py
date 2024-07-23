#!/usr/bin/python3
"""
View module for handling Scout objects
"""

from os import path, getenv
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, g, session, send_from_directory
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
from dynamic.v1.views import app_views
from models import storage, User, UserRoleEnum, Club, Player, Scout
from console import FootballScoutCommand
from models.country import Country
from dynamic.lazydict import update_obj_dict
import logging
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
import uuid

from datetime import datetime  # Import datetime module
from sqlalchemy.exc import IntegrityError  # Import IntegrityError

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

@app_views.route('/scouts', methods=['GET'])
def get_scouts():
    """Retrieves the list of all Scout objects"""
    scouts = storage.all(Scout).values()
    return jsonify([scout.to_dict() for scout in scouts])

@app_views.route('/scouts/<scout_id>', methods=['GET'])
def get_scout_info(scout_id):
    """Renders a Scout info and their Post objects"""
    scout = storage.get(Scout, scout_id)
    if not scout:
        abort(404)

    name = scout.first_name + " " + scout.last_name
    club = storage.get(Club, scout.club_id)
    country = storage.get(Country, club.country_id).name
    scout_dict = scout.to_dict()
    scout_dict.update({
        'scout_club': club.name,
        'country': country,
        'type': 'scout',
        'name': name,
        'profile_picture': scout.profile_picture
    })

    all_post_dicts = []
    for post in scout.posts:
        post_dict = post.to_dict()
        update_obj_dict(post, post_dict)
        post_dict.update({
            'comments_count': len(post.comments),
            'likes_count': len(post.likes)
        })
        all_post_dicts.append(post_dict)

    return render_template('player_scout.html', user=scout_dict,
                               posts=all_post_dicts)

@app_views.route('/scouts/<scout_id>', methods=['DELETE'])
def delete_scout(scout_id):
    """Deletes a Scout object"""
    scout = storage.get(Scout, scout_id)
    if not scout:
        abort(404)
    scout.delete()
    storage.save()
    return jsonify({}), 200

#@app_views.route('/scouts', methods=['POST'])
#def create_scout():
#    """Creates a Scout object"""
#    if not request.get_json():
#        abort(400, description="Not a JSON")
#    # data = request.get_json()
#    # if 'first_name' not in data or 'last_name' not in data:
#    #    abort(400, description="Missing first_name or last_name")
#    # if 'name' not in data:
#        # abort(400, description="Missing name")
#    # scout = Scout(**data)
#    # scout.save()
#    # return jsonify(scout.to_dict()), 201
#
#    data = request.get_json()
#
#    # Check for required fields
#    # required_fields = ['club_id', 'first_name', 'last_name', 'email', 'password']
#    required_fields = ['user_id', 'club_id']  # Add user_id to link to existing user
#    for field in required_fields:
#        if field not in data:
#            abort(400, description=f"Missing {field}")
#
#    # Generate a new unique ID for the scout if needed
#    # scout_id = data.get('id')
#    # if not scout_id:
#    #    scout_id = str(uuid.uuid4())  # Generate a new UUID
#
#    # Retrieve the user by user_id
#    user = storage.get(User, data['user_id'])
#    if not user:
#        abort(404, description="User not found")
#
#     # Check if user is already a scout
#    if user.role == 'scout':
#        abort(400, description="User is already a scout")
#
#    try:
#        # Switch user role to scout and transfer data
#        user.switch_role('scout')
#
#        # Create a new scout instance
#        new_scout = Scout(
#            email=user.email,
#            password=user.password,
#            first_name=user.first_name,
#            last_name=user.last_name,
#            club_id=data['club_id'],
#            created_at=datetime.utcnow(),
#            updated_at=datetime.utcnow()
#        )
#        new_scout.save()
#
#        return jsonify({"message": "Scout created successfully!"}), 201
#    except ValueError as e:
#        abort(400, description=str(e))
    
    # Create a new scout instance
    # new_scout = Scout(
    #    id=scout_id,
    #    club_id=data['club_id'],
    #    first_name=data['first_name'],
    #    last_name=data['last_name'],
    #    email=data['email'],
    #    password=data['password'],
    #    created_at=datetime.utcnow(),
    #    updated_at=datetime.utcnow()
    # )

    # try:
        # Add new scout to the database
        # storage.new(new_scout)
        # storage.save()
    #    new_scout.save()
        # return jsonify({"message": "Scout created successfully!"}), 201
    #    return jsonify(new_scout.to_dict()), 201
    # except IntegrityError as e:
    #    storage.rollback()
    #    abort(400, description=str(e))
        # return jsonify({"error": str(e.orig)}), 400

#@app_views.route('/scouts/<scout_id>', methods=['PUT'])
#def update_scout(scout_id):
#    """Updates a Scout object"""
#    scout = storage.get(Scout, scout_id)
#    if not scout:
#        abort(404)
#    if not request.get_json():
#        abort(400, description="Not a JSON")
#    data = request.get_json()
#    ignore_keys = ['id', 'created_at', 'updated_at']
#    for key, value in data.items():
#        if key not in ignore_keys:
#            setattr(scout, key, value)
#    scout.save()
#    return jsonify(scout.to_dict()), 200

@app_views.route('/scouts/<scout_id>/players', methods=['GET'])
def get_scouted_players(scout_id):
    """Retrieve the list of players being scouted by a specific scout"""
    scout = storage.get(Scout, scout_id)
    if not scout:
        abort(404)
    players = [player.to_dict() for player in scout.players]
    return jsonify(players)

@app_views.route('/scouts/<scout_id>/players/<player_id>', methods=['POST'])
def start_scouting_player(scout_id, player_id):
    """Start scouting a player (bookmark functionality)"""
    scout = storage.get(Scout, scout_id)
    if not scout:
        abort(404)
    player = storage.get(Player, player_id)
    if not player:
        abort(404)
    if player not in scout.players:
        scout.players.append(player)
        scout.save()
    return jsonify(scout.to_dict()), 200

@app_views.route('/scouts/<scout_id>/players/<player_id>', methods=['DELETE'])
def stop_scouting_player(scout_id, player_id):
    """Stop scouting a player"""
    scout = storage.get(Scout, scout_id)
    if not scout:
        abort(404)
    player = storage.get(Player, player_id)
    if not player:
        abort(404)
    if player in scout.players:
        scout.players.remove(player)
        scout.save()
    return jsonify(scout.to_dict()), 200
