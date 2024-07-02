#!/usr/bin/python3
from flask import Flask, render_template, abort
from models import storage
from models.scout import Scout
from models.club import Club

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session."""
    storage.close()

@app.route('/scouts', strict_slashes=False)
def list_scouts():
    """Display a HTML page with a list of all Scout objects."""
    scouts = storage.all(Scout).values()
    return render_template('scouts.html', scouts=sorted(scouts, key=lambda s: s.name))

@app.route('/scouts/<id>', strict_slashes=False)
def scout_by_id(id):
    """Display a HTML page with a Scout and their associated clubs."""
    scout = storage.get(Scout, id)
    if scout is None:
        return render_template('not_found.html')
    clubs = scout.clubs if storage_t == 'db' else scout.get_clubs()
    return render_template('scout.html', scout=scout, clubs=sorted(clubs, key=lambda c: c.name))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

