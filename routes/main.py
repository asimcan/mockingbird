
import flask
import json
import os 

from datetime import datetime, timedelta
from flask import render_template, redirect, Blueprint, g, request, Response

from settings import (
    ENDPOINTS_ROOT,
)

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
        project_path = "%s/%s" % (ENDPOINTS_ROOT.rstrip('/'), project.strip('/'))
        if os.path.is_dir(project_path) is False:
            os.makedirs(project_path)
        
        endpoint_path = "%s/%s" % (project_path.rstrip('/'), endpoint)

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

    resp = None
    if resp is None:
        return jsonify({
            "status_code": 404,
            "message": "Endpoint not found"
        }, code=404)

    return jsonify(resp.get('response_body', {}), mimetype=resp.get('response_mimetype', None), code=200)
