#!/usr/bin/python3
"""
States handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_all():
    """ return all State objects """
    all_states = []
    states = storage.all("State").values()
    for state in states:
        all_states.append(state.to_json())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_get(state_id):
    """ GET method for Id"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    s = s.to_json()
    return jsonify(s)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    """ handling the DELETE method """
    em_dict = {}
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify(em_dict), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """ handlling the POST method """
    objs = request.get_json()
    if objs is None:
        abort(400, "Not a JSON")
    if 'name' not in objs:
        abort(400, "Missing name")
    state = State(**objs)
    state.save()
    state = state.to_json()
    return jsonify(state), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    """ handling the PUT method """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    objs = request.get_json()
    if objs is None:
        abort(400, "Not a JSON")
    for k, v in objs.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if k not in ignore_keys:
            state.bm_update(k, v)
    state.save()
    state = state.to_json()
    return jsonify(state), 200
