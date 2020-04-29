#!/usr/bin/python3
"""
module:state to manage crud api state
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def displayAllStates():
    """ Display all states """
    states = storage.all("State").values()
    lista = []
    for i in states:
        lista.append(i.to_dict())
    return jsonify(lista)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def displayStatebyid(state_id):
    """ Display stata by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteStatebyid(state_id):
    """ Delete a especific state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def createState():
    """create a new state """
    content = request.get_json(silent=True)
    if not content:
        abort(400, {'Not a JSON'})
    if 'name' not in content:
        abort(400, {'Missing name'})
    newstate = State(**content)
    storage.new(newstate)
    storage.save()
    return jsonify(newstate.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updateState(state_id):
    """update a state """
    flag = 0
    content = request.get_json()
    if not content:
        abort(400, {'Not a JSON'})
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for key, value in content.items():
        setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
