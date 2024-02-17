#!/usr/bin/python3
"""Script to start a Flask web application."""
from flask import Flask, abort, render_template


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_route():
    """Displays `Hello HBNB!`"""
    return 'Hello HBNB!'


@app.route("/hbnb", strict_slashes=False)
def hbnb_route():
    """Displays `HBNB`"""
    return 'HBNB'


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """Displays `C <text>`"""
    return f"C {text.replace('_', ' ')}"


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text="is cool"):
    """Displays `Python <text>`"""
    return f"Python {text.replace('_', ' ')}"


@app.route("/number/<n>", strict_slashes=False)
def number_route(n):
    """Displays `<n> is a number` only if n is an integer"""
    try:
        n = int(n)
        return f"{n} is a number"
    except ValueError:
        abort(404)


@app.route("/number_template/<n>", strict_slashes=False)
def number_template(n):
    """Display a HTML page only if n is an integer"""
    try:
        n = int(n)
        return render_template('5-number.html', number=n)
    except ValueError:
        abort(404)


@app.route("/number_odd_or_even/<n>", strict_slashes=False)
def number_odd_or_even(n):
    """Displays a HTML page only if n is an integer"""
    try:
        n = int(n)
        return render_template('6-number_odd_or_even.html', number=n)
    except ValueError:
        abort(404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
