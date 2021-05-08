#!/usr/bin/python3
""" Route for amenities responses. """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def all_amenities():
    """ Route to GET method. Should be retrieve all amenity objs. """
    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            abort(400)
            abort(Response('Not a JSON'))
        else:
            if req.get('name') is None:
                abort(400)
                abort(Response('Missing name'))
            else:
                n_amenity = Amenity(**(req))
                storage.save()
                return n_amenity.to_dict(), 201

    list_ = [v.to_dict() for v in storage.all('Amenity').values()]
    return jsonify(list_)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
def amenity(amenity_id):
    """ Route to POST, PUT, DELETE and GET by ID methods. """

    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    elif request.method == 'GET':
        return jsonify(amenity.to_dict())

    elif request.method == 'DELETE':
        amenity.delete()
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
                    setattr(amenity, k, v)
            storage.save()
            return amenity.to_dict(), 200
