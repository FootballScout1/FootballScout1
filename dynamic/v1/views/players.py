#!/usr/bin/python3
"""
View module for handling Player objects
"""

from os import path, getenv
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, g, session, send_from_directory
from flask import make_response
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
from dynamic.v1.views import app_views
from models import storage, User, UserRoleEnum, Club, Player, Scout, Post, Country
from console import FootballScoutCommand
import logging
from dynamic.lazydict import update_obj_dict
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

@app_views.route('/players', methods=['GET'])
def get_players():
    """Retrieves the list of all Player objects"""
    players = storage.all(Player).values()
    return jsonify([player.to_dict() for player in players])

@app_views.route('/players/<player_id>', methods=['GET'])
def get_player(player_id):
    """Renders a Player info and their Post objects"""
    player = storage.get(Player, player_id)
    if not player:
        abort(404)
    name = player.first_name + " " + player.last_name
    club = storage.get(Club, player.club_id)
    country = storage.get(Country, club.country_id).name
    positions = [pos.name for pos in player.positions]
    player_dict = player.to_dict()
    player_dict.update({
        'player_club': club.name,
        'country': country,
        'player_positions': positions,
        'type': 'player',
        'name': name,
        'profile_picture': player.profile_picture
    })

    all_post_dicts = []
    for post in player.posts:
        post_dict = post.to_dict()
        update_obj_dict(post, post_dict)
        post_dict.update({
            'comments_count': len(post.comments),
            'likes_count': len(post.likes)
        })
        all_post_dicts.append(post_dict)

    return render_template('player_scout.html', user=player_dict,
                               posts=all_post_dicts)


@app_views.route('/players/<player_id>', methods=['DELETE'])
def delete_player(player_id):
    """Deletes a Player object"""
    player = storage.get(Player, player_id)
    if not player:
        abort(404)
    player.delete()
    storage.save()
    return jsonify({}), 200

# @app_views.route('/players', methods=['POST'])
# def create_player():
#    """Creates a Player object"""
#    if not request.get_json():
#        abort(400, description="Not a JSON")
#    data = request.get_json()
#    if 'name' not in data:
#        abort(400, description="Missing name")
#    player = Player(**data)
#    player.save()
#    return jsonify(player.to_dict()), 201
def create_player():
    """Creates a new Player"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Ensure required fields are present
    required_fields = ["email", "password", "first_name", "last_name"]
    for field in required_fields:
        if field not in request.json:
            return make_response(jsonify({"error": f"Missing {field}"}), 400)

    player_data = {
        "email": request.json.get("email"),
        "password": request.json.get("password"),
        "first_name": request.json.get("first_name"),
        "last_name": request.json.get("last_name"),
        "nationality": request.json.get("nationality", ""),
        "position": request.json.get("position", ""),
        "height": request.json.get("height", 0),
        "weight": request.json.get("weight", 0),
        "club_id": request.json.get("club_id", "")
    }

    new_player = Player(**player_data)
    new_player.save()
    return make_response(jsonify(new_player.to_dict()), 201)

@app_views.route('/players/<player_id>', methods=['PUT'])
def update_player(player_id):
    """Updates a Player object"""
    player = storage.get(Player, player_id)
    if not player:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(player, key, value)
    player.save()
    return jsonify(player.to_dict()), 200

@app_views.route('/players/<player_id>/posts', methods=['GET'])
def get_player_posts(player_id):
    """Fetches all posts made by a specific player"""
    player = storage.get(Player, player_id)
    if not player:
        abort(404)
    posts = [post.to_dict() for post in player.posts]
    return jsonify(posts)

@app_views.route('/players/<player_id>/posts', methods=['POST'])
def create_player_post(player_id):
    """Creates a new post for a specific player"""
    player = storage.get(Player, player_id)
    if not player:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'content' not in data:
        abort(400, description="Missing content")
    data['player_id'] = player_id
    post = Post(**data)
    post.save()
    return jsonify(post.to_dict()), 201
