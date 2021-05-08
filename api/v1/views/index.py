#!/usr/bin/python3
""" Script that returns a JSON: "status": "OK". """
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def return_status():
    """ Return status of the page. """
    return {"status": "OK"}


@app_views.route('/api/v1/stats')
def return_stats():
    """ Retrieves the number of each objects by type """
    return storage.count()
