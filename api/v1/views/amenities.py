#!/usr/bin/python3
"""Functionality for working with Amenities api"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all():
  """
  A function that gets all amenities from amenities class
  """
  all_values = []
  obj = storage.all('Amenity').values()
  for objs in obj():
    all_values.append(objs.to_dict())
  return jsonify(all_values)

@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_by_id(amenity_id):
  """
  A function that queries an amenity by it's id
  """
  data = storage.get('Amenity', amenity_id)
  if data is None:
    abort(404)
  return jsonify(data.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_by_id(amenity_id):
  """
  A function that deletes an amenity bi it's id
  """
  obj = storage.get('Amenity', amenity_id)
  if obj is None:
    abort(404)
  storage.delete(obj)
  storage.save()
  return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
  """
  A function that creates a new amenity
  """
  data = request.get_json()
  if data is None:
    abort(400, 'Not a JSON')
  if 'name' not in data:
    abort(400, 'Missing name')
  amenity = Amenity(**data)
  amenity.save()
  return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_by_id(amenity_id):
  """
  A function that updates the amenity
  """
  amenity = storage.get('Amenity', amenity_id)
  if amenity is None:
    abort(404)
  data = request.get_json()
  if not data:
    abort(400, 'Not a JSON')
  for key, value in data.items():
    if key not in ['id', 'created_at', 'updated_at']:
      setattr(amenity, key, value)
  amenity.save()
  return jsonify(amenity.to_dict()), 200
