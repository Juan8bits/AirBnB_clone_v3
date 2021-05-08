#!/usr/bin/python3
""" Route for States responses. """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def retrieves_obj():
    """ Route to GET method. Should be retrieve all State objs. """
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
                new_state = State(**(req))
                storage.save()
                return new_state.to_dict(), 201

    list_ = [v.to_dict() for v in storage.all('State').values()]
    return jsonify(list_)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
def states(state_id):
    """ Route to POST, PUT, DELETE and GET by ID methods. """

    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    elif request.method == 'GET':
        return jsonify(state.to_dict())

    elif request.method == 'DELETE':
        state.delete()
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
                    setattr(state, k, v)
            storage.save()
            return state.to_dict(), 200
