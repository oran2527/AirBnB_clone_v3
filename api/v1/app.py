#!/usr/bin/python3
"""
module:app
blueprint to api. register app_views blueprint
run web application to apis
"""


from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, Blueprint, make_response, jsonify
from flask_cors import CORS


app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


app.register_blueprint(app_views)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def tear_down(error):
    """
    close SQLAlchemy session
    """
    storage.close()


@app.errorhandler(404)
def errorhandler(error):
    """
    catch 404 response and response jsonify
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)
