#!/usr/bin/python3

"""
This is the main file for the Flask application.
"""

from flask import Flask
from models import storage
from dynamic_site.post.post import post
from dynamic_site.homepage.homepage import homepage
from dynamic_site.player_scout.player_scout import info


app = Flask(__name__)
app.register_blueprint(post)
app.register_blueprint(homepage)
app.register_blueprint(info)


@app.teardown_appcontext
def close_session(exception=None):
    """
    Closes the session
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
