#!/usr/bin/python3
"""
module:index
create api routes:
/status: return status always ok, method GET
/stats: return quantity of tables or clases. method GET
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<text>/cities', methods=['GET\
'], strict_slashes=False)
def displayCitiesByState(text):
    """Return the cities by state if not error 404
    """
    list_cities = []
    cities = storage.all('City')
    for key, value in cities.items():
        if value.state_id == text:
            list_cities.append(value.to_dict())
    if list_cities == []:
        abort(404)
    else:
        return jsonify(list_cities)


@app_views.route('/cities/<text>', methods=['GET'], strict_slashes=False)
def displayCities(text):
    """Return the cities if not error 404
    """
    list_cities = []
    cities = storage.all('City')
    for key, value in cities.items():
        if value.id == text:
            list_cities.append(value.to_dict())
            break
    if list_cities == []:
        abort(404)
    else:
        return jsonify(list_cities)


@app_views.route('/cities/<text>', methods=['DELETE'], strict_slashes=False)
def deleteCity(text):
    """Delete a city if not error 404
    """
    list_cities = {}
    flag = 0
    cities = storage.all('City')
    for key, value in cities.items():
        if value.id == text:
            flag = 1
            storage.delete(cities[key])
            storage.save()
            break
    if flag == 0:
        abort(404)
    return jsonify(list_cities.to_dict()), 200


@app_views.route('/states/<text>/cities', methods=['POST\
'], strict_slashes=False)
def createCity(text):
    """Create a city if not error 404
    """
    flag_state_id = 0
    city = request.get_json()
    if not city:
        abort(400, {'Not a JSON'})
    if 'name' not in city:
        abort(400, {'Missing name'})
    states = storage.all('State')
    text_final = "{}.{}".format('State', text)
    for key, value in states.items():
        if key == text_final:
            flag_state_id = 1
            break
    if flag_state_id == 0:
        abort(404)
    city.update(state_id=text)
    new_city = City(**city)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<text>', methods=['PUT'], strict_slashes=False)
def updateCity(text):
    """Update a city if not error 404
    """
    flag_city = 0
    city = request.get_json()
    if not city:
        abort(400, {'Not a JSON'})
    cities = storage.all('City')
    text_final = "{}.{}".format('City', text)
    for key, value in cities.items():
        if key == text_final:
            flag_city = 1
            break
    if flag_city == 0:
        abort(404)
    cit = storage.get('City', text)
    if not cit:
        abort(404)
    for key, value in city.items():
        setattr(cit, key, value)
    storage.save()
    return jsonify(cit.to_dict()), 200
