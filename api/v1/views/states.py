#!/usr/bin/python3
""" Route for States responses. """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
# from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieves_obj():
    """ Route to GET method. Should be retrieve all State objs. """
    list_ = [v.to_dict() for v in storage.all('State').values()]
    return jsonify(list_)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
def states(state_id):
    """ Route to POST, PUT, DELETE and GET by ID methods. """
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
                storage.new('State', req)
                storage.save()
                return req, 201

    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        req = request.get_json()
        if req is None:
            abort(400)
            abort(Response('Not a JSON'))
        else:
            for k, v in req.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    state.update({k: v})
            storage.save()
            return state, 200
