# import modules, models and configs
from datetime import datetime, timedelta
import re

import jwt
from flask import jsonify, request, abort
# jsonify converts objects to JSON strings
# abort method either accepts an error code or it can accept a Response object

from src.api.__init__ import app, databases
from src.api.v1.models import Pickanddrop
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
    response = jsonify({'error': 'Error, Server currently down, please restart the server to use the SPick and drop API'})
    response.status_code = 500
    return response


@app.route('/')
def homepage():
    """ The homepage route
    :return: A welcome message
    """
    return render_template('index.html')

# add pd type method
@app.route('/pickanddrop/api/v1/pickanddrop', methods=['POST'])
def add_pd_method():
    request.get_json(force=True)
    try:
    #     verification = verify_token(request)
    #     if isinstance(verification, dict):
    #         user_id = verification['user_id']
    #     else:
    #         return verification

        pd_name = request.json.get('name')
        pd_price = request.json.get('price')
        pd_description = request.json.get('description')
        if not pd_name:
            response = jsonify({'Error': 'Pick and drop mode has no name'})
            response.status_code = 400
            return response
        if not pd_price:
            response = jsonify({'Error': 'Pick and drop mode has no price tag'})
            response.status_code = 400
            return response
        if not pd_description:
            response = jsonify({'Error': 'Pick and drop mode has no description'})
            response.status_code = 400
            return response

        res = Pickanddrop.query.all()
        data_check = [data for data in res if data.name == pd_name]
        if data_check:
            response = jsonify({'Warning': 'this Pick and drop mode already exists'})
            response.status_code = 409
            return response
        else:
            pd = Pickanddrop(name=pd_name, price=pd_price, description=pd_description)
            pd.save()
            response = jsonify({'status': 'Pick and drop mode added successfully'})
            response.status_code = 201
            return response
    except KeyError:
        response = jsonify({'Error': 'Use the name for dict key.'})
        response.status_code = 500
        return response


# get pd package
@app.route('/pickanddrop/api/v1/pickanddrop', methods=['GET'])
def retrieve_pd_method():
    message = 'No Pick and drop mode has been created yet'
    # payload = verify_token(request)
    # if isinstance(payload, dict):
    #     user_id = payload['user_id']
    # else:
    #     return payload

    limit = int(request.args.get("limit", 3))
    if limit > 100:
        limit = 100
    respons = Pickanddrop.query.all()
    if not respons:
        response = jsonify({'error': 'No Pick and drop mode has been created yet'})
        response.status_code = 200
        return response
    else:
        search = request.args.get("q", "")
        if search:
            res = [pd for pd in respons if pd.name in search]
            if not res:
                response = jsonify({'error': 'The Pick and drop mode you searched does not exist'})
                return response
            else:
                pd_data = []
                for data in res:
                    final = {
                        'id': data.id,
                        'name': data.name,
                        'price': data.price,
                        'description': data.description,
                        'date-created': data.date_created,
                        'date_modified': data.date_modified,
                    }
                    pd_data.clear()
                    pd_data.append(final)
                response = jsonify(pd_data)
                response.status_code = 200
                return response
        else:
            res = [pd for pd in respons]
            pd_data = []
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
                    pd_data.append(final)
                response = jsonify(pd_data)
                response.status_code = 200
                return response


# get, update and delete pd modes
@app.route('/pickanddrop/api/v1/pickanddrop/<int:pd_id>', methods=['GET', 'PUT', 'DELETE'])
def pd_by_id(pd_id):
    # payload = verify_token(request)
    # if isinstance(payload, dict):
    #     user_id = payload['user_id']
    # else:
    #     return payload
    res = Pickanddrop.query.all()
    pd_data = [pd for pd in res if pd.id == pd_id]
    if request.method == 'GET':
        data = {}
        for data in pd_data:
            data = {
                'id': data.id,
                'name': data.name,
                'price': data.price,
                'description': data.description,
                'date-created': data.date_created,
                'date_modified': data.date_modified,
            }
        if pd_id not in data.values():
            response = jsonify({'warning': 'The Pick and drop mode you searched does not exist'})
            response.status_code = 404
            return response
        else:
            response = jsonify(data)
            response.status_code = 200
            return response
    elif request.method == 'DELETE':
        data = {}
        for data in pd_data:
            data = {
                'id': data.id,
                'name': data.name,
                'price': data.price,
                'description': data.description,
                'date-created': data.date_created,
                'date_modified': data.date_modified,
            }
        if pd_id not in data.values():
            response = jsonify({'warning': 'The Pick and drop mode you searched does not exist'})
            response.status_code = 404
            return response
        else:
            delete = Pickanddrop.query.filter_by(id=pd_id).first()
            databases.session.delete(delete)
            databases.session.commit()
            response = jsonify({'Status': 'Pick and drop mode added successfully'})
            response.status_code = 200
            return response
    elif request.method == 'PUT':
        request.get_json(force=True)
        data = Pickanddrop.query.filter_by(id=pd_id).first()
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
                for data in pd_data:
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