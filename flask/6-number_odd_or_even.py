#!/usr/bin/python3
""" Starts a Flask Web Application """
from flask import Flask, render_template
app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


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
    return render_template('number_template.html', value=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def odd_or_even(n):
    """ display a HTML page only if n is an integer """
    return render_template('number_odd_or_even.html', value=n)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)

