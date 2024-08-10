#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def cities_all(state_id):
    """ returns list of all City objects """
    cities_all = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    for city in cities:
        cities_all.append(city.to_dict())
    return jsonify(cities_all)