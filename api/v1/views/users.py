#!/usr/bin/python3
""" Route for States responses. """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def retrieve_users():
    """ Route for GET and POST methods. """
    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        else:
            if req.get('email') is None:
                abort(400, 'Missing email')
            elif req.get('password') is None:
                abort(400, 'Missing password')
            else:
                new_user = User(**(req))
                new_user.save()
                return new_user.to_dict(), 201

    list_ = [v.to_dict() for v in storage.all('User').values()]
    return jsonify(list_)


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def users(user_id):
    """ Route to POST, PUT, DELETE and GET by ID methods. """

    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    elif request.method == 'GET':
        return jsonify(user.to_dict())

    elif request.method == 'DELETE':
        user.delete()
        user.save()
        return {}, 200

    elif request.method == 'PUT':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        else:
            for k, v in req.items():
                if k not in ['id', 'email', 'created_at', 'updated_at']:
                    setattr(user, k, v)
            user.save()
            return user.to_dict(), 200
