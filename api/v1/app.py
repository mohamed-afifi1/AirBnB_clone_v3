#!/usr/bin/python3
"""
api app
"""

import os
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    '''
    teardown
    '''
    storage.close()


if __name__ == "__main__":
    try:
        host = os.environ.get('HBNB_API_HOST')
    except Exception as e:
        host = '0.0.0.0'

    try:
        port = 'HBNB_API_PORT'
    except Exception as e:
        port = '5000'

        app.run(host=host, port=port)
