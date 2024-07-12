from flask import Blueprint, jsonify, request, abort
from models import storage
from models.like import Like
from api.v1.views import app_views

# app_views = Blueprint('likes', __name__, url_prefix='/api/v1/likes')

@app_views.route('/', methods=['GET'], strict_slashes=False)
def get_likes():
    """Retrieve all likes"""
    likes = storage.all(Like).values()
    return jsonify([like.to_dict() for like in likes])

@app_views.route('/<like_id>', methods=['GET'], strict_slashes=False)
def get_like(like_id):
    """Retrieve a like by ID"""
    like = storage.get(Like, like_id)
    if like is None:
        abort(404)
    return jsonify(like.to_dict())

@app_views.route('/', methods=['POST'], strict_slashes=False)
def create_like():
    """Create a new like"""
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    like = Like(**data)
    like.save()
    return jsonify(like.to_dict()), 201

@app_views.route('/<like_id>', methods=['PUT'], strict_slashes=False)
def update_like(like_id):
    """Update an existing like"""
    like = storage.get(Like, like_id)
    if like is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        setattr(like, key, value)
    like.save()
    return jsonify(like.to_dict())

@app_views.route('/<like_id>', methods=['DELETE'], strict_slashes=False)
def delete_like(like_id):
    """Delete a like"""
    like = storage.get(Like, like_id)
    if like is None:
        abort(404)
    like.delete()
    storage.save()
    return jsonify({}), 200

