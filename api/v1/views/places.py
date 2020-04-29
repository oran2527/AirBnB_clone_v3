#!/usr/bin/python3
"""
module:places
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


@app_views.route('/cities/<city_id>/places', methods=['GET\
'], strict_slashes=False)
def displayPlacesByCity(city_id):
    """Return the places by city if not error 404
    """
    list_places = []
    places = storage.all('Place')
    for key, value in places.items():
        if value.city_id == city_id:
            list_places.append(value.to_dict())
    if list_places == []:
        abort(404)
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def displayPlacesbyId(place_id):
    """Return the places by id if not error 404
    """
    list_places = []
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE\
'], strict_slashes=False)
def deletePlace(place_id):
    """Delete a place if not error 404
    """
    list_places = {}
    place = storage.get('Place', place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify(list_places), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST\
'], strict_slashes=False)
def createPlace(city_id):
    """Create a place for a city if not error 404
    """
    place = request.get_json()
    if not place:
        abort(400, {'Not a JSON'})
    if 'name' not in place:
        abort(400, {'Missing name'})
    cities = storage.get('City', city_id)
    if not cities:
        abort(404)
    place.update(city_id=city_id)
    new_place = Place(**place)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updatePlace(place_id):
    """Update a place if not error 404
    """
    place = request.get_json()
    if not place:
        abort(400, {'Not a JSON'})
    places = storage.get('Place', place_id)
    if not places:
        abort(404)
    pla = storage.get('Place', place_id)
    if not pla:
        abort(404)
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in place.items():
        if key not in ignore:
            setattr(pla, key, value)
    storage.save()
    return jsonify(pla.to_dict()), 200
