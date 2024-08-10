#!/usr/bin/python3
"""
View for States that handles all RESTful API actions
"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_all():
    """ returns list of all State objects """
    states_all = []
    states = storage.all("State").values()
    for state in states:
        states_all.append(state.to_dict())
    return jsonify(states_all)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_get(state_id):
    """ handles GET method """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state = state.to_dict()
    return jsonify(state)


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def state_delete(state_id):
    """ handles DELETE method """
    empty_dict = {}
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """ handles POST method """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    state = state.to_dict()
    return make_response(jsonify(state), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id):
    """ update a state with its id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "created_at", "updated_at"]
    for k, v in data.items():
        if k not in ignored_keys:
            setattr(state, k, v)
    storage.save()
    state = state.to_dict()
    return make_response(jsonify(state), 200)
