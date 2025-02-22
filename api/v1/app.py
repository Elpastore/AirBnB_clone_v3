#!/usr/bin/python3
"""
Createw Flask app; and register the blueprint app_views to Flask instance app.
"""

# Import necessary module
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


# teardown method to call close
@app.teardown_appcontext
def call_close(code):
    """
    Removes the current SQLAlchemy Session object after each request.
    """
    storage.close()


# route for handling error
@app.errorhandler(404)
def error_handler(error):
    """
    An error handler function
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


# program execution point
if __name__ == "__main__":
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
