from flask import Blueprint, jsonify, request, abort
from models import storage
from models.comment import Comment
from api.v1.views import app_views

# app_views = Blueprint('comments', __name__, url_prefix='/api/v1/comments')

@app_views.route('/', methods=['GET'], strict_slashes=False)
def get_comments():
    """Retrieve all comments"""
    comments = storage.all(Comment).values()
    return jsonify([comment.to_dict() for comment in comments])

@app_views.route('/<comment_id>', methods=['GET'], strict_slashes=False)
def get_comment(comment_id):
    """Retrieve a comment by ID"""
    comment = storage.get(Comment, comment_id)
    if comment is None:
        abort(404)
    return jsonify(comment.to_dict())

@app_views.route('/', methods=['POST'], strict_slashes=False)
def create_comment():
    """Create a new comment"""
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    comment = Comment(**data)
    comment.save()
    return jsonify(comment.to_dict()), 201

@app_views.route('/<comment_id>', methods=['PUT'], strict_slashes=False)
def update_comment(comment_id):
    """Update an existing comment"""
    comment = storage.get(Comment, comment_id)
    if comment is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        setattr(comment, key, value)
    comment.save()
    return jsonify(comment.to_dict())

@app_views.route('/<comment_id>', methods=['DELETE'], strict_slashes=False)
def delete_comment(comment_id):
    """Delete a comment"""
    comment = storage.get(Comment, comment_id)
    if comment is None:
        abort(404)
    comment.delete()
    storage.save()
    return jsonify({}), 200

