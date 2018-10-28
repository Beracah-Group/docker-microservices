# add servicing package
@app.route('/service/api/package', methods=['POST'])
def add_package():
    request.get_json(force=True)
        p_name = request.json['name']
        if not p_name:
            response = jsonify({'Error': 'Package has no name'})
            response.status_code = 400
            return response

        res = Servicepackages.query.all()
        data_check = [data for data in res if data.name == p_name]
        if data_check:
            response = jsonify({'Warning': 'this service package already exists.'})
            response.status_code = 409
            return response
        else:
            p = Servicepackages(name=p_name)
            p.save()
            response = jsonify({'status': 'Package added successfully'})
            response.status_code = 201
            return response
    except KeyError:
        response = jsonify({'Error': 'Use the name for dict key.'})
        response.status_code = 500
        return response

# get servicing package
@app.route('/service/api/package', methods=['GET'])
def retrieve_package():
    message = 'No Packages have been created'

    limit = int(request.args.get("limit", 20))
    if limit > 100:
        limit = 100
    respons = Servicepackages.query.all()
    if not respons:
        response = jsonify({'error': 'No package has been created yet'})
        response.status_code = 200
        return response
    else:
        search = request.args.get("q", "")
        if search:
            res = [package for package in respons if package.name in search]
            if not res:
                response = jsonify({'error': 'The Package you searched does not exist'})
                return response
            else:
                package_data = []
                for data in res:
                    final = {
                        'id': data.id,
                        'name': data.name,
                        'price': data.price,
                        'description': data.description,
                    }
                    package_data.clear()
                    package_data.append(final)
                response = jsonify(package_data)
                response.status_code = 200
                return response
        else:
            res = [package for package in respons]
            package_data = []
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
                    }
                    package_data.append(final)
                response = jsonify(package_data)
                response.status_code = 200
                return response


# get update delete servicing package
@app.route('/service/api/package/<int:package_id>', methods=['GET', 'PUT', 'DELETE'])
def package_by_id(package_id):
    res = Servicepackages.query.all()
    package_data = [package for package in res if package.id == package_id]
    if request.method == 'GET':
        data = {}
        for data in package_data:
            data = {
                'id': data.id,
                'name': data.name,
                'price': data.price,
                'description': data.description
            }
        if package_id not in data.values():
            response = jsonify({'warning': 'the package does not exist.'})
            response.status_code = 404
            return response
        else:
            response = jsonify(data)
            response.status_code = 200
            return response
    elif request.method == 'DELETE':
        data = {}
        for data in package_data:
            data = {
                'id': data.id,
                'name': data.name,
                'price': data.price,
                'description': data.description
            }
        if package_id not in data.values():
            response = jsonify({'warning': 'the package does not exist.'})
            response.status_code = 404
            return response
        else:
            delete = Servicepackages.query.filter_by(id=package_id).first()
            db.session.delete(delete)
            db.session.commit()
            response = jsonify({'Status': 'Package deleted successfully.'})
            response.status_code = 200
            return response
    elif request.method == 'PUT':
        request.get_json(force=True)
        data = Servicepackages.query.filter_by(id=package_id).first()
        if not data:
            response = jsonify({'warning': 'the package does not exist.'})
            response.status_code = 404
            return response
        else:
            try:
                name = request.json['name', 'price', 'description']
                data.name = name
                db.session.commit()
                data = {}
                for data in package_data:
                    data = {
                        'id': data.id,
                        'name': data.name,
                        'price': data.price,
                        'description': data.description
                    }
                response = jsonify(data)
                response.status_code = 201
                return response
            except KeyError: 
                response = jsonify({'error': 'Please use name for dict keys.'})
                response.status_code = 500
                return response
