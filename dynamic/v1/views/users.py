# dynamic/v1/views/users.py

#!/usr/bin/python3
"""
View module for handling User objects
"""

from os import path
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, g, session
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
from dynamic.v1.views import app_views
from models import storage, User, UserRoleEnum, Club, Player, Scout
from console import FootballScoutCommand
import logging
from sqlalchemy.orm import sessionmaker
from models.base_model import Base

logging.basicConfig(level=logging.DEBUG)

# Database setup
db = "sqlite:///footDB.db"
engine = create_engine(db, pool_pre_ping=True)

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
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if 'file' not in request.files:
        abort(400, 'No file part')
    file = request.files['file']
    if file.filename == '':
        abort(400, 'No selected file')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
        user.profile_picture = filename
        storage.save()
        return jsonify(user.to_dict()), 200

    abort(400, 'File type not allowed')

def allowed_file(filename):
    """Check if the file is an allowed type"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app_views.route('/profile/<user_id>', methods=['GET'])
def profile(user_id):
    # Fetch user data based on user_id
    user = storage.get(User, user_id)
    if not user:
        return "User not found", 404
    return render_template('profile.html', content=user.to_dict())
