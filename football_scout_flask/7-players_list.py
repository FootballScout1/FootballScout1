#!/usr/bin/python3
""" Starts a Flask Web Application """
from models import storage
from models.player import Player
from flask import Flask, render_template
app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

@app.route('/players_list', strict_slashes=False)
def players_list():
    """ displays a HTML page with a list of players """
    players = storage.all(Player).values()
    players = sorted(players, key=lambda k: k.first_name)
    return render_template('players_list.html', players=players)

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)

