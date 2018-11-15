# import modules, models and configs
from datetime import datetime, timedelta
import re

import jwt
from flask import jsonify, request, abort
# jsonify converts objects to JSON strings
# abort method either accepts an error code or it can accept a Response object

from src.api.__init__ import app, databases
from src.api.v1.models import Denting
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
    response = jsonify({'error': 'Error, Server currently down, please restart the server to use the Denting API'})
    response.status_code = 500
    return response


@app.route('/')
def homepage():
    """ The homepage route
    :return: A welcome message
    """
    return render_template('index.html')

# add denting type method
@app.route('/denting/api/v1/dentingpackage', methods=['POST'])
def add_denting_method():
    request.get_json(force=True)
    try:
    #     verification = verify_token(request)
    #     if isinstance(verification, dict):
    #         user_id = verification['user_id']
    #     else:
    #         return verification

        d_package = request.json.get('package')
        d_price = request.json.get('price')
        d_description = request.json.get('description')
        if not d_package:
            response = jsonify({'Error': 'denting package has no name'})
            response.status_code = 400
            return response
        if not d_price:
            response = jsonify({'Error': 'denting package has no price tag'})
            response.status_code = 400
            return response
        if not d_description:
            response = jsonify({'Error': 'denting package has no description'})
            response.status_code = 400
            return response

        res = Denting.query.all()
        data_check = [data for data in res if data.package == d_package]
        if data_check:
            response = jsonify({'Warning': 'this denting package already exists.'})
            response.status_code = 409
            return response
        else:
            d = Denting(package=d_package, price=d_price, description=d_description)
            d.save()
            response = jsonify({'status': 'denting package added successfully'})
            response.status_code = 201
            return response
    except KeyError:
        response = jsonify({'Error': 'Use the name for dict key.'})
        response.status_code = 500
        return response


# get denting package
@app.route('/denting/api/v1/dentingpackage', methods=['GET'])
def retrieve_denting_method():
    message = 'No denting packages have been added yet'
    # payload = verify_token(request)
    # if isinstance(payload, dict):
    #     user_id = payload['user_id']
    # else:
    #     return payload

    limit = int(request.args.get("limit", 3))
    if limit > 100:
        limit = 100
    respons = Denting.query.all()
    if not respons:
        response = jsonify({'error': 'No denting package has been created yet'})
        response.status_code = 200
        return response
    else:
        search = request.args.get("q", "")
        if search:
            res = [dent for dent in respons if dent.package in search]
            if not res:
                response = jsonify({'error': 'The denting package you searched does not exist'})
                return response
            else:
                denting_data = []
                for data in res:
                    final = {
                        'id': data.id,
                        'package': data.package,
                        'price': data.price,
                        'description': data.description,
                        'date-created': data.date_created,
                        'date_modified': data.date_modified,
                    }
                    denting_data.clear()
                    denting_data.append(final)
                response = jsonify(denting_data)
                response.status_code = 200
                return response
        else:
            res = [dent for dent in respons]
            denting_data = []
            if not res:
                response = jsonify({'error': message})
                response.status_code = 200
                return response
            else:
                for data in res:
                    final = {
                        'id': data.id,
                        'package': data.package,
                        'price': data.price,
                        'description': data.description,
                        'date-created': data.date_created,
                        'date_modified': data.date_modified,
                    }
                    denting_data.append(final)
                response = jsonify(denting_data)
                response.status_code = 200
                return response


# get, update and delete denting package
@app.route('/denting/api/v1/dentingpackage/<int:dent_id>', methods=['GET', 'PUT', 'DELETE'])
def denting_by_id(dent_id):
    # payload = verify_token(request)
    # if isinstance(payload, dict):
    #     user_id = payload['user_id']
    # else:
    #     return payload
    res = Denting.query.all()
    denting_data = [dent for dent in res if dent.id == dent_id]
    if request.method == 'GET':
        data = {}
        for data in denting_data:
            data = {
                'id': data.id,
                'package': data.package,
                'price': data.price,
                'description': data.description,
                'date-created': data.date_created,
                'date_modified': data.date_modified,
            }
        if dent_id not in data.values():
            response = jsonify({'warning': 'the denting package does not exist.'})
            response.status_code = 404
            return response
        else:
            response = jsonify(data)
            response.status_code = 200
            return response
    elif request.method == 'DELETE':
        data = {}
        for data in denting_data:
            data = {
                'id': data.id,
                'package': data.package,
                'price': data.price,
                'description': data.description,
                'date-created': data.date_created,
                'date_modified': data.date_modified,
            }
        if dent_id not in data.values():
            response = jsonify({'warning': 'the denting package does not exist.'})
            response.status_code = 404
            return response
        else:
            delete = Denting.query.filter_by(id=dent_id).first()
            databases.session.delete(delete)
            databases.session.commit()
            response = jsonify({'Status': 'Denting package deleted successfully.'})
            response.status_code = 200
            return response
    elif request.method == 'PUT':
        request.get_json(force=True)
        data = Denting.query.filter_by(id=dent_id).first()
        if not data:
            response = jsonify({'warning': 'the denting package does not exist.'})
            response.status_code = 404
            return response
        else:
            try:
                package = request.json['package']
                data.package = package
                databases.session.commit()
                data = {}
                for data in denting_data:
                    data = {
                        'id': data.id,
                        'package': data.package,
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