#!/usr/bin/python3
"""
View module for handling User objects
"""

from flask import Flask, jsonify, request, abort
from dynamic.v1.views import app_views
from models import storage, User

@app_views.route('/users', methods=['GET'])
@app_views.route('/users/', methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users]), 200

@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200

@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a User"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data or 'password' not in data:
        abort(400, 'Missing email or password')
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    # if not user:
    #    abort(404)
    # user.delete()
    # return jsonify({}), 200

    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 204  # Return HTTP 204 No Content for successful deletion
    else:
        return jsonify({"error": "User not found"}), 404  # Handle case where user is not found

