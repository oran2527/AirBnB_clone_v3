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
