#!/usr/bin/python3
"""
Creates a view for Amenity objects - handles all default RESTful API actions
"""
from flask import abort, jsonify, make_response, request
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_all_user():
    """
    return all amenities
    """
    users = []
    for user in storage.all('User').values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route("/users/<string:user_id>", methods=['GET'],
                 strict_slashes=False)
def get_a_user(user_id):
    """
    get user with specific id
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    delete a user given its id
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_city():
    """
    add a new user
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**request.get_json())
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<string:user_id>", methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    update  an existing user
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    ignored = ['id', 'email', 'created_at', 'updated_at']
    for key, value in request.get_json().items():
        if key not in ignored:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
