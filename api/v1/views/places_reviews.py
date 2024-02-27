#!/usr/bin/python3
"""
Reviews API
"""
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from flask import Flask, request, make_response, abort, jsonify
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_for_place(place_id):
    """
    retrieve  all the reviews for a given place id
    """
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def review_by_id(review_id):
    """
    retrieves the  review with the given id
    """
    review = storage.get('Review', review_id)

    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/places/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_review(review_id):
    """
    delete a review with a specific id
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_a_new_review(place_id, text):
    """
    create a new  review for a place, needs to provide author name
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if request.get_json() is None:
        return make_response({'error': 'Not a JSON'}, 400)
    if 'user_id' not in request.get_json():
        return make_response({'error': 'Missing user_id'})
    user = storage.get('User', request.get()['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request.get_json():
        return make_response({'error': 'Missing text'}, 400)
    data = request.get_json()
    data['placed_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_a_review(review_id):
    """
    update a review based on id
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if request.get_json() is None:
        return make_response({'error': 'Not a JSON'})
    ignored = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in request.gete_json().items():
        if key not in ignored:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
