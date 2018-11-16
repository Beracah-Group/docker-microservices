# import modules, models and configs
from datetime import datetime, timedelta
import re

import jwt
from flask import jsonify, request, abort
# jsonify converts objects to JSON strings
# abort method either accepts an error code or it can accept a Response object

from src.api.__init__ import app, databases
from src.api.v1.models import Servicepkg
from flask import render_template

databases.create_all()

'''
 201  ok resulting to  creation of something
 200  ok
 400  bad request
 404  not found
 401  unauthorized
 409  conflict
'''

'''
    (UTF) Unicode Transformation Format
    its a character encoding
    A character in UTF8 can be from 1 to 4 bytes long
    UTF-8 is backwards compatible with ASCII
    is the preferred encoding for e-mail and web pages
'''


# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'The request can not be linked to, Please check your endpoint url'})
    response.status_code = 404
    return response


# 405 error handler
@app.errorhandler(405)
def method_not_allowed(e):
    response = jsonify({'error': 'Invalid request method. Please check the request method being used'})
    response.status_code = 405
    return response


# 401 error handler
@app.errorhandler(401)
def internal_server_error(e):
    response = jsonify({"error": "Token is invalid"})
    response.status_code = 401
    return response


# 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    response = jsonify({'error': 'Error, Server currently down, please restart the server to use the Service package API'})
    response.status_code = 500
    return response


@app.route('/')
def homepage():
    """ The homepage route
    :return: A welcome message
    """
    return render_template('index.html')

# add sp type method
@app.route('/servicepkg/api/v1/servicepkg', methods=['POST'])
def add_sp_method():
    request.get_json(force=True)
    try:
    #     verification = verify_token(request)
    #     if isinstance(verification, dict):
    #         user_id = verification['user_id']
    #     else:
    #         return verification

        d_name = request.json.get('name')
        d_price = request.json.get('price')
        d_description = request.json.get('description')
        if not d_name:
            response = jsonify({'Error': 'service package has no name'})
            response.status_code = 400
            return response
        if not d_price:
            response = jsonify({'Error': 'service package has no price tag'})
            response.status_code = 400
            return response
        if not d_description:
            response = jsonify({'Error': 'service package has no description'})
            response.status_code = 400
            return response

        res = Servicepkg.query.all()
        data_check = [data for data in res if data.name == d_name]
        if data_check:
            response = jsonify({'Warning': 'this service package already exists'})
            response.status_code = 409
            return response
        else:
            d = Servicepkg(name=d_name, price=d_price, description=d_description)
            d.save()
            response = jsonify({'status': 'service package added successfully'})
            response.status_code = 201
            return response
    except KeyError:
        response = jsonify({'Error': 'Use the name for dict key.'})
        response.status_code = 500
        return response


# get sp package
@app.route('/servicepkg/api/v1/servicepkg', methods=['GET'])
def retrieve_sp_method():
    message = 'No service packages have been added yet'
    # payload = verify_token(request)
    # if isinstance(payload, dict):
    #     user_id = payload['user_id']
    # else:
    #     return payload

    limit = int(request.args.get("limit", 3))
    if limit > 100:
        limit = 100
    respons = Servicepkg.query.all()
    if not respons:
        response = jsonify({'error': 'No service package has been created yet'})
        response.status_code = 200
        return response
    else:
        search = request.args.get("q", "")
        if search:
            res = [sp for sp in respons if sp.name in search]
            if not res:
                response = jsonify({'error': 'The service package you searched does not exist'})
                return response
            else:
                sp_data = []
                for data in res:
                    final = {
                        'id': data.id,
                        'name': data.name,
                        'price': data.price,
                        'description': data.description,
                        'date-created': data.date_created,
                        'date_modified': data.date_modified,
                    }
                    sp_data.clear()
                    sp_data.append(final)
                response = jsonify(sp_data)
                response.status_code = 200
                return response
        else:
            res = [sp for sp in respons]
            sp_data = []
            if not res:
                response = jsonify({'error': message})
                response.status_code = 200
                return response
            else:
                for data in res:
                    final = {
                        'id': data.id,
                        'name': data.name,
                        'price': data.price,
                        'description': data.description,
                        'date-created': data.date_created,
                        'date_modified': data.date_modified,
                    }
                    sp_data.append(final)
                response = jsonify(sp_data)
                response.status_code = 200
                return response


# get, update and delete sp package
@app.route('/servicepkg/api/v1/servicepkg/<int:sp_id>', methods=['GET', 'PUT', 'DELETE'])
def sp_by_id(sp_id):
    # payload = verify_token(request)
    # if isinstance(payload, dict):
    #     user_id = payload['user_id']
    # else:
    #     return payload
    res = Servicepkg.query.all()
    sp_data = [sp for sp in res if sp.id == sp_id]
    if request.method == 'GET':
        data = {}
        for data in sp_data:
            data = {
                'id': data.id,
                'name': data.name,
                'price': data.price,
                'description': data.description,
                'date-created': data.date_created,
                'date_modified': data.date_modified,
            }
        if sp_id not in data.values():
            response = jsonify({'warning': 'the service package does not exist.'})
            response.status_code = 404
            return response
        else:
            response = jsonify(data)
            response.status_code = 200
            return response
    elif request.method == 'DELETE':
        data = {}
        for data in sp_data:
            data = {
                'id': data.id,
                'name': data.name,
                'price': data.price,
                'description': data.description,
                'date-created': data.date_created,
                'date_modified': data.date_modified,
            }
        if sp_id not in data.values():
            response = jsonify({'warning': 'the service package does not exist.'})
            response.status_code = 404
            return response
        else:
            delete = Servicepkg.query.filter_by(id=sp_id).first()
            databases.session.delete(delete)
            databases.session.commit()
            response = jsonify({'Status': 'Service package deleted successfully.'})
            response.status_code = 200
            return response
    elif request.method == 'PUT':
        request.get_json(force=True)
        data = Servicepkg.query.filter_by(id=sp_id).first()
        if not data:
            response = jsonify({'warning': 'the service package does not exist.'})
            response.status_code = 404
            return response
        else:
            try:
                name = request.json['name']
                data.name = name
                databases.session.commit()
                data = {}
                for data in sp_data:
                    data = {
                        'id': data.id,
                        'name': data.name,
                        'price': data.price,
                        'description': data.description,
                        'date-created': data.date_created,
                        'date_modified': data.date_modified
                    }
                response = jsonify(data)
                response.status_code = 201
                return response
            except KeyError:
                response = jsonify({'error': 'Please use name for dict keys.'})
                response.status_code = 500
                return response