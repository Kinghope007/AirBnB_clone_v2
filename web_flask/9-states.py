#!/usr/bin/python3
"""Flask web application to display States and Cities"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy Session"""
    storage.close()


@app.route('/states', strict_slashes=False)
def states_list():
    """Display a list of states and cities"""
    states = list(storage.all(State).values())
    states = sorted(states, key=lambda state: state.name)
    return render_template('9-states.html', states=states, id=None)


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Display cities of a specific state"""
    states = storage.all(State)
    state = None
    for state_obj in states.values():
        if state_obj.id == id:
            state = state_obj
            break

    if state:
        cities = sorted(state.cities, key=lambda city: city.name)
        return render_template(
                '9-states.html', state=state, cities=cities, id=1)
    else:
        return render_template('9-states.html', not_found=True, id=1)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
