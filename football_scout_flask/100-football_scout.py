#!/usr/bin/python3
"""
Starts a Flask web application that serves an HTML page similar to 8-index.html.
"""

from flask import Flask, render_template
from models import storage
from models.player import Player
from models.comment import Comment
from models.scout import Scout
from models.club import Club

app = Flask(__name__)

# Teardown SQLAlchemy session
@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

# Route to display 100-hbnb.html
@app.route('/football_scout', strict_slashes=False)
def display_football_scout():
    players = sorted(storage.all(Player).values(), key=lambda p: p.first_name)
    comments = sorted(storage.all(Comment).values(), key=lambda c: c.text)
    scouts = sorted(storage.all(Scout).values(), key=lambda s: s.last_name)
    clubs = sorted(storage.all(Club).values(), key=lambda c: c.name)
    return render_template('100-football_scout.html', players=players, comments=comments, scouts=scouts, clubs=clubs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

