#!/usr/bin/python3
"""
View for States that handles all RESTful API actions
"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_all():
    """ returns list of all User objects """
    users_all = []
    users = storage.all("User").values()
    for user in users:
        users_all.append(user.to_dict())
    return jsonify(users_all)


@app_views.route('users/<user_id>', methods=['GET'], strict_slashes=False)
def user_get(user_id):
    """ handles GET method """

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user = user.to_dict()
    return jsonify(user)


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def user_delete(user_id):
    """ handles DELETE method """
    empty_dict = {}
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    """ update a state with its id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "email", "created_at", "updated_at"]
    for k, v in data.items():
        if k not in ignored_keys:
            setattr(user, k, v)
    storage.save()
    user = user.to_dict()
    return jsonify(user), 200
