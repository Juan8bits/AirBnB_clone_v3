#!/usr/bin/python3
""" Script that returns a JSON: "status": "OK". """
from api.v1.views import app_views


@app_views.route('/status')
def return_status():
    """ Return status of the page. """
    return {"status": "OK"}
