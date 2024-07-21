from flask import jsonify
from dynamic.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Returns the number of each objects by type"""
    stats = storage.count()
    return jsonify(stats)

