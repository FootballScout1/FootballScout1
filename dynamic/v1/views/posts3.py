#!/usr/bin/python3
"""
View module for handling Post objects
"""

from os import path, getenv
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, g, session, send_from_directory
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
from dynamic.v1.views import app_views
from models import storage, User, UserRoleEnum, Club, Player, Scout, Comment, Post, Like
from console import FootballScoutCommand
import logging
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
import uuid
from dynamic.lazydict import update_obj_dict

logging.basicConfig(level=logging.DEBUG)

# Database setup
db = "sqlite:///footDB.db"
engine = create_engine(db, pool_pre_ping=True)

# Create a session
Session = sessionmaker(bind=engine)
session_db = Session()

@app_views.before_request
def load_user():
    user_id = get_current_user_id()  # Function to get the current user ID
    if user_id:
        user = storage.get(User, user_id)
        if user:
            g.user_content = user.to_dict()
        else:
            g.user_content = {}
    else:
        g.user_content = {}

def get_current_user_id():
    """Get the current user ID from the session."""
    return session.get('user_id')

# Route to render the addpost.html template
@app_views.route('/create_post', methods=['GET'], strict_slashes=False)
def add_post_page():
    """Render the addpost.html template for creating a new post"""
    user_id = get_current_user_id()
    if not user_id:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

    user = storage.get(User, user_id)
    if not user or user.role not in [UserRoleEnum.PLAYER, UserRoleEnum.SCOUT]:
        abort(403)  # Forbidden if the user is not a player or scout

    return render_template('addpost.html', user_id=user_id, content=user.to_dict(), cache_id=uuid.uuid4())

# Route for handling the add post form submission
@app_views.route('/create_post', methods=['POST'], strict_slashes=False)
def create_post():
    """Handle form submission and create a new post"""
    user_id = get_current_user_id()
    if not user_id:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

    user = storage.get(User, user_id)
    if not user or user.role not in [UserRoleEnum.PLAYER, UserRoleEnum.SCOUT]:
        abort(403)  # Forbidden if the user is not a player or scout

    if not request.form:
        abort(400, 'Not a valid form submission')

    data = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'user_id': user_id
    }

    post = Post(**data)
    post.save()

    return redirect(url_for('fetch_post', post_id=post.id))  # Redirect to the newly created post

# Other existing routes...
@app_views.route('/post/<post_id>', strict_slashes=False)
def fetch_post(post_id):
    """
    Renders Post object with its Comment's and Like's
    """
    post = storage.get(Post, post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    post_dict = post.to_dict()
    update_obj_dict(post, post_dict)
    post_dict.update({
        'comments_count': len(post.comments),
        'likes_count': len(post.likes)
    })

    all_comments_dicts = [comment.to_dict() for comment in post.comments]
    all_likes_dicts = [like.to_dict() for like in post.likes]

    return render_template('post.html', comments=all_comments_dicts[:20], likes=all_likes_dicts[:20], post=post_dict, cache_id=uuid.uuid4())

# Additional routes for handling posts, comments, and likes...
@app_views.route('/posts', methods=['GET'], strict_slashes=False)
def get_posts():
    """Retrieve all posts"""
    posts = storage.all(Post).values()
    return jsonify([post.to_dict() for post in posts])

@app_views.route('/posts/<post_id>', methods=['PUT'], strict_slashes=False)
def update_post(post_id):
    """Update an existing post"""
    post = storage.get(Post, post_id)
    if post is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        setattr(post, key, value)
    post.save()
    return jsonify(post.to_dict())

@app_views.route('/posts/<post_id>', methods=['DELETE'], strict_slashes=False)
def delete_post(post_id):
    """Delete a post"""
    post = storage.get(Post, post_id)
    if post is None:
        abort(404)
    post.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/posts/<post_id>/comments', methods=['GET'], strict_slashes=False)
def get_post_comments(post_id):
    """Fetches all comments for a specific post"""
    post = storage.get(Post, post_id)
    if not post:
        abort(404)
    comments = [comment.to_dict() for comment in post.comments]
    return jsonify(comments)

@app_views.route('/posts/<post_id>/comments', methods=['POST'], strict_slashes=False)
def create_post_comment(post_id):
    """Creates a new comment for a specific post"""
    post = storage.get(Post, post_id)
    if not post:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'text' not in data:
        abort(400, description="Missing text")
    data['post_id'] = post_id
    comment = Comment(**data)
    comment.save()
    return jsonify(comment.to_dict()), 201

@app_views.route('/posts/<post_id>/likes', methods=['POST'], strict_slashes=False)
def add_like_to_post(post_id):
    """Adds a like to a specific post"""
    post = storage.get(Post, post_id)
    if not post:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    data['post_id'] = post_id
    like = Like(**data)
    like.save()
    return jsonify(like.to_dict()), 201

@app_views.route('/posts/<post_id>/likes/<like_id>', methods=['DELETE'], strict_slashes=False)
def remove_like_from_post(post_id, like_id):
    """Removes a like from a specific post"""
    post = storage.get(Post, post_id)
    if not post:
        abort(404)
    like = storage.get(Like, like_id)
    if not like:
        abort(404)
    like.delete()
    storage.save()
    return jsonify({}), 200

if __name__ == '__main__':
    app.run(debug=True)

