#!/usr/bin/env python3
"""
Makes Post page dynamic
"""
from flask import Flask, render_template
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

fbs = Flask(__name__)


@fbs.route('/post/<post_id>', strict_slashes=False)
def describe_post(post_id):
    """
    Displays a post with its comments
    """
    post = storage.get(Post, post_id)
    post_dict = post.to_dict()
    if post.player_id:
        player = storage.get(Player, post.player_id)
        player_name = player.first_name + " " + player.last_name
        player_position_id = (player.positions)[1].id
        player_position = storage.get(Position, player_position_id).abbrev
        club = storage.get(Club, player.club_id)
        player_club = club.name
        player_country = (storage.get(Country, club.country_id)).name
        post_dict.update({
            'player_name': player_name,
            'player_position': player_position,
            'player_club': player_club,
            'country': player_country,
        })
    else:
        scout = storage.get(Scout, post.scout_id)
        scout_name = scout.first_name + " " + scout.last_name
        club = storage.get(Club, scout.club_id)
        scout_club = club.name
        scout_country = (storage.get(Country, club.country_id)).name
        post_dict.update({
            'scout_name': scout_name,
            'scout_club': scout_club,
            'country': scout_country,
        })
    post_dict.update({
        'comments_count': len(post.comments),
        'likes_count': len(post.likes)
    })

    post_comments = post.comments
    all_comments_dicts = []
    for comment in post_comments:
        comment_dict = comment.to_dict()
        if comment.player_id:
            player = storage.get(Player, comment.player_id)
            player_name = player.first_name + " " + player.last_name
            player_position_id = (player.positions)[1].id
            player_position = storage.get(Position, player_position_id).abbrev
            club = storage.get(Club, player.club_id)
            player_club = club.name
            player_country = (storage.get(Country, club.country_id)).name
            comment_dict.update({
                'player_name': player_name,
                'player_position': player_position,
                'player_club': player_club,
                'country': player_country,
            })
        elif comment.scout_id:
            scout = storage.get(Scout, comment.scout_id)
            scout_name = scout.first_name + " " + scout.last_name
            club = storage.get(Club, player.club_id)
            scout_club = club.name
            scout_country = (storage.get(Country, club.country_id)).name
            comment_dict.update({
                'scout_name': scout_name,
                'scout_club': scout_club,
                'country': scout_country,
            })
        else:
            user = storage.get(User, comment.user_id)
            user_name = user.first_name + " " + user.last_name
            comment_dict.update({
                'user_name': user_name,
            })
        all_comments_dicts.append(comment_dict)

    return render_template('post.html',
                           comments=all_comments_dicts[:20], post=post_dict)


@fbs.teardown_appcontext
def shutdown_session(exception=None):
    storage.close()


if __name__ == "__main__":
    fbs.run(host='0.0.0.0', port=8080, debug=True)
