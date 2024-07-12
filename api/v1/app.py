#!/usr/bin/python3
"""
Flask App for Football Scout project
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from dotenv import load_dotenv
from werkzeug.exceptions import NotFound
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

# Allow CORS for all domains
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Close storage session"""
    storage.close()

# Custom 404 error handler
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

# Sample route to demonstrate 404 handling
@app.route('/api/v1/sample')
def sample_route():
    # Example route
    return jsonify({"message": "This is a sample route"}), 200


if __name__ == "__main__":
    host = getenv('FOOTBALL_SCOUT_API_HOST', '0.0.0.0')
    port = int(getenv('FOOTBALL_SCOUT_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)

