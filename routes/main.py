import flask
import json

from bson import ObjectId
from datetime import datetime, timedelta
from flask import render_template, redirect, Blueprint, g, request, Response
from mongo import get_connection

main_routes = Blueprint('main', __name__)

DEFAULT_MIMETYPE = "application/json"

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.strftime("%s")
        return json.JSONEncoder.default(self, o)

def jsonify(return_dict, mimetype=DEFAULT_MIMETYPE, code=200):
    return Response(
        JSONEncoder().encode(return_dict),
        mimetype=mimetype or DEFAULT_MIMETYPE
    ), code

@main_routes.route('/')
def main():
    """
        Main route for testing
    Attributes:
        None
    """

    return jsonify({
        "status_code": 200,
        "message": "OK",
    })


@main_routes.route('/route', methods=['GET', 'POST'])
def routes_endpoint():
    routes_collection = get_connection().routes

    if request.method == "POST":
        payload = request.get_json(force=True)

        project = payload.get('project', None)
        endpoint = payload.get('endpoint', None)
        methods = payload.get('methods', "GET,POST,OPTIONS")
        response_mime = payload.get('response_mime', DEFAULT_MIMETYPE)
        response_body = payload.get('response_body', None)

        if any([project is None, endpoint is None]):
            return jsonify({
                "status_code": 400,
                "message": "project and endpoint parameters are required to create a route"
            }, code=400)

        id = routes_collection.insert_one({
            "project": project,
            "endpoint" : endpoint,
            "methods": methods,  
            "response_mime": response_mime,
            "response_body": response_body,
        }).inserted_id

        return jsonify({
            "id": id,
            "status_code": 201
        }, code=201)

    
    return jsonify([
        route for route in routes_collection.find()
    ])


@main_routes.route('/api/<project>/<endpoint>', methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def api_routes_endpoint(project, endpoint):
    method = request.method

    routes_collection = get_connection().routes

    resp = routes_collection.find_one({
        "project": project,
        "endpoint": endpoint,
        "methods": method,
    })

    if resp is None:
        return jsonify({
            "status_code": 404,
            "message": "Endpoint not found"
        }, code=404)

    return jsonify(resp.get('response_body', {}), mimetype=resp.get('response_mimetype', None), code=200)
