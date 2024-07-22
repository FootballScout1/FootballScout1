#!/usr/bin/python3
"""
Module renders a quick info page for a player or a scout
"""
from os import path, getenv
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, g, session, send_from_directory
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
from dynamic.v1.views import app_views
from models import storage, User, UserRoleEnum, Club, Player, Scout
from models.country import Country
from dynamic.lazydict import update_obj_dict
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

@app_views.route('/player/<player_id>', strict_slashes=False)
def fetch_player(player_id):
    """
    Renders a Player info and their Post objects
    """
    
    try:
        player = storage.get(Player, player_id)
        if not player:
            raise ValueError(f"Player with ID {player_id} not found")

    # try:
        player = storage.get(Player, player_id)
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

    except Exception as e:
        abort(404)


@app_views.route('/scout/<scout_id>', strict_slashes=False)
def fetch_scout(scout_id):
    """
    Renders a Scout info and their Post objects
    """

    try:
        scout = storage.get(Scout, scout_id)
        if not player:
            raise ValueError(f"Scout with ID {scout_id} not found")

    # try:    
        scout = storage.get(Scout, scout_id)
        name = scout.first_name + " " + scout.last_name
        club = storage.get(Club, scout.club_id)
        country = storage.get(Country, club.country_id).name
        scout_dict = scout.to_dict()
        scout_dict.update({
            'scout_club': club.name,
            'country': country,
            'type': 'scout',
            'name': name,
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

    except Exception as e:
        abort(404)
