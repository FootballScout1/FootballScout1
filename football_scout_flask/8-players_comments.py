#!/usr/bin/python3
""" Starts a Flask Web Application to display players and comments """
from flask import Flask, render_template
import models
# from models import storage_t
from models.player import Player
from models.comment import Comment

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """ Removes the current SQLAlchemy Session """
    models.storage.close()


@app.route('/players_comments', strict_slashes=False)
def players_comments():
    """ Displays HTML page with list of players and their comments """
    players = models.storage.all(Player).values()

    return render_template('8-players_comments.html', players=players)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

