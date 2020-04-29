#!/usr/bin/python3
"""
module: amenities
create api routes:
/status: return status always ok, method GET
/stats: return quantity of tables or clases. method GET
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def displayAmenities():
    """Return all the amenities
    """
    list_amenities = []
    amenities = storage.all('Amenity')
    for key, value in amenities.items():
        list_amenities.append(value.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET\
'], strict_slashes=False)
def displayAmenityById(amenity_id):
    """Return amenity by id
    """
    list_amenities = []
    flag = 0
    amenities = storage.all('Amenity')
    for key, value in amenities.items():
        am_final = "Amenity.{}".format(amenity_id)
        if key == am_final:
            flag = 1
            list_amenities.append(value.to_dict())
            break
    if flag == 0:
        abort(404)
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE\
'], strict_slashes=False)
def deleteAmenity(amenity_id):
    """Delete an amenity if not error 404
    """
    list_amenities = {}
    flag = 0
    amenities = storage.all('Amenity')
    for key, value in amenities.items():
        if value.id == amenity_id:
            flag = 1
            storage.delete(amenities[key])
            storage.save()
            break
    if flag == 0:
        abort(404)
    return jsonify(list_amenities), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createAmenity():
    """Create an amenity if not error 404
    """
    flag = 0
    amenity = request.get_json()
    if not amenity:
        abort(400, {'Not a JSON'})
    if 'name' not in amenity:
        abort(400, {'Missing name'})
    new_amenity = Amenity(**amenity)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT\
'], strict_slashes=False)
def updateAmenity(amenity_id):
    """Update an amenity if not error 404
    """
    flag = 0
    amenity = request.get_json()
    text_final = "{}.{}".format('Amenity', amenity_id)
    if not amenity:
        abort(400, {'Not a JSON'})
    amen = storage.get('Amenity', amenity_id)
    if not amen:
        abort(404)
    for key, value in amenity.items():
        setattr(amen, key, value)
    storage.save()
    return jsonify(amen.to_dict()), 200
