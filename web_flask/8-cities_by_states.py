#!/usr/bin/python3
"""Script to start a Flask web application."""
from models import *
from models import storage
from flask import Flask, render_template


app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Remove the current SQLAlchemy Session after each request."""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def cities_by_states():
    """Displays a HTML page containing all states and their cities"""
    states = storage.all("State").values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
