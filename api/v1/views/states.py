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
    #print(f"=====test:::  {storage.all('State').values()}")
    states = storage.all("State").values()
    for state in states:
        #print("=====test section========")
        #print("- state itself: ", state)
        #print("- type of one state", type(state))
        #print("- state to dict", state.to_dict())
        #print("- type state to dict", type(state.to_dict()))
        print("- idddddddd state to dict", state.to_dict().get('id'))
        states_all.append(state.to_dict())
        print("=====test section========")
    return jsonify(states_all)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_get(state_id):
    """ handles GET method """

    state = storage.get(State, state_id)
    print("storage.get('State', state_id):::::", state)
    if state is None:
        abort(404)
    state = state.to_dict()
    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'],
        strict_slashes=False)
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
    state = state.to_json()
    return jsonify(state), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    """ handles PUT method """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            state.bm_update(key, value)
    state.save()
    state = state.to_json()
    return jsonify(state), 200
