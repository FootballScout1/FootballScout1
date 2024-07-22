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

# Database setup
# engine = create_engine('mysql+mysqlconnector://football_scout_dev:football_scout_dev_pwd@localhost/football_scout_dev_db')

# Database setup
# Extract the PostgreSQL connection details from environment variables
# user = getenv('FOOTBALL_SCOUT_DEV_PGSQL_USER', 'football_scout_dev')
# password = getenv('FOOTBALL_SCOUT_DEV_PGSQL_PWD', '8i0QuEi2hDvNDyUgmQpBY0tA2ztryywF')
# host = getenv('FOOTBALL_SCOUT_DEV_PGSQL_HOST', 'dpg-cqarnd08fa8c73asb9h0-a.oregon-postgres.render.com')
# database = getenv('FOOTBALL_SCOUT_DEV_PGSQL_DB', 'football_scout_dev_db')

# Create the engine using the PostgreSQL connection string
# DATABASE_URL = f'postgresql://{user}:{password}@{host}/{database}'
# engine = create_engine(DATABASE_URL)

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

# @app_views.route('/post/<user_id>/<post_id>', strict_slashes=False)
# def fetch_post(user_id, post_id):
@app_views.route('/post/<post_id>', strict_slashes=False)
def fetch_post(post_id):
    """
    Renders Post object with its Comment's and Like's
    """
    # user = storage.get(User, user_id)
    # if not user:
    #    return jsonify({"error": "User not found"}), 404
    post = storage.get(Post, post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    # try:
        # post = storage.get(Post, post_id)
    post_dict = post.to_dict()
    update_obj_dict(post, post_dict)
    post_dict.update({
        'comments_count': len(post.comments),
        'likes_count': len(post.likes)
    })

    # Prepare comments list
    all_comments_dicts = []
    for comment in post.comments:
        comment_dict = comment.to_dict()
        update_obj_dict(comment, comment_dict)
        all_comments_dicts.append(comment_dict)

    # Prepare likes list
    all_likes_dicts = []
    for like in post.likes:
        like_dict = like.to_dict()
        update_obj_dict(like, like_dict)
        all_likes_dicts.append(like_dict)

        # post_comments = post.comments
        # all_comments_dicts = []
        # for comment in post_comments:
        #    comment_dict = comment.to_dict()
        #    update_obj_dict(comment, comment_dict)
        #    all_comments_dicts.append(comment_dict)

        return render_template('post.html', comments=all_comments_dicts[:20], likes=all_likes_dicts[:20], post=post_dict, cache_id=uuid.uuid4())

    # except Exception as e:
    #    abort(404)


@app_views.route('/posts', methods=['GET'], strict_slashes=False)
def get_posts():
    """Retrieve all posts"""
    posts = storage.all(Post).values()
    return jsonify([post.to_dict() for post in posts])

# @app_views.route('/posts/<post_id>', methods=['GET'], strict_slashes=False)
# def get_post(post_id):
#    """Retrieve a post by ID"""
#    post = storage.get(Post, post_id)
#    if post is None:
#        abort(404)
#    return jsonify(post.to_dict())

@app_views.route('/posts', methods=['POST'], strict_slashes=False)
def create_post():
    """Create a new post"""
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    post = Post(**data)
    post.save()
    return jsonify(post.to_dict()), 201

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

# Route to render the static post.html template
# @app.route('/test_post/<user_id>/<post_id>')
# def test_post(user_id, post_id):

    # Fetch user data based on user_id
#    user = storage.get(User, user_id)
#    post = storage.get(Post, post_id)
#    if not user or not post:
#        return "User or Post not found", 404

#    return render_template('post.html', user_id=user_id, post_id=post_id, content=user.to_dict(), cache_id=uuid.uuid4())

# Route for rendering the addpost.html template
# @app.route('/addpost/<user_id>', methods=['GET'])
# def add_post_page(user_id):

#    user = storage.get(User, user_id)
#    if not user:
#        return "User not found", 404
#    return render_template('addpost.html', user_id=user_id, content=user.to_dict(), cache_id=uuid.uuid4())

# Route for handling create icon click, redirects to the addpost page
# @app.route('/create_icon/<user_id>')
# def create_icon(user_id):

#    user = storage.get(User, user_id)
#    if not user:
#        return "User not found", 404
#    return redirect(url_for('add_post_page', user_id=user_id, content=user.to_dict(), cache_id=uuid.uuid4()))  # Redirect to the addpost page

# Route for handling comment icon click, redirects to the comment page
# @app.route('/comment_icon/<user_id>/<post_id>')
# def comment_icon(user_id, post_id):

#    user = storage.get(User, user_id)
#    post = storage.get(Post, post_id)
#    if not user or not post:
#        return "User or Post not found", 404
#    return render_template('comment.html', user_id=user_id, post_id=post_id, content=user.to_dict(), cache_id=uuid.uuid4())

# Route for handling the add post form submission
# @app.route('/addpost/<user_id>', methods=['POST'])
# def add_post(user_id):

#    user = storage.get(User, user_id)
#    if not user:
#        return "User not found", 404
#    return redirect(url_for('test_post', user_id=user_id, content=user.to_dict(), cache_id=uuid.uuid4()))  # Redirect to the posts page

# Route for rendering the comment.html template
# @app.route('/comment/<user_id>/<post_id>')
# def comment_page(user_id, post_id):

    # Fetch user data based on user_id
#    user = storage.get(User, user_id)
#    post = storage.get(Post, post_id)
#    if not user or not post:
#        return "User or Post not found", 404

#    return render_template('comment.html', user_id=user_id, post_id=post_id, content=user.to_dict(), cache_id=uuid.uuid4())

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
