#!/usr/bin/python3
"""
new view for State objects that handles
all default RESTFul API actions
"""


from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_all():
    states = storage.all('State').values()
    
