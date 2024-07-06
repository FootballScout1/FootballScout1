#!/usr/bin/python3
"""
View module for handling Scout objects
"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage, Scout

@app_views.route('/scouts', methods=['GET'])
def get_scouts():
    """Retrieves the list of all Scout objects"""
    scouts = storage.all(Scout).values()
    return jsonify([scout.to_dict() for scout in scouts])

@app_views.route('/scouts/<scout_id>', methods=['GET'])
def get_scout(scout_id):
    """Retrieves a Scout object"""
    scout = storage.get(Scout, scout_id)
    if not scout:
        abort(404)
    return jsonify(scout.to_dict())

@app_views.route('/scouts/<scout_id>', methods=['DELETE'])
def delete_scout(scout_id):
    """Deletes a Scout object"""
    scout = storage.get(Scout, scout_id)
    if not scout:
        abort(404)
    scout.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/scouts', methods=['POST'])
def create_scout():
    """Creates a Scout object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    scout = Scout(**data)
    scout.save()
    return jsonify(scout.to_dict()), 201

@app_views.route('/scouts/<scout_id>', methods=['PUT'])
def update_scout(scout_id):
    """Updates a Scout object"""
    scout = storage.get(Scout, scout_id)
    if not scout:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(scout, key, value)
    scout.save()
    return jsonify(scout.to_dict()), 200

