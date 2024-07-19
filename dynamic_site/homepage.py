#!/usr/bin/env python3
"""
Renders posts dynamically on the site homepage
"""
from flask import Flask, render_template
from random import sample
from models import storage
from models.post import Post
from models.scout import Scout
from models.player import Player
from models.position import Position
from models.club import Club
from models.country import Country

fbs = Flask(__name__)


@fbs.route('/homepage', strict_slashes=False)
def render_homepage():
    all_posts = list(storage.all(Post).values())
    all_posts_info = list()
    for post in all_posts:
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
            club = storage.get(Club, player.club_id)
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
        all_posts_info.append(post_dict)

    return render_template('homepage.html', posts=all_posts_info[95:105])


@fbs.teardown_appcontext
def shutdown_session(exception=None):
    storage.close()


if __name__ == "__main__":
    fbs.run(host='0.0.0.0', port=8080, debug=True)
