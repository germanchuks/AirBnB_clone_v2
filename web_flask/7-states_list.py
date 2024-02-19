#!/usr/bin/python3
"""Script to start a Flask web application."""
from models.state import State
from models import storage
from flask import Flask, render_template


app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Remove the current SQLAlchemy Session after each request."""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Displays a HTML page containing all states"""
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
