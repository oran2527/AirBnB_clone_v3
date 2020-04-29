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
    else:
        return jsonify(list_cities)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def displayPlacesbyId(place_id):
    """Return the places by id if not error 404
    """
    list_places = []
    places = storage.all('Place')
    for key, value in places.items():
        if value.id == place_id:
            list_places.append(value.to_dict())
            break
    if list_cities == []:
        abort(404)
    else:
        return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['DELETE\
'], strict_slashes=False)
def deletePlace(place_id):
    """Delete a place if not error 404
    """
    list_places = {}
    flag = 0
    places = storage.all('Place')
    for key, value in places.items():
        if value.id == place_id:
            flag = 1
            storage.delete(places[key])
            storage.save()
            break
    if flag == 0:
        abort(404)
    return jsonify(list_places.to_dict()), 200


@app_views.route('/cities/<city_id>/places', methods=['POST\
'], strict_slashes=False)
def createPlace(city_id):
    """Create a place for a city if not error 404
    """
    flag_city_id = 0
    place = request.get_json()
    if not place:
        abort(400, {'Not a JSON'})
    if 'name' not in place:
        abort(400, {'Missing name'})
    cities = storage.all('City')
    text_final = "{}.{}".format('City', text)
    for key, value in states.items():
        if key == text_final:
            flag_city_id = 1
            break
    if flag_city_id == 0:
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
    flag_place = 0
    place = request.get_json()
    if not place:
        abort(400, {'Not a JSON'})
    places = storage.all('Place')
    text_final = "{}.{}".format('Place', text)
    for key, value in places.items():
        if key == text_final:
            flag_place = 1
            break
    if flag_place == 0:
        abort(404)
    pla = storage.get('Place', place_id)
    if not pla:
        abort(404)
    for key, value in place.items():
        setattr(pla, key, value)
    storage.save()
    return jsonify(pla.to_dict()), 200
