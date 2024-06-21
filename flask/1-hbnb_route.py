#!/usr/bin/python3
""" Starts a Flask Web Application Football Scout"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_football_scout():
    """ Prints a Message when / is called """
    return 'Hello Football Scout!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Prints a Message when /hbnb is called """
    return 'Football Scout Home'

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)

