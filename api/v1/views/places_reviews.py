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


@app_views.route('/places/<place_id>/reviews', methods=['GET\
'], strict_slashes=False)
def displayReviewsByPlace(place_id):
    """Return the reviews by place if not error 404
    """
    list_reviews = []
    reviews = storage.all('Review')
    for key, value in places.items():
        if value.place_id == place_id:
            list_reviews.append(value.to_dict())
    if list_places == []:
        abort(404)
    else:
        return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def displayReviewbyId(review_id):
    """Return the review by id if not error 404
    """
    list_reviews = []
    reviews = storage.all('Review')
    for key, value in reviews.items():
        if value.id == review_id:
            list_reviews.append(value.to_dict())
            break
    if list_reviews == []:
        abort(404)
    else:
        return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['DELETE\
'], strict_slashes=False)
def deleteReview(review_id):
    """Delete a review if not error 404
    """
    list_reviews = {}
    flag = 0
    reviews = storage.all('Review')
    for key, value in reviews.items():
        if value.id == review_id:
            flag = 1
            storage.delete(reviews[key])
            storage.save()
            break
    if flag == 0:
        abort(404)
    return jsonify(list_reviews.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST\
'], strict_slashes=False)
def createReview(place_id):
    """Create a review for a place if not error 404
    """
    flag_place_id = 0
    review = request.get_json()
    if not review:
        abort(400, {'Not a JSON'})
    if 'name' not in review:
        abort(400, {'Missing name'})
    places = storage.all('Place')
    text_final = "{}.{}".format('Place', place_id)
    for key, value in places.items():
        if key == text_final:
            flag_place_id = 1
            break
    if flag_place_id == 0:
        abort(404)
    review.update(place_id=place_id)
    new_review = Reviewe(**review)
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
    reviews = storage.all('Review')
    text_final = "{}.{}".format('Review', review_id)
    for key, value in reviews.items():
        if key == text_final:
            flag_place = 1
            break
    if flag_place == 0:
        abort(404)
    rev = storage.get('Review', review_id)
    if not rev:
        abort(404)
    for key, value in review.items():
        setattr(rev, key, value)
    storage.save()
    return jsonify(rev.to_dict()), 200
