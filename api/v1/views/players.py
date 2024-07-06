#!/usr/bin/python3
"""
View module for handling Player objects
"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage, Player

@app_views.route('/players', methods=['GET'])
def get_players():
    """Retrieves the list of all Player objects"""
    players = storage.all(Player).values()
    return jsonify([player.to_dict() for player in players])

@app_views.route('/players/<player_id>', methods=['GET'])
def get_player(player_id):
    """Retrieves a Player object"""
    player = storage.get(Player, player_id)
    if not player:
        abort(404)
    return jsonify(player.to_dict())

@app_views.route('/players/<player_id>', methods=['DELETE'])
def delete_player(player_id):
    """Deletes a Player object"""
    player = storage.get(Player, player_id)
    if not player:
        abort(404)
    player.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/players', methods=['POST'])
def create_player():
    """Creates a Player object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    player = Player(**data)
    player.save()
    return jsonify(player.to_dict()), 201

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

