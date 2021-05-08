#!/usr/bin/python3
""" Route for States responses. """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def all_places(city_id):
    """ Route to GET and POST method. Should be retrieve all place objs. """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([v.to_dict() for v in city.places])
    else:
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        user = storage.get('City', req.get(user_id))
        if user is None:
            abort(404)
        else:
            if req.get('name') is None:
                abort(400, 'Missing name')
            if req.get('user_id') is None:
                abort(400, 'Missing user_id')
            else:
                new_place = Place(**(req))
                new_place.save()
                return new_place.to_dict(), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def specific_place(place_id):
    """ Route to GET, PUT or DELETE a place by ID """
    place = storage.get('Place', place_id)

    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    elif request.method == 'DELETE':
        place.delete()
        place.save()
        return {}, 200

    elif request.method == 'PUT':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        else:
            for k, v in req.items():
                if k not in ['id', 'created_at', 'updated_at',
                             'user_id', 'city_id']:
                    setattr(place, k, v)
            place.save()
            return place.to_dict(), 200
