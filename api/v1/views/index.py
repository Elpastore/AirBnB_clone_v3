#!/usr/bin/python3
"""
Create a route `/status` on the object app_views.
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


hbnb_features = {
    'states': 'State',
    'cities': 'City',
    'users': 'User',
    'places': 'Place',
    'reviews': 'Review',
    'amenities': 'Amenity'
}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    return a JSON status
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    endpoint that retrieves the number of each objects by type
    """
    stats_dict = {}
    for key, values in hbnb_features.items():
        stats_dict[key] = storage.count(values)
    return jsonify(stats_dict)
