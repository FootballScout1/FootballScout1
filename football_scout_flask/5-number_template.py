#!/usr/bin/python3
""" Starts a Flask Web Application """
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_football_scout():
    """ Prints a Message when / is called """
    return 'Hello Football Scout!'


@app.route('/football_scout', strict_slashes=False)
def football_scout():
    """ Prints a Message when /football_scout is called """
    return 'Football Scout'


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """ Prints a Message when /c is called """
    return "C " + text.replace('_', ' ')


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text='is_cool'):
    """ Prints a Message when /python is called """
    return "Python " + text.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def is_n_number(n):
    """ Prints a Message when /number is called only if n is an int"""
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """ display a HTML page only if n is an integer """
    # print(f"Debug: n = {n}")  # Debug print
    return render_template('number_template.html', value=n)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)

