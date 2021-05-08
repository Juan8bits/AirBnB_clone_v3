#!/usr/bin/python3
""" Script that returns a JSON: "status": "OK". """
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status')
def return_status():
    """ Return status of the page. """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def return_stats():
    """ Retrieves the number of each objects by type. """
    characters = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    res = {}
    for key, value in characters.items():
        res.update({key: storage.count(value)})
    return jsonify(res)
