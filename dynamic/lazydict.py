#!/usr/bin/python3

"""
Module defines a quick method to update all dicts with user information
"""

from models import storage
from models.scout import Scout
from models.player import Player
from models.club import Club
from models.country import Country
from models.post import Post
from models.like import Like
from models.comment import Comment
from models.position import Position
from models.user import User


def update_obj_dict(obj, obj_dict):
    """
    Updates the object dictionary with additional user information
    """
    id_to_cls = {
        'player_id': ['player', Player],
        'scout_id': ['scout', Scout],
        'user_id': ['user', User]
    }

    _id = next((key for key in id_to_cls if key in obj_dict and obj_dict[key] is not None), None)

    if not _id:
        return

    user = storage.get(id_to_cls[_id][1], obj_dict[_id])
    if not user:
        return


    user_name = user.first_name + " " + user.last_name
    obj_dict.update({f'{id_to_cls[_id][0]}_name': user_name})

    if obj_dict.get('user_id') is None:
        user_club = storage.get(Club, user.club_id)
        country = storage.get(Country, user_club.country_id).name
        obj_dict.update({
            f'{id_to_cls[_id][0]}_club': user_club.name,
            'country': country
        })

    if obj.player_id:
        positions = [pos.abbrev for pos in user.positions]
        obj_dict.update({'player_positions': positions})
    del_keys = list()
    for key in obj_dict:
        if obj_dict.get(key) is None:
            del_keys.append(key)
    for key in del_keys:
        obj_dict.pop(key)
