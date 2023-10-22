#!/usr/bin/python3
"""Importing lightweight WSGI web application framework"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """display a HTML page like 6-index.html"""
    states = storage.all('State').values()
    states = sorted(states, key=lambda state: state.name)
    cities = storage.all('City').values()
    cities = sorted(cities, key=lambda city: city.name)
    amenities = storage.all('Amenity').values()
    amenities = sorted(amenities, key=lambda amenity: amenity.name)
    return render_template('10-hbnb_filters.html', states=states, cities=cities, amenities=amenities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
