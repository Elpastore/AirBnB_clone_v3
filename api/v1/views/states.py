#!/usr/bin/python3
"""State api"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.base_model import BaseModel


@app_views.route('/states', methods=['Get'], strict_slashes=False)
def all_states():
    """ A function that retrieves all_values states object"""
    all_values = []
    obj = storage.all('State').values()
    for objs in obj:
        all_values.append(objs.to_dict())
    return jsonify(all_values)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def state_by_id(state_id):
    """ A function that retrives a state by id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ A function that delete a state by id"""
    try:
        empty_obj = {}
        storage.delete(storage.get('State', state_id))
        storage.save()
        return jsonify(empty_obj)
    except Exception:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ A function that creates a new resource"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """A function that updates a state object"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        return abort(400, 'Not a Json')

    update = {key: value for key, value in data.items() if data not in [
        'id', 'created_at', 'updated_at']}
    if update:
        for key, value in update.items():
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
