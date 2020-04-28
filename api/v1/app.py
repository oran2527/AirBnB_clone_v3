#!/usr/bin/python3
"""
module:app
blueprint to api. register app_views blueprint
run web application to apis
"""


from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, Blueprint


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(error):
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)
