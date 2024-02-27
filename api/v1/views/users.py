#!/usr/bin/python3
"""Creates a view for Amenity objects - handles all default RESTful API actions
"""
from flask import abort, jsonify, make_response, request
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_user():
    """return all amenities
    """
    users = storage.all('User').values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_user(user_id):
    """get user with specific id
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete a user given its id
    """
    user = storage.get(User, user_id)

    if user:
        user.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_city():
    """add a new user
    """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    new_user = User(**request.get_json())

    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """update  an existing user
    """
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            # Return 400 error if the request data is not in JSON format
            abort(400, 'Not a JSON')
        ignored = ['id', 'email', 'created_at', 'updated_at']

        for key, value in request.get_json().items():
            if key not in ignored:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict())
    else:
        abort(404)
