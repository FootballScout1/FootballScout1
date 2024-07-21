#!/usr/bin/python3
"""
Defines the RESTful API actions for Player objects
"""
from flask import jsonify, abort, request
from dynamic.v1.views import app_views
from models import storage
from models.player import Player
from models.club import Club
from models.scout import Scout
from models.user import User

@app_views.route('/players_search', methods=['POST'], strict_slashes=False)
def players_search():
    """
    Retrieves all Player objects depending on the JSON in the request body
    """
    if not request.is_json:
        abort(400, description="Not a JSON")

    search_dict = request.get_json()
    if not search_dict:
        players = storage.all(Player).values()
        return jsonify([player.to_dict() for player in players])

    clubs = search_dict.get('clubs', [])
    scouts = search_dict.get('scouts', [])
    users = search_dict.get('users', [])

    players = set()

    if clubs:
        for club_id in clubs:
            club = storage.get(Club, club_id)
            if club:
                for player in club.players:
                    players.add(player)

    if scouts:
        for scout_id in scouts:
            scout = storage.get(Scout, scout_id)
            if scout:
                for player in scout.players:
                    players.add(player)

    if users:
        for user_id in users:
            user = storage.get(User, user_id)
            if user:
                for player in user.players:
                    players.add(player)

    return jsonify([player.to_dict() for player in players])


