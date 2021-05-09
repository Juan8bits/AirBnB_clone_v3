#!/usr/bin/python3
""" Route for Review responses. """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def all_reviews(place_id):
    """ Route to GET and POST method. Should be retrieve all place objs. """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([v.to_dict() for v in place.reviews])
    else:
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        else:
            if req.get('user_id') is None:
                abort(400, 'Missing user_id')
            user = storage.get('User', req.get('user_id'))
            if user is None:
                abort(404)
            if req.get('text') is None:
                abort(400, 'Missing text')
            else:
                new_review = Review(**(req))
                storage.save()
                return new_review.to_dict(), 201


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def specific_review(review_id):
    """ Route to GET, PUT or DELETE a review by ID """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    elif request.method == 'DELETE':
        review.delete()
        storage.save()
        return {}, 200

    elif request.method == 'PUT':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        else:
            for k, v in req.items():
                if k not in ['id', 'created_at', 'updated_at',
                             'user_id', 'place_id']:
                    setattr(review, k, v)
            storage.save()
            return review.to_dict(), 200
