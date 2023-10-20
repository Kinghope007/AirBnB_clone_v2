#!/usr/bin/python3
"""Importing lightweight WSGI web application framework"""
from flask import Flask


app = Flask(__name__)


# Define a route with the option strict_slashes=False
@app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
