#!/usr/bin/python3
"""
View module for handling User objects
"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage, User

@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])

@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a User object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    
    # Upgrade user to scout or player
    if 'role' in data:
        role = data['role']
        if role == 'scout':
            # Check if user is already a scout
            if not isinstance(user, Scout):
                scout = Scout(**user.to_dict())
                scout.save()
                user.delete()
                storage.save()
                return jsonify(scout.to_dict()), 200
            else:
                return jsonify(user.to_dict()), 200
        elif role == 'player':
            # Check if user is already a player
            if not isinstance(user, Player):
                player = Player(**user.to_dict())
                player.save()
                user.delete()
                storage.save()
                return jsonify(player.to_dict()), 200
            else:
                return jsonify(user.to_dict()), 200
        else:
            abort(400, description="Invalid role")


    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200

