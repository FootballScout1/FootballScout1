#!/usr/bin/python3

"""
Module renders dynamic content on homepage
"""

from flask import Blueprint, render_template, abort
from dynamic_site.lazydict import update_obj_dict
from models.post import Post
from models import storage

homepage = Blueprint('homepage', __name__,
                     template_folder='templates')


@homepage.route('/homepage', strict_slashes=False)
def render_homepage():
    """
    Renders the homepage
    """
    try:
        all_posts = list(storage.all(Post).values())
        all_posts_info = list()
        for post in all_posts:
            post_dict = post.to_dict()
            update_obj_dict(post, post_dict)
            post_dict.update({
                'comments_count': len(post.comments),
                'likes_count': len(post.likes)
            })
            all_posts_info.append(post_dict)

        return render_template('homepage.html', posts=all_posts_info[95:105])

    except Exception as e:
        abort(404)
