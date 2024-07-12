#!/usr/bin/python3
"""
View module for handling Player objects
"""

from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage, Player, Post

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
    required_fields = ["email", "password", "first_name", "second_name"]
    for field in required_fields:
        if field not in request.json:
            return make_response(jsonify({"error": f"Missing {field}"}), 400)

    player_data = {
        "email": request.json.get("email"),
        "password": request.json.get("password"),
        "first_name": request.json.get("first_name"),
        "second_name": request.json.get("second_name"),
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
