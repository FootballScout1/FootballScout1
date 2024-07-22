#!/usr/bin/python3

"""
Module renders a quick info page for a player or a scout
"""

from flask import abort, render_template, Blueprint
from models import storage
from models.country import Country
from models.player import Player
from models.scout import Scout
from models.club import Club
from dynamic_site.lazydict import update_obj_dict

info = Blueprint('info', __name__,
                 template_folder='templates')


@info.route('/player/<player_id>', strict_slashes=False)
def fetch_player(player_id):
    """
    Renders a Player info and their Post objects
    """
    try:
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


@info.route('/scout/<scout_id>', strict_slashes=False)
def fetch_scout(scout_id):
    """
    Renders a Scout info and their Post objects
    """
    try:
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
