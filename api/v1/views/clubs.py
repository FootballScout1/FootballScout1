#!/usr/bin/python3
"""
View module for handling Club objects
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.club import Club

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

