#!/usr/bin/python3

"""
Module renders a Post and its comments dynamically
"""
from flask import render_template, Blueprint, abort
from models import storage
from dynamic_site.lazydict import update_obj_dict
from models.post import Post


post = Blueprint('post', __name__,
                 template_folder='templates')


@post.route('/post/<post_id>', strict_slashes=False)
def fetch_post(post_id):
    """
    Renders Post object with its Comment's and Like's
    """
    try:
        post = storage.get(Post, post_id)
        post_dict = post.to_dict()
        update_obj_dict(post, post_dict)
        post_dict.update({
            'comments_count': len(post.comments),
            'likes_count': len(post.likes)
        })

        post_comments = post.comments
        all_comments_dicts = []
        for comment in post_comments:
            comment_dict = comment.to_dict()
            update_obj_dict(comment, comment_dict)
            all_comments_dicts.append(comment_dict)

        return render_template('post.html',
                               comments=all_comments_dicts[:20], post=post_dict)

    except Exception as e:
        abort(404)
