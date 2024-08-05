#!/usr/bin/python3
"""
index
"""


from flask import jsonify
from api.v1.views import app_views
from models import storage

hbnb = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status')
def status():
    '''
    status
    '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    '''
    status
    '''
    count = {}
    for key in hbnb.keys():
        count[key] = storage.count(hbnb[key])
    return jsonify(count)
