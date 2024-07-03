#!/usr/bin/python3
"""Starts a Flask web application to display a page with filters."""
from flask import Flask, render_template
from models import storage
from models.club import Club
from models.player import Player

app = Flask(__name__)

@app.teardown_appcontext
def teardown(exception):
    """Removes the current SQLAlchemy Session"""
    storage.close()

@app.route('/scout_filters', strict_slashes=False)
def scout_filters():
    """Displays a HTML page with clubs and players filters"""
    clubs = sorted(storage.all(Club).values(), key=lambda c: c.name)
    players = sorted(storage.all(Player).values(), key=lambda p: p.first_name) # Sort by first_name for consistency

    # Modify each player object to have a 'name' attribute based on first_name and last_name
    for player in players:
        player.name = f"{player.first_name} {player.last_name}"

    return render_template('10-scout_filters.html', clubs=clubs, players=players)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

