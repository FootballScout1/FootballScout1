from flask import Blueprint, jsonify, request, abort
from models import storage
from models.post import Post
from models.comment import Comment
from models.like import Like
from dynamic.v1.views import app_views

# app_views = Blueprint('posts', __name__, url_prefix='/api/v1/posts')

@app_views.route('/posts', methods=['GET'], strict_slashes=False)
def get_posts():
    """Retrieve all posts"""
    posts = storage.all(Post).values()
    return jsonify([post.to_dict() for post in posts])

@app_views.route('/posts/<post_id>', methods=['GET'], strict_slashes=False)
def get_post(post_id):
    """Retrieve a post by ID"""
    post = storage.get(Post, post_id)
    if post is None:
        abort(404)
    return jsonify(post.to_dict())

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
