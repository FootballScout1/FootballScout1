#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models.scout import Scout

app = Flask(__name__)

@app.route('/scouts', strict_slashes=False)
@app.route('/scouts/<id>', strict_slashes=False)
def scouts(id=None):
    """ Displays a list of all Scout objects or clubs of a specific scout """
    scouts = storage.all(Scout)
    if id:
        scout = scouts.get(f'Scout.{id}')
        if scout:
            return render_template('9-scouts.html', scout=scout, scouts=None)
        else:
            return render_template('9-scouts.html', scout=None, scouts=None)
    else:
        return render_template('9-scouts.html', scouts=scouts.values(), scout=None)

@app.teardown_appcontext
def teardown_db(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

