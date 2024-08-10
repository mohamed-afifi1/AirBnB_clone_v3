#!/usr/bin/python3
"""
View for Amenities that handles all RESTful API actions
"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_all():
    """ returns list of all Amenity objects """
    amenity_all = []
    amenities = storage.all("Amenity").values()
    for amenity in amenities:
        amenity_all.append(amenity.to_dict())
    return jsonify(amenity_all)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity_get(amenity_id):
    """ handles GET method """

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity = amenity.to_dict()
    return jsonify(amenity)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def amenity_delete(amenity_id):
    """ handles DELETE method """
    empty_dict = {}
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify(empty_dict), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_post():
    """ handles POST method """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    amenity.save()
    amenity = amenity.to_dict()
    return make_response(jsonify(amenity), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def amenity_put(amenity_id):
    """ update an Amenity with its id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "created_at", "updated_at"]
    for k, v in data.items():
        if k not in ignored_keys:
            setattr(amenity, k, v)
    storage.save()
    amenity = amenity.to_dict()
    return make_response(jsonify(amenity), 200)
