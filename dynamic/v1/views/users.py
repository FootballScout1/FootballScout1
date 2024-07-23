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

@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)

@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a User"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.json:
        abort(400, 'Missing password')
    new_user = User(**request.json)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})

@app_views.route('/users/<user_id>/profile_picture', methods=['POST'])
def upload_profile_picture(user_id):
    """Upload a profile picture for a user"""
    from dynamic.v1.app import app
    user = storage.get(User, user_id)
    if user:
        user_type = 'user'
    else:
        player = storage.get(Player, user_id)
        if player:
            user = player
            user_type = 'player'
        else:
            scout = storage.get(Scout, user_id)
            if scout:
                user = scout
                user_type = 'scout'
            else:
                abort(404)

    if 'profile_picture' not in request.files:
        logging.debug("No profile picture in request files")
        return jsonify({"error": "No profile picture in request files"}), 400

    file = request.files['profile_picture']
    if file.filename == '':
        logging.debug("Empty filename")
        return jsonify({"error": "Empty filename"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = path.join(app.config['UPLOAD_FOLDER'], filename)
        logging.debug(f"Saving file to {filepath}")
        file.save(filepath)

        # Update user's profile picture path in the database
        user.profile_picture = filename
        user.save()

        logging.debug(f"Updating user {user.first_name} profile picture to {filename}")
        # return jsonify(user.to_dict())
        return redirect(url_for('app_views.profile', user_id=user.id, cache_id=uuid.uuid4()))

    logging.debug("File type not allowed or file is invalid")
    return jsonify({"error": "File type not allowed or file is invalid"}), 400

def allowed_file(filename):
    """Check if the file is an allowed type"""
    from dynamic.v1.app import app
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app_views.route('/profile/<user_id>', methods=['GET'])
def profile(user_id):
    # Fetch user data based on user_id
    user = storage.get(User, user_id)
    if user:
        # return "User not found", 404
        return render_template('profile.html', content=user.to_dict(), user_type='user', cache_id=uuid.uuid4())
    # Fetch player data based on user_id
    player = storage.get(Player, user_id)
    if player:
        return render_template('profile.html', content=player.to_dict(), user_type='player', cache_id=uuid.uuid4())

    # Fetch scout data based on user_id
    scout = storage.get(Scout, user_id)
    if scout:
        return render_template('profile.html', content=scout.to_dict(), user_type='scout', cache_id=uuid.uuid4())

    # If none of the data is found, return an error
    return "User not found", 404

# Route for serving uploaded profile pictures
@app_views.route('/uploads/<filename>')
def uploaded_file(filename):
    from dynamic.v1.app import app
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
