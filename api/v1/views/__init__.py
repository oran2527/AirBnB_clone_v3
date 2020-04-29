#!/usr/bin/python3
"""
module: __init__ view package
create app_view Blueprint with prefix /api/v1
"""

from flask import Flask, Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
