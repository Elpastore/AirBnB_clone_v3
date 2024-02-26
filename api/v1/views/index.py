#!/usr/bin/python3
"""index.py route"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """return a JSON status"""
    return jsonify({"status": "OK"})
