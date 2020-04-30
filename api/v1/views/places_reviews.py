#!/usr/bin/python3
"""
module: places_reviews
create api routes:
/status: return status always ok, method GET
/stats: return quantity of tables or clases. method GET
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET\
'], strict_slashes=False)
def displayReviewsByPlace(place_id):
    """Return the reviews by place if not error 404
    """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    lista = []
    for i in place.reviews:
        lista.append(i.to_dict())
    return jsonify(lista)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def displayReviewbyId(review_id):
    """Return the review by id if not error 404
    """
    reviews = storage.get('Review', review_id)
    if not reviews:
        abort(404)
    return jsonify(reviews.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE\
'], strict_slashes=False)
def deleteReview(review_id):
    """Delete a review if not error 404
    """
    reviews = storage.get('Review', review_id)
    if not review:
        abort(404)
    storage.delete(reviews)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST\
'], strict_slashes=False)
def createReview(place_id):
    """Create a review for a place if not error 404
    """
    userid = ""
    review = request.get_json()
    if not review:
        abort(400, {'Not a JSON'})
    if 'user_id' not in review:
        abort(400, {'Missing user_id'})
    if 'text' not in review:
        abort(400, {'Missing text'})
    for key, value in review.items():
        if key == 'user_id':
            userid = value
    users = storage.get('User', userid)
    if not users:
        abort(404)
    places = storage.get('Place', place_id)
    if not places:
        abort(404)
    review.update(place_id=place_id)
    new_review = Review(**review)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def updateReview(review_id):
    """Update a review if not error 404
    """
    flag_review = 0
    review = request.get_json()
    if not review:
        abort(400, {'Not a JSON'})
    rev = storage.get('Review', review_id)
    if not rev:
        abort(404)
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in review.items():
        if key not in ignore:
            setattr(rev, key, value)
    storage.save()
    return jsonify(rev.to_dict()), 200
