#!/usr/bin/python3
""" Route for States responses. """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def all_cities(state_id):
    """ Route to GET method. Should be retrieve all State objs. """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([v.to_dict() for v in state.cities])
    else:
        req = request.get_json()
        if req is None:
            abort(400)
            abort(Response('Not a JSON'))
        else:
            if req.get('name') is None:
                abort(400)
                abort(Response('Missing name'))
            else:
                new_city = City(**(req))
                storage.save()
                return new_city.to_dict(), 201


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def specific_city(city_id):
    """ Route to GET, PUT or DELETE a city by ID """
    city = storage.get('City', city_id)

    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    elif request.method == 'DELETE':
        city.delete()
        storage.save()
        return {}, 200

    elif request.method == 'PUT':
        req = request.get_json()
        if req is None:
            abort(400)
            abort(Response('Not a JSON'))
        else:
            for k, v in req.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    setattr(city, k, v)
            storage.save()
            return city.to_dict(), 200
