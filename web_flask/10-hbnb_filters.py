#!/usr/bin/python3
"""Script to start a Flask web application."""
from models.state import State
from models import storage
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Displays a HTML page like 6-index.html."""
    states = storage.all(State).values()
    amenities = storage.all(State).values()
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Remove the current SQLAlchemy Session after each request."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
