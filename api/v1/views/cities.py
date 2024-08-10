#!/usr/bin/python3
""" handle REST requests """

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.city import City
from models.state import State
from flasgger.utils import swag_from


@app_views.route(
        '/states/<state_id>/cities',
        methods=['GET'],
        strict_slashes=False
        )
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def cities_all(state_id):
    """ returns list of all City objects """
    cities_all = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        cities_all.append(city.to_dict())
    return jsonify(cities_all)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def city_get(city_id):
    """ Get a city by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city = city.to_dict()
    return jsonify(city)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
def city_delete(city_id):
    """ Get a city by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
        '/states/<state_id>/cities',
        methods=['POST'],
        strict_slashes=False
        )
@swag_from('documentation/city/post_city.yml', methods=['POST'])
def city_post(state_id):
    """ Post a city """
    state = storage.get(State, state_id)
    data = request.get_json()
    if state is None:
        abort(404)
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    city = City(**data)
    city.state_id = state_id
    storage.save()
    city = city.to_dict()
    return make_response(jsonify(city), 200)


@app_views.route(
        '/cities/<city_id>',
        methods=['PUT'],
        strict_slashes=False
        )
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def city_update(city_id):
    """ Update a city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    ignored_keys = ["id", "created_at", "updated_at", "state_id"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()
    city = city.to_dict()
    return make_response(jsonify(city), 200)
