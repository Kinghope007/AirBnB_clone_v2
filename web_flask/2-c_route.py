#!/usr/bin/python3
"""Importing lightweight WSGI web application framework"""
from flask import Flask
from markupsafe import escape


app = Flask(__name__)


# Define a route with the option strict_slashes=False
@app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def display_c_text(text):
    # Replace underscores with spaces
    text = text.replace('_', ' ')
    return 'C {}'.format(escape(text))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)